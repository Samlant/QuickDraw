from pprint import pprint

from model.api.ms_graph.client import MicrosoftGraphClient


class MSGraphClient:
    """Responsible for creating a connection with Microsoft's Graph API and establishing authorization.  This module is able to read/write data to and from Microsoft services and has been tailored for Business-use."""

    def __init__(self, ms_graph_state_path: str):
        self.scopes = [
            "Files.ReadWrite.All",
            "Mail.ReadWrite",
            "Mail.Send",
            "User.Read",
        ]
        self.json_data: dict[any, any] = None
        self.graph_client = None
        self.workbooks_service = None
        self.mail_service = None
        self.user_service = None
        self.client_id: str = None
        self.tenant_id: str = None
        self.client_secret: str = None
        self.redirect_uri: str = None
        self.user_id: str = None
        self.group_id: str = None
        self.quote_tracker_id: str = None
        self.quote_worksheet_id: str = None
        self.quote_table_id: str = None
        self.service_tracker_id: str = None
        self.credentials = ms_graph_state_path
        self.session_id = None

    def setup_api(self, connection_data):
        self._set_connection_data(connection_data)
        self._init_graph_client()
        pprint("set graph_session successfully.")
        print("starting workbooks service")
        self._init_workbooks_service()
        print("starting mail service")
        self._init_mail_service()
        print("starting users service")
        self._init_user_service()

    def _set_connection_data(self, connection_data):
        pprint(connection_data)
        self.client_id = connection_data.get("client_id").value
        self.tenant_id = connection_data.get("tenant_id").value
        self.client_secret = connection_data.get("client_secret").value
        self.redirect_uri = connection_data.get("redirect_uri").value
        # self.user_id = connection_data.get("user_id").value
        self.group_id = connection_data.get("group_id").value
        self.quote_tracker_id = connection_data.get("quote_tracker_id").value
        self.quote_worksheet_id = connection_data.get("quote_worksheet_id").value
        self.quote_table_id = connection_data.get("quote_table_id").value
        self.service_tracker_id = connection_data.get("service_tracker_id").value
        pprint("set connection data successfully.")

    def run_excel_program(self, json_payload: dict[any, any]):
        self.json_data = json_payload
        self.session_id = self._create_workbook()

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
        """Create message and return the message object & id in a tuple"""
        new_message_draft = self.mail_service.create_my_message(
            message={
                "subject": json["subject"],
                "importance": "Normal",  # Low was default
                "body": {"contentType": "HTML", "content": json["HTML_content"]},
                "toRecipients": json["recipients"],
            }
        )
        pprint(new_message_draft)
        return new_message_draft, new_message_draft["id"]

    def send_message(self, message):
        # Consider accessing this below call directly from Presenter...
        self.mail_service.send_my_mail(message=message)

    ###############################################
    ################ USER SERVICES ################
    ###############################################

    def _init_user_service(self):
        self.user_service = self.graph_client.users()

    def get_user_id(self):
        self.user_id = self.user_service.get_user_id()
        return self.user_id
