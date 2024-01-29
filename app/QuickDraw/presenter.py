import ctypes
import threading
from ast import literal_eval
from pathlib import Path
from tkinter import TclError

from configupdater import ConfigUpdater

import model.quoteform_registrations as qf_reg
from QuickDraw.helper import open_config, VIEW_INTERPRETER
from QuickDraw.views.submission.helper import set_start_tab
from QuickDraw.models.customer.form import Quoteform
from QuickDraw.models.customer.info import Submission
import QuickDraw.protocols as protocols


class Presenter:
    """Responsible for communicating between the Models and
    Views, including all interactions between user input and
    program logic.

    Attributes:

        Models:
            model_api_client: establishes connection with MS Graph for excel functionality.
            home_model: standard calculations, string formatting;
            config_worker: config file operations;
            model_dir_watcher: detects when a new file is created within the watched folder;
            model_email_handler: creates and organizes emails;

        Views:
            submission: creates the submission window/settings;
            new_alert: creates dialog when model_dir_watcher is triggered;
            dialog_allocate_markets: creates dialog when user allocates
            markets for client;
            tray_icon: interactive icon that shows in system tray area;
    """

    def __init__(
        self,
        model_allocate: protocols.AllocateModel,
        model_api_client: protocols.MSGraphClient,
        model_api: protocols.API,
        model_dir_handler: protocols.Dirhandler,
        model_dir_watcher: protocols.DirWatch,
        model_email_handler: protocols.EmailHandler,
        model_email_options: protocols.EmailOptionsModel,
        model_new_alert: protocols.AlertModel,
        model_surplus_lines: protocols.SurplusLinesAutomator,
        model_tab_dirs: protocols.DirsModel,
        model_tab_home: protocols.HomeModel,
        model_tab_registrations: protocols.RegistrationsModel,
        model_tab_templates: protocols.TemplatesModel,
        model_form_builder: protocols.FormBuilder,
        view_allocate: protocols.AllocateView,
        view_main: protocols.MainWindow,
        view_new_file_alert: protocols.NewFileAlert,
        view_surplus_lines: protocols.SurplusLinesView,
        view_palette: protocols.Palette,
    ) -> None:
        # Models
        self.model_api_client = model_api_client
        self.model_api = model_api
        self.model_dir_handler = model_dir_handler
        self.model_dir_watcher = model_dir_watcher
        self.model_email_handler = model_email_handler
        self.model_email_options = model_email_options
        self.model_form_builder = model_form_builder
        self.model_new_alert = model_new_alert
        self.model_surplus_lines = model_surplus_lines
        self.model_tab_dirs = model_tab_dirs
        self.model_tab_home = model_tab_home
        self.model_tab_registrations = model_tab_registrations
        self.model_tab_templates = model_tab_templates
        self.view_allocate = view_allocate
        self.view_main = view_main
        self.view_new_file_alert = view_new_file_alert
        self.view_palette = view_palette
        self.quoteform: Quoteform = None
        self.current_submission = None
        self.only_view_msg: bool = None
        self.run_flag: bool = False
        self.run_template_settings_flag: bool = False
        self.run_email_settings_flag: bool = False
        self.run_folder_settings_flag: bool = False
        self.run_SL_automator_flag: bool = False
        self.quoteform_detected: bool = False
        self.new_file_path = None

    def setup_api(self) -> bool:
        graph_values = self.config_worker.get_section("graph_api")
        if not self.model_api_client.setup_api(connection_data=graph_values):
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
                user_id = self.model_api_client.get_user_id()["id"]
                self.config_worker.handle_save_contents(
                    "graph_api",
                    save_contents={
                        "user_id": user_id,
                    },
                )
        return True

    def start_program(self):
        print(f"Watching for any new PDF files in: {str(self.model_dir_watcher.path)}.")
        self.model_dir_watcher.begin_watch()

    def trigger_new_file(self, file: Path):
        self._process_document(file=file)
        print("Detected new Quoteform")
        print(f"the current client is: {self.current_submission.__repr__}")
        months = self.model_api.get_next_months()
        self.view_new_file_alert.initialize(
            presenter=self,
            view_interpreter=VIEW_INTERPRETER,
            view_palette=self.view_palette,
            submission_info=self.current_submission,
            months=months,
        )

    def _process_document(self, file: Path) -> bool:
        print("Processing/Parsing PDF document.")
        count = 0
        successful = False
        while not successful and count < 3:
            count += 1
            try:
                self.quoteform = self.model_form_builder.make(file)
                self.current_submission = Submission(
                    quoteform=self.quoteform,
                    status="PROCESSED",
                )
            except Exception as e:
                print(e)
                ctypes.windll.user32.MessageBoxW(
                    0,
                    "Please exit out of the PDF file so that the program can delete the original file.",
                    "Warning: Exit the PDF",
                    1,
                )
            else:
                successful = True
        return True

    def allocate_markets(self):
        self.view_allocate.initialize(
            self,
            VIEW_INTERPRETER,
            self.view_palette,
        )

    def save_user_choices(self) -> None:
        print("Saving choices")
        self.alert_model.process_user_choice(
            self.view_allocate.markets,
            self.current_submission,
        )

    def create_and_send_data_to_api(self):
        print("creating call to send to Microsoft API")
        config = open_config()
        username = config.get("General settings", "username")
        json = self.model_api.create_excel_json(self.current_submission, username)
        self.model_api_client.run_excel_program(
            json_payload=json,
        )

    def _send_excel_api_call(self):
        self.create_and_send_data_to_api()
        print("Adding excel row via API")
        ####################################
        ####################################
        """TODO: Abstract code into excel's api model."""
        ####################################
        ####################################
        if not self.quoteform_detected:
            self.excel_table_name = self.model_api.get_current_month()
        if not self.model_api_client.client_already_exists(self.excel_table_name):
            self.model_api_client.add_row(self.excel_table_name)
        else:
            print("Client already exists on tracker,  skipping adding to the tracker.")
        self.model_api_client.close_workbook_session()
        ####################################
        ####################################

    def choice(self, choice: str):
        self.quoteform_detected = True
        self.model_dir_handler.process_dirs(
            self.current_submission,
        )
        self._refresh_quoteform_with_user_input()
        self.view_new_file_alert.root.destroy()
        if choice == "track_allocate":
            self.allocate_markets()
            self._start_thread_for_excel()

        elif choice == "track_submit":
            self.start_submission_program(quote_path=self.current_submission.new_path)
        else:
            self._start_thread_for_excel()

    def _start_thread_for_excel(self):
        count = 0
        successful = False
        while not successful and count < 3:
            try:
                thread_xl = threading.Thread(
                    daemon=True,
                    target=self._send_excel_api_call,
                    name="Excel API Call",
                )
                thread_xl.start()
            except Exception as e:
                print(f"API call to Excel failed. {e}")

    def _refresh_quoteform_with_user_input(self) -> bool:
        self.excel_table_name = self.view_new_file_alert.selected_month
        self.current_submission.quoteform.vessel_year = self.view_new_file_alert.year
        self.current_submission.quoteform.vessel = self.view_new_file_alert.vessel
        self.current_submission.quoteform.referral = self.view_new_file_alert.referral
        return True

    ############# Start Submissions Program #############
    def start_submission_program(self, specific_tab: str | None = None, quote_path: str = None) -> None:  # type: ignore
        """Starts the program by creating GUI object,
        configuring initial values,  then running it
        This also sets the default mail application.
        """
        print("starting email submission program")
        self.view_main.create_UI_obj(self, VIEW_INTERPRETER, self.view_palette)
        if quote_path:
            self.set_initial_placeholders(quote_path)
        else:
            self.set_initial_placeholders()
        self.insert_qf_registration_placeholders()
        if specific_tab:
            set_start_tab(self.view_main, specific_tab)

    def set_dropdown_options(self) -> list:
        "Submission (View) calls this value upon creation."
        return self.templates_model_model.names()

    ############# Establish Main Tab #############

    def set_initial_placeholders(self, quote_path: str = None) -> None:
        """Sets initial texts for the main/home tab, if applicable"""
        self.btn_revert_folder_settings()
        personal_settings_keys: list[str] = [
            "username",
            "use_CC_defaults",
            "default_cc1",
            "default_cc2",
        ]
        config: ConfigUpdater = open_config()
        for key in personal_settings_keys:
            new_value = config.get("General settings", key)
            setattr(self.view_main, key, new_value)
        self._set_customize_tab_placeholders(config.get_section("Initial placeholders"))

        if quote_path:
            self.process_quoteform_path(quote_path=quote_path)
        else:
            pass

    def browse_file_path(self, event=None, is_quoteform: bool = False):
        path = self.model_tab_home.browse_file_path(is_quoteform)
        if is_quoteform:
            del self.view_main.quoteform
            self.view_main.quoteform = path
        else:
            self.view_main.extra_attachments = path

    def process_file_path(
        self,
        event,
        is_quoteform: bool = False,
        quote_path: str = None,
    ) -> None:
        """Sends the raw path of attachment/quoteform to model for processing and saving."""
        if quote_path:
            path = quote_path
        else:
            path = Path(self.model_tab_home.filter_out_brackets(event.data))
        if is_quoteform:
            del self.view_main.quoteform
            self.view_main.quoteform = path.name
        else:
            self.view_main.attachments = path.name
        return self.model_tab_home.save_path(path, is_quoteform)

    def process_signature_image_path(self, drag_n_drop_event) -> None:
        """Saves the signature image file onto the Settings page, but
        does not save it to the config file yet;  the Save button writes
        this to the config file.

        Arguments:
            raw_path {str} -- the raw str of full path of the file
        """
        print("saving signature image")
        raw_path: str = drag_n_drop_event.data
        path = self.model_tab_home.filter_out_brackets(raw_path)
        self.view_main.sig_image_file_path = path

    ############# END --Main Tab-- END #############

    ############# Establish Main Actions #############

    def btn_clear_attachments(self) -> None:
        self.model_tab_home.attachments: list = []
        self.model_tab_home.quoteform_path: str = ""
        del self.view_main.quoteform
        del self.view_main.attachments
        print("cleared attachments.")

    def btn_view_template(self) -> None:
        print(
            "Sorry,  viewing is not yet implemented.  Try sending a message to yourself using the settings tab to assign your email address, then try again."
        )
        self.only_view_msg = True
        print("Viewing templates has not yet been implemented!")

    def btn_send_envelopes(self, view_first: bool = False) -> None:
        print("clicked send button")
        self.only_view_msg = view_first
        self._process_document(self.model_tab_home.quoteform_path)
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
        raw_dict = self.get_single_carriers()
        processed_list = self.model_tab_home.filter_only_positive_submissions(raw_dict)
        return processed_list

    def _handle_redundancies(self) -> str:
        """Gets possible redundant carriers' checkbox values, filters to only keep
        positive submissions, then combines them into one submission

        Returns -- Dict: returns dict of a single, combined carrier submission
        """
        raw_dict: dict[str, any] = self._get_possible_redundancies()
        filtered_list = self.model_tab_home.filter_only_positive_submissions(raw_dict)
        processed_str = self.model_tab_home.handle_redundancies(filtered_list)
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
                "American Modern": self.view_main.am,
                "Kemah Marine": self.view_main.km,
                "Concept Special Risks": self.view_main.cp,
                "Yachtinsure": self.view_main.yi,
                "Century": self.view_main.ce,
                "Intact": self.view_main.In,
                "Travelers": self.view_main.tv,
            }
        except ValueError as ve:
            raise ValueError(f"Couldn't get carrier checkboxes saved into a dict. {ve}")
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
                "Seawave": self.view_main.sw,
                "Prime Time": self.view_main.pt,
                "New hampshire": self.view_main.nh,
            }
        except ValueError as ve:
            raise ValueError(f"Couldn't get carrier checkboxes saved into a dict. {ve}")
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
        self.model_email_handler.subject = self.model_email_handler.stringify_subject(
            self.current_submission,
        )

        unformatted_cc = self._handle_getting_CC_addresses()
        self.model_email_handler.cc = self.model_tab_home.format_cc_for_api(
            unformatted_cc,
        )
        self.model_email_handler.extra_notes = self.view_main.extra_notes
        self.model_email_handler.username = self.config_worker.get_value(
            {
                "section_name": "General settings",
                "key": "username",
            }
        )

        attachments = self.model_tab_home.get_all_attachments()
        self.model_email_handler.attachments_list = (
            self.model_api.create_attachments_json(attachment_paths=attachments)
        )

        self.model_email_handler.img_sig_url = self.config_worker.get_value(
            {
                "section_name": "General settings",
                "key": "signature_image",
            }
        )
        for carrier in self.current_submission.markets:
            carrier_section = self.config_worker.get_section(carrier)
            unformatted_to = carrier_section.get("address").value
            self.model_email_handler.to = self.model_tab_home.format_to_for_api(
                unformatted_to
            )
            signature_settings = self.get_signature_settings()
            self.model_email_handler.body = self.model_email_handler.make_msg(
                carrier_section,
                signature_settings,
            )

            self.json = self.model_api.create_email_json(email=self.model_email_handler)
            print("sending email message")
            count = 0
            successful = False
            while not successful and count > 5:
                count += 1
                try:
                    thread_ol = threading.Thread(
                        daemon=True, target=self.send_email_api, name="Outlook API Call"
                    )
                    thread_ol.start()
                except Exception as e:
                    print(f"Outlook API call failed. {e}")
            count = 0
            successful = False
            while not successful and count > 5:
                count += 1
                try:
                    thread_xl = threading.Thread(
                        daemon=True,
                        target=self._send_excel_api_call,
                        name="Excel API Call",
                    )
                    thread_xl.start()
                except Exception as e:
                    print(f"Excel API call failed. {e}")
        self.quoteform_detected = False

    def send_email_api(self):
        print("Sending email via MSGraph")
        self.model_api_client.send_message(message=self.json)
        print("Email sent.")

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
        list_of_cc = [self.view_main.userinput_CC1, self.view_main.userinput_CC2]
        if self.view_main.use_CC_defaults:
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

        self.view_main.address = section_obj.get("address").value
        self.view_main.greeting = section_obj.get("greeting").value
        del self.view_main.body
        self.view_main.body = section_obj.get("body").value
        self.view_main.outro = section_obj.get("outro").value
        self.view_main.salutation = section_obj.get("salutation").value

    def _get_customize_tab_placeholders(self):
        current_selection = self.view_main.selected_template
        return self.config_worker.get_section(current_selection)

    # Complete if necessary - 02.09.2023
    def on_change_template(self, *args, **kwargs) -> None:
        """Updates the placeholders on customize_tab when dropdown changes

        Returns:
                Bool -- returns a bool for success & for testing
        """
        selected_template = self.view_main.selected_template
        placeholders_dict = self.config_worker.get_section(selected_template)
        self._set_customize_tab_placeholders(placeholders_dict)

    def on_focus_out(self, event) -> bool | None:
        carrier = self.view_main.selected_template
        widget_name = event.widget.winfo_name()
        widget_type = event.widget.widgetName

        if carrier == "Select Market(s)":
            return True
        else:
            if widget_type == "text" and self.check_text_from_textbox(event):
                if widget_name == "body":
                    del self.view_main.body
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
        placeholder = self.config_worker.get_value(
            {
                "section_name": carrier,
                "key": widget_name,
            }
        )
        self.view_main.__setattr__(
            widget_name,
            placeholder,
        )
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
        self.config_worker.handle_save_contents(section_name, template_dict)
        self.config_worker.set_multi_line_values_for_option(
            section_name,
            "body",
            body,
        )

    def get_template_page_values(self) -> dict[str, str]:
        """This gets all userinput from the customize_tab

        Returns:
                Dict -- returns a dict of the selected template and all
                        userinput from the template fields, each
                    assigned accordingly to their config file keys
        """
        customize_dict = dict[str, str]

        customize_dict = {
            "selected_template": self.view_main.selected_template,
            "address": self.view_main.address,
            "greeting": self.view_main.greeting,
            "body": self.view_main.body,
            "outro": self.view_main.outro,
            "salutation": self.view_main.salutation,
        }

        return customize_dict

    ############# END --Customize Tab-- END #############

    ############# Establish Settings Tab #############
    ### Email Settings Tab ###
    def _set_email_settings_placeholders(self, section_obj) -> bool:
        """Sets the placeholders for the settings tab"""
        self.view_main.default_cc1 = section_obj.get("default_cc1").value
        self.view_main.default_cc2 = section_obj.get("default_cc2").value
        self.view_main.username = section_obj.get("username").value
        self.view_main.sig_image_file_path = section_obj.get("signature_image").value
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
            "default_cc1": self.view_main.default_cc1,
            "default_cc2": self.view_main.default_cc2,
            "username": self.view_main.username,
            "signature_image": self.view_main.sig_image_file_path,
        }
        return settings_dict

    ### End of Email Settings Tab ###
    ### Folder Settings Tab ###
    def _set_folder_settings_placeholders(self, section_obj) -> bool:
        """Sets the placeholders for the settings tab"""
        self.view_main.watch_dir = section_obj.get("watch_dir").value
        self.view_main.new_biz_dir = section_obj.get("new_biz_dir").value
        self.view_main.renewals_dir = section_obj.get("renewals_dir").value
        config_dirs = section_obj.get("custom_dirs").value
        if config_dirs != "":
            custom_dirs: list[str] = literal_eval(config_dirs)
            self.view_main.tree_dir.delete(*self.view_main.tree_dir.get_children())
            self.view_main.set_data_into_treeview(data=custom_dirs)
        return True

    def btn_revert_folder_settings(self) -> None:
        section = self.config_worker.get_section("Folder settings")
        self._set_folder_settings_placeholders(section)

    def btn_save_folder_settings(self) -> None:
        print("saving settings")
        settings_dict = self._get_folder_settings_values()
        self.config_worker.handle_save_contents("Folder settings", settings_dict)
        self.model_dir_watcher.path = Path(self.view_main.watch_dir)

    def _get_folder_settings_values(self) -> dict[str, str]:
        settings_dict: dict[str, str] = {
            "watch_dir": self.view_main.watch_dir,
            "new_biz_dir": self.view_main.new_biz_dir,
            "renewals_dir": self.view_main.renewals_dir,
            "custom_dirs": self.view_main.get_all_rows(),
        }
        return settings_dict

    ### End of Watch Dir Settings ###
    ### Begin Custom Dir Creation Settings ###

    ### End of Custom Dir Creation Settings ###
    ### End of Folder Settings Tab ###
    ### Begin Quoteform Registrations Tab ###
    def add_qf_registration(self):
        form_names = self.view_main.reg_tv.get_all_names()
        name = qf_reg.standardize_name(self.view_main.form_name)
        if qf_reg.validate_name(form_names, name):
            qf = Quoteform(
                name=name,
                fname=self.view_main.fname,
                lname=self.view_main.lname,
                year=self.view_main.year,
                vessel=self.view_main.vessel,
                referral=self.view_main.referral,
            )
            self.view_main.reg_tv.add_registration(qf)
            del self.view_main.form_name
            del self.view_main.fname
            del self.view_main.lname
            del self.view_main.year
            del self.view_main.vessel
            del self.view_main.referral
        else:
            ctypes.windll.user32.MessageBoxW(
                0,
                "A form already exists with this name. Please change the form name to a unique name and try adding again.",
                "Warning",
                0x10 | 0x0,
            )

    def btn_save_registration_settings(self):
        row_data = self.view_main.reg_tv.get_all_rows()
        config = self.config_worker._open_config()
        qf_reg.process_save(config, row_data)

    def btn_revert_registration_settings(self):
        self.view_main.reg_tv.delete(*self.view_main.reg_tv.get_children())
        self.insert_qf_registration_placeholders()

    def insert_qf_registration_placeholders(self):
        config = self.config_worker._open_config()
        quoteform_names = [y for y in config.sections() if "Form_" in y]
        for name in quoteform_names:
            section = config.get_section(name)
            options = section.items()
            form = Quoteform(
                name,
                options[0][1].value,
                options[1][1].value,
                options[2][1].value,
                options[3][1].value,
                options[4][1].value,
            )
            self.view_main.reg_tv.add_registration(form)

    ### End of Quoteform Registrations Tab ###
    ############# END --Settings Tabs-- END #############
    ############# END --Submissions Program-- END #############

    ############# --Surplus Lines Automator-- #############
    def run_surplus_lines(self):
        self.model_surplus_lines.start_view(VIEW_INTERPRETER, self.view_palette)

    def save_SL_output_dir(self, dir_path):
        config: ConfigUpdater = open_config()
        config["Surplus lines settings"]["output_save_dir"].value = dir_path

    ############# END --Surplus Lines Automator-- END #############
