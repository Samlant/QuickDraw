import shutil
from dataclasses import dataclass
from pathlib import Path

from model.dir_handler.charlie import Dirs as CharlieDirs
from model.dir_handler.dev_dirs import DevDirs
from model.dir_handler.florida import Dirs as FloridaDirs


@dataclass
class Resources:
    test: bool
    # User resources
    user_resources: Path = Path.home() / "AppData" / "Local" / "Work-Tools"
    ms_graph_state_path: Path = user_resources / "ms_graph_state.jsonc"
    config_path: Path = user_resources / "configurations.ini"
    app_dir: Path = user_resources / "QuickDraw"
    # App resources
    app_icon: Path = app_dir / "resources" / "img" / "app.ico"
    tray_icon: Path = app_dir / "resources" / "img" / "sys_tray"
    browser_driver: Path = app_dir / "resources" / "msedgedriver"
    readme: Path = app_dir / "resources" / "docs" / "index.html"

    def __post_init__(self):
        if self.test:
            self.app_dir = Path(__file__).parents[3]
            # User resources
            self.resource_path = self.app_dir / "app" / "resources"
            self.config_path = self.resource_path / "configurations.ini"
            self.ms_graph_state_path = self.resource_path / "ms_graph_state.jsonc"
            # App resources
            self.app_icon = self.resource_path / "img" / "app.ico"
            self.tray_icon = self.resource_path / "img" / "sys_tray.ico"
            self.browser_driver = self.resource_path / "msedgedriver.exe"
            self.readme = self.app_dir / "docs" / "site" / "index.html"


class DirHandler:
    def __init__(self, test: bool) -> None:
        self.user: str
        self.dirs: FloridaDirs | CharlieDirs | DevDirs
        self.test: bool = test

    def set_user(self, user: str):
        if self.test:
            self.dirs: DevDirs = DevDirs()
        elif user == "florida":
            self.dirs: FloridaDirs = FloridaDirs()
        elif user == "charlie":
            self.dirs: CharlieDirs = CharlieDirs()
        elif user == "ericka":
            raise NotImplementedError
        elif user == "peter":
            raise NotImplementedError
        elif user == "courtney":
            raise NotImplementedError
        elif user == "ed":
            raise NotImplementedError
        elif user == "craig":
            raise NotImplementedError
        elif user == "rob":
            raise NotImplementedError
        else:
            raise ValueError("user value passed to DirHandler is incorrect.")

    def get_watch_dir(self) -> Path:
        """returns the watch dir for the specific user in a Path obj."""
        return self.dirs.watch_path

    def _check_if_renewal(self, renewal: str) -> bool:
        if "RENEWAL" in renewal.upper():
            return self.dirs.renewal_path
        else:
            return self.dirs.new_biz_path

    def _assign_parent_dir(self, referral: bool):
        if str(referral).upper() == "RENEWAL":
            return self.dirs.renewal_path
        else:
            return self.dirs.new_biz_path

    def return_unused_path(self, client_dir: Path):
        test_dir_path = client_dir
        num = 1
        while test_dir_path.exists():
            num += 1
            test_dir_path = test_dir_path.with_stem(f"{client_dir.stem}-{num}")
        return test_dir_path

    def _create_client_dir(self, referral, fname, lname) -> Path:
        renewal = self._check_if_renewal(referral)
        parent_dir = self._assign_parent_dir(renewal)
        client_dir = self.dirs.assign_dir_name(
            fname=fname,
            lname=lname,
            parent_dir=parent_dir,
        )
        result_dir = self.return_unused_path(client_dir)
        result_dir.mkdir()
        return result_dir

    def create_dirs(self, submission_info) -> Path:
        """Creates the client folder and moves the .PDF file to it.
        This includes validating and renaming the dir until there's
        no collission with existing dirs.

        Returns:  Path obj of the new path of the .PDF file itself.
        """
        referral = submission_info.referral
        fname = submission_info.fname
        lname = submission_info.lname

        client_dir = self._create_client_dir(
            referral=referral,
            fname=fname,
            lname=lname,
        )
        self.dirs.make_other_dirs(client_dir)
        return client_dir

    def move_file(self, client_dir: Path, orgin_file: Path) -> Path:
        """Moves the client quoteform from its origin to dest dir."""
        new_file_path = client_dir / orgin_file.name
        shutil.move(
            str(orgin_file),
            str(new_file_path),
        )
        return new_file_path
