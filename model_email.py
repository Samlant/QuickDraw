import win32com.client as win32
import fillpdf
from fillpdf import fillpdfs
import string


class EmailHandler:
    """This class is responsible for interfacing with Outlook in creating
    email letters to send.  Once called,  data is gathered from the Presenter
    and applied to an email letter,  then once complete,  it is sent out.
    NOTE: If a PDF value changes,  please update the instance vars.
    """

    def __init__(self):
        self.outlook = win32.Dispatch("Outlook.Application")
        self.keys_dict = {
            "fname": "4669727374204e616d65",
            "lname": "4c617374204e616d65",
            "year": "Year",
            "make": "4d616b6520616e64204d6f64656c",
            "length": "Length",
        }

    def create_letter(self) -> None:
        """This creates the letter,  which absorbs all final data to be sent to the desired recipient."""
        return self.outlook.CreateItem(0)

    # we can directly access = [To, CC, Subject, HTMLBody, Attachment]
    # Build html body first, then base off the necessary vars*)

    def send_letter(self, view: bool) -> None:
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
        body_text = self._organize_HTML_body(
            greeting=greeting,
            body=body,
            extra_notes=extra_notes,
            salutation=salutation,
            username=username,
        )
        return body_text

    def _organize_HTML_body(
        self, greeting: str, body: str, extra_notes: str, salutation: str, username: str
    ) -> str:
        greeting_style = "font-size=14px;color:#1F3864"
        body_style = "font-size=14px;color:#1F3864"
        salutation_style = (
            "margin:0in;font-size:14px;font-family:Calibri,sans-serif;color:#1F3864;"
        )
        username_style = (
            "margin:0in;font-size=14px;font-family:Calibri,sans-serif;color:#1F3864;"
        )
        signature = """
    <img src='https://i.postimg.cc/Mp00s0vJ/mysig.png'>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>NOVAMAR INSURANCE GROUP</p>
    <img src='https://i.postimg.cc/dVzMBYkx/novamarlogo.png'>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Main:(800)-823-2798</p>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Office :(941)-444-5099</p>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Fax:(941)-328-3598</p><br>
    <p style='margin:0in;color:#0563C1;text-decoration:underline;text-underline:single;font-size:12px;font-family:Georgia Pro,serif;'>1549 Ringling Blvd., Suite 101</p>
    <p style='margin:0in;color:#0563C1;text-decoration:underline;text-underline:single;font-size:12px;font-family:Georgia Pro,serif;'>Sarasota, FL 34236</p><br>
    <p style='margin:0in;color:#1F3864;font-size:10.0pt;font-family:Georgia Pro,serif;color:blue;'><a href='http://www.novamarinsurance.com/' target='_blank'>www.novamarinsurance.com</a></p>
    <p style='margin:0in;color:#1F3864;font-size:10.0pt;font-family:Georgia Pro,serif;color:blue;'><a href='http://www.novamarinsurance.com.mx/' target='_blank'>www.novamarinsurance.com.mx</a></p>

    <p style'margin:0in'><a href='https://www.facebook.com/NovamarInsurance' target='_blank'><img width=24 height=24 src='https://cdn1.iconfinder.com/data/icons/social-media-2285/512/Colored_Facebook3_svg-512.png'></a>  <a href='https://www.instagram.com/novamar_insurance/' target='_blank'><img width=24 height=24 src='https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Instagram_colored_svg_1-512.png' style='display:block'></a>  <a href='https://twitter.com/NovamarIns' target='_blank'><img width=24 height=24 src='https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Twitter3_colored_svg-512.png' style='display:block'></a>  <a href='https://www.linkedin.com/company/novamar-insurance-group-inc' target='_blank'><img width=24 height=24 src='https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Linkedin_unofficial_colored_svg-512.png' style='display:block'></a></p>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Established in 1987 with offices in: Seattle | Newport Beach | San Diego | Sarasota | Jacksonville | Puerto Vallarta | Cancun | San Miguel de Allende</p>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Please be advised that coverage is not bound, renewed, amended or in force unless confirmed in writing by a Novamar Insurance Group agent or by the represented company.</p>
    """
        body_text = """
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

    def build_subject(self, pdf_path: dict) -> str:
        if pdf_path != "":
            pdf_dict = self.get_pdf_input(pdf_path)
            pdf_dict = self.filter_pdf_input(pdf_dict)
            formatted_pdf_dict = self.stringify_subject(pdf_dict)
            return formatted_pdf_dict
        else:
            raise ValueError("Need Quoteform path!")

    def get_pdf_input(self, pdf_path) -> dict:
        """Gets all pdf input from the given file path

        Arguments:
            pdf_path -- expects a str of the file location of the pdf

        Returns:
            dict -- returns a dict of all form fields in the pdf
        """
        pdf_dict = fillpdfs.get_form_fields(pdf_path)
        return pdf_dict

    def filter_pdf_input(self, pdf_dict: dict) -> dict:
        """Gets & returns the pdf_fields' keys attributes as a dict

        Arguments:
            pdf_input_dict -- expects a dict containing at least the needed keys that are defined as attributes.

        Returns:
            dict -- returns a dict of the needed attributes as the key and their values from the pdf quoteform just parsed.
        """
        pdf_dict = {
            key: pdf_dict[key] for key in pdf_dict.keys() & self.keys_dict.values()
        }
        return pdf_dict

    def format_subject_values(self, pdf_dict=dict) -> None:
        """This first formats each piece of the subject line,  then inserts those formatted values into a dict."""
        formatted_values_dict = {}

        formatted_values_dict.update(
            "first_name", pdf_dict.get(self.keys_dict["fname"].self.capitalize_words)
        )
        formatted_values_dict.update(
            "last_name", pdf_dict.get(self.keys_dict["lname"].self.str_to_uppercase)
        )
        formatted_values_dict.update(
            "make", pdf_dict.get(self.keys_dict["make"].self.capitalize_words)
        )
        formatted_values_dict.update("year", pdf_dict.get(self.keys_dict["year"]))
        formatted_values_dict.update("length", pdf_dict.get(self.keys_dict["length"]))
        return formatted_values_dict

    def stringify_subject(self, formatted_values: dict) -> str:
        fv = formatted_values
        subject_line = f"""New Quote Submission | {fv[self.keys_dict['lname']]}, {fv[self.keys_dict['fname']]} | {fv[self.keys_dict['year']]} {fv[self.keys_dict['make']]} {fv[self.keys_dict['length']]}
                        """
        return subject_line

    def capitalize_words(self, unformatted_string: str) -> str:
        return string.capwords(unformatted_string, sep=None)

    def str_to_uppercase(self, unformatted_string: str) -> str:
        return unformatted_string.upper()