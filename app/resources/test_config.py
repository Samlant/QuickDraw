# from configupdater import ConfigUpdater
import string

file_path = Path(__file__).parent.resolve() / "configurations.ini"
from dataclasses import dataclass
from pathlib import Path
import tkinter as tk
from tkinter import ttk, NSEW
from tkinter.ttk import Treeview


def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children("")]
    l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, "", index)

    tv.heading(
        col,
        text=col,
        command=lambda _col=col: treeview_sort_column(tv, _col, not reverse),
    )


reg_columns = []


@dataclass
class RegColumn:
    name: str
    width: int


class quoteform:
    id: str
    name: str
    fname: str
    lname: str
    year: str
    vessel: str
    referral: str

    def values(self) -> tuple[str]:
        return (self.fname, self.lname, self.year, self.vessel, self.referral)


class window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("760x600")
        # self.root.configure(background="red")
        self.root.attributes("-topmost", True)
        self.root.title("Treeview Test")
        self.root.attributes("-alpha", 0.95)
        current_reg_lf = ttk.Labelframe(
            self.root,
            text="Current Registrations",
        )
        current_reg_lf.grid(column=0, row=1, sticky=NSEW, pady=(5, 0), padx=10)
        current_reg_lf.columnconfigure(0, minsize=500)
        current_reg_lf.rowconfigure(0, minsize=155)
        left_registration_frame = ttk.Frame(current_reg_lf)
        left_registration_frame.grid(row=0, column=0)
        ### Treeview Section ###
        self.columns = [
            "fname",
            "lname",
            "year",
            "vessel",
            "referral",
        ]
        self.tree_reg = ttk.Treeview(
            left_registration_frame,
            columns=self.columns,
            # show="headings",
            height=6,
        )
        self.tree_reg.column(
            "#0",
            width=100,
            stretch=False,
        )
        self.tree_reg.column(
            self.columns[0],
            width=85,
            stretch=False,
        )
        self.tree_reg.column(
            self.columns[1],
            width=85,
            stretch=False,
        )
        self.tree_reg.column(
            self.columns[2],
            width=70,
            stretch=False,
        )
        self.tree_reg.column(
            self.columns[3],
            width=130,
            stretch=False,
        )
        self.tree_reg.column(
            self.columns[4],
            width=85,
            stretch=False,
        )
        self.tree_reg.heading(
            "#0",
            text="Unique ID",
            anchor="w",
            command=lambda _col="#0": treeview_sort_column(self.tree_reg, _col, False),
        )

        self.tree_reg.heading(
            self.columns[0],
            text="First Name",
            anchor="w",
        )
        self.tree_reg.heading(
            self.columns[1],
            text="Last Name",
            anchor="w",
        )
        self.tree_reg.heading(
            self.columns[2],
            text="Vessel Year",
            anchor="w",
        ),

        self.tree_reg.heading(
            self.columns[3],
            text="Vessel",
            anchor="w",
        ),

        self.tree_reg.heading(
            self.columns[4],
            text="Referral",
            anchor="w",
        ),

        self.tree_reg.grid(
            columnspan=2,
            column=0,
            row=0,
            pady=5,
            padx=(5, 0),
        )


a = window()

a.tree_reg.insert(
    "",
    "end",
    iid="Form_2",
    text="Form_2",
    values=("Austin", "Gutnik", "2023", "35 Pursuit", "RiverForest"),
)
a.tree_reg.insert(
    "",
    "end",
    iid="Form_1",
    text="Form_1",
    values=("David", "Marshall", "2023", "27 Sailboat", "Walker Marine"),
)

row_data = []
for parent in a.tree_reg.get_children():
    reg = a.tree_reg.item(parent)["values"]
    row_data.append(reg)
    print(f"Parent = {parent}, reg = {reg}")
print(f"row data: {row_data}")


a.root.mainloop()
config = ConfigUpdater(comment_prefixes=("^",))
config.read(file_path)

# x = config.sections()

# for y in x:
#     if "Form_" in y:
#         print(y)

print("trying list comprehension!")
quoteform_names = [y for y in config.sections() if "Form_" in y]
quoteforms: list[dict[str, str]] = []
for quoteform in quoteform_names:
    new_dict = {"name": quoteform}
    section = config.get_section(quoteform)
    options = section.items()
    for x, y in options:
        new_dict[x] = y.value
    quoteforms.append(new_dict)
print(quoteforms)

# zulu = [
#     {
#         "name": "First",
#         "one": "1",
#         "two": "2",
#         "three": "3",
#         "four": "4",
#     },
#     {
#         "name": "Second",
#         "one": "1",
#         "two": "2",
#         "four": "4",
#     },
# ]
# pdf_fields_and_values = {"1": "nice", "2": "bad", "3": "else", "4": "something"}

# counter = {}
# for z in zulu:
#     count = 0
#     for desired_key, field_name in z.items():
#         if field_name in pdf_fields_and_values.keys():
#             count += 1
#     counter[z["name"]] = count
#     print(counter)
#     print(max(counter))


# orig_list = ["Hatteras", "MY", "85"]

# new_string = " ".join(orig_list)
# print(new_string)
# new_string = string.capwords(new_string)
# print(new_string)
