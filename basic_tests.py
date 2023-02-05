import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Notebook, Style
from tkinter import * 
from tkinterdnd2 import *

root = Tk()
root.geometry('760x548')
root.configure(background='#5F9EA0')
root.title('Test Window')
root.attributes('-alpha',0.95)

def exampleFunction(*args):
    print(example_string_var)
    print(example_string_var.get())

def on_focus_out_entry(entry):
    print(entry)
    

example_string_var = StringVar(value='Select Carrier', name='Dropdown Menu')
example_string_var.trace_add('write', exampleFunction)
options = ['Seawave',
           'Prime Time',
           'New Hampshire',
           'American Modern',
           'Kemah',
           'Concept Special Risks',
           'Yachtinsure',
           'Century',
           'Intact',
           'Travelers',
           'Combination: Seawave and Prime Time',
           'Combination: Seawave and New Hampshire',
           'Combination: Prime Time and New Hampshire',
           'Combination: Seawave, Primetime and New Hampshire'
          ]

list_of_options = [
    'Seawave',
    'Prime Time',
    'New Hampshire',
    'American Modern',
    'Kemah', 'Concept Special Risks',
    'Yachtinsure',
    'Century',
    'Intact',
    'Travelers',
    'Combination: Seawave and Prime Time',
    'Combination: Seawave and New Hampshire',
    'Combination: Prime Time and New Hampshire',
    'Combination: Seawave, Primetime and New Hampshire'
    ]
    
#drop = OptionMenu(root, example_string_var, *options)
drop = OptionMenu(root, example_string_var, *list_of_options)
drop.configure(background='#aedadb', foreground='black', highlightbackground='#5F9EA0', activebackground='#5F9EA0')
drop['menu'].configure(background='#aedadb')
drop.pack(fill = X, expand=False)

my_name = StringVar(value='Sam', name='my_name')
name = Entry(master=root, textvariable=my_name)
name_focus_out = name.bind('<FocusOut>',
                           lambda x: on_focus_out_entry(my_name.get())
                           )
name.pack()
str1 = 'Seawave'
exec("%s = %d" % (str1, ''))
second_entry = Entry(root)
second_entry.pack()


root.mainloop()