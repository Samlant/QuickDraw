FORM_PREFIX = "Form_"

def process_save(config, row_data):
    "Clear's exisiting quoteforms that are saved in the config file,  then saves all rows within treeview into the config file."
    config = _remove_all_sections(config)
    _add_treeview_data_into_conf(config, row_data)
    
def _remove_all_sections(config):
    "Removes all existing qutoeforms within config to start with a clean slate."
    names = __get_all_names_from_conf(config)
    for name in names:
        config.remove_section(name)
    config.update_file()
    return config
        

def __get_all_names_from_conf(config) -> list[str]:
    "Retrieves all names of quoteforms from the config file."
    return [y for y in config.sections() if FORM_PREFIX in y]
    
def _add_treeview_data_into_conf(config, row_data):
    "Adds all entries in treeview into the config file."
    for row in row_data:
        config["Seawave"].add_before.section(row[0]).space(1)
        config[row[0]]["fname"] = row[1]
        config[row[0]]["lname"] = row[2]
        config[row[0]]["year"] = row[3]
        config[row[0]]["vessel"] = row[4]
        config[row[0]]["referral"] = row[5]
        config.update_file()

def standardize_name(name: str) -> str:
    "Assigns a prefix to identify all quoteforms properly within the config file."
    return f"{FORM_PREFIX}{name}"
    
def validate_name(existing_names: list[str], name: str):
    "Ensures a duplicate name is not assigned."
    if name in existing_names:
        return False
    else:
        return True
        