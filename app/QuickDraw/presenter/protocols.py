from typing import Protocol, Literal
from pathlib import Path
from tkinterdnd2 import TkinterDnD
from tkinter.ttk import Style


####################################################
####################    OBJs    ####################
####################################################


class Carrier(Protocol):
    friendly_name: str
    name: str
    id: str
    redundancies: int
    redundancy_group: int


class Customer(Protocol):
    fname: str
    lname: str
    referral: str


class Vessel(Protocol):
    year: str
    make: str


class Quoteform(Protocol):
    path: Path
    name: str
    fname: str
    lname: str
    year: str
    vessel: str
    referral: str


class Market(Protocol):
    name: str
    address: str
    greeting: str
    body: str
    outro: str
    salutation: str


class Submission(Protocol):
    quoteform: Quoteform
    customer: Customer
    vessel: Vessel
    tracker_month: str = ""
    status: Literal[
        "ALLOCATE AND SUBMIT TO MRKTS",
        "SUBMIT TO MRKTS",
        "PENDING WITH UW",
    ]
    carriers: list[Carrier] = []
    markets: list[Market]
    attachments: list[Path]


####################################################
##################    MODELS    ####################
####################################################


class API(Protocol):
    def create_excel_json(self, data) -> dict[str, any]: ...


class DirHandler(Protocol):
    def process_dirs(
        self,
        submission,
        section_obj,
    ) -> Submission: ...


class DirsModel(Protocol): ...


class DirWatch(Protocol):
    def begin_watch(self) -> None: ...


class EmailOptionsModel(Protocol): ...


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

    def stringify_subject(self, formatted_values: dict[str, str]) -> str: ...


class SubmissionModel(Protocol):
    def process_quoteform(
        self,
        _quoteform_path: str,
        carriers: list[Carrier] = [],
        markets: list[Market] = [],
        status: Literal[
            "ALLOCATE MRKTS AND SUBMIT",
            "SUBMIT TO MRKTS",
        ] = "ALLOCATE MRKTS AND SUBMIT",
    ) -> Submission: ...

    def make_markets(
        self,
        market_names: list[str],
    ) -> list[Market]: ...

    def validate_attachments(
        self,
        attachments: list[str],
    ) -> list[Path]: ...


class HomeModel(Protocol):
    def save_path(
        self,
        path,
        is_quoteform: bool,
    ) -> None: ...

    def filter_out_brackets(
        self,
        path,
    ) -> str: ...

    def get_all_attachments(self) -> list: ...


class MSGraphClient(Protocol):
    def run_excel_program(self, json_payload: dict) -> None: ...

    def client_already_exists(self) -> bool: ...

    def add_row(self) -> None: ...

    def close_workbook_session(self) -> None: ...

    def send_message(self, message) -> None: ...


class AlertModel(Protocol):
    def __init__(self) -> None: ...

    def get_current_month(self) -> str: ...

    def get_next_months(self) -> list[str]: ...


class RegistrationsModel(Protocol): ...


class TemplatesModel(Protocol): ...


class SurplusLinesAutomator(Protocol):
    def start(self) -> None: ...


####################################################
###################    VIEWS    ####################
####################################################


class AllocateView(Protocol):
    def initialize(
        self,
        presenter,
        view_interpreter: TkinterDnD.Tk,
        view_palette: Style,
    ) -> str: ...


class MainWindow(Protocol):
    extra_notes: str
    use_CC_defaults: bool
    Seawave: bool
    Primetime: bool
    NewHampshire: bool
    AmericanModern: bool
    Kemah: bool
    Concept: bool
    Yachtinsure: bool
    Century: bool
    Intact: bool
    Travelers: bool
    home: dict[str, str]
    templates: dict[str, str]
    email: dict[str, str]
    dirs: dict[str, str]
    quoteforms: dict[str, str]
    quoteform: str
    attachments: str
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
    ): ...

    def create_UI_obj(
        self,
        presenter,
        view_interpreter: TkinterDnD.Tk,
        view_palette: Style,
    ) -> None: ...

    def mainloop(self) -> None: ...

    def get_active_focus(
        self,
        event,
    ): ...

    def focus_get(self): ...

    def get_template_page_values(self) -> dict: ...

    def get_all_rows(self) -> list[str]: ...

    def set_data_into_treeview(self, data: list[str]): ...


class NewFileAlert(Protocol):
    submission: Submission

    def initialize(
        self,
        presenter,
        view_interpreter: TkinterDnD.Tk,
        view_palette: Style,
        submission: Submission,
        months: list[str],
    ) -> str: ...


class SurplusLinesView(Protocol):
    output_dir: str
    doc_path: str

    def show_view(
        self,
        presenter,
        view_interpreter: TkinterDnD.Tk,
        view_palette: Style,
    ): ...
