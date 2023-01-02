from configparser import ConfigParser
from configupdater import ConfigUpdater

# Method to read config file settings
def read_config():
    config = ConfigParser()
    config.read('configurations.ini')
    return config

# Method to update config file settings
def update_config():
    updater = ConfigUpdater()
    updater.read("configurations.ini")
    return updater

def update_def_cc(cc_1, cc_2, merge):
    
    updater['CarbonCopy Settings']['def_cc_address_1'].value = cc_1
    updater['CarbonCopy Settings']['def_cc_address_2'].value = cc_2
    updater['CarbonCopy Settings']['settings_merge_cc_addresses'].value = merge
    print('complete')
    
#    print(carrier)
#    updater["CarbonCopy Settings"]["def_cc_address_1"].value = "Alan Turing"