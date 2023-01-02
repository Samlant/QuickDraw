from helper import *

#print(config.get('SW email', 'sw_greeting'))

def update_carrier_email(carrier, email, greeting, body, salutation):
    config = read_config()
    carrier_section = carrier + ' email'
    address_key = f"{carrier}_address"
    greeting_key = f"{carrier}_greeting"
    body_key = f"{carrier}_body"
    salutation_key = f"{carrier}_salutation"
    config.set(carrier_section, address_key, email)
    config.set(carrier_section, greeting_key, greeting)
    config.set(carrier_section, body_key, body)
    config.set(carrier_section, salutation_key, salutation)
    with open('configurations.ini', 'w') as configfile:
        config.write(configfile)    

def getEmailContentToSend():
    config = read_config()
    check_dict = [(seawave_check.get()), (primetime_check.get()), (newhampshire_check.get()), (americanmodern_check.get()), (kemah_check.get()), (concept_check.get()), (yachtinsure_check.get()), (century_check.get()), (intact_check.get()), (travelers_check.get())]
    if check_dict[0]==1 and check_dict[1]==1 and check_dict[2]==0:
		pt[0] = 0
		sw[3] = config.get('Combo email', 'sw_and_pt_body')
	elif check_dict[0]==1 and check_dict[1]==0 and check_dict[2]==1:
		nh[0] = 0
		sw[3] = config.get('Combo email', 'sw_and_nh_body')
	elif check_dict[0]==1 and check_dict[1]==1 and check_dict[2]==1:
		pt[0] = 0
		nh[0] = 0
		sw[3] = config.get('Combo email', 'pt_and_nh_and_sw_body')
	elif check_dict[1]==1 and ncheck_dict[2]==1:
		nh[0] = 0
		pt[3] = config.get('Combo email', 'pt_and_nh_body')
	else:
		passing
    for section in config:
        carrier_name = config.get(section, 'name') #to have shorthand carrier name
        name_check = carrier_name + '_check' #to have checkbox name
        get_check = name_check.get()
        name_section = config.get(section, 'name') + ' email'
        address_key = config.get(section, 'address')
        greeting_key = config.get(section, 'name')
        body_key = config.get(section, 'name')
        salutation_key = config.get(section, 'salutation')
        your_name = config.get('General Settings', 'your name')
        create_var_name = (carrier_name
        locals()[create_var_name] = 2020
        carrier_tuple = (get_check, address_key, greeting_key, body_key, salutation_key, your_name)
        return carrier_tuple

#print(config.get('SW email', 'sw_greeting'))



#print(sw[4])
#print(config.sections())
#print(config['SW email'])
#print(list(config['SW email']))
#
#print(config['SW email']['sw_body'])