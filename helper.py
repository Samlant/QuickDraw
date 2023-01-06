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
    
#    print(carrier)
#    updater["CarbonCopy Settings"]["def_cc_address_1"].value = "Alan Turing"