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
    section_name = str
    print(f"this is the carrier: {carrier}")
    if carrier == 'Select Carrier':
        print('found a Select Carrier value!')
        section_name = 'Select Carrier'
        key = 'sammy'
    elif 'Combo' not in carrier and carrier!='':
        key='sammy'
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
            key = 'PTandNHbody'
        else:
            section_name='sammy'
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

#def getYourName():
    #config = update_config()
    #placeholder = config['General settings']['your_name'].value
    #return placeholder

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

def getPlaceholders(section_name, type_of_entry, name_of_field):
    config = update_config()
    if type_of_entry == 'entry':
        index_var = '1.0'
    else:
        index_var = 0

    if 'Combo' in section_name[0]:
        key_name = section_name[1]
        placeholder = config[section_name[0]][key_name].value

    else:
        if name_of_field == 'name':
            placeholder = config['General settings']['your_name'].value
        elif name_of_field == 'address':
            placeholder = config[section_name[0]]['address'].value
        elif name_of_field == 'greeting':
            placeholder = config[section_name[0]]['greeting'].value
        elif name_of_field == 'body':
            placeholder = config[section_name[0]]['body'].value
        elif name_of_field == 'salutation':
            placeholder = config[section_name[0]]['salutation'].value
        else:
            print(f"getPlaceholders() couldn't process the input: {name_of_field}")
            placeholder = 'sammy'
    return placeholder, index_var

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