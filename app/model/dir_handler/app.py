from pathlib import Path
import shutil

from model.dir_handler.charlie import Dirs as CharlieDirs
from model.dir_handler.florida import Dirs as FloridaDirs


class DirHandler:
    def __init__(
        self,
        user: str,
    ) -> None:
        self.user = user
        if self.user == "florida":
            self.dirs: FloridaDirs = FloridaDirs()
        elif self.user == "charlie":
            self.dirs: CharlieDirs = CharlieDirs()
        elif self.dirs == "ericka":
            raise NotImplementedError
        elif self.dirs == "peter":
            raise NotImplementedError
        elif self.dirs == "courtney":
            raise NotImplementedError
        elif self.dirs == "ed":
            raise NotImplementedError
        elif self.dirs == "craig":
            raise NotImplementedError
        elif self.dirs == "rob":
            raise NotImplementedError
        else:
            raise ValueError

    def get_watch_dir(self) -> Path:
        """returns the watch dir for the specific user in a Path obj."""
        return self.dirs.watch_path

    def create_dirs(self, submission_info) -> tuple[Path, Path]:
        """Creates the client folder and moves the .PDF file to it.
        This includes validating and renaming the dir until there's
        no collission with existing dirs.

        Returns:  Path obj of the new path of the .PDF file itself.
        """
        referral = submission_info.referral
        fname = submission_info.fname
        lname = submission_info.lname

        self._create_client_dir(referral=referral, fname=fname, lname=lname,)
    
    
    def _create_client_dir(self, referral, fname, lname):
        if self._check_if_renewal(referral):
            parent_dir = self.dirs.renewal_path
        else:
            parent_dir = self.dirs.new_biz_path
        client_dir = self._assign_dir_name(
            fname=fname,
            lname=lname,
            parent_dir=parent_dir,
        )
        client_dir.mkdir()
        # Path.mkdir(path)
        return client_dir
    
    def move_path(self, client_dir: Path, orgin_file: Path) -> Path:
        """Moves the client quoteform from its origin to dest dir."""
        new_file_path = client_dir / orgin_file.name
        shutil.move(
            str(orgin_file),
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
