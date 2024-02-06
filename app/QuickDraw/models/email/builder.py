from typing import NamedTuple
from pathlib import Path

from QuickDraw.helper import open_config
from QuickDraw.models.submission.underwriting import Submission, Market
from QuickDraw.models.email.content import EmailContent
from QuickDraw.models.email.options import EmailOptions
from QuickDraw.models.email.format import EmailFormat

class Email(NamedTuple):
    to: list[str]
    cc: list[str]
    subject: str
    body: str
    attachments: list[Path]

class EmailBuilder(EmailContent):
    def __init__(self):
        super().__init__()
        self.emails = list[Email]
    
    def make_all_emails(self,
            submission: Submission,
            extra_notes: str,
            user_carbon_copies: str,
        ) -> list[Email]:
        self.submission = submission
        self.extra_notes = extra_notes
        self.user_carbon_copies = user_carbon_copies
        self.format = EmailFormat()
        settings = self.get_email_config()
        self.username = settings.pop("username")
        self.options = EmailOptions(
            settings=settings,
        )
        for market in submission.markets:
            email = self._make_email(
                market=market,
                settings=settings,
            )
            self.emails.append(email)
        return self.emails
    
    def _make_email(
            self,
            market: Market,
            settings: dict[str, str]
        ) -> Email:
        # make signature
        signature = self._make_sig(settings=settings)
        body = self._make_body(market=market, signature=signature)
        # get recipients
        recipients = self._get_recipients(market=market)
        cc_recipients = self._get_carbon_copies(settings=settings)
        email = Email()
        return email

    
        
    
