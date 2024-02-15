from typing import Protocol
from dataclasses import dataclass
from pathlib import Path

from QuickDraw.helper import validate_paths
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
        event=None,
        is_quoteform: bool = False,
    ):
        if is_quoteform:
            try:
                path: str = filedialog.askopenfilename(filetypes=[("Quoteforms", "*.pdf")])
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
        self.save_path(path=_valid_path, path_purpose=is_quoteform)
        
    def valid_path(self, pathnames: str | list[str]) -> Path | list[Path]:
        try:
            _valid_path = validate_paths(pathnames=pathnames)
        except OSError as e:
            # log.info("The file path is invalid.")
            # log.debug(f"Caught {e}.\nContinuing on...")
            pass
        else:
            return _valid_path

    def save_path(self, path: Path | list[Path], path_purpose: str) -> None:
        if path_purpose == "quoteform" and isinstance(path, Path):
            self.quoteform_path = str(path)
        else:
            for _a in path:
                self.attachments.append(str(_a))

    def filter_out_brackets(self, path: str) -> str:
        """Cleans up the path str by removing any brackets---if present."""
        if "{" in path:
            path = path.translate({ord(c): None for c in "{}"})
        return path
