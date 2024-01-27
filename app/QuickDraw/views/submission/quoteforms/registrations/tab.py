from tkinter import ttk
from typing import Protocol

from QuickDraw.views.submission import base
from QuickDraw.views.submission.quoteforms.registrations.current import (
    CurrentRegistrations,
)
from QuickDraw.views.submission.quoteforms.registrations.new import NewRegistrations


class Presenter(Protocol):
    def btn_revert_registration_settings() -> None:
        ...

    def btn_save_registration_settings() -> None:
        ...


def make_quoteform_widgets(view: base.MainWindow, presenter: Presenter):
    ### START TITLE ###
    title_frame = ttk.Frame(
        view.tabs.quoteforms,
    )
    title_frame.grid(column=0, row=0, sticky="nsew")
    ttk.Label(title_frame, text="Quoteform Registrations", style="Header.TLabel").pack(
        fill="both",
        expand=True,
        padx=200,
    )
    # END OF TITLE
    # START CONTENT
    ### START Current Registrations TreeView ###
    current_reg_lf = ttk.Labelframe(
        view.tabs.quoteforms,
        text="Current Registrations",
    )
    current_reg_lf.grid(column=0, row=1, sticky="nsew", pady=(5, 0), padx=10)
    current_reg_lf.columnconfigure(0, minsize=500)
    current_reg_lf.rowconfigure(0, minsize=155)
    left_registration_frame = ttk.Frame(current_reg_lf)
    left_registration_frame.grid(row=0, column=0)

    ### Treeview Section ###
    view.reg_tv = CurrentRegistrations(left_registration_frame)
    view.reg_tv.grid(columnspan=2, column=0, row=0, pady=5, padx=(5, 0))
    right_registration_frame = ttk.Frame(current_reg_lf)
    right_registration_frame.grid(row=0, column=1)
    rm_registration_btn = ttk.Button(
        right_registration_frame,
        command=view.reg_tv.remove_registration,
        text="Remove",
    )
    rm_registration_btn.pack(
        fill="both",
        expand=False,
        side="left",
        padx=5,
        ipady=10,
    )
    ### END Current Registrations TreeView ###
    ##########################################
    ### START New Registration LF ###
    register_lf = NewRegistrations(
        view,
        presenter,
        view.tabs.quoteforms,
        text="Register a new Quoteform here",
    )
    register_lf.grid(column=0, row=2, sticky="nsew", padx=10, pady=(10, 0))
    ### END New Registration LF ###
    ###############################
    ### BUTTONS FRAME ###
    buttons_box = ttk.Frame(
        view.tabs.quoteforms,
    )
    buttons_box.grid(column=0, row=3, sticky="nsew", pady=(5, 0), padx=10)
    ttk.Button(
        master=buttons_box,
        text="Revert Back",
        command=presenter.btn_revert_registration_settings,
    ).pack(
        fill="both",
        expand=True,
        side="left",
        padx=(0, 5),
    )
    ttk.Button(
        master=buttons_box,
        text="Save Settings",
        command=presenter.btn_save_registration_settings,
    ).pack(
        fill="both",
        expand=True,
        side="left",
        padx=(5, 0),
    )
