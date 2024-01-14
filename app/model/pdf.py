import string
from pathlib import Path

from fillpdf import fillpdfs


class QuoteDoc:
    def __init__(self, quoteform: dict[str, str]):
        self.doc_name: str = quoteform["name"]
        self.fname: str = None
        self.lname: str = None
        self.year: str | int = None
        self.vessel: str = None
        self.referral: str = None
        self.quoteform = {}
        for key, value in quoteform.items():
            if "," in value:
                new_value = value.split(",")
                self.quoteform[key] = new_value
            else:
                self.quoteform[key] = [value]
        self.assign_attr()

    def assign_attr(self) -> None:
        """Assign attributes to the class from a dictionary of attribute names and values."""
        for attr, vals in self.quoteform.items():
            if len(vals) > 1:
                value = " ".join(vals)
            else:
                value = vals
            setattr(self, attr, value)

    def get_output(self, file_path) -> dict[str, str]:
        self.fname = string.capwords(self.fname)
        self.lname = self.lname.upper()
        output_dict = {
            "fname": self.fname,
            "lname": self.lname,
            "vessel_year": self.year,
            "vessel": self.vessel,
            "referral": self.referral,
            "status": "ALLOCATE AND SUBMIT TO MRKTS",
            "original_file_path": file_path,
        }
        return output_dict


class DocParser:
    def __init__(self, config_worker) -> None:
        self.config_worker = config_worker

    def process_doc(self, file_path: Path) -> dict[str, str]:
        """Extracts pdf form field data, filters them and
        returns key:value pairs within a dict.

        Arguments:
            file_path -- expects a str of the file location of the pdf

        Returns:
            dict -- returns only keys identified within self.keys
        """
        quoteform = self.identify_doc(file_path)
        quoteform_extract = self.get_doc_values(file_path, quoteform)
        quote_doc = QuoteDoc(quoteform_extract)
        return quote_doc.get_output(file_path)

    def identify_doc(self, file_path: Path):
        quoteforms = self._get_all_quoteforms()
        pdf_fields_and_values = fillpdfs.get_form_fields(file_path)
        counter = {}
        for quoteform in quoteforms:
            count = 0
            for desired_key, field_name in quoteform.items():
                if "," in field_name:
                    fields = field_name.split(",")
                    for field in fields:
                        if field in pdf_fields_and_values.keys():
                            count += 1
                elif field_name in pdf_fields_and_values.keys():
                    count += 1
            counter[quoteform["name"]] = count
        doc = max(counter)
        return quoteforms[doc]

    def get_doc_values(
        self, file_path, quoteform: dict[str, str | int]
    ) -> dict[str, str]:
        pdf_fields_and_values = fillpdfs.get_form_fields(file_path)
        new_dict = {}
        new_dict["name"] = quoteform.pop("name")
        for prog_field_name, pdf_field in quoteform.items():
            value = pdf_fields_and_values[pdf_field]
            if not isinstance(value, str):
                value = str(value)
            new_dict[prog_field_name] = value
        return new_dict

    def _get_all_quoteforms(self) -> list[dict[str, str]]:
        config = self.config_worker._open_config()
        quoteform_names = [x for x in config.sections() if "Form_" in x]
        quoteforms: list[dict[str, str]] = []
        for quoteform in quoteform_names:
            new_dict = {"name": quoteform}
            section = config.get_section(quoteform)
            options = section.items()
            for x, y in options:
                new_dict[x] = y.value
            quoteforms.append(new_dict)
        return quoteforms
