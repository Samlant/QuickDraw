from pathlib import Path
from dataclasses import dataclass

@dataclass
class Dirs:
    watch_path: Path = (
            Path.home() / "Novamar Insurance" / "Flordia Office Master - Documents"
        )
    new_biz_path: Path = watch_path / "QUOTES New"
    renewals_path: Path = watch_path / "QUOTES Renewal"

    def make_other_dirs(self, client_dir: Path):
        # dirs: list[Path] = []
        # for dir in dirs:
        #     dir.mkdir()
        pass
####### PLEASE COMPLETE BOTTOM ###################
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