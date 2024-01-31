from dataclasses import dataclass
from string import capwords


@dataclass
class Customer:
    fname: str
    lname: str
    referral: str

    @property
    def name(self):
        return capwords(self.fname) + " " + capwords(self.lname)

    @property
    def lfname(self):
        "Provides name in LAST First format"
        return self.lname.upper() + " " + capwords(self.fname)
