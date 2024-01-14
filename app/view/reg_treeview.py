from tkinter import ttk
from dataclasses import dataclass
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

    def data(self):
        ...


@dataclass
class RegColumn:
    name: str
    text: str
    width: int


class RegColumns:
    def __init__(self):
        self.objects = []
        self.names = []

    def add_column(self, name: str, text: str, width: int):
        x = RegColumn(name, text, width)
        self.objects.append(x)
        self.names.append(name)


class RegTreeView(ttk.Treeview):
    def __init__(self, parent):
        columns = RegColumns()

        columns.add_column("form", "Form Name", 135)
        columns.add_column("fname", "First Name", 85)
        columns.add_column("lname", "Last Name", 85)
        columns.add_column("year", "Year", 70)
        columns.add_column("vessel", "Vessel", 130)
        columns.add_column("referral", "Referral", 85)

        super().__init__(
            parent,
            columns=columns.names,
            show="headings",
            height=6,
        )
        for column in columns.objects:
            self.column(
                column.name,
                width=column.width,
                stretch=False,
            )

            self.heading(
                column.name,
                text=column.text,
                anchor="w",
            )

    def get_tv(self):
        return self

    def add_registration(self, quoteform: Quoteform):
        self.insert(
            "",
            "end",
            text=quoteform.name,
            values=quoteform.values(),
        )

    def remove_registration(self):
        current_item = self.selection()
        self.delete(current_item)

    def get_all_rows(self) -> list[list[str]]:
        row_data = []
        for parent in self.get_children():
            registration = self.item(parent)["values"]
            row_data.append(registration)
        return row_data

    def get_quoteforms(self) -> list[Quoteform]:
        rows = self.get_all_rows()
        for row in rows:
            pass

    def get_all_names(self) -> list[str]:
        form_names = []
        items = self.get_children()
        if items:
            print("yes")
            for item in items:
                registration = self.item(item)["values"][0]
                form_names.append(registration)
        return form_names
