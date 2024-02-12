from typing import NamedTuple
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

from QuickDraw.helper import open_config, MS_GRAPH_STATE_PATH, AVAILABLE_CARRIERS
from QuickDraw.models.submission.underwriting import Submission
from QuickDraw.models.graph.services.mail import Mail
from QuickDraw.models.graph.services.users import Users
from QuickDraw.models.graph.services.workbooks_and_charts.workbook import Workbooks

SCOPES = [
    "Files.ReadWrite.All",
    "Mail.ReadWrite",
    "Mail.Send",
    "User.Read",
]


class ConnectionData(NamedTuple):
    scope: list[str]
    client_id: str
    tenant_id: str
    client_secret: str
    redirect_uri: str
    user_id: str
    group_id: str
    quote_tracker_id: str
    credentials: Path


def make_connect_data() -> ConnectionData:
    data_from_config = _retrieve_properties_from_config()
    data_from_config["scope"] = SCOPES
    data_from_config["credentials"] = MS_GRAPH_STATE_PATH
    return ConnectionData(**data_from_config)


def _retrieve_properties_from_config() -> dict[str, str]:
    config = open_config()
    section = config.get_section(section_name="graph_api").to_dict()
    connection_data = {}
    for key, value in section.items():
        connection_data[key] = value
    return connection_data


@dataclass(init=False)
class Services:
    workbooks: Workbooks
    mail: Mail
    user: Users

    def make(self, graph_client):
        self.workbooks = graph_client.workbooks()
        self.workbooks = graph_client.mail()
        self.workbooks = graph_client.users()


class JsonBuilder:
    def __init__(self):
        pass

    def make_excel_row_entry(
        self,
        submission: Submission,
        initials: str,
        index: str,
        results: dict[str, str],
    ) -> dict[str, int | list[list[str]]]:
        carriers = self._assign_carrier_statuses(
            submission=submission,
            results=results,
        )
        _ = datetime.now()
        current_date = f"{_.month}-{_.day}"

        json = {
            "index": index,
            "values": [
                [
                    "",  # A
                    "",  # B
                    initials,  # C
                    submission.customer.lfname,  # D
                    current_date,  # E
                    "",  # F
                    current_date,  # G
                    submission.vessel.year,  # H
                    submission.vessel.make,  # I
                    submission.markets,  # J
                    "",  # K - CH
                    "",  # L - MK
                    "",  # M - AI
                    carriers["AM"],  # N - AM
                    "",  # O - PG
                    carriers["SW"],  # P - SW
                    carriers["KM"],  # Q - KM
                    carriers["CP"],  # R - CP
                    carriers["NH"],  # S - NH
                    carriers["IN"],  # T - IN
                    carriers["TV"],  # U - TV
                    "",  # V
                    "",  # W
                    "",  # X
                    submission.status,  # Y
                    submission.customer.referral,  # Z
                ]
            ],
        }
        return json

    def make_outlook(self):
        pass

    def _assign_carrier_statuses(
        self,
        submission: Submission,
        results = None,
    ) -> dict[str, str]:
        carriers = {}
        status = ""
        if results:
            for _r in results.values():
                if _r["success"]:
                    status = "P"
                for _id in _r["ids"]:
                    carriers[_id] = status
            return carriers
        else:
            for carrier in submission.carriers:
                carriers[carrier.id] = status
            for carrier in AVAILABLE_CARRIERS:
                if carrier.id not in carriers:
                    carriers[carrier.id] = status
            return carriers
