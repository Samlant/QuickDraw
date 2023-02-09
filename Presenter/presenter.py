from __future__ import annotations
import itertools
from ..Model.model import Model, ConfigWorker, EmailHandler, Envelope
from typing import Protocol
import win32com.client as win32


class View(Protocol):
    def create_GUI_obj(self) -> None:
        ...

    def start_main_loop(self) -> None:
        ...

    def setInitialView(self) -> None:
        ...

    def selected_template(self) -> str:
        ...

    def get_combo_checkbttns(self, possible_duplicates: list) -> str:
        ...

    def get_template_page_values(self) -> dict:
        ...
    
    def get_possible_redundancies(self) -> dict:
        ...

    def get_remaining_single_carriers(self) -> dict:
        ...

    def username(self,) -> str:
        ...
    
    def recipient(self, recipient: str) -> str:
        ...

    def greeting(self, greeting: str) -> str:
        ...
    
    def body(self, body: str) -> str:
        ...
    
    def salutation(self, salutation: str) -> str:
        ...
    
    def default_CC1(self, default_CC1: str) -> str:
        ...

    def default_CC2(self, default_cc2: str) -> str:
        ...

class ConfigWorker(Protocol):
    def get_value_from_config(self, request: dict) -> bool:
        ...

    def validate_section(self, section_name) -> bool: 
        ...

    def get_section(self, section_name) -> dict:
        ...

class Presenter:
    """ Creates a Presenter object that has the model & view 
    as attributes of itself. This is responsible for handling
    all interactions between user input and program logic.
    """
    def __init__(self, model: Model, view: View, configWorker: ConfigWorker) -> None:
        """ Sets the model & view to itself."""
        self.model = model
        self.view = view
        self.config_worker = configWorker

    def start_program(self) -> None:
        """ Starts the program by creating GUI object,
        configuring initial values,  then running it
        This also sets the default mail application.
        """
        self.view.create_GUI_obj(self)
        self.model.set_initial_view_values() #placeholders=work in progress
        self.view.start_main_loop()
        
        self.model.configWorker = self.model.c
        self.email_application = 'outlook.application'
        self.run_email_handler()

    def get_dropdown_options(self) -> list:
        return self.model.get_dropdown_options()

    def update_template_page(self, current_selection) -> None: #Complete if necessary - 02.09.2023
        payload = self.config_worker.get_section(current_selection)



    def get_selected_template(self) -> str:#GOOD
        """ Gets the current selection of the dropdown menu."""
        return self.view.selected_template()
    
    
    def save_path(self, raw_path, is_quoteform: bool) -> None:#GOOD
        """ Sends the raw path to model for saving."""
        self.config_worker.save_path(raw_path, is_quoteform)

    def save_extra_notes(self, notes: str) -> None:#GOOD
        self.model.save_extra_notes(input)

    def save_CC(self, cc_addresses) -> None:
        # Redo this function and how we save values.
        if self.model.check_cc_settings == False:
            self.model.save_CC(cc_addresses)
        else:
            pass

    def btnSaveMainSettings(self) -> None:
        save_contents = dict()
        def_CC1 = self.view.get_default_CC1()
        def_CC2 = self.view.get_default_CC2()
        save_contents.update({'default_CC1', def_CC1},
                             {'default_CC2', def_CC2}
                             )
        self.model.handle_save_contents('General settings', save_contents)

    def btnSendEmail(self) -> None:
        """ This starts the collection of data & sending of emails.
        It firsts gets a list of likely redundant submissions,  runs a redundancy-check,  and if true it creates the appropriate email template.""
        carrier_checkboxes_dict = dict(self.view.get_possible_redundancies())
        self.check_for_redundant_markets(carrier_checkboxes_dict)
        #work through fixing/preparing the redundant markets,  then...
        carrier_checkboxes_dict.update(self.view.get_remaining_single_carriers)
        if carrier_checkboxes_dict.values != 'submit':
            raise ValueError
        else:
            for carrier, value in carrier_checkboxes_dict:
                if value == 'submit':
                    pass
                elif
        #

        #check for redundancies:
        possbile_redundancies_dict = dict(self.view.get_possible_redundancies())

        if self.check_for_redundant_markets(redundancy_list) == True:
            self.fix_redundancies(carrier_checkboxes_dict)
        elif self.check_for_redundant_markets(redundancy_list) == False:
            pass
        else:
            raise ValueError


#       mail.CC = self.model.quoteform_path
#       mail.To = s

    def btnSaveEmailTemplate(self):
        pass


    def run_email_handler(self) -> None: #GOOD, currently being re-looked at.
        """ Instantiate an email handler to process requests"""
        self.outlook = win32.Dispatch(self.application)
        
    def create_email_item(self): #Re-EXAMINE and investigate
        mail_item = email()
    """ This creates the model,  which secures, validates, stores, and ultimately allocates data into an email object for sending away.
    """

    def reset_ui(self):
        """ This resets the view to start a clean, new submission."""
        self.view.variable_name


# PUT ALL FINAL FNs BELOW :)
# Start
    def get_template_page_values(self) -> dict:#GOOD
        payload = dict()
        payload.update({self.view.selected_template,
                        self.view.username,
                        self.view.recipient,
                        self.view.greeting,
                        self.view.body,
                        self.view.salutation}
                        )
        return payload
    
    def set_initial_placeholders(self):
        '''
        Sets the initial view for each field if applicable NOTE: Don't loop.
        '''
        pass

#BEGIN btnSendEmail functions :)

    def check_for_redundant_markets(self) -> bool: #GOOD
        """ Checks the redundancy list (after its creation in create_carrier_redundancy_list) for redundant submissions."""
        check_list = list()
        check_list
        if check_list.count('submit') > 1:
            return True
        elif check_list.count('submit') <= 1:
            return False
        else:
            raise ValueError()

    
    def fix_redundancies(self, carrier_checkboxes: dict) -> None: #GOOD
        #SW & PT submit!
        to_submit_list = list()
        for carrier, value in self.check_list:
            if value == 'submit':
                to_submit_list.append(carrier)
            elif value == 'pass':
                pass
            else:
                raise ValueError