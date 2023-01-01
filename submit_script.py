import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Notebook, Style
from tkinter import * 
from tkinterdnd2 import *
import fillpdf as fillpdf
from helper import *
#import .ini file via *update* (preferred) ..or.. helper.py scripts

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


def path_to_additional_attachments(event):
	if '{' in event.data:
		attachments.append(event.data.translate({ord(c): None for c in '{}'}))
	else:
		attachments.append(event.data)
	print(attachments)
	return attachments

def listToString(s):
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += ele
    # return string
    return str1

def passing():
	pass

	# this is the function to check the status of each checkbox (1 means checked, and 0 means unchecked)

def getCarrierValues():
	import basic_tests
	sw = [(seawave_check.get()), (config.get('SW email', 'sw_address'))]
	print(sw)
	pt = [primetime_check.get(), 'boatprograms@one80intermediaries.com', 'Hey Boat Programs,', 'Please see the attached for a new quote submission for the Prime Time market. Thank you in advance for your consideration of our client. ']
	nh = [newhampshire_check.get(), 'boatprograms@one80intermediaries.com', 'Hey Boat Programs,', 'Please see the attached for a new quote submission for the New Hampshire market. Thank you in advance for your consideration of our client. ']
	am = (americanmodern_check.get(), 'boatbrokerage@one80intermediaries.com', 'Hey BoatBrokerage,', 'Please see the attached for a new quote submission for the American Modern market.  Also submitting with paid-in-full + paperless + homeowners discounts to apply. Thank you in advance for your consideration of our client. ')
	km = (kemah_check.get(), 'tom_carroll@kemah_marine.com', 'Hey Tom,', 'Please see the attached for a new quote submission. Thank you in advance for your consideration of our client. ')
	cp = (concept_check.get(), 'quote.team@special-risks.co.uk', 'Hey Concept Quote team,', 'Please see the attached for a new quote submission. Thank you in advance for your consideration of our client. ')
	yi = (yachtinsure_check.get(), 'quotes@yachtinsure.uk.com', 'Hey Yachtinsure quote team,', 'Please see the attached for a new quote submission. Thank you in advance for your consideration of our client. ') 
	ce = (century_check.get(), 'rsmith@bassuw.com', 'Hey Richard,', 'Please see the attached for a new quote submission. Thank you in advance for your consideration of our client. ')
	in_ = (intact_check.get(), 'yucusa@intactinsurance.com', 'Hey Intact,', 'Please see the attached for a new quote submission. Thank you in advance for your consideration of our client. ')
	tv = (travelers_check.get(), 'mzadrick@travelers.com', 'Hey Mark,', 'Please see the attached for a new quote submission. Thank you in advance for your consideration of our client. ')
	#tv = (travelers_check.get(), 'sam@novamar.net', 'Hey Mark', 'Please see the attached for a new quote submission.')
	if sw[0]==1 and pt[0]==1 and nh[0]==0:
		pt[0] = 0
		sw[3] = updater['Combo email']['sw_and_pt_body']
	elif sw[0]==1 and pt[0]==0 and nh[0]==1:
		nh[0] = 0
		sw[3] = ' for both the Seawave and New Hampshire markets.'
	elif sw[0]==1 and pt[0]==1 and nh[0]==1:
		pt[0] = 0
		nh[0] = 0
		sw[3] = ' for the Seawave, Prime Time, & New Hampshire markets.'
	elif pt[0]==1 and nh[0]==1:
		nh[0] = 0
		pt[3] = ' for both the Prime Time and New Hampshire markets.'
	else:
		passing
	return (sw, pt, nh, am, km, cp, yi, ce, in_, tv)


def Get_Add_Notes():
	additional_notes = additional_email_body_notes.get()
	return additional_notes

def Get_CC_Addresses():
	if settings_merge_cc_addresses=='0':
		#insert default addresses from config
		cc_1 = cc_address_1_user_input.get()
		cc_2 = cc_address_2_user_input.get()
		cc_total = f"{def_cc_1}; {cc_1}; {def_cc_2}; {cc_2}"
		print(cc_total)
	else:
		cc_1 = cc_address_1_user_input
		cc_2 = cc_address_2_user_input.get()
		cc_total = f"{cc_1}; {cc_2}"
		print(cc_total)
	return cc_total

# this is the function called when the buttons are clicked:
def btnSave_Settings():
	import update_config
	updater["CC-address Settings"]["settings_merge_cc_addresses"].value = settings_merge_cc_addresses.get()
	updater["CC-address Settings"]["def_cc_address_1"].value = def_cc_address_1.get()
	updater["CC-address Settings"]["def_cc_address_2"].value = def_cc_address_2.get()

def btnClickFunction():
	import win32com.client as win32
	outlook = win32.Dispatch('outlook.application')
#	cc_output = ''
	cc_output = Get_CC_Addresses()
	mail = outlook.CreateItem(0)
	mail.Subject = Get_Subject()
	add_notes = Get_Add_Notes()
	carrier_values = getCarrierValues()
	for i in carrier_values:
		if i[0] == 1:
			mail.To = i[1]
			mail.CC = cc_output
			intro = i[2]
			body = i[3]
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
			<p style='margin:0in;font-size:14px;font-family:Calibri,sans-serif;color:#1F3864;'>With Pleasure,</p>
			<p style='margin:0in;font-size=14px;font-family:Calibri,sans-serif;color:#1F3864;'>Samuel Alexander Lanteigne</p><br>
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
			''' %(intro, body, add_notes)
			mail.Attachments.Add(Get_Path.quoteform_path)
			for attachment in attachments:
				mail.Attachments.Add(attachment)
			mail.Display()
#			mail.Send()

# This is the section of code which creates the main window
root = Tk()
root.geometry('690x500')
root.configure(background='#5F9EA0')
root.title('Quote Submissions Tool')
root.attributes('-alpha',0.84)
#use below to replace title icon when ready
#root.iconbitmap('./assets/example.ico') 

tabControl = ttk.Notebook(root)
main = ttk.Frame(tabControl)
settings = ttk.Frame(tabControl)
tabControl.add(main, text='Main')
tabControl.add(settings, text='Settings')
tabControl.pack(expand=1, fill="both")
#these are the declarations of the variables associated with the checkboxes
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

frame1 = Frame(main, bg='red', padx=2, pady=2)
frame1.place(x=0, y=0)
frame2 = Frame(main, bg='green', padx=2, pady=2)
frame2.place(x=265, y=0)
frame3 = Frame(main, bg='green', padx=2, pady=2)
frame3.place(x=475, y=0)


textarea = Text(frame1, height=4, width=25)
textarea.grid(row=2, column=0, pady=10)
textarea.drop_target_register(DND_FILES)
textarea.dnd_bind('<<Drop>>', Get_Path)

attachmentsarea = Text(frame1, height=4, width=25)
attachmentsarea.grid(row=5, column=0, pady=10)
attachmentsarea.drop_target_register(DND_FILES)
attachmentsarea.dnd_bind('<<Drop>>', path_to_additional_attachments)


# This is the section of code which creates the a labels--------------------------------------------------------------------------------------|
Label(frame1, text='Input Client Information', bg='#5F9EA0', font=('helvetica', 16, 'normal')).grid(row=0, column=0, pady=25)
Label(frame1, text='Dag-N-Drop Quoteform Below', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=1, column=0)
Label(frame1, text='Dag-N-Drop Additional Attachments Below', bg='#5F9EA0', font=('helvetica', 10, 'normal')).grid(row=4, column=0)
Label(frame2, text='Additional e-mail Notes', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=1, column=0)
Label(frame2, text='CC-Address 1:', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=4, column=0, pady=10)
Label(frame2, text='CC-Address 2:', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=7, column=0, pady=15) 
Label(frame2, text='Additional Notes/CC', bg='#5F9EA0', font=('helvetica', 16, 'normal')).grid(row=0, column=0, pady=25)
Label(frame3, text='Markets to Submit to:', bg='#5F9EA0', font=('helvetica', 16, 'normal')).grid(row=0, column=3, pady=15)
#Settings Tab~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Label(settings, text='Settings Page', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=0, column=0, columnspan=2, pady=25)
Label(settings, text='Preference on merging CC-addresses:', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=2, column=0, pady=25)
Label(settings, text='Placeholder setting', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=4, column=0, pady=25)
Label(settings, text='Placeholder setting', bg='#5F9EA0', font=('helvetica', 12, 'normal')).grid(row=5, column=0, pady=25)
#---------------------------------------------------------------------------------------------------------------------------------------------|


#---------------------------------------------------------------------------------------------------------------------------------------------|
# This is the section of code which creates the text input boxes
additional_email_body_notes = Entry(frame2)
additional_email_body_notes.grid(row=2, column=0, pady=5)
cc_address_1_user_input = Entry(frame2)
cc_address_1_user_input.grid(row=5, column=0)
cc_address_2_user_input = Entry(frame2)
cc_address_2_user_input.grid(row=8, column=0)
#Settings Tab~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cc_def_1 = Radiobutton(settings, text="Add user input to the below.", variable=settings_merge_cc_addresses, value='0')
cc_def_1.grid(row=2, column=1)
cc_def_2 = Radiobutton(settings, text="Replace the below with user input.", variable=settings_merge_cc_addresses, value='1')
cc_def_2.grid(row=2, column=1)
#---------------------------------------------------------------------------------------------------------------------------------------------|


# This is the section of code which creates the checkboxes
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

# This is the section of code which creates a button
Button(frame3, text='Submit and sent to markets!', bg='#7FFFD4', font=('helvetica', 12, 'normal'), command=btnClickFunction).grid(row=11, column=3, pady=10)
Button(settings, text='Save Settings!', bg='#7FFFD4', font=('helvetica', 12, 'normal'), command=btnSave_Settings).grid(row=11, column=3, pady=10)


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
