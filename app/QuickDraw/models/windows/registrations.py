from QuickDraw.helper import open_config
from QuickDraw.models.submission.quoteform import Quoteform

FORM_PREFIX = "Form_"


def process_save(row_data) -> bool:
    "Clear's exisiting quoteforms that are saved in the config file,  then saves all rows within treeview into the config file."
    config = open_config()
    config = _remove_all_sections(config)
    _add_treeview_data_into_conf(config, row_data)
    return True

def process_retrieval() -> list[Quoteform]:
    config = open_config()
    quoteform_names = __get_all_names_from_conf(config)
    forms: list[Quoteform] = []
    for name in quoteform_names:
        section = config.get_section(name)
        options = section.items()
        form = Quoteform(
                    name,
                    options[0][1].value,
                    options[1][1].value,
                    options[2][1].value,
                    options[3][1].value,
                    options[4][1].value,
                )
        forms.append(form)
    return forms

def _remove_all_sections(config):
    "Removes all existing quoteforms within config to start with a clean slate."
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
