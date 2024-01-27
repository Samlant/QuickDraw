from pathlib import Path

from configupdater import ConfigUpdater

# Insert config functions, PATHS constants, and TEST constant

TEST = False
GREEN_LIGHT = "yes"
RED_LIGHT = "no"

if TEST:
    APP_DIR = Path(__file__).parents[2]
    # User resources
    RESOURCE_PATH = APP_DIR / "app" / "resources"
    CONFIG_PATH = RESOURCE_PATH / "configurations.ini"
    MS_GRAPH_STATE_PATH = RESOURCE_PATH / "ms_graph_state.jsonc"
    # App resources
    APP_ICON = RESOURCE_PATH / "img" / "app.ico"
    TRAY_ICON = RESOURCE_PATH / "img" / "sys_tray.ico"
    README = APP_DIR / "docs" / "site" / "index.html"
else:
    # User resources
    user_resources: Path = Path.home() / "AppData" / "Local" / "QuickDraw"
    MS_GRAPH_STATE_PATH: Path = user_resources / "ms_graph_state.jsonc"
    CONFIG_PATH: Path = user_resources / "configurations.ini"
    # App resources
    APP_DIR: Path = Path("C:/Program Files/QuickDraw")
    app_resources: Path = APP_DIR / "_internal" / "resources"
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


def open_config(self) -> None:  # GOOD
    """This is a helper to read config when called using ConfigUpdater,  an improvement on configParser."""
    open_read_update = ConfigUpdater(comment_prefixes=("^",))
    open_read_update.read(self.file_path)
    return open_read_update
