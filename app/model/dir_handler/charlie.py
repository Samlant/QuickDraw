from pathlib import Path
from dataclasses import dataclass


@dataclass
class Dirs:
    watch_path: Path = (
        Path.home() / "NovamarUSSharedFiles" / "Newport Beach Office" / "CB NEW CLIENT"
    )
    new_biz_path: Path = (
        Path.home()
        / "Novamar Insurance"
        / "Novamar US Shared Files - Documents"
        / "Newport Beach Office"
        / "CB NOVAMAR CLIENTS"
    )
    renewal_path: Path = new_biz_path

    def make_other_dirs(self, client_dir: Path):
        client_folder = client_dir / "0. Client Folder"
        qt_forms = client_dir / "1. Quote Forms"
        boat_info = client_dir / "2. Boat Information"
        policy_docs = client_dir / "3. Policy Documents"
        pending_qts = client_dir / "4. Pending Quotes"
        invoice = client_dir / "5. Invoice"
        certificates = client_dir / "6. Certificates"
        dirs: list[Path] = [
            client_folder,
            qt_forms,
            boat_info,
            policy_docs,
            pending_qts,
            invoice,
            certificates,
            invoice,
            certificates,
        ]
        for dir in dirs:
            dir.mkdir()
####### PLEASE COMPLETE BOTTOM ###################
    def assign_dir_name(self, fname: str, lname: str, parent_dir: str):
        dir_name = lname + " " + fname
        dir_path = Path.joinpath(parent_dir) / dir_name
        return self.__validate_save_path(dir_path=dir_path)

    def _validate_save_path(self, dir_path: Path):
        test_dir_path = dir_path
        num = 1
        while Path.exists(test_dir_path):
            num += 1
            test_dir_path = test_dir_path.with_stem(f"{dir_path.stem}-{num}")
        return test_dir_path
