from pprint import pprint
from dataclasses import dataclass, field
from pathlib import Path

from requests import HTTPError

from Quickdraw.models.graph.client import MicrosoftGraphClient
from Quickdraw.models.graph.accessories import (
    ConnectionData,
    Services,
    make_connect_data,
)
from QuickDraw.models.graph.excel import ExcelManager
from QuickDraw.models.graph.outlook import OutlookManager

class GraphAPI:
    """Responsible for creating a connection with Microsoft's Graph API and establishing authorization.  This module is able to read/write data to and from Microsoft services and has been tailored for Business-use."""

    def __init__(self):
        self.graph_client = None
        self.services: Services = Services()
        self.connection_data: ConnectionData = None

    ########################################################
    ################   Preferred Methods   #################
    ########################################################

    def setup(self):
        self.connection_data = make_connect_data()
        self.graph_client = MicrosoftGraphClient(self.connection_data)
        self.graph_client.login()
        self.services.make(self.graph_client)

    def run_graph_calls(self, submission, outlook: bool = False, *args, **kwargs,):
        if outlook:
            emails, send = kwargs["emails"], kwargs["send"]
            manager = OutlookManager(service=self.services.mail)
            try:
                response = manager.send_emails(emails=emails, send=send)
            except HTTPError as e:
                print(f"code: {e.code}\nmessage: {e.message}\nError: {e.error}")


        manager = ExcelManager(
            service=self.services.workbooks,
            group_id=self.connection_data.group_id,
            quote_tracker_id=self.connection_data.quote_tracker_id,
            submission=submission,
        )
        if manager.client_is_already_on_tracker():
            manager.update_client_entry()
        else:
            manager.add_client_to_tracker()

    ########################################################
    ############   END Preferred Methods END   #############
    ########################################################

    ###############################################
    ################ EXCEL SERVICES ###############
    ###############################################

    def client_already_exists(self, quote_table_name: str) -> bool:
        try:
            table_row_obj = self.workbooks_service.get_table_rows(
                group_drive=self.group_id,
                workbook_id=self.quote_tracker_id,
                worksheet_id=self.quote_worksheet_id,
                table_id=quote_table_name,
                session_id=self.session_id,
            )
        except:
            table_row_obj = self.workbooks_service.get_table_rows(
                group_drive=self.group_id,
                workbook_id=self.quote_tracker_id,
                worksheet_id=self.quote_worksheet_id,
                table_id=quote_table_name,
                session_id=self.session_id,
            )
        name = self.json_data.get("values")[0][3]
        vessel = self.json_data.get("values")[0][8]
        for row in table_row_obj["value"]:
            row_name = row["values"][0][3]
            row_vessel = row["values"][0][8]
            if name in row_name and vessel in row_vessel:
                return True
        return False

    def add_row(self, table_name: str = None) -> None:
        "Creates the request to add an excel row"
        if table_name:
            target_table_id = table_name
        else:
            target_table_id = self.quote_table_id
        self.workbooks_service.add_row(
            group_drive=self.group_id,
            workbook_id=self.quote_tracker_id,
            table_id=target_table_id,
            session_id=self.session_id,
            json_data=self.json_data,
        )
        print("added row to excel tracker.")

    def close_workbook_session(self) -> None:
        self.workbooks_service.close_session(
            session_id=self.session_id,
            group_drive=self.group_id,
            item_id=self.quote_tracker_id,
        )
        print("Closed workbooks.")

    ###############################################
    ################ MAIL SERVICES ################
    ###############################################
    def _init_mail_service(self):
        self.mail_service = self.graph_client.mail()

    def create_message_draft(self, json: dict[str, any]):
        """Create message and return the message object & id in a tuple"""
        message = {
            "message": {
                "subject": json["subject"],
                "importance": "Normal",  # Low was default
                "body": {"contentType": "HTML", "content": json["HTML_content"]},
                "toRecipients": json["recipients"],
            }
        }
        print(message)
        new_message_draft = self.mail_service.create_my_message(message=message)
        print(new_message_draft)
        return new_message_draft, new_message_draft["id"]

    def send_message(self, message):
        self._init_graph_client()
        self._init_mail_service()
        self.mail_service.send_my_mail(message=message)

    ###############################################
    ################ USER SERVICES ################
    ###############################################

    def _init_user_service(self):
        self.user_service = self.graph_client.users()

    def get_user_id(self):
        self.user_id = self.user_service.get_user_id()
        return self.user_id
