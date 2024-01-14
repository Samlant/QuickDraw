def assign_registration_name(config) -> str:
    counter = 1
    name = "Form_"
    test_name = f"{name}{counter}"
    while config._validate_section(test_name):
        counter += 1
        test_name = f"{name}{counter}"
    return test_name


# def check_if_duplicate(quoteform, config):
#     conf = config._open_config()
#     quoteform_names = [y for y in conf.sections() if "Form_" in y]

#     quoteforms: list[dict[str, str]] = []

#     for saved_quoteform in quoteform_names:
#         new_dict = {}
#         section = config.get_section(saved_quoteform)
#         options = section.items()
#         for x, y in options:
#             new_dict[x] = y.value
#         quoteforms.append(new_dict)

#     for saved_quoteform in quoteforms:
#         if quoteform == saved_quoteform:
#             return True
#         else:
#             continue
#     return False
