from tkinter import ttk, Text
from typing import Protocol

from tkinterdnd2 import DND_FILES

from QuickDraw.views.themes.palettes import Palette
from QuickDraw.views.submission.base.protocols import Presenter


def make_email_widgets(view: Presenter, presenter: Presenter, style: Palette):
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
        text="""Want to CC specific groups of people by default?""",
    )
    default_cc_lf.grid(column=0, row=1, sticky="nsew", padx=10)
    default_cc_lf.columnconfigure(1, minsize=660)
    ttk.Label(
        master=default_cc_lf,
        text="CC Group 1:",
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
        font=1,
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
        padx=(0, 5),
    )
    cc2 = ttk.Entry(
        default_cc_lf,
        textvariable=view._default_cc2,
        name="default_cc2",
        font=1,
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
        text="Email Signature Settings",
    )
    signature_lf.grid(column=0, row=2, sticky="nsew", padx=10, pady=(15, 0))
    signature_lf.columnconfigure(2, minsize=170)

    ttk.Label(
        signature_lf,
        text="Your name:",
    ).grid(row=0, column=0, padx=(0, 5), pady=(5, 0))
    username_entry = ttk.Entry(
        master=signature_lf,
        textvariable=view._username,
        font=1,
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
    ttk.Frame(signature_lf).grid(row=0, column=2, columnspan=3)
    ttk.Label(
        signature_lf,
        text="Name image:",
    ).grid(row=1, column=0, padx=5, pady=(5, 0))
    view.sig_image_file_path = Text(
        signature_lf,
        name="sig_image_path_file",
        height=2,
        width=45,
        foreground=style.alt_fg_color,
        background=style.alt_bg_color,
        highlightcolor=style.alt_bg_color,
        selectbackground=style.alt_fg_color,
        selectforeground=style.alt_bg_color,
    )
    view.sig_image_file_path.grid(
        row=1,
        column=1,
        columnspan=2,
        pady=(5, 1),
        padx=(0, 1),
        sticky="ew",
    )
    view.sig_image_file_path.drop_target_register(DND_FILES)
    view.sig_image_file_path.dnd_bind(
        "<<Drop>>",
        presenter.process_signature_image_path,
    )
    view.sig_image_btn = ttk.Button(
        signature_lf,
        command=view._browse_name_img,
        text="Browse",
    )
    view.sig_image_btn.grid(
        row=1,
        column=3,
        ipady=8,
        pady=(2, 1),
        padx=5,
    )
    view.sig_upload_btn = ttk.Button(
        signature_lf,
        command=view._upload_img_btn,
        text="Upload",
    )
    view.sig_upload_btn.grid(
        row=1,
        column=4,
        ipady=8,
        pady=(2, 1),
        padx=5,
    )
    ### BUTTONS FRAME ###
    buttons_frame = ttk.Frame(
        view.tabs.email,
    )
    buttons_frame.grid(column=0, row=3, sticky="nsew", padx=10, pady=5)
    ttk.Button(
        master=buttons_frame,
        text="Revert Back",
        command=lambda: presenter.btn_revert_view_tab("email"),
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
        command=lambda: presenter.btn_save_view_tab("email"),
    ).pack(
        fill="both",
        expand=True,
        side="left",
        padx=10,
        pady=5,
    )
