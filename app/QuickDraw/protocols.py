from typing import Protocol
from pathlib import Path


class API(Protocol):
    def create_excel_json(self, data) -> dict[str, any]:
        ...


class HomeModel(Protocol):
    def save_path(
        self,
        path,
        is_quoteform: bool,
    ) -> None:
        ...

    def get_dropdown_options(self) -> list:
        ...

    def filter_only_positive_submissions(
        self,
        raw_checkboxes: dict,
    ) -> list:
        ...

    def handle_redundancies(
        self,
        filtered_submits: list,
    ) -> str:
        ...

    def filter_out_brackets(
        self,
        path,
    ) -> str:
        ...

    def get_all_attachments(self) -> list:
        ...


class RegistrationsModel(Protocol):
    ...


class DirsModel(Protocol):
    ...


class EmailOptionsModel(Protocol):
    ...


class TemplatesModel(Protocol):
    ...


class DialogAllocateMarkets(Protocol):
    def initialize(self, presenter) -> str:
        ...


class DirWatch(Protocol):
    def begin_watch(self) -> None:
        ...


class EmailHandler(Protocol):
    subject: str
    cc: str
    to: str
    body: str
    extra_notes: str
    username: str
    img_sig_url: str
    attachments_list: str

    def view_letter(self) -> bool:
        raise NotImplementedError

    def stringify_subject(self, formatted_values: dict[str, str]) -> str:
        ...


class MSGraphClient(Protocol):
    def run_excel_program(self, json_payload: dict) -> None:
        ...

    def client_already_exists(self) -> bool:
        ...

    def add_row(self) -> None:
        ...

    def close_workbook_session(self) -> None:
        ...

    def send_message(self, message) -> None:
        ...


class Quoteform(Protocol):
    path: Path
    name: str
    fname: str
    lname: str
    year: str
    vessel: str
    referral: str


class Submission(Protocol):
    quoteform: Quoteform
    new_path: Path = None
    status: str
    attachments: list = None
    markets: list[str] = ""
    submit_tool: bool = False


class MainWindow(Protocol):
    extra_notes: str
    use_CC_defaults: bool
    seawave: str | int | bool | list
    primetime: str | int | bool | list
    newhampshire: str | int | bool | list
    americanmodern: str | int | bool | list
    kemah: str | int | bool | list
    concept: str | int | bool | list
    yachtinsure: str | int | bool | list
    century: str | int | bool | list
    intact: str | int | bool | list
    travelers: str | int | bool | list
    home_values: dict[str, str]
    templates_values: dict[str, str]
    email_values: dict[str, str]
    dirs_values: dict[str, str]
    quoteforms_values: dict[str, str]
    quoteform: str
    extra_attachments: str
    selected_template: str
    address: str
    greeting: str
    body: str
    outro: str
    salutation: str
    default_cc1: str
    default_cc2: str
    username: str
    sig_image_file_path: str
    watch_dir: str
    new_biz_dir: str
    renewals_dir: str
    custom_parent_dir: str
    tree: any

    def reset_attributes(
        self,
        positive_value,
        negative_value,
    ):
        ...

    def create_UI_obj(
        self,
        presenter,
    ) -> None:
        ...

    def mainloop(self) -> None:
        ...

    def get_active_focus(
        self,
        event,
    ):
        ...

    def focus_get(self):
        ...

    def get_template_page_values(self) -> dict:
        ...

    def get_all_rows(self) -> list[str]:
        ...

    def set_data_into_treeview(self, data: list[str]):
        ...


class NewFileAlert(Protocol):
    def initialize(
        self,
        presenter,
        submission_info: Submission,
        months: list[str],
    ) -> str:
        ...


class Dirhandler(Protocol):
    def process_dirs(
        self,
        submission_info,
        section_obj,
    ) -> Submission:
        ...


class FormBuilder(Protocol):
    def make(self, file: Path) -> dict[str, str]:
        ...
