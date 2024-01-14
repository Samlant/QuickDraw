FORM_PREFIX = "Form_"

def process_save(config, row_data):
    config = _remove_all_sections(config)
    _add_treeview_data_into_conf(config, row_data)
    
def _remove_all_sections(config):
    names = __get_all_names_from_conf(config)
    for name in names:
        config.remove_section(name)
    config.update_file()
    return config
        

def __get_all_names_from_conf(config) -> list[str]:
    return [y for y in config.sections() if FORM_PREFIX in y]
    
def add_treeview_data_into_conf(config, row_data):
    for row in row_data:
        config["Seawave"].add_before.section(row[0]).space(1)
        config[row[0]]["fname"] = row[1]
        config[row[0]]["lname"] = row[2]
        config[row[0]]["year"] = row[3]
        config[row[0]]["vessel"] = row[4]
        config[row[0]]["referral"] = row[5]
        config.update_file()

def standardize_name(name: str) -> str:
    return f"{FORM_PREFIX}{name}"
    
def validate_name(existing_names: list[str], names: str):
    if name in existing_names:
        return False
    else:
        return True
        