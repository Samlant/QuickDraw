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

    def setup_api(self, connection_data) -> bool:
        self._set_connection_data(connection_data)
        if not self._init_graph_client():
            return False
        print("starting users service")
        self._init_user_service()
        return True

    def _set_connection_data(self, connection_data):
        pprint(connection_data)
        self.client_id = connection_data.get("client_id").value
        self.tenant_id = connection_data.get("tenant_id").value
        self.client_secret = connection_data.get("client_secret").value
        self.redirect_uri = connection_data.get("redirect_uri").value
        # self.user_id = connection_data.get("user_id").value
        self.group_id = connection_data.get("group_id").value
        self.quote_tracker_id = connection_data.get("quote_tracker_id").value
        # self.quote_worksheet_id = connection_data.get("quote_worksheet_id").value
        # self.quote_table_id = connection_data.get("quote_table_id").value
        # self.service_tracker_id = connection_data.get("service_tracker_id").value
        pprint("set connection data successfully.")

    def run_excel_program(self, json_payload: dict[any, any]):
        self.json_data = json_payload
        self._init_graph_client()
        self._init_workbooks_service()
        self.session_id = self._create_workbook()

    def _init_graph_client(self) -> bool:
        self.graph_client = MicrosoftGraphClient(
            client_id=self.client_id,
            tenant_id=self.tenant_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scopes,
            credentials=self.credentials,
        )
        print("logging into graph_client.")
        if self.try_login():
            return True
        else:
            if self.try_login():
                return True
            else:
                return False

    def try_login(self) -> bool:
        if self.graph_client.login():
            print("logged into graph client.")
            return True
        else:
            return False

    ###############################################
    ################ EXCEL SERVICES ###############
    ###############################################
    def _init_workbooks_service(self):
        self.workbooks_service = self.graph_client.workbooks()

    def _create_workbook(self):
        print("creating workbook session.")
        session_response = self.workbooks_service.create_session(
            group_drive=self.group_id,
            item_id=self.quote_tracker_id,
        )
        print("created workbook session.")
        print("The session ID for the API is:")
        pprint(session_response["id"])
        return session_response["id"]

    # def _get_table_id(self):
    #     tables_data = self.workbooks_service.list_tables_id(group_drive=self.group_id, item_id=self.quote_tracker_id,)
    #     table_data = tables_data["value"].pop()
    #     # Change from popping last element to popping the correct month's table id
    #     self.quote_table_id = table_data["id"]

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
        "Creates the reques to add an excel row"
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
        pprint(message)
        new_message_draft = self.mail_service.create_my_message(message=message)
        pprint(new_message_draft)
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
