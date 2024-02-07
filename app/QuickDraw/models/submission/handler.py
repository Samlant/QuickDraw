from pathlib import Path
from typing import Literal

from QuickDraw.helper import open_config, validate_paths
from QuickDraw.models.submission.quoteform import FormBuilder
from QuickDraw.models.submission.underwriting import Submission, Market, Carrier
from QuickDraw.models.submission.customer import Customer
from QuickDraw.models.submission.vessel import Vessel


class SubmissionModel:
    def __init__(self):
        pass

    def process_quoteform(
        self,
        _quoteform_path: str,
        carriers: list[Carrier] = [],
        markets: list[Market] = [],
        status: Literal[
            "ALLOCATE MRKTS AND SUBMIT",
            "SUBMIT TO MRKTS",
        ] = "ALLOCATE MRKTS AND SUBMIT",
    ) -> Submission:
        quoteform_path = self.validate_attachments(
            attachments=_quoteform_path
            )
        _ = FormBuilder()
        quoteform = _.make(quoteform=quoteform_path)
        customer: Customer = Customer(
            fname=quoteform.fname,
            lname=quoteform.lname,
            referral=quoteform.referral,
        )
        vessel: Vessel = Vessel(
            year=quoteform.year,
            make=quoteform.vessel,
        )
        submission: Submission = Submission(
            quoteform=quoteform,
            customer=customer,
            vessel=vessel,
            carriers=carriers,
            markets=markets,
            status=status,
        )
        return submission

    def validate_attachments(self, attachments: str) -> Path | list[Path]:
        "TODO: make the error handling USEFUL!"
        if "\n" in attachments:
            _ = attachments.split("\n")
        elif isinstance(attachments, str):
            _ = attachments
        try:
            paths = validate_paths(pathnames=_)
        except OSError as ose:
            print(str(ose))
        else:
            return paths

    def make_markets(self, market_tuples: list[tuple[str, list[str]]]) -> list[Market]:
        config = open_config()
        mrkts = []
        for carrier_tuple in market_tuples:
            section = config.get_section(carrier_tuple[0]).to_dict()
            mrkt = Market(
                name=carrier_tuple[0],
                ids=carrier_tuple[1],
                status="",
                address=section["address"],
                greeting=section["greeting"],
                body=section["body"],
                outro=section["outro"],
                salutation=section["salutation"],
            )
            mrkts.append(mrkt)
        return mrkts


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
            self.submission,
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
        for carrier in self.submission.markets:
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

    def send_email_api(self):
        print("Sending email via MSGraph")
        self.model_api_client.send_message(message=self.json)
        print("Email sent.")
