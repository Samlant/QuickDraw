import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Notebook, Style
from tkinter import * 
from tkinterdnd2 import *
from typing import Any, Callable, Protocol

class Presenter(Protocol):
    def insert_placeholders():
        pass
    def delete_placeholders():
        pass
    def save_path(self, event, usage_type: bool):
        ...
    def btnSaveEmailTemplate():
        ...
    def btnSaveMainSettings():
        ...
    def saveExtraNotes():
        ...
    def saveCC():
        ...
    


class TkView(tk.Tk):
    """ Using Tkinter,  this class creates a view object when called on from the Presenter.  There is an aggregate setup function (create_GUI_obj) calling on individual widget creation functions separated by page/tab, and finally methods to update widgets and send data to the Presenter.
    """
        # Add more class attributes as needed/desired.


    def create_GUI_obj(self, presenter: Presenter):
        """ This creates the GUI root,  along with the main
        functions to create the widgets."""
        self.root = tk.Tk()
        self.root.geometry('760x548')
        self.root.configure(background='#5F9EA0')
        self.root.title('Quick Submit Tool')
        self.root.attributes('-alpha',0.95)

        #instance attributes
        self.cc_default_check = BooleanVar #Is this okay/preferred way to store this?

        self.createStyle()
        self.createNotebook()
        self.createTabs()
        self.createMainTabWidgets()
        self.createTemplateSettingsTabWidgets()
        self.createSettingsTabWidgets()
        #self.root.set_initial_placeholders()
    
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
        addNotes_labelframe = LabelFrame(frame_middle, text= 'To end with a message, enter it below:', bg='#aedadb', font=('helvetica', 8, 'normal'))
        addNotes_labelframe.pack(fill=X, expand=False, side='top')

        self.additional_email_body_notes = Text(addNotes_labelframe, height=7, width=30, name='raw_additional_body_notes')
        self.additional_email_body_notes.pack(fill = X, anchor=N, expand=FALSE, side='top')
        # end of label_frame

        # this is a label_frame
        cc_labelframe = LabelFrame(frame_middle, text= 'CC-address settings for this submission:', bg='#aedadb', name='cc_labelframe')
        cc_labelframe.pack(fill=X, expand=True, side='top')

        self.cc_def_check = Checkbutton(cc_labelframe, text='Check to ignore default CC-addresses.', variable=self.cc_default_check, bg='#aedadb', name='cc_def_chcek').pack(pady=5, fill=X, expand=False, side='top')

        Label(cc_labelframe, text='email address to CC:', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(fill=X, expand=True, side='top')

        self.cc_address_1_user_input = Text(cc_labelframe, height=1, width=30)
        self.cc_address_1_user_input.pack(pady=2, ipady=4, anchor=N, fill = X, expand=True, side='top')

        Label(cc_labelframe, text='email address to CC:', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(fill=X, expand=True, side='top')

        self.cc_address_2_user_input = Text(cc_labelframe, height=1, width=30)
        self.cc_address_2_user_input.pack(ipady=4, anchor=N, fill = X, expand=True, side='top')
        # end of label_frame

        
        # Create widgets inside Frame Right
        self.seawave_var = StringVar(master=frame_right, name='Seawave')
        seawave = Checkbutton(master=frame_right, text='Seawave Insurance',
                              variable=self.seawave_var, onvalue='Submit',
                              offvalue='skip', bg='#aedadb',
                              font=('helvetica', 12, 'normal'),
                              command=Presenter.check_if_combo
                              )
        seawave.pack(ipady=3, fill=BOTH, expand=True)
       
        self.primetime_var = StringVar(master=frame_right, name='Prime Time')
        primetime = Checkbutton(frame_right, text='Prime Time Insurance', 
                                variable=self.primetime_var, onvalue='Submit',
                                offvalue='skip', bg='#aedadb',
                                font=('helvetica', 12, 'normal'),
                                command=Presenter.check_if_combo
                                )
        primetime.pack(ipady=3, fill=BOTH, expand=True)
        
        self.newhampshire_var = StringVar(master=frame_right, name='New Hampshire')
        newhampshire = Checkbutton(frame_right, text='New Hampshire',
                                   variable=self.newhampshire_var,
                                   onvalue='Submit',
                                   offvalue='skip', bg='#aedadb',
                                   font=('helvetica', 12, 'normal'),
                                   command=Presenter.check_if_combo
                                   )
        newhampshire.pack(ipady=3, fill=BOTH, expand=True)
        
        self.americanmodern_var = StringVar(master=frame_right, name='American Modern')
        americanmodern_chckbttn = Checkbutton(frame_right, text='American Modern',
                                     variable=self.americanmodern_var,
                                     onvalue='Submit',
                                     offvalue='skip', bg='#aedadb',
                                     font=('helvetica', 12, 'normal')
                                     )
        americanmodern_chckbttn.pack(ipady=3, fill=BOTH, expand=True)
        
        self.kemah_var = StringVar(master=frame_right, name='Kemah Marine')
        kemah_chckbttn = Checkbutton(frame_right, text='Kemah Marine',
                            variable=self.kemah_var, onvalue='Submit',
                            offvalue='skip', bg='#aedadb',
                            font=('helvetica', 12, 'normal')
                            )
        kemah_chckbttn.pack(ipady=3, fill=BOTH, expand=True)
        
        self.concept_var = StringVar(master=frame_right, name='Concept Special Risks')
        concept_chckbttn = Checkbutton(frame_right, text='Concept Special Risks',
                              variable=self.concept_var, onvalue='Submit',
                              offvalue='skip', bg='#aedadb',
                              font=('helvetica', 12, 'normal')
                              )
        concept_chckbttn.pack(ipady=3, fill=BOTH, expand=True)
        
        self.yachtinsure_var = StringVar(master=frame_right, name='Yachtinsure')
        yachtinsure_chckbttn = Checkbutton(frame_right, text='Yachtinsure',
                                  variable=self.yachtinsure_var, onvalue='Submit',
                                  offvalue='skip', bg='#aedadb',
                                  font=('helvetica', 12, 'normal')
                                  )
        yachtinsure_chckbttn.pack(ipady=3, fill=BOTH, expand=True)
        
        self.century_var = StringVar(master=frame_right, name='Century')
        century_chckbttn = Checkbutton(frame_right, text='Century Insurance',
                              variable=self.century_var, onvalue='Submit',
                              offvalue='skip', bg='#aedadb',
                              font=('helvetica', 12, 'normal')
                              )
        century_chckbttn.pack(ipady=3, fill=BOTH, expand=True)
        
        self.intact_var = StringVar(master=frame_right, name='Intact')
        intact_chckbttn = Checkbutton(frame_right, text='Intact',
                             variable=self.intact_var,
                             onvalue='Submit',
                             offvalue='skip', bg='#aedadb', 
                             font=('helvetica', 12, 'normal')
                             )
        intact_chckbttn.pack(ipady=3, fill=BOTH, expand=True)
        
        self.travelers_var = StringVar(master=frame_right, name='Travelers')
        travelers_chckbttn = Checkbutton(frame_right, text='Travelers',
                                variable=self.travelers_var, onvalue='Submit',
                                offvalue='skip', bg='#aedadb',
                                font=('helvetica', 12, 'normal')
                                )
        travelers_chckbttn.pack(ipady=3, fill=BOTH, expand=True)

        Button(frame_right, text='Submit and sent to markets!', bg='#22c26a', font=('helvetica', 12, 'normal'), command=self.btnSendEmail).pack(ipady=20, pady=10, anchor=S, fill=BOTH, expand=True)
        # End of creating the MAIN tab widgets

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
        
        self.username_value = StringVar(master=e_frame_header, name='username')

        self.username_entry = Entry(master=e_frame_header, textvariable=self.username_value)
        self.username_entry.pack(ipadx=900, pady=5, fill=BOTH, expand=True, side='right', anchor=NW)
        self.username_entry.bind()
        self.username_entry_focus_out = self.username_entry.bind('<FocusOut>', lambda x: on_focus_out(your_name, 'name'))
        # End of Header
        
        # Create widgets for the Top Frame
        Label(e_frame_top, text = "This drop-down menu allows you to view & edit a specific carrier's, or combo carriers', email message contents.", bg='#5F9EA0', font=('helvetica', 10, 'normal')).pack(fill = X, expand=True)
        
        
        
        #drop = OptionMenu(e_frame_top, dropdown_email_template, 'Select Carrier', *options)
        # The above line includes a default value choice,  whereas below doesn't. above could reduce redundancy ny deleting 'Select Carrier' from options list
        self.create_options_menu()
        
      # MOVE TO CONTROLLER?
        # End of Top Frame

        # Create widgets for the Bottom Left Frames
        Label(e_frame_bottomL, text = 'Submission Address:', bg='#aedadb', font=('helvetica', 16, 'normal')).pack(padx=2, pady=15, fill=BOTH, expand=True, anchor=E, side='top')
        Label(e_frame_bottomL, text = 'Greeting:', bg='#aedadb', font=('helvetica', 16, 'normal')).pack(padx=2, fill=BOTH, expand=True, anchor=E, side='top')
        Label(e_frame_bottomL, text = 'Body of the email:', bg='#aedadb', font=('helvetica', 16, 'normal')).pack(padx=2, pady=15, fill=BOTH, expand=True, anchor=E, side='top')
        Label(e_frame_bottomL, text = 'Salutation:', bg='#aedadb', font=('helvetica', 16, 'normal')).pack(padx=2, pady=63, fill=BOTH, expand=True, anchor=E, side='top')

        # Create widgets for the Bottom Right Frames
        self.msg_recipient_value = StringVar(master=e_frame_bottomR, name='msg_recipient_value')
        self.msg_recipient_entry = Entry(master=e_frame_bottomR, textvariable=self.msg_recipient_value)
        self.msg_recipient_entry.pack(padx=4, pady=15, ipadx=160, ipady=5, fill=BOTH, expand=False, side='top')
        #self.msg_recipient_entry_focus_out = msg_recipient_entry.bind('<FocusOut>', lambda x: Presenter.on_focus_out(msg_recipient_entry, 'recipient'))

        self.msg_greeting_value = StringVar(master=e_frame_bottomR, name='msg_greeting_value')
        self.msg_greeting_entry = Entry(e_frame_bottomR)
        self.msg_greeting_entry.pack(padx=4, pady=1, ipadx=160, ipady=5, fill=BOTH, expand=False, side='top')
        #self.msg_greeting_entry_focus_out = msg_greeting_entry.bind('<FocusOut>', lambda x: Presenter.on_focus_out_entry(msg_greeting_entry, 'greeting'))
        
        self.msg_body_value = StringVar(master=e_frame_bottomR, name='msg_body_value')
        self.msg_body_entry = Text(e_frame_bottomR, width=10, height=5)
        self.msg_body_entry.pack(padx=4, pady=15, ipadx=160, ipady=5, fill=BOTH, expand=False, side='top')
        #self.msg_body_entry_focus_out = msg_body_entry.bind('<FocusOut>', lambda x: Presenter.on_focus_out_text(msg_body_entry, 'body'))
        
        self.msg_salutation_value = StringVar(master=e_frame_bottomR, name='msg_salutation_value')
        self.msg_salutation_entry = Entry(e_frame_bottomR, width=27, highlightbackground='green', highlightcolor='red')
        self.msg_salutation_entry.pack(padx=4, ipadx=160, ipady=5, fill=BOTH, expand=False, side='top')
        #self.msg_salutation_entry_focus_out = msg_salutation_entry.bind('<FocusOut>', lambda x: Presenter.on_focus_out_entry(msg_salutation_entry, 'salutation'))
        
        self.btnSaveEmailTemplate = Button(e_frame_bottomR, text = 'Click to SAVE template for this market, & save your name!', bg='#22c26a', command = Presenter.btnSaveEmailTemplate).pack(padx=4, pady=20, ipady=50, fill=X, expand=False, anchor=S, side='bottom')

    def createSettingsTabWidgets(self):
        # Create frames for the tab
        entry_boxes_frame = Frame(master=self.settings, bg='#5F9EA0')
        entry_boxes_frame.pack(fill=BOTH, expand=False, side='top')

        save_btn_frame = Frame(master=self.settings, bg='#5F9EA0')
        save_btn_frame.pack(fill=BOTH, expand=False, side='top')

        # Header
        Label(self.settings, text='Settings Page', bg='#5F9EA0', font=('helvetica', 20, 'normal')).pack(fill=BOTH, expand=False, side='top')
        
        # content
        Label(settings, text='CC-address Settings (more to be added later or upon your request)', bg='#5F9EA0', font=('helvetica', 14, 'normal')).pack(fill=X, expand=False, side='top')
        
        Label(entry_boxes_frame, text='1st address to set as default cc: ', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(pady=3, ipady=2, padx=1, fill='none', expand=False, side='left', anchor=NW)
        
        self.default_CC1_value = StringVar(master=entry_boxes_frame, name='default_CC1_value')
        self.default_CC1_entry = Entry(entry_boxes_frame,textvariable=self.default_CC1_value)
        self.default_CC1_entry.pack(pady=3, fill=X, ipadx=10, ipady=4, expand=True, side='left', anchor=N)
        
        Label(entry_boxes_frame, text='2nd address to set as default cc: ', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(pady=3, ipady=2, padx=1, fill='none', expand=False, side='left', anchor=NW)
        
        self.default_CC2_value = StringVar(master=entry_boxes_frame, name='default_CC2_value')
        self.default_CC2_entry = Entry(entry_boxes_frame, textvariable=self.default_CC2_value)
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
        self.extra_attachments_path_box.dnd_bind('<<Drop>>', self.save_path(False))

    # def create_checkboxes(self,) -> None:
    #     self.seawave_var = StringVar(master=frame_right, name='Seawave')
    #     seawave = Checkbutton(master=frame_right, text='Seawave Insurance', variable=self.seawave_var, onvalue='Submit', offvalue='skip', bg='#aedadb', font=('helvetica', 12, 'normal'), command=self.check_if_combo)
    #     seawave.pack(ipady=3, fill=BOTH, expand=True)


    def create_option_menu_variable(self, initial_value: str, name: str) -> None:
        """ Creates the variable used to identify the current selection and assigns/updates a different variable with current choice.
        """
        self.current_dd_selection = str
        self.dropdown_menu_var = StringVar(value=initial_value, name=name)
        self.dropdown_menu_var.trace_add('write', self.current_dd_selection)
    
    def create_option_menu(self, parent, options: list) -> None:
        """ Creates the OptionMenu widget separately for less coupling."""

        dropdown_menu = OptionMenu(parent, self.dropdown_menu_var, options)
        dropdown_menu.configure(background='#aedadb', 
                                     foreground='black', highlightbackground='#5F9EA0', activebackground='#5F9EA0'
                                     )
        dropdown_menu['menu'].configure(background='#aedadb')
        dropdown_menu.pack(padx=15, ipady=5, fill = X, expand=True) 

    def get_checkbox_status(self, name: StringVar):
        return name.get()
    
    def get_list_of_duplicate_markets(self) -> list:
        self.list_of_possible_duplicates = list('Seawave',
                                            'Prime Time',
                                            'New Hampshire'
                                            )
    
    def get_combo_checkbttns(self, possible_duplicates: list) -> dict:
        """ This gets all possible combo markets into a dict
        and sends to the Presenter.
        """
        sw = self.get_checkbox_status(self.seawave_var)
        pt = self.get_checkbox_status(self.primetime_var)
        nh = self.get_checkbox_status(self.newhampshire_var)

        combo_checkbttns_dict = {'Seawave':sw, 
                                 'Prime Time':pt,
                                 'New Hampshire':nh
                                 }
        return combo_checkbttns_dict
    
    @property
    def get_selected_template(self) -> str:
        return self.current_dd_selection.get()
    @property
    def get_username(self) -> str:
        return self.username_value.get()
    
    @property
    def get_recipient(self) -> str:
        return self.msg_recipient_value.get()
    
    @property
    def get_greeting(self) -> str:
        return self.msg_greeting_value.get()
    
    @property
    def get_body(self) -> str:
        return self.msg_body_value.get()
    
    @property
    def get_salutation(self) -> str:
        return self.msg_salutation_value.get()
    
    @property
    def get_default_CC1(self) -> str:
        return self.default_CC1_value.get()

    @property
    def get_default_CC2(self) -> str:
        return self.default_CC2_value.get()
    
    

       
    def set_focus_out_bindings(self):
        self.your_name_focus_out = username_entry.bind('<FocusOut>', lambda x: Presenter.on_focus_out(get_username()))
        self.msg_address_entry_focus_out = msg_address_entry.bind('<FocusOut>', lambda x: on_focus_out(entry.get()))
        self.msg_greeting_entry_focus_out = msg_greeting_entry.bind('<FocusOut>', lambda x: on_focus_out(entry.get()))
        self.msg_body_entry_focus_out = msg_body_entry.bind('<FocusOut>', lambda x: on_focus_out(entry.get()
        ))
        self.msg_salutation_entry_focus_out = self.msg_salutation_entry.bind('<FocusOut>', lambda x: on_focus_out_entry(self.msg_salutation_entry, 'salutation'))


    def set_initial_placeholders(self):
        '''
        Sets the initial view for each field if applicable
        '''
        
        pass

    def get_placeholder(self, item):
        pass
        
    def insert_placeholder(self, item, indx, placeholder: str):
        self.item = item
        self.item_to_modify.insert(indx, placeholder)

    def delete_placeholder(self, item, indx):
        self.item.delete(indx, 'end')

    def enableField(self, item, wrap):
        item.configure(state='normal')

    def disableField(self, item):
        item.configure(state='disabled')
    
# THESE ARE THE REVISED EDITIONS AS OF 02/02:
# 
    def save_path(self, event, usage_type: bool):
        Presenter.save_path(event, usage_type)
    
    def save_extra_notes(self, input: str):
        Presenter.save_extra_notes(input)

    def save_CC(self,input):
        Presenter.save_CC(input)

    def check_if_combo(self):
        #Presenter.check_if_combo
        sw = self.seawave_var.get()
        pt = self.primetime_var.get()
        nh = self.newhampshire_var.get()

        if sw=='' and pt==1 and nh==0:
        elif sw==1 and pt==0 and nh==1:
        elif sw==1 and pt==1 and nh==1:
        elif pt==1 and nh==1:
        elif sw==1 or pt==1 or nh==1: