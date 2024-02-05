from typing import Protocol
from datetime import datetime
from pathlib import Path
import base64

from QuickDraw.helper import open_config
from QuickDraw.presenter.protocols import Submission, Quoteform
from QuickDraw.models.graph.accessories import JsonBuilder

class ConnectionData(Protocol):
    scope: list[str]
    client_id: str
    tenant_id: str
    client_secret: str
    redirect_uri: str
    user_id: str
    group_id: str
    quote_tracker_id: str
    credentials: Path

class ExcelManager:

    def __init__(
        self,
        service,
        connection_data: ConnectionData,
        submission: Submission,
    ):
        self.c_data = connection_data
        self.submission = submission
        self.service = service
        self.session_id: str = self._open_session(
            service=service,
            group_id=self.c_data.group_id,
            item_id=self.c_data.quote_tracker_id,
        )
        self.username: str = self.get_user_initials()
        # this is to add the row...
        # dont forget to implement checking if the row already exists
        # and that the whole process (opening session, getting row data,
        # checking that row data, then adding/updating the row depending on
        # that, THEN closing it---is all implemented fairly simply...)
        self.json: JsonBuilder = JsonBuilder()
        self.json.make_excel_row_entry()
        # send JSON to api request. Dont forget that this is only to
        # add a row, so fix it!

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

    def _close_session(self, session: str) -> bool:
        pass

    def client_is_already_on_tracker(self):
        self.service.get_table_rows(
            group_id=self.c_data.group_id,
            workbook_id=self.c_data.quote_tracker_id,
            table_id=self.submission.tracker_month,
            session_id=self.session_id,
        )