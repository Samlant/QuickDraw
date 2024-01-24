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
