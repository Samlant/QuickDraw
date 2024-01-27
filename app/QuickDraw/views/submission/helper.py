from tkinter import Text, Frame, StringVar, BooleanVar, IntVar, Checkbutton
from tkinter.ttk import OptionMenu
from typing import Protocol
from dataclasses import dataclass

from tkinterdnd2 import DND_FILES

from QuickDraw.helper import GREEN_LIGHT, RED_LIGHT
from QuickDraw.views.submission import base
from QuickDraw.views.themes.palettes import Palette


class Presenter(Protocol):
    def set_dropdown_options(self) -> list:
        ...


class MyStringVars(StringVar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def set_start_tab(self, specific_tab: str) -> None:
    if specific_tab == "template":
        self.root.tabControl.select(1)
    elif specific_tab == "email":
        self.root.tabControl.select(2)
    elif specific_tab == "folder":
        self.root.tabControl.select(3)


def make_draggable_txt_box(
    parent,
    name: str,
    height: int,
    width: int,
    palette: Palette,
    command,
):
    box = Text(
        parent,
        name=name,
        height=height,
        width=width,
        foreground=palette.alt_fg_color,
        background=palette.alt_bg_color,
        highlightcolor=palette.alt_bg_color,
        selectbackground=palette.alt_fg_color,
        selectforeground=palette.alt_bg_color,
    )
    box.drop_target_register(DND_FILES)
    box.dnd_bind("<<Drop>>", command)
    return box


def make_drag_drop_txt_box(
    parent: Frame,
    style: Palette,
    name: str,
    command,
) -> Text:
    """Creates the drag-n-drop box for any extra attachments."""
    box = Text(
        parent,
        name=name,
        height=8,
        width=10,
        foreground=style.alt_fg_color,
        background=style.alt_bg_color,
        highlightcolor=style.alt_bg_color,
        selectbackground=style.alt_fg_color,
        selectforeground=style.alt_bg_color,
    )
    box.drop_target_register(DND_FILES)
    box.dnd_bind("<<Drop>>", command)
    return box


def make_checkbutton(parent, text: str, var: StringVar | IntVar | BooleanVar):
    x = Checkbutton(
        parent=parent,
        name=text.lower(),
        text=text,
        variable=var,
        onvalue=GREEN_LIGHT,
        offvalue=RED_LIGHT,
        relief="raised",
        # font=("helvetica", 10, "bold"),
        justify="center",
        anchor="w",
        fg="#FFCAB1",
        bg="#5F634F",
        selectcolor="#000000",
    )
    x.pack(fill="both", expand=True, ipady=3, ipadx=40, pady=(0, 3))


def create_dropdown(view, parent, presenter: Presenter, style: Palette) -> OptionMenu:
    """Creates the OptionMenu widget separately for less coupling."""
    options: list[str] = presenter.set_dropdown_options()
    menu = OptionMenu(parent, view._selected_template, *options)
    menu.configure(
        background=style.btn_base_bg,
        foreground=style.btn_fg,
        activebackground=style.btn_active_bg,
        activeforeground=style.btn_fg,
        highlightbackground=style.alt_bg_color,
        highlightcolor="red",
        font=("helvetica", 14, "normal"),
        width=54,
    )
    menu["menu"].configure(
        background=style.menuoption_bg_color,
        foreground=style.menuoption_fg_color,
        activebackground=style.menuoption_fg_color,
        activeforeground=style.menuoption_bg_color,
        selectcolor="red",
    )
    return menu


ALL_TABS = {
    "home": {
        "quoteform": "text",
        "extra_attachments": "text",
        "extra_notes": "text",
        "userinput_CC1": "text",
        "userinput_CC2": "text",
        "use_CC_defaults": "bool",
    },
    "templates": {
        "selected_template": "str",
        "address": "str",
        "greeting": "str",
        "body": "str",
        "outro": "str",
        "salutation": "str",
    },
    "email": {
        "default_cc1": "str",
        "default_cc2": "str",
        "username": "str",
        "sig_image_file_path": "text",
    },
    "dirs": {
        "watch_dir": "str",
        "new_biz_dir": "str",
        "renewals_dir": "str",
        "custom_parent_dir": "str",
        "custom_sub_dir": "str",
    },
    "quoteforms": {
        "form_name": "str",
        "fname": "str",
        "lname": "str",
        "year": "str",
        "vessel": "str",
        "referral": "str",
    },
}
