from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


class API(Protocol):
    def create_json_payload(self, data) -> dict[str, any]:
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

    def list_of_cc_to_str(
        self,
        input_list: list,
    ) -> str:
        ...


class ConfigWorker(Protocol):
    def get_value(
        self,
        request: dict,
    ) -> any:
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
    def create_folder(
        self,
        submission_info,
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
    def create_letter(self) -> None:
        ...

    def assign_content_to_letter(
        self,
        subject: str,
        formatted_cc_str: str,
        extra_notes: str,
        username: str,
        carrier_config_dict: dict[str, str],
        attachments_list: list[str],
    ) -> None:
        ...

    def send_letter(self) -> None:
        ...

    def view_letter(self) -> bool:
        raise NotImplementedError

    def stringify_subject(self, formatted_values: dict[str, str]) -> str:
        ...


class MSGraphClient(Protocol):
    def run_program(
        self,
        connection_data: dict,
        json_payload: dict,
    ):
        ...

    def add_row(self) -> None:
        ...

    def close_workbook_session(self) -> None:
        ...


class Submission(Protocol):
    @property
    def extra_notes(self) -> str:
        ...

    @property
    def use_default_cc_addresses(self) -> bool:
        ...

    @property
    def sw(self) -> str | int | bool | list:
        ...

    @property
    def pt(self) -> str | int | bool | list:
        ...

    @property
    def nh(self) -> str | int | bool | list:
        ...

    @property
    def am(self) -> str | int | bool | list:
        ...

    @property
    def km(self) -> str | int | bool | list:
        ...

    @property
    def cp(self) -> str | int | bool | list:
        ...

    @property
    def yi(self) -> str | int | bool | list:
        ...

    @property
    def ce(self) -> str | int | bool | list:
        ...

    @property
    def In(self) -> str | int | bool | list:
        ...

    @property
    def tv(self) -> str | int | bool | list:
        ...

    @property
    def quoteform(self) -> str:
        ...

    @property
    def extra_attachments(self) -> str:
        ...

    @property
    def selected_template(self) -> str:
        ...

    @property
    def address(
        self,
        address: str,
    ) -> str:
        ...

    @property
    def greeting(
        self,
        greeting: str,
    ) -> str:
        ...

    @property
    def body(
        self,
        body: str,
    ) -> str:
        ...

    @property
    def salutation(
        self,
        salutation: str,
    ) -> str:
        ...

    @property
    def default_cc1(
        self,
        default_cc1: str,
    ) -> str:
        ...

    @property
    def default_cc2(
        self,
        default_cc2: str,
    ) -> str:
        ...

    @property
    def username(self) -> str:
        ...

    @property
    def sig_image_file(self) -> str:
        ...

    # extra_notes: str
    # selected_template:str
    # userinput_CC1: str
    # userinput_CC2: str
    # use_CC_defaults: bool
    # sw: str
    # pt: str
    # nh: str
    # am: str
    # km: str
    # cp: str
    # yi: str
    # ce: str
    # In: str
    # tv: str
    # address: str
    # greeting: str
    # body: str
    # salutation: str
    # default_cc1: str
    # default_cc2: str
    # username: str

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


class Presenter:
    """Responsible for communicating between the Models and Views, including all interactions between user input and program logic.

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
            dialog_allocate_markets: creates dialog when user allocates markets for client;
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
        # ALL GOOD. 3rd tier launch list.
        self.api_model = api_model
        self.base_model = base_model
        # ALL GOOD. Consider renaming. 1st tier launch list.
        self.config_worker = config_worker
        # GOOD. double-check at end. 1st tier launch list.
        self.dir_handler = dir_handler
        self.dir_watch = dir_watch
        # ALL GOOD. 1st tier launch list.
        self.email_handler = email_handler
        # Working on it now.  3rd tier launch list.
        self.pdf = pdf
        # ALL GOOD. 2nd tier launch list.

        # Views
        self.submission = submission
        # 3rd tier launch list.
        self.dialog_new_file = dialog_new_file
        # 2nd tier launch list.
        self.dialog_allocate_markets = dialog_allocate_markets
        # 2nd tier launch list.
        # self.tray_icon = tray_icon
        # Mostly good,  double-check. #1st tier launch list.
        self.current_submission = None
        self.send_or_view: str = None
        self.run_flag: bool = False

    def start_program(self):
        self.dir_watch.begin_watch()

    def trigger_new_file(self, file: Path):
        # start dialog_new_file
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
        print(f"the current client is: {self.current_submission.__repr__}")
        self.dialog_new_file.initialize(
            presenter=self,
            submission_info=self.current_submission,
        )
        self.dialog_new_file.root.mainloop()

    def choice(self, choice: str):
        path = self.dir_handler.create_folder(self.current_submission)
        self.dialog_new_file.root.destroy()
        if choice == "track_allocate":
            self.start_allocate_dialog()
        elif choice == "track_submit":
            self.start_submission_program()
            print("Submission emailed to markets.")
        self.create_and_send_data_to_api()
        self.api_client.add_row()
        self.api_client.close_workbook_session()

    def create_and_send_data_to_api(self):
        json = self.api_model.create_json_payload(self.current_submission)
        data = self.api_model.get_connection_data(self.config_worker)
        self.api_client.run_program(
            connection_data=data,
            json_payload=json,
        )

    def start_allocate_dialog(self):
        # start dialog_allocate_markets
        self.dialog_allocate_markets.initialize(self)
        self.dialog_allocate_markets.root.mainloop()

    def save_user_choices(self):
        all_options = self.dialog_allocate_markets.get_markets()
        self.current_submission = self.base_model.process_user_choice(
            all_options,
            self.current_submission,
        )

    ############# Start Submissions Program #############

    def start_submission_program(self) -> None:
        """Starts the program by creating GUI object,
        configuring initial values,  then running it
        This also sets the default mail application.
        """
        self.submission.create_UI_obj(self)
        self.set_initial_placeholders()
        self.submission.root.mainloop()

    def set_dropdown_options(self) -> list:
        "Submission (View) calls this value upon creation."
        return self.base_model.get_dropdown_options()

    ############# Establish Main Tab #############

    def set_initial_placeholders(self) -> None:
        """Sets initial texts for the main/home tab, if applicable"""
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

    def process_quoteform_path(self, drag_n_drop_event) -> None:  # GOOD
        """Sends the raw path to model for proccessing & saving.

        Arguments:
            raw_path {str} -- the raw str of full path of the file

        Returns:
            Tuple -- returns the path & a boolean for distinguishing
                          it apart from other attachments.
        """
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
        raw_path: str = drag_n_drop_event.data
        path = self.base_model.filter_out_brackets(raw_path)
        self.submission.extra_attachments = Path(path).name
        return self.base_model.save_path(path, is_quoteform=False)

    def process_signature_image_path(self, drag_n_drop_event) -> None:
        """Saves the signature image file onto the Settings page, but does not save it to the config file yet;  the Save button writes this to the config file.

        Arguments:
            raw_path {str} -- the raw str of full path of the file
        """
        raw_path: str = drag_n_drop_event.data
        path = self.base_model.filter_out_brackets(raw_path)
        self.submission.sig_image_file = path

    ############# END --Main Tab-- END #############

    ############# Establish Main Actions #############

    def btn_clear_attachments(self) -> None:
        self.base_model.extra_attachments: list = []
        self.base_model.quoteform_path: str = ""
        del self.submission.quoteform
        del self.submission.extra_attachments

    def btn_view_template(self) -> None:
        raise NotImplementedError

    def btn_send_envelopes(self) -> None:
        self.send_or_view = "send"
        self.current_submission.markets = self.gather_active_markets()
        self.loop_through_envelopes()

    ############# END --Main Actions-- END #############

    ############# Sending Envelope #############

    def gather_active_markets(self) -> list:
        """This gets the markets that the user chose. Also checks for and handles any duplicate email address.

        Returns: list of market names to submit to.

        Arguments (outdated):
                autosend = {bool}
                NOTE: If True, no window will be shown and all emails
                will be sequentially sent. If False, a window will be shown for
                each email prior to sending.
        """
        submission_list = self._handle_single_markets()
        redundant_result = self._handle_redundancies()
        if redundant_result != None:
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
        try:
            raw_dict: dict(str, any) = self._get_possible_redundancies()
            filtered_list = self.base_model.filter_only_positive_submissions(raw_dict)
            processed_str = self.base_model.handle_redundancies(filtered_list)
        except:
            raise Exception("Failed handling redundancies.")
        else:
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
        possible_redundancies_dict = dict(str, str | int | bool | list)
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
        (2) gets and transforms needed data into each of its final formatted type and form,
        (3) applies the properly formatted data into each the envelope, and,
        (4) sends the envelope to the recipient, inclusive of all data.
        """
        subject = str(
            self.email_handler.stringify_subject(
                self.current_submission,
            )
        )
        list_of_cc = list(self._handle_getting_CC_addresses())
        formatted_cc_str = self.base_model.list_of_cc_to_str(list_of_cc)
        extra_notes = self.submission.extra_notes
        username = str(
            self.config_worker.get_value(
                {"section_name": "General settings", "key": "username"}
            )
        )
        attachments_list = self.base_model.get_all_attachments()

        for carrier in self.current_submission.markets:
            self.email_handler.create_letter()
            carrier_config_dict: dict[str, any] = self.config_worker.get_section(
                carrier
            )

            signature_image_key = self.config_worker.get_value(
                {
                    "section_name": "General settings",
                    "key": "signature_image",
                }
            )
            carrier_config_dict["signature_image"] = signature_image_key
            self.email_handler.assign_content_to_letter(
                subject,
                formatted_cc_str,
                extra_notes,
                username,
                carrier_config_dict,
                attachments_list,
            )
            self.email_handler.send_letter()
            # time.wait(5000)
            # i = input("Press an key to send the next envelope.")
        # EXIT THE TKINTER WINDOW

        self.submission.root.quit()

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

    def on_focus_out(self, event) -> bool:
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
        try:
            self.config_worker.handle_save_contents(section_name, template_dict)
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

    def _set_settings_tab_placeholders(self, section_obj) -> None:
        """Sets the placeholders for the settings tab"""
        try:
            self.submission.default_cc1 = section_obj.get("default_cc1").value
            self.submission.default_cc2 = section_obj.get("default_cc2").value
            self.submission.username = section_obj.get("username").value
            self.submission.sig_image_file = section_obj.get("signature_image").value
        except:
            raise Exception("Couldn't set placeholders for the settings_tab")
        else:
            return True

    def btn_revert_settings(self) -> None:
        section = self.config_worker.get_section("General settings")
        self._set_settings_tab_placeholders(section)

    def btn_save_settings(self) -> None:
        """Calls a private getter method & saves output as a dict,
        along with the section_name as it appears in config file

        Returns:
                Str -- returns a string of the section_name as it
                   appears in the config file.
            Dict -- returns a dict of all userinput from settings_tab
        """
        settings_dict = self._get_settings_values()
        self.config_worker.handle_save_contents("General settings", settings_dict)

    def _get_settings_values(self) -> dict[str, any]:
        """Gets all userinput from the settings_tab.

        Returns:
                Dict -- returns a dict of key-names as they
                        appear in the config along with their
                    userinput values
        """
        settings_dict = dict[str, any]
        settings_dict = {
            "default_cc1": self.submission.default_cc1,
            "default_cc2": self.submission.default_cc2,
            "username": self.submission.username,
            "signature_image": self.submission.sig_image_file,
        }
        return settings_dict

    ############# END --Settings Tab-- END #############

    ############# END --Submissions Program-- END #############
