from configparser import ConfigParser
from configupdater import ConfigUpdater

# Method to read config file settings
def read_config():
    config = ConfigParser()
    config.read('configurations.ini')
    return config

# Method to read/update config file settings (REPLACE CONFIGPARSER ABOVE????)
def update_config():
    updater = ConfigUpdater()
    updater.read("configurations.ini")
    return updater
    
#Method to get the path of the quoteform


# tkinter functions that need to be declared at top of script but make the script look unorganized:
# Above not used yet,  but below are functions I want to put in helper.py

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

def Get_Subject(quoteform_fields_dict):
    quoteform_fields_dict = {key: quoteform_fields_dict[key] for key in quoteform_fields_dict.keys()
       & {'4669727374204e616d65', '4c617374204e616d65', 'Year', '4d616b6520616e64204d6f64656c', 'Length'}}
    first_name = quoteform_fields_dict.get('4669727374204e616d65')
    last_name = quoteform_fields_dict.get('4c617374204e616d65')
    year = quoteform_fields_dict.get('Year')
    make = quoteform_fields_dict.get('4d616b6520616e64204d6f64656c')
    length = quoteform_fields_dict.get('Length')
    msg_subject = f'{last_name}, {first_name} | {year} {make} {length} | New Quote Submission'
    return msg_subject

def listToString(s):
    str1 = ''
    for element in s:
        str1 += element
    return str1

def passing():
	pass