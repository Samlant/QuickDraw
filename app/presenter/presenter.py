from dataclasses import dataclass
from pathlib import Path
import ctypes
from typing import Protocol
import threading
from tkinter import TclError
from ast import literal_eval


class API(Protocol):
    def create_excel_json(self, data) -> dict[str, any]:
        ...


class BaseModel(Protocol):
    def save_path(
        self,
        path,
        is_quoteform: bool,
    ) -> None:
        ...

    def get_dropdown_options(self) -> list:
        ...

    def filter_only_positive_submissions(
        self,
        raw_checkboxes: dict,
    ) -> list:
        ...

    def handle_redundancies(
        self,
        filtered_submits: list,
    ) -> str:
        ...

    def filter_out_brackets(
        self,
        path,
    ) -> str:
        ...

    def get_all_attachments(self) -> list:
        ...


class ConfigWorker(Protocol):

    def get(
            self,
            section_name: str,
            option: str,
    ):
        ...
    def get_value(
        self,
        request: dict,
    ) -> str:
        ...

    def get_section(
        self,
        section_name,
    ) -> dict:
        ...

    def handle_save_contents(
        self,
        section_name: str,
        save_contents: dict,
    ) -> bool:
        ...

    def check_if_using_default_carboncopies(self) -> bool:
        ...
    def set_multi_line_values_for_option(
            self,
            section_name,
            option_name,
            values,):
        ...


class DialogNewFile(Protocol):
    def initialize(
        self,
        presenter,
        submission_info,
    ) -> str:
        ...


class DialogAllocateMarkets(Protocol):
    def initialize(self, presenter) -> str:
        ...


class Dirhandler(Protocol):
    def create_dirs(
        self,
        submission_info,
    ) -> Path:
        ...

    def move_file(
        self,
        client_dir: Path,
        orgin_file: Path,
    ) -> Path:
        ...


class DirWatch(Protocol):
    def begin_watch(self) -> None:
        ...


class DocParser(Protocol):
    def __init__(self) -> None:
        self.keys: dict[str, str]

    def process_doc(
        self,
        file_path: Path,
    ) -> dict:
        ...


class EmailHandler(Protocol):
    subject: str
    cc: str
    to: str
    body: str
    extra_notes: str
    username: str
    img_sig_url: str
    attachments_list: str

    def view_letter(self) -> bool:
        raise NotImplementedError

    def stringify_subject(self, formatted_values: dict[str, str]) -> str:
        ...


class MSGraphClient(Protocol):
    def run_excel_program(self, json_payload: dict) -> None:
        ...

    def client_already_exists(self) -> bool:
        ...

    def add_row(self) -> None:
        ...

    def close_workbook_session(self) -> None:
        ...

    def send_message(self, message) -> None:
        ...


class Submission(Protocol):
    extra_notes: str
    use_default_cc_addresses: bool
    sw: str | int | bool | list
    pt: str | int | bool | list
    nh: str | int | bool | list
    am: str | int | bool | list
    km: str | int | bool | list
    cp: str | int | bool | list
    yi: str | int | bool | list
    ce: str | int | bool | list
    In: str | int | bool | list
    tv: str | int | bool | list
    quoteform: str
    extra_attachments: str
    selected_template: str
    address: str
    greeting: str
    body: str
    salutation: str
    default_cc1: str
    default_cc2: str
    username: str
    sig_image_file: str
    watch_dir: str
    new_biz_dir: str
    renewals_dir: str
    custom_parent_dir: str
    tree: any

    def reset_attributes(
        self,
        positive_value,
        negative_value,
    ):
        ...

    def create_UI_obj(
        self,
        presenter,
    ) -> None:
        ...

    def set_start_tab(self) -> None:
        ...

    def mainloop(self) -> None:
        ...

    def get_active_focus(
        self,
        event,
    ):
        ...

    def focus_get(self):
        ...

    def get_template_page_values(self) -> dict:
        ...

    def get_all_rows(self) -> list[str]:
        ...

    def set_data_into_treeview(self, data: list[str]):
        ...


@dataclass
class ClientInfo:
    fname: str
    lname: str
    vessel: str
    vessel_year: int
    referral: str
    status: str
    original_file_path: Path
    new_file_path: Path = None
    extra_attachements: list = None
    markets: list | str = ""
    submit_tool: bool = False


class Presenter:
    """Responsible for communicating between the Models and
    Views, including all interactions between user input and
    program logic.

    Attributes:

        Models:
            api_client: establishes connection with MS Graph for excel functionality.
            base_model: standard calculations, string formatting;
            config_worker: config file operations;
            dir_watch: detects when a new file is created within the watched folder;
            email_handler: creates and organizes emails;

        Views:
            submission: creates the submission window/settings;
            dialog_new_file: creates dialog when dir_watch is triggered;
            dialog_allocate_markets: creates dialog when user allocates
            markets for client;
            tray_icon: interactive icon that shows in system tray area;
    """

    def __init__(
        self,
        api_client: MSGraphClient,
        api_model: API,
        base_model: BaseModel,
        config_worker: ConfigWorker,
        dir_handler: Dirhandler,
        dir_watch: DirWatch,
        email_handler: EmailHandler,
        pdf: DocParser,
        submission: Submission,
        dialog_new_file: DialogNewFile,
        dialog_allocate_markets: DialogAllocateMarkets,
    ) -> None:
        # Models
        self.api_client = api_client
        self.api_model = api_model
        self.base_model = base_model
        self.config_worker = config_worker
        self.dir_handler = dir_handler
        self.dir_watch = dir_watch
        self.email_handler = email_handler
        self.pdf = pdf
        self.submission = submission
        self.dialog_new_file = dialog_new_file
        self.dialog_allocate_markets = dialog_allocate_markets
        self.current_submission = None
        self.only_view_msg: bool = None
        self.run_flag: bool = False
        self.run_email_settings_flag: bool = False
        self.run_folder_settings_flag: bool = False

    def setup_api(self) -> bool:
        graph_values = self.config_worker.get_section("graph_api")
        if not self.api_client.setup_api(connection_data=graph_values):
            return False
        if self.config_worker.has_value("graph_api", "user_id"):
            str_count = len(
                self.config_worker.get_value(
                    {
                        "section_name": "graph_api",
                        "key": "user_id",
                    }
                )
            )
            if str_count < 10:
                user_id = self.api_client.get_user_id()["id"]
                self.config_worker.handle_save_contents(
                    "graph_api",
                    save_contents={
                        "user_id": user_id,
                    },
                )
        return True

    def start_program(self):
        print(f"Watching for any new PDF files in: {str(self.dir_watch.path)}.")
        self.dir_watch.begin_watch()

    def _process_document(self, file: Path):
        print("Processing/Parsing PDF document.")
        try:
            values_dict = self.pdf.process_doc(file)
        except:
            ctypes.windll.user32.MessageBoxW(
                0,
                "Please exit out of the PDF file so that the program can delete the original file.",
                "Warning: Exit the PDF",
                1,
            )
            try:
                values_dict = self.pdf.process_doc(file)
            except:
                ctypes.windll.user32.MessageBoxW(
                    0,
                    "Please exit out of the PDF file so that the program can delete the original file.",
                    "Warning: Exit the PDF",
                    1,
                )
                values_dict = self.pdf.process_doc(file)
        self.current_submission = ClientInfo(
            fname=values_dict["fname"],
            lname=values_dict["lname"],
            vessel=values_dict["vessel"],
            vessel_year=values_dict["vessel_year"],
            referral=values_dict["referral"],
            status=values_dict["status"],
            original_file_path=values_dict["original_file_path"],
        )
        return True

    def trigger_new_file(self, file: Path):
        self._process_document(file=file)
        print("Detected new Quoteform")
        print(f"the current client is: {self.current_submission.__repr__}")
        next_month, second_month = self.api_model.get_future_two_months()
        self.dialog_new_file.initialize(
            presenter=self,
            submission_info=self.current_submission,
            current_month=self.api_model.get_current_month(),
            next_month=next_month,
            second_month=second_month,
        )
        self.dialog_new_file.root.attributes('-topmost', True)
        self.dialog_new_file.root.update()
        self.dialog_new_file.root.attributes('-topmost', False)
        self.dialog_new_file.root.mainloop()

    def start_allocate_dialog(self):
        # start dialog_allocate_markets
        print("Starting dialog to allocate markets.")
        self.dialog_allocate_markets.initialize(self)
        self.dialog_allocate_markets.root.attributes('-topmost', True)
        self.dialog_allocate_markets.root.update()
        self.dialog_allocate_markets.root.attributes('-topmost', False)
        self.dialog_allocate_markets.root.mainloop()
        

    def save_user_choices(self):
        print("Saving choices")
        all_options = self.dialog_allocate_markets.get_markets()
        self.current_submission = self.base_model.process_user_choice(
            all_options,
            self.current_submission,
        )

    def create_and_send_data_to_api(self):
        print("creating call to send to Microsoft API")
        json = self.api_model.create_excel_json(self.current_submission)
        self.api_client.run_excel_program(
            json_payload=json,
        )

    def _send_excel_api_call(self):
        self.create_and_send_data_to_api()
        print("Adding excel row via API")
        if not self.api_client.client_already_exists():
            if self.excel_table_name:
                self.api_client.add_row(self.excel_table_name)
            else:
                self.api_client.add_row()
            self.api_client.close_workbook_session()
        else:
            print("Client already exists on tracker,  skipping adding to the tracker.")

    def choice(self, choice: str):
        section_obj = self.config_worker.get_section("Folder settings")
        client_dir = self.dir_handler.create_dirs(self.current_submission, section_obj)
        new_qf_path = self.dir_handler.move_file(
            client_dir,
            self.current_submission.original_file_path,
        )
        self.excel_table_name = self.dialog_new_file.selected_month
        self.dialog_new_file.root.destroy()
        if choice == "track_allocate":
            self.start_allocate_dialog()
            try:
                thread_xl = threading.Thread(
                    daemon=False,
                    target=self._send_excel_api_call,
                    name="Excel API Call",
                )
                thread_xl.start()
            except:
                thread_xl = threading.Thread(
                    daemon=False,
                    target=self._send_excel_api_call,
                    name="Excel API Call",
                )
                thread_xl.start()
        elif choice == "track_submit":
            self.start_submission_program(quote_path=new_qf_path)
            print("Submission emailed to markets.")
        else:
            try:
                thread_xl = threading.Thread(
                    daemon=True, target=self._send_excel_api_call, name="Excel API Call"
                )
                thread_xl.start()
            except:
                thread_xl = threading.Thread(
                    daemon=True, target=self._send_excel_api_call, name="Excel API Call"
                )
                thread_xl.start()

    ############# Start Submissions Program #############
    def start_submission_program(self, specific_tab: str | None = None, quote_path: str = None) -> None:  # type: ignore
        """Starts the program by creating GUI object,
        configuring initial values,  then running it
        This also sets the default mail application.
        """
        print("starting email submission program")
        self.submission.create_UI_obj(self)
        if quote_path:
            self.set_initial_placeholders(quote_path)
        else:
            self.set_initial_placeholders()
        if specific_tab:
            self.submission.set_start_tab(specific_tab)
        self.submission.root.attributes('-topmost', True)
        self.submission.root.update()
        self.submission.root.attributes('-topmost', False)
        self.submission.root.mainloop()

    def set_dropdown_options(self) -> list:
        "Submission (View) calls this value upon creation."
        return self.base_model.get_dropdown_options()

    ############# Establish Main Tab #############

    def set_initial_placeholders(self, quote_path: str = None) -> None:
        """Sets initial texts for the main/home tab, if applicable"""
        self.btn_revert_folder_settings()
        personal_settings_keys: list[str] = [
            "username",
            "use_default_cc_addresses",
            "default_cc1",
            "default_cc2",
        ]
        for key in personal_settings_keys:
            new_value = self.config_worker.get_value(
                {"section_name": "General settings", "key": key}
            )
            self.submission.__setattr__(key, new_value)
        self._set_customize_tab_placeholders(
            self.config_worker.get_section("Initial placeholders")
        )

        if quote_path:
            self.process_quoteform_path(quote_path=quote_path)
        else:
            pass

    def process_quoteform_path(
        self, drag_n_drop_event=None, quote_path: str = None
    ) -> None:  # GOOD
        """Sends the raw path to model for proccessing & saving.

        Arguments:
            raw_path {str} -- the raw str of full path of the file

        Returns:
            Tuple -- returns the path & a boolean for distinguishing
                          it apart from other attachments.
        """
        print("processing quoteform for email msg")
        if quote_path:
            path = quote_path
        else:
            raw_path: str = drag_n_drop_event.data
            path = self.base_model.filter_out_brackets(raw_path)
        del self.submission.quoteform
        self.submission.quoteform = Path(path).name
        return self.base_model.save_path(path, is_quoteform=True)

    def process_attachments_path(self, drag_n_drop_event) -> None:
        """Sends the raw path of all extra attachments (not the
                quoteform) to model for proccessing & saving.

        Arguments:
            raw_path {str} -- the raw str of full path of the file

        Returns:
            Tuple -- returns the path & a boolean for distinguishing
                          it apart from the client's quoteform.
        """
        print("processing additional attachments")
        raw_path: str = drag_n_drop_event.data
        path = self.base_model.filter_out_brackets(raw_path)
        self.submission.extra_attachments = Path(path).name
        return self.base_model.save_path(path, is_quoteform=False)

    def process_signature_image_path(self, drag_n_drop_event) -> None:
        """Saves the signature image file onto the Settings page, but
        does not save it to the config file yet;  the Save button writes
        this to the config file.

        Arguments:
            raw_path {str} -- the raw str of full path of the file
        """
        print("saving signature image")
        raw_path: str = drag_n_drop_event.data
        path = self.base_model.filter_out_brackets(raw_path)
        self.submission.sig_image_file = path

    ############# END --Main Tab-- END #############

    ############# Establish Main Actions #############

    def btn_clear_attachments(self) -> None:
        print("cleared attachments from QuickDraw")
        self.base_model.extra_attachments: list = []
        self.base_model.quoteform_path: str = ""
        del self.submission.quoteform
        del self.submission.extra_attachments

    def btn_view_template(self) -> None:
        print(
            "Sorry,  viewing is not yet implemented.  Try sending a message to yourself using the settings tab to assign your email address, then try again."
        )
        self.only_view_msg = True
        raise NotImplementedError

    def btn_send_envelopes(self) -> None:
        print("clicked send button")
        self.only_view_msg = False
        self._process_document(self.base_model.quoteform_path)
        self.current_submission.markets = self.gather_active_markets()
        self.current_submission.submit_tool = True
        self.loop_through_envelopes()

    ############# END --Main Actions-- END #############

    ############# Sending Envelope #############

    def gather_active_markets(self) -> list:
        """This gets the markets that the user chose. Also checks
        for and handles any duplicate email address.

        Returns: list of market names to submit to.

        Arguments (outdated):
                autosend = {bool}
                NOTE: If True, no window will be shown and all emails
                will be sequentially sent. If False, a window will be shown for
                each email prior to sending.
        """
        print("Gathering single markets and redundant markets")
        submission_list = self._handle_single_markets()
        redundant_result = self._handle_redundancies()
        if redundant_result is not None:
            submission_list.append(redundant_result)
        else:
            pass
        return submission_list

    def _handle_single_markets(self) -> list:
        """Gets possible redundant carriers' checkbox values, filters to only keep
        positive submissions, then combines them into one submission

        Returns -- Dict: returns dict of a single, combined carrier submission
        """
        try:
            raw_dict = self.get_single_carriers()
            processed_list = self.base_model.filter_only_positive_submissions(raw_dict)
        except:
            raise Exception("Failed getting or filtering the single markets.")
        else:
            return processed_list

    def _handle_redundancies(self) -> str:
        """Gets possible redundant carriers' checkbox values, filters to only keep
        positive submissions, then combines them into one submission

        Returns -- Dict: returns dict of a single, combined carrier submission
        """
        raw_dict: dict[str, any] = self._get_possible_redundancies()
        filtered_list = self.base_model.filter_only_positive_submissions(raw_dict)
        processed_str = self.base_model.handle_redundancies(filtered_list)
        return processed_str

    def get_single_carriers(self) -> dict:
        """This gets the values of the carriers' checkboxes that
        all submit to different, unique email addresses.

        Returns:
                Dict -- returns a dict of carrier checkbox values
        """
        carrier_submissions_dict = dict()
        try:
            carrier_submissions_dict = {
                "American Modern": self.submission.am,
                "Kemah Marine": self.submission.km,
                "Concept Special Risks": self.submission.cp,
                "Yachtinsure": self.submission.yi,
                "Century": self.submission.ce,
                "Intact": self.submission.In,
                "Travelers": self.submission.tv,
            }
        except:
            raise Exception("Couldn't get carrier checkboxes saved into a dict.")
        else:
            return carrier_submissions_dict

    def _get_possible_redundancies(self) -> dict[str, str | int | bool | list]:
        """This gets the values of the carriers' checkboxes that submit
        to the same email address. Separating this allows us to more
        easily update the list of likely redundancies.

        Returns:
                Dict -- returns a dict of carrier checkbox values
        """
        possible_redundancies_dict: dict(str, str | int | bool | list)
        try:
            possible_redundancies_dict = {
                "Seawave": self.submission.sw,
                "Prime Time": self.submission.pt,
                "New hampshire": self.submission.nh,
            }
        except:
            raise Exception("Couldn't get carrier checkboxes saved into a dict.")
        else:
            return possible_redundancies_dict

    def loop_through_envelopes(self):
        """This loops through each submission;  it:
        (1) forms an envelope when a positive_submission is found,
        (2) gets and transforms needed data into each of its final
        formatted type and form,
        (3) applies the properly formatted data into each the envelope, and,
        (4) sends the envelope to the recipient, inclusive of all data.
        """
        print("looping through envelopes for all carriers selected")
        self.email_handler.subject = self.email_handler.stringify_subject(
            self.current_submission,
        )

        unformatted_cc = self._handle_getting_CC_addresses()
        self.email_handler.cc = self.base_model.format_cc_for_api(
            unformatted_cc,
        )
        self.email_handler.extra_notes = self.submission.extra_notes
        self.email_handler.username = self.config_worker.get_value(
            {
                "section_name": "General settings",
                "key": "username",
            }
        )

        attachments = self.base_model.get_all_attachments()
        self.email_handler.attachments_list = self.api_model.create_attachments_json(
            attachment_paths=attachments
        )

        self.email_handler.img_sig_url = self.config_worker.get_value(
            {
                "section_name": "General settings",
                "key": "signature_image",
            }
        )
        for carrier in self.current_submission.markets:
            carrier_section = self.config_worker.get_section(carrier)
            unformatted_to = carrier_section.get("address").value
            self.email_handler.to = self.base_model.format_to_for_api(unformatted_to)
            signature_settings = self.get_signature_settings()
            self.email_handler.body = self.email_handler.make_msg(
                carrier_section,
                signature_settings,
            )

            self.json = self.api_model.create_email_json(email=self.email_handler)
            print("sending email message")
        try:
            thread_ol = threading.Thread(
                daemon=False, target=self.send_email_api, name="Outlook API Call"
            )
            thread_ol.start()
        except:
            thread_ol = threading.Thread(
                daemon=False, target=self.send_email_api, name="Outlook API Call"
            )
            thread_ol.start()
        try:
            thread_xl = threading.Thread(
                daemon=False, target=self._send_excel_api_call, name="Excel API Call"
            )
            thread_xl.start()
        except:
            thread_xl = threading.Thread(
                daemon=False, target=self._send_excel_api_call, name="Excel API Call"
            )
            thread_xl.start()

    def send_email_api(self):
        self.api_client.send_message(message=self.json)

    def get_signature_settings(self) -> dict[str, str]:
        print("Getting signature settings")
        office_phone = self.config_worker.get_value(
            {"section_name": "Signature settings", "key": "office_phone"}
        )
        office_street = self.config_worker.get_value(
            {"section_name": "Signature settings", "key": "office_street"}
        )
        office_city_st_zip = self.config_worker.get_value(
            {"section_name": "Signature settings", "key": "office_city_st_zip"}
        )

        return {
            "office_phone": office_phone,
            "office_street": office_street,
            "office_city_st_zip": office_city_st_zip,
        }

    def _handle_getting_CC_addresses(self) -> list:
        """Gets userinput of all CC addresses and adds the to a list. It then
        checks if it should ignore the default CC addresses set in config file
        or add them intothe list as well

        Returns:
                List -- returns a list of all desired CC adresses
        """
        list_of_cc = [self.submission.userinput_CC1, self.submission.userinput_CC2]
        if self.submission.use_default_cc_addresses:
            if self.config_worker.check_if_using_default_carboncopies():
                cc_from_config = [
                    self.config_worker.get_value(
                        {
                            "section_name": "General settings",
                            "key": "default_cc1",
                        }
                    ),
                    self.config_worker.get_value(
                        {
                            "section_name": "General settings",
                            "key": "default_cc2",
                        }
                    ),
                ]
                list_of_cc = list_of_cc + cc_from_config
        return list_of_cc

    ############# END --Sending Envelopes-- END #############

    ############# Establish Custimze Tab #############

    def _set_customize_tab_placeholders(self, section_obj) -> None:
        """Sets the placeholders for the customizations_tab"""

        self.submission.address = section_obj.get("address").value
        self.submission.greeting = section_obj.get("greeting").value
        del self.submission.body
        self.submission.body = section_obj.get("body").value
        self.submission.salutation = section_obj.get("salutation").value

    def _get_customize_tab_placeholders(self):
        current_selection = self.submission.selected_template
        return self.config_worker.get_section(current_selection)

    # Complete if necessary - 02.09.2023
    def on_change_template(self, *args, **kwargs) -> None:
        """Updates the placeholders on customize_tab when dropdown changes

        Returns:
                Bool -- returns a bool for success & for testing
        """
        selected_template = self.submission.selected_template
        placeholders_dict = self.config_worker.get_section(selected_template)
        self._set_customize_tab_placeholders(placeholders_dict)

    def on_focus_out(self, event) -> bool | None:
        carrier = self.submission.selected_template
        widget_name = event.widget.winfo_name()
        widget_type = event.widget.widgetName

        if carrier == "Select Market(s)":
            return True
        else:
            if widget_type == "text" and self.check_text_from_textbox(event):
                if widget_name == "body":
                    del self.submission.body
                self.assign_placeholder_on_focus_out(carrier, widget_name)
            elif widget_type == "entry" and self.check_text_from_entrybox(event):
                self.assign_placeholder_on_focus_out(carrier, widget_name)
            else:
                pass

    def check_text_from_textbox(self, event) -> bool | None:
        if event.widget.get("1.0", "end-1c") == "":
            return True

    def check_text_from_entrybox(self, event) -> bool | None:
        if event.widget.get() == "":
            return True

    def assign_placeholder_on_focus_out(self, carrier: str, widget_name: str) -> bool:
        try:
            placeholder = self.config_worker.get_value(
                {
                    "section_name": carrier,
                    "key": widget_name,
                }
            )
            self.submission.__setattr__(
                widget_name,
                placeholder,
            )
        except:
            raise Exception("Couldn't get & assign widget values")
        else:
            return True

    def btn_reset_template(self) -> None:
        """Replaces template page with the last-saved placeholders"""
        placeholders_section_obj = self._get_customize_tab_placeholders()
        self._set_customize_tab_placeholders(placeholders_section_obj)

    def btn_save_template(self) -> None:
        """Calls a private getter method & saves output as a dict,
        along with the section_name as it appears in config file

        Returns:
                Str -- returns a string of the section_name as it
                   appears in the config file.
            Dict -- returns a dict of all userinput from customize_tab
        """
        template_dict: dict = self.get_template_page_values()
        section_name = template_dict.pop("selected_template")
        body: list[str] = template_dict.pop("body").splitlines()
        print(f"saving template for {section_name}")
        try:
            self.config_worker.handle_save_contents(section_name, template_dict)
            self.config_worker.set_multi_line_values_for_option(
                section_name,
                "body",
                body,
                )
        except:
            raise Exception("Couldn't save template_dict to config.")

    def get_template_page_values(self) -> dict[str, str]:
        """This gets all userinput from the customize_tab

        Returns:
                Dict -- returns a dict of the selected template and all
                        userinput from the template fields, each
                    assigned accordingly to their config file keys
        """
        customize_dict = dict[str, str]
        try:
            customize_dict = {
                "selected_template": self.submission.selected_template,
                "address": self.submission.address,
                "greeting": self.submission.greeting,
                "body": self.submission.body,
                "salutation": self.submission.salutation,
            }
        except:
            raise Exception("Couldn't get customize_tab input saved into a dict.")
        else:
            return customize_dict

    ############# END --Customize Tab-- END #############

    ############# Establish Settings Tab #############
    ### Email Settings Tab ###
    def _set_email_settings_placeholders(self, section_obj) -> bool:
        """Sets the placeholders for the settings tab"""
        self.submission.default_cc1 = section_obj.get("default_cc1").value
        self.submission.default_cc2 = section_obj.get("default_cc2").value
        self.submission.username = section_obj.get("username").value
        self.submission.sig_image_file = section_obj.get("signature_image").value
        return True

    def btn_revert_email_settings(self) -> None:
        section = self.config_worker.get_section("General settings")
        self._set_email_settings_placeholders(section)

    def btn_save_email_settings(self) -> None:
        """Calls a private getter method & saves output as a dict,
        along with the section_name as it appears in config file

        Returns:
                Str -- returns a string of the section_name as it
                   appears in the config file.
            Dict -- returns a dict of all userinput from settings_tab
        """
        print("saving settings")
        settings_dict = self._get_email_settings_values()
        self.config_worker.handle_save_contents("General settings", settings_dict)

    def _get_email_settings_values(self) -> dict[str, str]:
        """Gets all userinput from the settings_tab.

        Returns:
                Dict -- returns a dict of key-names as they
                        appear in the config along with their
                    userinput values
        """
        settings_dict: dict[str, str] = {
            "default_cc1": self.submission.default_cc1,
            "default_cc2": self.submission.default_cc2,
            "username": self.submission.username,
            "signature_image": self.submission.sig_image_file,
        }
        return settings_dict

    ### End of Email Settings Tab ###
    ### Folder Settings Tab ###
    def _set_folder_settings_placeholders(self, section_obj) -> bool:
        """Sets the placeholders for the settings tab"""
        self.submission.watch_dir = section_obj.get("watch_dir").value
        self.submission.new_biz_dir = section_obj.get("new_biz_dir").value
        self.submission.renewals_dir = section_obj.get("renewals_dir").value
        config_dirs = section_obj.get("custom_dirs").value
        if config_dirs is not "":
            custom_dirs: list[str] = literal_eval(config_dirs)
            self.submission.tree.delete(*self.submission.tree.get_children())
            self.submission.set_data_into_treeview(data=custom_dirs)
        return True

    def btn_revert_folder_settings(self) -> None:
        section = self.config_worker.get_section("Folder settings")
        self._set_folder_settings_placeholders(section)

    def btn_save_folder_settings(self) -> None:
        print("saving settings")
        settings_dict = self._get_folder_settings_values()
        self.config_worker.handle_save_contents("Folder settings", settings_dict)
        self.dir_watch.path = Path(self.submission.watch_dir)

    def _get_folder_settings_values(self) -> dict[str, str]:
        settings_dict: dict[str, str] = {
            "watch_dir": self.submission.watch_dir,
            "new_biz_dir": self.submission.new_biz_dir,
            "renewals_dir": self.submission.renewals_dir,
            "custom_dirs": self.submission.get_all_rows(),
        }
        return settings_dict

    ### End of Watch Dir Settings ###
    ### Begin Custom Dir Creation Settings ###

    ### End of Custom Dir Creation Settings ###
    ### End of Folder Settings Tab ###
    ############# END --Settings Tabs-- END #############
    ############# END --Submissions Program-- END #############
