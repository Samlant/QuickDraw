from tkinter import ttk, Text, Frame, StringVar, BooleanVar, IntVar, Checkbutton
from tkinter.ttk import OptionMenu
from typing import Protocol
from dataclasses import dataclass

from tkinterdnd2 import DND_FILES

from QuickDraw.helper import POSITIVE_SUBMISSION_VALUE, NEGATIVE_SUBMISSION_VALUE
from QuickDraw.views.submission import base
from QuickDraw.views.themes.palettes import Palette


class Presenter(Protocol):
    ...


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


def make_checkbutton(parent, text: str, int_variable: IntVar):
    x = Checkbutton(
        parent=parent,
        name=text.lower(),
        text=text,
        variable=int_variable,
        onvalue=POSITIVE_SUBMISSION_VALUE,
        offvalue=NEGATIVE_SUBMISSION_VALUE,
        relief="raised",
        # font=("helvetica", 10, "bold"),
        justify="center",
        anchor="w",
        fg="#FFCAB1",
        bg="#5F634F",
        selectcolor="#000000",
    )
    x.pack(fill="both", expand=True, ipady=3, ipadx=40, pady=(0, 3))


def create_dropdown(
    view: base.Submission, parent, presenter: Presenter, style: Palette
) -> OptionMenu:
    """Creates the OptionMenu widget separately for less coupling."""
    options: list[str] = presenter.set_dropdown_options()
    menu = OptionMenu(parent, view._dropdown_menu_var, *options)
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


@dataclass
class BaseVars:
    # main_tab vars
    _use_CC_defaults = BooleanVar(name="use_CC_defaults")
    _seawave = StringVar(
        name="Seawave",
        value=NEGATIVE_SUBMISSION_VALUE,
    )
    _primetime = StringVar(
        name="Primetime",
        value=NEGATIVE_SUBMISSION_VALUE,
    )
    _newhampshire = StringVar(
        name="NewHampshire",
        value=NEGATIVE_SUBMISSION_VALUE,
    )
    _americanmodern = StringVar(
        name="AmericanModern",
        value=NEGATIVE_SUBMISSION_VALUE,
    )
    _kemah = StringVar(
        name="Kemah",
        value=NEGATIVE_SUBMISSION_VALUE,
    )
    _concept = StringVar(
        name="Concept",
        value=NEGATIVE_SUBMISSION_VALUE,
    )
    _yachtinsure = StringVar(
        name="Yachtinsure",
        value=NEGATIVE_SUBMISSION_VALUE,
    )
    _century = StringVar(
        name="Century",
        value=NEGATIVE_SUBMISSION_VALUE,
    )
    _intact = StringVar(
        name="Intact",
        value=NEGATIVE_SUBMISSION_VALUE,
    )
    _travelers = StringVar(
        name="Travelers",
        value=NEGATIVE_SUBMISSION_VALUE,
    )
    # customize_tab vars
    _dropdown_menu_var = StringVar(value="dropdown_menu_var")
    _address = StringVar(name="address", value="")
    _greeting = StringVar(name="greeting", value="")
    _salutation = StringVar(name="salutation", value="")
    _outro = StringVar(name="outro", value="")
    # settings_tab vars
    _username = StringVar(name="username", value="")
    _default_cc1 = StringVar(name="default_cc1", value="")
    _default_cc2 = StringVar(name="default_cc2", value="")
    _watch_dir = StringVar(name="watch_dir", value="")
    _new_biz_dir = StringVar(name="new_biz_dir", value="")
    _renewals_dir = StringVar(name="renewals_dir", value="")
    _custom_parent_dir = StringVar(name="custom_parent_dir", value="")
    _custom_sub_dir = StringVar(name="custom_sub_dir", value="")
    # registrations_tab vars
    _form_name = StringVar(name="form_name", value="")
    _fname = StringVar(name="fname", value="")
    _lname = StringVar(name="lname", value="")
    _year = StringVar(name="year", value="")
    _vessel = StringVar(name="vessel", value="")
    _referral = StringVar(name="referral", value="")
    # self._quoteform_name = StringVar(name="quoteform_name", value="")
