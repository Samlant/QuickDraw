from pathlib import Path
import sys
import threading
import time
from tkinter import Tk

# TODO revise paths on these
from model.graph.graph import MSGraphClient
from model.graph.model import API
from model.email.email import EmailHandler

# NOTE These are likely OKAY!
# PRESENTER
from QuickDraw.presenter import Presenter

# MODELS
# from QuickDraw.models.windows.dirs import
# from QuickDraw.models.windows.registrations import
# from QuickDraw.models.windows.email_options import
from QuickDraw.models.dir.handler import DirHandler
from QuickDraw.models.dir.watcher import DirWatch
from QuickDraw.models.customer.form import FormBuilder
from QuickDraw.models.surplus_lines.interface import SurplusLinesAutomator
from QuickDraw.models.updater import update_app
from QuickDraw.models.submission import SubmissionModel
from QuickDraw.models.windows.alert import AlertModel
from QuickDraw.models.windows.allocate import AllocateModel
from QuickDraw.models.windows.templates import TemplatesModel
from QuickDraw.models.windows.home import HomeModel

# VIEWS
from QuickDraw.views.submission.interface import MainWindow
from QuickDraw.views.surplus_lines import SurplusLinesView
from QuickDraw.views.tray_icon import TrayIcon
from QuickDraw.views.submission.quoteforms.detections.alert import NewFileAlert
from QuickDraw.views.submission.quoteforms.detections.allocate import (
    AllocateView,
)
from QuickDraw.views.themes import palettes

from QuickDraw.helper import (
    MS_GRAPH_STATE_PATH,
    GREEN_LIGHT,
    RED_LIGHT,
    TRAY_ICON,
    APP_ICON,
    README,
    VIEW_INTERPRETER,
    open_config,
)


def get_theme() -> palettes.Palette:
    palette_name = open_config.get("View theme", "theme")
    theme = getattr(palettes, palette_name)
    return theme


def login_to_MS_graph():
    """Logs into Microsoft's Graph API
    TODO: Revise overall process structure of how we login!"""
    try:
        model_api_client = MSGraphClient(
            ms_graph_state_path=str(
                MS_GRAPH_STATE_PATH,
            )
        )
    except PermissionError as pe:
        print(
            f"Couldn't login using existing credentials. Deleting and trying again.\n {str(pe)}"
        )
        # Delete credential file
        Path.unlink(MS_GRAPH_STATE_PATH)
        # Retry login
        model_api_client = MSGraphClient(
            ms_graph_state_path=str(
                MS_GRAPH_STATE_PATH,
            )
        )
        return model_api_client


def initialize_modules() -> Presenter:
    """Creates and passes all models and views to the Presenter and
    returns the Presenter as an object."""
    # Models
    model_allocate = AllocateModel()
    model_api_client = login_to_MS_graph()
    model_api = API()
    model_dir_handler = DirHandler()
    watch_dir: Path = Path(
        open_config.get(
            "Folder settings",
            "watch_dir",
        )
    )
    model_dir_watcher = DirWatch(path_to_watch=watch_dir)
    model_email_handler = EmailHandler()
    model_form_builder = FormBuilder()
    model_new_alert = AlertModel(
        icon_src=str(APP_ICON),
    )
    model_submission = SubmissionModel()
    model_surplus_lines = SurplusLinesAutomator()
    model_tab_home = HomeModel(
        positive_value=GREEN_LIGHT,
        negative_value=RED_LIGHT,
    )
    model_tab_templates = TemplatesModel()
    # Views
    theme = get_theme()
    view_allocate = (AllocateView(icon_src=str(APP_ICON)),)
    view_main = MainWindow(
        icon_src=str(TRAY_ICON),
        view_interpreter=VIEW_INTERPRETER,
        view_palette=theme,
    )
    view_new_file_alert = NewFileAlert()
    view_surplus_lines = SurplusLinesView()
    # Presenter
    presenter = Presenter(
        model_allocate=model_allocate,
        model_api_client=model_api_client,
        model_api=model_api,
        model_dir_handler=model_dir_handler,
        model_dir_watcher=model_dir_watcher,
        model_email_handler=model_email_handler,
        model_form_builder=model_form_builder,
        model_new_alert=model_new_alert,
        model_submission=model_submission,
        model_surplus_lines=model_surplus_lines,
        model_tab_home=model_tab_home,
        model_tab_registrations=model_tab_registrations,
        model_tab_dirs=model_tab_dirs,
        model_tab_templates=model_tab_templates,
        view_allocate=view_allocate,
        view_main=view_main,
        view_new_file_alert=view_new_file_alert,
        view_surplus_lines=view_surplus_lines,
        view_theme=theme,
    )
    return presenter


def main():
    update_app(sys.argv[1:])
    presenter = initialize_modules()
    if not presenter.setup_api():
        sys.exit()
    presenter.model_dir_watcher.assign_presenter(presenter)
    tray_icon = TrayIcon(README)
    tray_icon.assign_presenter(presenter=presenter)
    thread1 = tray_icon.create_icon(src_icon=str(TRAY_ICON))
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
        elif presenter.run_template_settings_flag:
            presenter.start_submission_program(specific_tab="template")
            presenter.run_template_settings_flag = False
        elif presenter.run_email_settings_flag:
            presenter.start_submission_program(specific_tab="email")
            presenter.run_email_settings_flag = False
        elif presenter.run_folder_settings_flag:
            presenter.start_submission_program(specific_tab="folder")
            presenter.run_folder_settings_flag = False
        elif presenter.run_SL_automator_flag:
            presenter.run_surplus_lines()
            presenter.run_SL_automator_flag = False
        else:
            pass
        time.sleep(2)
    thread1.join()
    sys.exit()


if __name__ == "__main__":
    main()
