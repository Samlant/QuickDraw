import os
import time
import sys

import pystray
import time

from view.test_sys_icon import TrayIcon


tray_icon = TrayIcon()
tray_icon.create_icon()
while tray_icon.active == True:
    
