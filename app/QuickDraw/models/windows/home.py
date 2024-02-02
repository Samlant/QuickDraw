from typing import Protocol
from dataclasses import dataclass
from pathlib import Path

from QuickDraw.helper import open_config, validate_paths
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
            for attachment in self.attachments:
                attachments.append(attachment)
        else:
            return attachments
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
            path: str = filedialog.askopenfilename(filetypes=[("Quoteforms", "*.pdf")])
        else:
            path: list[str] = filedialog.askopenfilenames()

        if self._validate_paths(path):
            self.save_path(path, is_quoteform)
            return path
        else:
            raise ValueError(f"Invalid file path. Path={path}")

    def _validate_paths(self, path: str | list[str]) -> bool:
        if isinstance(path, list):
            if path == []:
                return False
        elif isinstance(path, list):
            if path == "":
                return False
        elif not Path(path).exists:
            return False
        return True

    def save_path(self, path: str, path_purpose: str) -> None:
        if path_purpose == "quoteform":
            self.quoteform_path = path
        else:
            self.attachments.append(path)

    def filter_out_brackets(self, path: str) -> str:
        """Cleans up the path str by removing any brackets---if present."""
        if "{" in path:
            path = path.translate({ord(c): None for c in "{}"})
        return path
