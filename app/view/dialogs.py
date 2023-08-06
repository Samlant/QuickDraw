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

    def initialize(self, presenter: Presenter, submission_info: ClientInfo) -> str:
        self.presenter = presenter
        self._setup_window()
        self._create_widgets(submission_info)

    def _setup_window(self):
        self.root = Tk()
        self.root.geometry("300x400")
        self.root.title("Next Steps")
        self.root.iconbitmap(self.icon_path)
        self.root.text_frame = Frame(self.root, bg="#CFEBDF")
        self.root.text_frame.pack(fill=BOTH, expand=True)
        self.root.btn_frame = Frame(self.root, bg="#CFEBDF")
        self.root.btn_frame.pack(fill=BOTH, expand=True, ipady=2)

    def _create_widgets(self, submission_info):
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
            self.root.text_frame, width=30, justify="center", bg="#5F634F", fg="#FFCAB1"
        )
        vessel_entry.insert(0, submission_info.vessel)
        vessel_entry.grid(column=0, row=3, pady=(0, 8))

        Label(self.root.text_frame, text="Vessel year: ", bg="#CFEBDF").grid(
            column=0, row=4
        )
        year_entry = Entry(
            self.root.text_frame, width=10, justify="center", bg="#5F634F", fg="#FFCAB1"
        )
        year_entry.insert(0, submission_info.vessel_year)
        year_entry.grid(column=0, row=5, pady=(0, 8))

        Label(self.root.text_frame, text="Referral: ", bg="#CFEBDF").grid(
            column=0, row=6
        )
        referral_entry = Entry(
            self.root.text_frame,
            width=30,
            justify="center",
            bg="#5F634F",
            fg="#FFCAB1",
        )
        referral_entry.insert(0, submission_info.referral)
        referral_entry.grid(column=0, row=7, pady=(0, 7))

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


class DialogAllocateMarkets:
    def __init__(self, icon_src) -> None:
        self.icon_path = icon_src
        self.market_info: dict[str, any] = None
        self.root: Tk = None
        self.presenter: Presenter = None

    def initialize(self, presenter: Presenter):
        self.presenter = presenter
        self.root = Tk()
        self.root.geometry("260x560")
        self.root.title("Allocate Markets")
        self.root.iconbitmap(self.icon_path)
        self.root.frame = Frame(self.root, bg="#CFEBDF")
        self.root.frame.pack(fill=BOTH, expand=False)
        self.ch_checkbtn = IntVar(self.root.frame)
        self.mk_checkbtn = IntVar(self.root.frame)
        self.ai_checkbtn = IntVar(self.root.frame)
        self.am_checkbtn = IntVar(self.root.frame)
        self.pg_checkbtn = IntVar(self.root.frame)
        self.sw_checkbtn = IntVar(self.root.frame)
        self.km_checkbtn = IntVar(self.root.frame)
        self.cp_checkbtn = IntVar(self.root.frame)
        self.nh_checkbtn = IntVar(self.root.frame)
        self.In_checkbtn = IntVar(self.root.frame)
        self.tv_checkbtn = IntVar(self.root.frame)
        self._create_widgets()

    def _create_widgets(self):
        Label(
            self.root.frame,
            text="ALLOCATE MARKETS",
            justify="center",
            bg="#CFEBDF",
            fg="#5F634F",
        ).pack(fill=X, ipady=6)
        self.__create_button("Chubb", self.ch_checkbtn)
        self.__create_button("Markel", self.mk_checkbtn)
        self.__create_button("American Integrity", self.ai_checkbtn)
        self.__create_button("American Modern", self.am_checkbtn)
        self.__create_button("Progressive", self.pg_checkbtn)
        self.__create_button("Seawave", self.sw_checkbtn)
        self.__create_button("Kemah Marine", self.km_checkbtn)
        self.__create_button("Concept Special Risks", self.cp_checkbtn)
        # self.yi_checkbtn = IntVar(self.root.frame)
        # self.__create_button("Yachtinsure", self.yi_checkbtn)
        self.__create_button("New Hampshire", self.nh_checkbtn)
        # self.sf_checkbtn = IntVar(self.root.frame)
        # self.__create_button("Seafarer", self.sf_checkbtn)
        self.__create_button("Intact", self.In_checkbtn)
        self.__create_button("Travelers", self.tv_checkbtn)

        allocate_btn = Button(
            master=self.root.frame,
            text="ALLOCATE",
            width=30,
            height=10,
            # font=("helvetica", 14, "bold"),
            bg="#1D3461",
            fg="#CFEBDF",
            command=self.presenter.save_user_choices,
        )
        allocate_btn.pack(
            fill=X,
            expand=False,
            pady=5,
            padx=10,
            ipady=6,
            ipadx=10,
        )

    def __create_button(self, text: str, int_variable: IntVar):
        x = Checkbutton(
            self.root.frame,
            text=text,
            variable=int_variable,
            relief="raised",
            # font=("helvetica", 10, "bold"),
            justify=CENTER,
            anchor=W,
            fg="#FFCAB1",
            bg="#5F634F",
            selectcolor="#000000",
        )
        x.pack(
            fill=X,
            expand=False,
            ipady=6,
            ipadx=10,
            pady=3,
            padx=10,
            anchor=NW,
        )

    def get_markets(self) -> dict[str, any]:
        """Retrieves all market options and
        whether the user wants to submit to
        those markets within a dict."""
        dict_of_markets = {
            "ch": self.ch_checkbtn.get(),
            "mk": self.mk_checkbtn.get(),
            "ai": self.ai_checkbtn.get(),
            "am": self.am_checkbtn.get(),
            "pg": self.pg_checkbtn.get(),
            "sw": self.sw_checkbtn.get(),
            "km": self.km_checkbtn.get(),
            "cp": self.cp_checkbtn.get(),
            # "yi": self.yi_checkbtn.get(),
            "nh": self.nh_checkbtn.get(),
            # "sf": self.sf_checkbtn.get(),
            "In": self.In_checkbtn.get(),
            "tv": self.tv_checkbtn.get(),
        }
        self.root.destroy()
        return dict_of_markets


class DialogAuthAPI:
    def __init__(self):
        self.presenter = presenter
        self.root = Tk()
        self.root.geometry("300x50")
        self.root.title("Login")
        # self.root.iconbitmap(self.icon_path)
        self.URI_second = StringVar(self.root.frame, name="second_URI")
        self.root.frame = Frame(self.root, bg="#CFEBDF")
        self.root.frame.pack(fill=BOTH, expand=False)
        self._create_widgets()

    def _create_widgets(self):
        Label(text="Test:", font=(None, 28), width=9).grid(column=0, row=0)
        Entry(
            master=self.root.frame,
            name="second URI entry",
            textvariable=self.URI_second,
        ).grid(column=0, row=1)
        Button(master=self.root.frame, text="Submit", command=self.return_URI)

    def return_URI(self):
        pass
