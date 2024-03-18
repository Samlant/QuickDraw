from tkinter import Text, Frame, StringVar, BooleanVar, Checkbutton, OptionMenu
# from tkinter.ttk import OptionMenu
from typing import Protocol

from tkinterdnd2 import DND_FILES

from QuickDraw.views.themes.palettes import Palette


class Presenter(Protocol):
    def get_carrier_combos(self, all: bool) -> list: ...


class MyStringVars(StringVar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def set_start_tab(obj, specific_tab: str) -> None:
    if specific_tab == "template":
        obj.root.tabControl.select(1)
    elif specific_tab == "email":
        obj.root.tabControl.select(2)
    elif specific_tab == "folder":
        obj.root.tabControl.select(3)
    elif specific_tab == "forms":
        obj.root.tabControl.select(4)
    obj.root.attributes("-topmost", True)
    obj.root.update()
    obj.root.attributes("-topmost", False)
    obj.root.mainloop()


def make_drag_drop_txt_box(
    parent: Frame,
    palette: Palette,
    name: str,
    command,
) -> Text:
    """Creates the drag-n-drop box for any extra attachments."""
    box = Text(
        parent,
        name=name,
        height=8,
        width=10,
        foreground=palette.alt_fg_color,
        background=palette.alt_bg_color,
        highlightcolor=palette.alt_bg_color,
        selectbackground=palette.alt_fg_color,
        selectforeground=palette.alt_bg_color,
    )
    box.drop_target_register(DND_FILES)
    box.dnd_bind("<<Drop>>", command)
    return box


def make_checkbutton(parent, text: str, var: BooleanVar):
    x = Checkbutton(
        master=parent,
        name=text.lower(),
        text=text,
        variable=var,
        onvalue=True,
        offvalue=False,
        relief="raised",
        # font=("helvetica", 10, "bold"),
        justify="center",
        anchor="w",
        fg="#FFCAB1",
        bg="#5F634F",
        selectcolor="#000000",
    )
    return x


def create_dropdown(view, parent, presenter: Presenter, palette: Palette) -> OptionMenu:
    """Creates the OptionMenu widget separately for less coupling."""
    options: list[str] = presenter.get_carrier_combos(all=True)
    menu = OptionMenu(parent,
                      view._selected_template,
                      *options)
    menu.configure(
        background=palette.btn_base_bg,
        foreground=palette.btn_fg,
        activebackground=palette.btn_active_bg,
        activeforeground=palette.btn_fg,
        highlightbackground=palette.alt_bg_color,
        highlightcolor="red",
        font=("helvetica", 14, "normal"),
        width=54,
    )
    menu["menu"].configure(
        background=palette.menuoption_bg_color,
        foreground=palette.menuoption_fg_color,
        activebackground=palette.menuoption_fg_color,
        activeforeground=palette.menuoption_bg_color,
        selectcolor="red",
    )
    return menu


ALL_TABS = {
    "home": {
        "quoteform": "text",
        "attachments": "text",
        "extra_notes": "text",
        "user_CC1": "text",
        "user_CC2": "text",
        "use_CC_defaults": "bool",
    },
    "template": {
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
        "office_phone": "str",
        "office_fax": "str",
        "office_street": "str",
        "office_city_st_zip": "str",
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
