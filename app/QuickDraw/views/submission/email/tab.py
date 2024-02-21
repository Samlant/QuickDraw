from tkinter import ttk, Text
from typing import Protocol

from tkinterdnd2 import DND_FILES

from QuickDraw.views.themes.palettes import Palette
from QuickDraw.views.submission.base.protocols import Presenter


def make_email_widgets(view: Presenter, presenter: Presenter, palette: Palette):
    view.tabs.email.rowconfigure(3, minsize=100, pad=5)
    ### START TITLE ###
    title_frame = ttk.Frame(
        view.tabs.email,
        height=10,
    )
    title_frame.grid(column=0, row=0, sticky="nsew", pady=(0, 5), padx=15)
    ttk.Label(
        title_frame,
        text="Email Settings Page",
        style="Header.TLabel",
    ).pack(
        fill="both",
        expand=True,
        padx=200,
    )
    # END OF TITLE
    # BEGIN CC SETTINGS
    default_cc_lf = ttk.Labelframe(
        view.tabs.email,
        text="""Want to CC specific groups of people by default?""", style="TLabelframe",
    )
    default_cc_lf.grid(column=0, row=1, sticky="nsew", padx=10)
    default_cc_lf.columnconfigure(1, minsize=660)
    ttk.Label(
        master=default_cc_lf,
        text="CC Group 1:", style="TLabel",
    ).grid(
        column=0,
        row=0,
        pady=6,
        padx=(0, 5),
        sticky="ew",
    )
    cc1 = ttk.Entry(
        default_cc_lf,
        textvariable=view._default_cc1,
        name="default_cc1",
        font=1, style="TEntry",
    )
    cc1.grid(
        column=1,
        row=0,
        sticky="ew",
        ipadx=200,
        ipady=3,
        pady=6,
    )
    ttk.Label(
        default_cc_lf,
        text="CC Group 2:",
    ).grid(
        column=0,
        row=1,
        pady=6,
        padx=(0, 5), style="TLabel",
    )
    cc2 = ttk.Entry(
        default_cc_lf,
        textvariable=view._default_cc2,
        name="default_cc2",
        font=1, style="TEntry",
    )
    cc2.grid(
        column=1,
        row=1,
        rowspan=4,
        sticky="ew",
        ipadx=200,
        ipady=3,
        pady=6,
    )
    # END OF CC SETTINGS
    # BEGIN SIGNATURE SETTINGS
    signature_lf = ttk.Labelframe(
        view.tabs.email,
        text="Email Signature Settings", style="TLabelframe",
    )
    signature_lf.grid(column=0, row=2, sticky="nsew", padx=10, pady=(15, 0))
    signature_lf.columnconfigure(2, minsize=170)

    ttk.Label(
        signature_lf,
        text="Your name:", style="TLabel",
    ).grid(row=0, column=0, padx=(0, 5), pady=(5, 0))
    username_entry = ttk.Entry(
        master=signature_lf,
        textvariable=view._username,
        font=1, style="TEntry",
    )
    username_entry.grid(
        row=0,
        column=1,
        columnspan=1,
        padx=(0, 7),
        pady=(5, 0),
        ipadx=30,
        ipady=3,
        sticky="w",
    )
    ttk.Label(
        signature_lf,
        text="Your name's image:", style="TLabel",
    ).grid(row=1, column=0, padx=5, pady=(5, 0))
    view._sig_image_file_path = Text(
        signature_lf,
        name="sig_image_path_file",
        height=2,
        width=45,
        foreground=palette.alt_fg_color,
        background=palette.alt_bg_color,
        highlightcolor=palette.alt_bg_color,
        selectbackground=palette.alt_fg_color,
        selectforeground=palette.alt_bg_color,
    )
    view._sig_image_file_path.grid(
        row=1,
        column=1,
        columnspan=2,
        pady=(5, 1),
        padx=(0, 1),
        sticky="ew",
    )
    view._sig_image_file_path.drop_target_register(DND_FILES)
    view._sig_image_file_path.dnd_bind(
        "<<Drop>>",
        lambda: presenter.process_file_path(path_purpose="sig_image_file_path"),
    )
    view.sig_image_btn = ttk.Button(
        signature_lf,
        command=lambda: presenter.browse_file_path(path_purpose="sig_image_file_path"),
        text="Browse",
        style="TButton",
    )
    view.sig_image_btn.grid(
        row=1,
        column=3,
        ipady=8,
        pady=(2, 1),
        padx=5,
    )
    ttk.Label(
        signature_lf,
        text="Office Phone #:", style="TLabel",
    ).grid(row=2, column=0, padx=(0, 5), pady=(5, 0))
    office_ph_entry = ttk.Entry(
        master=signature_lf,
        textvariable=view._office_phone,
        font=1, style="TEntry",
    )
    office_ph_entry.grid(
        row=2,
        column=1,
        columnspan=2,
        padx=(0, 7),
        pady=(5, 0),
        ipadx=30,
        ipady=3,
        sticky="w",
    )
    ttk.Label(
        signature_lf,
        text="Office Fax #:", style="TLabel",
    ).grid(row=3, column=0, padx=(0, 5), pady=(5, 0))
    office_fax_entry = ttk.Entry(
        master=signature_lf,
        textvariable=view._office_fax,
        font=1, style="TEntry",
    )
    office_fax_entry.grid(
        row=3,
        column=1,
        columnspan=2,
        padx=(0, 7),
        pady=(5, 0),
        ipadx=30,
        ipady=3,
        sticky="w",
    )
    ttk.Label(
        signature_lf,
        text="Office Street:", style="TLabel",
    ).grid(row=4, column=0, padx=(0, 5), pady=(5, 0))
    office_st_entry = ttk.Entry(
        master=signature_lf,
        textvariable=view._office_street,
        font=1, style="TEntry",
    )
    office_st_entry.grid(
        row=4,
        column=1,
        columnspan=2,
        padx=(0, 7),
        pady=(5, 0),
        ipadx=30,
        ipady=3,
        sticky="w",
    )
    ttk.Label(
        signature_lf,
        text="Office City, State, Zip:", style="TLabel",
    ).grid(row=5, column=0, padx=(0, 5), pady=(5, 0))
    office_city_st_zip_entry = ttk.Entry(
        master=signature_lf,
        textvariable=view._office_city_st_zip,
        font=1, style="TEntry",
    )
    office_city_st_zip_entry.grid(
        row=5,
        column=1,
        columnspan=2,
        padx=(0, 7),
        pady=(5, 0),
        ipadx=30,
        ipady=3,
        sticky="w",
    )
    ### BUTTONS FRAME ###
    buttons_frame = ttk.Frame(
        view.tabs.email, style="TFrame",
    )
    buttons_frame.grid(column=0, row=3, sticky="nsew", padx=10, pady=5)
    ttk.Button(
        master=buttons_frame,
        text="Revert Back",
        command=lambda: presenter.btn_revert_view_tab("email"), style="TButton",
    ).pack(
        fill="both",
        expand=True,
        side="left",
        padx=10,
        pady=5,
    )
    ttk.Button(
        master=buttons_frame,
        text="Save Settings",
        command=lambda: presenter.btn_save_view_tab("email"), style="TButton",
    ).pack(
        fill="both",
        expand=True,
        side="left",
        padx=10,
        pady=5,
    )
