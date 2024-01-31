from pathlib import Path

from QuickDraw.helper import GREEN_LIGHT
from QuickDraw.models.submission.quoteform import FormBuilder
from QuickDraw.models.submission.submission import Submission
from QuickDraw.models.submission.customer import Customer
from QuickDraw.models.submission.markets import Market, Markets
from QuickDraw.models.submission.quoteform import Quoteform
from QuickDraw.models.submission.vessel import Vessel


class SubmissionModel:
    def __init__(self):
        pass

    def process_quoteform(self, quoteform_path: Path) -> Submission:
        _ = FormBuilder()
        quoteform = _.make(quoteform=quoteform_path)
        customer: Customer = Customer(fname=quoteform.fname,lname=quoteform.lname, referral=quoteform.referral)
        vessel: Vessel = Vessel(year=quoteform.year, make=quoteform.vessel)
        submission: Submission = Submission(
            quoteform=quoteform,
            customer=customer,
            vessel=vessel,
            status="PROCESSED",
        )
        return submission

    def filter_only_positive_submissions(self, raw_checkboxes: dict) -> list:
        market_list: list[str] = []
        for market, value in raw_checkboxes.items():
            if value == GREEN_LIGHT:
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

    #######################################################
    #############  MS GRAPH API MODEL  ####################
    #######################################################

    def format_cc_for_api(self, all_addresses: list | str) -> list[str]:
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

    def format_to_for_api(self, addresses: str) -> list[str]:
        list_of_strings: list[str] = []
        if ";" in addresses:
            x = addresses.split(";")
            for y in x:
                if y.strip("; ") != "":
                    list_of_strings.append(y)
            formatted_addresses = self._eliminate_whitespaces_invalid_chars(
                list_of_strings
            )
        else:
            formatted_addresses = self._del_whitespace_invalid_chars(addresses)
        return formatted_addresses

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
        return x

    #######################################################
    #############  MS GRAPH API MODEL  ####################
    #######################################################

    #######################################################
    ################  FROM THE PRESENTER  #################
    #######################################################

    def gather_active_markets(self) -> list:
        """This gets the markets that the user chose. Also checks
        for and handles any duplicate email address.

        Returns: list of market names to submit to.

        Arguments (outdated):
                autosend = {bool}
                NOTE: If True, no window will be shown and all emails
                will be sequentially sent. If False, a window will be shown for
                each email prior to sending.
        """
        print("Gathering single markets and redundant markets")
        submission_list = self._handle_single_markets()
        redundant_result = self._handle_redundancies()
        if redundant_result is not None:
            submission_list.append(redundant_result)
        else:
            pass
        return submission_list

    def _handle_single_markets(self) -> list:
        """Gets possible redundant carriers' checkbox values, filters to only keep
        positive submissions, then combines them into one submission

        Returns -- Dict: returns dict of a single, combined carrier submission
        """
        raw_dict = self.get_single_carriers()
        processed_list = self.model_tab_home.filter_only_positive_submissions(raw_dict)
        return processed_list

    def _handle_redundancies(self) -> str:
        """Gets possible redundant carriers' checkbox values, filters to only keep
        positive submissions, then combines them into one submission

        Returns -- Dict: returns dict of a single, combined carrier submission
        """
        raw_dict: dict[str, any] = self._get_possible_redundancies()
        filtered_list = self.model_tab_home.filter_only_positive_submissions(raw_dict)
        processed_str = self.model_tab_home.handle_redundancies(filtered_list)
        return processed_str

    def get_single_carriers(self) -> dict:
        """This gets the values of the carriers' checkboxes that
        all submit to different, unique email addresses.

        Returns:
                Dict -- returns a dict of carrier checkbox values
        """
        carrier_submissions_dict = dict()
        try:
            carrier_submissions_dict = {
                "American Modern": self.view_main.am,
                "Kemah Marine": self.view_main.km,
                "Concept Special Risks": self.view_main.cp,
                "Yachtinsure": self.view_main.yi,
                "Century": self.view_main.ce,
                "Intact": self.view_main.In,
                "Travelers": self.view_main.tv,
            }
        except ValueError as ve:
            raise ValueError(f"Couldn't get carrier checkboxes saved into a dict. {ve}")
        else:
            return carrier_submissions_dict

    def _get_possible_redundancies(self) -> dict[str, str | int | bool | list]:
        """This gets the values of the carriers' checkboxes that submit
        to the same email address. Separating this allows us to more
        easily update the list of likely redundancies.

        Returns:
                Dict -- returns a dict of carrier checkbox values
        """
        possible_redundancies_dict: dict(str, str | int | bool | list)
        try:
            possible_redundancies_dict = {
                "Seawave": self.view_main.sw,
                "Prime Time": self.view_main.pt,
                "New hampshire": self.view_main.nh,
            }
        except ValueError as ve:
            raise ValueError(f"Couldn't get carrier checkboxes saved into a dict. {ve}")
        else:
            return possible_redundancies_dict

    def loop_through_envelopes(self):
        """This loops through each submission;  it:
        (1) forms an envelope when a positive_submission is found,
        (2) gets and transforms needed data into each of its final
        formatted type and form,
        (3) applies the properly formatted data into each the envelope, and,
        (4) sends the envelope to the recipient, inclusive of all data.
        """
        print("looping through envelopes for all carriers selected")
        self.model_email_handler.subject = self.model_email_handler.stringify_subject(
            self.current_submission,
        )

        unformatted_cc = self._handle_getting_CC_addresses()
        self.model_email_handler.cc = self.model_tab_home.format_cc_for_api(
            unformatted_cc,
        )
        self.model_email_handler.extra_notes = self.view_main.extra_notes
        self.model_email_handler.username = self.config_worker.get_value(
            {
                "section_name": "General settings",
                "key": "username",
            }
        )

        attachments = self.model_tab_home.get_all_attachments()
        self.model_email_handler.attachments_list = (
            self.model_api.create_attachments_json(attachment_paths=attachments)
        )

        self.model_email_handler.img_sig_url = self.config_worker.get_value(
            {
                "section_name": "General settings",
                "key": "signature_image",
            }
        )
        for carrier in self.current_submission.markets:
            carrier_section = self.config_worker.get_section(carrier)
            unformatted_to = carrier_section.get("address").value
            self.model_email_handler.to = self.model_tab_home.format_to_for_api(
                unformatted_to
            )
            signature_settings = self.get_signature_settings()
            self.model_email_handler.body = self.model_email_handler.make_msg(
                carrier_section,
                signature_settings,
            )

            self.json = self.model_api.create_email_json(email=self.model_email_handler)
            print("sending email message")
            count = 0
            successful = False
            while not successful and count > 5:
                count += 1
                try:
                    thread_ol = threading.Thread(
                        daemon=True, target=self.send_email_api, name="Outlook API Call"
                    )
                    thread_ol.start()
                except Exception as e:
                    print(f"Outlook API call failed. {e}")
            count = 0
            successful = False
            while not successful and count > 5:
                count += 1
                try:
                    thread_xl = threading.Thread(
                        daemon=True,
                        target=self._send_excel_api_call,
                        name="Excel API Call",
                    )
                    thread_xl.start()
                except Exception as e:
                    print(f"Excel API call failed. {e}")
        self.quoteform_detected = False

    def send_email_api(self):
        print("Sending email via MSGraph")
        self.model_api_client.send_message(message=self.json)
        print("Email sent.")

    def _handle_getting_CC_addresses(self) -> list:
        """Gets userinput of all CC addresses and adds the to a list. It then
        checks if it should ignore the default CC addresses set in config file
        or add them intothe list as well

        Returns:
                List -- returns a list of all desired CC adresses
        """
        list_of_cc = [self.view_main.userinput_CC1, self.view_main.userinput_CC2]
        if self.view_main.use_CC_defaults:
            if self.config_worker.check_if_using_default_carboncopies():
                cc_from_config = [
                    self.config_worker.get_value(
                        {
                            "section_name": "General settings",
                            "key": "default_cc1",
                        }
                    ),
                    self.config_worker.get_value(
                        {
                            "section_name": "General settings",
                            "key": "default_cc2",
                        }
                    ),
                ]
                list_of_cc = list_of_cc + cc_from_config
        return list_of_cc
