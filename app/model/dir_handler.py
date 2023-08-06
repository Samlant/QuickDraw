from pathlib import Path
import shutil


class DirHandler:
    def __init__(
        self,
        quotes_dir: str,
        renewals_dir: str,
    ) -> None:
        self.quotes_dir = quotes_dir
        self.renewals_dir = renewals_dir

    def create_folder(self, submission_info) -> Path:
        """Creates the client folder and moves the .PDF file to it.
        This includes validating and renaming the dir until there's
        no collission with existing dirs.

        Returns:  Path obj of the new path of the .PDF file itself.
        """
        if self._check_if_renewal(submission_info.referral):
            parent_dir = self.renewals_dir
        else:
            parent_dir = self.quotes_dir
        path = self._assign_dir_name(
            fname=submission_info.fname,
            lname=submission_info.lname,
            parent_dir=parent_dir,
        )
        Path.mkdir(path)
        new_file_path = Path.joinpath(path) / submission_info.original_file_path.name
        shutil.move(
            str(submission_info.original_file_path),
            str(new_file_path),
        )
        return new_file_path

    def _check_if_renewal(self, referral: str) -> bool:
        if "RENEWAL" in referral:
            return True
        else:
            return False

    def _assign_dir_name(self, fname: str, lname: str, parent_dir: str):
        dir_name = lname + " " + fname
        dir_path = Path.joinpath(parent_dir) / dir_name
        return self.__validate_save_path(dir_path=dir_path)

    def __validate_save_path(self, dir_path: Path):
        test_dir_path = dir_path
        num = 1
        while Path.exists(test_dir_path):
            num += 1
            test_dir_path = test_dir_path.with_stem(f"{dir_path.stem}-{num}")
        return test_dir_path
