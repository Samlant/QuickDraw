from dataclasses import InitVar, dataclass
from pathlib import Path
import ctypes

from fillpdf import fillpdfs

from QuickDraw.models.submission.submission import Submission


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

    path: InitVar[Path]
    name: InitVar[str]
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


class FormBuilder:
    def __init__(self) -> None:
        pass

    def make(self, quoteform: Path) -> Quoteform | bool:
        """Wrapper function for processing a PDF form and creating a Quoteform obj from it."""
        print("Processing/Parsing PDF document.")
        count = 0
        successful = False
        while not successful and count < 4:
            count += 1
            try:
                parsed_form = self._process_document(quoteform)
            except Exception as e:
                print(e)
                ctypes.windll.user32.MessageBoxW(
                    0,
                    "Please exit out of the PDF file so that the program can delete the original file.",
                    "Warning: Exit the PDF",
                    1,
                )
            else:
                successful = True
                return parsed_form
        return False

    def _process_document(self, quoteform: Path) -> Quoteform:
        """Extracts pdf form field data, filters them and
        returns key:value pairs within a dict.

        Arguments:
            quoteform -- expects a str of the quoteform location of the pdf

        Returns:
            dict -- returns only keys identified within self.keys
        """
        form_field_names = self._identify_doc(quoteform)
        form_extract = self._get_doc_values(quoteform, form_field_names)
        quoteform = Quoteform(
            path=quoteform,
            name=form_extract["name"],
            fname=form_extract["fname"],
            lname=form_extract["lname"],
            year=form_extract["year"],
            vessel=form_extract["vessel"],
            referral=form_extract["referral"],
        )
        return quoteform

    def _identify_doc(self, quoteform: Path):
        forms = self.__get_all_quoteforms()
        pdf_fields_values = fillpdfs.get_form_fields(quoteform)
        counter = self.__count_same_field_occurrences(forms, pdf_fields_values)
        doc = max(counter)
        for form in forms:
            if form["name"] == doc:
                return form

    def __count_same_field_occurrences(
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
            form_name = quoteform["name"]
            counter[form_name] = count
        return counter

    def _get_doc_values(self, quoteform, form) -> dict[str, str]:
        pdf_fields_values = fillpdfs.get_form_fields(quoteform)
        form_registry = self._extract_values(pdf_fields_values, form)
        return form_registry

    def _extract_values(self, pdf_fields_values, form) -> dict[str, str]:
        form_registry = self.__loop_fields(pdf_fields_values, form)
        form_registry["name"] = form.pop("name")
        return form_registry

    def __loop_fields(self, pdf_fields_values, form) -> dict[str, str]:
        form_registry = {}
        for prog_field_name, pdf_field in form.items():
            if prog_field_name == "name":
                pass
            elif "," in pdf_field:
                fields = pdf_field.split(",")
                field_values = ""
                for field in fields:
                    value = pdf_fields_values[field.strip()]
                    if not isinstance(value, str):
                        value = str(value)
                    field_values = field_values + " " + value
                form_registry[prog_field_name] = field_values.strip()
            else:
                value = pdf_fields_values[pdf_field]
                if not isinstance(value, str):
                    value = str(value)
                form_registry[prog_field_name] = value
        return form_registry

    def __get_all_quoteforms(self) -> list[dict[str, str]]:
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
