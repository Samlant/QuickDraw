from typing import Protocol
from dataclasses import dataclass

from tkinter import Tk, IntVar, Checkbutton, ttk


class Presenter(Protocol):
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
        self.root.attributes("-topmost", True)
        self.root.update()
        self.root.attributes("-topmost", False)
        self.root.iconbitmap(self.icon_path)
        self.root.frame = ttk.Frame(self.root, bg="#CFEBDF")
        self.root.frame.pack(fill="both", expand=False)
        self.ch_checkbtn = IntVar(self.root)
        self.mk_checkbtn = IntVar(self.root)
        self.ai_checkbtn = IntVar(self.root)
        self.am_checkbtn = IntVar(self.root)
        self.pg_checkbtn = IntVar(self.root)
        self.sw_checkbtn = IntVar(self.root)
        self.km_checkbtn = IntVar(self.root)
        self.cp_checkbtn = IntVar(self.root)
        self.nh_checkbtn = IntVar(self.root)
        self.In_checkbtn = IntVar(self.root)
        self.tv_checkbtn = IntVar(self.root)
        self._create_widgets()
        self.root.mainloop()

    def _create_widgets(self):
        ttk.Label(
            self.root.frame,
            text="ALLOCATE MARKETS",
            justify="center",
            bg="#CFEBDF",
            fg="#5F634F",
        ).pack(fill="x", ipady=6)
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

        allocate_btn = ttk.Button(
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
            fill="x",
            expand=False,
            pady=5,
            padx=10,
            ipady=6,
            ipadx=10,
        )

    def __create_button(self, text: str, var: IntVar):
        x = Checkbutton(
            self.root.frame,
            text=text,
            variable=var,
            relief="raised",
            # font=("helvetica", 10, "bold"),
            justify="center",
            anchor="w",
            fg="#FFCAB1",
            bg="#5F634F",
            selectcolor="#000000",
        )
        x.pack(
            fill="x",
            expand=False,
            ipady=6,
            ipadx=10,
            pady=3,
            padx=10,
            anchor="nw",
        )

    @property
    def markets(self) -> dict[str, any]:
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
