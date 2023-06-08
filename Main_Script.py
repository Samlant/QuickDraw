from model import Model, ConfigWorker, EmailHandler
from view import TkView
from presenter import Presenter

import os
import time
import sys

POSITIVE_SUBMISSION_VALUE = "submit"
NEGATIVE_SUBMISSION_VALUE = "pass"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

config_file_path = resource_path("configurations.ini")
view_icon_file_path = resource_path("quickdraw.png")

def main() -> None:
    configworker = ConfigWorker(file_path=config_file_path)
    emailhandler = EmailHandler()
    model = Model(
        positive_value=POSITIVE_SUBMISSION_VALUE,
        negative_value=NEGATIVE_SUBMISSION_VALUE,
    )
    view = TkView(
        positive_value=POSITIVE_SUBMISSION_VALUE,
        negative_value=NEGATIVE_SUBMISSION_VALUE,
        icon_src=view_icon_file_path,
    )
    presenter = Presenter(model=model, config_worker=configworker, email_handler=emailhandler, view=view)
    presenter.start_program()


if __name__ == "__main__":
    main()
