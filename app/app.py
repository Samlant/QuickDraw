import sys
import threading
import time
from pathlib import Path

from model.api.app import MSGraphClient
from model.api.model import API
from model.base_model import BaseModel
from model.config import ConfigWorker
from model.dir_handler.app import DirHandler, Resources
from model.dir_watch import DirWatch
from model.email.email import EmailHandler
from model.pdf import DocParser
from presenter.presenter import Presenter
from view.base_view import Submission
from view.dialogs import DialogAllocateMarkets, DialogNewFile
from view.sys_tray_icon import TrayIcon

TEST = False
POSITIVE_SUBMISSION_VALUE = "yes"
NEGATIVE_SUBMISSION_VALUE = "no"
SAM = "ad0819fd-96be-42cb-82bd-ed8aa2f767fb"
JERRY = "bbc08f20-6f81-4f0d-8904-0f21b453f116"
CHARLIE = "aa7432c6-d322-4669-8640-2c48570dd7a8"

PATHS = Resources(TEST)

config_worker = ConfigWorker(
    file_path=str(PATHS.config_path),
)
user_id: str = config_worker.get_value(
    {
        "section_name": "graph_api",
        "key": "user_id",
    }
)
dir_handler = DirHandler(TEST)
if user_id == SAM:
    user = "sam"
elif user_id == JERRY:
    user = "jerry"
elif user_id == CHARLIE:
    user = "charlie"
else:
    sys.exit()

dir_handler.set_user(user)


def initialize_modules() -> Presenter:
    """Creates and passes all models and views to the Presenter and
    returns the Presenter as an object."""
    # Models
    api_client = MSGraphClient(
        ms_graph_state_path=str(
            PATHS.ms_graph_state_path,
        )
    )
    api_model = API()
    base_model = BaseModel(
        positive_value=POSITIVE_SUBMISSION_VALUE,
        negative_value=NEGATIVE_SUBMISSION_VALUE,
    )
    watch_dir: Path = dir_handler.get_watch_dir()
    dir_watch = DirWatch(path_to_watch=watch_dir)
    email_handler = EmailHandler()
    pdf = DocParser()
    # Views
    submission = Submission(
        positive_value=POSITIVE_SUBMISSION_VALUE,
        negative_value=NEGATIVE_SUBMISSION_VALUE,
        icon_src=str(PATHS.app_icon),
    )
    dialog_new_file = DialogNewFile(
        icon_src=str(PATHS.app_icon),
    )
    dialog_allocate_markets = DialogAllocateMarkets(
        icon_src=str(PATHS.app_icon),
    )
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
    if not presenter.setup_api(browser_driver=str(PATHS.browser_driver)):
        sys.exit()
    presenter.dir_watch.assign_presenter(presenter)
    tray_icon = TrayIcon(PATHS.readme)
    tray_icon.assign_presenter(presenter=presenter)
    thread1 = tray_icon.create_icon(src_icon=str(PATHS.tray_icon))
    thread1.start()
    thread2 = threading.Thread(
        daemon=True, target=presenter.start_program, name="Dir_Watch"
    )
    thread2.start()
    while tray_icon.active is True:
        if presenter.run_flag:
            presenter.start_submission_program()
            presenter.run_flag = False
        elif presenter.run_settings_flag:
            presenter.start_submission_program(settings_tab=True)
            presenter.run_settings_flag = False
        else:
            pass
        time.sleep(2)
    thread1.join()
    sys.exit()


if __name__ == "__main__":
    main()
