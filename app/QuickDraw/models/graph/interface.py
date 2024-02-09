from Quickdraw.models.graph.client import MicrosoftGraphClient
from Quickdraw.models.graph.accessories import (
    ConnectionData,
    Services,
    make_connect_data,
)
from QuickDraw.models.graph.excel import ExcelManager
from QuickDraw.models.graph.outlook import OutlookManager

class GraphAPI:
    """Responsible for creating a connection with Microsoft's Graph API
    and establishing authorization.  This module is able to read/write
    data to and from Microsoft services and has been tailored for
    Business-use.
    """

    def __init__(self):
        self.graph_client = None
        self.services: Services = Services()
        self.connection_data: ConnectionData = None

    def setup(self) -> bool:
        self.connection_data = make_connect_data()
        count = 0
        while count < 2:
            try:
                self.graph_client = MicrosoftGraphClient(self.connection_data)
                self.graph_client.login()
            except PermissionError as pe:
                print(f"""Permission Error upon logging in.\nDeleting credentials
                      & trying again.\n{str(pe)}""")
                count += 1
                self.connection_data.credentials.unlink(missing_ok=True)
            else:
                self.services.make(self.graph_client)
                return True
        return False

    def run_graph_calls(self, submission, outlook: bool = False, *args, **kwargs,):
        results = None
        if outlook:
            emails, auto_send = kwargs["emails"], kwargs["auto_send"]
            manager = OutlookManager(service=self.services.mail)
            results = manager.send_emails(emails=emails, auto_send=auto_send)
        manager = ExcelManager(
            service=self.services.workbooks,
            group_id=self.connection_data.group_id,
            quote_tracker_id=self.connection_data.quote_tracker_id,
            submission=submission,
        )
        if index := manager.client_already_on_tracker():
            manager.process_client_entry(results=results, index=index)
        else:
            manager.process_client_entry(results=results)
        manager.close_session()