import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Notebook, Style
from tkinter import *
from tkinterdnd2 import DND_FILES, TkinterDnD
from typing import Any, Callable, Protocol
from dataclasses import dataclass


class Presenter(Protocol):
    """This enables us to call funtions from the Presenter
    class, either to send/retrieve data.
    """

    def btn_send_envelopes(self, autosend: bool) -> None:
        ...

    def btn_view_template(self) -> None:
        ...

    def btn_clear_attachments(self) -> None:
        ...

    def btn_save_template(self) -> None:
        ...

    def btn_save_settings(self) -> None:
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

    def __init__(self, positive_value, negative_value) -> None:
        super().__init__()
        self.geometry("760x548")
        self.configure(background="#5F9EA0")
        self.title("Quick Submit Tool")
        self.attributes("-alpha", 0.95)
        self._username = tk.StringVar(name="username", value="")
        self._use_CC_defaults = BooleanVar(name="use_CC_defaults")
        self._yes = positive_value
        self._no = negative_value
        self._recipient = StringVar(name="recipient", value="")
        self._greeting = tk.StringVar(name="greeting", value="")
        self._salutation = StringVar(name="salutation", value="")
        self._default_CC1 = StringVar(name="default_CC1", value="")
        self._default_CC2 = StringVar(name="default_CC2", value="")
        self._seawave = StringVar(name="Seawave", value=self._no)
        self._primetime = StringVar(name="Prime Time", value=self._no)
        self._newhampshire = StringVar(name="New Hampshire", value=self._no)
        self._americanmodern = StringVar(
            name="American Modern", value=self._no)
        self._kemah = StringVar(name="Kemah Marine", value=self._no)
        self._concept = StringVar(name="Concept Special Risks", value=self._no)
        self._yachtinsure = StringVar(name="Yachtinsure", value=self._no)
        self._century = StringVar(name="Century", value=self._no)
        self._intact = StringVar(name="Intact", value=self._no)
        self._travelers = StringVar(name="Travelers", value=self._no)
        self.dropdown_menu_var = StringVar(
            value="Select Market(s)"
            # name='Current Selection'
        )

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
    def use_CC_defaults(self) -> bool:
        return self._use_CC_defaults.get()

    @use_CC_defaults.setter
    def use_CC_defaults(self, usage: bool) -> None:
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
    def selected_template(self) -> str:
        return self.dropdown_menu_var.get()

    @property
    def recipient(self) -> str:
        return self._recipient.get()

    @recipient.setter
    def recipient(self, new_recipient: str) -> None:
        print(new_recipient)
        self._recipient.set(new_recipient)

    @recipient.deleter
    def recipient(self) -> None:
        self._recipient.set("")

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

    @property
    def default_CC1(self) -> str:
        return self._default_CC1.get()

    @default_CC1.setter
    def default_CC1(self, new_default_CC: str) -> None:
        self._default_CC1.set(new_default_CC)

    @default_CC1.deleter
    def default_CC1(self) -> None:
        self._default_CC1.set("")

    @property
    def default_CC2(self) -> str:
        return self._default_CC2.get()

    @default_CC2.setter
    def default_CC2(self, new_default_CC: str) -> None:
        self._default_CC2.set(new_default_CC)

    @default_CC2.deleter
    def default_CC2(self) -> None:
        self._default_CC2.set("")

    @property
    def username(self) -> str:
        return self._username.get()

    @username.setter
    def username(self, new_username: str):
        self._username.set(new_username)

    @username.deleter
    def username(self) -> None:
        self._username.set("")

    # def assign_attributes(self, positive_value, negative_value) -> None:
    #     """Assigns tkinter-specific attributes so that the getters/
    #     setters work and other modules do not need to need tkinter."""

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
        self.tabControl.add(self.template_customization,
                            text="Customize Templates")
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
        frame_left.pack(padx=5, fill=Y, side="left",
                        expand=False, anchor=NE)
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
            command=lambda: presenter.btn_clear_attachments,
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
            labelframe_main1, height=7, width=30, name="raw_extra_notes"
        )
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
        self._userinput_CC2.pack(
            ipady=4, anchor=N, fill=X, expand=True, side="top")
        Button(
            frame_middle,
            text="View Each Before Sending!",
            bg="#22c26a",
            font=("helvetica", 12, "normal"),
            command=lambda: presenter.btn_send_envelopes(autosend=False),
        ).pack(ipady=20, ipadx=2, pady=10, anchor=S, fill=Y, expand=False)

        self.frame_right = Frame(self.home, bg="#5F9EA0")
        self.frame_right.pack(
            padx=5, fill=BOTH, side="left", expand=True, anchor=NW)
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
            command=lambda: presenter.btn_send_envelopes(autosend=True),
        ).pack(ipady=20, pady=10, anchor=S, fill=BOTH, expand=True)

    def create_customize_tab_widgets(self, presenter: Presenter):
        title_frame = Frame(self.template_customization, bg="#5F9EA0", height=17).pack(
            fill=X, expand=False
        )
        Label(
            title_frame,
            text="Customize Your Envelopes Here",
            bg="#5F9EA0",
            font=("helvetica", 16, "normal"),
        ).pack(fill=X, expand=True, side="top")
        Label(
            title_frame,
            text="Customize the contents/template for each carrier,  or combination of carriers.",
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(padx=4, pady=5, fill=BOTH, expand=True, side="left", anchor=E)

        template_select_frame = Frame(self.template_customization, bg="#5F9EA0").pack(
            padx=5, fill=BOTH, expand=True
        )
        Label(
            template_select_frame,
            text="""Select a scenario below 
                to customize its content/template.""",
            bg="#5F9EA0",
            font=("helvetica", 10, "normal"),
        ).pack(fill=X, expand=True)
        self.create_dropdown(parent=template_select_frame, presenter=presenter)
        self.dropdown_menu_var.trace_add("write", presenter.on_change_template)

        address_frame = Frame(self.template_customization, bg="#5F9EA0")
        address_frame.pack(fill=BOTH, expand=False, anchor=N)
        Label(
            address_frame,
            text="Submission Address:",
            bg="#aedadb",
            font=("helvetica", 16, "normal"),
        ).pack(padx=2, pady=15, fill=BOTH, expand=True, anchor=E, side="top")
        Entry(master=address_frame, textvariable=self._recipient).pack(
            padx=4, pady=15, ipadx=160, ipady=5, fill=BOTH, expand=False, side="top"
        ).bind("<FocusOut>", lambda: presenter.on_focus_out("recipient",
                                                            self.recipient)
               )
        greeting_frame = Frame(self.template_customization, bg="#5F9EA0")
        greeting_frame.pack(fill=BOTH, expand=False, anchor=N)
        Label(
            greeting_frame,
            text="Greeting:",
            bg="#aedadb",
            font=("helvetica", 16, "normal"),
        ).pack(padx=2, fill=BOTH, expand=True, anchor=E, side="top")
        Entry(master=greeting_frame, textvariable=self._greeting).pack(
            padx=4, pady=1, ipadx=160, ipady=5, fill=BOTH, expand=False, side="top"
        ).bind("<FocusOut>", lambda: presenter.on_focus_out("greeting", self.greeting))
        body_frame = Frame(self.template_customization, bg="#5F9EA0")
        body_frame.pack(fill=BOTH, expand=False, anchor=N)
        Label(
            body_frame,
            text="Body of the email:",
            bg="#aedadb",
            font=("helvetica", 16, "normal"),
        ).pack(padx=2, pady=15, fill=BOTH, expand=True, anchor=E, side="top")
        salutation_frame = Frame(self.template_customization, bg="#5F9EA0")
        salutation_frame.pack(fill=BOTH, expand=False, anchor=N)
        Label(
            salutation_frame,
            text="Salutation:",
            bg="#aedadb",
            font=("helvetica", 16, "normal"),
        ).pack(padx=2, pady=63, fill=BOTH, expand=True, anchor=E, side="top")

        buttons_frame = Frame(self.template_customization, bg="#5F9EA0")
        buttons_frame.pack(fill=BOTH, expand=True, anchor=N)

        self._body_text = Text(e_frame_bottomR, width=10, height=5)
        self._body_text.pack(
            padx=4, pady=15, ipadx=160, ipady=5, fill=BOTH, expand=False, side="top"
        )
        self._body_text.bind(
            "<FocusOut>", lambda: presenter.on_focus_out("body", self.body)
        )
        salutation_entry = Entry(
            e_frame_bottomR,
            textvariable=self._salutation,
            width=27,
            highlightbackground="green",
            highlightcolor="red",
        )
        salutation_entry.pack(
            padx=4, ipadx=160, ipady=5, fill=BOTH, expand=False, side="top"
        )
        salutation_entry.bind(
            "<FocusOut>", lambda: presenter.on_focus_out(
                "salutation", self.salutation)
        )
        Button(
            e_frame_bottomR,
            name="btnSaveTemplate",
            text="Click to SAVE the template",
            bg="#22c26a",
            command=presenter.btn_save_template,
        ).pack(padx=4, pady=20, ipady=50, fill=X, expand=False, anchor=S, side="bottom")
        Button(
            e_frame_bottomR,
            name="btnViewTemplate",
            text="Click to VIEW a sample message",
            bg="#22c26a",
            command=presenter.btn_view_template,
        ).pack(padx=4, pady=20, ipady=50, fill=X, expand=False, anchor=S, side="bottom")

    def create_settings_tab_widgets(self, presenter: Presenter):
        title_frame = Frame(master=self.settings, bg="#5F9EA0")
        title_frame.pack(fill=BOTH, expand=False, side="top")
        Label(
            title_frame,
            text="Settings Page",
            bg="#5F9EA0",
            font=("helvetica", 20, "normal"),
        ).pack(fill=BOTH, expand=False, side="top")
        Label(
            master=title_frame,
            text="Default CC Addresses",
            bg="#5F9EA0",
            font=("helvetica", 14, "normal"),
        ).pack(fill=X, expand=False, side="top")
        settings_CC_frame = Frame(master=self.settings, bg="#5F9EA0")
        settings_CC_frame.pack(fill=X, expand=False, side="top")
        Label(
            master=settings_CC_frame,
            text="Add first set of addresses to CC: ",
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(
            pady=3, ipady=2, padx=1, fill="none", expand=False, side="left", anchor=NW
        )
        cc1 = Entry(settings_CC_frame, textvariable=self._default_CC1)
        cc1.pack(pady=3, fill=X, ipadx=10, ipady=4,
                 expand=True, side="left", anchor=N)
        Label(
            settings_CC_frame,
            text="Add second set of addresses to CC: ",
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(
            pady=3, ipady=2, padx=1, fill="none", expand=False, side="left", anchor=NW
        )
        cc2 = Entry(settings_CC_frame, textvariable=self._default_CC2)
        cc2.pack(pady=3, fill=X, ipadx=10, ipady=4,
                 expand=True, side="left", anchor=N)
        settings_username_header_frame = Frame(
            master=self.settings, bg="#5F9EA0")
        settings_username_header_frame.pack(
            fill=BOTH, expand=False, side="top")
        settings_username_frame = Frame(master=self.settings, bg="#5F9EA0")
        settings_username_frame.pack(fill=BOTH, expand=False, side="top")
        Label(
            settings_username_frame,
            text="Your name",
            bg="#aedadb",
            font=("helvetica", 12, "normal"),
        ).pack(
            pady=3, ipady=2, padx=1, fill="none", expand=False, side="left", anchor=NW
        )
        username_entry = Entry(
            master=settings_username_frame, textvariable=self._username
        )
        username_entry.pack(
            ipadx=30, pady=5, fill=X, expand=True, side="right", anchor=NW
        )
        save_btn_frame = Frame(master=self.settings, bg="#5F9EA0")
        save_btn_frame.pack(fill=BOTH, expand=False, side="top")
        Button(
            master=save_btn_frame,
            text="Save Settings",
            bg="#22c26a",
            font=("helvetica", 12, "normal"),
            command=presenter.btn_save_settings,
        ).pack(
            ipady=10, pady=10, padx=10, fill=BOTH, expand=False, anchor=N, side="top"
        )

    def create_quoteform_path_box(self, parent: Frame, presenter=Presenter) -> None:
        """Creates the drag-n-drop box for the quoteform."""
        self.quoteform_path_box = Text(
            parent, height=8, width=27, background="#59f3e3", name="raw_quoteform_path"
        )
        self.quoteform_path_box.drop_target_register(DND_FILES)
        self.quoteform_path_box.dnd_bind(
            "<<Drop>>", presenter.process_quoteform_path)
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
        # Create functionality to show the paths of the files in box.

    def create_dropdown(self, parent, presenter: Presenter) -> None:
        """Creates the OptionMenu widget separately for less coupling."""
        options = list()
        options = presenter.set_dropdown_options()
        dropdown_menu = OptionMenu(parent, self.dropdown_menu_var, *options)
        dropdown_menu.configure(
            background="#aedadb",
            foreground="black",
            highlightbackground="#5F9EA0",
            activebackground="#5F9EA0",
        )
        dropdown_menu["menu"].configure(background="#aedadb")
        dropdown_menu.pack(padx=15, ipady=5, fill=X, expand=True)
