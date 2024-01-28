from typing import Protocol


class Quoteform(Protocol):
    """Stores the characteristics of a specific PDF quoteform.

    Attributes:
        id : standardized name used to ID mapping in config.ini file
        name : user-chosen name for the specific mapping
        all other attrs : required fields from PDF

    """

    id: str
    name: str
    fname: str
    lname: str
    year: str
    vessel: str
    referral: str

    def values(self) -> tuple[str]:
        ...


class Presenter(Protocol):
    def browse_file_path(is_quoteform):
        ...
