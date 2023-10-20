from tkinter import *
from tkinter import ttk
from tkinter.ttk import Style
from dataclasses import dataclass


@dataclass
class BlueRose:
    base_bg_color = "#CFEBDF"
    base_fg_color = "#5F634F"  # black or grey
    alt_bg_color = "#5F634F"  # dark grey; for text inputs + chkbtns
    alt_fg_color = "#FFCAB1"  # pink
    dragdrop_bg_color = "#5F634F"  # temp: same as text inputs
    menuoption_bg_color = "#5F634F"  # dark grey; same as text inputs
    menuoption_fg_color = "#FFCAB1"  # pink
    btn_base_bg = "#1D3461"
    btn_active_bg = "#203b6f"
    btn_pressed_bg = "#16294d"
    btn_fg = "#CFEBDF"
    chck_btn_bg = "#5F634F"
    chck_btn_fg = "#FFCAB1"
    chck_btn_select_color = "#000000"


BR = BlueRose()


def create_style(master_object):
    s = Style(master_object)
    s.theme_use("alt")
    s = assign_default_static_colors(s)
    s = map_default_dynamic_colors(s)
    s = assign_custom_static_colors(s)
    s = map_custom_dynamic_colors(s)
    return s


def assign_default_static_colors(style_object):
    s = style_object
    s.configure(
        "TNotebook",
        background=BR.base_bg_color,
    )

    s.configure(
        "TFrame",
        background=BR.base_bg_color,
    )
    s.configure(
        "TLabelframe",
        background=BR.base_bg_color,
    )
    s.configure(
        "TLabelframe.Label",
        background=BR.base_bg_color,
        font=("helvetica", 14, "normal"),
    )
    s.configure(
        "TButton",
        background=BR.btn_base_bg,
        foreground=BR.btn_fg,
        font=("helvetica", 12, "bold"),
    )
    # s.configure(
    #     "TCheckbutton",
    #     indicatorbackground="black",
    #     indicatorforeground="white",
    #     background="black",
    #     foreground="white",
    # )
    # s.configure(
    #     "TCheckbutton",
    #     background=BR.alt_bg_color,
    #     foreground=BR.alt_fg_color,
    #     indicatorcolor="black",
    #     selectbackground=BR.chck_btn_select_color,
    #     font=("helvetica", 12, "normal"),
    #     relief="raised",
    # )
    s.configure(
        "TEntry",
        background=BR.alt_bg_color,
        fieldbackground=BR.alt_bg_color,
        selectbackground=BR.alt_fg_color,
        selectforeground=BR.alt_bg_color,
        foreground=BR.alt_fg_color,
    )
    s.configure(
        "TLabel",
        background=BR.base_bg_color,
        foreground=BR.base_fg_color,
    )
    # s.configure(
    #     "TMenubutton",
    #     background=BR.menuoption_bg_color,
    #     foreground=BR.menuoption_fg_color,
    #     highlightbackground=BR.menuoption_bg_color,
    #     activebackground="red",
    #     font=("helvetica", 12, "normal"),
    # )
    s.configure(
        "Treeview",
        background=BR.alt_bg_color,
        foreground=BR.alt_fg_color,
        fieldbackground=BR.alt_bg_color,
    )
    s.configure(
        "Treeview.field",
        fieldbackground=BR.alt_bg_color,
    )
    return s


def map_default_dynamic_colors(style_obj):
    s = style_obj
    s.map(
        "TNotebook",
        background=[("selected", BR.base_bg_color)],
    )
    s.map(
        "TButton",
        background=[
            ("pressed", BR.btn_pressed_bg),
            ("active", BR.btn_active_bg),
        ],
        foreground=[
            ("pressed", BR.btn_fg),
            ("active", BR.btn_fg),
        ],
    )
    return s


def assign_custom_static_colors(style_obj):
    s = style_obj
    s.configure(
        "Header.TLabel",
        font=("helvetica", 20, "normal"),
    )
    return s


def map_custom_dynamic_colors(style_obj):
    s = style_obj
    return s
