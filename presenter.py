from model import Model
from typing import Protocol
import win32com.client as win32
from __future__ import annotations


class View(Protocol):
    def setInitialView(self) -> None:
        ...

    def clear_placeholder_content(self) -> None:
        ...
    
    def insert_placeholder_content(self) -> None:
        ...
    
    def savePath(self, event, isquoteform: bool) -> None:
        ...
        
    def save_extra_notes(self, input: str) -> None:
        ...

    def save_CC(self, input) -> None:
        ...

    def check_if_combo(self, name):
        ...
    
    def create_GUI_obj(self) -> None:
        ...

    def start_main_loop(self) -> None:
        ...

    def get_selected_template(self, selected_template: str) -> str:
        ...

    def get_username(self, username: str) -> str:
        ...
    
    def get_recipient(self, recipient: str) -> str:
        ...

    def get_greeting(self, greeting: str) -> str:
        ...
    
    def get_body(self, body: str) -> str:
        ...
    
    def get_salutation(self, salutation: str) -> str:
        ...
    
    def get_default_CC1(self, default_CC1: str) -> str:
        ...

    def get_default_CC2(self, default_cc2: str) -> str:
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

        email_handler = 'outlook.application'
        self.init_email_handler(email_handler)


    def getCurrentDropDownSelection(self) -> str:
        """ Gets the current selection of the email template 
        dropdown menu.
        """
        self.view.get_current_drop_down()

    def onFocusOut(self, item, current_dropdown_selection):
        pass
    
    def save_path(self, event, usage_type: bool ):
        """ Saves the path of the file."""
        self.model.save_path(event, usage_type)

    def save_extra_notes(self, notes: str) -> None:
        self.model.save_extra_notes(input)

    def save_CC(self, cc_addresses) -> None:
        # Redo this function and how we save values.
        if check_cc_settings == False:
            self.model.save_CC(cc_addresses)
        else:
            pass

    def check_if_combo(self):
        possible_duplicates_list = self.model.list_of_possible_duplicates
        input_dict = self.view.get_combo_checkbttns(possible_duplicates_list)
        self.model.check_if_duplicates_exist(input_dict)

    def btnSaveMainSettings(self):
        settings_dict = self.view.get_main_settings_values()
        self.model.save_main_settings(settings_dict)

    def btnSendEmail(self):
        pass
#       mail.CC = self.model.quoteform_path
#       mail.To = s

    def btnSaveEmailTemplate(self):
        pass






