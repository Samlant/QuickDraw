from dataclasses import dataclass
from pathlib import Path


@dataclass
class Resources:
    test: bool
    # User resources
    user_resources: Path = Path.home() / "AppData" / "Local" / "QuickDraw"
    ms_graph_state_path: Path = user_resources / "ms_graph_state.jsonc"
    config_path: Path = user_resources / "configurations.ini"
    # App resources
    app_dir: Path = Path("C:/Program Files/QuickDraw")
    app_resources: Path = app_dir / "_internal" / "resources"
    app_icon: Path = app_resources / "img" / "app.ico"
    tray_icon: Path = app_resources / "img" / "sys_tray.ico"
    readme: Path = app_resources / "docs" / "readme.html"

    def __post_init__(self):
        if self.test:
            self.app_dir = Path(__file__).parents[2]
            # User resources
            self.resource_path = self.app_dir / "app" / "resources"
            self.config_path = self.resource_path / "configurations.ini"
            self.ms_graph_state_path = self.resource_path / "ms_graph_state.jsonc"
            # App resources
            self.app_icon = self.resource_path / "img" / "app.ico"
            self.tray_icon = self.resource_path / "img" / "sys_tray.ico"
            self.readme = self.app_dir / "docs" / "site" / "index.html"
