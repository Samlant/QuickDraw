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
    key = str
    print(carrier)
    if 'Combo' not in carrier:
        key='none'
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
    else:
        if carrier=='Combo SW and PT':
            carrier = 'Combo email'
            key = 'SWandPTbody'
        elif carrier=='Combo SW and NH':
            carrier = 'Combo email'
            key = 'SWandNHbody'
        elif carrier=='Combo SW, PT and NH':
            carrier = 'Combo email'
            key = 'PTandNHandSWbody'
        elif carrier=='Combo PT and NH':
            carrier = 'Combo email'
            key = 'PTandNHandSWbody'
    return carrier, key

def Get_Subject(quoteform_fields_dict):
    import string
    quoteform_fields_dict = {key: quoteform_fields_dict[key] for key in quoteform_fields_dict.keys()
       & {'4669727374204e616d65', '4c617374204e616d65', 'Year', '4d616b6520616e64204d6f64656c', 'Length'}}
    first_name = string.capwords(quoteform_fields_dict.get('4669727374204e616d65'), sep=None)
    last_name = quoteform_fields_dict.get('4c617374204e616d65').upper()
    year = quoteform_fields_dict.get('Year')
    make = string.capwords(quoteform_fields_dict.get('4d616b6520616e64204d6f64656c'), sep=None)
    length = quoteform_fields_dict.get('Length')
    msg_subject = f'{last_name}, {first_name} | {year} {make} {length} | New Quote Submission'
    return msg_subject

def getYourName():
    config = update_config()
    placeholder = config['General settings']['your_name'].value
    return placeholder

def getPlaceholders(entry, section_name):
    config = update_config
    if 'Combo' in section_name:
        placeholder = config[section_name]['body'].value
    else:
        if 'address' in entry:
            placeholder = config[section_name]['address'].value
        elif 'greeting' in entry:
            placeholder = config[section_name]['greeting'].value
        elif 'body' in entry:
            placeholder = config[section_name]['body'].value
        elif 'salutation' in entry:
            placeholder = config[section_name]['salutation'].value
        else:
            pass
    return placeholder

def getyourName():
    config = read_config()
    placeholder_your_name = config.get('General settings', 'your_name')
    return placeholder_your_name

def listToString(s):
    str1 = ''
    for element in s:
        str1 += element
    return str1

def passing():
	pass