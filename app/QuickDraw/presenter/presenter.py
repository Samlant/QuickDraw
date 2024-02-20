import ctypes
import threading
from ast import literal_eval
from pathlib import Path
##################################
# this is kept to catch Tclerrors if they show up again;
# from tkinter import TclError 
# was caused by issues arising from multi-threading with Tkinter.
# NOTE: Tkinter needs to stem from the main thread ONLY (darn).
# *NOT* thread-safe.
##################################
import itertools
# from multiprocessing import p

from win10toast import ToastNotifier


import QuickDraw.models.windows.registrations as qf_reg
from QuickDraw.helper import open_config, VIEW_INTERPRETER, AVAILABLE_CARRIERS
from QuickDraw.views.submission.helper import set_start_tab, ALL_TABS
import QuickDraw.presenter.protocols as protocols
from exceptions.surplus_lines import OutputDirNotSet

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
        model_alert_new_qf: protocols.AlertModel,
        model_dir_handler: protocols.DirHandler,
        model_dir_watcher: protocols.DirWatch,
        model_email_builder: protocols.EmailBuilder,
        model_graph_api: protocols.GraphAPI,
        model_submission: protocols.SubmissionModel,
        model_surplus_lines: protocols.SurplusLinesAutomator,
        # model_tab_dirs: protocols.DirsModel,
        model_tab_home: protocols.HomeModel,
        model_tab_templates: protocols.TemplatesModel,
        view_allocate: protocols.AllocateView,
        view_main: protocols.MainWindow,
        view_new_file_alert: protocols.NewFileAlert,
        view_surplus_lines: protocols.SurplusLinesView,
        view_palette: protocols.Palette,
    ) -> None:
        self.model_alert_new_qf = model_alert_new_qf
        self.model_dir_handler = model_dir_handler
        self.model_dir_watcher = model_dir_watcher
        self.model_email_builder = model_email_builder
        self.model_graph_api = model_graph_api
        self.model_submission = model_submission
        self.model_surplus_lines = model_surplus_lines
        # self.model_tab_dirs = model_tab_dirs
        self.model_tab_home = model_tab_home
        self.model_tab_templates = model_tab_templates
        self.view_allocate = view_allocate
        self.view_main = view_main
        self.view_new_file_alert = view_new_file_alert
        self.view_palette = view_palette
        self.view_surplus_lines = view_surplus_lines
        self.quoteform: protocols.Quoteform = None
        self.submission: protocols.Submission = None
        self.only_view_msg: bool = None
        self.run_flag: bool = False
        self.run_template_settings_flag: bool = False
        self.run_email_settings_flag: bool = False
        self.run_folder_settings_flag: bool = False
        self.run_SL_automator_flag: bool = False
        self.new_file_path = None

    def setup_api(self) -> bool:
        return self.model_graph_api.setup()
    
    def start_program(self):
        print(f"Watching for any new PDF files in: {str(self.model_dir_watcher.path)}.")
        self.model_dir_watcher.begin_watch()

    def trigger_new_file(self, file: Path):
        print("Detected new Quoteform ")
        self.submission = self.model_submission.process_quoteform(
            _quoteform_path=file,
        )
        print(f"the current client is: {self.submission.__repr__}")
        months = self.model_alert_new_qf.get_next_months()
        self.view_new_file_alert.initialize(
            presenter=self,
            view_interpreter=VIEW_INTERPRETER,
            view_palette=self.view_palette,
            submission=self.submission,
            months=months,
        )

    def choice(self, choice: str):
        self.model_dir_handler.process_dirs(
            self.submission,
        )
        self._refresh_submission_with_user_input()
        self.view_new_file_alert.root.destroy()
        if choice == "track_allocate":
            self.allocate_markets()

        elif choice == "track_submit":
            # SEND EXCEL API (in case submission prog crashes...)
            
            quoteform_path = self.submission.quoteform.path
            self.submission = None
            self.start_submission_program(quoteform=quoteform_path)
        else:
            self._start_thread_for_excel()
            self.submission = None

    def _refresh_submission_with_user_input(self) -> bool:
        self.submission.tracker_month = self.view_new_file_alert.selected_month
        self.submission.vessel.year = self.view_new_file_alert.year
        self.submission.vessel.make = self.view_new_file_alert.vessel
        self.submission.customer.referral = self.view_new_file_alert.referral
        return True

    def allocate_markets(self):
        self.view_allocate.initialize(
            self,
            VIEW_INTERPRETER,
            self.view_palette,
        )

    def save_allocated_markets(self) -> list[protocols.Carrier]:
        carriers = self.__get_carrier_results(self.view_allocate)
        self.view_allocate.root.destroy()
        self.submission.carriers = carriers
        self._start_thread_for_excel()
        self.submission = None

    #######################################################
    ############# Start Submissions Program #############
    #######################################################
    def start_submission_program(
        self, specific_tab: str = None, quoteform: Path = None
    ) -> None:
        """Starts the program by creating GUI object,
        configuring initial values,  then running it
        This also sets the default mail application.
        """
        print("starting email submission program")
        self.view_main.create_UI_obj(self, VIEW_INTERPRETER, self.view_palette)
        if quoteform:
            self._set_initial_placeholders(quoteform)
        else:
            self._set_initial_placeholders()
        if specific_tab:
            set_start_tab(self.view_main, specific_tab)

    def browse_file_path(self, event=None, is_quoteform: bool = False):
        path = self.model_tab_home.browse_file_path(is_quoteform)
        if is_quoteform:
            del self.view_main.quoteform
            self.view_main.quoteform = path
        elif isinstance(path, list) or isinstance(path, tuple):
            for _a in path:
                self.view_main.attachments = path
        else:
            self.view_main.attachments = path

    def process_file_path(
        self,
        event,
        path_purpose: str,
        quoteform: Path = None,
    ) -> None:
        """Sends the raw path of attachment/quoteform to model for
        processing and saving."""
        if quoteform:
            path = str(quoteform)
        else:
            path = event.data
        output = self.model_tab_home.process_file(path, path_purpose)
        setattr(self.view_main, path_purpose, output)

    def btn_clear_attachments(self) -> None:
        self.model_tab_home.attachments: list = []
        self.model_tab_home.quoteform_path: str = ""
        del self.view_main.quoteform
        del self.view_main.attachments
        print("cleared attachments.")

    def __get_carrier_results(
        self,
        view: protocols.AllocateView | protocols.MainWindow,
    ) -> list[protocols.Carrier]:
        carriers = []
        for carrier in AVAILABLE_CARRIERS:
            value = getattr(view, carrier.name)
            if value:
                carriers.append(carrier)
        return carriers

    def btn_process_envelopes(self, auto_send: bool = True) -> None:
        carriers = self.__get_carrier_results(self.view_main)
        carrier_combos = self.get_carrier_combos(
            all=False,
            carrier_list=carriers,
        )
        markets = self.model_submission.make_markets(
            maket_tuples=(carrier_combos),
        )
        view_results = self.view_main.home
        self.submission = self.model_submission.process_quoteform(
            _quoteform_path=view_results["quoteform"],
            carriers=carriers,
            markets=markets,
            status="SUBMIT TO MRKTS",
        )
        self.submission.attachments = self.model_submission.validate_attachments(
            attachments=view_results["attachments"],
        )
        user_carbon_copies = view_results["user_CC1"] + view_results["user_CC2"]
        emails = self.model_email_builder.make_all_emails(
            submission=self.submission,
            extra_notes=view_results["extra_notes"],
            user_CC=user_carbon_copies,
        )
        self.model_graph_api.run_graph_calls(
            submission=self.submission,
            outlook=True,
            emails=emails,
            auto_send=auto_send,
        )

    ########################################################
    ########## BEGIN --PLACEHOLDERS FUNCS-- BEGIN ##########
    ################# LOOKS GOOD 1/29/2024 #################
    def _set_initial_placeholders(self, quoteform: Path = None) -> None:
        """Sets initial texts for all tabs, if applicable"""
        for tab in ALL_TABS:
            self.btn_revert_view_tab(tab)
        if quoteform:
            self.process_file_path(
                event=None,
                path_purpose="quoteform",
                quoteform=quoteform,
            )
        else:
            pass

    def btn_revert_view_tab(self, tab_name: str) -> bool:
        if tab_name == "quoteforms":
            self.view_main.reg_tv.delete(*self.view_main.reg_tv.get_children())
            forms = qf_reg.process_retrieval()
            self.view_main.reg_tv.add_registration(forms)
            return True
        elif tab_name == "template":
            tab_name = self.view_main.selected_template
        return self._set_tab_placeholders(tab_name=tab_name)

    def _set_tab_placeholders(self, tab_name: str) -> bool:
        tab_placeholders = self.__get_tab_placeholders(tab_name)
        self.__assign_placeholders(
            tab_placeholders=tab_placeholders,
            tab_name=tab_name,
        )
        return True

    def __get_tab_placeholders(self, tab_name) -> dict[str, str]:
        config = open_config()
        section_obj = config.get_section(tab_name)
        tab_placeholders = section_obj.to_dict()
        return tab_placeholders

    def __assign_placeholders(
        self, tab_placeholders: dict[str, str], tab_name: str
    ) -> bool:
        """Sets the placeholders inside desired tab"""
        for key, value in tab_placeholders.items():
            if tab_name == "surplus lines":
                setattr(self.view_surplus_lines, key, value)
            elif tab_name == "dirs" and key == "custom_dirs":
                if value != "":
                    custom_dirs: list[str] = literal_eval(value)
                    self.view_main.tree_dir.delete(
                        *self.view_main.tree_dir.get_children()
                    )
                    self.view_main.set_data_into_treeview(data=custom_dirs)
            else:
                if isinstance(value, list):
                    value = "\n".join(value)
                if key == "body":
                    del self.view_main.body
                setattr(self.view_main, key, value)
        return True

    def get_carrier_combos(
        self,
        all: bool,
        carrier_list: list[protocols.Carrier] = AVAILABLE_CARRIERS,
    ) -> list[str] | list[tuple[str, list[str]]]:
        """
        SUMMARY: Gets either all combinations of available carriers within a list of strings, OR gets the correct string listing all redundant carriers for each and every redundant carrier group that are present in the provided carrier_list.

        ARGUMENTS:
            all: bool --
                get all carrier combinations or only the largest list within each provided group. All should be set to True for providing all carrier options in the settings tab of the view.

            carrier_list: list[Carrier] --
                list of the carriers to loop through

        TODO: Possibly extract into an appropriate model and split up into separate methods for testability.
        """
        combos: list[tuple[str, list[str]]] = []
        redundancies: dict[int, list[str]] = {}
        for carrier in carrier_list:
            if carrier.redundancy_group == 0:
                if all:
                    combos.append(carrier.name)
                else:
                    combos.append((carrier.name, [carrier.id]))
            if carrier.redundancy_group != 0:
                if carrier.redundancy_group not in redundancies:
                    redundancies[carrier.redundancy_group] = []
                redundancies[carrier.redundancy_group].append(carrier)
        for carriers in redundancies.values():
            ids = []
            _names = []
            for carrier in carriers:
                ids.append(carrier.id)
                _names.append(carrier.name)
            if all:
                count = len(_names)
                while count > 1:
                    for combo in itertools.combinations(_names, count):
                        sorted_combo = sorted(combo, reverse=True)
                        combos.append(
                            f'Combination: {" + ".join(sorted_combo)}',
                        )
                    count -= 1
            else:
                names = sorted(_names, reverse=True)
                combos.append((f'Combination: {" + ".join(names)}', ids))
        return combos

    def on_change_template(self, *args, **kwargs) -> None:
        """Updates template tab view when user changes template."""
        self._set_tab_placeholders(self.view_main.selected_template)

    def btn_save_view_tab(self, tab_name: str) -> bool:
        """Save current state of a given view tab to the config file."""
        config = open_config()
        if tab_name == "surplus lines":
            x = self.view_surplus_lines.output_path
            config.set(tab_name, "output_save_dir", x)
            return True
        elif tab_name == "quoteforms":
            row_data = self.view_main.reg_tv.get_all_rows()
            return qf_reg.process_save(
                row_data=row_data,
            )
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

    def on_focus_out(self, event) -> bool | None:
        """Replaces blank text on template tab with prior saved data
        from config. This is done because templates should never be blank."""
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

    def _assign_single_placeholder(self, carrier: str, widget_name: str) -> bool:
        config = open_config()
        placeholder = config.get(carrier, widget_name).value
        self.view_main.__setattr__(
            widget_name,
            placeholder,
        )
        return True

    ##############################################################
    #################   NEED TO REFACTOR BELOW   #################
    ##############################################################
    ### Begin Quoteform Registrations Tab ###
    def add_qf_registration(self):
        form_names = self.view_main.reg_tv.get_all_names()
        name = qf_reg.standardize_name(self.view_main.form_name)
        if qf_reg.validate_name(form_names, name):
            qf = protocols.Quoteform(
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
    ##############################################################
    ##############################################################
    ##############################################################

    ############# --Surplus Lines Automator-- #############
    def run_surplus_lines(self):
        output_dir = self.model_surplus_lines.output_dir()
        self.view_surplus_lines.make_view(
            presenter=self,
            view_interpreter=VIEW_INTERPRETER,
            view_palette=self.view_palette,
            output_dir=output_dir,
        )
        self.view_surplus_lines.root.mainloop()

    def process_SL_doc(self, event):
        doc_path = event.data.strip("{}")

        self.view_surplus_lines.root.destroy()
        try:
            self.model_surplus_lines.start(doc_path)
        except OutputDirNotSet:
            self.run_surplus_lines()
        else:
            toaster = ToastNotifier()
            toaster.show_toast(
                "SUCCESS! Your doc is now stamped.",
                "A new window will show you the finished file.",
                duration=5,
            )

    def save_sl_output_dir(self, event):
        _dir = event.data.strip("{}")
        self.model_surplus_lines.output_dir(new_dir=_dir)
        self._set_tab_placeholders(tab_name="surplus lines")

    ############# END --Surplus Lines Automator-- END #############

    ################ LOOK AT THE END #########################
