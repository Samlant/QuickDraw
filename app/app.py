from pathlib import Path
import sys
import threading
import time

from model.api.api import API
from model.api.client import MSGraphClient
from model.base_model import BaseModel
from model.config import ConfigWorker
from model.dir_handler import DirHandler
from model.dir_watch import DirWatch
from model.email import EmailHandler
from model.pdf import DocParser
from view.base_view import Submission
from view.dialogs import DialogNewFile
from view.dialogs import DialogAllocateMarkets
from view.sys_tray_icon import TrayIcon
from presenter.presenter import Presenter


# TODO CREATE PATHS WITHIN FUNCTION AND RETURN THEM... CLEAN NAMESPACE
# Debugging & development purposes
TEST = True

# Check if frozen or not, then assign path to config & icon
if getattr(sys, "frozen", False):
    app_dir = sys._MEIPASS
else:
    app_dir = Path(__file__).parent

# production environment
production_dir = Path.home() / "AppData" / "Local" / "Work-Tools"

# Assign appropriate resource file names
if TEST:
    RESOURCE_PATH = Path(app_dir) / "resources"
    PATH_TO_WATCH = Path(app_dir).parent / "tests"
    APP_ICON = RESOURCE_PATH / "app.ico"
    TRAY_ICON = RESOURCE_PATH / "sys_tray.ico"
else:
    RESOURCE_PATH = Path(production_dir) / "resources"
    PATH_TO_WATCH = (
        Path.home() / "Novamar Insurance" / "Flordia Office Master - Documents"
    )
    FROZEN_RESOURCE_PATH = Path(app_dir) / "resources"
    APP_ICON = FROZEN_RESOURCE_PATH / "app.ico"
    print(str(FROZEN_RESOURCE_PATH))
    TRAY_ICON = FROZEN_RESOURCE_PATH / "sys_tray.ico"
QUOTES_DIR = PATH_TO_WATCH / "QUOTES New"
RENEWALS_DIR = PATH_TO_WATCH / "QUOTES Renewal"
CONFIG_PATH = RESOURCE_PATH / "configurations.ini"
MS_GRAPH_STATE_PATH = RESOURCE_PATH / "ms_graph_state.jsonc"
POSITIVE_SUBMISSION_VALUE = "yes"
NEGATIVE_SUBMISSION_VALUE = "no"


def initialize_modules() -> Presenter:
    "Creates and passes all models and views to the Presenter and returns the Presenter as an object."
    # Models
    api_client = MSGraphClient(ms_graph_state_path=MS_GRAPH_STATE_PATH)
    api_model = API()
    base_model = BaseModel(
        positive_value=POSITIVE_SUBMISSION_VALUE,
        negative_value=NEGATIVE_SUBMISSION_VALUE,
    )
    config_worker = ConfigWorker(file_path=CONFIG_PATH)
    dir_handler = DirHandler(
        quotes_dir=QUOTES_DIR,
        renewals_dir=RENEWALS_DIR,
    )
    dir_watch = DirWatch(path_to_watch=PATH_TO_WATCH)
    email_handler = EmailHandler()
    pdf = DocParser()
    # Views
    submission = Submission(
        positive_value=POSITIVE_SUBMISSION_VALUE,
        negative_value=NEGATIVE_SUBMISSION_VALUE,
        icon_src=APP_ICON,
    )
    dialog_new_file = DialogNewFile(icon_src=str(APP_ICON))
    dialog_allocate_markets = DialogAllocateMarkets(icon_src=APP_ICON)
    # Presenter
    presenter = Presenter(
        api_client=api_client,
        api_model=api_model,
        base_model=base_model,
        config_worker=config_worker,
        dir_handler=dir_handler,
        dir_watch=dir_watch,
        email_handler=email_handler,
        pdf=pdf,
        submission=submission,
        dialog_new_file=dialog_new_file,
        dialog_allocate_markets=dialog_allocate_markets,
    )
    return presenter


def main():
    presenter = initialize_modules()
    presenter.setup_api()
    presenter.dir_watch.assign_presenter(presenter)
    tray_icon = TrayIcon()
    tray_icon.assign_presenter(presenter=presenter)
    thread1 = tray_icon.create_icon(src_icon=TRAY_ICON)
    thread1.start()
    thread2 = threading.Thread(
        daemon=False,
        target=presenter.set_connection_data,
    )
    thread2.start()
    thread3 = threading.Thread(daemon=True, target=presenter.start_program)
    thread3.start()
    while tray_icon.active is True:
        if presenter.run_flag:
            presenter.start_submission_program()
            presenter.run_flag = False
        time.sleep(2)
    thread1.join()
    sys.exit()


if __name__ == "__main__":
    main()

# def initialize_modules():
# model = BaseModel()
#     positive_value=POSITIVE_SUBMISSION_VALUE,
#     negative_value=NEGATIVE_SUBMISSION_VALUE,
#     pdf_path=pdf_data,
# )
# view = TkView(
#     positive_value=POSITIVE_SUBMISSION_VALUE,
#     negative_value=NEGATIVE_SUBMISSION_VALUE,
#     icon_src=APP_ICON,
# )

# class Model:
#     def __init__(self) -> None:
#         self.base_model = BaseModel(
#             positive_value=POSITIVE_SUBMISSION_VALUE,
#             negative_value=NEGATIVE_SUBMISSION_VALUE,
#             pdf_path=pdf_data,
#         )
#         self.config_worker = ConfigWorker(file_path=CONFIG)
#         self.api_client = MSGraphClient()
#         self.email_handler = EmailHandler()
#         self.dir_watch = DirWatch()


# class View:
#     def __init__(self, presenter: Presenter) -> None:
#         self.submission = Submission(
#             positive_value=POSITIVE_SUBMISSION_VALUE,
#             negative_value=NEGATIVE_SUBMISSION_VALUE,
#             icon_src=ICON,
#         )
#         self.dialog_new_file = DialogNewFile()
#         self.dialog_allocate_markets = DialogAllocateMarkets()
#         self.tray_icon = TrayIcon()

# # Initialize ConfigWorker
# model = Model()
# view = View()
# presenter = Presenter(model=model, view=view)
# view.tray_icon.assign_presenter(presenter=presenter)
