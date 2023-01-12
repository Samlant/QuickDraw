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
    updater.read('configurations.ini')
    return updater
    
#Method to get the path of the quoteform


# tkinter functions that need to be declared at top of script but make the script look unorganized:
# Above not used yet,  but below are functions I want to put in helper.py

def assignCorrectCarrierNames(carrier):
    key = str
    print(carrier)
    if 'Combo' not in carrier and carrier!='':
        key='none'
        if carrier=='Seawave':
            section_name = 'SW email'
        elif carrier =='Prime Time':
            section_name = 'PT email'
        elif carrier=='New Hampshire':
            section_name = 'NH email'
        elif carrier=='American Modern':
            section_name = 'AM email'
        elif carrier=='Kemah':
            section_name = 'KM email'
        elif carrier=='Concept':
            section_name = 'CP email'
        elif carrier=='Yachtinsure':
            section_name = 'YI email'
        elif carrier=='Century':
            section_name = 'CE email'
        elif carrier=='Intact':
            section_name = 'IN email'
        elif carrier=='Travelers':
            section_name = 'TV email'
    elif 'Combo' in carrier:
        section_name = 'Combo email'
        if carrier=='Combo SW and PT':
            key = 'SWandPTbody'
        elif carrier=='Combo SW and NH':
            key = 'SWandNHbody'
        elif carrier=='Combo SW, PT and NH':
            key = 'PTandNHandSWbody'
        elif carrier=='Combo PT and NH':
            key = 'PTandNHandSWbody'
        else:
            print(f"Assign CorrectCarrierNsmes in helper file wasnt able to allocate the carrier variable: {carrier} ... correctly to a specific Combo option so it was left for the last else statement")
    else:
        print(f"Assign CorrectCarrierNsmes in helper file wasnt able to allocate the carrier variable: {carrier} ... correctly so it was left for the last else statement")
    return section_name, key

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
        key_ name = 'SWandPTbody' #TODO: Replace hard coded value to .get() the key name asit is in the config file.  i can use assign correct carrier name i think..
        placeholder = config[section_name][key_name].value
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
            print('Was not a Combo according to section_name, and then entry did not match any of the listed options such asbody, greeting..')
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