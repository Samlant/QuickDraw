import itertools
from __future__ import annotations
from typing import Protocol

from ..Model.model import Model, ConfigWorker
from ..Model.email_handler import EmailHandler


class View(Protocol):
    def create_GUI_obj(self) -> None:
        ...

    def start_main_loop(self) -> None:
        ...

    def positive_submission_value(self):
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
    """ Creates a Presenter object that has the model, config_worker & view 
    as attributes of itself. This is responsible for handling
    all interactions between user input and program logic.
    """

    self.recipient = str
    self.CC_recipients = str
    self.subject = str
    self.greeting = str
    self.body = str
    self.salutation = str
    self.username = str

    def __init__(self, model: Model, view: View, configWorker: ConfigWorker) -> None:
        """ Sets the model, config_worker & view to itself."""
        self.model = model
        self.view = view
        self.config_worker = configWorker
        self.postman = self.email_handler.EmailHandler

    def start_program(self) -> None:
        """ Starts the program by creating GUI object,
        configuring initial values,  then running it
        This also sets the default mail application.
        """
        self.view.create_GUI_obj(self)
        self.model.positive_submission = self.view.positive_submission_value
        self.view.start_main_loop()        

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

    def btnSaveEmailTemplate(self):
        pass

    def reset_ui(self):
        """ This resets the view to start a clean, new submission."""
        self.view.variable_name

# PUT ALL FINAL FNs BELOW :)

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


    def btnSendEmail(self) -> None:
        """ This starts the collection of data & sending of emails.
        
        Some markets submit to the same email address,  so in order to combine those emails all into a single submission for all those applicable markets,  this function handles that situation first: it gets a dict from the view (hard-coded values) of likely redundant submissions, & then runs a redundancy-check. 

        
        If True, it deletes the existing values and assigns the correct data to the specific combination of redundant markets. 

        If False,  it proceeds to add the rest of the markets' checkboxes.

        
        Once the function knows which markets to submit to,  we create a loop that cycles through the desired markets. Each cycle represents an envelope & data for each submission is inputted---and subsequently sent.
        """
        carrier_checkboxes_dict = dict(self.view.get_possible_redundancies())
        carrier_checkboxes_dict = self.model.handle_redundancies(carrier_checkboxes_dict)
        carrier_checkboxes_dict.update(self.view.get_remaining_single_carriers)
        
        self.loop_through_envelopes(carrier_checkboxes_dict)


    def loop_through_envelopes(self, dict):
        for carrier, value in dict:
        if value == 'submit':
            carrier_details = self.config_worker.get_section(carrier)
            carrier_details[]
            # 
            # apply key names,
            # Once we have the necessary data, create the email envelope.   
                
        else:
            pass