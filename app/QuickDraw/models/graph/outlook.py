import base64
from pathlib import Path
from typing import Protocol
import win32com.client as win32

class Email(Protocol):
    to: list[str]
    cc: list[str]
    subject: str
    body: str
    attachments: list[Path]

class OutlookManager:
    def __init__(self, service, emails: list[Email]):
        self.service = service
        self.emails: list[Email] = emails

    def send_emails(self, emails: list[Email], send: bool) -> dict[str, str]:
        for email in emails:
            # format attachments
            self.attachments = self._make_attachments(email.attachments)
            # format json request
            msg_json = self._email_to_json(email=email, send=send)
            # send or view API request
            if send:
                self.service.send_my_mail(message=msg_json)
            else:
                self.service.create_my_message(message=msg_json)
                outlook = win32.Dispatch('outlook.application')
                # Decide whether to create draft email using Graph API THEN grab 
                # the local draft email using its ID ---or--- by using the win32com 
                # interface instead, similar to how prog was originally written...
                # mail = outlook.CreateItem(0)
                # mail.To = email.to
                # mail.CC = email.cc
                # mail.Subject = email.subject
                # mail.HtmlBody = email.body
                # mail.Attachment = email.attachments
                drafts = outlook.GetNamespace("MAPI").GetDefaultFolder(16)
                mail = drafts.Items.GetLast()
                ################################
                # Once we have the draft email item...
                ###############################
                mail.Display(False)

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
        send: bool,
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
        if send:
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
