import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Notebook, Style
from tkinter import * 
from tkinterdnd2 import *
import fillpdf
from fillpdf import fillpdfs
from helper import *
# Create the main window
root = Tk()
root.geometry('760x548')
root.configure(background='#5F9EA0')
root.title('Quote Submissions Tool')
root.attributes('-alpha',0.95)
# use below to replace title icon when ready
#root.iconbitmap('./assets/example.ico') 

# Create an instance of Tk Style so that we can style our tabs
style = Style()
style.theme_use('default')
style.configure('TNotebook', background='#5F9EA0')
style.configure('TFrame', background='#5F9EA0')
style.map('TNotebook', background= [('selected', '#5F9EA0')])
#Create a Notebook under root, then tabs to make sub-windows.
tabControl = ttk.Notebook(root)
main = ttk.Frame(tabControl)
template_settings = ttk.Frame(tabControl)
settings = ttk.Frame(tabControl)
tabControl.add(main, text='Main')
tabControl.add(template_settings, text='Templates')
tabControl.add(settings, text='Settings')
# Done setting up main window with tabs---Declaring variables upfront below (no packing):
# Declaring variables used on the MAIN TAB
# Frames
frame_header = Frame(main, bg='#5F9EA0', pady=17)
frame_left = Frame(main, bg='#5F9EA0')
frame_middle = Frame(main, bg='#5F9EA0')
frame_right = Frame(main, bg='#5F9EA0')
#Frame left
textarea = Text(frame_left, height=7, width=27, background='#59f3e3')
attachmentsarea = Text(frame_left, height=9, width=27, background='#59f3e3')
# Frame middle
addNotes_labelframe = LabelFrame(frame_middle, text= 'To end with a message, enter it below:', bg='#aedadb', font=('helvetica', 8, 'normal'))
cc_labelframe = LabelFrame(frame_middle, text= 'CC-address settings for this submission:', bg='#aedadb')
cc_default_check = tk.IntVar()
additional_email_body_notes = Text(addNotes_labelframe, height=7, width=30)
cc_address_1_user_input = Text(cc_labelframe, height=1, width=30)
cc_address_2_user_input = Text(cc_labelframe, height=1, width=30)
cc_def_check = Checkbutton(cc_labelframe, text='Check to ignore default CC-addresses.', variable=cc_default_check, bg='#aedadb').pack(pady=5, fill=X, expand=False, side='top')
# Frame right
seawave_check = tk.IntVar()
primetime_check = tk.IntVar()
newhampshire_check = tk.IntVar()
americanmodern_check = tk.IntVar()
kemah_check = tk.IntVar()
concept_check = tk.IntVar()
yachtinsure_check = tk.IntVar()
century_check = tk.IntVar()
intact_check = tk.IntVar()
travelers_check = tk.IntVar()
seawave = Checkbutton(frame_right, text='Seawave Insurance', variable=seawave_check, bg='#aedadb', font=('helvetica', 12, 'normal'))
primetime = Checkbutton(frame_right, text='Prime Time Insurance', variable=primetime_check, bg='#aedadb', font=('helvetica', 12, 'normal'))
newhampshire = Checkbutton(frame_right, text='New Hampshire', variable=newhampshire_check, bg='#aedadb', font=('helvetica', 12, 'normal'))
americanmodern = Checkbutton(frame_right, text='American Modern', variable=americanmodern_check, bg='#aedadb', font=('helvetica', 12, 'normal'))
kemah = Checkbutton(frame_right, text='Kemah Marine', variable=kemah_check, bg='#aedadb', font=('helvetica', 12, 'normal'))
concept = Checkbutton(frame_right, text='Concept Special ', variable=concept_check, bg='#aedadb', font=('helvetica', 12, 'normal'))
yachtinsure = Checkbutton(frame_right, text='Yachtinsure', variable=yachtinsure_check, bg='#aedadb', font=('helvetica', 12, 'normal'))
century = Checkbutton(frame_right, text='Century Insurance', variable=century_check, bg='#aedadb', font=('helvetica', 12, 'normal'))
intact = Checkbutton(frame_right, text='Intact', variable=intact_check, bg='#aedadb', font=('helvetica', 12, 'normal'))
travelers = Checkbutton(frame_right, text='Travelers', variable=travelers_check, bg='#aedadb', font=('helvetica', 12, 'normal'))
# Declaring variables used on the EMAIL TEMPLATE TAB
#Frames
e_frame_header_spacer = Frame(template_settings, bg='#5F9EA0', height=17)
e_frame_header = Frame(template_settings, bg='#5F9EA0')
e_frame_top = Frame(template_settings, bg='#5F9EA0')
e_frame_content = Frame(template_settings, bg='#5F9EA0')
e_frame_bottomL = Frame(template_settings, bg='#5F9EA0' )
e_frame_bottomR = Frame(template_settings, bg='#5F9EA0')
# Universal header content
your_name_placeholder = getyourName()
your_name = Entry(e_frame_header)
your_name.insert(0, your_name_placeholder)
# Dropdown selection
options = [
	'Select Carrier',
    'Seawave',
    'Prime Time',
    'New Hampshire',
    'American Modern',
    'Kemah',
    'Concept',
    'Yachtinsure',
	'Century',
	'Intact',
	'Travelers',
	'Combo SW and PT',
	'Combo SW and NH',
	'Combo SW, PT and NH',
	'Combo PT and NH'
]
dropdown_email_template = StringVar(value='Select Carrier')
drop = OptionMenu(e_frame_top, dropdown_email_template, *options)
drop.configure(background='#aedadb', foreground='black', highlightbackground='#5F9EA0', activebackground='#5F9EA0')
drop['menu'].configure(background='#aedadb')
# Template content section
carrier_address_placeholder = ''
carrier_body_placeholder = ''
carrier_greeting_placeholder = ''
carrier_salutation_placeholder = ''
carrier_address = Entry(e_frame_bottomR)
carrier_greeting = Entry(e_frame_bottomR)
carrier_body = Text(e_frame_bottomR, width=10, height=5)
carrier_salutation = Entry(e_frame_bottomR, width=27, highlightbackground='green', highlightcolor='red')
carrier_address.insert(0, carrier_address_placeholder)
carrier_address.configure(state='disabled')
carrier_greeting.insert(0, carrier_greeting_placeholder)
carrier_greeting.configure(state='disabled')
carrier_body.insert(1.0, carrier_body_placeholder)
carrier_body.configure(state='disabled', wrap='word')
carrier_salutation.insert(0, carrier_salutation_placeholder)
carrier_salutation.configure(state='disabled')
your_name_focus_out = your_name.bind('<FocusOut>', lambda x: on_focus_out_entry(your_name, 'name'))
carrier_address_focus_out = carrier_address.bind('<FocusOut>', lambda x: on_focus_out_entry(carrier_address, 'address'))
carrier_greeting_focus_out = carrier_greeting.bind('<FocusOut>', lambda x: on_focus_out_entry(carrier_greeting, 'greeting'))
carrier_body_focus_out = carrier_body.bind('<FocusOut>', lambda x: on_focus_out_text(carrier_body, 'body'))
carrier_salutation_focus_out = carrier_salutation.bind('<FocusOut>', lambda x: on_focus_out_entry(carrier_salutation, 'salutation'))
# Declaring variables used on the SETTINGS TAB
# Frames
entry_boxes_frame = Frame(settings, bg='#5F9EA0')
save_btn_frame = Frame(settings, bg='#5F9EA0')
# Settings variables (more to come with time and requests)
defaultCCaddress1 = Entry(entry_boxes_frame)
defaultCCaddress2 = Entry(entry_boxes_frame)
#GLOBAL variables to ensure tha teach loop is started with empty values.
attachments = []
last_name = ''
first_name = ''
year = 0
make = ''
length = 0
# ---End of GLOBAL variables---

# ---Beginning Functions---
def updateCarrierChoice(*args):
# Get the current dropdown selection,  load config, and ensure that entries are empty prior to loading placeholder text
    current_selected_carrier = dropdown_email_template.get()
    print(current_selected_carrier)
    current_selected_carrier = assignCorrectCarrierNames(current_selected_carrier)
    print(current_selected_carrier)
    config = update_config()
    carrier_address.delete(0, 'end')
    carrier_greeting.delete(0, 'end')
    carrier_body.delete('1.0', 'end')
    carrier_salutation.delete(0, 'end')
    #Was I going to continue this upper section?
# If current choice is the default 'Select Carriers' option,  then disable the fields.
    if current_selected_carrier[0]=='Select Carrier':
        carrier_address.configure(state='disabled')
        carrier_greeting.configure(state='disabled')
        carrier_body.configure(state='disabled')
        carrier_salutation.configure(state='disabled')
# If current choice is a combo-market email, use the correct placeholder text.
    elif 'Combo' in current_selected_carrier[0]:
        print(current_selected_carrier)
        placeholder = config['Combo email'][current_selected_carrier[1]].value
        carrier_body.configure(state='normal')
        carrier_body.insert('1.0', placeholder)
        carrier_address.insert(0, 'N/A, uses same as Seawaves template')
        carrier_greeting.insert(0, 'N/A, uses same as Seawaves template')
        carrier_salutation.insert(0, 'N/A, uses same as Seawaves template')
        carrier_address.configure(state='disabled')
        carrier_greeting.configure(state='disabled')
        carrier_salutation.configure(state='disabled')
    else:
# Otherwise,  first activate all fields if they're disabled, then assign placeholders.
        if carrier_address.cget('state')=='disabled':
            carrier_address.configure(state='normal')
            carrier_body.configure(state='normal')
            carrier_greeting.configure(state='normal')
            carrier_salutation.configure(state='normal')
        else:
            pass
        placeholder_address = config[current_selected_carrier[0]]['address'].value
        placeholder_greeting = config[current_selected_carrier[0]]['greeting'].value
        placeholder_body = config[current_selected_carrier[0]]['body'].value
        placeholder_salutation = config[current_selected_carrier[0]]['salutation'].value
        carrier_address.insert(0, placeholder_address)
        carrier_greeting.insert(0, placeholder_greeting)
        carrier_body.insert('1.0', placeholder_body)
        carrier_salutation.insert(0, placeholder_salutation) 

def on_focus_out_entry(entry, field_name):
    section_name = assignCorrectCarrierNames(dropdown_email_template.get())
    if section_name[0] != 'Select Carrier':
# Put placeholder txt & index_variable (to tell if it's entry or text widget: 0 or '1.0') in a tuple.
        placeholder_tuple = getPlaceholders(section_name, 'entry', field_name)
        if entry.get() == "":
# The below uses either '1.0' or 0 for the index to insert txt at.
            entry.insert(placeholder_tuple[1], placeholder_tuple[0])
    else:
        print(f"On ENTRY_focus out, the section_name is: {section_name}")

def on_focus_out_text(entry, field_name):
    section_name = assignCorrectCarrierNames(dropdown_email_template.get())
    if section_name[0] != 'Select Carrier':
        if entry.get("1.0", 'end') == '':
            placeholder = getPlaceholders(section_name, 'text', field_name)
            entry.insert(0, placeholder)
    else:
        print(f"On TEXT_focus out, the section_name is: {section_name}")

def btnSaveCarrierTemplate():
    config = update_config()
    carrier = dropdown_email_template.get()
    carrier_tuple = assignCorrectCarrierNames(carrier)
    if carrier_tuple[0]=='Select Carrier':
        pass
    elif 'Combo' in carrier_tuple:
        config[carrier_tuple[0]][carrier_tuple[1]].value = carrier_body.get()
    elif carrier_tuple[1]=='sammy':
        # Singling out the only text box present to define it appropriately apart from entries.
        body_text = carrier_body.get('1.0', 'end')
        config['General settings']['your_name'].value = your_name.get()
        config[carrier_tuple[0]]['address'].value = carrier_address.get()
        config[carrier_tuple[0]]['greeting'].value = carrier_greeting.get()
#        config.set(carrier_tuple[0], 'body', carrier_body.get('1.0', 'end'))
        config[carrier_tuple[0]]['body'].set_values(body_text, 4*'')
        print(body_text)
        config[carrier_tuple[0]]['salutation'].value = carrier_salutation.get()
    config.update_file()
  
def btnSaveMainSettings(): # 1/13: WORKS, saves to config as expected.
    updater = update_config()
    cc1 = defaultCCaddress1.get()
    cc2 = defaultCCaddress2.get()
    print(cc1)
    updater['CarbonCopy Settings']['defaultCCaddress1'].value = cc1
    updater['CarbonCopy Settings']['defaultCCaddress2'].value = cc2
    updater.update_file()

#End of SETTINGS#

# Helper Functions------------------
def getDropDownSelection():
    get_dropdown_selection = dropdown_email_template.get()
    return get_dropdown_selection

def Get_CC_Addresses(): #NEED TO REVISE HOW WE KEEP ADDRESS...It gets replaced with 'None'
    config = read_config()
    cc_addresses = [cc_address_1_user_input.get('1.0', 'end-1c'), cc_address_2_user_input.get('1.0', 'end-1c')]
    if cc_default_check.get()=='0':
        try:
            cc_addresses.append(config.get('CarbonCopy Settings', 'defaultCCaddress1'), config.get('CarbonCopy Settings', 'defaultCCaddress2'))
            cc_addresses = f"{cc_addresses}"
        except:
            print('The cc append didnt work, trying the other way...')
            try:
                cc_addresses.append(config.get('CarbonCopy Settings', 'defaultCCaddress1'))
                cc_addresses.append(config.get('CarbonCopy Settings', 'defaultCCaddress2'))
                cc_addresses = f"{cc_addresses}"
                print('Done.')
            except:
                print('Not successful in saving CC addresses')
    else:
        cc_addresses = ';'.join(str(element) for element in cc_addresses)
        print(cc_addresses)
    return cc_addresses

def path_to_additional_attachments(event):
	if '{' in event.data:
		attachments.append(event.data.translate({ord(c): None for c in '{}'}))
	else:
		attachments.append(event.data)
	return attachments
			    
#MAIN FUNCTIONS-------|
def sameCarrierSubmission():
    config = read_config()
    dict0 = [seawave_check.get(), primetime_check.get(), newhampshire_check.get()]
    if dict0[0]==1 and dict0[1]==1 and dict0[2]==0:
        address = config.get('SW email', 'address')
        greeting = config.get('SW email', 'greeting')
        body = config.get('Combo email', 'SWandPTbody')
        salutation = config.get('SW email', 'salutation')
        your_name = config.get('General settings', 'your_name')
    elif dict0[0]==1 and dict0[1]==0 and dict0[2]==1:
        address = config.get('SW email', 'address')
        greeting = config.get('SW email', 'greeting')
        body = config.get('Combo email', 'SWandNHbody')
        salutation = config.get('SW email', 'salutation')
        your_name = config.get('General settings', 'your_name')
    elif dict0[0]==1 and dict0[1]==1 and dict0[2]==1:
        address = config.get('SW email', 'address')
        greeting = config.get('SW email', 'greeting')
        body = config.get('Combo email', 'PTandNHandSWbody')
        salutation = config.get('SW email', 'salutation')
        your_name = config.get('General settings', 'your_name')
    elif dict0[1]==1 and dict0[2]==1:
        address = config.get('SW email', 'address')
        greeting = config.get('SW email', 'greeting')
        body = config.get('Combo email', 'PTandNHbody')
        salutation = config.get('SW email', 'salutation')
        your_name = config.get('General settings', 'your_name')
    elif dict0[0]==1 or dict0[1]==1 or dict0[2]==1:
        if dict0[0]==1:
            address = config.get('SW email', 'address')
            greeting = config.get('SW email', 'greeting')
            body = config.get('SW email', 'body')
            salutation = config.get('SW email', 'salutation')
            your_name = config.get('General settings', 'your_name')
        elif dict0[1]==1:
            address = config.get('PT email', 'address')
            greeting = config.get('PT email', 'greeting')
            body = config.get('PT email', 'body')
            salutation = config.get('PT email', 'salutation')
            your_name = config.get('General settings', 'your_name')
        else:
            address = config.get('NH email', 'address')
            greeting = config.get('NH email', 'greeting')
            body = config.get('NH email', 'body')
            salutation = config.get('NH email', 'salutation')
            your_name = config.get('General settings', 'your_name')
    else:
        pass
    for section in config:
        if section=='SW email' or section=='PT email' or 'NH email':
            pass
        else:
            try:
                address = config.get(section, 'address')
                greeting = config.get(section, 'name')
                body = config.get(section, 'name')
                salutation = config.get(section, 'salutation')
                your_name = config.get('General Settings', 'your name')
            except:
                pass
    sendEmail(address, greeting, body, salutation, your_name)

def sendEmail(address, greeting, body, salutation, your_name):
    import win32com.client as win32
    outlook = win32.Dispatch('outlook.application')
    cc_output = Get_CC_Addresses()
    add_notes = additional_email_body_notes.get('1.0', 'end-1c')
    mail = outlook.CreateItem(0)
    quoteform_fields_dict = fillpdfs.get_form_fields(Get_Path.quoteform_path)
    mail.Subject = Get_Subject(quoteform_fields_dict)
    mail.To = address
    mail.CC = cc_output
    mail.HTMLBody = '''
    <html><head>
    <title>New Quote Submission</title>
    <meta http-equiv='Content-Type' content='text/html; charset=windows-1252'>
    <meta name='ProgId' content='Word.Document'>
    <meta name='Generator' content='Microsoft Word 15'>
    <meta name='Originator' content='Microsoft Word 15'>
    </head>
    <body>
    <p style='font-size=14px;color:#1F3864'>%s</p>
    <p style='font-size=14px;color:#1F3864'>%s %s</p><br>
    </body>
    <footer>
    <p style='margin:0in;font-size:14px;font-family:Calibri,sans-serif;color:#1F3864;'>%s</p>
    <p style='margin:0in;font-size=14px;font-family:Calibri,sans-serif;color:#1F3864;'>%s</p><br>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Main:(800)-823-2798</p>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Office :(941)-444-5099</p>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Fax:(941)-328-3598</p><br>
    <p style='margin:0in;color:#0563C1;text-decoration:underline;text-underline:single;font-size:12px;font-family:Georgia Pro,serif;'>1549 Ringling Blvd., Suite 101</p>
    <p style='margin:0in;color:#0563C1;text-decoration:underline;text-underline:single;font-size:12px;font-family:Georgia Pro,serif;'>Sarasota, FL 34236</p><br>
    <p style='margin:0in;color:#1F3864;font-size:10.0pt;font-family:Georgia Pro,serif;color:blue;'><a href='http://www.novamarinsurance.com/' target='_blank'>www.novamarinsurance.com</a></p>
    <p style='margin:0in;color:#1F3864;font-size:10.0pt;font-family:Georgia Pro,serif;color:blue;'><a href='http://www.novamarinsurance.com.mx/' target='_blank'>www.novamarinsurance.com.mx</a></p>

    <p style'margin:0in'><a href='https://www.facebook.com/NovamarInsurance' target='_blank'><img width=24 height=24 src='https://cdn1.iconfinder.com/data/icons/social-media-2285/512/Colored_Facebook3_svg-512.png'></a>  <a href='https://www.instagram.com/novamar_insurance/' target='_blank'><img width=24 height=24 src='https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Instagram_colored_svg_1-512.png' style='display:block'></a>  <a href='https://twitter.com/NovamarIns' target='_blank'><img width=24 height=24 src='https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Twitter3_colored_svg-512.png' style='display:block'></a>  <a href='https://www.linkedin.com/company/novamar-insurance-group-inc' target='_blank'><img width=24 height=24 src='https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Linkedin_unofficial_colored_svg-512.png' style='display:block'></a></p>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Established in 1987 with offices in: Seattle | Newport Beach | San Diego | Sarasota | Jacksonville | Puerto Vallarta | Cancun | San Miguel de Allende</p>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Please be advised that coverage is not bound, renewed, amended or in force unless confirmed in writing by a Novamar Insurance Group agent or by the represented company.</p>
    </footer></html>
    ''' %(greeting, body, add_notes, salutation, your_name)
    mail.Attachments.Add(Get_Path.quoteform_path)
    for attachment in attachments:
        mail.Attachments.Add(attachment)
    mail.Display()
#   mail.Send()

#Packing Tabs
tabControl.pack(expand=1, fill='both')
#tkinter modules by tab
#MAIN TAB
# Packing MAIN tab with frames
frame_header.pack(padx=5, fill=X, expand=False)
frame_left.pack(padx=5, fill = Y, side='left', expand = False, anchor=NE)
frame_middle.pack(padx=5, fill = Y, side='left', expand = False, anchor=N)
frame_right.pack(padx=5, fill = Y, side='left', expand = False, anchor=NW)
# frame_left ->DECLARE VARIABLES, FUNCTIONS, & PACK
Label(frame_header, text='Get Client Information', bg='#5F9EA0', font=('helvetica', 20, 'normal')).pack(fill=X, expand=True, side='left')
Label(frame_header, text='Extra Notes & CC', bg='#5F9EA0', font=('helvetica', 20, 'normal')).pack(fill=X, expand=True, side='left')
Label(frame_header, text='Choose Markets:', bg='#5F9EA0', font=('helvetica', 20, 'normal')).pack(fill=X, expand=True, side='left')
Label(frame_left, text='Dag-N-Drop Quoteform Below', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(fill=BOTH, expand=True)
textarea.pack(fill=BOTH, anchor=N, expand=True)
Label(frame_left, text='Dag-N-Drop Extra Attachments Below', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(fill=BOTH, expand=True)
attachmentsarea.pack(fill=X, expand=True, anchor=N)
# Make both Text boxes be drag-n-droppable, and register the path of the quoteform and attachments
textarea.drop_target_register(DND_FILES)
textarea.dnd_bind('<<Drop>>', Get_Path)
attachmentsarea.drop_target_register(DND_FILES)
attachmentsarea.dnd_bind('<<Drop>>', path_to_additional_attachments)
# frame_middle ->DECLARE VARIABLES, FUNCTIONS, & PACK
addNotes_labelframe.pack(fill=X, expand=False, side='top')
additional_email_body_notes.pack(fill = X, anchor=N, expand=FALSE, side='top')
cc_labelframe.pack(fill=X, expand=True, side='top')
Label(cc_labelframe, text='email address to CC:', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(fill=X, expand=True, side='top')
cc_address_1_user_input.pack(pady=2, ipady=4, anchor=N, fill = X, expand=True, side='top')
Label(cc_labelframe, text='email address to CC:', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(fill=X, expand=True, side='top')
cc_address_2_user_input.pack(ipady=4, anchor=N, fill = X, expand=True, side='top')
# frame_right ->DECLARE VARIABLES, FUNCTIONS, & PACK
seawave.pack(ipady=3, fill=BOTH, expand=True)
primetime.pack(ipady=3, fill=BOTH, expand=True)
newhampshire.pack(ipady=3, fill=BOTH, expand=True)
americanmodern.pack(ipady=3, fill=BOTH, expand=True)
kemah.pack(ipady=3, fill=BOTH, expand=True)
concept.pack(ipady=3, fill=BOTH, expand=True)
yachtinsure.pack(ipady=3, fill=BOTH, expand=True)
century.pack(ipady=3, fill=BOTH, expand=True)
intact.pack(ipady=3, fill=BOTH, expand=True)
travelers.pack(ipady=3, fill=BOTH, expand=True)
Button(frame_right, text='Submit and sent to markets!', bg='#22c26a', font=('helvetica', 12, 'normal'), command=sameCarrierSubmission).pack(ipady=20, pady=10, anchor=S, fill=BOTH, expand=True)
#-----------------EMAIL_TEMPLATE TAB-------------------------
e_frame_header_spacer.pack(fill=X, expand=False)
e_frame_header.pack(padx=5, fill = X, expand=True)
e_frame_top.pack(fill=BOTH, expand=False)
e_frame_content.pack(fill=BOTH, expand=False, anchor=N)
e_frame_bottomL.pack(fill=X, expand=True, side='left', anchor=N)
e_frame_bottomR.pack(fill=X, expand=True, side='left', anchor=N)
# Install a trace on the dropdown selection to update the template placeholder texts each time it changes 
dropdown_email_template.trace_add('write', updateCarrierChoice)
# Continue creating GUI
Label(e_frame_header, text = 'Adjust the Default Email Templates for Each Carrier', bg='#5F9EA0', font=('helvetica', 16, 'normal')).pack(fill = X, expand=True, side='top')
Label(e_frame_header, text = 'Your name (used in Signature):', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(padx=4, pady=5, fill=BOTH, expand=True, side='left', anchor=E)
your_name.pack(ipadx=900, pady=5, fill=BOTH, expand=True, side='right', anchor=NW)
Label(e_frame_top, text = "This drop-down menu allows you to view & edit a specific carrier's, or combo carriers', email message contents.", bg='#5F9EA0', font=('helvetica', 10, 'normal')).pack(fill = X, expand=True)
drop.pack(padx=15, ipady=5, fill = X, expand=True)
Label(e_frame_bottomL, text = 'Submission Address:', bg='#aedadb', font=('helvetica', 16, 'normal')).pack(padx=2, pady=15, fill=BOTH, expand=True, anchor=E, side='top')
carrier_address.pack(padx=4, pady=15, ipadx=160, ipady=5, fill=BOTH, expand=False, side='top')
Label(e_frame_bottomL, text = 'Greeting:', bg='#aedadb', font=('helvetica', 16, 'normal')).pack(padx=2, fill=BOTH, expand=True, anchor=E, side='top')
carrier_greeting.pack(padx=4, pady=1, ipadx=160, ipady=5, fill=BOTH, expand=False, side='top')
Label(e_frame_bottomL, text = 'Body of the email:', bg='#aedadb', font=('helvetica', 16, 'normal')).pack(padx=2, pady=15, fill=BOTH, expand=True, anchor=E, side='top')
carrier_body.pack(padx=4, pady=15, ipadx=160, ipady=5, fill=BOTH, expand=False, side='top')
Label(e_frame_bottomL, text = 'Salutation:', bg='#aedadb', font=('helvetica', 16, 'normal')).pack(padx=2, pady=63, fill=BOTH, expand=True, anchor=E, side='top')
carrier_salutation.pack(padx=4, ipadx=160, ipady=5, fill=BOTH, expand=False, side='top')
button = Button(e_frame_bottomR, text = 'Click to SAVE template for this market, & save your name!', bg='#22c26a', command = btnSaveCarrierTemplate).pack(padx=4, pady=20, ipady=50, fill=X, expand=False, anchor=S, side='bottom')
#-------------------SETTINGS TAB------------------
Label(settings, text='Settings Page', bg='#5F9EA0', font=('helvetica', 20, 'normal')).pack(fill=BOTH, expand=False, side='top')
Label(settings, text='CC-address Settings (more to be added later or upon your request)', bg='#5F9EA0', font=('helvetica', 14, 'normal')).pack(fill=X, expand=False, side='top')
entry_boxes_frame.pack(fill=BOTH, expand=False, side='top')
save_btn_frame.pack(fill=BOTH, expand=False, side='top')
Label(entry_boxes_frame, text='1st address to set as default cc: ', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(pady=3, ipady=2, padx=1, fill='none', expand=False, side='left', anchor=NW)
defaultCCaddress1.pack(pady=3, fill=X, ipadx=10, ipady=4, expand=True, side='left', anchor=N)
Label(entry_boxes_frame, text='2nd address to set as default cc: ', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(pady=3, ipady=2, padx=1, fill='none', expand=False, side='left', anchor=NW)
defaultCCaddress2.pack(pady=3, fill=X, ipadx=10, ipady=4, expand=True, side='left', anchor=N)
Button(save_btn_frame, text='Save Settings!', bg='#22c26a', font=('helvetica', 12, 'normal'), command=btnSaveMainSettings).pack(ipady=10, pady=10, padx=10, fill=BOTH, expand=False, anchor=N, side='top')
#---------END OF DECLARATIONS---BEGIN TKINTER FUNCTIONS---------#

#SETTING THE WINDOW TO CENTER
# get the screen dimension
#screen_width = root.winfo_screenwidth()
#screen_height = root.winfo_screenheight()

# find the center point
#center_x = int(screen_width/2 - window_width / 2)
#center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
#root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}') 

root.mainloop()
