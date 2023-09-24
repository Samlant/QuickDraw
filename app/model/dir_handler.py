import shutil
from dataclasses import dataclass
from pathlib import Path
from ast import literal_eval
import ctypes
from string import capwords


@dataclass
class Resources:
    test: bool
    # User resources
    user_resources: Path = Path.home() / "AppData" / "Local" / "Work-Tools"
    ms_graph_state_path: Path = user_resources / "ms_graph_state.jsonc"
    config_path: Path = user_resources / "configurations.ini"
    # App resources
    app_dir: Path = user_resources / "QuickDraw"
    app_resources: Path = app_dir / "resources"
    app_icon: Path = app_resources / "img" / "app.ico"
    tray_icon: Path = app_resources / "img" / "sys_tray.ico"
    readme: Path = app_resources / "docs" / "readme.html"

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
            self.readme = self.app_dir / "docs" / "site" / "index.html"


class DirHandler:
    def __init__(self) -> None:
        pass

    def create_dirs(self, submission_info, folder_section_obj) -> Path:
        """Creates the client folder and moves the .PDF file to it.
        This includes validating and renaming the dir until there's
        no collission with existing dirs.

        Returns:  Path obj of the new path of the .PDF file itself.
        """
        referral = submission_info.referral
        fname = submission_info.fname
        lname = submission_info.lname

        client_dir = self._create_client_dir(
            referral=referral, fname=fname, lname=lname, section_obj=folder_section_obj
        )
        self.make_other_dirs(client_dir, folder_section_obj)
        return client_dir

    def _create_client_dir(self, referral, fname, lname, section_obj) -> Path:
        if self._check_if_renewal(referral):
            parent_dir = section_obj.get("renewals_dir").value
        else:
            parent_dir = Path(section_obj.get("new_biz_dir").value)
        client_dir = self.assign_dir_name(
            fname=fname,
            lname=lname,
            parent_dir=parent_dir,
        )
        result_dir = self.return_new_unique_path(client_dir)
        result_dir.mkdir()
        return result_dir

    def _check_if_renewal(self, referral: str) -> bool:
        if "RENEWAL" in referral.upper():
            return True
        else:
            return False

    def return_new_unique_path(self, client_dir: Path):
        test_dir_path = client_dir
        num = 1
        while test_dir_path.exists():
            num += 1
            test_dir_path = test_dir_path.with_stem(f"{client_dir.stem}-{num}")
        return test_dir_path

    def make_other_dirs(self, client_dir: Path, section_obj):
        config_dirs = section_obj.get("custom_dirs").value
        custom_dirs: list[str] = literal_eval(config_dirs)
        for path in custom_dirs:
            new_path = client_dir / str(path)
            new_path.mkdir(exist_ok=True)

    def move_file(self, client_dir: Path, origin_file: Path) -> Path:
        """Moves the client quoteform from its origin to dest dir."""
        new_file_path = client_dir / origin_file.name
        copied_file = self._create_copy(origin_file=origin_file)
        shutil.move(
            str(copied_file),
            str(new_file_path),
        )
        self._delete_original(origin_file)
        return new_file_path

    def _create_copy(self, origin_file: Path) -> Path:
        new_file_name = origin_file.stem + "1" + origin_file.suffix
        new_file = origin_file.parent / new_file_name
        try:
            shutil.copyfile(
                str(origin_file),
                str(new_file),
            )
        except:
            ctypes.windll.user32.MessageBoxW(
                0,
                "Please exit out of the PDF file so that the program can delete the original file.",
                "Warning: Exit the PDF",
                1,
            )
            self._create_copy(origin_file=origin_file)
        return new_file

    def _delete_original(self, origin_file: Path):
        try:
            origin_file.unlink()
        except:
            ctypes.windll.user32.MessageBoxW(
                0,
                "Please exit out of the PDF file so that the program can delete the original file.",
                "Warning: Exit the PDF",
                1,
            )
            self._delete_original(origin_file=origin_file)

    def assign_dir_name(
        self,
        fname: str,
        lname: str,
        parent_dir: Path,
    ) -> Path:
        dir_name = lname + " " + capwords(fname)
        return parent_dir / dir_name
