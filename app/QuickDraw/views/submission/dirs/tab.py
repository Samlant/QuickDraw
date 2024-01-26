from tkinter import ttk
from typing import Protocol

from QuickDraw.views.themes.palettes import palette
from QuickDraw.views.submission import base


class Presenter(Protocol):
    ...


def make_dirs_widgets(view: base.Submission, presenter: Presenter, style=palette):
    ### Start Watch Dir Settings ###
    view.tabs.dirs.rowconfigure(3, minsize=100, pad=5)
    ### START TITLE ###
    title_frame = ttk.Frame(
        view.tabs.dirs,
    )
    title_frame.grid(column=0, row=0, sticky="nsew")
    ttk.Label(title_frame, text="Folder Settings Page", style="Header.TLabel").pack(
        fill="both",
        expand=True,
        padx=200,
    )
    # END OF TITLE
    # START CONTENT
    watch_dir_lf = ttk.Labelframe(
        view.tabs.dirs,
        text="Watch Folder Options",
    )
    watch_dir_lf.grid(column=0, row=1, sticky="nsew", padx=10, pady=(5, 0))
    ttk.Label(
        watch_dir_lf,
        text="Current Watch Folder:",
    ).grid(column=0, row=0, ipady=3, pady=6)
    view.watch_dir_entry = ttk.Entry(
        watch_dir_lf,
        textvariable=view._watch_dir,
    )
    view.watch_dir_entry.grid(column=1, row=0, padx=5, pady=6, ipady=3, ipadx=149)
    watch_dir_btn = ttk.Button(
        watch_dir_lf,
        command=view._browse_watch_dir,
        text="Browse to change",
    )
    watch_dir_btn.grid(column=2, row=0, padx=5, pady=6, ipady=3, ipadx=4)
    ttk.Label(
        watch_dir_lf,
        text="New Biz Client Folder:",
    ).grid(column=0, row=1, ipady=3, padx=0)
    view.new_biz_dir_entry = ttk.Entry(
        watch_dir_lf,
        textvariable=view._new_biz_dir,
    )
    view.new_biz_dir_entry.grid(column=1, row=1, padx=5, pady=0, ipady=3, ipadx=149)
    new_biz_dir_btn = ttk.Button(
        watch_dir_lf,
        command=view._browse_new_biz_dir,
        text="Browse to change",
    )
    new_biz_dir_btn.grid(column=2, row=1, padx=5, pady=0, ipady=3, ipadx=4)
    ttk.Label(
        watch_dir_lf,
        text="Renewals Client Folder:",
    ).grid(column=0, row=2, ipady=3, padx=0)
    view.renewals_dir_entry = ttk.Entry(
        watch_dir_lf,
        textvariable=view._renewals_dir,
    )
    view.renewals_dir_entry.grid(column=1, row=2, padx=5, pady=6, ipady=3, ipadx=149)
    renewals_dir_btn = ttk.Button(
        watch_dir_lf,
        command=view._browse_renewals_dir,
        text="Browse to change",
    )
    renewals_dir_btn.grid(column=2, row=2, padx=5, pady=6, ipady=3, ipadx=4)
    custom_dir_lf = ttk.Labelframe(
        view.tabs.dirs,
        text="Create additional folders when a client folder is created",
    )
    ### START Custom Dir Structure Label Frame ###
    custom_dir_lf.grid(column=0, row=2, sticky="nsew", pady=(5, 0), padx=10)
    ### LEFT SECTION ###
    left_custom_dir_frame = ttk.Frame(custom_dir_lf)
    left_custom_dir_frame.pack(
        fill="x",
        expand=False,
        side="left",
    )
    ### Treeview Section ###
    view.tree_dir = ttk.Treeview(
        left_custom_dir_frame,
        columns=1,
    )
    view.tree_dir.column(
        "#0",
        width=120,
        stretch=False,
    )
    view.tree_dir.column(
        "#1",
        width=350,
        stretch=False,
    )
    view.tree_dir.heading("#0", text="Folder Structure", anchor="w")
    view.tree_dir.heading("#1", text="Folder Name", anchor="w")
    # view.tree_dir.pack(fill="both", expand=True, side="left")
    view.tree_dir.grid(column=0, row=0, pady=(5, 0))
    ### END OF TREEVIEW SECTION ###
    ### END OF LEFT SECTION ###
    ### RIGHT SECTION ###
    right_custom_dir_frame = ttk.Frame(custom_dir_lf)
    right_custom_dir_frame.pack(
        fill="both",
        expand=True,
        side="left",
        pady=5,
        padx=7,
    )
    ### TOP SECTION ###
    top_custom_dir_frame = ttk.Frame(
        right_custom_dir_frame,
    )
    top_custom_dir_frame.pack(
        fill="both",
        expand=True,
        side="top",
    )
    # top_custom_dir_frame.grid(column=0, row=0, padx=(10, 0), pady=(5,0), columnspan=2)
    ### Top Left ###
    top_left_custom_dir_frame = ttk.Frame(
        top_custom_dir_frame,
    )
    top_left_custom_dir_frame.pack(
        fill="both",
        expand=True,
        side="left",
        anchor="s",
    )
    ttk.Label(
        top_left_custom_dir_frame,
        text="Add a Parent folder:",
        justify="left",
    ).pack(
        fill="both",
        expand=True,
        side="top",
    )
    view.top_left_custom_dir_entry = ttk.Entry(
        top_left_custom_dir_frame,
        textvariable=view._custom_parent_dir,
    )
    view.top_left_custom_dir_entry.pack(
        fill="x", expand=True, side="top", ipady=3, anchor="n"
    )
    ### Top Right ###
    top_right_custom_dir_frame = ttk.Frame(
        top_custom_dir_frame,
    )
    top_right_custom_dir_frame.pack(
        fill="both",
        expand=True,
        side="left",
    )
    custom_parent_dir_btn = ttk.Button(
        top_right_custom_dir_frame,
        command=view._add_custom_parent_dir,
        text="Add",
    )
    custom_parent_dir_btn.pack(
        fill="both", expand=True, side="left", pady=6, padx=(5, 0)
    )
    ### MIDDLE SECTION ###
    middle_custom_dir_frame = ttk.Frame(right_custom_dir_frame)
    middle_custom_dir_frame.pack(
        fill="both",
        expand=True,
        side="top",
        pady=15,
    )
    # middle_custom_dir_frame.grid(column=0, row=1, padx=(10, 0), pady=(20,20), columnspan=2)

    ### Middle Left ###
    middle_left_custom_dir_frame = ttk.Frame(middle_custom_dir_frame)
    middle_left_custom_dir_frame.pack(
        fill="both",
        expand=True,
        side="left",
    )
    ttk.Label(
        middle_left_custom_dir_frame,
        text="Add a sub-folder:",
        font=("helvetica", 10, "normal"),
        justify="left",
    ).pack(fill="both", expand=True, side="top", anchor="s")
    view.middle_left_custom_dir_entry = ttk.Entry(
        middle_left_custom_dir_frame,
        textvariable=view._custom_sub_dir,
    )
    view.middle_left_custom_dir_entry.pack(
        fill="x", expand=True, side="top", ipady=3, anchor="n"
    )
    ### Middle Right ###
    middle_right_custom_dir_frame = ttk.Frame(middle_custom_dir_frame)
    middle_right_custom_dir_frame.pack(
        fill="both",
        expand=True,
        side="left",
    )
    custom_sub_dir_btn = ttk.Button(
        middle_right_custom_dir_frame,
        command=view._add_custom_sub_dir,
        text="Add",
    )
    custom_sub_dir_btn.pack(fill="both", expand=True, side="left", pady=6, padx=(5, 0))
    ### BOTTOM SECTION ###
    bottom_custom_dir_frame = ttk.Frame(right_custom_dir_frame)
    bottom_custom_dir_frame.pack(
        fill="both",
        expand=True,
        side="top",
    )
    # bottom_custom_dir_frame.grid(column=0, row=2, padx=(10, 0), pady=(0,0), columnspan=2)

    custom_rm_dir_btn = ttk.Button(
        bottom_custom_dir_frame,
        command=view._rm_custom_dir,
        text="Remove selected folder",
    )
    custom_rm_dir_btn.pack(
        fill="both",
        expand=True,
        side="top",
    )
    ### END OF CUSTOM DIR STRUCTURE SECTION ###
    ### BUTTONS FRAME ###
    buttons_box = ttk.Frame(
        view.tabs.dirs,
    )
    buttons_box.grid(column=0, row=3, sticky="nsew", pady=(10, 0), padx=10)
    ttk.Button(
        master=buttons_box,
        text="Revert Back",
        command=presenter.btn_revert_folder_settings,
    ).pack(
        fill="both",
        expand=True,
        side="left",
        padx=(0, 5),
    )
    ttk.Button(
        master=buttons_box,
        text="Save Settings",
        command=presenter.btn_save_folder_settings,
    ).pack(
        fill="both",
        expand=True,
        side="left",
        padx=(5, 0),
    )