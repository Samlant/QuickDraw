from __future__ import annotations
import itertools
from typing import Protocol

from Model.model import Model
from Model.email_handler import EmailHandler

# from Model.email import EmailHandler


class View(Protocol):
    def create_UI_obj(self, presenter: Presenter) -> None:
        ...

    def mainloop(self) -> None:
        ...

    @property
    def positive_submission_value(self):
        ...

    @property
    def negative_submission_value(self):
        ...
    # get userinput for the envelope:

    @property
    def extra_notes(self) -> str:
        ...

    @property
    def selected_template(self) -> str:
        ...

    def userinput_CC1(self) -> str:
        ...

    def userinput_CC2(self) -> str:
        ...

    @property
    def ignore_default_cc(self) -> bool:
        ...

    @property
    def sw(self) -> str:
        ...

    @property
    def pt(self) -> str:
        ...

    @property
    def nh(self) -> str:
        ...

    @property
    def am(self) -> str:
        ...

    @property
    def km(self) -> str:
        ...

    @property
    def cp(self) -> str:
        ...

    @property
    def yi(self) -> str:
        ...

    @property
    def ce(self) -> str:
        ...

    @property
    def In(self) -> str:
        ...

    @property
    def tv(self) -> str:
        ...
    # get template/settings fields to save in config:

    def get_template_page_values(self) -> dict:
        ...

    @property
    def recipient(self, recipient: str) -> str:
        ...

    @property
    def greeting(self, greeting: str) -> str:
        ...

    @property
    def body(self, body: str) -> str:
        ...

    @property
    def salutation(self, salutation: str) -> str:
        ...

    @property
    def default_CC1(self, default_CC1: str) -> str:
        ...

    @property
    def default_CC2(self, default_cc2: str) -> str:
        ...

    @property
    def username(self) -> str:
        ...


class ConfigWorker(Protocol):
    def get_value_from_config(self, request: dict) -> bool:
        ...

    def get_section(self, section_name) -> dict:
        ...

    def handle_save_contents(self, section_name: str, save_contents: dict) -> bool:
        ...

    def check_to_skip_default_carboncopies(self) -> bool:
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
        self.model.negative_submission = self.view.negative_submission_value
        self.CC_recipients = str
        self.subject = str
        self.username = str

    def start_program(self) -> None:
        """Starts the program by creating GUI object,
        configuring initial values,  then running it
        This also sets the default mail application.
        """
        if self.view.create_UI_obj(self) and
        self.set_initial_placeholders() and
        self.view.mainloop():
        	return True
        else:
            raise Exception("Couldn't create UI object.")
        	

    def set_dropdown_options(self) -> list:
        return self.model.get_dropdown_options()

    # Complete if necessary - 02.09.2023
    def update_template_tab_on_changed_dropdown(self) -> None:
        """Updates the placeholders on customize_tab when dropdown changes
        
        Returns:
        	Bool -- returns a bool for success & for testing
        """
        selected_template = self.view.selected_template
        self.clear_customize_template_placeholders()
        payload = self.config_worker.get_section(selected_template)
        if self.insert_placeholders(payload):
            return True
        else:
            raise Exception("Could't update customize_tab upon changing.")

    def process_quoteform_path(self, raw_path) -> None:  # GOOD
        """Sends the raw path to model for proccessing & saving.
        
        Arguments: 
            raw_path {str} -- the raw str of full path of the file 
 
        Returns: 
            Tuple -- returns the path & a boolean for distinguishing 
            		  it apart from other attachments.
        """
        return self.model.save_path(raw_path, is_quoteform=True)

    def process_attachments_path(self, raw_path) -> None:
        """Sends the raw path of all extra attachments (not the 
        	quoteform) to model for proccessing & saving.
        
        Arguments: 
            raw_path {str} -- the raw str of full path of the file 
 
        Returns: 
            Tuple -- returns the path & a boolean for distinguishing 
            		  it apart from the client's quoteform.
        """
        return self.model.save_path(raw_path, is_quoteform=False)

    def _get_settings_values(self) -> dict:
        """Gets all userinput from the settings_tab.
        
        Returns:
    		Dict -- returns a dict of key-names as they 
            		appear in the config along with their 
                    userinput values
        """
        settings_dict = dict()
        settings_dict = {'default_CC1': self.view.default_CC1,
        				  'default_CC2': self.view.default_CC2,
        				  'username': self.view.username
                         }
        return settings_dict

    def btn_save_settings(self) -> None:
        """Calls a private getter method & saves output as a dict, 
        along with the section_name as it appears in config file
        
        Returns:
        	Str -- returns a string of the section_name as it 
            	   appears in the config file.
            Dict -- returns a dict of all userinput from settings_tab
        """
        settings_dict = self._get_settings_values()
        self.config_worker.handle_save_contents(
            'General settings', settings_dict)

    def btn_save_template(self) -> None:
        """Calls a private getter method & saves output as a dict, 
        along with the section_name as it appears in config file
        
        Returns:
        	Str -- returns a string of the section_name as it 
            	   appears in the config file.
            Dict -- returns a dict of all userinput from customize_tab
        """
        template_dict = self.get_template_page_values()
        section_name = template_dict.pop('selected_template')
        try:
            self.config_worker.handle_save_contents(
                section_name, template_dict)
        except:
            raise Exception("Couldn't save template_dict to config.")

    def reset_ui(self):
        """This resets the view to start a clean, new submission."""
        pass

    def on_focus_out(self):
        pass

    def get_possible_redundancies(self) -> dict:
        """This gets the values of the carriers' checkboxes that submit
        to the same email address. Separating this allows us to more
        easily update the list of likely redundancies.
        
        Returns:
        	Dict -- returns a dict of carrier checkbox values
        """
        possible_redundancies_dict = dict()
        if possible_redundancies_dict = {sw: self.view.sw,
                                     	  pt: self.view.pt,
                                      	  nh: self.view.nh
                                      	  }:
        	return possible_redundancies_dict
        else:
            raise Exception("Couldn't get carrier checkboxes saved into a dict.")

    def get_remaining_single_carriers(self) -> dict:
        """This gets the values of the carriers' checkboxes that 
        all submit to different, unique email addresses.
        
        Returns:
        	Dict -- returns a dict of carrier checkbox values
        """
        carrier_submissions_dict = dict()
        if carrier_submissions_dict = {'am': self.view.am,
                                   	'km': self.view.km,
                                    	'cp': self.view.cp,
                                    	'yi': self.view.yi,
                                    	'ce': self.view.ce,
                                    	'In': self.view.In,
                                    	'tv': self.view.tv
                                    	}:
        	return carrier_submissions_dict
        else:
            raise Exception("Couldn't get carrier checkboxes saved into a dict.")

    def get_template_page_values(self) -> dict:
        """This gets all userinput from the customize_tab
        
        Returns:
        	Dict -- returns a dict of the selected template and all
            		userinput from the template fields, each
                    assigned accordingly to their config file keys
        """
        customize_dict = dict()
        if customize_dict = {selected_template: self.view.selected_template,
                   	       recipient: self.view.recipient,
                   		   greeting: self.view.greeting,
                   		   body: self.view.body,
                   		   salutation: self.view.salutation
                   		   }:
        	return customize_dict
        else:
            raise Exception("Couldn't get customize_tab input saved into a dict.")

    def clear_customize_template_placeholders(self) -> None:
        """Clears all inputtable fields on the customize_tab"""
        del (self.view.recipient, self.view.greeting, self.view.body,
             self.view.salutation, self.view.username
             )
            
    def clear_settings_placeholders(self) -> None:
        """Clears all inputtable fields on the settings_tab"""
        del (self.view.default_CC1, self.view.default_CC2)

    def set_initial_placeholders(self) -> None:
        '''Sets the initial view for each input field, if applicable'''
        self.clear_customize_template_placeholders()
        self.clear_settings_placeholders()
        self.view.ignore_default_cc = self.config_worker.get_value_from_config(
            								{'section_name': 'General settings',
             								 'key': 'ignore_default_cc_addresses'
             								 })
        self.view.default_CC1 = self.config_worker.get_value_from_config(
            							{'section_name': 'General settings',
             							 'key': 'default_CC1'
             							 })
        self.view.default_CC2 = self.config_worker.get_value_from_config(
            							{'section_name': 'General settings',
             							 'key': 'default_CC2'
             							 })
        initial_placeholders_dict = self.config_worker.get_section(
            								'Default placeholders'
                                       	)
        self._set_customize_tab_placeholders(initial_placeholders_dict)

    def _set_customize_tab_placeholders(self, placeholder_dict: dict) -> None:
        """Sets the placeholders for the customizations_tab"""
        if (self.view.recipient = placeholder_dict['address'] and
        	self.view.greeting = placeholder_dict['greeting'] and
        	self.view.body = placeholder_dict['body'] and
        	self.view.salutation = placeholder_dict['salutation']):
            return True
        else:
            raise Exception("Couldn't set placeholders for the customize_tab")

    def _get_customize_tab_placeholders(self) -> dict:
        current_selection = self.view.selected_template
        return self.config_worker.get_section(current_selection)

    def btn_send_envelopes(self, autosend: bool) -> None:
        """ This collects all required data from both the config file and
        userinput, then 
        

        Some markets submit to the same email address,  so in order to combine
        those emails all into a single submission for all those applicable markets,
        this function handles that situation first: it gets a dict from the view
        of likely redundant submissions, & then runs the redundancy-check.

        Arguments:
        	autosend = {bool} If True, it deletes the existing values and assigns
            				   the correct data to the specific combination of
                              redundant markets.  If False, it proceeds to add the
                              rest of the markets' checkboxes without modifying

        Once the function knows which markets to submit to,  we create a loop that
        cycles through the desired markets. Each cycle represents an envelope & data
        for each submission is inputted---and subsequently sent.
        """
        

        raw_checkboxes_dict = self.get_remaining_single_carriers()
        filtered_submits_dict = self.model.filter_only_positive_submissions(
            raw_checkboxes_dict)

        finalized_submits_dict.update(filtered_submits_dict)
        self.loop_through_envelopes(finalized_submits_dict, autosend)

	def _handle_redundancies(self) -> dict:
        """Gets possible redundant carriers' checkbox values, filters to only keep
        positive submissions, then combines them into one submission
        
        Returns -- Dict: returns dict of a single, combined carrier submission
        """
        try:
        	raw_checkboxes_dict = self.get_possible_redundancies()
        	filtered_submits_dict = self.model.filter_only_positive_submissions(raw_checkboxes_dict)
            condensed_output = self.model.handle_redundancies(filtered_submits_dict)
        except:
        	raise Exception("Failed handling redundancies.")
        else:
        	return condensed_output
        
    def loop_through_envelopes(self, finalized_submits_dict: dict, autosend: bool):
        """ This loops through each submission;  it:
        (1) forms an envelope when a positive_submission is found,
        (2) gets and transforms needed data into each of its final formatted type and form,
        (3) applies the properly formatted data into each the envelope, and,
        (4) sends the envelope to the recipient, inclusive of all data. 
        """
        postman = EmailHandler()
        subject = str
        subject = postman.build_subject(self.model.quoteform_path)
        list_of_CC = self._handle_getting_CC_addresses()
        formatted_CC_str = self.model.list_of_CC_to_str(list_of_CC)

        for carrier_section_name, value in finalized_submits_dict:
            postman.create_envelope()

            carrier_config_dict = dict()
            carrier_config_dict = self.config_worker.get_section(
                carrier_section_name)

            recipient = carrier_config_dict.get('address')
            postman.greeting = carrier_config_dict.get('greeting')
            postman.body = carrier_config_dict.get('body')
            postman.extra_notes = self.view.extra_notes
            postman.salutation = carrier_config_dict.get('salutation')
            postman.username = self.view.username
            body_text = postman.build_HTML_body()
            attachments_list = list(self.model.get_all_attachments())

            postman.assign_recipient(recipient=recipient)
            postman.assign_CC(cc_addresses=formatted_CC_str)
            postman.assign_subject(subject=subject)
            postman.assign_body_text(body=body_text)
            for attachment_path in attachments_list:
                postman.assign_attachments(attachment_path)
            postman.send_envelope(autosend)

    def _handle_getting_CC_addresses(self) -> list:
        """Gets userinput of all CC addresses and adds the to a list. It then
        checks if it should ignore the default CC addresses set in config file
        or add them intothe list as well
        
        Returns:
        	List -- returns a list of all desired CC adresses
        """
        list_of_CC = list()
        userinput_CC1 = self.view.userinput_CC1
        userinput_CC2 = self.view.userinput_CC2
        list_of_CC.append(userinput_CC1)
        list_of_CC.append(userinput_CC2)
        if self.view.ignore_CC_defaults == False:
            if self.config_worker.check_to_skip_default_carboncopies() == False:
                default_CC_addresses = self.model.get_default_cc_addresses()
                list_of_CC.append(default_CC_addresses)
            else:
                pass
        else:
            pass
        return list_of_CC
