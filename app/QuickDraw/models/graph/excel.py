from typing import Protocol
from datetime import datetime
from pathlib import Path
import base64

from QuickDraw.helper import open_config
from QuickDraw.presenter.protocols import Submission, Quoteform
from QuickDraw.models.graph.accessories import JsonBuilder


class ExcelManager:

    def __init__(
        self,
        service,
        group_id: str,
        quote_tracker_id: str,
        submission: Submission,
    ):
        self.session_id: str = self._open_session(
            service=service,
            group_drive=group_id,
            item_id=quote_tracker_id,
        )
        self.username: str = self.get_user_initials()
        # this is to add the row...
        # dont forget to implement checking if the row already exists
        # and that the whole process (opening session, getting row data,
        # checking that row data, then adding/updating the row depending on
        # that, THEN closing it---is all implemented fairly simply...)
        json = JsonBuilder(
            submission=submission,
            initials=self.username,
        )
        # send JSON to api request. Dont forget that this is only to
        # add a row, so fix it!

    def _open_session(
        self,
        service,
    ) -> str:
        session_response = service.create_session(
            group_drive=self.group_id,
            item_id=self.quote_tracker_id,
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

    def create_attachments_json(
        self, attachment_paths: list[Path]
    ) -> list[dict[str, str]]:
        output = []
        for path in attachment_paths:
            name = path.name
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

    def __create_address_list(
        self, addresses: list[str]
    ) -> list[dict[str, dict[str, str]]]:
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
