import string
from pathlib import Path
from dataclasses import dataclass, InitVar


@dataclass(kw_only=True)
class Quoteform:
    """Stores the characteristics of a specific PDF quoteform.

    Attributes:
        name : user-chosen name for the specific mapping of doc;
        path: system path to the PDF file;
        fname : first name of customer;
        lname : last name of customer;
        year : year of vessel;
        vessel : brand of vessel;
        referral : referral source of customer;

    Usage:
        Quoteform(
            name="my_default",
            path=Path.cwd(),
            fname="sam",
            lname="smith",
            year="2023",
            vessel="Regal 36 XO",
            referral="Quality Boats",
        )
    """

    name: InitVar[str]
    path: InitVar[Path]
    fname: str
    lname: str
    year: str
    vessel: str
    referral: str

    def __post_init__(self, name, path):
        self.name = name
        self.path = path

    def values(self) -> tuple[str]:
        return (
            self.name,
            self.fname,
            self.lname,
            self.year,
            self.vessel,
            self.referral,
        )

    def data(self) -> dict[str, str]:
        return {
            "fname": self.fname,
            "lname": self.lname,
            "year": self.year,
            "vessel": self.vessel,
            "referral": self.referral,
        }
