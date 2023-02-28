import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Notebook, Style
from tkinter import *
from tkinterdnd2 import *
from typing import Any, Callable, Protocol


class Presenter(Protocol):
    """ This enables us to call funtions from the Presenter class,  either to send/retrieve data.
    NOTE: finished functions are at top, revised underneath,  and the outdated are at the bottom with Pass instead of elipses.
    """

    def btn_send_envelopes(self, view: bool) -> None:
        ...

    def btn_save_template():
        ...

    def btn_save_settings(self) -> None:
        ...

    def set_dropdown_options() -> list:
        ...

    def process_attachments_path(self, raw_path) -> None:
        ...

    def process_quoteform_path(self, raw_path) -> None:
        ...

    def update_dropdown(self):
        ...

    def save_extra_notes(self, notes: str) -> None:  # GOOD
        ...

    def saveCC():
        ...

    def update_template_tab_on_changed_dropdown(self) -> None:
        ...

    def insert_placeholders():
        pass

    def delete_placeholders():
        pass


class TkView(tk.Tk):
    """ This class uses tkinter to create a view object when instantiated by the main_script.  After __init__,  there's a parent method, create_GUI_obj, responsivle for creating the widgets.  These sub-functions are divided by page/tab. Lastly, there are methods to allow data retrieval and updating.
    class attr positive_submission is for setting the value for a submission to be processed and sent. This is the one spot it needs updating. 
    """

    def __init__(self) -> None:
        super().__init__()
        self.geometry('760x548')
        self.configure(background='#5F9EA0')
        self.title('Quick Submit Tool')
        self.attributes('-alpha', 0.95)
        self._positive_submission = 'submit'
        self._negative_submission = 'skip'
        self.options = list()
        self._seawave = StringVar(
            name='Seawave', value=self._negative_submission)
        self._primetime = StringVar(
            name='Prime Time', value=self._negative_submission)
        self._newhampshire = StringVar(
            name='New Hampshire', value=self._negative_submission)
        self._americanmodern = StringVar(
            name='American Modern', value=self._negative_submission)
        self._kemah = StringVar(name='Kemah Marine',
                                value=self._negative_submission)
        self._concept = StringVar(
            name='Concept Special Risks', value=self._negative_submission)
        self._yachtinsure = StringVar(
            name='Yachtinsure', value=self._negative_submission)
        self._century = StringVar(
            name='Century', value=self._negative_submission)
        self._intact = StringVar(
            name='Intact', value=self._negative_submission)
        self._travelers = StringVar(
            name='Travelers', value=self._negative_submission)
        self._recipient = None
        self._greeting = None
        self._body = None
        self._salutation = None

    def create_GUI_obj(self, presenter: Presenter):
        """ This creates the GUI root,  along with the main
        functions to create the widgets.
        """
        self.cc_default_check = BooleanVar  # Is this okay/preferred way to store this?
        self.create_style()
        self.create_notebook()
        self.create_tabs()
        self.create_main_tab_widgets(presenter)
        self.create_customize_tab_widgets(presenter)
        self.create_settings_tab_widgets(presenter)
        # self.set_initial_placeholders()

    def create_style(self):
        self.style = Style(master=self)
        self.style.theme_use('default')
        self.style.configure('TNotebook', background='#5F9EA0')
        self.style.configure('TFrame', background='#5F9EA0')
        self.style.map('TNotebook', background=[('selected', '#5F9EA0')])

    def create_notebook(self):
        self.tabControl = ttk.Notebook(master=self)
        self.tabControl.pack(pady=0, expand=True)

    def create_tabs(self):
        self.home = ttk.Frame(self.tabControl)
        self.template_settings = ttk.Frame(self.tabControl)
        self.settings = ttk.Frame(self.tabControl)
        self.tabControl.add(self.home, text='Main - Setup Envelopes')
        self.tabControl.add(self.template_settings, text='Customize')
        self.tabControl.add(self.settings, text='Settings')

    def create_main_tab_widgets(self, presenter: Presenter):
        # Add the frames to the tab
        frame_header = Frame(self.home, bg='#5F9EA0', pady=17)
        frame_header.pack(padx=5, fill=X, expand=False)

        frame_left = Frame(self.home, bg='#5F9EA0')
        frame_left.pack(padx=5, fill=Y, side='left', expand=False, anchor=NE)

        frame_middle = Frame(self.home, bg='#5F9EA0')
        frame_middle.pack(padx=5, fill=Y, side='left', expand=False, anchor=N)

        self.frame_right = Frame(self.home, bg='#5F9EA0')
        self.frame_right.pack(padx=5, fill=Y, side='left',
                              expand=False, anchor=NW)

        # Create widgets inside Frame Header
        Label(frame_header, text='Get Client Information', bg='#5F9EA0', font=(
            'helvetica', 20, 'normal')).pack(fill=X, expand=True, side='left')
        Label(frame_header, text='Extra Notes & CC', bg='#5F9EA0', font=(
            'helvetica', 20, 'normal')).pack(fill=X, expand=True, side='left')
        Label(frame_header, text='Choose Markets:', bg='#5F9EA0', font=(
            'helvetica', 20, 'normal')).pack(fill=X, expand=True, side='left')

        # Create widgets inside Frame Left
        Label(frame_left, text='Dag-N-Drop Quoteform Below', bg='#aedadb',
              font=('helvetica', 12, 'normal')).pack(fill=BOTH, expand=True)

        self.create_quoteform_path_box(frame_left, presenter)

        Label(frame_left, text='Dag-N-Drop Extra Attachments Below', bg='#aedadb',
              font=('helvetica', 12, 'normal')).pack(fill=BOTH, expand=True)

        self.create_extra_attachments_path_box(frame_left, presenter)

        # Create widgets inside Frame Middle
        # this is a label_frame
        extra_notes_labelframe = LabelFrame(frame_middle,
                                            text='To end with a message, enter it below:', bg='#aedadb',
                                            font=('helvetica', 8, 'normal')
                                            )
        extra_notes_labelframe.pack(fill=X, expand=False, side='top')

        self.extra_notes_text = Text(
            extra_notes_labelframe, height=7, width=30, name='raw_extra_notes')
        self.extra_notes_text.pack(fill=X, anchor=N, expand=FALSE, side='top')
        # end of label_frame

        # this is a label_frame
        cc_labelframe = LabelFrame(frame_middle,
                                   text='CC-address settings for this submission:', bg='#aedadb', name='cc_labelframe'
                                   )
        cc_labelframe.pack(fill=X, expand=True, side='top')

        Label(cc_labelframe, text='email address to CC:', bg='#aedadb', font=(
            'helvetica', 12, 'normal')).pack(fill=X, expand=True, side='top')

        self.ignore_CC_defaults = BooleanVar(name='ignore_CC_defaults')
        ignore_CC_defaults = Checkbutton(cc_labelframe, text='Check to ignore default CC-addresses.', variable=self.ignore_CC_defaults,
                                         bg='#aedadb', name='cc_def_chcek', onvalue=True, offvalue=False).pack(pady=5, fill=X, expand=False, side='top')

        self.userinput_CC1 = Text(cc_labelframe, height=1, width=30)
        self.userinput_CC1.pack(pady=2, ipady=4, anchor=N,
                                fill=X, expand=True, side='top')

        Label(cc_labelframe, text='email address to CC:', bg='#aedadb', font=(
            'helvetica', 12, 'normal')).pack(fill=X, expand=True, side='top')

        self.userinput_CC2 = Text(cc_labelframe, height=1, width=30)
        self.userinput_CC2.pack(
            ipady=4, anchor=N, fill=X, expand=True, side='top')

        Button(frame_middle, text='Display & View Each Envelope!', bg='#22c26a', font=('helvetica', 12, 'normal'),
               command=presenter.btn_send_envelopes(view=True)).pack(ipady=20, pady=10, anchor=S, fill=Y, expand=False)
        # end of label_frame

        # Create checkboxes and StringVars

        seawave_checkbox = Checkbutton(master=self.frame_right, name='seawave', text='Seawave', variable=self._seawave,
                                       onvalue=self._positive_submission, offvalue=self._negative_submission, bg='#aedadb', font=('helvetica', 12, 'normal'))
        seawave_checkbox.pack(ipady=3, fill=BOTH, expand=True)

        primetime_checkbox = Checkbutton(master=self.frame_right, name='prime time', text='Prime Time', variable=self._primetime,
                                         onvalue=self._positive_submission, offvalue=self._negative_submission, bg='#aedadb', font=('helvetica', 12, 'normal'))
        primetime_checkbox.pack(ipady=3, fill=BOTH, expand=True)

        newhampshire_checkbox = Checkbutton(master=self.frame_right, name='newhampshire', text='New Hampshire', variable=self._newhampshire,
                                            onvalue=self._positive_submission, offvalue=self._negative_submission, bg='#aedadb', font=('helvetica', 12, 'normal'))
        newhampshire_checkbox.pack(ipady=3, fill=BOTH, expand=True)

        americanmodern_checkbox = Checkbutton(master=self.frame_right, name='americanmodern', text='American Modern', variable=self._americanmodern,
                                              onvalue=self._positive_submission, offvalue=self._negative_submission, bg='#aedadb', font=('helvetica', 12, 'normal'))
        americanmodern_checkbox.pack(ipady=3, fill=BOTH, expand=True)

        kemah_checkbox = Checkbutton(master=self.frame_right, name='kemah', text='Kemah Marine', variable=self._kemah,
                                     onvalue=self._positive_submission, offvalue=self._negative_submission, bg='#aedadb', font=('helvetica', 12, 'normal'))
        kemah_checkbox.pack(ipady=3, fill=BOTH, expand=True)

        concept_checkbox = Checkbutton(master=self.frame_right, name='concept', text='Concept', variable=self._concept,
                                       onvalue=self._positive_submission, offvalue=self._negative_submission, bg='#aedadb', font=('helvetica', 12, 'normal'))
        concept_checkbox.pack(ipady=3, fill=BOTH, expand=True)

        yachtinsure_checkbox = Checkbutton(master=self.frame_right, name='yachtinsure', text='Yacht Insure', variable=self._yachtinsure,
                                           onvalue=self._positive_submission, offvalue=self._negative_submission, bg='#aedadb', font=('helvetica', 12, 'normal'))
        yachtinsure_checkbox.pack(ipady=3, fill=BOTH, expand=True)

        century_checkbox = Checkbutton(master=self.frame_right, name='century', text='Century', variable=self._century,
                                       onvalue=self._positive_submission, offvalue=self._negative_submission, bg='#aedadb', font=('helvetica', 12, 'normal'))
        century_checkbox.pack(ipady=3, fill=BOTH, expand=True)

        intact_checkbox = Checkbutton(master=self.frame_right, name='intact', text='Intact', variable=self._intact,
                                      onvalue=self._positive_submission, offvalue=self._negative_submission, bg='#aedadb', font=('helvetica', 12, 'normal'))
        intact_checkbox.pack(ipady=3, fill=BOTH, expand=True)

        travelers_checkbox = Checkbutton(master=self.frame_right, name='travelers', text='Travelers', variable=self._travelers,
                                         onvalue=self._positive_submission, offvalue=self._negative_submission, bg='#aedadb', font=('helvetica', 12, 'normal'))
        travelers_checkbox.pack(ipady=3, fill=BOTH, expand=True)
        Button(self.frame_right, text='Submit & auto-send to markets!', bg='#22c26a', font=('helvetica', 12, 'normal'),
               command=presenter.btn_send_envelopes(False)).pack(ipady=20, pady=10, anchor=S, fill=BOTH, expand=True)
        # End of creating the MAIN tab.

    def create_customize_tab_widgets(self, presenter: Presenter):
        # Add the frames to tab
        e_frame_header_spacer = Frame(
            self.template_settings, bg='#5F9EA0', height=17)
        e_frame_header_spacer.pack(fill=X, expand=False)
        e_frame_header = Frame(self.template_settings, bg='#5F9EA0')
        e_frame_header.pack(padx=5, fill=X, expand=True)
        e_frame_top = Frame(self.template_settings, bg='#5F9EA0')
        e_frame_top.pack(fill=BOTH, expand=False)
        e_frame_content = Frame(self.template_settings, bg='#5F9EA0')
        e_frame_content.pack(fill=BOTH, expand=False, anchor=N)
        e_frame_bottomL = Frame(self.template_settings, bg='#5F9EA0')
        e_frame_bottomL.pack(fill=X, expand=True, side='left', anchor=N)
        e_frame_bottomR = Frame(self.template_settings, bg='#5F9EA0')
        e_frame_bottomR.pack(fill=X, expand=True, side='left', anchor=N)

        # Crfeate widgets for the Header Frame
        Label(e_frame_header, text='Customize Your Envelopes Here', bg='#5F9EA0', font=(
            'helvetica', 16, 'normal')).pack(fill=X, expand=True, side='top')
        Label(e_frame_header, text='Customize the contents/template for each carrier,  or combination of carriers.',
              bg='#aedadb', font=('helvetica', 12, 'normal')).pack(padx=4, pady=5, fill=BOTH, expand=True, side='left', anchor=E)

        # username used to go here

        # End of Header
        # Create widgets for the Top Frame
        Label(e_frame_top, text="Select a scenario below to customize its content/template.",
              bg='#5F9EA0', font=('helvetica', 10, 'normal')).pack(fill=X, expand=True)
        self.create_dropdown_variable(
            initial_value='Select Market(s)', name='Current Selection', presenter=presenter)
        self.create_dropdown(parent=e_frame_top, presenter=presenter)
        # End of Top Frame
        # Create widgets for the Bottom Left Frames
        Label(e_frame_bottomL, text='Submission Address:', bg='#aedadb', font=(
            'helvetica', 16, 'normal')).pack(padx=2, pady=15, fill=BOTH, expand=True, anchor=E, side='top')
        Label(e_frame_bottomL, text='Greeting:', bg='#aedadb', font=(
            'helvetica', 16, 'normal')).pack(padx=2, fill=BOTH, expand=True, anchor=E, side='top')
        Label(e_frame_bottomL, text='Body of the email:', bg='#aedadb', font=(
            'helvetica', 16, 'normal')).pack(padx=2, pady=15, fill=BOTH, expand=True, anchor=E, side='top')
        Label(e_frame_bottomL, text='Salutation:', bg='#aedadb', font=('helvetica', 16, 'normal')).pack(
            padx=2, pady=63, fill=BOTH, expand=True, anchor=E, side='top')
        # Create widgets for the Bottom Right Frames
        # TO CREATE THE FUNCTIONS TO REPLACE THE LAMDA functions in bindings.
        self._recipient = StringVar(master=e_frame_bottomR, name='recipient')
        self.recipient_entry = Entry(
            master=e_frame_bottomR, textvariable=self._recipient)
        self.recipient_entry.pack(
            padx=4, pady=15, ipadx=160, ipady=5, fill=BOTH, expand=False, side='top')
        self.recipient_entry_focus_out = self.recipient_entry.bind(
            '<FocusOut>', self.on_focus_out)
        self._greeting = StringVar(master=e_frame_bottomR, name='greeting')
        self.greeting_entry = Entry(
            master=e_frame_bottomR, textvariable=self._greeting)
        self.greeting_entry.pack(
            padx=4, pady=1, ipadx=160, ipady=5, fill=BOTH, expand=False, side='top')
        self.greeting_entry_focus_out = self.greeting_entry.bind(
            '<FocusOut>', self.on_focus_out)
        self._body_text = Text(e_frame_bottomR, width=10, height=5)
        self._body_text.pack(padx=4, pady=15, ipadx=160,
                             ipady=5, fill=BOTH, expand=False, side='top')
        self.body_entry_focus_out = self._body_text.bind(
            '<FocusOut>', self.on_focus_out)
        self._salutation = StringVar(master=e_frame_bottomR, name='salutation')
        self.salutation_entry = Entry(e_frame_bottomR, textvariable=self._salutation,
                                      width=27, highlightbackground='green', highlightcolor='red')
        self.salutation_entry.pack(
            padx=4, ipadx=160, ipady=5, fill=BOTH, expand=False, side='top')
        self.salutation_entry_focus_out = self.salutation_entry.bind(
            '<FocusOut>', self.on_focus_out)

        Button(e_frame_bottomR, name='btnSaveTemplate', text='Click to SAVE template for this market, & save your name!', bg='#22c26a',
               command=presenter.btn_save_template).pack(padx=4, pady=20, ipady=50, fill=X, expand=False, anchor=S, side='bottom')

    def create_settings_tab_widgets(self, presenter: Presenter):
        # Header
        Label(self.settings, text='Settings Page', bg='#5F9EA0', font=(
            'helvetica', 20, 'normal')).pack(fill=BOTH, expand=False, side='top')
        # Create frames for the tab
        entry_boxes_frame = Frame(master=self.settings, bg='#5F9EA0')
        entry_boxes_frame.pack(fill=BOTH, expand=False, side='top')
        save_btn_frame = Frame(master=self.settings, bg='#5F9EA0')
        save_btn_frame.pack(fill=BOTH, expand=False, side='top')
        # Content
        Label(master=entry_boxes_frame, text='CC-Addresses & Settings', bg='#5F9EA0',
              font=('helvetica', 14, 'normal')).pack(fill=X, expand=False, side='top')
        Label(master=entry_boxes_frame, text='1st address to set as default cc: ', bg='#aedadb', font=(
            'helvetica', 12, 'normal')).pack(pady=3, ipady=2, padx=1, fill='none', expand=False, side='left', anchor=NW)
        self._default_CC1 = StringVar(
            master=entry_boxes_frame, name='default_CC1')
        self.default_CC1_entry = Entry(
            entry_boxes_frame, textvariable=self.default_CC1)
        self.default_CC1_entry.pack(
            pady=3, fill=X, ipadx=10, ipady=4, expand=True, side='left', anchor=N)
        Label(entry_boxes_frame, text='2nd address to set as default cc: ', bg='#aedadb', font=(
            'helvetica', 12, 'normal')).pack(pady=3, ipady=2, padx=1, fill='none', expand=False, side='left', anchor=NW)
        self._default_CC2 = StringVar(
            master=entry_boxes_frame, name='default_CC2')
        self.default_CC2_entry = Entry(
            entry_boxes_frame, textvariable=self.default_CC2)
        self.default_CC2_entry.pack(
            pady=3, fill=X, ipadx=10, ipady=4, expand=True, side='left', anchor=N)

        self._username = StringVar(
            master=self.settings, value='Default', name='username')
        self.username_entry = Entry(
            master=self.settings, textvariable=self._username)
        self.username_entry.pack(
            ipadx=900, pady=5, fill=BOTH, expand=True, side='right', anchor=NW)
        self.your_name_focus_out = self.username_entry.bind(
            '<FocusOut>', self.on_focus_out(self.username))

        Button(master=save_btn_frame, text='Save Settings!', bg='#22c26a', font=('helvetica', 12, 'normal'),
               command=presenter.btn_save_settings).pack(ipady=10, pady=10, padx=10, fill=BOTH, expand=False, anchor=N, side='top')

    def create_quoteform_path_box(self, parent: Frame, presenter=Presenter) -> None:
        """ Creates the drag-n-drop box for the quoteform."""
        self.quoteform_path_box = Text(
            parent,
            height=7,
            width=27,
            background='#59f3e3',
            name='raw_quoteform_path'
        )
        self.quoteform_path_box.pack(fill=BOTH, anchor=N, expand=True)
        self.quoteform_path_box.drop_target_register(DND_FILES)
        self.quoteform_path_box.dnd_bind(
            '<<Drop>>', presenter.process_quoteform_path)

    def create_extra_attachments_path_box(self, parent: Frame, presenter=Presenter) -> None:
        """ Creates the drag-n-drop box for any extra attachments."""
        self.extra_attachments_path_box = Text(
            parent,
            height=9,
            width=27,
            background='#59f3e3',
            name='raw_list_of_attachments_paths'
        )
        self.extra_attachments_path_box.pack(fill=X, expand=True, anchor=N)
        self.extra_attachments_path_box.drop_target_register(DND_FILES)
        self.extra_attachments_path_box.dnd_bind(
            '<<Drop>>', presenter.process_attachments_path)
        # Create functionality to show the paths of the files in box.

    def create_dropdown_variable(self, initial_value: str, name: str, presenter: Presenter) -> None:
        """ Creates the variable used to identify the current selection and assigns/updates a different variable with current choice.
        """
        self.dropdown_menu_var = StringVar(value=initial_value, name=name)
        self.dropdown_menu_var.trace_add(
            'write', presenter.update_template_tab_on_changed_dropdown)

    def create_dropdown(self, parent, presenter: Presenter) -> None:
        """ Creates the OptionMenu widget separately for less coupling."""
        options = list()
        options = presenter.set_dropdown_options()
        print(options)
        dropdown_menu = OptionMenu(parent, self.dropdown_menu_var, *options)
        dropdown_menu.configure(background='#aedadb',
                                foreground='black', highlightbackground='#5F9EA0', activebackground='#5F9EA0'
                                )
        dropdown_menu['menu'].configure(background='#aedadb')
        dropdown_menu.pack(padx=15, ipady=5, fill=X, expand=True)

    def on_focus_out(self, item) -> None:  # START & FINISH
        """ NOTE: THIS IS NOT AN IMPORTANT FUNCTION TO IMPLEMENT. This function performs actions on them to increase user UI experience.  NOTE:  This originally was a very lame function that repopulated specific fields if they were modified & subsequently left empty upon leaving focus---WOW...
        Instead,  this will also change text (foreground) color if it's changed."""
        print(item)
        # self.item.

    @property
    def positive_submission_value(self):
        return self._positive_submission

    @property
    def negative_submission_value(self):
        return self._negative_submission

    @property
    def extra_notes(self) -> str:
        return self.extra_notes_text.get()

    @extra_notes.deleter
    def extra_notes(self):
        del self.extra_notes_text

    def userinput_CC1(self) -> str:
        return self.userinput_CC1.get('1.0', 'end-1c')

    def userinput_CC2(self) -> str:
        return self.userinput_CC2.get('1.0', 'end-1c')

    @property
    def ignore_default_cc(self) -> bool:
        return self.ignore_CC_defaults.get()

    @ignore_default_cc.setter
    def ignore_default_cc(self, ignore_is_True: bool) -> None:
        self.ignore_CC_defaults = ignore_is_True

    # These are getters for the checkbuttons

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
        self._recipient = new_recipient

    @recipient.deleter
    def recipient(self) -> None:
        del self._recipient

    @property
    def greeting(self) -> str:
        return self._greeting.get()

    @greeting.setter
    def greeting(self, new_greeting: str) -> None:
        self._greeting = new_greeting

    @greeting.deleter
    def greeting(self) -> None:
        del self._greeting

    @property
    def body(self) -> str:
        return self._body.get()

    @body.setter
    def body(self, new_body: str) -> None:
        self._body = new_body

    @body.deleter
    def body(self) -> None:
        del self._body

    @property
    def salutation(self) -> str:
        return self._salutation.get()

    @salutation.setter
    def salutation(self, new_salutation: str) -> None:
        self._salutation = new_salutation

    @salutation.deleter
    def salutation(self) -> None:
        del self._salutation

    @property
    def default_CC1(self) -> str:
        return self._default_CC1.get()

    @default_CC1.setter
    def default_CC1(self, new_default_CC: str) -> None:
        self._default_CC1 = new_default_CC

    @property
    def default_CC2(self) -> str:
        return self._default_CC2.get()

    @default_CC2.setter
    def default_CC2(self, new_default_CC: str) -> None:
        self._default_CC2 = new_default_CC

    @property
    def username(self) -> str:
        return self._username.get()

    @username.setter
    def username(self, new_username: str):
        self._username = new_username

    @username.deleter
    def username(self) -> None:
        del self._username

    # Make these below FNs loop to accomodate multiple requests at once ;)
    # def assign_placeholder(self, name_of_widget, placeholder: str):
    #     pass
    # def get_placeholder(self, item):
    #     pass
    # def insert_placeholder(self, item, indx, placeholder: str):
    #     item.insert(indx, placeholder)
    # def delete_placeholder(self, item, indx):
    #     self.item.delete(indx, 'end')
    # def enableField(self, item, wrap):
    #     item.configure(state='normal')
    # def disableField(self, item):
    #     item.configure(state='disabled')
# End of needing loop section :)

    # def start_program(self) -> None:
    #     self.create_GUI_obj()

# app = TkView()
