from __future__ import annotations
import itertools
from typing import Protocol

from Model.model import Model
from Model.email_handler import EmailHandler

# from Model.email import EmailHandler


class View(Protocol):
    extra_notes: str
    selected_template:str
    userinput_CC1: str
    userinput_CC2: str
    use_CC_defaults: bool
    sw: str
    pt: str
    nh: str
    am: str
    km: str
    cp: str
    yi: str
    ce: str
    In: str
    tv: str
    recipient: str
    greeting: str
    body: str
    salutation: str
    default_CC1: str
    default_CC2: str
    username: str
    
    def reset_attributes(self, positive_value, negative_value):
        ...
        
    def create_UI_obj(self, presenter: Presenter) -> None:
        ...

    def mainloop(self) -> None:
        ...

    def get_template_page_values(self) -> dict:
        ...


class ConfigWorker(Protocol):
    def get_value_from_config(self, request: dict) -> bool:
        ...

    def get_section(self, section_name) -> dict:
        ...

    def handle_save_contents(self, section_name: str, save_contents: dict) -> bool:
        ...

    def check_if_using_default_carboncopies(self) -> bool:
        ...


class Presenter:
    """ Creates a Presenter object that has the model, config_worker & view 
    as attributes of itself. This is responsible for handling
    all interactions between user input and program logic.
    """

    def __init__(self, model: Model, view: View,
                 config_worker: ConfigWorker
                 ) -> None:
        """Stores the model, config_worker & view to itself."""
        self.model = model
        self.view = view
        self.config_worker = config_worker

    def start_program(self) -> None:
        """Starts the program by creating GUI object,
        configuring initial values,  then running it
        This also sets the default mail application.
        """
        try:
            self.view.create_UI_obj(self)
            self.set_initial_placeholders()
            self.view.mainloop()
        except:
            raise Exception("Couldn't create UI object.")
        else:
            return True

    def set_dropdown_options(self) -> list:
        return self.model.get_dropdown_options()

    def btn_clear_attachments(self) -> None:
        self.model.extra_attachments = ''

    # Complete if necessary - 02.09.2023
    def on_change_template(self, *args, **kwargs) -> None:
        """Updates the placeholders on customize_tab when dropdown changes
        
        Returns:
        	Bool -- returns a bool for success & for testing
        """
        print ('these are args:')
        print(*args)
        print ('these are kwargs:')
        print (**kwargs)
        selected_template = self.view.selected_template
        print(f'this is the current template: {selected_template}')
        self.clear_customize_template_placeholders()
        payload = self.config_worker.get_section(selected_template)
        print(payload)
        self._set_customize_tab_placeholders(payload)
        #     return True
        # else:
        #     raise Exception("Could't update customize_tab upon changing.")

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


    def on_focus_out(self, field_name: str, current_text: str) -> bool:
        if current_text == '':
            config_section = self.view.selected_template
            try:
                if field_name == 'recipient':
                    self.view.recipient = self.config_worker.get_value_from_config(
                                            config_section)
                elif field_name == 'greeting':
                    self.view.greeting = self.config_worker.get_value_from_config(
                                            config_section)
                elif field_name == 'body':
                    self.view.body = self.config_worker.get_value_from_config(
                                        config_section)
                else:
                    field_name == 'salutation'
                    self.view.salutation = self.config_worker.get_value_from_config(
                                            config_section)
            except:
                raise Exception("Couldn't get & assign placeholder for customize_tab on focus out")
            else:
                return True

    def get_possible_redundancies(self) -> dict:
        """This gets the values of the carriers' checkboxes that submit
        to the same email address. Separating this allows us to more
        easily update the list of likely redundancies.
        
        Returns:
        	Dict -- returns a dict of carrier checkbox values
        """
        possible_redundancies_dict = dict()
        try:
            possible_redundancies_dict = {'sw': self.view.sw,
                                     	  'pt': self.view.pt,
                                      	  'nh': self.view.nh
                                      	  }
        except:
            raise Exception("Couldn't get carrier checkboxes saved into a dict.")
        else:
            return possible_redundancies_dict

    def get_remaining_single_carriers(self) -> dict:
        """This gets the values of the carriers' checkboxes that 
        all submit to different, unique email addresses.
        
        Returns:
        	Dict -- returns a dict of carrier checkbox values
        """
        carrier_submissions_dict = dict()
        try:
            carrier_submissions_dict = {'am': self.view.am,
                                   	    'km': self.view.km,
                                    	'cp': self.view.cp,
                                    	'yi': self.view.yi,
                                    	'ce': self.view.ce,
                                    	'In': self.view.In,
                                    	'tv': self.view.tv
                                    	}
        except:
            raise Exception("Couldn't get carrier checkboxes saved into a dict.")
        else:
            return carrier_submissions_dict

    def get_template_page_values(self) -> dict:
        """This gets all userinput from the customize_tab
        
        Returns:
        	Dict -- returns a dict of the selected template and all
            		userinput from the template fields, each
                    assigned accordingly to their config file keys
        """
        customize_dict = dict()
        try:
            customize_dict = {'selected_template': self.view.selected_template,
                              'recipient': self.view.recipient,
                              'greeting': self.view.greeting,
                              'body': self.view.body,
                              'salutation': self.view.salutation
                              }
        except:
            raise Exception("Couldn't get customize_tab input saved into a dict.")
        else:
            return customize_dict

    def clear_customize_template_placeholders(self) -> None:
        """Clears all inputtable fields on the customize_tab"""
        del self.view.recipient
        del self.view.greeting
        del self.view.body
        del self.view.salutation
            
    def clear_settings_placeholders(self) -> None:
        """Clears all inputtable fields on the settings_tab"""
        del self.view.default_CC1
        del self.view.default_CC2
        del self.view.username

    def set_initial_placeholders(self) -> None:
        '''Sets the initial view for each input field, if applicable'''
        self.clear_customize_template_placeholders()
        self.clear_settings_placeholders()
        self.view.use_CC_defaults = self.config_worker.get_value_from_config(
            								{'section_name': 'General settings',
             								 'key': 'use_default_CC_addresses'
             								 })
        self.view.username = self.config_worker.get_value_from_config(
            {'section_name': 'General settings', 'key': 'username'}
        )
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
        try:
            self.view.recipient = placeholder_dict.pop('address')
            self.view.greeting = placeholder_dict.pop('greeting')
            self.view.body = placeholder_dict.pop('body')
            self.view.salutation = placeholder_dict.pop('salutation')
        except:
             raise Exception("Couldn't set placeholders for the customize_tab")
        else:
            return True
            
    def _get_customize_tab_placeholders(self) -> dict:
        current_selection = self.view.selected_template
        return self.config_worker.get_section(current_selection)

    def btn_view_template(self) -> None:
        selected_template = self.view.selected_template
        postman = EmailHandler()
        letter = postman.create_letter()
        subject = f"Test view of the template for {selected_template}"
        postman.greeting = self.view.greeting
        postman.body = self.view.body
        postman.extra_notes = self.view.extra_notes
        postman.salutation = self.view.salutation
        postman.username = self.config_worker.get_value_from_config(
        							'General setiings', 'username'
                                    )
        body_text = postman.build_HTML_body(
            greeting=self.view.greeting,
            body = self.view.body,
            extra_notes = self.view.extra_notes,
            salutation = self.view.salutation
            )
        letter.To = self.view.recipient
        letter.Subject = subject
        letter.HTMLBody = body_text
        postman.send_letter(autosend=False)

    def btn_send_envelopes(self, autosend: bool) -> None:
        """This gets and checks which markets to prepare a ubmission to; it first
        keeps most carriers that we'll submit to,  although there are a few that
        use the same email address, so this then handles those markets by
        transforming them into a single submission. This data is then sent to be
        looped through and emailed away.

        Arguments:
        	autosend = {bool} 
                NOTE: If True, no window will be shown and all emails
                will be sequentially sent. If False, a window will be shown for
                each email prior to sending.
        """
        submission_dict = self._handle_single_markets()
        fixed_redundancies_dict = self._handle_redundancies()
        submission_dict.update(fixed_redundancies_dict)
        #try:
        self.loop_through_envelopes(submission_dict, autosend)
        #except:
        #    raise Exception("Error while looping through envelopes.")
        #else:
        #    return True

    def _handle_single_markets(self) -> dict:
        """Gets possible redundant carriers' checkbox values, filters to only keep
        positive submissions, then combines them into one submission
        
        Returns -- Dict: returns dict of a single, combined carrier submission
        """
        try:
            raw_dict = self.get_remaining_single_carriers()
            processed_dict = self.model.filter_only_positive_submissions(raw_dict)
        except:
            raise Exception("Failed getting or filtering the single markets.")
        else:
            return processed_dict
            
    def _handle_redundancies(self) -> dict:
        """Gets possible redundant carriers' checkbox values, filters to only keep
        positive submissions, then combines them into one submission
        
        Returns -- Dict: returns dict of a single, combined carrier submission
        """
        try:
            raw_dict = self.get_possible_redundancies()
            filtered_dict = self.model.filter_only_positive_submissions(raw_dict)
            processed_dict = self.model.handle_redundancies(filtered_dict)
        except:
            raise Exception("Failed handling redundancies.")
        else:
            return processed_dict
        
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
            letter = postman.create_letter()

            carrier_config_dict = dict()
            carrier_config_dict = self.config_worker.get_section(
                carrier_section_name)

            letter.To = carrier_config_dict.pop('address')
            letter.CC = formatted_CC_str
            letter.Subject = subject

            extra_notes = self.view.extra_notes
            body_text = self.model.build_HTML_body(
                carrier_config_dict, extra_notes
                )
            letter.HTMLBody = body_text

            attachments_list = list(self.model.get_all_attachments())
            for attachment_path in attachments_list:
                letter.Attachments.Add(attachment_path)
            if autosend:
                letter.Send()
            elif autosend == False:
                letter.Display()
            else:
                raise ValueError
            #postman.send_letter(autosend)

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
        print(self.view.use_CC_defaults)
        print(self.view.extra_notes)
        if self.view.use_CC_defaults == True:
            if self.config_worker.check_if_using_default_carboncopies() == True:
                default_CC_addresses = self.model.get_default_cc_addresses()
                list_of_CC.append(default_CC_addresses)
            else:
                pass
        else:
            pass
        return list_of_CC
