from configparser import ConfigParser
from configupdater import ConfigUpdater

config = ConfigParser()
config.read('configurations.ini')
updater = ConfigUpdater()
updater.read("configurations.ini")

# Method to read config file settings
def read_config():
    config = ConfigParser()
    config.read('configurations.ini')
    return config

def update_def_cc(cc_1, cc_2, merge):
    
    updater['CarbonCopy Settings']['def_cc_address_1'].value = cc_1
    updater['CarbonCopy Settings']['def_cc_address_2'].value = cc_2
    updater['CarbonCopy Settings']['settings_merge_cc_addresses'].value = merge
    print('complete')

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
    
#    print(carrier)
#    updater["CarbonCopy Settings"]["def_cc_address_1"].value = "Alan Turing"