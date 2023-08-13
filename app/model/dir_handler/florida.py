from dataclasses import dataclass
from pathlib import Path
from string import capwords


@dataclass
class Dirs:
    watch_path: Path = (
        Path.home() / "Novamar Insurance" / "Flordia Office Master - Documents"
    )
    new_biz_path: Path = watch_path / "QUOTES New"
    renewal_path: Path = watch_path / "QUOTES Renewal"

    def make_other_dirs(self, client_dir: Path):
        # dirs: list[Path] = []
        # for dir in dirs:
        #     dir.mkdir(exist_ok=True)
        pass

    def assign_dir_name(
        self,
        fname: str,
        lname: str,
        parent_dir: Path,
    ) -> Path:
        dir_name = lname + " " + capwords(fname)
        return parent_dir / dir_name


#################################################################################
# below is for when dir paths are retrieved from config file,
# then made via default_factory  upon instantiation.

# def make_watch_path(self):
#     if self.test:
#         return Path(app_dir).parent / "tests"
#     else:
#         return (
#             Path.home() / "Novamar Insurance" / "Flordia Office Master - Documents"
#         )

# def make_new_biz_path(self):
#     return self.watch_path / "QUOTES New"

# def make_renewal_path(self):
#     return self.watch_path / "QUOTES Renewal"
