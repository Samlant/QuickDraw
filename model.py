from configupdater import ConfigUpdater
import win32com.client as win32
import fillpdf
from fillpdf import fillpdfs
import string


class Model:
    """This is our model which handles validating, transforming, moving and storing data appropriately.
    NOTE: any config interactions are routed to the Config class object.
    """

    # NOTE: change this LAST:  These are class vars bc we want to keep them until emails are sent...store in email obj not here.

    def __init__(self, positive_value, negative_value, pdf_path: dict) -> None:
        self.yes = positive_value
        self.no = negative_value
        self.quoteform_path = ""
        self.extra_attachments = []
        if not pdf_path == {}:
            self.save_path(pdf_path, True)

    def get_dropdown_options(self) -> list:
        return [
            "Seawave",
            "Prime Time",
            "New Hampshire",
            "American Modern",
            "Kemah Marine",
            "Concept Special Risks",
            "Yachtinsure",
            "Century",
            "Intact",
            "Travelers",
            "Combination: Seawave + Prime Time + New Hampshire",
            "Combination: Prime Time + New Hampshire",
            "Combination: Seawave + New Hampshire",
            "Combination: Seawave + Prime Time",
        ]

    def filter_only_positive_submissions(self, raw_checkboxes: dict) -> list:
        checkboxes_dict = raw_checkboxes.copy()
        for x in raw_checkboxes:
            if raw_checkboxes[x] == self.no:
                checkboxes_dict.pop(x)
            elif raw_checkboxes[x] == self.yes:
                pass
            else:
                raise ValueError
        checkboxes_list = []
        for x in checkboxes_dict.keys():
            checkboxes_list.append(x)
        return checkboxes_list

    def handle_redundancies(self, filtered_submits: list) -> str:
        """Checks if multiple redundant markets are present,  then combines them & returns the appropriate config section name"""
        if self._redundancy_check(filtered_submits):
            section_name = str(self._fix_redundancies(filtered_submits))
            return section_name
        else:
            if len(filtered_submits) == 0:
                pass
            else:
                return filtered_submits[0]

    def _redundancy_check(self, filtered_submits: list) -> bool:
        """Counts the number of items in the dictionary supplied. NOTE: the dict input should already be filtered and be a positive submission."""
        if len(filtered_submits) > 1:
            return True
        elif len(filtered_submits) <= 1:
            return False
        else:
            raise ValueError()

    def _fix_redundancies(self, positive_redundants: list) -> str:  # GOOD
        """Receives a dict of the name of the carrier as a key,  and the
        positive submission value as the"""
        redundancies = positive_redundants
        section_name = self._assign_redundant_section(redundancies)
        return section_name

    def _assign_redundant_section(self, redundancies: list[str]):
        string = " + ".join(redundancies)
        section_name = f"Combination: {string}"
        return section_name

    def save_path(self, path, is_quoteform: bool) -> None:
        if is_quoteform == True:
            self.quoteform_path = path
        elif is_quoteform == False:
            self.extra_attachments.append(path)
        else:
            raise Exception("Type of param:is_quoteform is wrong or empty.")

    def filter_out_brackets(self, path) -> str:
        """Cleans up the path str by removing any brackets---if present."""
        if "{" in path:
            path = path.translate({ord(c): None for c in "{}"})
        return path

    def get_all_attachments(self) -> list:
        attachments = []
        attachments.append(self.quoteform_path)
        if len(self.extra_attachments) >= 1:
            for attachment in self.extra_attachments:
                attachments.append(attachment)
        else:
            return attachments
        return attachments

    def list_of_CC_to_str(self, input_list: list) -> str:
        """Transforms lists into strings. In-use for CC_address assignment."""
        input_list = "; ".join(str(element) for element in input_list)
        return input_list

    def get_default_cc_addresses(self):
        list_of_CC = list()
        if self.check_if_ignore_default_cc_is_on() == False:
            default_cc1 = ConfigWorker.get_value(
                dict("General settings", "default_cc1")
            )
            default_cc2 = ConfigWorker.get_value(
                dict("General settings", "default_cc2")
            )
            list_of_CC.append(default_cc1, default_cc2)
            return list_of_CC
        else:
            return None


class EmailHandler:
    """This class is responsible for interfacing with Outlook in creating
    email letters to send.  Once called,  data is gathered from the Presenter
    and applied to an email letter,  then once complete,  it is sent out.
    NOTE: If a PDF value changes,  please update the instance vars.
    """

    def __init__(self):
        self.outlook = win32.Dispatch("Outlook.Application")
        self.keys_dict = {
            "fname": "fname",
            "lname": "lname",
            "year": "vessel_year",
            "make": "vessel_make_model",
        }

    def create_letter(self) -> None:
        """This creates the letter,  which absorbs all final data to be sent to the desired recipient."""
        self.letter = self.outlook.CreateItem(0)

    def assign_content_to_letter(
        self,
        subject,
        formatted_CC_str,
        extra_notes,
        username,
        carrier_config_dict,
        attachments_list,
    ):
        "Assigns all content to the letter prior to sending"
        self.letter.Subject = subject
        self.letter.CC = formatted_CC_str
        self.letter.To = carrier_config_dict.pop("address")
        self.letter.HTMLBody = self.build__HTML_Body(
            carrier_config_dict, extra_notes, username
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
        return formatted_values_dict

    def stringify_subject(self, formatted_values: dict) -> str:
        fv = formatted_values
        subject_line = f"""New Quote Submission from Novamar | {fv[self.keys_dict['lname']]}, {fv[self.keys_dict['fname']]} | {fv[self.keys_dict['year']]} {fv[self.keys_dict['make']]}'
        """
        return subject_line

    def capitalize_words(self, unformatted_string: str) -> str:
        return string.capwords(unformatted_string, sep=None)

    def str_to_uppercase(self, unformatted_string: str) -> str:
        return unformatted_string.upper()


class ConfigWorker:
    """This class handles all interactions between the python and config file. It utilizes open_config() as a helper to acces config, discerns the path of flowing information & then performs those queries on the config file."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def open_config(self) -> None:  # GOOD
        """This is a helper to read config when called using ConfigUpdater,  an improvement on configParser."""
        open_read_update = ConfigUpdater()
        open_read_update.read(self.file_path)
        return open_read_update

    def get_value(self, request: dict) -> any:
        """This returns the value from config given a section_name:key dict."""
        config = self.open_config()
        section_name = request["section_name"]
        key = request["key"]
        result = config.get(section_name, key).value
        return result

    def _validate_section(self, section_name) -> bool:  # GOOD
        """Validates a given section name to ensure its existence in config."""
        config = self.open_config()
        if config.has_section(section_name):
            return True
        else:
            print(
                "section_name validation failed within the ConfigWorker. Double-check input."
            )
            return False

    def get_section(self, section_name) -> dict:  # GOOD
        """This returns the section keys:values in a dict"""
        config = self.open_config()
        section = config.get_section(section_name)
        section = section.to_dict()
        return section

    def handle_save_contents(self, section_name: str, save_contents: dict) -> bool:
        """This is a generic function to save both Save buttons' data to the appropriate config section. It also ensures the section exists."""
        config = self.open_config()
        if self._validate_section(section_name):
            for option, value in save_contents.items():
                try:
                    config[section_name][option] = value
                except:
                    raise Exception("Couldn't assign save_contents dict to config file")
            try:
                config.update_file()
            except:
                raise Exception("Couldn't save file")

    def check_if_using_default_carboncopies(self) -> bool:
        section_name_value = "General settings"
        key = "use_default_cc_addresses"
        config = {"section_name": section_name_value, "key": key}
        try:
            result = self.get_value(config)
        except:
            raise KeyError("Couldn't access config with values")
        else:
            return result
