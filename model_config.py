from configupdater import ConfigUpdater


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
        section = config.get_section(section_name)
        section = section.to_dict()
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
