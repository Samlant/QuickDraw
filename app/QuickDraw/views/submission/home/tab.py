from tkinter import ttk, Text, Checkbutton
from typing import Protocol
from operator import attrgetter
from QuickDraw.views.submission import base
from QuickDraw.views.submission.helper import make_drag_drop_txt_box, make_checkbutton
from QuickDraw.helper import AVAILABLE_CARRIERS

# from QuickDraw.views.submission.helper import create_button
from QuickDraw.views.themes.palettes import Palette


class Presenter(Protocol):
    def process_file_path(
        self,
        event,
        is_quoteform: bool,
        quote_path: str = None,
    ) -> None:
        ...

    def btn_clear_attachments(self) -> None:
        ...

    def btn_process_envelopes(self, autosend: bool | None) -> None:
        ...


def make_home_widgets(
    view: base.MainWindow,
    presenter: Presenter,
    palette: Palette,
):
    view.tabs.home.rowconfigure(2, minsize=100, pad=5)
    view.tabs.home.columnconfigure(0, pad=5)
    view.tabs.home.columnconfigure(1, pad=5)
    view.tabs.home.columnconfigure(2, pad=5)
    left_header_frame = ttk.Frame(view.tabs.home, style="TFrame")
    left_header_frame.grid(column=0, row=0, pady=(0, 5))
    ttk.Label(
        left_header_frame,
        text="Get Client Information",
        style="Header.TLabel",
    ).pack(fill="x", expand=True, side="left")
    frame_left = ttk.Frame(view.tabs.home, style="TFrame")
    frame_left.grid(column=0, row=1, sticky="n", pady=(5, 0), padx=(5, 0))
    labelframe_dd_qf = ttk.Labelframe(
        frame_left,
        text="Dag-N-Drop Quoteform Below",
        name="labelframe_dd_qf",
        style="TLabelframe"
    )
    ### Quoteform DnD Labelframe ###
    labelframe_dd_qf.pack(fill="none", expand=False, side="top")
    view._quoteform = make_drag_drop_txt_box(
        parent=labelframe_dd_qf,
        palette=palette,
        name="raw_quoteform_path",
        command=lambda: presenter.process_file_path(path_purpose="quoteform"),
    )
    view._quoteform.pack(fill="both", expand=False, anchor="n")
    ttk.Button(
        labelframe_dd_qf,
        text="Browse",
        command=lambda: presenter.browse_file_path(is_quoteform=True), style="TButton"
    ).pack(fill="none", pady=5, expand=False, side="top")
    ### Extra Attachments DnD Labelframe ###
    labelframe_dd_ea = ttk.Labelframe(
        frame_left,
        text="Dag-N-Drop Extra Files Below",
        name="labelframe_dd_ea", style="TLabelframe",
    )
    labelframe_dd_ea.pack(fill="none", expand=False, side="top", pady=(15, 0))
    view._extra_attachments = make_drag_drop_txt_box(
        parent=labelframe_dd_ea,
        palette=palette,
        name="raw_attachments_path_list",
        command=lambda: presenter.process_file_path(path_purpose="attachments"),
    )
    ttk.Button(
        labelframe_dd_ea,
        text="Browse",
        command=lambda: presenter.browse_file_path(is_quoteform=False), style="TButton",
    ).pack(fill="none", pady=5, expand=False, side="top")
    ttk.Button(
        view.tabs.home,
        text="Clear attachments",
        command=presenter.btn_clear_attachments, style="TButton",
    ).grid(column=0, row=2, sticky="nsew", padx=5, pady=10)

    middle_header_frame = ttk.Frame(view.tabs.home, style="TFrame",)
    middle_header_frame.grid(column=1, row=0, pady=(0, 5))
    ttk.Label(
        middle_header_frame,
        style="Header.TLabel",
        text="Extra Notes & CC",
    ).pack(fill="x", expand=True, side="left")
    frame_middle = ttk.Frame(view.tabs.home, style="TFrame",)
    frame_middle.grid(column=1, row=1, sticky="n")
    labelframe_main1 = ttk.Labelframe(
        frame_middle,
        text="Want to add any notes?", style="TLabelframe",
    )
    labelframe_main1.pack(fill="both", expand=True, side="top")
    view._extra_notes = Text(
        labelframe_main1,
        height=7,
        width=10,
        name="raw_extra_notes",
        background=palette.alt_bg_color,
        foreground=palette.alt_fg_color,
        highlightcolor=palette.alt_bg_color,
        selectbackground=palette.alt_fg_color,
        selectforeground=palette.alt_bg_color,
    )
    view._extra_notes.focus_set()
    view._extra_notes.pack(fill="both", expand=False, side="top")
    labelframe_cc = ttk.Labelframe(
        frame_middle,
        text="Want to CC Anyone?",
        name="labelframe_cc", style="TLabelframe",
    )
    labelframe_cc.pack(fill="x", expand=False, side="top", pady=(15, 0))
    Checkbutton(
        labelframe_cc,
        text="Include default CC addresses",
        variable=view._use_CC_defaults,
        name="cc_def_check",
        onvalue=True,
        offvalue=False,
        relief="raised",
        justify="center",
        anchor="w",
        background=palette.alt_bg_color,
        foreground=palette.alt_fg_color,
        highlightcolor=palette.alt_bg_color,
        selectcolor="#000000",
    ).pack(pady=5, expand=False, side="top", ipady=3)
    ttk.Label(
        labelframe_cc,
        text="Add emails here to copy them:", style="TLabel",
    ).pack(fill="x", expand=False, side="top")
    view._user_CC1 = Text(
        labelframe_cc,
        height=1,
        width=30,
        background=palette.alt_bg_color,
        foreground=palette.alt_fg_color,
        highlightcolor=palette.alt_bg_color,
        selectbackground=palette.alt_fg_color,
        selectforeground=palette.alt_bg_color,
    )
    view._user_CC1.pack(pady=2, ipady=4, anchor="n", fill="x", expand=False, side="top")
    ttk.Label(
        labelframe_cc,
        text="2nd Optional list to copy:", style="TLabel",
    ).pack(fill="x", expand=False, side="top")
    view._user_CC2 = Text(
        labelframe_cc,
        height=1,
        width=30,
        background=palette.alt_bg_color,
        foreground=palette.alt_fg_color,
        highlightcolor=palette.alt_bg_color,
        selectbackground=palette.alt_fg_color,
        selectforeground=palette.alt_bg_color,
    )
    view._user_CC2.pack(ipady=4, anchor="n", fill="x", expand=False, side="top")
    ttk.Button(
        view.tabs.home,
        text="View Each Before Sending!",
        command=lambda: presenter.btn_process_envelopes(view_first=True), style="TButton",
    ).grid(column=1, row=2, sticky="nsew", padx=(10), pady=10)
    # .pack(ipady=20, ipadx=2, pady=10, anchor=S, fill=Y, expand=False)
    right_header_frame = ttk.Frame(view.tabs.home)
    right_header_frame.grid(column=2, row=0, pady=5)
    ttk.Label(
        right_header_frame,
        style="Header.TLabel",
        text="Choose Markets:", style="TLabel",
    ).pack(fill="x", expand=True, side="left")

    frame_right = ttk.Frame(view.tabs.home, style="TFrame",)
    frame_right.grid(column=2, row=1, pady=(0, 5), sticky="n")
    for carrier in AVAILABLE_CARRIERS:
        attr_name = f"_{carrier.name}"
        var = attrgetter(attr_name)(view)
        chckbtn = make_checkbutton(
            parent=frame_right,
            text=carrier.friendly_name,
            var=var,
        )
        chckbtn.pack(fill="both", expand=True, ipady=3, ipadx=40, pady=(0, 3))

    ttk.Button(
        view.tabs.home,
        text="Submit & auto-send all",
        command=presenter.btn_process_envelopes, style="TButton",
    ).grid(column=2, row=2, sticky="nsew", padx=5, pady=10)
