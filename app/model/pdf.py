import string
from pathlib import Path

from fillpdf import fillpdfs



class DocParser:
    def __init__(self) -> None:
        self.keys: dict[str, str] = {
            "fname": "fname",
            "lname": "lname",
            "year": "vessel_year",
            "vessel": "",
            "referral": "referral",
        }

    def process_doc(self, file_path: Path) -> dict:
        """Extracts pdf form field data, filters them and
        returns key:value pairs within a dict.

        Arguments:
            file_path -- expects a str of the file location of the pdf

        Returns:
            dict -- returns only keys identified within self.keys
        """
        needed_values = self._get_values_from_PDF(file_path)
        return self._assign_values_to_dict(
            needed_values,
            file_path,
        )

    def _get_values_from_PDF(
        self,
        file_path: Path,
    ) -> dict:
        """Extracts pdf form field data, filters them and
        returns key:value pairs within a dict.

        Arguments:
            file_path -- expects a Path obj from the .PDF file's path.

        Returns:
            dict -- returns only the keys identified within self.keys
        """
        pdf_dict = fillpdfs.get_form_fields(file_path)
        if "vessel_make_model" in pdf_dict.keys():
            self.keys["vessel"] = "vessel_make_model"
        elif "vessel_make" in pdf_dict.keys():
            self.keys["vessel"] = "vessel_make"
            self.keys["vessel model"] = "vessel_model"
            self.keys["vessel length"] = "vessel_length"
        else:
            raise KeyError("Double check the keys in quoteform")
        pdf_dict = {key: pdf_dict[key] for key in pdf_dict.keys() & self.keys.values()}
        # try:
        #     entity_dict = {"entity": "entity"}
        #     entity = {key: pdf_dict[key] for key in pdf_dict.keys() & entity_dict.values()}
        #     pdf_dict["entity"] = entity["entity"]
        # except:
        #     print("No entity shown on quoteform, passing.")
        return pdf_dict

    def _assign_values_to_dict(
        self,
        needed_values: dict[str, str | int],
        file_path: Path,
    ) -> dict[str, str | int]:
        """Extracts pdf form field data, filters them and returns
        key:value pairs within a dict.

        Arguments:
            file_path -- expects a str of the file location of the pdf

        Returns:
            dict -- returns only keys identified within self.keys
        """
        values_dict = {}
        fname = needed_values.get(self.keys["fname"])
        values_dict["fname"] = string.capwords(fname)
        lname = needed_values.get(self.keys["lname"])
        values_dict["lname"] = lname.upper()
        if "vessel model" in needed_values.keys():
            make = string.capwords(needed_values.get("vessel"))
            model = string.capwords(needed_values.get("vessel model"))
            length = needed_values.get("vessel length")
            vessel = f"{make} {model} {length}"
        else:
            vessel = needed_values.get(self.keys["vessel"])
        values_dict["vessel"] = string.capwords(vessel)
        values_dict["vessel_year"] = needed_values.get(self.keys["year"])
        referral = needed_values.get(self.keys["referral"])
        values_dict["referral"] = referral.upper()

        values_dict["status"] = "ALLOCATE AND SUBMIT TO MRKTS"
        values_dict["original_file_path"] = file_path
        return values_dict
