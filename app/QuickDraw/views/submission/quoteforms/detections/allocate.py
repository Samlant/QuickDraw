from typing import Protocol
from dataclasses import dataclass

from tkinter import *


class Presenter(Protocol):
    def choice(self, choice: str):
        ...

    def save_user_choices(self, event):
        ...


@dataclass
class ClientInfo(Protocol):
    fname: str
    lname: str
    vessel: str
    vessel_year: int
    referral: str


class DialogAllocateMarkets:
    def __init__(self, icon_src) -> None:
        self.icon_path: str = icon_src
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
