from typing import Protocol
from dataclasses import dataclass


class ConfigWorker(Protocol):
    def get_value(self, request: dict) -> dict:
        ...


@dataclass
class ClientInfo(Protocol):
    markets: list
    status: str


class BaseModel:
    def __init__(self, positive_value, negative_value) -> None:
        self.yes: str | int | bool | list = positive_value
        self.no: str | int | bool | list = negative_value
        self.quoteform_path: str = None
        self.extra_attachments: list = []

    def save_path(self, path: str, is_quoteform: bool) -> None:
        if is_quoteform:
            self.quoteform_path = path
        elif is_quoteform is False:
            self.extra_attachments.append(path)
        else:
            raise Exception("Type of param:is_quoteform is wrong or empty.")

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
        return list(filter(self._is_positive, checkboxes_dict))

    def _is_positive(self, market) -> bool:
        return market == self.yes

    def handle_redundancies(self, filtered_submits: list) -> str:
        """Checks if multiple redundant markets are present,  then combines them & returns the appropriate config section name"""
        if self._redundancy_check(filtered_submits):
            section_name = self._fix_redundancies(filtered_submits)
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

    def filter_out_brackets(self, path: str) -> str:
        """Cleans up the path str by removing any brackets---if present."""
        if "{" in path:
            path = path.translate({ord(c): None for c in "{}"})
        return path

    def get_all_attachments(self) -> list:
        attachments = []
        attachments.append(self.quoteform_path)
        if len(self.extra_attachments) >= 1:
            for attachment in self.extra_attachments:
                attachments.append(attachment)
        else:
            return attachments
        return attachments

    def list_of_cc_to_str(self, input_list: list) -> str:
        """Transforms lists into strings. In-use for CC_address assignment."""
        input_list = "; ".join(str(element) for element in input_list)
        return input_list

    ########## Dialog-related Functions Below ############
    def process_user_choice(self, all_options: dict[str, any], current_submission):
        for market, value in all_options.items():
            if value == self.yes:
                mrkt = market.upper()
                current_submission.markets.append(mrkt)
        current_submission.status = "SUBMIT TO MRKTS"
        return current_submission
