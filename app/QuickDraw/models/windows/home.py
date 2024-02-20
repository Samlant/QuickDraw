from typing import Protocol
from dataclasses import dataclass
from pathlib import Path

from QuickDraw.helper import validate_paths, open_config
from tkinter import filedialog


@dataclass
class ClientInfo(Protocol):
    markets: list
    status: str


class HomeModel:
    def __init__(
        self,
    ) -> None:
        self.quoteform_path: str = None
        self.attachments: list = []

    def get_all_attachments(self) -> list:
        attachments = []
        attachments.append(self.quoteform_path)
        if len(self.attachments) >= 1:
            for _a in self.attachments:
                attachments.append(_a)
        return attachments

    #####################################################################
    #####################################################################
    #####################################################################
    #####################################################################

    def browse_file_path(
        self,
        path_purpose: str,
        event = None,
    ):
        if path_purpose == "quoteform" or path_purpose =="sig_image_file_path":
            try:
                if path_purpose == "quoteform":
                    path: str = filedialog.askopenfilename(filetypes=[("Quoteforms", "*.pdf")])
                else:
                    path: str = filedialog.askopenfilename()
            except AttributeError as e:
                # log.info("The file browser window must have been closed before choosing a file.")
                # log.debug(f"Caught {e}.\nContinuing on...")
                pass
            else:
                _valid_path = self.valid_path(pathnames=path)
        else:
            try:
                path: tuple[str] = filedialog.askopenfilenames()
            except AttributeError as e:
                # log.info("The file browser window must have been closed before choosing a file.")
                # log.debug(f"Caught {e}.\nContinuing on...")
                pass
            else:
                _valid_path = self.valid_path(pathnames=path)
        return _valid_path
        
    def valid_path(self, pathnames: str | list[str]) -> Path | list[Path]:
        try:
            _valid_path = validate_paths(pathnames=pathnames)
        except OSError as e:
            # log.info("The file path is invalid.")
            # log.debug(f"Caught {e}.\nContinuing on...")
            pass
        else:
            return _valid_path
        
    def process_file(self, path: str, path_purpose: str) -> str:
        if path_purpose == "sig_image_file_path":
            config = open_config()
            config.set("email", "signature_image", path)
            return path
        else:
            _p = validate_paths(pathnames=path)
        if path_purpose == "quoteform":
            self.quoteform_path = str(_p)
        elif path_purpose == "attachments":
            self.attachments.append(str(_p))
        return _p.name

    def save_path(self, path: Path | list[Path], path_purpose: str) -> None:
        if path_purpose == "quoteform" and isinstance(path, Path):
            self.quoteform_path = str(path)
        else:
            for _a in path:
                self.attachments.append(str(_a))