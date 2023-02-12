import itertools
from __future__ import annotations
from typing import Protocol

from ..Model.model import Model, ConfigWorker
from ..Model.email import EmailHandler


class View(Protocol):
    def create_GUI_obj(self) -> None:
        ...
    def start_main_loop(self) -> None:
        ...
    def positive_submission_value(self):
        ...

    # get checkbox values:
    def get_possible_redundancies(self) -> dict:
        ...
    def get_remaining_single_carriers(self) -> dict:
        ...

    # get userinput for the envelope:
    def extra_notes(self) -> str:
        ...
    def selected_template(self) -> str:
        ...
    def userinput_CC1(self) -> str:
        ...
    def userinput_CC2(self) -> str:
        ...
    def ignore_default_cc(self) -> bool:
        ...

    # get template/settings fields to save in config:    
    def get_template_page_values(self) -> dict:
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

    def __init__(self, model: Model, view: View, configWorker: ConfigWorker) -> None:
        """ Sets the model, config_worker & view to itself, then necessary instance vars.
        """
        self.model = model
        self.view = view
        self.config_worker = configWorker
        self.model.positive_submission = self.view.positive_submission_value
        self.CC_recipients = str
        self.subject = str
        self.username = str

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
    
    def save_path(self, raw_path, is_quoteform: bool) -> None:#GOOD
        """ Sends the raw path to model for saving."""
        self.config_worker.save_path(raw_path, is_quoteform)

    def save_CC(self, cc_addresses) -> None:
        # Redo this function and how we save values.
        if self.model.check_cc_settings == False:
            self.model.save_CC(cc_addresses)
        else:
            pass

    def handle_save_settings(self) -> None:
        cc_dict = dict()
        cc_dict.update('default_CC1', self.view.default_CC1)
        cc_dict.update('default_CC2', self.view.default_CC2)
        self.model.handle_save_contents('General settings', cc_dict)

    def btnSaveEmailTemplate(self):
        pass

    def reset_ui(self):
        """ This resets the view to start a clean, new submission."""
        pass

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
        positive_submissions_dict = self.model.filter_only_positive_submissions(carrier_checkboxes_dict)
        self.loop_through_envelopes(positive_submissions_dict)
    
    def loop_through_envelopes(self, positive_submissions_dict: dict):
        """ This loops through each submission;  it:
        (1) forms an envelope when a positive_submission is found,
        (2) gets and transforms needed data into each of its final formatted type and form,
        (3) applies the properly formatted data into each the envelope, and,
        (4) sends the envelope to the recipient, inclusive of all data. 
        """
        postman = EmailHandler()
        subject = str
        subject = postman.build_subject(self.model.quoteform_path)
        string_of_CC = str
        string_of_CC = NotImplemented

        for carrier_section_name, value in positive_submissions_dict:
            postman.create_envelope()

            carrier_config_dict = dict()
            carrier_config_dict = self.config_worker.get_section(carrier_section_name)

            recipient = carrier_config_dict.get('address')
                
            postman.greeting = carrier_config_dict.get('greeting')
            postman.body = carrier_config_dict.get('body')
            postman.extra_notes = self.view.extra_notes
            postman.salutation = carrier_config_dict.get('salutation')
            postman.username = self.view.username
            body_text = postman.build_HTML_body()    
                
            postman.assign_recipient(recipient=recipient)
            postman.assign_CC(cc_addresses=string_of_CC)
            postman.assign_subject(subject=subject)
            postman.assign_body_text(body=body_text)

            for attachment_path in attachment_list:
                postman.assign_attachments(attachment_path)
            
    def prepare_attachments(self) -> None:
        return self.model.get_all_attachments()
    
    def assign_from_config_to_envelope(self, carrier_config_section_dict: dict) -> None:
        greeting = 
