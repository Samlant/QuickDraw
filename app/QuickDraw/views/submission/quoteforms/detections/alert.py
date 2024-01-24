from typing import Protocol
from dataclasses import dataclass

from tkinter import *


class Presenter(Protocol):
    def choice(self, choice: str):
        ...

    def save_user_choices(self, event):
        ...


@dataclass
class ClientInfo:
    fname: str
    lname: str
    vessel: str
    vessel_year: int
    referral: str


class DialogNewFile:
    def __init__(
        self,
        icon_src,
    ) -> None:
        self.submission_info = None
        self.root: Tk = None
        self.presenter: Presenter = None
        self.icon_path = icon_src

    @property
    def selected_month(self) -> str:
        return self._dropdown_menu_var.get().lower()

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
        submission_info: ClientInfo,
        current_month: str,
        next_month: str,
        second_month: str,
    ) -> str:
        self.presenter = presenter
        self._setup_window(current_month)
        self._create_widgets(submission_info, current_month, next_month, second_month)

    def _setup_window(self, current_month: str):
        self.root = Tk()
        self.root.geometry("300x400")
        self.root.title("Next Steps")
        self.root.iconbitmap(self.icon_path)
        self.root.text_frame = Frame(self.root, bg="#CFEBDF")
        self.root.text_frame.pack(fill=BOTH, expand=True)
        self.root.btn_frame = Frame(self.root, bg="#CFEBDF")
        self.root.btn_frame.pack(fill=BOTH, expand=True, ipady=2)
        self._dropdown_menu_var = StringVar(value=current_month.capitalize())
        self._vessel = StringVar(name="vessel", value="")
        self._year = StringVar(name="year", value="")
        self._referral = StringVar(name="referral", value="")

    def _create_widgets(
        self,
        submission_info,
        current_month: str,
        next_month: str,
        second_month: str,
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
            self.root.text_frame, width=30, justify="center", bg="#5F634F", fg="#FFCAB1"
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
        self.referral = submission_info.referral
        referral_entry.grid(column=0, row=7, pady=(0, 7))
        if submission_info.referral.lower() == "renewal":
            Label(self.root.text_frame, text="Add Client to Month:", bg="#CFEBDF").grid(
                column=0, row=8
            )
            self.root.geometry("300x448")
            options: list[str] = [
                current_month.capitalize(),
                next_month.capitalize(),
                second_month.capitalize(),
            ]
            dropdown_menu = OptionMenu(
                self.root.text_frame, self._dropdown_menu_var, *options
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
            default=ACTIVE,
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
            default=ACTIVE,
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
            default=ACTIVE,
            bg="#1D3461",
            fg="#CFEBDF",
        )
        submit_btn.grid(row=2, column=0, padx=5, pady=(0, 5))

