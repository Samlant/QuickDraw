import sys
import threading
import time
from pathlib import Path

from model.api.app import MSGraphClient
from model.api.model import API
from model.base_model import BaseModel
from model.config import ConfigWorker
from model.dir_handler import DirHandler, Resources
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

PATHS = Resources(TEST)

config_worker = ConfigWorker(
    file_path=str(PATHS.config_path),
)


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
    watch_dir: Path = Path(
        config_worker.get_value(
            {
                "section_name": "Folder settings",
                "key": "watch_dir",
            }
        )
    )
    dir_handler = DirHandler()
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
    if not presenter.setup_api():
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
        if presenter.new_file_path != None:
            try:
                presenter.trigger_new_file(file=presenter.new_file_path)
            except:
                print("exception raised during triggering new file.")
            else:
                presenter.new_file_path = None
        elif presenter.run_flag:
            presenter.start_submission_program()
            presenter.run_flag = False
        elif presenter.run_email_settings_flag:
            presenter.start_submission_program(specific_tab="email")
            presenter.run_email_settings_flag = False
        elif presenter.run_folder_settings_flag:
            presenter.start_submission_program(specific_tab="folder")
            presenter.run_folder_settings_flag = False
        else:
            pass
        time.sleep(2)
    thread1.join()
    sys.exit()


if __name__ == "__main__":
    main()
