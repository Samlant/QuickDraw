from dataclasses import dataclass

from configupdater import ConfigUpdater

from ..Presenter.presenter import Presenter


class Model:
    """ This is our model which handles validating, transforming, moving and storing data appropriately. 
    NOTE: any config interactions are routed to the Config class object.
    """
    #NOTE: change this LAST:  These are class vars bc we want to keep them until emails are sent...store in email obj not here.

    def __init__(self) -> None:
        self.positive_submission = None
        self.quoteform_path = str
        self.extra_attachments = []
    
    def handle_redundancies(self, carrier_checkboxes: dict) -> dict:
        if self.redundancy_check(carrier_checkboxes):
            section_name = str(self.fix_redundancies(carrier_checkboxes))
            new_single_submission = dict(section_name, 'submit') #hardcode value
            return new_single_submission
        else:
            return carrier_checkboxes
        
    def redundancy_check(self, carrier_checkboxes: dict) -> bool: #Recheck
        """ Checks the redundancy list that the view provides for duplicates."""
        check_list = list()
        # make into a list
        check_list.append(carrier_checkboxes.values()) 
        if check_list.count('submit') > 1:
            return True
        elif check_list.count('submit') <= 1:
            return False
        else:
            raise ValueError()
    
    def fix_redundancies(self, carrier_checkboxes: dict) -> str: #GOOD
        """ Receives a dict of name:boolean where it finds the two---or three---key:value pairs & then assigns the correct config section name.  This allows the program to access the proper data for the envelope to be sent.
        """
        section_name = str
        yes = 'submit'
        if (carrier_checkboxes['Sw'].value == yes) and (carrier_checkboxes['pt'].value == yes) and carrier_checkboxes['nh'].value == yes:
            section_name = 'Combination: Seawave, Prime Time and New Hampshire'
            return section_name
        elif (carrier_checkboxes['sw'].value == yes) and (carrier_checkboxes['pt'].value == yes):
            section_name = 'Combination: Seawave and Prime Time'
            return section_name
        elif (carrier_checkboxes['sw'].value == yes) and (carrier_checkboxes['nh'].value == yes):
            section_name = 'Combination: Seawave and New Hampshire'
            return section_name        
        elif (carrier_checkboxes['pt'].value == yes) and (carrier_checkboxes['nh'].value == yes):
            section_name = 'Combination: Prime Time and New Hampshire'
            return section_name
        else:
            raise ValueError

    def save_path(self, raw_path, is_quoteform: bool):#GOOD
        path = self.clean_path(raw_path)
        if is_quoteform == True:
            self.quoteform_path = path
        elif is_quoteform == False:
            self.extra_attachments.append(path)
        else:
            print('Raising type error: is_quoted parameter is either empty or wrong type. It needs to be boolean.')

    def clean_path(self, path) -> str:
        """ Cleans up the path str by removing any brackets---if present."""
        if '{' in path.data:
            path = path.data.translate({ord(c): None for c in '{}'})
        else:
            return path
        return path

    def get_all_attachments(self) -> list:
        attachments = []
        attachments.append(self.quoteform_path)
        attachments.append(self.extra_attachments)
        return attachments
    
    def list_to_str(self, input: list) - str:
        string = str
        for element in input:
            string += element
        return string
        
            
class ConfigWorker:
    """ This class handles all interactions between the python and config file. It utilizes open_config() as a helper to acces config, discerns the path of flowing information & then performs those queries on the config file.
    """

    def open_config(self) -> None: #GOOD
        """ This is a helper to read config when called using ConfigUpdater,  an improvement on configParser.
        """
        open_read_update = ConfigUpdater()
        open_read_update.read('configurations.ini')
        return open_read_update
    
    def get_value_from_config(self, request: dict) -> bool: #GOOD - prior name: get_config_value()
        """ This returns the value from config given a section:key dict."""
        worker = self.open_config()
        for section_name, key in request:
            return worker.get(section_name, key)
    
    def validate_section(self, section_name) -> bool: #GOOD
        """ Validates a given section name to ensure its existence in config."""
        config = self.open_config()
        if config.has_section(section_name):
            return True
        else:
            print('section_name validation failed within the ConfigWorker. Double-check input.')
            return False

    def get_section(self, section_name) -> dict: #GOOD
        """ This returns the section keys:values in a dict"""
        config = self.open_config()
        return config.get_section(section_name, 'Error section')
        
    # def handle_save_contents(self, section_name: str, save_contents: dict) -> bool: #NEED TO FINISH !!!
    #     """ This is a generic function to save both Save buttons' data to the appropriate config section. It also ensures the section exists.
    #     """
    #     config = self.open_config()
    #     if self.validate_section(section_name):
                

    #     for key, value in save_contents:
    #         config.update(section_name, key, value)
    # End of CONFIG FILE operations
