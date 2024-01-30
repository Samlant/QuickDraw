from typing import Protocol


class Quoteform(Protocol):
    """Stores the characteristics of a specific PDF quoteform.

    Attributes:
        id : standardized name used to ID mapping in config.ini file
        name : user-chosen name for the specific mapping
        all other attrs : required fields from PDF

    """

    path: str
    name: str
    fname: str
    lname: str
    year: str
    vessel: str
    referral: str

    def values(self) -> tuple[str]:
        ...


class Presenter(Protocol):
    def browse_file_path(is_quoteform):
        ...

    def btn_save_view_tab(self, tab_name: str):
        ...

    def on_change_template(self, *args, **kwargs) -> None:
        ...

    def process_signature_image_path(self, drag_n_drop_event) -> None:
        ...

    def on_focus_out(self, field_name: str, current_text: str) -> bool:
        ...

    def btn_revert_view_tab(self, tab_name: str):
        ...
