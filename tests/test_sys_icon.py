import threading

from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem


def create_image(color1, color2, width=64, height=64):
    image = Image.new("RGB", (width, height), color1)
    dc = ImageDraw.Draw(image)

    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height), fill=color2)

    return image


class TrayIcon:
    def __init__(self):
        self.active = True

    def _on_clicked(self, icon, item):
        if str(item) == "Settings":
            print("Opening Settings")
        elif str(item) == "Open ReadMe":
            # os.startfile(README_FILE)
            print("Opening ReadMe")
        elif str(item) == "Exit":
            icon.visible = False
            icon.stop()
            self.active = False

    def create_icon(self):
        thread = threading.Thread(
            daemon=True,
            target=lambda: Icon(
                "test",
                create_image("black", "white"),
                menu=Menu(
                    MenuItem("Settings", self._on_clicked),
                    MenuItem("Open ReadMe", self._on_clicked),
                    MenuItem("Exit", self._on_clicked),
                ),
            ).run(),
        )
        thread.start()
        print("started sys tray thread")
