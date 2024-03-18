from tkinter import ttk, Text

from QuickDraw.views.submission.base.window import Window
from QuickDraw.views.submission.helper import create_dropdown
from QuickDraw.views.themes.palettes import Palette
from QuickDraw.views.submission.base.protocols import Presenter


def make_templates_widgets(
    view: Window, presenter: Presenter, palette: Palette
):
    view.tabs.templates.columnconfigure(0, minsize=740, pad=5)
    view.tabs.templates.rowconfigure(2, minsize=100, pad=5)

    title_frame = ttk.Frame(
        view.tabs.templates,
        height=5,
        style="TFrame",
    )
    title_frame.grid(column=0, row=0, pady=(0, 5), padx=10, sticky="n")
    ttk.Label(
        title_frame,
        text="Customize Email Templates for Each Underwriter",
        style="Header.TLabel",
    ).pack(
        fill="x",
        expand=True,
        side="top",
        anchor="n",
    )
    customize_msg_lf = ttk.Labelframe(
        view.tabs.templates,
        text="Don't forget to save",
        style="TLabelframe",
    )
    customize_msg_lf.grid(column=0, row=1, padx=10, sticky="nsew")

    template_select_frame = ttk.Frame(
        customize_msg_lf,
        style="TFrame",
    )
    template_select_frame.grid(
        column=0, row=0, padx=15, pady=10, sticky="nsew", columnspan=2
    )
    view.dropdown_menu = create_dropdown(
        view=view,
        parent=template_select_frame,
        presenter=presenter,
        palette=palette,
    )
    view.dropdown_menu.pack(padx=15, ipady=5, fill="x", expand=True)
    view._selected_template.trace_add(
        "write",
        presenter.on_change_template,
    )

    ttk.Label(
        customize_msg_lf,
        text="Submission Address:",
    ).grid(column=0, row=1)

    view.address_entry = ttk.Entry(
        master=customize_msg_lf,
        name="address",
        textvariable=view._address,
        width=89,
        style="TEntry",
        # validate="focusout",
        # validatecommand=presenter.on_focus_out,
    )
    view.address_entry.grid(
        column=1,
        row=1,
        sticky="ew",
        ipady=5,
        pady=5,
    )
    view.address_entry.bind(
        "<FocusOut>",
        presenter.on_focus_out,
    )

    ttk.Label(
        customize_msg_lf,
        text="Greeting:",
        style="TLabel",
    ).grid(column=0, row=2)

    view.greet_entry = ttk.Entry(
        master=customize_msg_lf,
        name="greeting",
        textvariable=view._greeting,
        width=89,
        style="TEntry",
    )
    view.greet_entry.grid(
        column=1,
        row=2,
        pady=5,
        ipady=5,
        sticky="ew",
    )
    view.greet_entry.bind(
        "<FocusOut>",
        presenter.on_focus_out,
    )

    ttk.Label(
        customize_msg_lf,
        text="Body of the email:",
        style="TLabel",
    ).grid(column=0, row=3)

    view._body = Text(
        customize_msg_lf,
        name="body",
        width=73,
        height=5,
        wrap="word",
        foreground=palette.alt_fg_color,
        background=palette.alt_bg_color,
        highlightcolor=palette.alt_bg_color,
        selectbackground=palette.alt_fg_color,
        selectforeground=palette.alt_bg_color,
    )
    view._body.grid(
        column=1,
        row=3,
        sticky="w",
        pady=5,
    )
    view._body.bind(
        "<FocusOut>",
        presenter.on_focus_out,
    )

    ttk.Label(
        customize_msg_lf,
        text="Outro:",
        style="TLabel",
    ).grid(column=0, row=4)

    view.outro_entry = ttk.Entry(
        customize_msg_lf,
        name="outro",
        textvariable=view._outro,
        width=89,
        style="TEntry",
    )
    view.outro_entry.grid(
        column=1,
        row=4,
        sticky="ew",
        pady=5,
        ipady=5,
    )
    view.outro_entry.bind("<FocusOut>", presenter.on_focus_out)

    ttk.Label(
        customize_msg_lf,
        text="Salutation:",
        style="TLabel",
    ).grid(column=0, row=5)

    view.sal_entry = ttk.Entry(
        customize_msg_lf,
        name="salutation",
        textvariable=view._salutation,
        width=89,
        style="TEntry",
    )
    view.sal_entry.grid(
        column=1,
        row=5,
        sticky="ew",
        pady=5,
        ipady=5,
    )
    view.sal_entry.bind("<FocusOut>", presenter.on_focus_out)

    buttons_frame = ttk.Frame(
        view.tabs.templates,
        style="TFrame",
    )
    buttons_frame.grid(column=0, row=2, padx=10, sticky="nsew")
    ttk.Button(
        buttons_frame,
        name="btnResetTemplate",
        text="Revert Back",
        command=lambda: presenter.btn_revert_view_tab("template"),
        style="TButton",
    ).pack(
        padx=10,
        pady=10,
        fill="both",
        expand=True,
        anchor="n",
        side="left",
    )
    ttk.Button(
        buttons_frame,
        name="btnViewTemplate",
        text="View Current Example",
        width=20,
        command=lambda: presenter.btn_process_envelopes(auto_send=False),
        style="TButton",
    ).pack(
        padx=4,
        pady=10,
        fill="both",
        expand=True,
        anchor="n",
        side="left",
    )
    ttk.Button(
        buttons_frame,
        name="btnSaveTemplate",
        text="Save",
        width=20,
        command=lambda: presenter.btn_save_view_tab("template"),
        style="TButton",
    ).pack(
        padx=10,
        pady=10,
        fill="both",
        expand=True,
        anchor="n",
        side="left",
    )
