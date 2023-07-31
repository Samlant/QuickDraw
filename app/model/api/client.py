from pprint import pprint

from model.api.ms_graph.client import MicrosoftGraphClient


class MSGraphClient:
    """Responsible for creating a connection with Microsoft's Graph API and establishing authorization.  This module is able to read/write data to and from Microsoft services and has been tailored for Business-use."""

    def __init__(self, ms_graph_state_path: str):
        self.scopes = [
            "Files.ReadWrite.All",
            "Mail.ReadWrite",
        ]
        self.json_data = None
        self.graph_client = None
        self.workbooks_service = None
        self.client_id = None
        self.tenant_id = None
        self.client_secret = None
        self.redirect_uri = None
        self.group_id = None
        self.quote_tracker_id = None
        self.quote_worksheet_id = None
        self.quote_table_id = None
        self.service_tracker_id = None
        self.credentials = ms_graph_state_path
        self.session_id = None

    # CONFIG_FILE = Path(__file__).parent.resolve() / "configs" / "config.ini"
    # CREDENTIALS_FILE = (
    #     Path(__file__).parent.resolve() / "configs" / "ms_graph_state.jsonc"
    # )

    def run_excel_program(self, connection_data: dict, json_payload: dict):
        self.json_data = json_payload
        self._set_connection_data(connection_data=connection_data)
        self._init_graph_client()
        self._init_workbooks_service()
        # self._init_mail_service()
        self.session_id = self._create_workbook()

    def _set_connection_data(self, connection_data: dict):
        pprint(connection_data)
        self.client_id = connection_data["client_id"]
        self.tenant_id = connection_data["tenant_id"]
        self.client_secret = connection_data["client_secret"]
        self.redirect_uri = connection_data["redirect_uri"]
        self.group_id = connection_data["group_id"]
        self.quote_tracker_id = connection_data["quote_tracker_id"]
        self.quote_worksheet_id = connection_data["quote_worksheet_id"]
        self.quote_table_id = connection_data["quote_table_id"]
        self.service_tracker_id = connection_data["service_tracker_id"]
        pprint("set connection data successfully")

    def _init_graph_client(self):
        self.graph_client = MicrosoftGraphClient(
            client_id=self.client_id,
            tenant_id=self.tenant_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scopes,
            credentials=self.credentials,
        )
        pprint("logging into graph_client.")
        self.graph_client.login()
        pprint("logged into graph client.")

###############################################
################ EXCEL SERVICES ###############
###############################################
    def _init_workbooks_service(self):
        self.workbooks_service = self.graph_client.workbooks()
    
    
    def _create_workbook(self):
        pprint("creating workbook session.")
        session_response = self.workbooks_service.create_session(
            group_drive=self.group_id,
            item_id=self.quote_tracker_id,
        )
        pprint("created workbook session.")
        pprint(session_response["id"])
        return session_response["id"]

    def add_row(self) -> None:
        "Creates the reques to add an excel row"
        self.workbooks_service.add_row(
            group_drive=self.group_id,
            workbook_id=self.quote_tracker_id,
            worksheet_id=self.quote_worksheet_id,
            table_id=self.quote_table_id,
            session_id=self.session_id,
            json_data=self.json_data,
        )
        pprint("added row to excel tracker.")

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
        new_message_draft = self.mail_service.create_my_message(
            message={
                "subject": json["subject"],
                "importance": "Normal", # Low was default
                "body": {"contentType": "HTML", "content": json["HTML_content"]},
                "toRecipients": json["recipients"],
                })
        pprint(new_message_draft)
        return new_message_draft

    def get_message_id(self, message_draft):
        new_message_id = message_draft["id"]
        return new_message_id
    
    def send_message(self, message_id):
        # Consider accessing this below call directly from Presenter...
        self.mail_service.send_my_message(message_id=message_id)