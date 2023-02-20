import win32com.client as win32
import fillpdf
from fillpdf import fillpdfs
import string

class EmailHandler:
    """ This class is responsible for interfacing with Outlook in creating email envelopes to send.  Once called,  data is gathered from the Presenter and applied to an email envelope,  then once complete,  it is sent out.
    NOTE: This will be looped through for each envelope every button press.
    NOTE: If a PDF value changes,  please update the instance vars.
    """

    def __init__(self) -> None:
        self.outlook = win32.Dispatch(self.application)
        self.application = 'outlook.application'
        self.fname_pdf_key = '4669727374204e616d65'
        self.lname_pdf_key = '4c617374204e616d65'
        self.year_pdf_key = 'Year'
        self.make_pdf_key = '4d616b6520616e64204d6f64656c'
        self.length_pdf_key = 'Length'
        self.greeting = str
        self.body = str
        self.extra_notes = str
        self.salutation = str
        self.username = str

    def create_envelope(self) -> None:
        """ This creates the envelope,  which absorbs all final data to be sent to the desired recipient.
        """
        self.envelope = self.outlook.CreateItem(0)

    def assign_recipient(self, recipient: str) -> None:
        self.envelope.To = recipient

    def assign_CC(self, cc_addresses: str) -> None:
        self.envelope.CC = cc_addresses

    def assign_subject(self, subject: str) -> None:
        self.envelope.Subject = subject

    def assign_body_text(self, body: str) -> None:
        self.envelope.HTMLBody = body

    def assign_attachments(self, attachments: str) -> None:
        self.envelope.Attachments.Add(attachments)

    def send_envelope(self) -> None:
        try:
            self.envelope.Display()
            # self.envelope.Send()
        except:
            error_msg = f"Failed to send envelope to {self.envelope.To}."
            raise Exception(error_msg)
        else:
            print('Sent message successfully.')
        finally:
            print('Moving on to the next envelope...')

    def build_HTML_body(self) -> str:
        body_text = '''
    <html><head>
    <title>New Quote Submission</title>
    <meta http-equiv='Content-Type' content='text/html; charset=windows-1252'>
    <meta name='ProgId' content='Word.Document'>
    <meta name='Generator' content='Microsoft Word 15'>
    <meta name='Originator' content='Microsoft Word 15'>
    </head>
    <body>
    <p style='font-size=14px;color:#1F3864'>%s</p>
    <p style='font-size=14px;color:#1F3864'>%s %s</p><br>
    </body>
    <footer>
    <p style='margin:0in;font-size:14px;font-family:Calibri,sans-serif;color:#1F3864;'>%s</p>
    <p style='margin:0in;font-size=14px;font-family:Calibri,sans-serif;color:#1F3864;'>%s</p><br>
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
    </footer></html>
    ''' %(self.greeting, self.body, self.extra_notes, self.salutation, self.username)
        return body_text

    def build_subject(self, pdf_path) -> str:
        pdf_dict = dict(fillpdfs.get_form_fields(pdf_path))
        needed_values_dict = self.select_fields_from_pdf(pdf_dict)
        formatted_values_dict = self.assign_subject_values(needed_values_dict)
        return self.stringify_subject(formatted_values_dict)

    def select_fields_from_pdf(self, pdf_fields_dict: dict) -> dict:
        needed_field_values = {key: pdf_fields_dict[key] for key in pdf_fields_dict.keys()
        & {self.fname_pdf_key,self.lname_pdf_key, self.year_pdf_key, self.make_pdf_key, self.length_pdf_key}}
        return needed_field_values

    def format_subject_values(self, raw_dict = dict) -> None:
        """ This first formats each piece of the subject line,  then inserts those formatted values into a dict.
        """
        formatted_values_dict = {}
        
        first_name = raw_dict.get(self.fname_pdf_key)
        last_name = raw_dict.get(self.lname_pdf_key)
        year = raw_dict.get(self.year_pdf_key)
        make = raw_dict.get(self.make_pdf_key)
        length = raw_dict.get(self.length_pdf_key)
                
        first_name = self.capitalize_words(first_name)
        last_name = self.str_to_uppercase(last_name)
        make = self.capitalize_words(make)
        
        formatted_values_dict.update('first_name', first_name)
        formatted_values_dict.update('last_name', last_name)
        formatted_values_dict.update('year', year)
        formatted_values_dict.update('make', make)
        return formatted_values_dict

    def stringify_subject(self, formatted_values: dict) -> str:
        fv = dict(formatted_values)
        subject_line = f"{fv.get('last_name')}, {fv.get('first_name')} | {fv.get('year')} {fv.get('make')} {fv.get('length')} | New Quote Submission"
        return subject_line






    def capitalize_words(self, unformatted_string: str) -> str:
        return string.capwords(unformatted_string, sep=None)

    def str_to_uppercase(self, unformatted_string: str) -> str:
        return unformatted_string.upper()





















