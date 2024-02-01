from pathlib import Path
from dataclasses import dataclass

from QuickDraw.models.submission.customer import Customer
from QuickDraw.models.submission.markets import Market, Markets
from QuickDraw.models.submission.quoteform import Quoteform
from QuickDraw.models.submission.vessel import Vessel


@dataclass
class Submission:
    quoteform: Quoteform
    customer: Customer
    vessel: Vessel
    status: str
    markets: list[Market | Markets] = []
    attachments: list = None
    submit_tool: bool = False


# Maybe use the below for storing the submission info from View...
# Currently view includes a lot of logic for this, but probs not an issue...
@dataclass(frozen=True)
class SubmissionRequest:
    attachments: list[Path]
    extra_notes: str
    user_CC: list[str]
    use_CC_defaults: bool
    markets: dict[str, bool]
