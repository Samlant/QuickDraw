def remove_all_sections(config, names: list[str]):
    conf = config._open_file()
    for name in names:
        conf.remove_section(name)
        
def standardize_name(name: str) -> str:
    return f"Form_{name}"
    
def validate_name(existing_names: list[str], names: str):
    if name in existing_names:
        return False
    else:
        return True
        