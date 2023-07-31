from pprint import pprint

from model.api.ms_graph.client import MicrosoftGraphClient


class MSGraphClient:
    """Responsible for creating a connection with Microsoft's Graph API and establishing authorization.  This module is able to read/write data to and from Microsoft services and has been tailored for Business-use."""

    def __init__(self, ms_graph_state_path: str):
        self.scopes = [
            "Files.ReadWrite.All",
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

    def run_program(self, connection_data: dict, json_payload: dict):
        self.json_data = self.assign_json_payload(json_payload=json_payload)
        self._set_connection_data(connection_data=connection_data)
        self._init_graph_client()
        self._init_workbooks_service()
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

    def assign_json_payload(self, json_payload: dict = None):
        # json_payload = json_payload
        json_payload = {
            "index": 1,
            "values": [
                [
                    "",
                    "",
                    "JN",
                    "TEST Name",
                    "7/22",
                    "",
                    "",
                    "2020",
                    "Hurricane 23",
                    "AM, AI, PG",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "submit to markets",
                    "TEST QUALITY BOATS",
                ]
            ],
        }
        pprint(json_payload)
        return json_payload

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
