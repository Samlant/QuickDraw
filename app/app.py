from pathlib import Path
import sys
import threading
import time

from model.api.model import API
from model.api.app import MSGraphClient
from model.base_model import BaseModel
from model.config import ConfigWorker
from model.dir_handler.app import DirHandler
from model.dir_watch import DirWatch
from model.email import EmailHandler
from model.pdf import DocParser
from view.base_view import Submission
from view.dialogs import DialogNewFile
from view.dialogs import DialogAllocateMarkets
from view.sys_tray_icon import TrayIcon
from presenter.presenter import Presenter


# Debugging & development purposes
TEST = True

# production environment
production_data = Path.home() / "AppData" / "Local" / "Work-Tools"
production_dir = production_data / "QuickDraw"

# Check if frozen or not, then assign path to config & icon
if getattr(sys, "frozen", False):
    app_dir = sys._MEIPASS
else:
    app_dir = Path(__file__).parent

SAM = "ad0819fd-96be-42cb-82bd-ed8aa2f767fb"
JERRY = "bbc08f20-6f81-4f0d-8904-0f21b453f116"
CHARLIE = "aa7432c6-d322-4669-8640-2c48570dd7a8"

# Assign appropriate resource file names
RESOURCE_PATH = Path(app_dir) / "resources"
APP_ICON = RESOURCE_PATH / "app.ico"
TRAY_ICON = RESOURCE_PATH / "sys_tray.ico"
if TEST:
    PATH_TO_WATCH = Path(app_dir).parent / "tests"
    QUOTES_DIR = PATH_TO_WATCH / "QUOTES New"
    RENEWALS_DIR = PATH_TO_WATCH / "QUOTES Renewal"
    MS_GRAPH_STATE_PATH = RESOURCE_PATH / "ms_graph_state.jsonc"
    CONFIG_PATH = RESOURCE_PATH / "configurations.ini"
else:
    RESOURCE_PATH = production_dir / "resources"
    MS_GRAPH_STATE_PATH = production_data / "ms_graph_state.jsonc"
    CONFIG_PATH = production_data / "configurations.ini"

BROWSER_DRIVER = RESOURCE_PATH / "msedgedriver.exe"
POSITIVE_SUBMISSION_VALUE = "yes"
NEGATIVE_SUBMISSION_VALUE = "no"

# def assign_per_user_settings() -> dict[str, str]:
config_worker = ConfigWorker(file_path=CONFIG_PATH)
user: str = config_worker.get_value({"section_name": "graph_api", "key": "user_id"})
if (user == SAM) or (user == JERRY):
    user = "florida"
elif user == CHARLIE:
    user = "charlie"
else:
    sys.exit()


def initialize_modules() -> Presenter:
    "Creates and passes all models and views to the Presenter and returns the Presenter as an object."
    # Models
    api_client = MSGraphClient(ms_graph_state_path=MS_GRAPH_STATE_PATH)
    api_model = API()
    base_model = BaseModel(
        positive_value=POSITIVE_SUBMISSION_VALUE,
        negative_value=NEGATIVE_SUBMISSION_VALUE,
    )
    # config_worker = ConfigWorker(file_path=CONFIG_PATH)
    dir_handler = DirHandler(
        user=user,
    )
    watch_dir: Path = dir_handler.get_watch_dir()
    dir_watch = DirWatch(path_to_watch=watch_dir)
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
    # user_data = assign_per_user_settings()
    presenter = initialize_modules()
    if not presenter.setup_api(browser_driver=str(BROWSER_DRIVER)):
        sys.exit()
    presenter.dir_watch.assign_presenter(presenter)
    tray_icon = TrayIcon()
    tray_icon.assign_presenter(presenter=presenter)
    thread1 = tray_icon.create_icon(src_icon=TRAY_ICON)
    thread1.start()
    thread2 = threading.Thread(daemon=True, target=presenter.start_program, name="Dir_Watch")
    thread2.start()
    while tray_icon.active is True:
        if presenter.run_flag:
            presenter.start_submission_program()
            presenter.run_flag = False
        time.sleep(2)
    thread1.join()
    sys.exit()


if __name__ == "__main__":
    main()
