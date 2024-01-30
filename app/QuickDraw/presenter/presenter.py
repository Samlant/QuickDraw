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
import QuickDraw.presenter.protocols as protocols


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
        self.view_surplus_lines = view_surplus_lines
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

    ########################################################
    ########### Refactor within API Models #################
    ########################################################
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
    def _start_thread_for_excel(self) -> bool:
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
            else:
                return True
        return False

    ########################################################
    ########### Refactor within API Models #################
    ########################################################
    def start_program(self):
        print(f"Watching for any new PDF files in: {str(self.model_dir_watcher.path)}.")
        self.model_dir_watcher.begin_watch()

    def trigger_new_file(self, file: Path):
        print("Detected new Quoteform ")
        self.current_submission = self.model_form_builder.make(file=file)
        print(f"the current client is: {self.current_submission.__repr__}")
        months = self.model_api.get_next_months()
        self.view_new_file_alert.initialize(
            presenter=self,
            view_interpreter=VIEW_INTERPRETER,
            view_palette=self.view_palette,
            submission_info=self.current_submission,
            months=months,
        )

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

    def _refresh_quoteform_with_user_input(self) -> bool:
        self.excel_table_name = self.view_new_file_alert.selected_month
        qf = self.current_submission.quoteform
        qf.vessel_year = self.view_new_file_alert.year
        qf.vessel = self.view_new_file_alert.vessel
        qf.referral = self.view_new_file_alert.referral
        return True

    #######################################################
    ############# Start Submissions Program #############
    #######################################################
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
        path_purpose: str,
        quote_path: str = None,
    ) -> None:
        """Sends the raw path of attachment/quoteform to model for processing and saving."""
        if quote_path:
            path = quote_path
        else:
            path = Path(self.model_tab_home.filter_out_brackets(event.data))
        setattr(self.view_main, path_purpose, path.name)
        if path_purpose != "sig_image_file_path":
            return self.model_tab_home.save_path(path, path_purpose)
        else:
            return True

    def btn_clear_attachments(self) -> None:
        self.model_tab_home.attachments: list = []
        self.model_tab_home.quoteform_path: str = ""
        del self.view_main.quoteform
        del self.view_main.attachments
        print("cleared attachments.")

    def btn_process_envelopes(self, view_first: bool = False) -> None:
        """TODO REFACTOR BELOW USING SUBMISSION & EMAIL MODELS!"""
        print("clicked send button")
        self.only_view_msg = view_first
        self.current_submission = self.model_form_builder.make(
            self.model_tab_home.quoteform_path
        )
        self.current_submission.markets = self.gather_active_markets()
        self.current_submission.submit_tool = True
        self.loop_through_envelopes()

    ########################################################
    ########## BEGIN --PLACEHOLDERS FUNCS-- BEGIN ##########
    ################# LOOKS GOOD 1/29/2024 #################
    def btn_revert_view_tab(self, tab_name: str) -> bool:
        if tab_name == "quoteforms":
            self.view_main.reg_tv.delete(*self.view_main.reg_tv.get_children())
            config = open_config()
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
                return True
        elif tab_name=="template":
            tab_name == self.view_main.selected_template
        return self._set_tab_placeholders(tab_name=tab_name)
        
    def _set_tab_placeholders(self, tab_name: str) -> bool:
        tab_placeholders = self.__get_tab_placeholders(tab_name)
        self.__assign_placeholders(tab_placeholders=tab_placeholders, tab_name=tab_name)
        return True
        
    def __get_tab_placeholders(self, tab_name) -> dict[str, str]:
        config = open_config()
        section_obj = config.get_section(tab_name)
        tab_placeholders = section_obj.to_dict()
        return tab_placeholders

    def __assign_placeholders(self, tab_placeholders: dict[str, str], tab_name: str) -> bool:
        """Sets the placeholders inside desired tab"""
        for key, value in tab_placeholders.items():
            if tab_name == "surplus lines":
                setattr(self.view_surplus_lines, key, value)
            elif tab_name == "dirs" and key =="custom_dirs":
                if value != "":
                    custom_dirs: list[str] = literal_eval(value)
                    self.view_main.tree_dir.delete(*self.view_main.tree_dir.get_children())
                    self.view_main.set_data_into_treeview(data=custom_dirs)
            else:
                if isinstance(value, list):
                    value = "\n".join(value)
                if key == "body":
                    del self.view_main.body
                setattr(self.view_main, key, value)
        return True

    def on_change_template(self, *args, **kwargs) -> None:
        """Updates template tab view when user changes template."""
        self._set_tab_placeholders(self.view_main.selected_template)

    def btn_save_view_tab(self, tab_name: str):
        """Save current state of a given view tab to the config file."""
        config = open_config()
        if tab_name == "surplus lines":
            x = self.view_surplus_lines.output_path
            config.set(tab_name, "output_save_dir", x)
        elif tab_name == "quoteforms":
            row_data = self.view_main.reg_tv.get_all_rows()
            qf_reg.process_save(config=config, row_data=row_data,)
        else:
            x: dict[str, str] = getattr(self.view_main, tab_name)
            if "selected_template" in x:
                tab_name = x.pop("selected_template")
            if "watch_dir" in x:
                self.model_dir_watcher.path = Path(self.view_main.watch_dir)
            section = config.get_section(tab_name).to_dict()
            for key in section:
                if key in x:
                    if "\n" in x[key]:
                        values = x[key].splitlines()
                        option = config.get(tab_name, key)
                        option.set_values(values=values)
                    else:
                        config.set(section=tab_name, option=key, value=x[key])
                    if key ++""

    ##############################################################
    #################   NEED TO REFACTOR BELOW   #################
    ##############################################################

    def set_dropdown_options(self) -> list:
        "Submission (View) calls this value upon creation."
        return self.model_tab_templates.names()

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

    def _assign_single_placeholder(self, carrier: str, widget_name: str) -> bool:
        config = open_config()
        placeholder = config.get(carrier, widget_name).value
        self.view_main.__setattr__(
            widget_name,
            placeholder,
        )
        return True

    ############ END --PLACEHOLDERS FUNCS-- END ############
    ################ Establish Templates Tab ###############

    ############# END --Templates Tab-- END #############

    ### Folder Settings Tab ###
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
            del self.view_main.quoteforms
            ctypes.windll.user32.MessageBoxW(
                0,
                "A form already exists with this name. Please change the form name to a unique name and try adding again.",
                "Warning",
                0x10 | 0x0,
            )

    ############# --Surplus Lines Automator-- #############
    def run_surplus_lines(self):
        self.model_surplus_lines.start_view(VIEW_INTERPRETER, self.view_palette)

    ############# END --Surplus Lines Automator-- END #############

    ################ LOOK AT THE END #########################

    def on_focus_out(self, event) -> bool | None:
        """Looks like it's only applicable to templates tab.
        TODO: Verify if applicable to other tabs.
        """
        carrier = self.view_main.selected_template
        widget_name = event.widget.winfo_name()
        widget_type = event.widget.widgetName

        if carrier == "Select Market(s)":
            return True
        else:
            if (
                widget_type == "text"
                and self.check_text_from_textbox(event)
                and widget_name == "body"
            ):
                del self.view_main.body
                self._assign_single_placeholder(carrier, widget_name)
            elif widget_type == "entry" and self.check_text_from_entrybox(event):
                self._assign_single_placeholder(carrier, widget_name)
            else:
                pass

    def check_text_from_textbox(self, event) -> bool | None:
        if event.widget.get("1.0", "end-1c") == "":
            return True

    def check_text_from_entrybox(self, event) -> bool | None:
        if event.widget.get() == "":
            return True
