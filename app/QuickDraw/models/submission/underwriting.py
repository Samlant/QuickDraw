from pathlib import Path
from dataclasses import dataclass
from typing import Literal, NamedTuple

from QuickDraw.models.submission.customer import Customer
from QuickDraw.models.submission.quoteform import Quoteform
from QuickDraw.models.submission.vessel import Vessel


class Carrier(NamedTuple):
    friendly_name: str
    name: str
    id: str
    redundancies: int = 0
    redundancy_group: int = 0
    status: str = ""


@dataclass
class Market:
    name: str
    ids: list[str]
    status: Literal["", "P"]
    address: str
    greeting: str
    body: str
    outro: str
    salutation: str


@dataclass
class Submission:
    quoteform: Quoteform
    customer: Customer
    vessel: Vessel
    tracker_month: str = ""
    status: Literal[
        "ALLOCATE AND SUBMIT TO MRKTS",
        "SUBMIT TO MRKTS",
        "PENDING WITH UW",
    ] = "ALLOCATE AND SUBMIT TO MRKTS"
    carriers: list[Carrier] = []
    markets: list[Market] = []
    attachments: list[Path] = []
