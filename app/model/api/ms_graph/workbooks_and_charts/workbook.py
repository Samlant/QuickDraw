from model.api.ms_graph.session import GraphSession


class Workbooks:

    """
    ## Overview:
    ----
    You can use Microsoft Graph to allow web and mobile applications to
    read and modify Excel workbooks stored in OneDrive for Business, SharePoint
    site or Group drive. The Workbook (or Excel file) resource contains all the
    other Excel resources through relationships. You can access a workbook through
    the Drive API by identifying the location of the file in the URL.
    """

    def __init__(self, session: object) -> None:
        """Initializes the `Workbooks` object.

        ### Parameters
        ----
        session : object
            An authenticated session for our Microsoft Graph Client.
        """

        # Set the session.
        self.graph_session: GraphSession = session

    def create_session(
        self,
        group_drive: str = None,
        item_id: str = None,
        item_path: str = None,
    ) -> dict:
        """Create a new Workbook Session using the Item ID or Item Path

        ### Parameters
        ----
        item_id : str (optional, Default=None)
            The Drive Item Resource ID.

        item_path : str (optional, Default=None)
            The Item Path. An Example would be the following:
            `/TestFolder/TestFile.txt`

        ### Returns
        ----
        dict:
            A workbookSessionInfo resource object.
        """
        if group_drive:
            path = f"/groups/{group_drive}"
        else:
            path = "/me"
        if item_id:
            content = self.graph_session.make_request(
                method="post",
                endpoint=f"{path}/drive/items/{item_id}/workbook/createSession",
            )
        elif item_path:
            content = self.graph_session.make_request(
                method="post",
                endpoint=f"{path}/drive/root:/{item_path}:/workbook/createSession",
            )

        return content

    def refresh_session(
        self,
        session_id: str,
        group_drive: str = None,
        item_id: str = None,
        item_path: str = None,
    ) -> dict:
        """Used to Refresh an existing Workbook Session using the Item ID or
        Item Path.

        ### Parameters
        ----
        session_id : str
            Workbook session Id to be refreshed

        item_id : str (optional, Default=None)
            The Drive Item Resource ID.

        item_path : str (optional, Default=None)
            The Item Path. An Example would be the following:
            `/TestFolder/TestFile.txt`

        ### Returns
        ----
        dict:
            A response object, 204 for a success.
        """
        if group_drive:
            path = f"/groups/{group_drive}"
        else:
            path = "/me"
        if item_id:
            content = self.graph_session.make_request(
                method="post",
                endpoint=f"{path}/drive/items/{item_id}/workbook/refreshSession",
                additional_headers={"workbook-session-id": session_id},
                expect_no_response=True,
            )
        elif item_path:
            content = self.graph_session.make_request(
                method="post",
                endpoint=f"{path}/drive/root:/{item_path}:/workbook/refreshSession",
                additional_headers={"workbook-session-id": session_id},
                expect_no_response=True,
            )

        return content

    def close_session(
        self,
        session_id: str,
        group_drive: str = None,
        item_id: str = None,
        item_path: str = None,
    ) -> dict:
        """Used to close an existing Workbook Session using the Item ID or
        Item Path.

        ### Parameters
        ----
        session_id : str
            Workbook session Id to be closed.

        item_id : str (optional, Default=None)
            The Drive Item Resource ID.

        item_path : str (optional, Default=None)
            The Item Path. An Example would be the following:
            `/TestFolder/TestFile.txt`

        ### Returns
        ----
        dict:
            A response object, 204 for a success.
        """
        if group_drive:
            path = f"/groups/{group_drive}"
        else:
            path = "/me"
        if item_id:
            content = self.graph_session.make_request(
                method="post",
                endpoint=f"{path}/drive/items/{item_id}/workbook/closeSession",
                additional_headers={"workbook-session-id": session_id},
                expect_no_response=True,
            )
        elif item_path:
            content = self.graph_session.make_request(
                method="post",
                endpoint=f"{path}/drive/root:/{item_path}:/workbook/closeSession",
                additional_headers={"workbook-session-id": session_id},
                expect_no_response=True,
            )

        return content

    def list_tables(
        self,
        group_drive: str = None,
        item_id: str = None,
        item_path: str = None,
    ) -> dict:
        """Retrieves a list of table objects using the Item ID or
        Item Path.

        ### Parameters
        ----
        item_id : str (optional, Default=None)
            The Drive Item Resource ID.

        item_path : str (optional, Default=None)
            The Item Path. An Example would be the following:
            `/TestFolder/TestFile.txt`

        ### Returns
        ----
        dict:
            A collection of Table Object resources.
        """
        if group_drive:
            path = f"/groups/{group_drive}"
        else:
            path = "/me"
        if item_id:
            content = self.graph_session.make_request(
                method="get", endpoint=f"{path}/drive/items/{item_id}/workbook/tables"
            )
        elif item_path:
            content = self.graph_session.make_request(
                method="get",
                endpoint=f"{path}/drive/root:/{item_path}:/workbook/tables",
            )

        return content

    def list_worksheets(
        self,
        group_drive: str = None,
        item_id: str = None,
        item_path: str = None,
    ) -> dict:
        """Retrieves a list of worksheet objects using the Item ID or
        Item Path.

        ### Parameters
        ----
        item_id : str (optional, Default=None)
            The Drive Item Resource ID.

        item_path : str (optional, Default=None)
            The Item Path. An Example would be the following:
            `/TestFolder/TestFile.txt`

        ### Returns
        ----
        dict:
            A collection of Worksheet resource objects.
        """
        if group_drive:
            path = f"/groups/{group_drive}"
        else:
            path = "/me"
        if item_id:
            content = self.graph_session.make_request(
                method="get",
                endpoint=f"{path}/drive/items/{item_id}/workbook/worksheets",
            )
        elif item_path:
            content = self.graph_session.make_request(
                method="get",
                endpoint=f"{path}/drive/root:/{item_path}:/workbook/worksheets",
            )

        return content

    def list_names(
        self,
        group_drive: str = None,
        item_id: str = None,
        item_path: str = None,
    ) -> dict:
        """Retrieves a list of named objects using the Item ID or
        Item Path.

        ### Parameters
        ----
        item_id : str (optional, Default=None)
            The Drive Item Resource ID.

        item_path : str (optional, Default=None)
            The Item Path. An Example would be the following:
            `/TestFolder/TestFile.txt`

        ### Returns
        ----
        dict:
            A collection of Named resource objects.
        """
        if group_drive:
            path = f"/groups/{group_drive}"
        else:
            path = "/me"
        if item_id:
            content = self.graph_session.make_request(
                method="get", endpoint=f"{path}/drive/items/{item_id}/workbook/names"
            )
        elif item_path:
            content = self.graph_session.make_request(
                method="get", endpoint=f"{path}/drive/root:/{item_path}:/workbook/names"
            )

        return content

    def add_row(
        self,
        group_drive: str = None,
        workbook_id: str = None,
        workbook_path: str = None,
        worksheet_id: str = None,
        worksheet_path: str = None,
        table_id: str = None,
        table_path: str = None,
        session_id: str = None,
        json_data: dict = None,
    ) -> dict:
        """Retrieves a list of named objects using the Item ID or
        Item Path.

        ### Parameters
        ----
        workbook_id : str (optional, Default=None)
            The Drive Item Resource ID for the workbook.

        workbook_path : str (optional, Default=None)
            The Item Path for the workbook. An Example would be the following:
            `/TestFolder/TestFile.txt`

        ### Returns
        ----
        dict:
            A collection of Named resource objects.
        """
        header_payload = {
            "Content-Type": "application/json",
            # "Workbook-Session-Id": session_id,
        }
        if group_drive:
            path = f"/groups/{group_drive}"
        else:
            path = "/me"
        if workbook_id and table_id:
            content = self.graph_session.make_request(
                method="post",
                # endpoint=f"{path}/drive/items/{workbook_id}/workbook/tables/{table_id}/rows",
                # https://graph.microsoft.com/v1.0/groups/8c653932-c7aa-44c2-af48-26692d17cc2a/drive/items/01E2ZXUSLHIGJIXN6Q2NC2S73MSSQ2GITD/workbook/tables/july_table/rows
                endpoint=f"{path}/drive/items/{workbook_id}/workbook/tables/{table_id}/rows",
                additional_headers=header_payload,
                json=json_data,
            )
        elif workbook_path and table_path and worksheet_path:
            content = self.graph_session.make_request(
                method="post",
                # endpoint=f"{path}/drive/root:/{workbook_path}:/workbook/tables/{table_path}/rows",
                endpoint=f"{path}/drive/items/{workbook_path}/workbook/worksheets/{worksheet_path}/tables/{table_path}/rows",
                additional_headers=header_payload,
                data=json_data,
            )
        else:
            print("Add functionality to accommodate mixing paths & id's in endpoint!")
            raise NotImplementedError
        return content

    def get_operation_result(self, operation_id: str) -> dict:
        """This function is the last in a series of steps to create a
        `workbookTableRow` resource asynchronously.

        ### Parameters
        ----
        operation_id : str
            The operationId provided in the `workbook_operation` response
            returned in the preceding `get_workbook_operation` request.

        ### Returns
        ----
        dict:
            A workbookTableRow object.
        """

        content = self.graph_session.make_request(
            method="get",
            endpoint=f"/driveItem/workbook/tableRowOperationResult(key={operation_id})",
        )

        return content
