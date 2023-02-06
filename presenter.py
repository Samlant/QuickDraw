from __future__ import annotations
from model import Model
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

        email_handler = 'outlook.application'
        self.init_email_handler(email_handler)

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
        possible_duplicates_list = self.model.list_of_possible_duplicates
        input_dict = self.view.get_combo_checkbttns(possible_duplicates_list)
        self.model.check_if_duplicates_exist(input_dict)

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






