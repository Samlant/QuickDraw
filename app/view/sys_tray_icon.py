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
    def run_flag(self) -> bool:
        ...

    @property
    def run_settings_flag(self) -> bool:
        ...

    def start_program(self) -> None:
        ...

    def start_submission_program(self) -> None:
        ...


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
            if self.presenter.run_settings_flag is False:
                self.presenter.run_flag = True
        elif str(item) == "Settings":
            print("Opening Settings")
            if self.presenter.run_flag is False:
                self.presenter.run_settings_flag = True

        elif str(item) == "Open ReadMe":
            path = self.readme.resolve()
            print("Opening ReadMe")
            webbrowser.open(path.as_uri())
        elif str(item) == "Exit":
            icon.visible = False
            icon.stop()
            self.active = False
            self.presenter.run_flag = False
            # self.presenter.submission.withdraw()
            print(self.presenter.submission.root.state())
            self.presenter.submission.root.quit()
            # print(self.presenter.submission.state())

    def create_icon(self, src_icon):
        thread = threading.Thread(
            daemon=True,
            target=lambda: Icon(
                "test",
                Image.open(src_icon),
                menu=Menu(
                    MenuItem("Run QuickDraw", self._on_clicked),
                    MenuItem("Settings", self._on_clicked),
                    MenuItem("Open ReadMe", self._on_clicked),
                    MenuItem("Exit", self._on_clicked),
                ),
            ).run(),
            name="Sys Tray Icon",
        )
        return thread

    # def use_image(self):
    #     if self.icon:
    #         Image.open(self.icon)
    #     else:
    #         self.create_image("black", "white")

    # def create_image(self, color1, color2, width=64, height=64):
    #     if not self.icon:
    #         image = Image.new("RGB", (width, height), color1)
    #         dc = ImageDraw.Draw(image)

    #         dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    #         dc.rectangle((0, height // 2, width // 2, height), fill=color2)
    #         return image
