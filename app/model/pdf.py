import string
from pathlib import Path

from fillpdf import fillpdfs


class QuoteDoc:
    def __init__(self, quoteform: dict[str, str]):
        self.name: str = None
        self._fname: str = None
        self._lname: str = None
        self.year: str | int = None
        self.vessel: str = None
        self.referral: str = None
        formatted = self._change_lists_to_str(quoteform)

        self._assign_attr(formatted)

    @property
    def fname(self):
        return self._fname

    @fname.setter
    def fname(self, new_fname: str):
        self._fname = string.capwords(new_fname)

    @property
    def lname(self):
        return self._lname

    @fname.setter
    def lname(self, new_lname: str):
        self._lname = new_lname.upper()

    def change_lists_to_str(
        self, quoteform: dict[str, str | list[str]]
    ) -> dict[str, str]:
        formatted = {}
        for key, value in quoteform.items():
            if "," in value:
                new_value = value.split(",")
                formatted[key] = new_value
            else:
                formatted[key] = [value]
        return formatted

    def _assign_attr(self, formatted: dict[str, str]) -> None:
        """Assign attributes to the class from a formatted dict of attr names & values."""
        for attr, vals in formatted.items():
            if isinstance(vals, list) and len(vals) > 1:
                value = " ".join(vals)
            else:
                value = vals
            setattr(self, attr, value)

    def dict(self, file_path) -> dict[str, str]:
        output = {
            "fname": self.fname,
            "lname": self.lname,
            "vessel_year": self.year,
            "vessel": self.vessel,
            "referral": self.referral,
            "status": "ALLOCATE AND SUBMIT TO MRKTS",
            "original_file_path": file_path,
        }
        return output


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
        form_extract = self.get_doc_values(file_path, quoteform)
        quote_doc = QuoteDoc(form_extract)
        return quote_doc.dict(file_path)

    def identify_doc(self, file_path: Path):
        forms = self._get_all_quoteforms()
        pdf_fields_values = fillpdfs.get_form_fields(file_path)
        counter = self._count_same_field_occurrences(forms, pdf_fields_values)
        doc = max(counter)
        return forms[doc]

    def _count_same_field_occurrences(
        self, forms: list[dict[str, str]], pdf_fields_values
    ) -> dict[str, int]:
        counter = {}
        for quoteform in forms:
            count = 0
            for desired_key, field_name in quoteform.items():
                if "," in field_name:
                    fields = field_name.split(",")
                    for field in fields:
                        if field in pdf_fields_values.keys():
                            count += 1
                elif field_name in pdf_fields_values.keys():
                    count += 1
            counter[quoteform["name"]] = count
        return counter

    def get_doc_values(self, file_path, form) -> dict[str, str]:
        pdf_fields_values = fillpdfs.get_form_fields(file_path)
        form_registry = self._extract_values(pdf_fields_values, form)
        return form_registry

    def _extract_values(self, pdf_fields_values, form) -> dict[str, str]:
        form_registry = {}
        form_registry["name"] = form.pop("name")
        other_values = self.__loop_fields(pdf_fields_values, form)
        return form_registry | other_values

    def __loop_fields(self, pdf_fields_values, form) -> dict[str, str]:
        form_registry = {}
        for prog_field_name, pdf_field in form.items():
            value = pdf_fields_values[pdf_field]
            if not isinstance(value, str):
                value = str(value)
            form_registry[prog_field_name] = value
        return form_registry

    def _get_all_quoteforms(self) -> list[dict[str, str]]:
        config = self.config_worker._open_config()
        form_names = self.__get_names_from_config(config)
        forms = self.__get_values_from_config(config, form_names)
        return forms

    def __get_names_from_config(self, config) -> list[str]:
        return [x for x in config.sections() if "Form_" in x]

    def __get_values_from_config(self, config, form_names) -> list[dict[str, str]]:
        forms = []
        for name in form_names:
            new_dict = {"name": name}
            section = config.get_section(name)
            options = section.items()
            for x, y in options:
                new_dict[x] = y.value
            forms.append(new_dict)
        return forms
