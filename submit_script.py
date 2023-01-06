import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Notebook, Style
from tkinter import * 
from tkinterdnd2 import *
import fillpdf
from helper import *

#Global variables
settings_merge_cc_addresses = int
attachments = []
last_name = ''
first_name = ''
year = 0
make = ''
length = 0
#-----------------------

#Functions--------------
#SETTINGS - Save & update
def btn_save_carrier_template():
    updater = update_config()
    try:
        carrier = dropdown_email_template.get()
        if carrier!='Combo SW and PT' or 'Combo SW and NH' or 'Combo SW, PT and NH' or 'Combo SW, PT and NH':
            if carrier=='Seawave':
                carrier = 'SW email'
            if carrier=='Prime Time':
                carrier = 'PT email'
            if carrier=='New Hampshire':
                carrier = 'NH email'
            if carrier=='American Modern':
                carrier = 'AM email'
            if carrier=='Kemah':
                carrier = 'KM email'
            if carrier=='Concept':
                carrier = 'CP email'
            if carrier=='Yachtinsure':
                carrier = 'YI email'
            if carrier=='Century':
                carrier = 'CE email'
            if carrier=='Intact':
                carrier = 'IN email'
            if carrier=='Travelers':
                carrier = 'TV email'
            updater[carrier]['address'].value = carrier_address.get()
            updater[carrier]['greeting'].value = carrier_greeting.get()
            updater[carrier]['body'].value = carrier_body.get()
            updater[carrier]['salutation'].value = carrier_salutation.get()
        else:
            if carrier=='Combo SW and PT':
                carrier = 'Combo email'
                key = 'sw_and_pt_body'
                updater[carrier][key].value = carrier_body.get()
            if carrier=='Combo SW and NH':
                carrier = 'Combo email'
                key = 'sw_and_nh_body'
                updater[carrier][key].value = carrier_body.get()
            if carrier=='Combo SW, PT and NH':
                carrier = 'Combo email'
                key = 'pt_and_nh_body'
                updater[carrier][key].value = carrier_body.get()
            if carrier=='Combo PT and NH':
                carrier = 'Combo email'
                key = 'pt_and_nh_and_sw_body'
                updater[carrier][key].value = carrier_body.get()
        updater['General settings']['your_name'].value = your_name.get()
    except:
        print('save carrier template to config file FAILED!')

def btnSaveMainSettings():
    updater = update_config()
    updater["CC-address Settings"]["settings_merge_cc_addresses"].value = settings_merge_cc_addresses.get()
    updater["CC-address Settings"]["def_cc_address_1"].value = def_cc_address_1.get()
    updater["CC-address Settings"]["def_cc_address_2"].value = def_cc_address_2.get()

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
    msg_subject = f"{last_name}, {first_name} | {year} {make} {length} | New Quote Submission"
    return msg_subject

def Get_Add_Notes():
    additional_notes = additional_email_body_notes.get()
    return additional_notes

def Get_CC_Addresses():
    config = read_config()
    cc_addresses = [cc_address_1_user_input.get(), cc_address_2_user_input.get()]
    if config.get('CarbonCopy Settings', 'settings_merge_cc_addresses')=='0':
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
    str1 = ""
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
    <meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
    <meta name="ProgId" content="Word.Document">
    <meta name="Generator" content="Microsoft Word 15">
    <meta name="Originator" content="Microsoft Word 15">
    </head>
    <body>
    <p style="font-size=14px;color:#1F3864">%s</p>
    <p style="font-size=14px;color:#1F3864">%s %s</p><br>
    </body>
    <footer>
    <p style='margin:0in;font-size:14px;font-family:Calibri,sans-serif;color:#1F3864;'>%s</p>
    <p style='margin:0in;font-size=14px;font-family:Calibri,sans-serif;color:#1F3864;'>%s</p><br>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Main:(800)-823-2798</p>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Office :(941)-444-5099</p>
    <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Fax:(941)-328-3598</p><br>
    <p style='margin:0in;color:#0563C1;text-decoration:underline;text-underline:single;font-size:12px;font-family:Georgia Pro,serif;'>1549 Ringling Blvd., Suite 101</p>
    <p style='margin:0in;color:#0563C1;text-decoration:underline;text-underline:single;font-size:12px;font-family:Georgia Pro,serif;'>Sarasota, FL 34236</p><br>
    <p style='margin:0in;color:#1F3864;font-size:10.0pt;font-family:Georgia Pro,serif;color:blue;'><a href="http://www.novamarinsurance.com/" target="_blank">www.novamarinsurance.com</a></p>
    <p style='margin:0in;color:#1F3864;font-size:10.0pt;font-family:Georgia Pro,serif;color:blue;'><a href="http://www.novamarinsurance.com.mx/" target="_blank">www.novamarinsurance.com.mx</a></p>

    <p style'margin:0in'><a href="https://www.facebook.com/NovamarInsurance" target="_blank"><img width=24 height=24 src="https://cdn1.iconfinder.com/data/icons/social-media-2285/512/Colored_Facebook3_svg-512.png"></a>  <a href="https://www.instagram.com/novamar_insurance/" target="_blank"><img width=24 height=24 src="https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Instagram_colored_svg_1-512.png" style="display:block"></a>  <a href="https://twitter.com/NovamarIns" target="_blank"><img width=24 height=24 src="https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Twitter3_colored_svg-512.png" style="display:block"></a>  <a href="https://www.linkedin.com/company/novamar-insurance-group-inc" target="_blank"><img width=24 height=24 src="https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Linkedin_unofficial_colored_svg-512.png" style="display:block"></a></p>
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
root.geometry('690x500')
root.configure(background='#5F9EA0')
root.title('Quote Submissions Tool')
root.attributes('-alpha',0.84)
#use below to replace title icon when ready
#root.iconbitmap('./assets/example.ico') 
#TabControl
tabControl = ttk.Notebook(root)
main = ttk.Frame(tabControl)
template_settings = ttk.Frame(tabControl)
settings = ttk.Frame(tabControl)
tabControl.add(main, text='Main')
tabControl.add(template_settings, text='Templates')
tabControl.add(settings, text='Settings')
tabControl.pack(expand=1, fill="both")
#tkinter modules by tab
#main

frame3 = Frame(main)
frame3.grid(row=0, rowspan=10, column=3)

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

textarea = Text(main, height=4, width=25)
textarea.grid(row=2, column=0, pady=10)
textarea.drop_target_register(DND_FILES)
textarea.dnd_bind('<<Drop>>', Get_Path)
attachmentsarea = Text(main, height=4, width=25)
attachmentsarea.grid(row=5, column=0, pady=10)
attachmentsarea.drop_target_register(DND_FILES)
attachmentsarea.dnd_bind('<<Drop>>', path_to_additional_attachments)

Label(main, text='Input Client Information', bg='#5F9EA0', font=('helvetica', 16, 'normal')).grid(row=0, column=0, pady=25)
Label(main, text='Dag-N-Drop Quoteform Below', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=1, column=0)
Label(main, text='Dag-N-Drop Additional Attachments Below', bg='#5F9EA0', font=('helvetica', 10, 'normal')).grid(row=4, column=0)
Label(main, text='Additional e-mail Notes', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=1, column=1)
Label(main, text='CC-Address 1:', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=4, column=1, pady=10)
Label(main, text='CC-Address 2:', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=7, column=1, pady=15) 
Label(main, text='Additional Notes/CC', bg='#5F9EA0', font=('helvetica', 16, 'normal')).grid(row=0, column=1, pady=25)
Label(frame3, text='Markets to Submit to:', bg='#5F9EA0', font=('helvetica', 16, 'normal')).grid(row=0, column=3, pady=15)

seawave = Checkbutton(frame3, text='Seawave Insurance', variable=seawave_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
seawave.grid(row=1, column=3)
primetime = Checkbutton(frame3, text='Prime Time Insurance', variable=primetime_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
primetime.grid(row=2, column=3, pady=5)
newhampshire = Checkbutton(frame3, text='New Hampshire', variable=newhampshire_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
newhampshire.grid(row=3, column=3)
americanmodern = Checkbutton(frame3, text='American Modern', variable=americanmodern_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
americanmodern.grid(row=4, column=3, pady=5)
kemah = Checkbutton(frame3, text='Kemah Marine', variable=kemah_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
kemah.grid(row=5, column=3)
concept = Checkbutton(frame3, text='Concept Special ', variable=concept_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
concept.grid(row=6, column=3, pady=5)
yachtinsure = Checkbutton(frame3, text='Yachtinsure', variable=yachtinsure_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
yachtinsure.grid(row=7, column=3)
century = Checkbutton(frame3, text='Century Insurance', variable=century_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
century.grid(row=8, column=3, pady=5)
intact = Checkbutton(frame3, text='Intact', variable=intact_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
intact.grid(row=9, column=3)
travelers = Checkbutton(frame3, text='Travelers', variable=travelers_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
travelers.grid(row=10, column=3, pady=5)

additional_email_body_notes = Entry(main)
additional_email_body_notes.grid(row=2, column=1, pady=5)
cc_address_1_user_input = Entry(main)
cc_address_1_user_input.grid(row=5, column=1)
cc_address_2_user_input = Entry(main)
cc_address_2_user_input.grid(row=8, column=1)

Button(frame3, text='Submit and sent to markets!', bg='#7FFFD4', font=('helvetica', 12, 'normal'), command=sameCarrierSubmission).grid(row=11, column=3, pady=10)

#settings
cc_merge_0 = Radiobutton(settings, text="Add user input to the below.", variable=settings_merge_cc_addresses, value='0')
cc_merge_0.grid(row=3, column=0)
cc_merge_1 = Radiobutton(settings, text="Replace the below with user input.", variable=settings_merge_cc_addresses, value='1')
cc_merge_1.grid(row=4, column=0)
def_cc_address_1 = Entry(settings)
def_cc_address_1.grid(row=6, column=0)
def_cc_address_2 = Entry(settings)
def_cc_address_2.grid(row=8, column=0)

Label(settings, text='Settings Page', bg='#5F9EA0', font=('helvetica', 16, 'normal')).grid(row=0, column=0, columnspan=2, pady=10)
Label(settings, text='General Settings', bg='#5F9EA0', font=('helvetica', 14, 'normal')).grid(row=1, column=0, pady=10)
Label(settings, text='Preference on merging CC-addresses:', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=2, column=0, pady=10)
Label(settings, text='Insert address to always CC', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=5, column=0, pady=10)
Label(settings, text='Insert another address to CC', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=7, column=0, pady=10)

Button(settings, text='Save Settings!', bg='#7FFFD4', font=('helvetica', 12, 'normal'), command=btnSaveMainSettings).grid(row=11, column=3, pady=10)

#email_template
Label(template_settings, text = 'Email Template Adjustment', bg='#5F9EA0', font=('helvetica', 16, 'normal')).grid(row=0, column=0, pady=10)
Label(template_settings, text = 'Select a specific market, or one of the combo options, to change the template for the email message.', bg='#5F9EA0', font=('helvetica', 14, 'normal')).grid(row=1, column=0, columnspan=3, pady=10)

options = [
	"Select Carrier"
    "Seawave",
    "Prime Time",
    "New Hampshire",
    "American Modern",
    "Kemah",
    "Concept",
    "Yachtinsure"
	"Century"
	"Intact"
	"Travelers"
	"Combo SW and PT"
	"Combo SW and NH"
	"Combo SW, PT and NH"
	"Combo PT and NH"
]
dropdown_email_template = StringVar()
dropdown_email_template.set('Select Carrier')
drop = OptionMenu(template_settings, dropdown_email_template, *options)
drop.grid(row=2, column=1)

Label(template_settings, text = 'Submission Address: ', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=3, column=0, pady=10)
Label(template_settings, text = 'Greeting: ', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=4, column=0, pady=10)
Label(template_settings, text = 'Body of the email: ', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=5, column=0, pady=10)
Label(template_settings, text = 'Salutation: ', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=8, column=0, pady=10)
Label(template_settings, text = 'Your name: ', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=9, column=0, pady=10)
carrier_address = Entry(template_settings)
carrier_address.grid(row=3, column=1)
carrier_greeting = Entry(template_settings)
carrier_greeting.grid(row=4, column=1, columnspan=2)
carrier_body = Entry(template_settings)
carrier_body.grid(row=5, column=1, columnspan=2)
carrier_salutation = Entry(template_settings)
carrier_salutation.grid(row=8, column=1, columnspan=2)
your_name = Entry(template_settings)
your_name.grid(row=9, column=1)

button = Button(settings, text = "Save!", command = btn_save_carrier_template).grid(row=4, column=1)

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
