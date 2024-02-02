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
    _ids: int
    name: str
    id: str
    address: str
    greeting: str
    body: str
    outro: str
    salutation: str

class Markets(Protocol):
    num_of_carriers: int
    names: list[str]
    _ids: int
    name: str
    id: str
    address: str
    greeting: str
    body: str
    outro: str
    salutation: str

class Submission(Protocol):
    quoteform: Quoteform
    customer: Customer
    vessel: Vessel
    status: Literal[
        "ALLOCATE AND SUBMIT TO MRKTS",
        "SUBMIT TO MRKTS",
        "PENDING WITH UW",
        ]
    markets: list[Market | Markets]
    attachments: list[Path]
    submit_tool: bool


####################################################
##################    MODELS    ####################
####################################################


class API(Protocol):
    def create_excel_json(self, data) -> dict[str, any]:
        ...


class DirHandler(Protocol):
    def process_dirs(
        self,
        submission_info,
        section_obj,
    ) -> Submission:
        ...


class DirsModel(Protocol):
    ...


class DirWatch(Protocol):
    def begin_watch(self) -> None:
        ...


class EmailOptionsModel(Protocol):
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


class SubmissionModel(Protocol):
    def process_request(
        self,
        view_results: dict[str, str | list[str]],
        carriers: dict[str, bool] = None,
    ) -> Submission:
        ...

    def process_quoteform(
        self,
        _quoteform_path: str,
        carriers: dict[str, bool] = None,
        not_validated: bool = True,
    ) -> Submission:
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


class RegistrationsModel(Protocol):
    ...


class TemplatesModel(Protocol):
    ...


class SurplusLinesAutomator(Protocol):
    def start(self) -> None:
        ...


####################################################
###################    VIEWS    ####################
####################################################


class AllocateView(Protocol):
    def initialize(
        self,
        presenter,
        view_interpreter: TkinterDnD.Tk,
        view_palette: Style,
    ) -> str:
        ...


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
    home_values: dict[str, str]
    templates_values: dict[str, str]
    email_values: dict[str, str]
    dirs_values: dict[str, str]
    quoteforms_values: dict[str, str]
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
    ):
        ...

    def create_UI_obj(
        self,
        presenter,
        view_interpreter: TkinterDnD.Tk,
        view_palette: Style,
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
    submission_info: Submission

    def initialize(
        self,
        presenter,
        view_interpreter: TkinterDnD.Tk,
        view_palette: Style,
        submission_info: Submission,
        months: list[str],
    ) -> str:
        ...


class SurplusLinesView(Protocol):
    output_dir: str
    doc_path: str

    def show_view(
        self,
        presenter,
        view_interpreter: TkinterDnD.Tk,
        view_palette: Style,
    ):
        ...


