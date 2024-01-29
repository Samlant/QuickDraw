from pathlib import Path
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


CARRIERS = [
    "Seawave",
    "Primetime",
    "NewHampshire",
    "AmericanModern",
    "Kemah",
    "Concept",
    "Yachtinsure",
    "Century",
    "Intact",
    "Travelers",
]


def open_config() -> ConfigUpdater:  # GOOD
    """This is a helper to read config when called using ConfigUpdater,  an improvement on configParser."""
    open_read_update = ConfigUpdater(comment_prefixes=("^",))
    open_read_update.read(CONFIG_PATH)
    return open_read_update
