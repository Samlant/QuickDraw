import threading
from typing import Protocol
import webbrowser
from pathlib import Path

from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem


class Presenter(Protocol):
    """This enables us to call funtions from the Presenter
    class, either to send/retrieve data.
    """

    @property
    def run_flag(self) -> bool: ...

    @property
    def run_template_settings_flag(self) -> bool: ...

    @property
    def run_email_settings_flag(self) -> bool: ...

    @property
    def run_folder_settings_flag(self) -> bool: ...

    def start_program(self) -> None: ...

    def start_submission_program(self) -> None: ...


class TrayIcon:
    def __init__(self, readme: Path):
        self.active = True
        self.presenter = None
        self.readme: Path = readme

    def assign_presenter(self, presenter: Presenter):
        self.presenter = presenter

    def _on_clicked(self, icon, item):
        if str(item) == "Run QuickDraw":
            print("Running QuickDraw")
            if self.presenter.run_flag is False:
                self.presenter.run_flag = True

        elif str(item) == "Custom Templates":
            print("Opening custom templates")
            if self.presenter.run_flag is False:
                self.presenter.run_template_settings_flag = True

        elif str(item) == "Email Settings":
            print("Opening Email Settings")
            if self.presenter.run_flag is False:
                self.presenter.run_email_settings_flag = True
        elif str(item) == "Folder Settings":
            print("Opening Folder Settings")
            if self.presenter.run_flag is False:
                self.presenter.run_folder_settings_flag = True
        elif str(item) == "Open ReadMe":
            path = self.readme.resolve()
            print("Opening ReadMe")
            webbrowser.open(path.as_uri())
        elif str(item) == "Exit":
            icon.visible = False
            icon.stop()
            self.active = False
            self.presenter.run_flag = False
            self.presenter.view_main.root.quit()
        elif str(item) == "Add Surplus Lines Stamp":
            print("Running Surplus Lines Calculator")
            self.presenter.run_SL_automator_flag = True

    def create_icon(self, src_icon):
        thread = threading.Thread(
            daemon=True,
            target=lambda: Icon(
                "test",
                Image.open(src_icon),
                menu=Menu(
                    MenuItem("Run QuickDraw", self._on_clicked),
                    MenuItem("Add Surplus Lines Stamp", self._on_clicked),
                    MenuItem(
                        "Settings",
                        Menu(
                            MenuItem("Custom Templates", self._on_clicked),
                            MenuItem("Email Settings", self._on_clicked),
                            MenuItem("Folder Settings", self._on_clicked),
                        ),
                    ),
                    MenuItem("Open ReadMe", self._on_clicked),
                    MenuItem("Exit", self._on_clicked),
                ),
            ).run(),
            name="Sys Tray Icon",
        )
        return thread
