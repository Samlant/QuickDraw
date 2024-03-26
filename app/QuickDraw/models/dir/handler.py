import ctypes
import shutil
from ast import literal_eval
from pathlib import Path
from string import capwords
from typing import Protocol

from QuickDraw.helper import open_config


class Quoteform(Protocol):
    path: Path
    name: str
    fname: str
    lname: str
    year: str
    vessel: str
    referral: str


class Submission(Protocol):
    quoteform: Quoteform
    new_path: Path
    status: str
    attachments: list[str | Path]
    markets: list[str]


class DirHandler:
    def __init__(self) -> None:
        pass

    def process_dirs(self, submission: Submission):
        client_dir = self._create_dirs(
            submission,
        )
        submission.new_path = self._move_file(
            client_dir,
            submission.quoteform.path,
        )

    def _create_dirs(self, submission) -> Path:
        """Creates the client folder and moves the .PDF file to it.
        This includes validating and renaming the dir until there's
        no collision with existing dirs.

        Returns:  Path obj of the new path of the .PDF file itself.
        """
        fname = submission.customer.fname
        lname = submission.customer.lname
        config = open_config()
        section_obj = config.get_section("Folder settings")
        parent_dir = self.assign_parent_dir(submission.quoteform.referral, section_obj)
        client_dir = self.__create_client_dir(
            parent_dir=parent_dir,
            fname=fname,
            lname=lname,
        )
        self._make_other_dirs(client_dir, section_obj)
        return client_dir

    def assign_parent_dir(self, referral, section_obj) -> Path:
        if self.__check_if_renewal(referral):
            return Path(section_obj.get("renewals_dir").value)
        else:
            return Path(section_obj.get("new_biz_dir").value)

    def __create_client_dir(self, parent_dir, fname, lname) -> Path:
        client_dir = self._assign_dir_name(
            fname=fname,
            lname=lname,
            parent_dir=parent_dir,
        )
        result_dir = self._return_new_unique_path(client_dir)
        result_dir.mkdir()
        return result_dir

    def __check_if_renewal(self, referral: str) -> bool:
        if "RENEWAL" in referral.upper():
            return True
        else:
            return False

    def _return_new_unique_path(self, client_dir: Path) -> Path:
        test_dir_path = client_dir
        num = 1
        while test_dir_path.exists():
            num += 1
            test_dir_path = test_dir_path.with_stem(f"{client_dir.stem}-{num}")
        return test_dir_path

    def _make_other_dirs(self, client_dir: Path, section_obj):
        config_dirs = section_obj.get("custom_dirs").value
        custom_dirs: list[str] = literal_eval(config_dirs)
        for path in custom_dirs:
            filtered_dir_name = str(path).translate({ord(i): None for i in r'?<>:*|"'})
            if filtered_dir_name != path:
                print(
                    "Invalid characters removed from folder name because they're invalid for Windows systems."
                )
            new_path = client_dir / str(filtered_dir_name)
            new_path.mkdir(exist_ok=True)

    def _move_file(self, client_dir: Path, origin_file: Path) -> Path:
        """Moves the client quoteform from its origin to dest dir."""
        new_file_path = client_dir / origin_file.name
        copied_file = self.__create_copy(origin_file=origin_file)
        shutil.move(
            str(copied_file),
            str(new_file_path),
        )
        self.__delete_original(origin_file)
        return new_file_path

    def __create_copy(self, origin_file: Path) -> Path:
        new_file_name = origin_file.stem + "1" + origin_file.suffix
        new_file = origin_file.parent / new_file_name
        # try:
        shutil.copyfile(
            str(origin_file),
            str(new_file),
        )
        # except:
        ctypes.windll.user32.MessageBoxW(
            0,
            "Please exit out of the PDF file so that the program can create a copy of the original file.",
            "Warning: Exit the PDF",
            1,
        )
        self.__create_copy(origin_file=origin_file)
        return new_file

    def __delete_original(self, origin_file: Path):
        # try:
        origin_file.unlink()
        # except:
        #     ctypes.windll.user32.MessageBoxW(
        #         0,
        #         "Please exit out of the PDF file so that the program can delete the original file.",
        #         "Warning: Exit the PDF",
        #         1,
        #     )
        self.__delete_original(origin_file=origin_file)

    def _assign_dir_name(
        self,
        fname: str,
        lname: str,
        parent_dir: Path,
    ) -> Path:
        dir_name = lname + " " + capwords(fname)
        filtered_dir_name = dir_name.translate({ord(i): None for i in r'/?<>\:*|"'})
        if filtered_dir_name != dir_name:
            print(
                "Invalid characters removed from folder name because they're invalid for Windows systems."
            )
        return parent_dir / filtered_dir_name
