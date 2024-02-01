from typing import Protocol
from dataclasses import dataclass
from operator import attrgetter

from tkinter import Tk, BooleanVar, Checkbutton, ttk, Toplevel

from QuickDraw.helper import AVAILABLE_CARRIERS
from QuickDraw.views.submission.helper import make_checkbutton
from QuickDraw.views.themes.applicator import create_style


class Presenter(Protocol):
    def save_allocated_markets(self, event):
        ...


class AllocateView:
    def __init__(self, icon_src) -> None:
        self.icon_path: str = icon_src
        self.market_info: dict[str, any] = None
        self.root: Tk = None
        self.presenter: Presenter = None

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
    
    def initialize(
        self,
        presenter: Presenter,
        view_interpreter: Tk,
        view_palette,
    ):
        self.root: Toplevel = Toplevel(
            master=view_interpreter,
            background=view_palette.base_bg_color,
        )
        self.style = create_style(self.root, view_palette)
        self.palette = view_palette
        self.presenter = presenter
        self.assign_window_traits()
        self.assign_vars()
        self._create_widgets()
        self.root.mainloop()

    def assign_window_traits(self):
        self.root.iconbitmap(self.icon_path)
        self.root.geometry("260x560")
        self.root.title("Allocate Markets")
        self.root.attributes("-topmost", True)
        self.root.update()
        self.root.attributes("-topmost", False)

    def assign_vars(self):
        for carrier in AVAILABLE_CARRIERS:
            var = BooleanVar(
                master=self.root,
                value=False,
                name=carrier.name,
            )
            setattr(self, "_" + carrier.name, var),

    def _create_widgets(self):
        frame = ttk.Frame(self.root, style=self.style)
        frame.pack(fill="both", expand=False)
        ttk.Label(
            frame,
            style=self.style,
            text="ALLOCATE MARKETS",
            justify="center",
        ).pack(fill="x", ipady=6)
        for carrier in AVAILABLE_CARRIERS:
            attr_name = f"_{carrier.name}"
            var = attrgetter(attr_name)(self)
            chckbtn = make_checkbutton(
                parent=frame,
                text=carrier.friendly_name,
                var=var,
            )
            chckbtn.pack(
                fill="x",
                expand=False,
                ipady=6,
                ipadx=10,
                pady=3,
                padx=10,
                anchor="nw",
            )
        allocate_btn = ttk.Button(
            master=frame,
            text="ALLOCATE",
            width=30,
            height=10,
            command=self.presenter.save_allocated_markets,
        )
        allocate_btn.pack(
            fill="x",
            expand=False,
            pady=5,
            padx=10,
            ipady=6,
            ipadx=10,
        )

    def __create_button(self, text: str, var: BooleanVar):
        x = Checkbutton(
            parent=frame,
            text=text,
            variable=var,
            onvalue=True,
            offvalue=False,
            relief="raised",
            justify="center",
            anchor="w",
            background=self.palette.alt_bg_color,
            foreground=self.palette.alt_fg_color,
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

