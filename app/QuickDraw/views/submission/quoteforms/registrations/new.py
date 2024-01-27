from tkinter import ttk
from typing import Protocol


from QuickDraw.views.submission import base


class Presenter(Protocol):
    def add_qf_registration(self) -> None:
        ...


class NewRegistrations(ttk.LabelFrame):
    def __init__(
        self,
        view: base.MainWindow,
        presenter: Presenter,
        parent,
        text: str,
    ):
        super().__init__(master=parent, text=text)

        ttk.Label(
            self,
            text="You may register your own quoteform to be used by the program. You may also remove them if it's unused or changes.",
        ).grid(column=0, row=0, pady=3, columnspan=5)
        ttk.Label(
            self,
            text="If your quoteform splits any of the below required fields into two or more fields, then separate each field with a comma",
        ).grid(column=0, row=1, columnspan=5)
        ttk.Label(
            self,
            text="For example: if your form uses 'Make', 'Model' & 'Length' fields, list all under the Vessel field, separated by a comma.",
        ).grid(column=0, row=2, columnspan=5, pady=(0, 5))

        ttk.Label(
            self,
            text="Form Name:",
        ).grid(column=0, row=3, padx=(3, 0))
        view.form_name_entry = ttk.Entry(
            master=self,
            name="form_name",
            textvariable=view._form_name,
            width=35,
        )
        view.form_name_entry.grid(
            column=1,
            row=3,
            sticky="ew",
            ipady=5,
            pady=1,
        )

        ttk.Label(
            self,
            text="First Name:",
        ).grid(column=0, row=4, padx=(3, 0))
        view.fname_entry = ttk.Entry(
            master=self,
            name="fname",
            textvariable=view._fname,
            width=35,
        )
        view.fname_entry.grid(
            column=1,
            row=4,
            sticky="ew",
            ipady=5,
            pady=1,
        )

        ttk.Label(
            self,
            text="Last Name:",
        ).grid(column=0, row=5, padx=(3, 0))
        view.lname_entry = ttk.Entry(
            master=self,
            name="lname",
            textvariable=view._lname,
            width=35,
        )
        view.lname_entry.grid(
            column=1,
            row=5,
            sticky="ew",
            ipady=5,
            pady=5,
        )

        ttk.Label(
            self,
            text="Vessel Year:",
        ).grid(column=2, row=3, padx=(3, 0))
        view.year_entry = ttk.Entry(
            master=self,
            name="year",
            textvariable=view._year,
            width=35,
        )
        view.year_entry.grid(
            column=3,
            row=3,
            sticky="ew",
            ipady=5,
            pady=5,
        )

        ttk.Label(
            self,
            text="Vessel:",
        ).grid(column=2, row=4, padx=(3, 0))
        view.vessel_entry = ttk.Entry(
            master=self,
            name="vessel",
            textvariable=view._vessel,
            width=35,
        )
        view.vessel_entry.grid(
            column=3,
            row=4,
            sticky="ew",
            ipady=5,
            pady=5,
        )

        ttk.Label(
            self,
            text="Referral:",
        ).grid(column=2, row=5, padx=(3, 0))
        view.referral_entry = ttk.Entry(
            master=self,
            name="referral",
            textvariable=view._referral,
            width=35,
        )
        view.referral_entry.grid(
            column=3,
            row=5,
            sticky="ew",
            ipady=5,
            pady=5,
        )

        ttk.Button(
            master=self,
            text="Register",
            command=presenter.add_qf_registration,
        ).grid(
            rowspan=5,
            column=4,
            row=3,
            sticky="ew",
            padx=5,
            pady=10,
            ipady=40,
        )
