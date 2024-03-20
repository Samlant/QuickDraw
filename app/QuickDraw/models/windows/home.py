from typing import Literal
from pathlib import Path
from tkinter import filedialog

from QuickDraw.helper import validate_paths, open_config


class HomeModel:
    def __init__(
        self,
    ) -> None:
        self._quoteform_path: str = None
        self._attachments: list = []

    ###############################################
    #############   Getters/Setters   #############
    ###############################################
    
    @property
    def quoteform(self) -> str:
        return str(self._quoteform_path)
    
    @quoteform.setter
    def quoteform(self, new_path: Path):
        del self.quoteform
        self._quoteform_path = new_path

    @quoteform.deleter
    def quoteform(self):
        self._quoteform_path = None

    @property
    def attachments(self) -> list[str | None]:
        paths = []
        for _p in self._attachments:
            paths.append(str(_p))
        return paths
    
    @attachments.setter
    def attachments(self, new_path: Path):
        del self.attachments
        self._attachments.append(new_path)

    @attachments.deleter
    def attachments(self):
        self._attachments = []

    @property
    def all_attachments(self) -> list[str]:
        if len(self.attachments) >= 1:
            attachments = [self.quoteform] + self.attachments
        else:
            return [self.quoteform]
        return attachments

    ###############################################
    ##############   Class Methods   ##############
    ###############################################

    def browse_file_path(
        self,
        path_purpose: Literal[
            "quoteform", 
            "attachments", 
            "sig_image_file_path",    
        ],
    ) -> Path | list[Path]:
        if path_purpose == "quoteform" or path_purpose =="sig_image_file_path":
            try:
                if path_purpose == "quoteform":
                    path: str = filedialog.askopenfilename(filetypes=[("Quoteforms", "*.pdf")])
                else:
                    path: str = filedialog.askopenfilename()
            except AttributeError as e:
                # log.info("The file browser window must have been closed before choosing a file.")
                # log.debug(f"Caught {e}.\nContinuing on...")
                return False
            else:
                return self.valid_path(pathnames=path)
                
        else:
            try:
                path: tuple[str] = filedialog.askopenfilenames()
            except AttributeError as e:
                # log.info("The file browser window must have been closed before choosing a file.")
                # log.debug(f"Caught {e}.\nContinuing on...")
                return False
            else:
                return self.valid_path(pathnames=path)
    
        
    def process_file(
            self,
            path: Path | list[Path] | str,
            path_purpose: Literal[
                "quoteform", 
                "attachments"
                "sig_image_file_path",
                ],
    ) -> str | list[str]:
        if path_purpose == "sig_image_file_path":
            assert(isinstance(path, str))
            config = open_config()
            config.set("email", "signature_image", path)
            config.update_file()
            return path
        elif path_purpose == "quoteform":
            assert(isinstance(path, Path))
            del self.quoteform
            self.quoteform = path
            return path.name
        elif path_purpose == "attachments":
            assert(isinstance(
                path,
                (list[Path] | tuple[Path]),
            ))
            paths = []
            for _p in path:
                self.attachments = _p
                paths.append(_p.name)
            return paths
        # else:
        # raise CustomException as e:
        # point to needing to add specific use-case
    
    ###############################################
    #############   Static Methods   ##############
    ###############################################
    
    @staticmethod
    def valid_path(pathnames: str | list[str]) -> Path | list[Path]:
        try:
            _valid_path = validate_paths(pathnames=pathnames)
        except OSError as e:
            # log.info("The file path is invalid.")
            # log.debug(f"Caught {e}.\nContinuing on...")
            return False
        else:
            return _valid_path