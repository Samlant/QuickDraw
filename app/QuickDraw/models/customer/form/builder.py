from pathlib import Path
from QuickDraw.models.customer import QuoteDoc
from fillpdf import fillpdfs


class FormBuilder:
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
        quote_doc = QuoteDoc(form_extract, file_path)
        return quote_doc.dict()

    def identify_doc(self, file_path: Path):
        forms = self._get_all_quoteforms()
        pdf_fields_values = fillpdfs.get_form_fields(file_path)
        counter = self._count_same_field_occurrences(forms, pdf_fields_values)
        doc = max(counter)
        for form in forms:
            if form["name"] == doc:
                return form

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
