import tkinter as tk
from tkinter import ttk
from tkinter import * 
	
# this is the function to get the user input from the text input boxes
def getInputBoxValues():
	fname = first_name.get()
	lname = last_name.get()
	year = year_.get()
	make = make_.get()
	length = length_.get()
	additional_email_body_notes = additional_email_body_notes_.get()
	return fname, lname, year, make, length, additional_email_body_notes


	# these are the functions to check the status of each checkbox (1 means checked, and 0 means unchecked)
def getCheckboxValues():
	sw_check = seawave_check.get()
	pt_check = primetime_check.get()
	am_check = americanmodern_check.get()
	km_check = kemah_check.get()
	tv_check = travelers_check.get()
	ce_check = century_check.get()
	cp_check = concept_check.get()
	yi_check = yachtinsure_check.get()
	return sw_check, pt_check, am_check, km_check, tv_check, ce_check, cp_check, yi_check


	# this is the function called when the button is clicked
def btnClickFunction():
	GetValues.getInputBoxValues()
	GetValues.getCheckboxValues()
	print(fname_+ ' ' + lname)
	  #save all user input into variables


root = Tk()

#these are the declarations of the variables associated with the checkboxes
seawave_check = tk.IntVar()
primetime_check = tk.IntVar()
americanmodern_check = tk.IntVar()
kemah_check = tk.IntVar()
travelers_check = tk.IntVar()
century_check = tk.IntVar()
concept_check = tk.IntVar()
yachtinsure_check = tk.IntVar()

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
year_=Entry(root)
year_.place(x=101, y=136)
make_=Entry(root)
make_.place(x=101, y=156)
length_=Entry(root)
length_.place(x=101, y=176)
additional_email_body_notes_=Entry(root)
additional_email_body_notes_.place(x=41, y=276)

# This is the section of code which creates the checkboxes
seawave=Checkbutton(root, text='Seawave Insurance', variable=seawave_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
seawave.place(x=371, y=66)

primetime=Checkbutton(root, text='Prime Time Insurance', variable=primetime_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
primetime.place(x=371, y=96)

americanmodern=Checkbutton(root, text='American Modern via MPG', variable=americanmodern_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
americanmodern.place(x=371, y=126)

kemah=Checkbutton(root, text='Kemah Marine', variable=kemah_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
kemah.place(x=371, y=156)

travelers=Checkbutton(root, text='Travelers', variable=travelers_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
travelers.place(x=371, y=186)

century=Checkbutton(root, text='Century Insurance', variable=century_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
century.place(x=371, y=216)

concept=Checkbutton(root, text='Concept Special Risks', variable=concept_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
concept.place(x=371, y=246)

yachtinsure=Checkbutton(root, text='Yachtinsure', variable=yachtinsure_check, bg='#7FFFD4', font=('helvetica', 12, 'normal'))
yachtinsure.place(x=371, y=276)


# This is the section of code which creates a button
Button(root, text='Submit and sent to markets!', bg='#7FFFD4', font=('helvetica', 12, 'normal'), command=GetValues.btnClickFunction).place(x=371, y=346)


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