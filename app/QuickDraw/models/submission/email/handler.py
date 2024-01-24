from dataclasses import dataclass
from typing import Optional

from model.email.html import build_HTML_message as build_html


@dataclass
class EmailHandler:
    """This class is responsible for interfacing with Outlook in creating
    email letters to send.  Once called,  data is gathered from the Presenter
    and applied to an email letter,  then once complete,  it is sent out.
    NOTE: If a PDF value changes, update the instance vars.
    """

    subject: Optional[str] = None
    cc: Optional[str] = None
    to: Optional[str] = None
    body: Optional[str] = None
    extra_notes: Optional[str] = None
    username: Optional[str] = None
    img_sig_url: Optional[str] = None
    attachments_list: Optional[list] = None
    greeting_style: str = "font-size:14px;color:#1F3864;"
    body_style: str = "font-size:14px;color:#1F3864;"
    salutation_style: str = (
        "margin:0in;font-size:14px;font-family:Calibri,sans-serif;color:#1F3864;"
    )
    username_style: str = (
        "margin:0in;font-size:14px;font-family:Calibri,sans-serif;color:#1F3864;"
    )

    def view_letter(self) -> bool:
        """Wrapper for displaying the message for unit-testing"""
        raise NotImplementedError

    def make_msg(self, carrier_section, signature_settings) -> str:
        html_msg = build_html(self, carrier_section, signature_settings)
        return html_msg

    def stringify_subject(self, current_submission) -> str:
        subject_line = f"New Quote Submission from Novamar | {current_submission.lname}, {current_submission.fname} | {current_submission.vessel_year} {current_submission.vessel}"
        return subject_line

    def str_to_uppercase(self, unformatted_string: str) -> str:
        return unformatted_string.upper()
