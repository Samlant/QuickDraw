import string

import win32com.client as win32


class EmailHandler:
    """This class is responsible for interfacing with Outlook in creating
    email letters to send.  Once called,  data is gathered from the Presenter
    and applied to an email letter,  then once complete,  it is sent out.
    NOTE: If a PDF value changes, update the instance vars.
    """

    def __init__(self) -> None:
        self.outlook = win32.Dispatch("Outlook.Application")
        self.letter = self.outlook.CreateItem(0)

    def create_letter(self) -> None:
        """This creates the letter,  which absorbs all final data to be sent to the desired recipient."""
        self.letter.Subject = str

    def assign_content_to_letter(
        self,
        subject: str,
        formatted_cc_str: str,
        extra_notes: str,
        username: str,
        carrier_config_dict: dict,
        attachments_list: list,
    ):
        "Assigns all content to the letter prior to sending"
        self.letter.Subject = subject
        self.letter.CC = formatted_cc_str
        self.letter.To = carrier_config_dict.pop("address")
        self.letter.HTMLBody = self.build__HTML_Body(
            carrier_config_dict,
            extra_notes,
            username,
        )
        for attachment_path in attachments_list:
            self.letter.Attachments.Add(attachment_path)

    def send_letter(self) -> None:
        """Wrapper for sending the message for unit-testing"""
        try:
            self.letter.Send()
        except:
            raise Exception("Couldn't send letter, check email_handler")
        else:
            return True

    def view_letter(self) -> bool:
        """Wrapper for displaying the message for unit-testing"""
        try:
            self.letter.Display()
        except:
            raise Exception("Couldn't display letter, check email_hanletter")
        else:
            return True

    def build__HTML_Body(
        self, carrier_config_dict: dict, extra_notes: str, username: str
    ) -> str:
        greeting = carrier_config_dict.pop("greeting")
        body = carrier_config_dict.pop("body")
        extra_notes = extra_notes
        salutation = carrier_config_dict.pop("salutation")
        username = username
        signature_image = carrier_config_dict.pop("signature_image")
        body_text = self._organize_HTML_body(
            greeting=greeting,
            body=body,
            extra_notes=extra_notes,
            salutation=salutation,
            username=username,
            signature_image=signature_image,
        )
        return body_text

    def _organize_HTML_body(
        self,
        greeting: str,
        body: str,
        extra_notes: str,
        salutation: str,
        username: str,
        signature_image: str,
    ) -> str:
        greeting_style = "font-size=14px;color:#1F3864;"
        body_style = "font-size=14px;color:#1F3864;"
        salutation_style = (
            "margin:0in;font-size:14px;font-family:Calibri,sans-serif;color:#1F3864;"
        )
        username_style = (
            "margin:0in;font-size=14px;font-family:Calibri,sans-serif;color:#1F3864;"
        )
        signature = r"""
    <img src='%s'>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>NOVAMAR INSURANCE GROUP</p>
    <img src='https://i.postimg.cc/yWCHTYjJ/novamar.png'>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Main:(800)-823-2798</p>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Office :(941)-444-5099</p>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Fax:(941)-328-3598</p><br>
    <p style='margin:0in;color:#0563C1;text-decoration:underline;text-underline:single;font-size:12px;font-family:Georgia Pro,serif;'>1549 Ringling Blvd., Suite 101</p>
    <p style='margin:0in;color:#0563C1;text-decoration:underline;text-underline:single;font-size:12px;font-family:Georgia Pro,serif;'>Sarasota, FL 34236</p><br>
    <p style='margin:0in;color:#1F3864;font-size:10.0pt;font-family:Georgia Pro,serif;color:blue;'><a href='http://www.novamarinsurance.com/' target='_blank'>www.novamarinsurance.com</a></p>
    <p style='margin:0in;color:#1F3864;font-size:10.0pt;font-family:Georgia Pro,serif;color:blue;'><a href='http://www.novamarinsurance.com.mx/' target='_blank'>www.novamarinsurance.com.mx</a></p>

    <p style='margin:0in;'><a href='https://www.facebook.com/NovamarInsurance' target='_blank'><img width=24 height=24 src='https://cdn1.iconfinder.com/data/icons/social-media-2285/512/Colored_Facebook3_svg-512.png'></a>  <a href='https://www.instagram.com/novamar_insurance/' target='_blank'><img width=24 height=24 src='https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Instagram_colored_svg_1-512.png' style='display:block'></a>  <a href='https://twitter.com/NovamarIns' target='_blank'><img width=24 height=24 src='https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Twitter3_colored_svg-512.png' style='display:block'></a>  <a href='https://www.linkedin.com/company/novamar-insurance-group-inc' target='_blank'><img width=24 height=24 src='https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Linkedin_unofficial_colored_svg-512.png' style='display:block'></a></p>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Established in 1987 with offices in: Seattle | Newport Beach | San Diego | Sarasota | Jacksonville | Puerto Vallarta | Cancun | San Miguel de Allende</p>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Please be advised that coverage is not bound, renewed, amended or in force unless confirmed in writing by a Novamar Insurance Group agent or by the represented company.</p>
    """ % (
            signature_image,
        )
        body_text = r"""
    <html><head>
    <title>New Quote Submission</title>
    <meta http-equiv='Content-Type' content='text/html; charset=windows-1252'>
    <meta name='ProgId' content='Word.Document'>
    <meta name='Generator' content='Microsoft Word 15'>
    <meta name='Originator' content='Microsoft Word 15'>
    </head>
    <body>
    <p style=%s>%s</p>
    <p style=%s>%s %s</p>
    </body>
    <footer>
    <p style=%s>%s</p>
    <p style=%s>%s</p>
    %s
    </footer></html>
    """ % (
            greeting_style,
            greeting,
            body_style,
            body,
            extra_notes,
            salutation_style,
            salutation,
            username_style,
            username,
            signature,
        )
        return body_text

    def stringify_subject(self, fname, lname, vessel_year, vessel) -> str:
        subject_line = f"New Quote Submission from Novamar | {lname}, {fname} | {vessel_year} {vessel}"
        return subject_line

    def capitalize_words(self, unformatted_string: str) -> str:
        return string.capwords(unformatted_string, sep=None)

    def str_to_uppercase(self, unformatted_string: str) -> str:
        return unformatted_string.upper()
