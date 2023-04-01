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
            "Combination: Seawave + Prime Time + New Hampshire",
            "Combination: Prime Time + New Hampshire",
            "Combination: Seawave + New Hampshire",
            "Combination: Seawave + Prime Time",
        ]

    def filter_only_positive_submissions(self, raw_checkboxes: dict) -> list:
        checkboxes_dict = raw_checkboxes.copy()
        for x in raw_checkboxes:
            if raw_checkboxes[x] == self.no:
                checkboxes_dict.pop(x)
            elif raw_checkboxes[x] == self.yes:
                pass
            else:
                raise ValueError
        checkboxes_list = []
        for x in checkboxes_dict.keys():
            checkboxes_list.append(x)
        return checkboxes_list

    def handle_redundancies(self, filtered_submits: list) -> str:
        """Checks if multiple redundant markets are present,  then combines them & returns the appropriate config section name"""
        if self._redundancy_check(filtered_submits):
            section_name = str(self._fix_redundancies(filtered_submits))
            return section_name
        else:
            if len(filtered_submits) == 0:
                pass
            else:
                return filtered_submits[0]

    def _redundancy_check(self, filtered_submits: list) -> bool:
        """Counts the number of items in the dictionary supplied. NOTE: the dict input should already be filtered and be a positive submission."""
        if len(filtered_submits) > 1:
            return True
        elif len(filtered_submits) <= 1:
            return False
        else:
            raise ValueError()

    def _fix_redundancies(self, positive_redundants: list) -> str:  # GOOD
        """Receives a dict of the name of the carrier as a key,  and the
        positive submission value as the"""
        redundancies = positive_redundants
        section_name = self._assign_redundant_section(redundancies)
        return section_name

    def _assign_redundant_section(self, redundancies: list[str]):
        string = " + ".join(redundancies)
        section_name = f"Combination: {string}"
        return section_name

    def save_path(self, raw_path, is_quoteform: bool) -> bool:
        try:
            path = self._filter_out_brackets(raw_path)
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
        if len(self.extra_attachments) >= 1:
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
