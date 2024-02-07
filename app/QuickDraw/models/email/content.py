from typing import Protocol
from pathlib import Path

from email_validator import validate_email, EmailNotValidError

from QuickDraw.helper import open_config
from QuickDraw.models.submission.underwriting import Submission, Market
from app.QuickDraw.models.email.format import EmailFormat
from app.QuickDraw.models.email.options import EmailOptions

class Email(Protocol):
    to: list[str]
    cc: list[str]
    subject: str
    body: str
    attachments: list[Path]
    
class EmailContent:
    def __init__(self):
        self.submission: Submission = None
        self.format: EmailFormat = None
        self.options: EmailOptions = None
        self.username: str = None
        self.extra_notes: str = None
        self.user_carbon_copies: str = None
    
    def get_email_config(self) -> dict[str, str]:
        config = open_config()
        settings = config.get_section("email").to_dict()
        return settings
        
    def _make_sig(self, settings: dict[str, str]) -> str:
        signature = f"""
        <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>
        NOVAMAR INSURANCE GROUP
        <br>
        <img src='{settings["logo_img"]}'>
        <br>
        Main:(800)-823-2798
        <br>
        Office :{settings["office_phone"]}
        <br>
        Fax  :{settings["office_fax"]}
        <br>
        {settings["office_street"]}
        <br>
        {settings["office_city_st_zip"]}
        <br>
        <a href='http://www.novamarinsurance.com/' target='_blank'>www.novamarinsurance.com</a>
        <br>
        <a href='http://www.novamarinsurance.com.mx/' target='_blank'>www.novamarinsurance.com.mx</a>
        </p>
        <br>
        
        <p style='margin:0in;'>
        <a href='https://www.facebook.com/NovamarInsurance' target='_blank'><img width=24 height=24 src='https://cdn1.iconfinder.com/data/icons/social-media-2285/512/Colored_Facebook3_svg-512.png'></a>
        <a href='https://www.instagram.com/novamar_insurance/' target='_blank'><img width=24 height=24 src='https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Instagram_colored_svg_1-512.png'></a>
        <a href='https://twitter.com/NovamarIns' target='_blank'><img width=24 height=24 src='https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Twitter3_colored_svg-512.png'></a>
        <a href='https://www.linkedin.com/company/novamar-insurance-group-inc' target='_blank'><img width=24 height=24 src='https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Linkedin_unofficial_colored_svg-512.png'></a>
        </p>
        <br>
        <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>
        Established in 1987 with offices in: Seattle | Newport Beach | San Diego | Sarasota | Jacksonville | Puerto Vallarta | Cancun | San Miguel de Allende
        <br>
        Please be advised that coverage is not bound, renewed, amended or in force unless confirmed in writing by a Novamar Insurance Group agent or by the represented company.
        </p>
        """
        if self.options._use_CC_defaults:
            signature = f"<img src='{settings['sig_img_url']}'>" + signature
        return signature
        
    def _make_body(self, market: Market, signature: str,):
        body = f"""
        <html>
            <head>
                <title>New Quote Submission</title>
                <meta http-equiv='Content-Type' content='text/html; charset=windows-1252'>
                <meta name='ProgId' content='Word.Document'>
                <meta name='Generator' content='Microsoft Word 15'>
                <meta name='Originator' content='Microsoft Word 15'>
            </head>
            <body>
                <p style={self.format.greeting}>{market.greeting}</p>
                <p style={self.format.body}>{market.body}</p> 
                <p style={self.format.body}>{self.extra_notes}</p>
                <p style={self.format.body}>{market.outro}</p>
            </body>
            <footer>
            <p style={self.format.salutation}>{market.salutation}</p>
            <p style={self.format.username}>{self.username}</p>
            {signature}
            </footer>
        </html>
        """
        return body

    def _get_recipients(self, market: Market) -> list[str]:
        _a = self.__split_addresses(addresses=market.address)
        _b = self.__format_addresses(_addresses=_a)
        recipients = self.__validate_addresses(addresses=_b)
        return recipients

    def _get_carbon_copies(self, settings: dict[str, str]) -> list[str]:
        # combine all cc (defaults and user-inputted) into one string
        if self.options.use_default_cc_addresses:
            _1 = settings["user_CC1"]
            _2 = settings["user_CC2"]
            _addresses = self.user_carbon_copies + _1 + _2
        else:
            _addresses = self.user_carbon_copies
        _a = self.__split_addresses(_addresses=_addresses)
        _b = self.__format_addresses(_addresses=_a)
        carbon_copy_recipients = self.__validate_addresses(addresses=_b)
        return carbon_copy_recipients

    def __split_addresses(self, _addresses: str) -> list[str]:
        joined = []
        _a: list[str] = [x.strip() for x in _addresses.split(";")]
        for _b in _a:
            if _b.strip() != "":
                joined.append(_b)
        return joined

    def __format_addresses(self, _addresses: list[str]) -> list[str]:
        addresses = []
        for _ in _addresses:
            address = _.translate({ord(i): None for i in r'"() ,:;<>[\]'})
            addresses.append(address)
        return addresses
    
    def __validate_addresses(self, addresses: list[str]) -> list[str]:
        _validated_addresses = []
        for address in addresses:
            try:
                email_info = validate_email(address, check_deliverability=False)
                email = email_info.normalized
            except EmailNotValidError as e:
                print(str(e))
            else:
                _validated_addresses.append(email)
        unique_valid_addresses = list(set(_validated_addresses))
        return unique_valid_addresses
        
    def make_subject_line(self, submission: Submission)-> str:
        _ = f"""New Quote Submission from Novamar |
        {self.submission.customer.lfname} |
        {self.submission.vessel.year}
        {self.submission.vessel.make}"""
        subject = _.replace("\n", " ")
        return subject
