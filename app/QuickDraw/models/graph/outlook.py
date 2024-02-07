import base64
from pathlib import Path
from typing import Protocol

class Email(Protocol):
    to: list[str]
    cc: list[str]
    subject: str
    body: str
    attachments: list[Path]

class OutlookManager:
    def __init__(self, emails: list[Email]):
        self.emails: list[Email] = emails

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

    def email_to_json(
        self, email: Email
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

