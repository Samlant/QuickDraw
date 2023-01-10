import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Notebook, Style
from tkinter import * 
from tkinterdnd2 import *
import fillpdf
from fillpdf import fillpdfs
from helper import *

#Global variables
attachments = []
last_name = ''
first_name = ''
year = 0
make = ''
length = 0
#-----------------------

#Functions--------------
#SETTINGS - Save & update
def btnSaveCarrierTemplate(carrier):
    config = update_config()
    carrier_tuple = assignCorrectCarrierNames(carrier)
    section_name = carrier_tuple[0]
    if carrier_tuple[0]=='Select Carrier':
        pass
    elif carrier_tuple[1]==0:
        config[section_name]['address'].value = carrier_address.get()
        config[section_name]['greeting'].value = carrier_greeting.get()
        config[section_name]['body'].value = carrier_body.get()
        config[section_name]['salutation'].value = carrier_salutation.get()
    else:
        key = carrier_tuple[1]
        config[section_name][key].value = carrier_body.get()
  
def btnSaveMainSettings():
    updater = update_config()
    updater['CarbonCopy Settings']['settings_merge_cc_addresses'].value = settings_merge_cc-addresses.get()
    updater['CarbonCopy Settings']['def_cc_address_1'].value = def_cc_address_1.get()
    updater['CarbonCopy Settings']['def_cc_address_2'].value = def_cc_address_2.get()

#Helper Functions
def assignCorrectCarrierNames(carrier):
    carrier_tuple = tuple()
    if carrier!='Combo SW and PT' or 'Combo SW and NH' or 'Combo SW, PT and NH' or 'Combo SW, PT and NH':
        if carrier=='Seawave':
            carrier = 'SW email'
        elif carrier =='Prime Time':
            carrier = 'PT email'
        elif carrier=='New Hampshire':
            carrier = 'NH email'
        elif carrier=='American Modern':
            carrier = 'AM email'
        elif carrier=='Kemah':
            carrier = 'KM email'
        elif carrier=='Concept':
            carrier = 'CP email'
        elif carrier=='Yachtinsure':
            carrier = 'YI email'
        elif carrier=='Century':
            carrier = 'CE email'
        elif carrier=='Intact':
            carrier = 'IN email'
        elif carrier=='Travelers':
            carrier = 'TV email'
        carrier_tuple = (carrier, 0)
    else:
        if carrier=='Combo SW and PT':
            carrier = 'Combo email'
            key = 'sw_and_pt_body'
        elif carrier=='Combo SW and NH':
            carrier = 'Combo email'
            key = 'sw_and_nh_body'
        elif carrier=='Combo SW, PT and NH':
            carrier = 'Combo email'
            key = 'pt_and_nh_body'
        elif carrier=='Combo PT and NH':
            carrier = 'Combo email'
            key = 'pt_and_nh_and_sw_body'
        carrier_tuple = (carrier, key)
    return carrier_tuple

def updateCarrierChoice():
    current_selection = dropdown_email_template.get()
    if 'Combo' in current_selection:
        carrier_address.configure(state='disabled')
        carrier_greeting.configure(state='disabled')
        carrier_salutation.configure(state='disabled')
    else:
        carrier_address.configure(state='normal')
        carrier_greeting.configure(state='normal')
        carrier_salutation.configure(state='normal')        


#End of SETTINGS#

# Helper Functions------------------
def Get_Path(event):
	if '{' in event.data:
		Get_Path.quoteform_path = ''
		Get_Path.quoteform_path = event.data.translate({ord(c): None for c in '{}'})
		print(Get_Path.quoteform_path)
	else:
		Get_Path.quoteform_path = event.data
		print(Get_Path.quoteform_path)
		listToString(Get_Path.quoteform_path)
		print(Get_Path.quoteform_path)
	return Get_Path.quoteform_path

def Get_Subject():
    needed_values_dict = fillpdfs.get_form_fields(Get_Path.quoteform_path)
    needed_values_dict = {key: needed_values_dict[key] for key in needed_values_dict.keys()
       & {'4669727374204e616d65', '4c617374204e616d65', 'Year', '4d616b6520616e64204d6f64656c', 'Length'}}
    first_name = needed_values_dict.get('4669727374204e616d65')
    last_name = needed_values_dict.get('4c617374204e616d65')
    year = needed_values_dict.get('Year')
    make = needed_values_dict.get('4d616b6520616e64204d6f64656c')
    length = needed_values_dict.get('Length')
    msg_subject = f'{last_name}, {first_name} | {year} {make} {length} | New Quote Submission'
    return msg_subject

def Get_Add_Notes():
    additional_notes = additional_email_body_notes.get()
    return additional_notes

def Get_CC_Addresses(): #NEED TO REVISE HOW WE KEEP ADDRESS...It gets replaced with 'None'
    config = read_config()
    cc_addresses = [cc_address_1_user_input.get(), cc_address_2_user_input.get()]
    if cc_default_check.get()=='0':
        try:
            cc_addresses.append(config.get('CarbonCopy Settings', ''), config.get('CarbonCopy Settings', ''))
        except:
            print('The cc append didnt work, trying the other way...')
            try:
                cc_addresses.append(config.get('CarbonCopy Settings', ''))
                cc_addresses.append(config.get('CarbonCopy Settings', ''))
                print('Done.')
            except:
                print('Not successful in saving CC addresses')
        return cc_addresses

def path_to_additional_attachments(event):
	if '{' in event.data:
		attachments.append(event.data.translate({ord(c): None for c in '{}'}))
	else:
		attachments.append(event.data)
	return attachments

def listToString(s):
    str1 = ''
    for element in s:
        str1 += element
    return str1

def passing():
	pass

				    
#MAIN FUNCTIONS-------|
def sameCarrierSubmission():
    config = read_config()
    dict0 = [seawave_check.get(), primetime_check.get(), newhampshire_check.get()]
    if dict0[0]==1 and dict0[1]==1 and dict0[2]==0:
        address = config.get('SW email', 'address')
        greeting = config.get('SW email', 'greeting')
        body = config.get('Combo email', 'sw_and_pt_body')
        salutation = config.get('SW email', 'salutation')
        your_name = config.get('General settings', 'your_name')
    elif dict0[0]==1 and dict0[1]==0 and dict0[2]==1:
        address = config.get('SW email', 'address')
        greeting = config.get('SW email', 'greeting')
        body = config.get('Combo email', 'sw_and_nh_body')
        salutation = config.get('SW email', 'salutation')
        your_name = config.get('General settings', 'your_name')
    elif dict0[0]==1 and dict0[1]==1 and dict0[2]==1:
        address = config.get('SW email', 'address')
        greeting = config.get('SW email', 'greeting')
        body = config.get('Combo email', 'pt_and_nh_and_sw_body')
        salutation = config.get('SW email', 'salutation')
        your_name = config.get('General settings', 'your_name')
    elif dict0[1]==1 and dict0[2]==1:
        address = config.get('SW email', 'address')
        greeting = config.get('SW email', 'greeting')
        body = config.get('Combo email', 'pt_and_nh_body')
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
    add_notes = Get_Add_Notes()
    mail = outlook.CreateItem(0)
    mail.Subject = Get_Subject()
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


# This is the section of code which creates the main window

root = Tk()
root.geometry('760x548')
root.configure(background='#5F9EA0')
root.title('Quote Submissions Tool')
root.attributes('-alpha',0.95)
#use below to replace title icon when ready
#root.iconbitmap('./assets/example.ico') 

#Creating and Styling Tabs on main window

# Create an instance of ttk style
style = Style()
style.theme_use('default')
style.configure('TNotebook', background='#5F9EA0')
style.configure('TFrame', background='#5F9EA0')
style.map('TNotebook', background= [('selected', '#5F9EA0')])
#Create tabs
tabControl = ttk.Notebook(root)
#tabControl.configure(bg='#5F9EA0')
main = ttk.Frame(tabControl)
template_settings = ttk.Frame(tabControl)
settings = ttk.Frame(tabControl)
tabControl.add(main, text='Main')
tabControl.add(template_settings, text='Templates')
tabControl.add(settings, text='Settings')
tabControl.pack(expand=1, fill='both')

#tkinter modules by tab

#MAIN TAB

frame_header = Frame(main, bg='#5F9EA0', pady=17)
frame_left = Frame(main, bg='#5F9EA0')
frame_middle = Frame(main, bg='#5F9EA0')
frame_right = Frame(main, bg='#5F9EA0')
frame_header.pack(padx=5, fill=X, expand=False)
frame_left.pack(padx=5, fill = Y, side='left', expand = False, anchor=NE)
frame_middle.pack(padx=5, fill = Y, side='left', expand = False, anchor=N)
frame_right.pack(padx=5, fill = Y, side='left', expand = False, anchor=NW)

#DECLARE VARIABLES THEN PACKING OF frame_left ELEMENTS

textarea = Text(frame_left, height=7, width=27, background='#59f3e3')
attachmentsarea = Text(frame_left, height=9, width=27, background='#59f3e3')


Label(frame_header, text='Get Client Information', bg='#5F9EA0', font=('helvetica', 20, 'normal')).pack(fill=X, expand=True, side='left')
Label(frame_header, text='Extra Notes & CC', bg='#5F9EA0', font=('helvetica', 20, 'normal')).pack(fill=X, expand=True, side='left')
Label(frame_header, text='Choose Markets:', bg='#5F9EA0', font=('helvetica', 20, 'normal')).pack(fill=X, expand=True, side='left')
Label(frame_left, text='Dag-N-Drop Quoteform Below', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(fill=BOTH, expand=True)
textarea.pack(fill=BOTH, anchor=N, expand=True)
Label(frame_left, text='Dag-N-Drop Extra Attachments Below', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(fill=BOTH, expand=True)
attachmentsarea.pack(fill=X, expand=True, anchor=N)

textarea.drop_target_register(DND_FILES)
textarea.dnd_bind('<<Drop>>', Get_Path)
attachmentsarea.drop_target_register(DND_FILES)
attachmentsarea.dnd_bind('<<Drop>>', path_to_additional_attachments)

#DECLARE VARIABLES THEN PACKING OF frame_middle ELEMENTS
addNotes_labelframe = LabelFrame(frame_middle, text= 'To end with a message, enter it below:', bg='#aedadb', font=('helvetica', 8, 'normal'))
cc_labelframe = LabelFrame(frame_middle, text= 'CC-address settings for this submission:', bg='#aedadb')
cc_default_check = tk.IntVar()
additional_email_body_notes = Text(addNotes_labelframe, height=7, width=30)
cc_address_1_user_input = Text(cc_labelframe, height=1, width=30)
cc_address_2_user_input = Text(cc_labelframe, height=1, width=30)

addNotes_labelframe.pack(fill=X, expand=False, side='top')
additional_email_body_notes.pack(fill = X, anchor=N, expand=FALSE, side='top')
cc_labelframe.pack(fill=X, expand=True, side='top')
cc_default_check = Checkbutton(cc_labelframe, text='Check to ignore default CC-addresses.', variable=cc_default_check, bg='#aedadb').pack(pady=5, fill=X, expand=False, side='top')
Label(cc_labelframe, text='email address to CC:', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(fill=X, expand=True, side='top')
cc_address_1_user_input.pack(pady=2, ipady=4, anchor=N, fill = X, expand=True, side='top')
Label(cc_labelframe, text='email address to CC:', bg='#aedadb', font=('helvetica', 12, 'normal')).pack(fill=X, expand=True, side='top')
cc_address_2_user_input.pack(ipady=4, anchor=N, fill = X, expand=True, side='top')

#DECLARE VARIABLES THEN PACKING OF frame_right ELEMENTS

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

options = [
	'Select Carrier'
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
e_frame_header_spacer = Frame(template_settings, bg='#5F9EA0', height=17)
e_frame_header = Frame(template_settings, bg='#5F9EA0')
e_frame_top = Frame(template_settings, bg='#5F9EA0')
e_frame_content = Frame(template_settings, bg='#5F9EA0')
e_frame_bottomL = Frame(template_settings, bg='#5F9EA0' )
e_frame_bottomR = Frame(template_settings, bg='#5F9EA0')
e_frame_header_spacer.pack(fill=X, expand=False)
e_frame_header.pack(padx=5, fill = X, expand=True)
e_frame_top.pack(fill=BOTH, expand=False)
e_frame_content.pack(fill=BOTH, expand=False, anchor=N)
e_frame_bottomL.pack(fill=X, expand=True, side='left', anchor=N)
e_frame_bottomR.pack(fill=X, expand=True, side='left', anchor=N)


dropdown_email_template = StringVar()
dropdown_email_template.trace_add('write', updateCarrierChoice)
dropdown_email_template.set('Select Carrier')
drop = OptionMenu(e_frame_top, dropdown_email_template, *options)
drop.configure(background='#aedadb', foreground='black', highlightbackground='#5F9EA0', activebackground='#5F9EA0')
drop['menu'].configure(background='#aedadb')
your_name = Entry(e_frame_header)

carrier_address = Entry(e_frame_bottomR)
carrier_greeting = Entry(e_frame_bottomR)
carrier_body = Text(e_frame_bottomR, width=10, height=5)
carrier_salutation = Entry(e_frame_bottomR, width=27, highlightbackground='green', highlightcolor='red')

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
button = Button(e_frame_bottomR, text = 'Save template for this carrier choice!', command = btnSaveCarrierTemplate(dropdown_email_template.get())).pack(padx=4, pady=20, ipady=50, fill=X, expand=False, anchor=S, side='bottom')
#REPLACE THE ABOVE BTN COMMAND'S PARAMETER WITH THE VARIABLE dropdown_email_template#
#-------------------SETTINGS TAB------------------
settings_merge_cc_addresses = IntVar()
def_cc_address_1 = Entry(settings)
def_cc_address_2 = Entry(settings)
cc_merge_0 = Radiobutton(settings, text='Add user input to the below.', variable=settings_merge_cc_addresses, value='0')
cc_merge_1 = Radiobutton(settings, text='Replace the below with user input.', variable=settings_merge_cc_addresses, value='1')

cc_merge_0.grid(row=3, column=0)
cc_merge_1.grid(row=4, column=0)
def_cc_address_1.grid(row=6, column=0)
def_cc_address_2.grid(row=8, column=0)

Label(settings, text='Settings Page', bg='#5F9EA0', font=('helvetica', 16, 'normal')).grid(row=0, column=0, columnspan=2, pady=10)
Label(settings, text='CC-address Settings (more to be added later or upon your request)', bg='#5F9EA0', font=('helvetica', 14, 'normal')).grid(row=1, column=0, pady=10)
Label(settings, text='If you find yourself wanting to CC the same people on most quote submissions,  enter their email address below.  This will CC them on all outgoing emails, UNLESS you check the "ignore default CC addresses" checkbox on the front page!', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=2, column=0, pady=10)
Label(settings, text='If desired, enter an address to always CC:', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=5, column=0, pady=10)
Label(settings, text='If desired, enter an address to always CC:', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=7, column=0, pady=10)

Button(settings, text='Save Settings!', bg='#7FFFD4', font=('helvetica', 12, 'normal'), command=btnSaveMainSettings).grid(row=11, column=3, pady=10)


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
