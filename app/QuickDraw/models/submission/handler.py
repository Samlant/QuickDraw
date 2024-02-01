from pathlib import Path

from email_validator import validate_email, EmailNotValidError

from QuickDraw.helper import validate_path
from QuickDraw.models.submission.quoteform import FormBuilder
from QuickDraw.models.submission.submission import Submission
from QuickDraw.models.submission.customer import Customer
from QuickDraw.models.submission.markets import Market, Markets
from QuickDraw.models.submission.quoteform import Quoteform
from QuickDraw.models.submission.vessel import Vessel


class SubmissionModel:
    def __init__(self):
        pass

    def process_request(
        self,
        view_results: dict[str, str | list[str]],
        carriers: dict[str, bool] = None,
    ) -> Submission:
        # validate quoteform path and ensure it's permissible/readable.
        quoteform_path = validate_path(
            paths=view_results.pop("quoteform"),
        )
        assert quoteform_path.exists(), f"File not found:\n{quoteform_path}"
        # validate all attachment paths and ensure they're permissible/readable.
        attachments = view_results["attachments"].copy()
        view_results["attachments"] = []
        for path in attachments:
            valid_path = validate_path(pathname=path)
            assert path.exists(), f"Path not found.\n{path}"
            view_results["attachments"].append(valid_path)
        # combine CC addresses into a single string if necessary.
        view_results["user_CC"] = self.process_user_CC(
            view_results["user_CC1"], view_results["user_CC2"]
        )
        assert isinstance(
            view_results["user_CC"], list[str]
        ), f"CC addresses are not strings within a list:\n{view_results['user_CC']}"

        submission = self._process_quoteform(
            quoteform_path=quoteform_path, carriers=carriers
        )
        return submission

    def process_user_CC(cc_1: str, cc_2: str) -> str:
        cc_1_list = [x.strip() for x in cc_1.split(";")]
        cc_2_list = [x.strip() for x in cc_2.split(";")]
        cc = list(set(cc_1_list + cc_2_list))
        for email in cc:
            if not validate_email(email):
                raise ValueError(f"Invalid email address:\n{email}")
        return ";".join(cc)

    def _process_quoteform(
        self,
        _quoteform_path: str,
        carriers: dict[str, bool] = None,
    ) -> Submission:
        quoteform_path = self.validate_paths(paths=_quoteform_path)
        _ = FormBuilder()
        quoteform = _.make(quoteform=quoteform_path)
        customer: Customer = Customer(
            fname=quoteform.fname, lname=quoteform.lname, referral=quoteform.referral
        )
        vessel: Vessel = Vessel(year=quoteform.year, make=quoteform.vessel)
        submission: Submission = Submission(
            quoteform=quoteform,
            customer=customer,
            vessel=vessel,
            markets=[],
            status="PROCESSED",
        )
        return submission

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

    def _handle_getting_CC_addresses(self) -> list:
        """Gets userinput of all CC addresses and adds the to a list. It then
        checks if it should ignore the default CC addresses set in config file
        or add them intothe list as well

        Returns:
                List -- returns a list of all desired CC adresses
        """
        list_of_cc = [self.view_main.user_CC1, self.view_main.user_CC2]
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

    #######################################################
    #############  MS GRAPH API MODEL  ####################
    #######################################################

    #######################################################
    ################  FROM THE PRESENTER  #################
    #######################################################

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
