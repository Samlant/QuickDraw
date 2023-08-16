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
    def __init__(
        self,
        positive_value: str | int | bool,
        negative_value: str | int | bool,
    ) -> None:
        self.yes = positive_value
        self.no = negative_value
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
        market_list: list[str] = []
        for market, value in raw_checkboxes.items():
            if value == self.yes:
                market_list.append(market)
        return market_list

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

    def format_cc_for_api(self, all_addresses: list | str) -> list:
        """Prepares list of CC addresses to be properly formatted for api call."""
        if isinstance(all_addresses, list):
            split_address = self._split_addresses(input_list=all_addresses)
            formatted_address = self._eliminate_whitespaces_invalid_chars(
                list_of_str=split_address
            )
            return formatted_address
        elif isinstance(all_addresses, str):
            formatted_address = self._del_whitespace_invalid_chars(input=all_addresses)
            return formatted_address
        else:
            raise TypeError(
                "email address is neither a string nor list. Please double-check."
            )

    def _split_addresses(self, input_list: list[str]) -> list[str]:
        list_of_strings: list[str] = []
        for item in input_list:
            x = item.split(";")
            for y in x:
                if y.strip() != "":
                    list_of_strings.append(y)
        return list_of_strings

    def _eliminate_whitespaces_invalid_chars(self, list_of_str: list[str]) -> list[str]:
        list_of_formatted_str: list[str] = []
        for item in list_of_str:
            x = self._del_whitespace_invalid_chars(input=item)
            list_of_formatted_str.append(x)
        return list_of_formatted_str

    def _del_whitespace_invalid_chars(self, input: str) -> str:
        x = input.translate({ord(i): None for i in r'"() ,:;<>[\]'})
        print(x)
        return x

    ########## Dialog-related Functions Below ############
    def process_user_choice(self, all_options: dict[str, any], current_submission):
        list_mrkts = []
        for market, value in all_options.items():
            if value == 1:
                mrkt = market.upper()
                list_mrkts.append(mrkt)
            else:
                pass
        current_submission.status = "SUBMIT TO MRKTS"
        current_submission.markets = list_mrkts
        return current_submission
