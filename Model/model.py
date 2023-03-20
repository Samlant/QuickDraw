from dataclasses import dataclass

from configupdater import ConfigUpdater, Section


class Model:
    """This is our model which handles validating, transforming, moving and storing data appropriately.
    NOTE: any config interactions are routed to the Config class object.
    """

    # NOTE: change this LAST:  These are class vars bc we want to keep them until emails are sent...store in email obj not here.

    def __init__(self, positive_value, negative_value) -> None:
        self.yes = positive_value
        self.no = negative_value
        self.quoteform_path = ""
        self.extra_attachments = []

    def get_dropdown_options(self) -> list:
        return [
            "Seawave",
            "Prime Time",
            "New Hampshire",
            "American Modern",
            "Kemah Marine",
            "Concept Special Risks",
            "Yachtinsure",
            "Century",
            "Intact",
            "Travelers",
        ]

    def filter_only_positive_submissions(self, raw_checkboxes: dict) -> dict:
        checkboxes_dict = raw_checkboxes.copy()
        for x in raw_checkboxes:
            if raw_checkboxes[x] == self.no:
                checkboxes_dict.pop(x)
            elif raw_checkboxes[x] == self.yes:
                pass
            else:
                raise ValueError
        return checkboxes_dict

    def handle_redundancies(self, filtered_submits_dict: dict) -> dict:
        if self._redundancy_check(filtered_submits_dict):
            section_name_value = str(self._fix_redundancies(filtered_submits_dict))
            eliminated_redundancies = {
                "section_name": section_name_value,
                "key": self.yes,
            }
            return eliminated_redundancies
        else:
            return filtered_submits_dict

    def _redundancy_check(self, filtered_submits_dict: dict) -> bool:
        """Counts the number of items in the dictionary supplied. NOTE: the dict input should already be filtered and be a positive submission."""
        if len(filtered_submits_dict) > 1:
            return True
        elif len(filtered_submits_dict) <= 1:
            return False
        else:
            raise ValueError()

    def _fix_redundancies(self, filtered_submits_dict: dict) -> str:  # GOOD
        """Receives a dict of name:boolean where it finds the two---or three---key:value pairs & then assigns the correct config section name.  This allows the program to access the proper data for the envelope to be sent."""
        section_name = str
        yes = self.yes
        if (
            (filtered_submits_dict["sw"] == yes)
            and (filtered_submits_dict["pt"] == yes)
            and (filtered_submits_dict["nh"] == yes)
        ):
            section_name = "Combination: Seawave, Prime Time and New Hampshire"
            return section_name
        elif (filtered_submits_dict["sw"] == yes) and (
            filtered_submits_dict["pt"] == yes
        ):
            section_name = "Combination: Seawave and Prime Time"
            return section_name
        elif (filtered_submits_dict["sw"] == yes) and (
            filtered_submits_dict["nh"] == yes
        ):
            section_name = "Combination: Seawave and New Hampshire"
            return section_name
        elif (filtered_submits_dict["pt"] == yes) and (
            filtered_submits_dict["nh"] == yes
        ):
            section_name = "Combination: Prime Time and New Hampshire"
            return section_name
        else:
            pass

    def save_path(self, raw_path, is_quoteform: bool) -> bool:
        try:
            path = self._clean_path(raw_path)
        except:
            error = f'cannot clean the path of the file; input was: "{raw_path}"'
            raise Exception(error)
        else:
            if is_quoteform == True:
                self.quoteform_path = path
                return True
            elif is_quoteform == False:
                self.extra_attachments.append(path)
                return True
            else:
                raise Exception("Type of param:is_quoteform is wrong or empty.")

    def _filter_out_brackets(self, path) -> str:
        """Cleans up the path str by removing any brackets---if present."""
        if "{" in path.data:
            path = path.data.translate({ord(c): None for c in "{}"})
        return path

    def get_all_attachments(self) -> list:
        attachments = []
        attachments.append(self.quoteform_path)
        attachments.append(self.extra_attachments)
        return attachments

    def list_of_CC_to_str(self, input_list: list) -> str:
        """Transforms lists into strings. In-use for CC_address assignment."""
        input_list = "; ".join(str(element) for element in input_list)
        return input_list

    def get_default_cc_addresses(self):
        list_of_CC = list()
        if self.check_if_ignore_default_cc_is_on() == False:
            default_cc1 = ConfigWorker.get_value_from_config(
                dict("General settings", "default_cc1")
            )
            default_cc2 = ConfigWorker.get_value_from_config(
                dict("General settings", "default_cc2")
            )
            list_of_CC.append(default_cc1, default_cc2)
            return list_of_CC
        else:
            return None


class ConfigWorker:
    """This class handles all interactions between the python and config file. It utilizes open_config() as a helper to acces config, discerns the path of flowing information & then performs those queries on the config file."""

    def open_config(self) -> None:  # GOOD
        """This is a helper to read config when called using ConfigUpdater,  an improvement on configParser."""
        open_read_update = ConfigUpdater()
        open_read_update.read("configurations.ini")
        return open_read_update

    # GOOD - prior name: get_config_value()
    def get_value_from_config(self, request: dict) -> any:
        """This returns the value from config given a section_name:key dict."""
        config = self.open_config()
        section_name = request["section_name"]
        key = request["key"]
        result = config.get(section_name, key).value
        return result

    def _validate_section(self, section_name) -> bool:  # GOOD
        """Validates a given section name to ensure its existence in config."""
        config = self.open_config()
        if config.has_section(section_name):
            return True
        else:
            print(
                "section_name validation failed within the ConfigWorker. Double-check input."
            )
            return False

    def get_section(self, section_name) -> dict:  # GOOD
        """This returns the section keys:values in a dict"""
        config = self.open_config()
        section = config.get_section(section_name).to_dict()
        return section

    def handle_save_contents(self, section_name: str, save_contents: dict) -> bool:
        """This is a generic function to save both Save buttons' data to the appropriate config section. It also ensures the section exists."""
        config = self.open_config()
        if self._validate_section(section_name):
            for option, value in save_contents.items():
                try:
                    config[section_name][option] = value
                except:
                    raise Exception("Couldn't assign save_contents dict to config file")
            try:
                config.update_file()
            except:
                raise Exception("Couldn't save file")

    def check_if_using_default_carboncopies(self) -> bool:
        section_name_value = "General settings"
        key = "ignore_default_cc_addresses"
        config = {"section_name": section_name_value, "key": key}
        try:
            result = self.get_value_from_config(config)
        except:
            raise KeyError("Couldn't access config with values")
        else:
            return result

    # End of CONFIG FILE operations
