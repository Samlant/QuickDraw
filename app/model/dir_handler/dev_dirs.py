from pathlib import Path
from dataclasses import dataclass
from string import capwords


@dataclass
class DevDirs:
    app_dir: Path = Path(__file__).parents[3]
    watch_path: Path = app_dir / "tests"
    new_biz_path: Path = app_dir / "tests" / "QUOTES New"
    renewal_path: Path = app_dir / "tests" / "QUOTES Renewal"

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
    ) -> Path:
        dir_name = lname + " " + capwords(fname)
        return parent_dir / dir_name
