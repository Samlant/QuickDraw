from typing import Protocol
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
import base64


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


@dataclass
class EmailHandler(Protocol):
    def __init__(self) -> None:
        subject: str
        cc: str
        to: str
        body: str
        extra_notes: str
        username: str
        img_sig_url: str
        attachments_list: list


class API:
    def __init__(self) -> None:
        pass

    def create_excel_json(self, data: ClientInfo) -> dict[str, any]:
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
            "user_id": section.get("user_id").value,
            "group_id": section.get("flordia_office_master_group_id").value,
            "quote_tracker_id": section.get("quote_tracker_id").value,
            "quote_worksheet_id": section.get("quote_worksheet_id").value,
            "quote_table_id": section.get("quote_table_id").value,
            "service_tracker_id": section.get("service_tracker_id").value,
        }
        print(connection_data)
        return connection_data

    def create_attachments_json(self, attachment_paths: list) -> list[dict[str, str]]:
        output = []
        for path in attachment_paths:
            name = Path(path).name
            content = base64.b64encode(open(str(path), "rb").read())
            content = content.decode()
            file = {
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": name,
                "contentBytes": content,
            }
            content_type = self._assign_content_type(path=path)
            if content_type:
                file["contentType"] = content_type
            output.append(file)
        return output

    def _assign_content_type(self, path: str):
        suffix = Path(path).suffix
        if suffix == ".pdf":
            return "application/pdf"
        elif suffix == ".doc" or suffix == ".docx":
            return "application/msword"
        elif suffix == ".zip":
            return "application/zip"
        elif suffix in [".png", ".gif", ".jpeg", ".bmp", ".png", ".tiff"]:
            return f"image/{suffix[1:]}"
        else:
            print(f"Unsupported file format detected. File: {path}")
            print("Not specifying a ContentType because of this...")
            return None

    def create_email_json(
        self, data: EmailHandler
    ) -> dict[str, str | dict[str, str] | list[dict[str, dict[str, str]]]]:
        json = {
            "subject": data.subject,
            "importance": "normal",
            "body": {"contentType": "HTML", "content": data.body},
            "toRecipients": [{"emailAddress": {"address": data.to}}],
            "attachments": data.attachments_list,
        }
        cc_addresses = self._create_address_list(data.cc)
        json["ccRecipients"] = [{"emailAddress": {"address": cc_addresses}}]
        return json

    def _create_address_list(self, input: list[str]) -> list[dict[str, dict[str, str]]]:
        output: list[dict[str, dict[str, str]]] = []
        for address in input:
            x: dict[str, dict[str, str]] = {"emailAddress": {"address": address}}
            output.append(x)
        return output
