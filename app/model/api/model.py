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
        self.submit_tool: bool


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

months: dict[int, str] = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


class API:
    def __init__(self) -> None:
        pass

    def create_excel_json(self, data: ClientInfo) -> dict[str, any]:
        """Uses input from the program and
        compiles it together to create the
        json payload, which will be used as
        the values for the new excel row.
        """
        name = data.lname + " " + data.fname
        start_date = self.__get_current_date()
        vessel = data.vessel
        vessel_year = data.vessel_year
        if data.submit_tool:
            markets = self.__get_submitted_markets(data.markets)
            market_status = self.__format_markets_from_submission_tool(data.markets)
        else:
            markets = self.__get_allocated_markets(data.markets)
            market_status = self.__assign_empty_str_markets()
        status = data.status
        referral = data.referral

        json = {
            "index": 2,
            "values": [
                [
                    "",  # A
                    "",  # B
                    "SL",  # C
                    name,  # D
                    start_date,  # E
                    "",  # F
                    start_date,  # G
                    vessel_year,  # H
                    vessel,  # I
                    markets,  # J
                    "",  # K - CH
                    "",  # L - MK
                    "",  # M - AI
                    market_status["AM"],  # N - AM
                    "",  # O - PG
                    market_status["SW"],  # P - SW
                    market_status["KM"],  # Q - KM
                    market_status["CP"],  # R - CP
                    market_status["NH"],  # S - NH
                    market_status["IN"],  # T - IN
                    market_status["TV"],  # U - TV
                    "",  # V
                    "",  # W
                    "",  # X
                    status,  # Y
                    referral,  # Z
                ]
            ],
        }
        return json

    def __get_allocated_markets(self, markets: list[str]) -> list:
        mrkt: list[str] = [mrkt for mrkt in markets]
        mrkt = ", ".join(mrkt)
        print(mrkt)
        return mrkt
    
    def __get_submitted_markets(self, markets: list[str]) -> list:
        mrkt = []
        if "Seawave" in markets:
            mrkt.append("SW")
        elif "New hampshire" in markets:
            mrkt.append("NH")
        elif "Prime Time" in markets:
            mrkt.append("PT")
        elif "American Modern" in markets:
            mrkt.append("AM")
        elif "Kemah Marine" in markets:
            mrkt.append("KM")
        elif "Concept Special Risks" in markets:
            mrkt.append("CP")
        elif "Yachtinsure" in markets:
            mrkt.append("YI")
        elif "Travelers" in markets:
            mrkt.append("TV")
        elif "Intact" in markets:
            mrkt.append("IN")
        elif "Century" in markets:
            mrkt.append("CE")
        else:
            return []
        return mrkt
    
    def __assign_empty_str_markets(self) -> dict[str, str]:
        mrkt_status = {}
        mrkt_status["AM"] = ""
        mrkt_status["SW"] = ""
        mrkt_status["KM"] = ""
        mrkt_status["CP"] = ""
        mrkt_status["NH"] = ""
        mrkt_status["IN"] = ""
        mrkt_status["TV"] = ""
        return mrkt_status
    
    def __format_markets_from_submission_tool(
        self, markets: list[str]
    ) -> dict[str, str]:
        submitted: dict[str, str] = {}
        if len(markets) >= 1:
            if "Seawave" in markets:
                submitted["SW"] = "P"
            else:
                submitted["SW"] = ""
            if "Hampshire" in markets:
                submitted["NH"] = "P"
            else:
                submitted["NH"] = ""
            if "PT" in markets:
                submitted["PT"] = "P"
            else:
                submitted["PT"] = ""
            if "AM" in markets:
                submitted["AM"] = "P"
            else:
                submitted["AM"] = ""
            if "KM" in markets:
                submitted["KM"] = "P"
            else:
                submitted["KM"] = ""
            if "CP" in markets:
                submitted["CP"] = "P"
            else:
                submitted["CP"] = ""
            if "YI" in markets:
                submitted["YI"] = "P"
            else:
                submitted["YI"] = ""
            if "TV" in markets:
                submitted["TV"] = "P"
            else:
                submitted["TV"] = ""
            if "IN" in markets:
                submitted["IN"] = "P"
            else:
                submitted["IN"] = ""
        else:
            submitted = {
                "SW": "",
                "NH": "",
                "PT": "",
                "AM": "",
                "KM": "",
                "CP": "",
                "YI": "",
                "TV": "",
                "IN": "",
            }
        return submitted

    def __get_current_date(self) -> str:
        "Gets todays date and formats it (mm-dd)."
        current_date = datetime.now()
        current_date = f"{current_date.month}-{current_date.day}"
        return current_date

    def get_current_month(self):
        current_month = datetime.now().month
        return months[current_month].lower()

    def get_future_two_months(self):
        current_month = datetime.now().month
        next_month = current_month + 1
        if next_month > 12:
            next_month -= 12
        second_month = current_month + 2
        if second_month > 12:
            second_month -= 12
            print(current_month, next_month, second_month)
        next_month = months[next_month].lower()
        second_month = months[second_month].lower()
        return next_month, second_month
    


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
        self, email: EmailHandler
    ) -> dict[str, str | dict[str, str] | list[dict[str, dict[str, str]]]]:
        json = {
            "message": {
                "subject": email.subject,
                "importance": "normal",
                "body": {"contentType": "HTML", "content": email.body},
                "attachments": email.attachments_list,
                "toRecipients": self.__create_address_list(email.to),
            }
        }
        if email.cc:
            json["message"]["ccRecipients"] = self.__create_address_list(email.cc)
        return json

    def __create_address_list(self, addresses: list[str]) -> list[dict[str, dict[str, str]]]:
        output: list[dict[str, dict[str, str]]] = []
        if not addresses:
            addresses = [""]
        if isinstance(addresses, list):
            for address in addresses:
                x: dict[str, dict[str, str]] = {"emailAddress": {"address": address}}
                output.append(x)
        elif isinstance(addresses, str):
            x = {"emailAddress": {"address": addresses}}
            output.append(x)
        return output
