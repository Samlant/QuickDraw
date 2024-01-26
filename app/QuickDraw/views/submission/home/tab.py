from tkinter import ttk, Text, Checkbutton
from typing import Protocol
from operator import attrgetter
from QuickDraw.views.submission import base
from QuickDraw.views.submission.helper import make_drag_drop_txt_box, make_checkbutton

# from QuickDraw.views.submission.helper import create_button
from QuickDraw.views.themes.palettes import palette


class Presenter(Protocol):
    ...


def make_home_widgets(view: base.Submission, presenter: Presenter, style: palette):
    view.tabs.home.rowconfigure(2, minsize=100, pad=5)
    view.tabs.home.columnconfigure(0, pad=5)
    view.tabs.home.columnconfigure(1, pad=5)
    view.tabs.home.columnconfigure(2, pad=5)
    left_header_frame = ttk.Frame(view.tabs.home)
    left_header_frame.grid(column=0, row=0, pady=(0, 5))
    ttk.Label(
        left_header_frame,
        text="Get Client Information",
        style="Header.TLabel",
    ).pack(fill="x", expand=True, side="left")
    frame_left = ttk.Frame(view.tabs.home)
    frame_left.grid(column=0, row=1, sticky="n", pady=(5, 0), padx=(5, 0))
    labelframe_dd_qf = ttk.Labelframe(
        frame_left,
        text="Dag-N-Drop Quoteform Below",
        name="labelframe_dd_qf",
    )
    ### Quoteform DnD Labelframe ###
    labelframe_dd_qf.pack(fill="none", expand=False, side="top")
    view.quoteform_path_box = make_drag_drop_txt_box(
        labelframe_dd_qf,
        style,
        "raw_quoteform_path",
        presenter.process_quoteform_path,
    )
    view.quoteform_path_box.pack(fill="both", expand=False, anchor="n")
    ttk.Button(
        labelframe_dd_qf,
        text="Browse",
        command=view._browse_qf_path,
    ).pack(fill="none", pady=5, expand=False, side="top")
    ### Extra Attachments DnD Labelframe ###
    labelframe_dd_ea = ttk.Labelframe(
        frame_left,
        text="Dag-N-Drop Extra Files Below",
        name="labelframe_dd_ea",
    )
    labelframe_dd_ea.pack(fill="none", expand=False, side="top", pady=(15, 0))
    view.extra_attachments_path_box = make_drag_drop_txt_box(
        labelframe_dd_ea,
        style,
        "raw_attachments_path_list",
        presenter.process_attachments_path,
    )
    ttk.Button(
        labelframe_dd_ea,
        text="Browse",
        command=view._browse_extra_file_path,
    ).pack(fill="none", pady=5, expand=False, side="top")
    ttk.Button(
        view.tabs.home,
        text="Clear attachments",
        command=presenter.btn_clear_attachments,
    ).grid(column=0, row=2, sticky="nsew", padx=5, pady=10)

    middle_header_frame = ttk.Frame(view.tabs.home)
    middle_header_frame.grid(column=1, row=0, pady=(0, 5))
    ttk.Label(
        middle_header_frame,
        style="Header.TLabel",
        text="Extra Notes & CC",
    ).pack(fill="x", expand=True, side="left")
    frame_middle = ttk.Frame(view.tabs.home)
    frame_middle.grid(column=1, row=1, sticky="n")
    labelframe_main1 = ttk.Labelframe(
        frame_middle,
        text="Want to add any notes?",
    )
    labelframe_main1.pack(fill="both", expand=True, side="top")
    view._extra_notes_text = Text(
        labelframe_main1,
        height=7,
        width=10,
        name="raw_extra_notes",
        background=style.alt_bg_color,
        foreground=style.alt_fg_color,
        highlightcolor=style.alt_bg_color,
        selectbackground=style.alt_fg_color,
        selectforeground=style.alt_bg_color,
    )
    view._extra_notes_text.focus_set()
    view._extra_notes_text.pack(fill="both", expand=False, side="top")
    labelframe_cc = ttk.Labelframe(
        frame_middle,
        text="Want to CC Anyone?",
        name="labelframe_cc",
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
        fg="#FFCAB1",
        bg="#5F634F",
        selectcolor="#000000",
    ).pack(pady=5, expand=False, side="top", ipady=3)
    ttk.Label(
        labelframe_cc,
        text="Add emails here to copy them:",
    ).pack(fill="x", expand=False, side="top")
    view._userinput_CC1 = Text(
        labelframe_cc,
        height=1,
        width=30,
        background=style.alt_bg_color,
        foreground=style.alt_fg_color,
        highlightcolor=style.alt_bg_color,
        selectbackground=style.alt_fg_color,
        selectforeground=style.alt_bg_color,
    )
    view._userinput_CC1.pack(
        pady=2, ipady=4, anchor="n", fill="x", expand=False, side="top"
    )
    ttk.Label(
        labelframe_cc,
        text="2nd Optional list to copy:",
    ).pack(fill="x", expand=False, side="top")
    view._userinput_CC2 = Text(
        labelframe_cc,
        height=1,
        width=30,
        background=style.alt_bg_color,
        foreground=style.alt_fg_color,
        highlightcolor=style.alt_bg_color,
        selectbackground=style.alt_fg_color,
        selectforeground=style.alt_bg_color,
    )
    view._userinput_CC2.pack(ipady=4, anchor="n", fill="x", expand=False, side="top")
    ttk.Button(
        view.tabs.home,
        text="View Each Before Sending!",
        command=lambda: presenter.btn_send_envelopes(autosend=False),
    ).grid(column=1, row=2, sticky="nsew", padx=(10), pady=10)
    # .pack(ipady=20, ipadx=2, pady=10, anchor=S, fill=Y, expand=False)
    right_header_frame = ttk.Frame(view.tabs.home)
    right_header_frame.grid(column=2, row=0, pady=5)
    ttk.Label(
        right_header_frame,
        style="Header.TLabel",
        text="Choose Markets:",
    ).pack(fill="x", expand=True, side="left")

    view.frame_right = ttk.Frame(view.tabs.home)
    view.frame_right.grid(column=2, row=1, pady=(0, 5), sticky="n")
    carriers = [
        "Seawave",
        "Primetime",
        "NewHampshire",
        "AmericanModern",
        "Kemah",
        "Concept",
        "Yachtinsure",
        "Century",
        "Intact",
        "Travelers",
    ]
    for carrier in carriers:
        attr_name = f"_{carrier.lower()}"
        attr = attrgetter(attr_name)(view)
        make_checkbutton(
            parent=view.frame_right,
            text=carrier,
            int_variable=attr,
        )
        # attr used to be view._<carrier_name>
        # we are trying to get the IntVar from view...

    ttk.Button(
        view.tabs.home,
        text="Submit & auto-send all",
        command=presenter.btn_send_envelopes,
    ).grid(column=2, row=2, sticky="nsew", padx=5, pady=10)
