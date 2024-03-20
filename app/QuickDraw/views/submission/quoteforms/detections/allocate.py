from typing import Protocol
from operator import attrgetter
from tkinter import Tk, BooleanVar, ttk

from tkinterdnd2 import TkinterDnD


from QuickDraw.helper import AVAILABLE_CARRIERS
from QuickDraw.views.submission.helper import make_checkbutton
from QuickDraw.views.themes.applicator import create_style


class Presenter(Protocol):
    def save_allocated_markets(self, event):
        ...


class AllocateView:
    def __init__(self, icon_src) -> None:
        self.icon_src: str = icon_src
        self.market_info: dict[str, any] = None
        self.root: Tk = None
        self.presenter: Presenter = None

    @property
    def Seawave(self) -> str:
        return self._Seawave.get()

    @property
    def Primetime(self) -> str:
        return self._Primetime.get()

    @property
    def NewHampshire(self) -> str:
        return self._NewHampshire.get()

    @property
    def AmericanModern(self) -> str:
        return self._AmericanModern.get()

    @property
    def Kemah(self) -> str:
        return self._Kemah.get()

    @property
    def Concept(self) -> str:
        return self._Concept.get()

    @property
    def Yachtinsure(self) -> str:
        return self._Yachtinsure.get()

    @property
    def Century(self) -> str:
        return self._Century.get()

    @property
    def Intact(self) -> str:
        return self._Intact.get()

    @property
    def Travelers(self) -> str:
        return self._Travelers.get()

    def initialize(
        self,
        presenter: Presenter,
        view_palette,
    ):
        self.root = TkinterDnD.Tk()
        self.style = create_style(self.root, view_palette)
        self.palette = view_palette
        self.presenter = presenter
        self.assign_window_traits()
        self.assign_vars()
        self._create_widgets()
        self.root.mainloop()

    def assign_window_traits(self):
        self.root.iconbitmap(self.icon_src)
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
