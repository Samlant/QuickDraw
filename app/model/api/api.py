from typing import Protocol
from datetime import datetime
from dataclasses import dataclass


@dataclass
class ClientInfo(Protocol):
    def __init__(self) -> None:
        self.fname: str
        self.lname: str
        self.vessel: str
        self.vessel_year: int
        self.referral: str
        self.status: str
        self.extra_attachements: list
        self.markets: list[str]


class API:
    def __init__(self) -> None:
        pass

    def create_json_payload(self, data: ClientInfo) -> dict[str, any]:
        """Uses input from the program and
        compiles it together to create the
        json payload, which will be used as
        the values for the new excel row.
        """
        name = data.lname + data.fname
        start_date = self.__get_current_date()
        vessel = data.vessel
        vessel_year = data.vessel_year
        markets = data.markets
        status = data.status
        referral = data.referral

        json = {
            "index": 2,
            "value": [
                "",  # A
                "",  # B
                "SL",  # C
                name,  # D
                start_date,  # E
                "",  # F
                start_date,  # G
                vessel,  # H
                vessel_year,  # I
                markets,  # J
                "",  # K
                "",  # L
                "",  # M
                "",  # N
                "",  # O
                "",  # P
                "",  # Q
                "",  # R
                "",  # S
                "",  # T
                "",  # U
                "",  # V
                "",  # W
                "",  # X
                status,  # Y
                referral,  # Z
            ],
        }
        return json

    def __get_current_date(self) -> str:
        "Gets todays date and formats it (mm-dd)."
        current_date = datetime.now()
        current_date = f"{current_date.month}-{current_date.day}"
        return current_date

    def get_connection_data(self, config_) -> dict[str, any]:
        config = config_
        section = config.get_section(section_name="graph_api")
        connection_data = {
            "client_id": section.get("client_id").value,
            "tenant_id": section.get("tenant_id").value,
            "client_secret": section.get("client_secret").value,
            "redirect_uri": section.get("redirect_uri").value,
            "group_id": section.get("flordia_office_master_group_id").value,
            "quote_tracker_id": section.get("quote_tracker_id").value,
            "quote_worksheet_id": section.get("quote_worksheet_id").value,
            "quote_table_id": section.get("quote_table_id").value,
            "service_tracker_id": section.get("service_tracker_id").value,
        }
        print(connection_data)
        return connection_data