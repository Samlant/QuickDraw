import base64
from pathlib import Path
from typing import Protocol
import win32com.client as win32

from requests import HTTPError

class Email(Protocol):
    name: str
    ids: list[str]
    to: list[str]
    cc: list[str]
    subject: str
    body: str
    attachments: list[Path]

class OutlookManager:
    def __init__(self, service, emails: list[Email]):
        self.service = service
        self.emails: list[Email] = emails
        self.attachments = None

    def send_emails(self, emails: list[Email], auto_send: bool) -> dict[str, str]:
        self.attachments = self._make_attachments(emails[0].attachments)
        results: dict[str, dict[str, str | bool]] = {}
        for email in emails:
            msg_json = self._email_to_json(email=email, auto_send=auto_send)
            try:
                if auto_send:
                    self.service.send_my_mail(message=msg_json)
                else:
                    self.service.create_my_message(message=msg_json)
                    outlook = win32.Dispatch('outlook.application')
                    drafts = outlook.GetNamespace("MAPI").GetDefaultFolder(16)
                    mail = drafts.Items.GetLast()
                    mail.Display(False)
            except HTTPError as e:
                print(f"Error upon sending email for the {email.name} markets.")
                print(f"code: {e.code}\nmessage: {e.message}\nError: {e.error}")
                results[email.name] = {"ids": email.ids, "success": False}
            else:
                results[email.name] = {"ids": email.ids, "success": True}
        return results
                
    def _make_attachments(
        self, _attachments: list[Path]
    ) -> list[dict[str, str]]:
        attachment_payload = []
        for _a in _attachments:
            content = base64.b64encode(open(str(_a), "rb").read())
            content = content.decode()
            file = {
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": _a.name,
                "contentBytes": content,
            }
            content_type = self.__assign_content_type(path=_a)
            if content_type:
                file["contentType"] = content_type
            attachment_payload.append(file)
        return attachment_payload

    def __assign_content_type(self, path: Path) -> str | None:
        suffix = path.suffix
        if suffix == ".pdf":
            return "application/pdf"
        if suffix == ".doc" or suffix == ".docx":
            return "application/msword"
        if suffix == ".zip":
            return "application/zip"
        if suffix in [".png", ".gif", ".jpeg", ".bmp", ".png", ".tiff"]:
            return f"image/{suffix[1:]}"
        print(f"Unsupported file format detected. File: {path}")
        print("Not specifying a ContentType because of this...")
        return None

    def _email_to_json(
        self, 
        email: Email,
        auto_send: bool,
    ) -> dict[str, str | dict[str, str] | list[dict[str, dict[str, str]]]]:
        _json = {
                "subject": email.subject,
                "importance": "normal",
                "body": {"contentType": "HTML", "content": email.body},
                "attachments": self.attachments,
                "toRecipients": self.__make_addresses(email.to),
            }
        if email.cc:
            _json["ccRecipients"] = self.__make_addresses(email.cc)
        if auto_send:
            json = {"message": _json}
        else:
            json = _json
        return json

    def __make_addresses(
        self, _addresses: list[str]
    ) -> list[dict[str, dict[str, str]]]:
        address_payload = []
        for _a in _addresses:
            _b: dict[str, dict[str, str]] = {"emailAddress": {"address": _a}}
            address_payload.append(_b)
        return address_payload
