import tkinter as tk
from tkinter import ttk
from tkinter import * 
#import win32com.client as win32

	# this is the function to check the status of each checkbox (1 means checked, and 0 means unchecked)
def getCarrierValues():
#If desired,  can work on creating a list for each carrier...)	
	carrier_to_submit = (seawave_check.get(), primetime_check.get(), newhampshire_check.get(), americanmodern_check.get(), kemah_check.get(), concept_check.get(), yachtinsure_check.get(), century_check.get(), intact_check.get(), travelers_check.get())
#	carrier_address = ('sam@novamar.net', 'sam@novamar.net', 'sam@novamar.net', 'sam@novamar.net', 'sam@novamar.net', 'sam@novamar.net', 'sam@novamar.net', 'sam@novamar.net', 'sam@novamar.net', 'sam@novamar.net')
	carrier_address = ('boatprograms@one80intermediaries.com', 'boatprograms@one80intermediaries.com', 'boatprograms@one80intermediaries.com', 'boatbrokerage@one80intermediaries.com', 'tom_carroll@kemah_marine.com', 'quote@concept_special_risks.co.uk', 'quotes@yachtinsure.co.uk', 'richard@bassuw.com', 'yachtquotes@intact.com', 'yachtquotes@travelers.com')
	carrier_greeting = ('Hey Boat Programs,', 'Hey Boat Programs,', 'Hey Boat Programs,', 'Hey BoatBrokerage,', 'Hey Tom,', 'Hey Concept Quote team,', 'Hey Yachtinsure quote team,', 'Hey there Richard,',  'Hey Intact Quote team,', 'Hey Travelers quote team,')
	carrier_body = (' for the Seawave market.', 'for the Prime Time market.', 'for the New Hampshire market,', 'for the American Modern market.  Also submitting with paid-in-full discount,  paperless, & homeowners discounts to apply.', '.', '.', '.', '.', '.', '.')
#	for cs, ca, cg, cb in zip(carrier_to_submit, carrier_address, carrier_greeting, carrier_body):
#		carrier_values = (cs, ca, cg, cb)

	return carrier_to_submit, carrier_address, carrier_greeting, carrier_greeting

def get_html_msgs():
	add_notes = additional_notes()
	html_msg = '''<html>
					<head>
						<title>New Quote Submission</title>
					</head>
					<body>
						<p>{carrier_greeting},</p>
						<p>Please see the attached for a new quote submission{carrier_body}  Thank you in advance for your consideration of our client.</p>{add_notes}
					</body>
				</html>
				'''

def additional_notes():
         additional_notes = additional_email_body_notes.get()

# this is the function called when the button is clicked
def btnClickFunction():
	#additional_email_body_notes.get()
#	subject_line = f"{last_name.get()}, {first_name.get()} | {year.get()} {make.get()} {length.get()} | New Quote Submission"
	#print(subject_line)
	#(carrier_submit, carrier_address, carrier_greeting, carrier_body) = carrier_values
	carrier_values = ()
	carrier_values = getCarrierValues()
	#for i in range(0, len(carrier_values[0])):
	if carrier_values[0] == 1:
		print(carrier_value[1])
#		if cs == 1:
#			print(i)
#			print(ca)
#			print(cg)
#			print(cb)

		print('Success?')
				#print('This is j: ')
				#print(j)
				#print('This is k: ')
				#print(k)

	


root = Tk()

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

# This is the section of code which creates the main window
root.geometry('750x470')
root.configure(background='#5F9EA0')
root.title('Mass Quote Submissions tool')
root.attributes('-alpha',0.84)
#use below to replace title icon when ready
#root.iconbitmap('./assets/example.ico') 

# This is the section of code which creates the a labels
Label(root, text='Client Information', bg='#5F9EA0', font=('helvetica', 16, 'normal')).place(x=21, y=16)
Label(root, text='First name:', bg='#5F9EA0', font=('helvetica', 12, 'normal')).place(x=41, y=56)
Label(root, text='Last name:', bg='#5F9EA0', font=('helvetica', 12, 'normal')).place(x=41, y=76)
Label(root, text='Boat Details', bg='#5F9EA0', font=('helvetica', 14, 'normal')).place(x=31, y=106)
Label(root, text='Additional e-mail Notes', bg='#5F9EA0', font=('helvetica', 12, 'normal')).place(x=41, y=256) 
Label(root, text='Year:', bg='#5F9EA0', font=('helvetica', 12, 'normal')).place(x=41, y=136)
Label(root, text='Make:', bg='#5F9EA0', font=('helvetica', 12, 'normal')).place(x=41, y=156)
Label(root, text='Length:', bg='#5F9EA0', font=('helvetica', 12, 'normal')).place(x=41, y=176)
Label(root, text='Markets to Submit to:', bg='#5F9EA0', font=('helvetica', 16, 'normal')).place(x=371, y=26)


# This is the section of code which creates the text input boxes
first_name=Entry(root)
first_name.place(x=131, y=56)
first_name.focus()
last_name=Entry(root)
last_name.place(x=131, y=76)
year=Entry(root)
year.place(x=101, y=136)
make=Entry(root)
make.place(x=101, y=156)
length=Entry(root)
length.place(x=101, y=176)
additional_email_body_notes=Entry(root)
additional_email_body_notes.place(x=41, y=276)

# This is the section of code which creates the checkboxes
seawave=Checkbutton(root, text='Seawave Insurance', variable=seawave_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
seawave.place(x=371, y=66)
primetime=Checkbutton(root, text='Prime Time Insurance', variable=primetime_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
primetime.place(x=371, y=96)
newhampshire=Checkbutton(root, text='New Hampshire', variable=newhampshire_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
newhampshire.place(x=371, y=126)
americanmodern=Checkbutton(root, text='American Modern', variable=americanmodern_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
americanmodern.place(x=371, y=156)
kemah=Checkbutton(root, text='Kemah Marine', variable=kemah_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
kemah.place(x=371, y=186)
concept=Checkbutton(root, text='Concept Special ', variable=concept_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
concept.place(x=371, y=216)
yachtinsure=Checkbutton(root, text='Yachtinsure', variable=yachtinsure_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
concept.place(x=371, y=246)
century=Checkbutton(root, text='Century Insurance', variable=century_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
century.place(x=371, y=276)
intact=Checkbutton(root, text='Intact', variable=intact_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
intact.place(x=371, y=306)
travelers=Checkbutton(root, text='Travelers', variable=travelers_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
travelers.place(x=371, y=336)

# This is the section of code which creates a button
Button(root, text='Submit and sent to markets!', bg='#7FFFD4', font=('helvetica', 12, 'normal'), command=btnClickFunction).place(x=371, y=346)


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
