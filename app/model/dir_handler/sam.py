from dataclasses import dataclass
from pathlib import Path
from string import capwords


@dataclass
class Dirs:
    # watch_path: Path = (
    #     Path.home() / "OneDrive - Novamar Insurance" / "Desktop"
    # )
    # new_biz_path: Path = (Path.home()
    #                       / "Novamar Insurance"
    #                       / "Flordia Office Master - Documents"
    #                       / "QUOTES New")
    # renewal_path: Path = (Path.home()
    #                       / "Novamar Insurance"
    #                       / "Flordia Office Master - Documents"
    #                       / "QUOTES Renewal")
    watch_path: Path = Path.home()
    new_biz_path = watch_path
    renewal_path = watch_path

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
