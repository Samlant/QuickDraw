from typing import Protocol
from pathlib import Path
import tkinter as tk
from tkinter import StringVar
from tkinter.ttk import Frame, Label, Entry, OptionMenu, Button


class Presenter(Protocol):
    def choice(self, choice: str):
        ...


class Quoteform(Protocol):
    path: Path
    name: str
    fname: str
    lname: str
    year: str
    vessel: str
    referral: str


class Submission(Protocol):
    quoteform: Quoteform
    new_path: Path | None
    status: str
    attachments: list | None
    markets: list[str] | None
    submit_tool: bool


class NewFileAlert:
    def __init__(
        self,
        icon_src,
    ) -> None:
        self.submission_info: Submission = None
        self.root: tk.Tk = None
        self.presenter: Presenter = None
        self.icon_path = icon_src

    @property
    def selected_month(self) -> str:
        return self._selected_template.get().lower()

    @property
    def vessel(self) -> str:
        return self._vessel.get()

    @vessel.setter
    def vessel(self, new_vessel: str) -> None:
        self._vessel.set(new_vessel)

    @property
    def year(self) -> str:
        return self._year.get()

    @year.setter
    def year(self, new_year: str) -> None:
        self._year.set(new_year)

    @property
    def referral(self) -> str:
        return self._referral.get()

    @referral.setter
    def referral(self, new_referral: str) -> None:
        self._referral.set(new_referral)

    def initialize(
        self,
        presenter: Presenter,
        submission_info: Submission,
        months: list[str],
    ) -> str:
        self.presenter = presenter
        self._setup_window(months[0])
        self._create_widgets(submission_info, months)
        self.root.mainloop()

    def _setup_window(self, current_month: str):
        self.root = tk.Tk()
        self.root.geometry("300x400")
        self.root.title("Next Steps")
        self.root.attributes("-topmost", True)
        self.root.update()
        self.root.attributes("-topmost", False)
        self.root.iconbitmap(self.icon_path)
        self.root.text_frame = Frame(self.root, bg="#CFEBDF")
        self.root.text_frame.pack(fill="both", expand=True)
        self.root.btn_frame = Frame(self.root, bg="#CFEBDF")
        self.root.btn_frame.pack(fill="both", expand=True, ipady=2)
        self._selected_template = StringVar(value=current_month.capitalize())
        self._vessel = StringVar(name="vessel", value="")
        self._year = StringVar(name="year", value="")
        self._referral = StringVar(name="referral", value="")

    def _create_widgets(
        self,
        submission_info: Submission,
        months: list[str],
    ):
        client_name = " ".join(
            [
                submission_info.fname,
                submission_info.lname,
            ]
        )

        self.root.text_frame.grid_columnconfigure(0, weight=1)
        self.root.btn_frame.grid_columnconfigure(0, weight=1)

        Label(self.root.text_frame, text="Client name: ", bg="#CFEBDF").grid(
            column=0, row=0, pady=(3, 0)
        )
        name_entry = Entry(
            self.root.text_frame,
            width=30,
            justify="center",
            bg="#5F634F",
            fg="#FFCAB1",
            state="inactive",
        )
        name_entry.insert(0, client_name)
        name_entry.grid(column=0, row=1, pady=(0, 8))

        Label(self.root.text_frame, text="Vessel: ", bg="#CFEBDF").grid(column=0, row=2)
        vessel_entry = Entry(
            self.root.text_frame,
            textvariable=self._vessel,
            width=30,
            justify="center",
            bg="#5F634F",
            fg="#FFCAB1",
        )
        self.vessel = submission_info.vessel
        vessel_entry.grid(column=0, row=3, pady=(0, 8))

        Label(self.root.text_frame, text="Vessel year: ", bg="#CFEBDF").grid(
            column=0, row=4
        )
        year_entry = Entry(
            self.root.text_frame,
            textvariable=self._year,
            width=10,
            justify="center",
            bg="#5F634F",
            fg="#FFCAB1",
        )
        self.year = submission_info.vessel_year
        year_entry.grid(column=0, row=5, pady=(0, 8))

        Label(self.root.text_frame, text="Referral: ", bg="#CFEBDF").grid(
            column=0, row=6
        )
        referral_entry = Entry(
            self.root.text_frame,
            textvariable=self._referral,
            width=30,
            justify="center",
            bg="#5F634F",
            fg="#FFCAB1",
        )
        self.referral = submission_info.quoteform.referral
        referral_entry.grid(column=0, row=7, pady=(0, 7))
        if submission_info.quoteform.referral.lower() == "renewal":
            Label(self.root.text_frame, text="Add Client to Month:", bg="#CFEBDF").grid(
                column=0, row=8
            )
            self.root.geometry("300x448")
            options: list[str] = [
                months[0].capitalize(),
                months[1].capitalize(),
                months[2].capitalize(),
            ]
            dropdown_menu = OptionMenu(
                self.root.text_frame, self._selected_template, *options
            )
            dropdown_menu.configure(
                background="#1D3461",
                foreground="#CFEBDF",
                activebackground="#203b6f",
                activeforeground="#CFEBDF",
                highlightbackground="#5F634F",
                highlightcolor="red",
                font=("helvetica", 14, "normal"),
            )
            dropdown_menu["menu"].configure(
                background="#5F634F",
                foreground="#FFCAB1",
                activebackground="#FFCAB1",
                activeforeground="#5F634F",
                selectcolor="red",
            )
            dropdown_menu.grid(column=0, row=9, pady=(0, 7))

        create_folder_only_btn = Button(
            self.root.btn_frame,
            text="Create Folder & Track Client",
            width=36,
            height=3,
            command=lambda: self.presenter.choice("track_create"),
            default="active",
            bg="#1D3461",
            fg="#CFEBDF",
        )
        create_folder_only_btn.grid(row=0, column=0, padx=5, pady=(0, 0))

        allocate_btn = Button(
            self.root.btn_frame,
            text="Create & Track Client + Allocate Markets",
            width=36,
            height=3,
            command=lambda: self.presenter.choice("track_allocate"),
            default="active",
            bg="#1D3461",
            fg="#CFEBDF",
        )
        allocate_btn.grid(row=1, column=0, padx=5, pady=(3, 3))

        submit_btn = Button(
            self.root.btn_frame,
            text="Create & Track Client + SUBMIT to Markets",
            width=36,
            height=3,
            command=lambda: self.presenter.choice("track_submit"),
            default="active",
            bg="#1D3461",
            fg="#CFEBDF",
        )
        submit_btn.grid(row=2, column=0, padx=5, pady=(0, 5))
