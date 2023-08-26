from dataclasses import dataclass
from pathlib import Path
from string import capwords


@dataclass
class Dirs:
    watch_path: Path = (
        Path.home() 
        / "Novamar Insurance"
        / "Novamar US Shared Files - Documents"
        / "Newport Beach Office"
        / "CB NEW CLIENT"
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
            dir.mkdir(exist_ok=True)

    def assign_dir_name(
        self,
        fname: str,
        lname: str,
        parent_dir: Path,
        **kwargs: str,
    ):
        try:
            kwargs["entity"]
            dir_name = kwargs["entity"]
        except KeyError:
            dir_name = capwords(fname) + " " + capwords(lname)
        return parent_dir / dir_name
