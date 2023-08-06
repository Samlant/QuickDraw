import string
from pathlib import Path

from fillpdf import fillpdfs


class DocParser:
    def __init__(self) -> None:
        self.keys: dict[str, str | int] = {
            "fname": "fname",
            "lname": "lname",
            "year": "vessel_year",
            "vessel": "vessel_make_model",
            "referral": "referral",
        }

    def process_doc(self, file_path: Path) -> dict:
        """Extracts pdf form field data, filters them and returns key:value pairs within a dict.

        Arguments:
            file_path -- expects a str of the file location of the pdf

        Returns:
            dict -- returns only keys identified within self.keys
        """
        desired_values_dict = self._get_values_from_PDF(file_path=file_path)
        return self._assign_values_to_dict(
            pdf_dict=desired_values_dict,
            file_path=file_path,
        )

    def _get_values_from_PDF(self, file_path: Path) -> dict:
        """Extracts pdf form field data, filters them and returns key:value pairs within a dict.

        Arguments:
            file_path -- expects a Path obj from the .PDF file's path.

        Returns:
            dict -- returns only the keys identified within self.keys
        """
        pdf_dict = fillpdfs.get_form_fields(file_path)
        pdf_dict = {key: pdf_dict[key] for key in pdf_dict.keys() & self.keys.values()}
        return pdf_dict

    def _assign_values_to_dict(self, pdf_dict: dict, file_path: Path) -> dict:
        """Extracts pdf form field data, filters them and returns key:value pairs within a dict.

        Arguments:
            file_path -- expects a str of the file location of the pdf

        Returns:
            dict -- returns only keys identified within self.keys
        """
        values_dict = {}
        fname = pdf_dict.get(self.keys["fname"])
        values_dict["fname"] = string.capwords(fname)
        lname = pdf_dict.get(self.keys["lname"])
        values_dict["lname"] = lname.upper()
        vessel = pdf_dict.get(self.keys["vessel"])
        values_dict["vessel"] = string.capwords(vessel)
        values_dict["vessel_year"] = pdf_dict.get(self.keys["year"])
        referral = pdf_dict.get(self.keys["referral"])
        values_dict["referral"] = referral.upper()
        values_dict["status"] = "ALLOCATE AND SUBMIT TO MRKTS"
        values_dict["original_file_path"] = file_path
        return values_dict
