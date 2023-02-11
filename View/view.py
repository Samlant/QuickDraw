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
    def get_drop_down_options(self) -> list:
        ...
    def save_path(self, event, is_quoteform: bool) -> None:#GOOD
        ...
    def btnSaveMainSettings(self):
        ...

    def update_dropdown(self):
        ...
    def btnSaveEmailTemplate():
        ...
    def save_extra_notes(self, notes: str) -> None:#GOOD
        ...
    def saveCC():
        ...

    def insert_placeholders():
        pass
    def delete_placeholders():
        pass
    


class TkView(tk.Tk):
    """ This class uses tkinter to create a view object when instantiated by the main_script.  After __init__,  there's a parent method, create_GUI_obj, responsivle for creating the widgets.  These sub-functions are divided by page/tab. Lastly, there are methods to allow data retrieval and updating.
    class attr positive_submission is for setting the value for a submission to be processed and sent. This is the one spot it needs updating. 
    """

    self.positive_submission = 'submit'


    def __init__(self) -> None:
        super().__init__()
        self.geometry('760x548')
        self.configure(background='#5F9EA0')
        self.title('Quick Submit Tool')
        self.attributes('-alpha',0.95)


    def create_GUI_obj(self, presenter: Presenter):
        """ This creates the GUI root,  along with the main
        functions to create the widgets.
        """

        self.cc_default_check = BooleanVar #Is this okay/preferred way to store this?

        self.createStyle()
        self.createNotebook()
        self.createTabs()
        self.createMainTabWidgets()
        self.createTemplateSettingsTabWidgets()
        self.createSettingsTabWidgets()
        #self.set_initial_placeholders()
    
    def createStyle(self):
        self.style = Style()
        self.style.theme_use('default')
        self.style.configure('TNotebook', background='#5F9EA0')
        self.style.configure('TFrame', background='#5F9EA0')
        self.style.map('TNotebook', background= [('selected', '#5F9EA0')])

    def createNotebook(self):
        self.tabControl = ttk.Notebook(self.root, style=self.style)

    def createTabs(self):
        self.home = ttk.Frame(self.tabControl)
        self.template_settings = ttk.Frame(self.tabControl)
        self.settings = ttk.Frame(self.tabControl)
        self.tabControl.add(self.home, text='Main')
        self.tabControl.add(self.template_settings, text='Templates')
        self.tabControl.add(self.settings, text='Settings')
        
    def createMainTabWidgets(self):
        # Add the frames to the tab
        frame_header = Frame(self.home, bg='#5F9EA0', pady=17)
        frame_header.pack(padx=5, fill=X, expand=False)

        frame_left = Frame(self.home, bg='#5F9EA0')
        frame_left.pack(padx=5, fill = Y, side='left', expand = False, anchor=NE)

        frame_middle = Frame(self.home, bg='#5F9EA0')
        frame_middle.pack(padx=5, fill = Y, side='left', expand = False, anchor=N)

        frame_right = Frame(self.home, bg='#5F9EA0')
        frame_right.pack(padx=5, fill = Y, side='left', expand = False, anchor=NW)

        # Create widgets inside Frame Header
        Label(frame_header, text='Get Client Information', bg='#5F9EA0', font=('helvetica', 20, 'normal')).pack(fill=X, expand=True, side='left')
        Label(frame_header, text='Extra Notes & CC', bg='#5F9EA0', font=('helvetica', 20, 'normal')).pack(fill=X, expand=True, side='left')
        Label(frame_header, text='Choose Markets:', bg='#5F9EA0', font=('helvetica', 20, 'normal')).pack(fill=X, expand=True, side='left')

        # Create widgets inside Frame Left
        Label(frame_left, text='Dag-N-Drop Quoteform Below', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(fill=BOTH, expand=True)

        self.create_quoteform_path_box(frame_left)

        Label(frame_left, text='Dag-N-Drop Extra Attachments Below', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(fill=BOTH, expand=True)

        self.create_extra_attachments_path_box(frame_left)

        # Create widgets inside Frame Middle
        # this is a label_frame
        extra_notes_labelframe = LabelFrame(frame_middle,
                                            text= 'To end with a message, enter it below:', bg='#aedadb', 
                                            font=('helvetica', 8, 'normal')
                                            )
        extra_notes_labelframe.pack(fill=X, expand=False, side='top')

        self.extra_notes_text = Text(extra_notes_labelframe, height=7, width=30, name='raw_extra_notes')
        self.extra_notes_text.pack(fill = X, anchor=N, expand=FALSE, side='top')
        # end of label_frame

        # this is a label_frame
        cc_labelframe = LabelFrame(frame_middle,
                                   text= 'CC-address settings for this submission:', bg='#aedadb', name='cc_labelframe'
                                   )
        cc_labelframe.pack(fill=X, expand=True, side='top')


        Label(cc_labelframe, text='email address to CC:', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(fill=X, expand=True, side='top')

        self.ignore_CC_defaults = BooleanVar(name='ignore_CC_defaults')
        ignore_CC_defaults = Checkbutton(cc_labelframe, text='Check to ignore default CC-addresses.', variable=self.cc_default_check, bg='#aedadb', name='cc_def_chcek', onvalue=True, offvalue=False).pack(pady=5, fill=X, expand=False, side='top')

        self.userinput_CC1 = Text(cc_labelframe, height=1, width=30)
        self.userinput_CC1.pack(pady=2, ipady=4, anchor=N, fill = X, expand=True, side='top')

        Label(cc_labelframe, text='email address to CC:', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(fill=X, expand=True, side='top')

        self.userinput_CC2 = Text(cc_labelframe, height=1, width=30)
        self.userinput_CC2.pack(ipady=4, anchor=N, fill = X, expand=True, side='top')
        # end of label_frame

        # Create checkboxes and StringVars
        self.seawave = StringVar(name='Seawave', value='skip')
        self.create_carrier_checkboxes('Seawave Insurance', self.seawave)
        self.primetime = StringVar(name='Prime Time', value='skip')
        self.create_carrier_checkboxes('Seawave Insurance', self.seawave)        
        self.newhampshire = StringVar(name='New Hampshire', value='skip')
        self.create_carrier_checkboxes('New Hampshire', self.newhampshire)   
        self.americanmodern = StringVar(name='American Modern', value='skip')
        self.create_carrier_checkboxes('American Modern', self.americanmodern)   
        self.kemah = StringVar(name='Kemah Marine', value='skip')
        self.create_carrier_checkboxes('Kemah Marine', self.kemah)
        self.concept = StringVar(name='Concept Special Risks', value='skip')
        self.create_carrier_checkboxes('Concept Special Risks', self.concept)
        self.yachtinsure = StringVar(name='Yachtinsure', value='skip')
        self.create_carrier_checkboxes('Yachtinsure', self.yachtinsure)
        self.century = StringVar(name='Century', value='skip')
        self.create_carrier_checkboxes('Century', self.century)
        self.intact = StringVar(name='Intact', value='skip')
        self.create_carrier_checkboxes('Intact', self.intact)
        self.travelers = StringVar(name='Travelers', value='skip')
        self.create_carrier_checkboxes('Travelers', self.travelers)
        Button(frame_right, text='Submit and sent to markets!', bg='#22c26a', font=('helvetica', 12, 'normal'), command=Presenter.btnSendEmail).pack(ipady=20, pady=10, anchor=S, fill=BOTH, expand=True)
        # End of creating the MAIN tab.

    def createTemplateSettingsTabWidgets(self):
        # Add the frames to tab
        e_frame_header_spacer = Frame(self.template_settings, bg='#5F9EA0', height=17)
        e_frame_header_spacer.pack(fill=X, expand=False)
        e_frame_header = Frame(self.template_settings, bg='#5F9EA0')
        e_frame_header.pack(padx=5, fill = X, expand=True)
        e_frame_top = Frame(self.template_settings, bg='#5F9EA0')
        e_frame_top.pack(fill=BOTH, expand=False)
        e_frame_content = Frame(self.template_settings, bg='#5F9EA0')
        e_frame_content.pack(fill=BOTH, expand=False, anchor=N)
        e_frame_bottomL = Frame(self.template_settings, bg='#5F9EA0' )
        e_frame_bottomL.pack(fill=X, expand=True, side='left', anchor=N)
        e_frame_bottomR = Frame(self.template_settings, bg='#5F9EA0')
        e_frame_bottomR.pack(fill=X, expand=True, side='left', anchor=N)
        
        # Crfeate widgets for the Header Frame
        Label(e_frame_header, text = 'Adjust the Default Email Templates for Each Carrier', bg='#5F9EA0', font=('helvetica', 16, 'normal')).pack(fill = X, expand=True, side='top')
        Label(e_frame_header, text = 'Your name (used in Signature):', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(padx=4, pady=5, fill=BOTH, expand=True, side='left', anchor=E)

        self.username = StringVar(master=e_frame_header, name='username')
        self.username_entry = Entry(master=e_frame_header, textvariable=self.username)
        self.username_entry.pack(ipadx=900, pady=5, fill=BOTH, expand=True, side='right', anchor=NW)
        self.your_name_focus_out = self.username_entry.bind('<FocusOut>', self.on_focus_out(self.username))
        # End of Header
        # Create widgets for the Top Frame
        Label(e_frame_top, text = "This drop-down menu allows you to view & edit a specific carrier's, or combo carriers', email message contents.", bg='#5F9EA0', font=('helvetica', 10, 'normal')).pack(fill = X, expand=True)
        self.create_dropdown_variable()
        self.create_dropdown(e_frame_top)
        # End of Top Frame
        # Create widgets for the Bottom Left Frames
        Label(e_frame_bottomL, text = 'Submission Address:', bg='#aedadb', font=('helvetica', 16, 'normal')).pack(padx=2, pady=15, fill=BOTH, expand=True, anchor=E, side='top')
        Label(e_frame_bottomL, text = 'Greeting:', bg='#aedadb', font=('helvetica', 16, 'normal')).pack(padx=2, fill=BOTH, expand=True, anchor=E, side='top')
        Label(e_frame_bottomL, text = 'Body of the email:', bg='#aedadb', font=('helvetica', 16, 'normal')).pack(padx=2, pady=15, fill=BOTH, expand=True, anchor=E, side='top')
        Label(e_frame_bottomL, text = 'Salutation:', bg='#aedadb', font=('helvetica', 16, 'normal')).pack(padx=2, pady=63, fill=BOTH, expand=True, anchor=E, side='top')
        # Create widgets for the Bottom Right Frames
        #TO CREATE THE FUNCTIONS TO REPLACE THE LAMDA functions in bindings.
        self.recipient = StringVar(master=e_frame_bottomR, name='recipient')
        self.recipient_entry = Entry(master=e_frame_bottomR, textvariable=self.recipient)
        self.recipient_entry.pack(padx=4, pady=15, ipadx=160, ipady=5, fill=BOTH, expand=False, side='top')
        self.recipient_entry_focus_out = self.recipient_entry.bind('<FocusOut>', self.on_focus_out)
        self.greeting = StringVar(master=e_frame_bottomR, name='greeting')
        self.greeting_entry = Entry(e_frame_bottomR)
        self.greeting_entry.pack(padx=4, pady=1, ipadx=160, ipady=5, fill=BOTH, expand=False, side='top')
        self.greeting_entry_focus_out = self.greeting_entry.bind('<FocusOut>', self.on_focus_out)
        self.body = StringVar(master=e_frame_bottomR, name='body')
        self.body_entry = Text(e_frame_bottomR, width=10, height=5)
        self.body_entry.pack(padx=4, pady=15, ipadx=160, ipady=5, fill=BOTH, expand=False, side='top')
        self.body_entry_focus_out = self.body_entry.bind('<FocusOut>', self.on_focus_out)
        self.salutation = StringVar(master=e_frame_bottomR, name='salutation')
        self.salutation_entry = Entry(e_frame_bottomR, width=27, highlightbackground='green', highlightcolor='red')
        self.salutation_entry.pack(padx=4, ipadx=160, ipady=5, fill=BOTH, expand=False, side='top')
        self.salutation_entry_focus_out = self.salutation_entry.bind('<FocusOut>', self.on_focus_out)
        
        self.btnSaveEmailTemplate = Button(e_frame_bottomR, text = 'Click to SAVE template for this market, & save your name!', bg='#22c26a', command = Presenter.btnSaveEmailTemplate).pack(padx=4, pady=20, ipady=50, fill=X, expand=False, anchor=S, side='bottom')

    def createSettingsTabWidgets(self):
        # Create frames for the tab
        entry_boxes_frame = Frame(master=self.settings, bg='#5F9EA0')
        entry_boxes_frame.pack(fill=BOTH, expand=False, side='top')
        save_btn_frame = Frame(master=self.settings, bg='#5F9EA0')
        save_btn_frame.pack(fill=BOTH, expand=False, side='top')
        # Header
        Label(self.settings, text='Settings Page', bg='#5F9EA0', font=('helvetica', 20, 'normal')).pack(fill=BOTH, expand=False, side='top')
        # Content
        Label(master=entry_boxes_frame, text='CC-address Settings (more to be added later or upon your request)', bg='#5F9EA0', font=('helvetica', 14, 'normal')).pack(fill=X, expand=False, side='top')
        
        Label(master=entry_boxes_frame, text='1st address to set as default cc: ', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(pady=3, ipady=2, padx=1, fill='none', expand=False, side='left', anchor=NW)
        
        self.default_CC1 = StringVar(master=entry_boxes_frame, name='default_CC1')
        self.default_CC1_entry = Entry(entry_boxes_frame,textvariable=self.default_CC1)
        self.default_CC1_entry.pack(pady=3, fill=X, ipadx=10, ipady=4, expand=True, side='left', anchor=N)
        
        Label(entry_boxes_frame, text='2nd address to set as default cc: ', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(pady=3, ipady=2, padx=1, fill='none', expand=False, side='left', anchor=NW)
        
        self.default_CC2 = StringVar(master=entry_boxes_frame, name='default_CC2')
        self.default_CC2_entry = Entry(entry_boxes_frame, textvariable=self.default_CC2)
        self.default_CC2_entry.pack(pady=3, fill=X, ipadx=10, ipady=4, expand=True, side='left', anchor=N)
        
        Button(save_btn_frame, text='Save Settings!', bg='#22c26a', font=('helvetica', 12, 'normal'), command=Presenter.btnSaveMainSettings).pack(ipady=10, pady=10, padx=10, fill=BOTH, expand=False, anchor=N, side='top')

    def create_quoteform_path_box(self, parent: Frame) -> None:
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
        self.quoteform_path_box.dnd_bind('<<Drop>>', Presenter.save_path(True))

    def create_extra_attachments_path_box(self, parent: Frame) -> None:
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
        self.extra_attachments_path_box.dnd_bind('<<Drop>>', Presenter.save_path(False))
        # Create functionality to show the paths of the files in box.

    def create_carrier_checkboxes(self, name: str, var_name: str,) -> None:
        Checkbutton(master=frame_right, name=name, text=name, variable=var_name, onvalue=self.positive_submission, offvalue='skip', bg='#aedadb', font=('helvetica', 12, 'normal'))
        name.pack(ipady=3, fill=BOTH, expand=True)


    def create_dropdown_variable(self, initial_value: str, name: str) -> None:
        """ Creates the variable used to identify the current selection and assigns/updates a different variable with current choice.
        """
        self.dropdown_menu_var = StringVar(value=initial_value, name=name)
        self.dropdown_menu_var.trace_add('write',
                                         Presenter.update_template_page(self, self.get_selected_template))
    
    def create_dropdown(self, parent) -> None:
        """ Creates the OptionMenu widget separately for less coupling."""

        options = list(Presenter.get_dropdown_options())
        dropdown_menu = OptionMenu(parent, self.dropdown_menu_var, options)
        dropdown_menu.configure(background='#aedadb', 
                                     foreground='black', highlightbackground='#5F9EA0', activebackground='#5F9EA0'
                                     )
        dropdown_menu['menu'].configure(background='#aedadb')
        dropdown_menu.pack(padx=15, ipady=5, fill = X, expand=True) 

    def on_focus_out(self, item, current_selection):#START & FINISH
        """ NOTE: THIS IS NOT AN IMPORTANT FUNCTION TO IMPLEMENT. This function performs actions on them to increase user UI experience.  NOTE:  This originally was a very lame function that repopulated specific fields if they were modified & subsequently left empty upon leaving focus---WOW...
        Instead,  this will also change text (foreground) color if it's changed."""
        print(item)
        #self.item.    
    
    @property
    def positive_submission_value(self):
        return self.positive_submission

    @property
    def extra_notes(self) -> str:
        return self.extra_notes_text.get()

    @extra_notes.deleter
    def extra_notes(self):
        del self.extra_notes_text

    @property
    def userinput_CC1(self) -> str:
        return self.userinput_CC1.get()
    @userinput_CC1.deleter
    def userinput_CC1(self) -> str:
        del self.userinput_CC1.get()

    @property
    def userinput_CC2(self) -> str:
        return self.userinput_CC2.get()
    @userinput_CC2.deleter
    def userinput_CC2(self) -> str:
        return self.userinput_CC2.get()

    @property
    def ignore_default_cc(self) -> bool:
        return self.ignore_CC_defaults.get()
    @ignore_default_cc.setter
    def ignore_default_cc(self, ignore_is_True: bool) -> None:
        self.ignore_CC_defaults = ignore_is_True
    
    
    #These are getters for the checkbuttons
    @property
    def sw(self) -> str:
        return self.seawave.get()
    @property
    def pt(self) -> str:
        return self.primetime.get()
    @property
    def nh(self) -> str:
        return self.newhampshire.get()
    @property
    def am(self) -> str:
        return self.americanmodern.get()
    @property
    def km(self) -> str:
        return self.kemah.get()
    @property
    def cp(self) -> str:
        return self.concept.get()
    @property
    def yi(self) -> str:
        return self.yachtinsure.get()
    @property
    def ce(self) -> str:
        return self.century.get()
    @property
    def In(self) -> str:
        return self.intact.get()
    @property
    def tv(self) -> str:
        return self.travelers.get()
    
    @property
    def selected_template(self) -> str:
        return self.dropdown_menu_var.get()
    @property
    def username(self) -> str:
        return self.username.get()
    @username.setter
    def username(self, new_username: str) -> None:
        self.username = new_username
    @username.deleter
    def username(self) -> None:
        del self.username
    @property
    def recipient(self) -> str:
        return self.recipient.get()
    @recipient.setter
    def recipient(self, new_recipient: str) -> None:
        self.recipient = new_recipient
    @recipient.deleter
    def recipient(self) -> None:
        del self.recipient
    @property
    def greeting(self) -> str:
        return self.greeting.get()
    @greeting.setter
    def greeting(self, new_greeting: str) -> None:
        self.greeting = new_greeting
    @greeting.deleter
    def body(self) -> None:
        del self.greeting
    @property
    def body(self) -> str:
        return self.body.get()
    @body.setter
    def body(self, new_body: str) -> None:
        self.body = new_body
    @body.deleter
    def body(self) -> None:
        del self.body
    @property
    def salutation(self) -> str:
        return self.salutation.get()
    @salutation.setter
    def salutation(self, new_salutation: str) -> None:
        self.salutation = new_salutation
    @salutation.deleter
    def salutation(self) -> None:
        del self.salutation
    
    @property
    def default_CC1(self) -> str:
        return self.default_CC1.get()
    @default_CC1.setter
    def default_CC1(self, new_default_CC: str) -> None:
        self.default_CC1 = new_default_CC
    @property
    def default_CC2(self) -> str:
        return self.default_CC2.get()
    @default_CC2.setter
    def default_CC2(self, new_default_CC: str) -> None:
        self.default_CC2 = new_default_CC
    

    def get_possible_redundancies(self) -> dict:
        """ This allows us to easily update list of likely redundancies."""
        possible_redundancies_dict = dict(self.sw,
                                          self.pt,
                                          self.nh
                                          )
        return possible_redundancies_dict
   
    def get_remaining_single_carriers(self) -> dict:#GOOD
        carrier_submissions_dict = {}
        carrier_submissions_dict.update({'am', self.am},
                                        {'km', self.km},
                                        {'cp', self.cp},
                                        {'yi', self.yi},
                                        {'ce', self.ce},
                                        {'In', self.In},
                                        {'in', self.tv},
                                        )
        return carrier_submissions_dict
    
    # Make these below FNs loop to accomodate multiple requests at once ;)
    def assign_placeholder(self, name_of_widget, placeholder: str):
        pass
    def get_placeholder(self, item):
        pass
    def insert_placeholder(self, item, indx, placeholder: str):
        item.insert(indx, placeholder)
    def delete_placeholder(self, item, indx):
        self.item.delete(indx, 'end')
    def enableField(self, item, wrap):
        item.configure(state='normal')
    def disableField(self, item):
        item.configure(state='disabled') 
# End of needing loop section :)


