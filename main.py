from model import Model, ConfigWorker, EmailHandler
from view import TkView
from presenter import Presenter

import os
import time
import sys

POSITIVE_SUBMISSION_VALUE = "submit"
NEGATIVE_SUBMISSION_VALUE = "pass"

TEST = False

ICON_NAME = "icon.ico"
CONFIG_NAME = "configurations.ini"
app_dir = os.path.expandvars(r'%LOCALAPPDATA%\Work Tools')

if TEST == True:
    ICON_NAME = os.path.join("resources", ICON_NAME)
    CONFIG_PATH = os.path.join(app_dir, CONFIG_NAME)

if getattr(sys, "frozen", False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

ICON = os.path.join(application_path, ICON_NAME)
CONFIG = os.path.join(app_dir, CONFIG_NAME)


def main(pdf_data=dict) -> None:
    configworker = ConfigWorker(file_path=CONFIG)
    emailhandler = EmailHandler()
    model = Model(
        positive_value=POSITIVE_SUBMISSION_VALUE,
        negative_value=NEGATIVE_SUBMISSION_VALUE,
        pdf_path=pdf_data,
    )
    view = TkView(
        positive_value=POSITIVE_SUBMISSION_VALUE,
        negative_value=NEGATIVE_SUBMISSION_VALUE,
        icon_src=ICON,
    )
    presenter = Presenter(
        model=model, config_worker=configworker, email_handler=emailhandler, view=view
    )
    presenter.start_program()


if __name__ == "__main__":
    pdf_data = {}
    main(pdf_data)
else:
    pdf_data = input()
    main(pdf_data)
