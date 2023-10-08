import tkinter
from typing import Protocol
from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.ttk import Notebook, Style, Treeview

from tkinter import *
from tkinterdnd2 import DND_FILES, TkinterDnD

from view.styling import BlueRose, create_style


class Presenter(Protocol):
    """This enables us to call funtions from the Presenter
    class, either to send/retrieve data.
    """

    def btn_send_envelopes(self, autosend: bool) -> None:
        ...

    def btn_clear_attachments(self) -> None:
        ...

    def btn_reset_template(self) -> None:
        ...

    def btn_view_template(self) -> None:
        ...

    def btn_save_template(self) -> None:
        ...

    def btn_save_email_settings(self) -> None:
        ...

    def btn_save_folder_settings(self) -> None:
        ...

    def btn_revert_email_settings(self, event) -> None:
        ...

    def btn_revert_folder_settings(self, event) -> None:
        ...

    def set_dropdown_options(self) -> list:
        ...

    def process_quoteform_path(self, drag_n_drop_event) -> None:
        ...

    def process_attachments_path(self, drag_n_drop_event) -> None:
        ...

    def process_signature_image_path(self, drag_n_drop_event) -> None:
        ...

    def _save_signature_image_path(self, path: str) -> None:
        ...

    def save_extra_notes(self, notes: str) -> None:
        ...

    def on_change_template(self, *args, **kwargs) -> None:
        ...

    def on_focus_out(self, field_name: str, current_text: str) -> bool:
        ...


BR = BlueRose()


class Submission:
    def __init__(self, positive_value, negative_value, icon_src: str) -> None:
        self._yes = positive_value
        self._no = negative_value
        self.icon = icon_src

    def assign_private_string_bool_vars(self) -> None:
        """Assigns tkinter-specific attributes so that the getters /
        setters work and other modules do not need to need tkinter.
        """
        # main_tab vars
        self._use_CC_defaults = BooleanVar(name="use_CC_defaults")
        self._seawave = StringVar(name="Seawave", value=self._no)
        self._primetime = StringVar(name="Prime Time", value=self._no)
        self._newhampshire = StringVar(name="New Hampshire", value=self._no)
        self._americanmodern = StringVar(name="American Modern", value=self._no)
        self._kemah = StringVar(name="Kemah Marine", value=self._no)
        self._concept = StringVar(name="Concept Special Risks", value=self._no)
        self._yachtinsure = StringVar(name="Yachtinsure", value=self._no)
        self._century = StringVar(name="Century", value=self._no)
        self._intact = StringVar(name="Intact", value=self._no)
        self._travelers = StringVar(name="Travelers", value=self._no)
        # customize_tab vars
        self._dropdown_menu_var = StringVar(
            value="Select Market(s)"
            # name='Current Selection'
        )
        self._address = StringVar(name="address", value="")
        self._greeting = StringVar(name="greeting", value="")
        self._salutation = StringVar(name="salutation", value="")
        # settings_tab vars
        self._username = StringVar(name="username", value="")
        self._default_cc1 = StringVar(name="default_cc1", value="")
        self._default_cc2 = StringVar(name="default_cc2", value="")
        self._watch_dir = StringVar(name="watch_dir", value="")
        self._new_biz_dir = StringVar(name="new_biz_dir", value="")
        self._renewals_dir = StringVar(name="renewals_dir", value="")
        self._custom_parent_dir = StringVar(name="custom_parent_dir", value="")
        self._custom_sub_dir = StringVar(name="custom_sub_dir", value="")

    # main_tab: getters/setters
    @property
    def extra_notes(self) -> str:
        return self._extra_notes_text.get("1.0", "end-1c")

    @extra_notes.deleter
    def extra_notes(self):
        self._extra_notes_text.delete("1.0")

    @property
    def userinput_CC1(self) -> str:
        return self._userinput_CC1.get("1.0", "end-1c")

    @property
    def userinput_CC2(self) -> str:
        return self._userinput_CC2.get("1.0", "end-1c")

    @property
    def use_default_cc_addresses(self) -> bool:
        return self._use_CC_defaults.get()

    @use_default_cc_addresses.setter
    def use_default_cc_addresses(self, usage: bool) -> None:
        self._use_CC_defaults.set(usage)

    @property
    def sw(self) -> str:
        return self._seawave.get()

    @property
    def pt(self) -> str:
        return self._primetime.get()

    @property
    def nh(self) -> str:
        return self._newhampshire.get()

    @property
    def am(self) -> str:
        return self._americanmodern.get()

    @property
    def km(self) -> str:
        return self._kemah.get()

    @property
    def cp(self) -> str:
        return self._concept.get()

    @property
    def yi(self) -> str:
        return self._yachtinsure.get()

    @property
    def ce(self) -> str:
        return self._century.get()

    @property
    def In(self) -> str:
        return self._intact.get()

    @property
    def tv(self) -> str:
        return self._travelers.get()

    @property
    def quoteform(self):
        return self.quoteform_path_box.get("1.0", "end-1c")

    @quoteform.setter
    def quoteform(self, new_attachment: str):
        self.quoteform_path_box.insert("1.0", new_attachment)

    @quoteform.deleter
    def quoteform(self):
        self.quoteform_path_box.delete("1.0", END)

    @property
    def extra_attachments(self):
        return self.extra_attachments_path_box.get("1.0", "end-1c")

    @extra_attachments.setter
    def extra_attachments(self, new_attachment: str):
        self.extra_attachments_path_box.insert("1.0", new_attachment + "\n")

    @extra_attachments.deleter
    def extra_attachments(self):
        self.extra_attachments_path_box.delete("1.0", END)

    # customize_tab: getters/setters
    @property
    def selected_template(self) -> str:
        return self._dropdown_menu_var.get()

    @property
    def address(self) -> str:
        return self._address.get()

    @address.setter
    def address(self, new_address: str) -> None:
        self._address.set(new_address)

    @address.deleter
    def address(self) -> None:
        self._address.set("")

    @property
    def greeting(self) -> str:
        return self._greeting.get()

    @greeting.setter
    def greeting(self, new_greeting: str) -> None:
        self._greeting.set(new_greeting)

    @greeting.deleter
    def greeting(self) -> None:
        self._greeting.set("")

    @property
    def body(self) -> str:
        return self._body_text.get("1.0", "end-1c")

    @body.setter
    def body(self, new_body: str) -> None:
        self._body_text.insert("1.0", new_body)

    @body.deleter
    def body(self) -> None:
        self._body_text.delete("1.0", "end-1c")

    @property
    def salutation(self) -> str:
        return self._salutation.get()

    @salutation.setter
    def salutation(self, new_salutation: str) -> None:
        self._salutation.set(new_salutation)

    @salutation.deleter
    def salutation(self) -> None:
        self._salutation.set("")

    # Email settings_tab: getters/setters
    @property
    def default_cc1(self) -> str:
        return self._default_cc1.get()

    @default_cc1.setter
    def default_cc1(self, new_default_cc: str) -> None:
        self._default_cc1.set(new_default_cc)

    @default_cc1.deleter
    def default_cc1(self) -> None:
        self._default_cc1.set("")

    @property
    def default_cc2(self) -> str:
        return self._default_cc2.get()

    @default_cc2.setter
    def default_cc2(self, new_default_cc: str) -> None:
        self._default_cc2.set(new_default_cc)

    @default_cc2.deleter
    def default_cc2(self) -> None:
        self._default_cc2.set("")

    @property
    def username(self) -> str:
        return self._username.get()

    @username.setter
    def username(self, new_username: str):
        self._username.set(new_username)

    @username.deleter
    def username(self) -> None:
        self._username.set("")

    @property
    def sig_image_file(self) -> str:
        return self.sig_image_path_box.get("1.0", "end-1c")

    @sig_image_file.setter
    def sig_image_file(self, new_image_file: str):
        self.sig_image_path_box.delete("1.0", END)
        self.sig_image_path_box.insert("1.0", new_image_file)

    @sig_image_file.deleter
    def sig_image_file(self):
        self.sig_image_path_box.delete("1.0", END)

    # Folder Settings Tab: getters/setters
    @property
    def watch_dir(self) -> str:
        return self._watch_dir.get()

    @watch_dir.setter
    def watch_dir(self, new_watch_dir: str):
        self._watch_dir.set(new_watch_dir)

    @watch_dir.deleter
    def watch_dir(self):
        self._watch_dir.set("")

    @property
    def new_biz_dir(self) -> str:
        return self._new_biz_dir.get()

    @new_biz_dir.setter
    def new_biz_dir(self, new_new_biz_dir: str):
        self._new_biz_dir.set(new_new_biz_dir)

    @new_biz_dir.deleter
    def new_biz_dir(self):
        self._new_biz_dir.set("")

    @property
    def renewals_dir(self) -> str:
        return self._renewals_dir.get()

    @renewals_dir.setter
    def renewals_dir(self, new_renewals_dir: str):
        self._renewals_dir.set(new_renewals_dir)

    @renewals_dir.deleter
    def renewals_dir(self):
        self._renewals_dir.set("")

    @property
    def custom_parent_dir(self) -> str:
        return self._custom_parent_dir.get()

    @custom_parent_dir.setter
    def custom_parent_dir(self, new_custom_parent_dir: str):
        self._custom_parent_dir.set(new_custom_parent_dir)

    @custom_parent_dir.deleter
    def custom_parent_dir(self):
        self._custom_parent_dir.set("")

    @property
    def custom_sub_dir(self) -> str:
        return self._custom_sub_dir.get()

    @custom_sub_dir.setter
    def custom_sub_dir(self, new__custom_sub_dir: str):
        self._custom_sub_dir.set(new__custom_sub_dir)

    @custom_sub_dir.deleter
    def custom_sub_dir(self):
        self._custom_sub_dir.set("")

    ### END of Getters/Setters ###

    def create_UI_obj(self, presenter: Presenter):
        """This creates the GUI root,  along with the main
        functions to create the widgets.
        """
        self.root = TkinterDnD.Tk()
        self.assign_private_string_bool_vars()
        self.assign_window_traits()
        self.style = create_style(self.root)
        self.create_notebook()
        self.create_tabs()
        self.create_main_tab_widgets(presenter)
        self.create_customize_tab_widgets(presenter)
        self.create_email_settings_tab_widgets(presenter)
        self.create_folder_settings_tab_widgets(presenter)

    def assign_window_traits(self):
        self.root.geometry("760x600")
        # self.root.configure(background="red")
        self.root.attributes("-topmost", True)
        self.root.title("QuickDraw")
        self.root.attributes("-alpha", 0.95)
        self.root.iconbitmap(self.icon)

    def create_notebook(self):
        self.root.tabControl = Notebook(master=self.root)
        self.root.tabControl.pack(fill="both", pady=0, expand=True)

    def create_tabs(self):
        self.home = ttk.Frame(self.root.tabControl)
        self.template_customization = ttk.Frame(self.root.tabControl)
        self.email_settings = ttk.Frame(self.root.tabControl)
        self.folder_settings = ttk.Frame(self.root.tabControl)
        self.root.tabControl.add(self.home, text="Home - Outbox")
        self.root.tabControl.add(self.template_customization, text="Email Templates")
        self.root.tabControl.add(self.email_settings, text="Email Settings")
        self.root.tabControl.add(self.folder_settings, text="Folder Settings")

    def create_main_tab_widgets(self, presenter: Presenter):
        self.home.rowconfigure(2, minsize=100, pad=5)
        self.home.columnconfigure(0, pad=5)
        self.home.columnconfigure(1, pad=5)
        self.home.columnconfigure(2, pad=5)
        left_header_frame = ttk.Frame(self.home)
        left_header_frame.grid(column=0, row=0, pady=(0, 5))
        ttk.Label(
            left_header_frame,
            text="Get Client Information",
            style="Header.TLabel",
        ).pack(fill=X, expand=True, side="left")
        frame_left = ttk.Frame(self.home)
        frame_left.grid(column=0, row=1, sticky=N, pady=(5, 0), padx=(5, 0))
        labelframe_dd_qf = ttk.Labelframe(
            frame_left,
            text="Dag-N-Drop Quoteform Below",
            name="labelframe_dd_qf",
        )
        labelframe_dd_qf.pack(fill=NONE, expand=False, side="top")
        self.create_quoteform_path_box(labelframe_dd_qf, presenter)
        ttk.Button(
            labelframe_dd_qf,
            text="Browse",
            command=self._browse_qf_path,
        ).pack(fill=None, pady=5, expand=False, side="top")
        labelframe_dd_ea = ttk.Labelframe(
            frame_left,
            text="Dag-N-Drop Extra Files Below",
            name="labelframe_dd_ea",
        )
        labelframe_dd_ea.pack(fill=None, expand=False, side="top", pady=(15, 0))
        self.create_extra_attachments_path_box(labelframe_dd_ea, presenter)
        ttk.Button(
            labelframe_dd_ea,
            text="Browse",
            command=self._browse_extra_file_path,
        ).pack(fill=None, pady=5, expand=False, side="top")
        ttk.Button(
            self.home,
            text="Clear attachments",
            command=presenter.btn_clear_attachments,
        ).grid(column=0, row=2, sticky=NSEW, padx=5, pady=10)

        middle_header_frame = ttk.Frame(self.home)
        middle_header_frame.grid(column=1, row=0, pady=(0, 5))
        ttk.Label(
            middle_header_frame,
            style="Header.TLabel",
            text="Extra Notes & CC",
        ).pack(fill=X, expand=True, side="left")
        frame_middle = ttk.Frame(self.home)
        frame_middle.grid(column=1, row=1, sticky=N)
        labelframe_main1 = ttk.Labelframe(
            frame_middle,
            text="Want to add any notes?",
        )
        labelframe_main1.pack(fill=BOTH, expand=True, side="top")
        self._extra_notes_text = Text(
            labelframe_main1,
            height=7,
            width=10,
            name="raw_extra_notes",
            background=BR.alt_bg_color,
            foreground=BR.alt_fg_color,
            highlightcolor=BR.alt_bg_color,
            selectbackground=BR.alt_fg_color,
            selectforeground=BR.alt_bg_color,
        )
        self._extra_notes_text.focus_set()
        self._extra_notes_text.pack(fill=BOTH, expand=FALSE, side="top")
        labelframe_cc = ttk.Labelframe(
            frame_middle,
            text="Want to CC Anyone?",
            name="labelframe_cc",
        )
        labelframe_cc.pack(fill=X, expand=False, side="top", pady=(15, 0))
        Checkbutton(
            labelframe_cc,
            text="Include default CC addresses",
            variable=self._use_CC_defaults,
            name="cc_def_check",
            onvalue=True,
            offvalue=False,
            relief="raised",
            justify=CENTER,
            anchor=W,
            fg="#FFCAB1",
            bg="#5F634F",
            selectcolor="#000000",
        ).pack(pady=5, expand=False, side="top", ipady=3)
        ttk.Label(
            labelframe_cc,
            text="Add emails here to copy them:",
        ).pack(fill=X, expand=False, side="top")
        self._userinput_CC1 = Text(
            labelframe_cc,
            height=1,
            width=30,
            background=BR.alt_bg_color,
            foreground=BR.alt_fg_color,
            highlightcolor=BR.alt_bg_color,
            selectbackground=BR.alt_fg_color,
            selectforeground=BR.alt_bg_color,
        )
        self._userinput_CC1.pack(
            pady=2, ipady=4, anchor=N, fill=X, expand=False, side="top"
        )
        ttk.Label(
            labelframe_cc,
            text="2nd Optional list to copy:",
        ).pack(fill=X, expand=False, side="top")
        self._userinput_CC2 = Text(
            labelframe_cc,
            height=1,
            width=30,
            background=BR.alt_bg_color,
            foreground=BR.alt_fg_color,
            highlightcolor=BR.alt_bg_color,
            selectbackground=BR.alt_fg_color,
            selectforeground=BR.alt_bg_color,
        )
        self._userinput_CC2.pack(ipady=4, anchor=N, fill=X, expand=False, side="top")
        ttk.Button(
            self.home,
            text="View Each Before Sending!",
            command=lambda: presenter.btn_send_envelopes(autosend=False),
        ).grid(column=1, row=2, sticky=NSEW, padx=(10), pady=10)
        # .pack(ipady=20, ipadx=2, pady=10, anchor=S, fill=Y, expand=False)
        right_header_frame = ttk.Frame(self.home)
        right_header_frame.grid(column=2, row=0, pady=5)
        ttk.Label(
            right_header_frame,
            style="Header.TLabel",
            text="Choose Markets:",
        ).pack(fill=X, expand=True, side="left")

        self.frame_right = ttk.Frame(self.home)
        self.frame_right.grid(column=2, row=1, pady=(0, 5), sticky=N)
        self.__create_button(
            self.frame_right,
            "Seawave",
            self._seawave,
        )
        self.__create_button(
            self.frame_right,
            "Prime Time",
            self._primetime,
        )
        self.__create_button(
            self.frame_right,
            "New Hampshire",
            self._newhampshire,
        )
        self.__create_button(
            self.frame_right,
            "American Modern",
            self._americanmodern,
        )
        self.__create_button(
            self.frame_right,
            "Kemah Marine",
            self._kemah,
        )
        self.__create_button(
            self.frame_right,
            "Concept",
            self._concept,
        )
        self.__create_button(
            self.frame_right,
            "Yachtinsure",
            self._yachtinsure,
        )
        self.__create_button(
            self.frame_right,
            "Century",
            self._century,
        )
        self.__create_button(
            self.frame_right,
            "Intact",
            self._intact,
        )
        self.__create_button(
            self.frame_right,
            "Travelers",
            self._travelers,
        )
        ttk.Button(
            self.home,
            text="Submit & auto-send all",
            command=presenter.btn_send_envelopes,
        ).grid(column=2, row=2, sticky=NSEW, padx=5, pady=10)

    def create_customize_tab_widgets(self, presenter: Presenter):
        self.template_customization.columnconfigure(0, minsize=740, pad=5)
        self.template_customization.rowconfigure(2, minsize=100, pad=5)

        title_frame = ttk.Frame(
            self.template_customization,
            height=5,
        )
        title_frame.grid(column=0, row=0, pady=(0, 5), padx=10, sticky=N)
        ttk.Label(
            title_frame,
            text="Customize Email Templates for Each Underwriter",
            style="Header.TLabel",
        ).pack(
            fill=X,
            expand=True,
            side="top",
            anchor=N,
        )
        customize_msg_lf = ttk.Labelframe(
            self.template_customization,
            text="Don't forget to save!",
        )
        customize_msg_lf.grid(column=0, row=1, padx=10, sticky=NSEW)

        template_select_frame = ttk.Frame(
            customize_msg_lf,
        )
        template_select_frame.grid(
            column=0, row=0, padx=15, pady=10, sticky=NSEW, columnspan=2
        )
        # .pack(
        #     padx=15,
        #     pady=10,
        #     fill=BOTH,
        #     expand=True,
        # )
        self.create_dropdown(
            parent=template_select_frame,
            presenter=presenter,
        )
        self._dropdown_menu_var.trace_add(
            "write",
            presenter.on_change_template,
        )

        ttk.Label(
            customize_msg_lf,
            text="Submission Address:",
        ).grid(column=0, row=1)

        self.address_entry = ttk.Entry(
            master=customize_msg_lf,
            name="address",
            textvariable=self._address,
            width=89,
            # validate="focusout",
            # validatecommand=presenter.on_focus_out,
        )
        self.address_entry.grid(
            column=1,
            row=1,
            sticky=W,
            ipady=5,
            pady=5,
        )
        self.address_entry.bind(
            "<FocusOut>",
            presenter.on_focus_out,
        )

        ttk.Label(
            customize_msg_lf,
            text="Greeting:",
        ).grid(column=0, row=2)

        self.greet_entry = ttk.Entry(
            master=customize_msg_lf,
            name="greeting",
            textvariable=self._greeting,
            width=89,
            style="TEntry",
        )
        self.greet_entry.grid(
            column=1,
            row=2,
            sticky=W,
            pady=5,
            ipady=5,
        )
        self.greet_entry.bind(
            "<FocusOut>",
            presenter.on_focus_out,
        )

        ttk.Label(
            customize_msg_lf,
            text="Body of the email:",
        ).grid(column=0, row=3)

        self._body_text = Text(
            customize_msg_lf,
            name="body",
            width=67,
            height=5,
            wrap=WORD,
            foreground=BR.alt_fg_color,
            background=BR.alt_bg_color,
            highlightcolor=BR.alt_bg_color,
            selectbackground=BR.alt_fg_color,
            selectforeground=BR.alt_bg_color,
        )
        self._body_text.grid(
            column=1,
            row=3,
            sticky=W,
            pady=5,
        )
        self._body_text.bind(
            "<FocusOut>",
            presenter.on_focus_out,
        )

        ttk.Label(
            customize_msg_lf,
            text="Salutation:",
        ).grid(column=0, row=4)

        self.sal_entry = ttk.Entry(
            customize_msg_lf,
            name="salutation",
            textvariable=self._salutation,
            width=89,
        )
        self.sal_entry.grid(
            column=1,
            row=4,
            sticky=W,
            pady=5,
            ipady=5,
        )
        self.sal_entry.bind("<FocusOut>", presenter.on_focus_out)

        buttons_frame = ttk.Frame(
            self.template_customization,
        )
        buttons_frame.grid(column=0, row=2, padx=10, sticky=NSEW)
        ttk.Button(
            buttons_frame,
            name="btnResetTemplate",
            text="Revert Back",
            command=presenter.btn_reset_template,
        ).pack(
            padx=10,
            pady=10,
            fill=BOTH,
            expand=True,
            anchor=N,
            side="left",
        )
        ttk.Button(
            buttons_frame,
            name="btnViewTemplate",
            text="View Current Example",
            width=20,
            command=presenter.btn_view_template,
        ).pack(
            padx=4,
            pady=10,
            fill=BOTH,
            expand=True,
            anchor=N,
            side="left",
        )
        ttk.Button(
            buttons_frame,
            name="btnSaveTemplate",
            text="Save",
            width=20,
            command=presenter.btn_save_template,
        ).pack(
            padx=10,
            pady=10,
            fill=BOTH,
            expand=True,
            anchor=N,
            side="left",
        )

    def create_email_settings_tab_widgets(self, presenter: Presenter):
        self.email_settings.rowconfigure(3, minsize=100, pad=5)
        ### START TITLE ###
        title_frame = ttk.Frame(
            self.email_settings,
            height=10,
        )
        title_frame.grid(column=0, row=0, sticky=NSEW, pady=(0, 5), padx=15)
        ttk.Label(
            title_frame,
            text="Email Settings Page",
            style="Header.TLabel",
        ).pack(
            fill=BOTH,
            expand=True,
            padx=200,
        )
        # END OF TITLE
        # BEGIN CC SETTINGS
        default_cc_lf = ttk.Labelframe(
            self.email_settings,
            text="""Want to CC specific groups of people by default?""",
        )
        default_cc_lf.grid(column=0, row=1, sticky=NSEW, padx=10)
        default_cc_lf.columnconfigure(1, minsize=660)
        ttk.Label(
            master=default_cc_lf,
            text="CC Group 1:",
        ).grid(
            column=0,
            row=0,
            pady=6,
            padx=(0, 5),
            sticky=EW,
        )
        cc1 = ttk.Entry(
            default_cc_lf,
            textvariable=self._default_cc1,
            name="default_cc1",
            font=1,
        )
        cc1.grid(
            column=1,
            row=0,
            sticky=EW,
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
            textvariable=self._default_cc2,
            name="default_cc2",
            font=1,
        )
        cc2.grid(
            column=1,
            row=1,
            rowspan=4,
            sticky=EW,
            ipadx=200,
            ipady=3,
            pady=6,
        )
        # END OF CC SETTINGS
        # BEGIN SIGNATURE SETTINGS
        signature_lf = ttk.Labelframe(
            self.email_settings,
            text="Email Signature Settings",
        )
        signature_lf.grid(column=0, row=2, sticky=NSEW, padx=10, pady=(15, 0))
        signature_lf.columnconfigure(4, minsize=105)
        ttk.Label(
            signature_lf,
            text="Your name:",
        ).grid(row=0, column=0, padx=(0, 5), pady=(5, 0))
        username_entry = ttk.Entry(
            master=signature_lf,
            textvariable=self._username,
            font=1,
        )
        username_entry.grid(
            row=0,
            column=1,
            columnspan=2,
            padx=(0, 7),
            pady=(5, 0),
            ipadx=30,
            ipady=3,
        )
        ttk.Label(
            signature_lf,
            text="Signature image:",
        ).grid(row=0, column=4, padx=5, pady=(5, 0))
        self.sig_image_path_box = Text(
            signature_lf,
            name="sig_image_path_file",
            height=4,
            width=36,
            foreground=BR.alt_fg_color,
            background=BR.alt_bg_color,
            highlightcolor=BR.alt_bg_color,
            selectbackground=BR.alt_fg_color,
            selectforeground=BR.alt_bg_color,
        )
        self.sig_image_path_box.grid(
            row=0,
            column=5,
            columnspan=2,
            rowspan=2,
            pady=(5, 1),
            padx=(0, 1),
            sticky=NSEW,
        )
        self.sig_image_path_box.drop_target_register(DND_FILES)
        self.sig_image_path_box.dnd_bind(
            "<<Drop>>",
            presenter.process_signature_image_path,
        )
        self.sig_image_btn = ttk.Button(
            signature_lf,
            command=self._browse_sig_image,
            text="Browse",
        )
        self.sig_image_btn.grid(
            row=1,
            column=4,
            ipady=8,
            pady=(2, 1),
            padx=5,
        )
        ### BUTTONS FRAME ###
        buttons_frame = ttk.Frame(
            self.email_settings,
        )
        buttons_frame.grid(column=0, row=3, sticky=NSEW, padx=10, pady=5)
        ttk.Button(
            master=buttons_frame,
            text="Revert Back",
            command=presenter.btn_revert_email_settings,
        ).pack(
            fill=BOTH,
            expand=True,
            side="left",
            padx=10,
            pady=5,
        )
        ttk.Button(
            master=buttons_frame,
            text="Save Settings",
            command=presenter.btn_save_email_settings,
        ).pack(
            fill=BOTH,
            expand=True,
            side="left",
            padx=10,
            pady=5,
        )

    def create_folder_settings_tab_widgets(self, presenter: Presenter):
        ### Start Watch Dir Settings ###
        self.folder_settings.rowconfigure(3, minsize=100, pad=5)
        ### START TITLE ###
        title_frame = ttk.Frame(
            self.folder_settings,
        )
        title_frame.grid(column=0, row=0, sticky=NSEW)
        ttk.Label(title_frame, text="Folder Settings Page", style="Header.TLabel").pack(
            fill=BOTH,
            expand=True,
            padx=200,
        )
        # END OF TITLE
        # START CONTENT
        watch_dir_lf = ttk.Labelframe(
            self.folder_settings,
            text="Watch Folder Options",
        )
        watch_dir_lf.grid(column=0, row=1, sticky=NSEW, padx=10, pady=(5, 0))
        ttk.Label(
            watch_dir_lf,
            text="Current Watch Folder:",
        ).grid(column=0, row=0, ipady=3, pady=6)
        self.watch_dir_entry = ttk.Entry(
            watch_dir_lf,
            textvariable=self._watch_dir,
        )
        self.watch_dir_entry.grid(column=1, row=0, padx=5, pady=6, ipady=3, ipadx=149)
        watch_dir_btn = ttk.Button(
            watch_dir_lf,
            command=self._browse_watch_dir,
            text="Browse to change",
        )
        watch_dir_btn.grid(column=2, row=0, padx=5, pady=6, ipady=3, ipadx=4)
        ttk.Label(
            watch_dir_lf,
            text="New Biz Client Folder:",
        ).grid(column=0, row=1, ipady=3, padx=0)
        self.new_biz_dir_entry = ttk.Entry(
            watch_dir_lf,
            textvariable=self._new_biz_dir,
        )
        self.new_biz_dir_entry.grid(column=1, row=1, padx=5, pady=0, ipady=3, ipadx=149)
        new_biz_dir_btn = ttk.Button(
            watch_dir_lf,
            command=self._browse_new_biz_dir,
            text="Browse to change",
        )
        new_biz_dir_btn.grid(column=2, row=1, padx=5, pady=0, ipady=3, ipadx=4)
        ttk.Label(
            watch_dir_lf,
            text="Renewals Client Folder:",
        ).grid(column=0, row=2, ipady=3, padx=0)
        self.renewals_dir_entry = ttk.Entry(
            watch_dir_lf,
            textvariable=self._renewals_dir,
        )
        self.renewals_dir_entry.grid(
            column=1, row=2, padx=5, pady=6, ipady=3, ipadx=149
        )
        renewals_dir_btn = ttk.Button(
            watch_dir_lf,
            command=self._browse_renewals_dir,
            text="Browse to change",
        )
        renewals_dir_btn.grid(column=2, row=2, padx=5, pady=6, ipady=3, ipadx=4)
        custom_dir_lf = ttk.Labelframe(
            self.folder_settings,
            text="Create additional folders when a client folder is created",
        )
        ### START Custom Dir Structure Label Frame ###
        custom_dir_lf.grid(column=0, row=2, sticky=NSEW, pady=(5, 0), padx=10)
        ### LEFT SECTION ###
        left_custom_dir_frame = ttk.Frame(custom_dir_lf)
        left_custom_dir_frame.pack(
            fill=X,
            expand=False,
            side="left",
        )
        ### Treeview Section ###
        self.tree = ttk.Treeview(
            left_custom_dir_frame,
            columns=1,
        )
        self.tree.column(
            "#0",
            width=120,
            stretch=False,
        )
        self.tree.column(
            "#1",
            width=350,
            stretch=False,
        )
        self.tree.heading("#0", text="Folder Structure", anchor="w")
        self.tree.heading("#1", text="Folder Name", anchor="w")
        # self.tree.pack(fill="both", expand=True, side="left")
        self.tree.grid(column=0, row=0, pady=(5, 0))
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
            anchor=S,
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
        self.top_left_custom_dir_entry = ttk.Entry(
            top_left_custom_dir_frame,
            textvariable=self._custom_parent_dir,
        )
        self.top_left_custom_dir_entry.pack(
            fill=X, expand=True, side="top", ipady=3, anchor=N
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
            command=self._add_custom_parent_dir,
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
        ).pack(fill="both", expand=True, side="top", anchor=S)
        self.middle_left_custom_dir_entry = ttk.Entry(
            middle_left_custom_dir_frame,
            textvariable=self._custom_sub_dir,
        )
        self.middle_left_custom_dir_entry.pack(
            fill=X, expand=True, side="top", ipady=3, anchor=N
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
            command=self._add_custom_sub_dir,
            text="Add",
        )
        custom_sub_dir_btn.pack(
            fill="both", expand=True, side="left", pady=6, padx=(5, 0)
        )
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
            command=self._rm_custom_dir,
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
            self.folder_settings,
        )
        buttons_box.grid(column=0, row=3, sticky=NSEW, pady=(10, 0), padx=10)
        ttk.Button(
            master=buttons_box,
            text="Revert Back",
            command=presenter.btn_revert_folder_settings,
        ).pack(
            fill=BOTH,
            expand=True,
            side="left",
            padx=(0, 5),
        )
        ttk.Button(
            master=buttons_box,
            text="Save Settings",
            command=presenter.btn_save_folder_settings,
        ).pack(
            fill=BOTH,
            expand=True,
            side="left",
            padx=(5, 0),
        )

    def create_quoteform_path_box(
        self,
        parent: Frame,
        presenter=Presenter,
    ) -> None:
        """Creates the drag-n-drop box for the quoteform."""
        self.quoteform_path_box = Text(
            parent,
            name="raw_quoteform_path",
            height=8,
            width=10,
            background=BR.alt_bg_color,
            foreground=BR.alt_fg_color,
            highlightcolor=BR.alt_bg_color,
            selectbackground=BR.alt_fg_color,
            selectforeground=BR.alt_bg_color,
        )
        self.quoteform_path_box.drop_target_register(DND_FILES)
        self.quoteform_path_box.dnd_bind(
            "<<Drop>>",
            presenter.process_quoteform_path,
        )
        self.quoteform_path_box.pack(
            fill=BOTH,
            anchor=N,
            expand=False,
        )

    def _browse_qf_path(self):
        try:
            dir_name = filedialog.askdirectory()
            if not dir_name == "":
                self.quoteform_path_box = self.quoteform
        except AttributeError as e:
            print(f"caught {e}. Continuing on.")

    def create_extra_attachments_path_box(
        self, parent: Frame, presenter=Presenter
    ) -> None:
        """Creates the drag-n-drop box for any extra attachments."""
        self.extra_attachments_path_box = Text(
            parent,
            height=8,
            width=10,
            foreground=BR.alt_fg_color,
            background=BR.alt_bg_color,
            highlightcolor=BR.alt_bg_color,
            selectbackground=BR.alt_fg_color,
            selectforeground=BR.alt_bg_color,
            name="raw_attachments_paths_list",
        )
        self.extra_attachments_path_box.pack(fill=BOTH, expand=False, anchor=N)
        self.extra_attachments_path_box.drop_target_register(DND_FILES)
        self.extra_attachments_path_box.dnd_bind(
            "<<Drop>>", presenter.process_attachments_path
        )

    def _browse_extra_file_path(self):
        try:
            dir_name = filedialog.askdirectory()
            if not dir_name == "":
                self.extra_attachments_path_box = self.extra_attachments
        except AttributeError as e:
            print(f"caught {e}. Continuing on.")

    def __create_button(self, root, text: str, int_variable: IntVar):
        x = Checkbutton(
            root,
            name=text.lower(),
            text=text,
            variable=int_variable,
            onvalue=self._yes,
            offvalue=self._no,
            relief="raised",
            # font=("helvetica", 10, "bold"),
            justify=CENTER,
            anchor=W,
            fg="#FFCAB1",
            bg="#5F634F",
            selectcolor="#000000",
        )
        x.pack(fill=BOTH, expand=True, ipady=3, ipadx=40, pady=(0, 3))

    def create_dropdown(self, parent, presenter: Presenter) -> None:
        """Creates the OptionMenu widget separately for less coupling."""
        options: list[str] = presenter.set_dropdown_options()
        dropdown_menu = OptionMenu(parent, self._dropdown_menu_var, *options)
        dropdown_menu.configure(
            background=BR.btn_base_bg,
            foreground=BR.btn_fg,
            activebackground=BR.btn_active_bg,
            activeforeground=BR.btn_fg,
            highlightbackground=BR.alt_bg_color,
            highlightcolor="red",
            font=("helvetica", 14, "normal"),
        )
        print(dropdown_menu["menu"].keys())
        dropdown_menu["menu"].configure(
            background=BR.menuoption_bg_color,
            foreground=BR.menuoption_fg_color,
            activebackground=BR.menuoption_fg_color,
            activeforeground=BR.menuoption_bg_color,
            selectcolor="red",
        )
        dropdown_menu.pack(padx=15, ipady=5, fill=X, expand=True)

    def get_active_focus(self) -> dict:
        return self.root.focus_get()

    def _browse_sig_image(self):
        try:
            file_name = filedialog.askopenfile().name
            self.sig_image_path_box.delete("1.0", "end")
            self.sig_image_path_box.insert("1.0", file_name)
        except AttributeError as e:
            print(f"caught {e}. Continuing on.")
        # del self.sig_image_file

    def _browse_watch_dir(self):
        try:
            dir_name = filedialog.askdirectory()
            if not dir_name == "":
                self.watch_dir = dir_name
        except AttributeError as e:
            print(f"caught {e}. Continuing on.")

    def _browse_new_biz_dir(self):
        try:
            dir_name = filedialog.askdirectory()
            if not dir_name == "":
                self.new_biz_dir = dir_name
        except AttributeError as e:
            print(f"caught {e}. Continuing on.")

    def _browse_renewals_dir(self):
        try:
            dir_name = filedialog.askdirectory()
            if not dir_name == "":
                self.renewals_dir = dir_name
        except AttributeError as e:
            print(f"caught {e}. Continuing on.")

    def _add_custom_parent_dir(self):
        dir_name: str | int = self.custom_parent_dir
        self._insert_row(data=dir_name)
        del self.custom_parent_dir

    def _add_custom_sub_dir(self):
        # Get selected row_id
        current_selected_id = self.tree.selection()
        parent_name = self.tree.set(current_selected_id)["1"]
        dir_name: str | int = self.custom_sub_dir
        self.tree.insert(
            parent=current_selected_id,
            index="end",
            text=parent_name,
            values=dir_name,
            open=True,
        )
        del self.custom_sub_dir

    def _insert_row(self, data: str):
        if isinstance(data, int):
            data = str(data)
        if "/" in data:
            # split "/" up into a list of strings
            entry_list = data.split("/")
            # find the top-most parent's row id by name & label == "Top Level"
            parent_id = self.__find_row_id_by_name(entry_list[0])
            # check for any other slashes / parents
            if len(entry_list) == 3:
                # find the next parent's row id by name & label != "Top Level"
                sub_parent_id = self.__find_row_id_by_name(entry_list[1])
                # create row under sub_parent row:
                self.tree.insert(
                    parent=sub_parent_id,
                    index="end",
                    text=entry_list[1],
                    values=entry_list[2],
                    open=True,
                )
            else:
                # create row under parent row:
                self.tree.insert(
                    parent=parent_id,
                    index="end",
                    text=entry_list[0],
                    values=[entry_list[1]],
                    open=True,
                )
        else:
            # add entry as a row:
            # assign "Top Level" as label,
            # "name" as folder name, and
            # a unique row id
            self.tree.insert(
                parent="",
                index="end",
                text="----------------",
                values=[data],
                open=True,
            )

    def get_all_rows(self) -> list[str]:
        row_data = []
        for parent in self.tree.get_children():
            parent_dir = self.tree.item(parent)["values"]
            row_data.append(parent_dir[0])
            for child in self.tree.get_children(parent):
                child_dir = self.tree.item(child)["values"]
                path = f"{parent_dir[0]}/{child_dir.pop()}"
                row_data.append(path)
        return row_data

    def set_data_into_treeview(self, data: list[str]):
        if isinstance(data, list):
            for item in data:
                self._insert_row(item)
        else:
            self._insert_row(data)

    def _rm_custom_dir(self):
        current_item = self.tree.selection()
        self.tree.delete(current_item)

    def __find_row_id_by_name(self, name: str):
        for parent in self.tree.get_children():
            if name in str(self.tree.item(parent)["values"]):
                return parent
            for child in self.tree.get_children(parent):
                if name in self.tree.item(str(child))["values"]:
                    return child

    def set_start_tab(self, specific_tab: str) -> None:
        if specific_tab == "email":
            self.root.tabControl.select(2)
        if specific_tab == "folder":
            self.root.tabControl.select(3)
