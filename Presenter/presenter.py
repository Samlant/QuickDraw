from __future__ import annotations
from model import Model, ConfigWorker, EmailHandler, Envelope
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
    #THESE ARE KEPT FOR PLACEHOLDERS WHEN IMPLEMENTED
    def assign_placeholders(self, payload: dict) -> None:
        ...

    def clear_placeholder_content(self) -> None:
        ...
    
    def insert_placeholder_content(self) -> None:
        ...
    #END OF PLACEHOLDER PLACEHOLDERS -haha
    def savePath(self, event, isquoteform: bool) -> None:
        ...
        
    def save_extra_notes(self, input: str) -> None:
        ...

    def save_CC(self, input) -> None:
        ...

    def check_if_combo(self) -> bool: #All above, excluding placeholders, are GOOD
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


    


class Presenter:
    """ Creates a Presenter object that has the model & view 
    as attributes of itself. This is responsible for handling
    all interactions between user input and program logic.
    """
    def __init__(self, model: Model, view: View) -> None:
        """ Sets the model & view to itself."""
        self.model = model
        self.view = view

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

    def update_template_page(self, current_selection) -> None:
        payload = self.model.get_section(current_selection)



    def get_selected_template(self) -> str:#GOOD
        """ Gets the current selection of the dropdown menu."""
        return self.view.selected_template()
    
    
    def save_path(self, raw_path, is_quoteform: bool) -> None:#GOOD
        """ Sends the raw path to model for saving."""
        self.model.save_path(raw_path, usage_type)

    def save_extra_notes(self, notes: str) -> None:#GOOD
        self.model.save_extra_notes(input)

    def save_CC(self, cc_addresses) -> None:
        # Redo this function and how we save values.
        if check_cc_settings == False:
            self.model.save_CC(cc_addresses)
        else:
            pass

    def check_if_combo(self):
        """ This is responsible for checking if there is a duplicate submission."""
        possible_duplicates_list = self.model.list_of_possible_duplicates
        input_dict = self.view.get_combo_checkbttns(possible_duplicates_list)
        self.model.check_if_duplicates_exist(input_dict)

    def get_list_of_duplicate_markets(self) -> list:
        """This is responsible for maintaining the list of possible duplicate submission markets.
        """
        list_of_possible_duplicates = list('Seawave',
                                            'Prime Time',
                                            'New Hampshire'
                                            )
        return list_of_possible_duplicates

    def btnSaveMainSettings(self) -> None:
        save_contents = dict()
        def_CC1 = self.view.get_default_CC1()
        def_CC2 = self.view.get_default_CC2()
        save_contents.update({'default_CC1', def_CC1},
                             {'default_CC2', def_CC2}
                             )
        self.model.handle_save_contents('General settings', save_contents)

    def btnSendEmail(self):
        pass
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

def get_all_carrier_checkboxes(self) -> dict:#GOOD
    payload_dict = {}
    payload_dict.update({'sw', self.sw},
                        {'pt', self.pt},
                        {'nh', self.nh},
                        {'am', self.am},
                        {'km', self.km},
                        {'cp', self.cp},
                        {'yi', self.yi},
                        {'ce', self.ce},
                        {'In', self.In},
                        {'in', self.tv},
                        )
    return payload_dict