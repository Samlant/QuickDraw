from presenter import Presenter
            


class Model:
    
    def set_options(self):
        pass
        
    
    self.list_of_options = list('Seawave',
                                'Prime Time',
                                'New Hampshire',
                                'American Modern',
                                'Kemah', 'Concept Special Risks',
                                'Yachtinsure',
                                'Century',
                                'Intact',
                                'Travelers',
                                'Combination: Seawave and Prime Time',
                                'Combination: Seawave and New Hampshire',
                                'Combination: Prime Time and New Hampshire',
                                'Combination: Seawave, Primetime and New Hampshire'
                                )
    
    
    def init_email_handler(self, application: str) -> None:
        """ Instantiate an email handler to process requests"""
        self.outlook = win32.Dispatch(application)
        
    def create_email_item(self):
        mail_item = email()
    """ This creates the model,  which secures, validates, stores, and ultimately allocates data into an email object for sending away.
    """
    #These are class vars bc we want to keep them until emails are sent.
    self.quoteform_path = str
    self.extra_attachments = []
    self.attachments = []
    self.extra_notes = str
    self.subject = str
    self.cc_addresses = []

    

    def set_initial_view_values(self):
        ''' Set the entries and textboxes on the 
        template page to disabled since the default 
        drop-down isn't a valid choice.
        '''
        #getPlaceHolder(list)
        #insertPlaceholder(list)

        self.view.carrier_address.insert(0, carrier_address_placeholder)
        self.view.carrier_address.configure(state='disabled')
        self.view.carrier_greeting.insert(0, carrier_greeting_placeholder)
        self.view.carrier_greeting.configure(state='disabled')
        self.view.carrier_body.insert(1.0, carrier_body_placeholder)
        self.view.carrier_body.configure(state='disabled', wrap='word')
        self.view.carrier_salutation.insert(0, carrier_salutation_placeholder)
        self.view.carrier_salutation.configure(state='disabled')
        # REPLACE BELOW LINES' functions by creating & using some in this presenter class. Remain basic and use multiple if needed...
        self.view.your_name_focus_out = your_name.bind('<FocusOut>', lambda x: on_focus_out_entry(your_name, 'name'))
        self.view.carrier_address_focus_out = carrier_address.bind('<FocusOut>', lambda x: on_focus_out_entry(carrier_address, 'address'))
        self.view.carrier_greeting_focus_out = carrier_greeting.bind('<FocusOut>', lambda x: on_focus_out_entry(carrier_greeting, 'greeting'))
        self.view.carrier_body_focus_out = carrier_body.bind('<FocusOut>', lambda x: on_focus_out_text(carrier_body, 'body'))
        self.view.carrier_salutation_focus_out = carrier_salutation.bind('<FocusOut>', lambda x: on_focus_out_entry(carrier_salutation, 'salutation'))


    def onFocusOut(self, field_item):
        section_name = self.model.assignCorrectCarrierNames(dropdown_email_template.get())
        # Replace above line with below function that gets the current selection for dropdown_email_template
        # current_selection = self.view.getCurrentDropdownSelection()
        
        # Then, assign same section name that's in the config file
        # section_name = self.AssignCorrectSectionName(current_selection)
        if section_name[0] != 'Select Carrier':
            # Put placeholder txt & index_variable (to tell if it's entry or text widget: 0 or '1.0') in a tuple.
            placeholder_tuple = getPlaceholders(section_name, 'entry', field_name)
            if entry.get() == "":
            # The below uses either '1.0' or 0 for the index to insert txt at.
                entry.insert(placeholder_tuple[1], placeholder_tuple[0])
        else:
            print(f"On ENTRY_focus out, the section_name is: {section_name}")

    def savePath(self, raw_path, is_quoteform: bool):
        path = self.__validatePath(raw_path)
        if is_quoteform == True:
            self.quoteform_path = path
        elif is_quoteform == False:
            self.extra_attachments.append(path)
        else:
            print('Raising type error: is_quoted parameter is either empty or wrong type. It needs to be boolean.')
    
    def save_extra_notes(self, notes: str):
        self.extra_notes = notes

    def getAllAttachments(self) -> list:
         self.attachments.append(self.quoteform_path)
         self.attachments.append(self.extra_attachments)
         return self.attachments

    def __validatePath(self, path) -> str:
        """ Checks if brackets exists and removes if so."""
        if '{' in path.data:
            path = path.data.translate({ord(c): None for c in '{}'})
        else:
            return None
        return path
    
    def check_if_duplicates_exist(self, input: dict):
        num = self.count_list(input)
        check_bool = self.check_list(num)
        if check_bool:
            list = self.add_submits_to_list(input)
            section_name = self.get_correct_combination(list)
            var1 = self.get_config_value(section_name, 'address')
            var2 = self.get_config_value(section_name, 'body')
            self.assign_correct_combination(list)
        elif not check_bool:
            pass
        else:
            print('This model function did not perform as expected.')
            return None

    def get_correct_combination(self, input:list) -> str:
        if num == 2:
            output_str = f"Combination: {input[0]} and {input[1]}"
            return output_str
        elif num == 3:
            output_str = f"Combination: {input[0]} and {input[1]} and {input[2]}"
            return output_str
        else:
            print('Not offering four combo markets- check this model function for errors in unexpected input.')
            return None

    def check_list(self, num: int) -> bool:
        if num > 1:
            return True
        elif num <= 1:
            return False
        else:
            print('This model function failed to count.')
            return None

    def count_list(self, input:dict) -> int:
        return input.items().count('Submit')
    
    def add_submits_to_list(self, input: dict) -> list:
        submitting_list = list()
        for carrier, result in input:
            if result == 'Submit':
                submitting_list.append(carrier)
            elif result == 'skip':
                pass
            else:
                print('this model function did not receive input as expected.')
        return submitting_list
    def get_config_value(self, section_name)
    def saveCC(self, input):
         #check if ignore defaults
         pass

class email:
    """ Creates an email object with necessary attributes."""
    def __init__(self, 
            recipient: str,
            cc: str,
            subject: str,
            body: str,
            attachment_paths: list,
            ) -> None:
        self.email_item = self.outlook.CreateItem(0)
        self.assign_recipient()
        self.assign_CC()
        self.assign_subject()
        self.assign_body_text()
        self.assign_attachments()

    def assign_recipient(self):
        pass

    def assign_CC(self):
        pass

    def assign_subject(self):
        pass

    def assign_body_text(self):
        pass
    #This function is complete (assignAttachments)
    def assignAttachments(self):
        attachment_paths_list = self.model.attachments
        mail.Attachments.Add(attachment_paths_list)