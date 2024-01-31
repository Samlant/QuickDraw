from pathlib import Path
from typing import NamedTuple

from tkinterdnd2 import TkinterDnD
from configupdater import ConfigUpdater

# Insert config functions, PATHS constants, and TEST constant

TEST = False
GREEN_LIGHT = "yes"
RED_LIGHT = "no"

_view_backend = TkinterDnD.Tk()
_view_backend.withdraw()
VIEW_INTERPRETER = _view_backend

if TEST:
    app_dir = Path(__file__).parents[2]
    # User resources
    resource_path = app_dir / "app" / "resources"
    CONFIG_PATH = resource_path / "configurations.ini"
    MS_GRAPH_STATE_PATH = resource_path / "ms_graph_state.jsonc"
    # App resources
    APP_ICON = resource_path / "img" / "app.ico"
    TRAY_ICON = resource_path / "img" / "sys_tray.ico"
    README = app_dir / "docs" / "site" / "index.html"
else:
    # User resources
    user_resources: Path = Path.home() / "AppData" / "Local" / "QuickDraw"
    MS_GRAPH_STATE_PATH: Path = user_resources / "ms_graph_state.jsonc"
    CONFIG_PATH: Path = user_resources / "configurations.ini"
    # App resources
    app_dir: Path = Path("C:/Program Files/QuickDraw")
    app_resources: Path = app_dir / "_internal" / "resources"
    APP_ICON: Path = app_resources / "img" / "app.ico"
    TRAY_ICON: Path = app_resources / "img" / "sys_tray.ico"
    README: Path = app_resources / "docs" / "readme.html"


class Carrier(NamedTuple):
    name: str
    id: str
    redundancies: int = 0
    redundancy_group: int = 0


AVAILABLE_CARRIERS = [
    Carrier("Seawave", "SW", 3, 1),
    Carrier("Primetime", "PT", 3, 1),
    Carrier("NewHampshire", "NH", 3, 1),
    Carrier("AmericanModern", "AM"),
    Carrier("Kemah", "KM"),
    Carrier("Concept", "CP"),
    Carrier("Yachtinsure", "YI"),
    Carrier("Century", "CE"),
    Carrier("Intact", "IN"),
    Carrier("Travelers", "TV"),
]


def open_config() -> ConfigUpdater:  # GOOD
    """This is a helper to read config when called using ConfigUpdater,  an improvement on configParser."""
    open_read_update = ConfigUpdater(comment_prefixes=("^",))
    open_read_update.read(CONFIG_PATH)
    return open_read_update
