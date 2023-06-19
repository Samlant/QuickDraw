import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.ttk import Notebook, Style
from tkinter import *
from tkinterdnd2 import DND_FILES, TkinterDnD
from typing import Any, Protocol


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

    def btn_save_settings(self) -> None:
        ...

    def btn_revert_settings(event) -> None:
        ...

    def set_dropdown_options(self) -> list:
        ...

    def process_quoteform_path(self, raw_path) -> None:
        ...

    def process_attachments_path(self, raw_path) -> None:
        ...

    def update_dropdown(self):
        ...

    def save_extra_notes(self, notes: str) -> None:  # GOOD
        ...

    def on_change_template(self, *args, **kwargs) -> None:
        ...

    def on_focus_out(self, field_name: str, current_text: str) -> bool:
        ...


class TkView(TkinterDnD.Tk):
    """This class uses tkinter to create a view object when instantiated by the main_script.  After __init__,  there's a parent method, create_GUI_obj, responsivle for creating the widgets.  These sub-functions are divided by page/tab. Lastly, there are methods to allow data retrieval and updating.
    class attr positive_submission is for setting the value for a submission to be processed and sent. This is the one spot it needs updating.
    """

    def __init__(self, positive_value, negative_value, icon_src: str) -> None:
        super().__init__()
        self.geometry("760x548")
        self.configure(background="#5F9EA0")
        self.attributes("-topmost", True)
        self.title("QuickDraw")
        self.attributes("-alpha", 0.95)
        self.iconbitmap(icon_src)
        self._yes = positive_value
        self._no = negative_value
        self.assign_private_string_bool_vars()

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

    # settings_tab: getters/setters
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
        self.sig_image_path_box.insert("1.0", new_image_file)

    @sig_image_file.deleter
    def sig_image_file(self):
        self.sig_image_file.delete("1.0", END)

    # def resource_path(self, relative_path):
    #     """ Get absolute path to resource, works for dev and for PyInstaller """
    #     try:
    #         # PyInstaller creates a temp folder and stores path in _MEIPASS
    #         base_path = sys._MEIPASS
    #     except Exception:
    #         base_path = os.path.abspath(".")
    #     return os.path.join(base_path, relative_path)

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

    def create_UI_obj(self, presenter: Presenter):
        """This creates the GUI root,  along with the main
        functions to create the widgets.
        """
        self.create_style()
        self.create_notebook()
        self.create_tabs()
        self.create_main_tab_widgets(presenter)
        self.create_customize_tab_widgets(presenter)
        self.create_settings_tab_widgets(presenter)

    def create_style(self):
        self.style = Style(master=self)
        self.style.theme_use("default")
        self.style.configure("TNotebook", background="#5F9EA0")
        self.style.configure("TFrame", background="#5F9EA0")
        self.style.map("TNotebook", background=[("selected", "#5F9EA0")])

    def create_notebook(self):
        self.tabControl = ttk.Notebook(master=self)
        self.tabControl.pack(pady=0, expand=True)

    def create_tabs(self):
        self.home = ttk.Frame(self.tabControl)
        self.template_customization = ttk.Frame(self.tabControl)
        self.settings = ttk.Frame(self.tabControl)
        self.tabControl.add(self.home, text="Home - Outbox")
        self.tabControl.add(self.template_customization, text="Customize Templates")
        self.tabControl.add(self.settings, text="Settings")

    def create_main_tab_widgets(self, presenter: Presenter):
        frame_header = Frame(self.home, bg="#5F9EA0", pady=17)
        frame_header.pack(padx=5, fill=X, expand=False)
        Label(
            frame_header,
            text="Get Client Information",
            bg="#5F9EA0",
            font=("helvetica", 20, "normal"),
        ).pack(fill=X, expand=True, side="left")
        Label(
            frame_header,
            text="Extra Notes & CC",
            bg="#5F9EA0",
            font=("helvetica", 20, "normal"),
        ).pack(fill=X, expand=True, side="left")
        Label(
            frame_header,
            text="Choose Markets:",
            bg="#5F9EA0",
            font=("helvetica", 20, "normal"),
        ).pack(fill=X, expand=True, side="left")

        frame_left = Frame(self.home, bg="#5F9EA0")
        frame_left.pack(padx=5, fill=Y, side="left", expand=False, anchor=NE)
        Label(
            frame_left,
            text="Dag-N-Drop Quoteform Below",
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(ipady=5, fill=BOTH, expand=True)
        self.create_quoteform_path_box(frame_left, presenter)
        Label(
            frame_left,
            text="Dag-N-Drop Extra Attachments Below",
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(ipady=5, fill=BOTH, expand=True)
        self.create_extra_attachments_path_box(frame_left, presenter)
        Button(
            frame_left,
            text="Clear attachments",
            bg="#e50000",
            font=("helvetica", 12, "normal"),
            command=presenter.btn_clear_attachments,
        ).pack(ipady=20, pady=10, anchor=S, fill=BOTH, expand=True)

        frame_middle = Frame(self.home, bg="#5F9EA0")
        frame_middle.pack(padx=5, fill=Y, side="left", expand=False, anchor=N)
        labelframe_main1 = LabelFrame(
            frame_middle,
            text="To end with a message, enter it below:",
            bg="#aedadb",
            font=("helvetica", 8, "normal"),
        )
        labelframe_main1.pack(fill=X, expand=False, side="top")
        self._extra_notes_text = Text(
            labelframe_main1,
            height=7,
            width=30,
            name="raw_extra_notes",
        )
        self._extra_notes_text.focus_set()
        self._extra_notes_text.pack(fill=X, anchor=N, expand=FALSE, side="top")
        labelframe_cc = LabelFrame(
            frame_middle,
            text="CC-address settings for this submission:",
            bg="#aedadb",
            name="labelframe_cc",
        )
        labelframe_cc.pack(fill=X, expand=True, side="top")
        Label(
            labelframe_cc,
            text="email address to CC:",
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(fill=X, expand=True, side="top")
        Checkbutton(
            labelframe_cc,
            text="Include default CC addresses",
            variable=self._use_CC_defaults,
            bg="#aedadb",
            name="cc_def_check",
            onvalue=True,
            offvalue=False,
        ).pack(pady=5, fill=X, expand=False, side="top")
        self._userinput_CC1 = Text(labelframe_cc, height=1, width=30)
        self._userinput_CC1.pack(
            pady=2, ipady=4, anchor=N, fill=X, expand=True, side="top"
        )
        Label(
            labelframe_cc,
            text="email address to CC:",
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(fill=X, expand=True, side="top")
        self._userinput_CC2 = Text(labelframe_cc, height=1, width=30)
        self._userinput_CC2.pack(ipady=4, anchor=N, fill=X, expand=True, side="top")
        Button(
            frame_middle,
            text="View Each Before Sending!",
            bg="#22c26a",
            font=("helvetica", 12, "normal"),
            command=lambda: presenter.btn_send_envelopes(autosend=False),
        ).pack(ipady=20, ipadx=2, pady=10, anchor=S, fill=Y, expand=False)

        self.frame_right = Frame(self.home, bg="#5F9EA0")
        self.frame_right.pack(padx=5, fill=BOTH, side="left", expand=True, anchor=NW)
        Checkbutton(
            master=self.frame_right,
            name="seawave",
            text="Seawave",
            variable=self._seawave,
            onvalue=self._yes,
            offvalue=self._no,
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(ipady=3, fill=BOTH, expand=True)
        Checkbutton(
            master=self.frame_right,
            name="prime time",
            text="Prime Time",
            variable=self._primetime,
            onvalue=self._yes,
            offvalue=self._no,
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(ipady=3, fill=BOTH, expand=True)
        Checkbutton(
            master=self.frame_right,
            name="newhampshire",
            text="New Hampshire",
            variable=self._newhampshire,
            onvalue=self._yes,
            offvalue=self._no,
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(ipady=3, fill=BOTH, expand=True)
        Checkbutton(
            master=self.frame_right,
            name="americanmodern",
            text="American Modern",
            variable=self._americanmodern,
            onvalue=self._yes,
            offvalue=self._no,
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(ipady=3, fill=BOTH, expand=True)
        Checkbutton(
            master=self.frame_right,
            name="kemah",
            text="Kemah Marine",
            variable=self._kemah,
            onvalue=self._yes,
            offvalue=self._no,
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(ipady=3, fill=BOTH, expand=True)
        Checkbutton(
            master=self.frame_right,
            name="concept",
            text="Concept",
            variable=self._concept,
            onvalue=self._yes,
            offvalue=self._no,
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(ipady=3, fill=BOTH, expand=True)
        Checkbutton(
            master=self.frame_right,
            name="yachtinsure",
            text="Yacht Insure",
            variable=self._yachtinsure,
            onvalue=self._yes,
            offvalue=self._no,
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(ipady=3, fill=BOTH, expand=True)
        Checkbutton(
            master=self.frame_right,
            name="century",
            text="Century",
            variable=self._century,
            onvalue=self._yes,
            offvalue=self._no,
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(ipady=3, fill=BOTH, expand=True)
        Checkbutton(
            master=self.frame_right,
            name="intact",
            text="Intact",
            variable=self._intact,
            onvalue=self._yes,
            offvalue=self._no,
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(ipady=3, fill=BOTH, expand=True)
        Checkbutton(
            master=self.frame_right,
            name="travelers",
            text="Travelers",
            variable=self._travelers,
            onvalue=self._yes,
            offvalue=self._no,
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(ipady=3, fill=BOTH, expand=True)
        Button(
            self.frame_right,
            text="Submit & auto-send all",
            bg="#22c26a",
            font=("helvetica", 12, "normal"),
            command=presenter.btn_send_envelopes,
        ).pack(ipady=20, pady=10, anchor=S, fill=BOTH, expand=True)

    def create_customize_tab_widgets(self, presenter: Presenter):
        title_frame = Frame(
            self.template_customization,
            bg="#5F9EA0",
            height=5,
        )
        title_frame.pack(pady=20, fill=X, expand=False)
        Label(
            title_frame,
            text="Customize Your Envelopes Here",
            bg="#aedadb",
            font=("helvetica", 20, "normal"),
        ).pack(
            fill=X,
            expand=True,
            side="top",
            anchor=N,
            padx=140,
        )
        Label(
            title_frame,
            text="Customize the email template for each carrier,  or a  combination of carriers if they use the same address.",
            bg="#5F9EA0",
            font=("helvetica", 12, "normal"),
        ).pack(
            padx=4,
            pady=5,
            fill=X,
            expand=True,
            side="top",
            anchor=N,
        )

        template_select_frame = Frame(self.template_customization, bg="#5F9EA0")
        template_select_frame.pack(padx=15, pady=10, fill=BOTH, expand=True)
        self.create_dropdown(parent=template_select_frame, presenter=presenter)
        self._dropdown_menu_var.trace_add("write", presenter.on_change_template)

        content_frame = Frame(self.template_customization, bg="#aedadb")
        content_frame.pack(fill=BOTH, expand=True, anchor=N, side="top", padx=5, pady=5)

        Label(
            content_frame,
            text="Submission Address:",
            bg="#aedadb",
            font=("helvetica", 16, "normal"),
        ).grid(column=0, row=0)

        self.address_entry = Entry(
            master=content_frame,
            name="address",
            textvariable=self._address,
            width=89,
            validate="focusout",
            validatecommand=presenter.on_focus_out,
        )
        self.address_entry.grid(
            column=1,
            row=0,
            sticky=W,
            ipady=5,
            pady=5,
        )

        self.address_entry.bind("<FocusOut>", presenter.on_focus_out)

        Label(
            content_frame,
            text="Greeting:",
            bg="#aedadb",
            font=("helvetica", 16, "normal"),
        ).grid(column=0, row=1)

        self.greet_entry = Entry(
            master=content_frame,
            name="greeting",
            textvariable=self._greeting,
            width=89,
        )
        self.greet_entry.grid(
            column=1,
            row=1,
            sticky=W,
            pady=5,
            ipady=5,
        )
        self.greet_entry.bind("<FocusOut>", presenter.on_focus_out)

        Label(
            content_frame,
            text="Body of the email:",
            bg="#aedadb",
            font=("helvetica", 16, "normal"),
        ).grid(column=0, row=2)

        self._body_text = Text(
            content_frame,
            name="body",
            width=67,
            height=5,
            wrap=WORD,
        )
        self._body_text.grid(
            column=1,
            row=2,
            sticky=W,
            pady=5,
        )
        self._body_text.bind("<FocusOut>", presenter.on_focus_out)

        Label(
            content_frame,
            text="Salutation:",
            bg="#aedadb",
            font=("helvetica", 16, "normal"),
        ).grid(column=0, row=3)

        self.sal_entry = Entry(
            content_frame,
            name="salutation",
            textvariable=self._salutation,
            width=89,
            highlightbackground="green",
            highlightcolor="red",
        )
        self.sal_entry.grid(column=1, row=3, sticky=W, pady=5, ipady=5)
        self.sal_entry.bind("<FocusOut>", presenter.on_focus_out)

        buttons_frame = Frame(self.template_customization, bg="#5F9EA0")
        buttons_frame.pack(fill=X, expand=True, anchor=N)
        Button(
            buttons_frame,
            name="btnResetTemplate",
            text="RESET to last saved",
            bg="#ff0032",
            font=("helvetica", 16, "normal"),
            command=presenter.btn_reset_template,
        ).pack(
            padx=10,
            pady=10,
            ipady=30,
            fill=X,
            expand=False,
            anchor=N,
            side="left",
        )
        Button(
            buttons_frame,
            name="btnViewTemplate",
            text="View Current Example",
            bg="#00feff",
            font=("helvetica", 16, "normal"),
            width=20,
            command=presenter.btn_view_template,
        ).pack(
            padx=4,
            pady=10,
            ipady=30,
            fill=X,
            expand=False,
            anchor=N,
            side="left",
        )
        Button(
            buttons_frame,
            name="btnSaveTemplate",
            text="Save",
            bg="#22c26a",
            font=("helvetica", 16, "normal"),
            width=20,
            command=presenter.btn_save_template,
        ).pack(
            padx=10,
            pady=10,
            ipady=30,
            fill=X,
            expand=False,
            anchor=N,
            side="left",
        )

    def create_settings_tab_widgets(self, presenter: Presenter):
        content_boder = Frame(
            self.settings,
            padx=20,
            pady=20,
            bg="#5F9EA0",
        )
        content_boder.pack(
            fill=BOTH,
            expand=True,
        )
        title_frame = Frame(
            content_boder,
            bg="#5F9EA0",
            height=10,
        )
        title_frame.pack(fill=X, expand=False, side="top")
        Label(
            title_frame,
            text="Settings Page",
            bg="#aedadb",
            font=("helvetica", 20, "normal"),
        ).pack(
            fill=BOTH,
            expand=True,
            padx=200,
        )
        # END OF TITLE
        # BEGIN CC SETTINGS
        main_settings_frame = Frame(
            content_boder,
            bg="#5F9EA0",
        )
        main_settings_frame.pack(
            fill=BOTH,
            expand=True,
            side="top",
        )
        default_cc_lf = LabelFrame(
            main_settings_frame,
            text='Add emails that you want to CC quote submissions on---separate using a ";" (semicolon)',
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        )
        default_cc_lf.pack(
            fill=X,
            expand=False,
            pady=10,
            side="top",
        )
        Label(
            master=default_cc_lf,
            text="CC Group 1:",
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).grid(
            column=0,
            row=0,
            pady=6,
        )
        cc1 = Entry(
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
        Label(
            default_cc_lf,
            text="CC Group 2:",
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).grid(
            column=0,
            row=1,
            pady=6,
        )
        cc2 = Entry(
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
        signature_lf = LabelFrame(
            main_settings_frame,
            text="Settings for your Signature",
            bg="#aedadb",
            font=("helvetica", 8, "normal"),
        )
        signature_lf.pack(
            fill=X,
            expand=False,
            pady=10,
            side="top",
        )
        sig_frame = Frame(signature_lf, bg="#aedadb")
        sig_frame.pack(fill=X, expand=True, side="top")
        Label(
            sig_frame,
            text="Your name:",
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).grid(row=0, column=0, padx=(0, 5))
        username_entry = Entry(
            master=sig_frame,
            textvariable=self._username,
            font=1,
        )
        username_entry.grid(
            row=0,
            column=1,
            columnspan=2,
            padx=(0, 7),
            ipadx=30,
            ipady=3,
        )
        Label(
            sig_frame,
            text="Signature image:",
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).grid(row=0, column=4, padx=(5, 5))
        self.sig_image_path_box = Text(
            sig_frame,
            background="#59f3e3",
            name="sig_image_path_file",
            height=4,
        )
        self.sig_image_path_box.grid(
            row=0,
            column=5,
            columnspan=2,
            rowspan=2,
            pady=(0, 1),
        )
        self.sig_image_path_box.drop_target_register(DND_FILES)
        self.sig_image_path_box.dnd_bind("<<Drop>>", presenter.process_attachments_path)
        self.sig_image_btn = Button(
            sig_frame,
            command=self._browse_sig_image,
            text="Browse",
        )
        self.sig_image_btn.grid(
            row=1,
            column=4,
            ipadx=35,
            ipady=8,
            pady=(2, 1),
        )

        future_settings_frame = Frame(
            content_boder,
            bg="#5F9EA0",
        )
        future_settings_frame.pack(
            fill=BOTH,
            expand=True,
            side="top",
        )
        buttons_frame = Frame(
            content_boder,
            bg="#5F9EA0",
        )
        buttons_frame.pack(
            fill=BOTH,
            expand=True,
            side="top",
        )
        left_btn_spacer = Frame(
            buttons_frame,
            bg="#5F9EA0",
        )
        left_btn_spacer.pack(
            fill=BOTH,
            expand=True,
            side="left",
        )
        Button(
            master=buttons_frame,
            text="Revert Back",
            bg="#ff0032",
            font=("helvetica", 12, "normal"),
            command=presenter.btn_revert_settings,
        ).pack(
            fill=BOTH,
            expand=True,
            side="left",
            padx=10,
            pady=10,
        )
        Button(
            master=buttons_frame,
            text="Save Settings",
            bg="#22c26a",
            font=("helvetica", 12, "normal"),
            command=presenter.btn_save_settings,
        ).pack(
            fill=BOTH,
            expand=True,
            side="left",
            padx=10,
            pady=10,
        )
        right_btn_spacer = Frame(
            buttons_frame,
            bg="#5F9EA0",
        )
        right_btn_spacer.pack(
            fill=BOTH,
            expand=True,
            side="left",
        )

    def create_quoteform_path_box(self, parent: Frame, presenter=Presenter) -> None:
        """Creates the drag-n-drop box for the quoteform."""
        self.quoteform_path_box = Text(
            parent, height=8, width=27, background="#59f3e3", name="raw_quoteform_path"
        )
        self.quoteform_path_box.drop_target_register(DND_FILES)
        self.quoteform_path_box.dnd_bind("<<Drop>>", presenter.process_quoteform_path)
        self.quoteform_path_box.pack(fill=X, anchor=N, expand=True)

    def create_extra_attachments_path_box(
        self, parent: Frame, presenter=Presenter
    ) -> None:
        """Creates the drag-n-drop box for any extra attachments."""
        self.extra_attachments_path_box = Text(
            parent,
            height=8,
            width=27,
            background="#59f3e3",
            name="raw_attachments_paths_list",
        )
        self.extra_attachments_path_box.pack(fill=X, expand=True, anchor=N)
        self.extra_attachments_path_box.drop_target_register(DND_FILES)
        self.extra_attachments_path_box.dnd_bind(
            "<<Drop>>", presenter.process_attachments_path
        )

    def create_dropdown(self, parent, presenter: Presenter) -> None:
        """Creates the OptionMenu widget separately for less coupling."""
        options = list()
        options = presenter.set_dropdown_options()
        dropdown_menu = OptionMenu(parent, self._dropdown_menu_var, *options)
        dropdown_menu.configure(
            background="#aedadb",
            foreground="black",
            highlightbackground="#5F9EA0",
            activebackground="#5F9EA0",
            font=("helvetica", 12, "normal"),
        )
        dropdown_menu["menu"].configure(background="#aedadb")
        dropdown_menu.pack(padx=15, ipady=5, fill=X, expand=True)

    def get_active_focus(self) -> dict:
        return self.focus_get()

    def _browse_sig_image(self):
        dir_name = filedialog.askdirectory()
        self.sig_image_file = dir_name
