from typing import Protocol
from datetime import datetime
from pathlib import Path
import base64

from QuickDraw.helper import open_config
from QuickDraw.presenter.protocols import Submission
from QuickDraw.models.graph.accessories import JsonBuilder

class ExcelManager:

    def __init__(
        self,
        service,
        group_id: str,
        quote_tracker_id: str,
        submission: Submission,
    ):
        self.group_id = group_id
        self.quote_tracker_id = quote_tracker_id
        self.submission = submission
        self.service = service
        self.session_id: str = self._open_session(
            service=service,
            group_id=self.group_id,
            item_id=self.quote_tracker_id,
        )
        

    def _open_session(
        self,
        service,
        group_id: str,
        item_id: str,
    ) -> str:
        session_response = service.create_session(
            group_drive=group_id,
            item_id=item_id,
        )
        return session_response["id"]

    def get_user_initials(self):
        config = open_config()
        username = config.get("email", "username").value
        portions = username.split(sep=" ")
        first, last = portions[0], portions[len(portions) - 1]
        initials = f"{first[0]}{last[0]}"
        return initials.upper()

    def close_session(self) -> bool:
        self.service.close_session(
            session_id=self.session_id,
            group_drive=self.group_id,
            item_id=self.quote_tracker_id,
        )
        return True
    
    def process_client_entry(self, results: dict[str, str] | None, index: str = "",):
        initials = self.get_user_initials()
        json = JsonBuilder()
        row_data = json.make_excel_row_entry(
            submission=self.submission,
            initials=initials,
            index=index,
            results=results,
        )
        self._add_row(json_excel_row=row_data, index=index)

    def _add_row(self, json_excel_row, index: str = ""):
        self.service.add_row(
            group_drive=self.group_id,
            workbook_id=self.quote_tracker_id,
            table_id = self.submission.tracker_month,
            session_id=self.session_id,
            json_data=json_excel_row,
            index=index,
            )

    def client_already_on_tracker(self) -> str | bool:
        rows_data = list[dict[str, int | list[list, str | int]]]
        rows_data = self.service.get_table_rows(
            group_id=self.group_id,
            workbook_id=self.quote_tracker_id,
            table_id=self.submission.tracker_month,
            session_id=self.session_id,
        )["value"]
        target_name = self.submission.customer.lfname
        target_vessel_year = self.submission.vessel.year
        target_vessel_make = self.submission.vessel.make
        print("Identifying if client already exists on tracker...")
        for row in rows_data:
            row_name = row["values"][0][3]
            row_vessel_year = row["values"][0][7]
            row_vessel_make = row["values"][0][8]
            if ((target_name == row_name) and 
                (target_vessel_year == row_vessel_year) and 
                (target_vessel_make == row_vessel_make)):
                index = str(row["index"])
                return index
        return False
