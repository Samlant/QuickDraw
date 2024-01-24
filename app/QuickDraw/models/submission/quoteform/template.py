import string
from pathlib import Path


class QuoteDoc:
    def __init__(self, quoteform: dict[str, str], file_path: Path):
        self.name: str = quoteform["name"]
        self._fname: str = quoteform["fname"]
        self._lname: str = quoteform["lname"]
        self.year: str | int = quoteform["year"]
        self.vessel: str = quoteform["vessel"]
        self.referral: str = quoteform["referral"]
        self.file_path: Path = file_path

    @property
    def fname(self):
        return string.capwords(self._fname)

    @fname.setter
    def fname(self, new_fname: str):
        self._fname = string.capwords(new_fname)

    @property
    def lname(self):
        return self._lname.upper()

    @lname.setter
    def lname(self, new_lname: str):
        self._lname = new_lname.upper()

    def dict(self) -> dict[str, str]:
        output = {
            "fname": self.fname,
            "lname": self.lname,
            "vessel_year": self.year,
            "vessel": self.vessel,
            "referral": self.referral,
            "status": "ALLOCATE AND SUBMIT TO MRKTS",
            "original_file_path": self.file_path,
        }
        return output
