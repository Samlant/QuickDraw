from pathlib import Path
import sys
import threading
import time
from tkinter import Tk

# NOTE These are likely OKAY!
# PRESENTER
from QuickDraw.presenter.presenter import Presenter

# MODELS
from QuickDraw.models.dir.handler import DirHandler
from QuickDraw.models.dir.watcher import DirWatch
from QuickDraw.models.email.builder import EmailBuilder
from QuickDraw.models.graph.interface import GraphAPI
from QuickDraw.models.surplus_lines.interface import SurplusLinesAutomator
from QuickDraw.models.updater import update_app
from QuickDraw.models.submission.handler import SubmissionModel
from QuickDraw.models.windows.alert import AlertModel
# from QuickDraw.models.windows.allocate import AllocateModel
from QuickDraw.models.windows.templates import TemplatesModel
from QuickDraw.models.windows.home import HomeModel
# from QuickDraw.models.windows.dirs import
# from QuickDraw.models.windows.email_options import

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
    TRAY_ICON,
    APP_ICON,
    README,
    VIEW_INTERPRETER,
    open_config,
)


def get_theme() -> palettes.Palette:
    palette_name = open_config().get("View theme", "theme").value
    theme_palette = getattr(palettes, palette_name)
    return theme_palette


def initialize_modules() -> Presenter:
    """Creates and passes all models and views to the Presenter and
    returns the Presenter as an object."""
    # Models
    model_graph_api = GraphAPI()
    model_alert_new_qf = AlertModel()
    model_dir_handler = DirHandler()
    config = open_config()
    watch_dir = Path(config.get(
            "dirs",
            "watch_dir",
        ).value)
    model_dir_watcher = DirWatch(path_to_watch=watch_dir)
    model_email_builder = EmailBuilder()
    model_submission = SubmissionModel()
    model_surplus_lines = SurplusLinesAutomator()
    model_tab_home = HomeModel()
    model_tab_templates = TemplatesModel()
    # Views
    theme_palette = get_theme()
    view_allocate = (AllocateView(icon_src=str(APP_ICON)))
    view_main = MainWindow(icon_src=str(TRAY_ICON))
    view_new_file_alert = NewFileAlert(icon_src=str(APP_ICON))
    view_surplus_lines = SurplusLinesView()
    # Presenter
    presenter = Presenter(
        model_alert_new_qf=model_alert_new_qf,
        model_dir_handler=model_dir_handler,
        model_dir_watcher=model_dir_watcher,
        model_email_builder=model_email_builder,
        model_graph_api=model_graph_api,
        model_submission=model_submission,
        model_surplus_lines=model_surplus_lines,
        model_tab_home=model_tab_home,
        model_tab_templates=model_tab_templates,
        view_allocate=view_allocate,
        view_main=view_main,
        view_new_file_alert=view_new_file_alert,
        view_surplus_lines=view_surplus_lines,
        view_palette=theme_palette,
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
        if presenter.new_file_path:
            try:
                presenter.trigger_new_file(file=presenter.new_file_path)
            except Exception as e:
                print(f"exception raised during triggering new file.\n{e}")
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
