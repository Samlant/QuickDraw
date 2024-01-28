from dataclasses import dataclass


@dataclass
class EmailFormat:
    greeting: str = "font-size:14px;color:#1F3864;"
    body: str = "font-size:14px;color:#1F3864;"
    salutation: str = (
        "margin:0in;font-size:14px;font-family:Calibri,sans-serif;color:#1F3864;"
    )
    username: str = (
        "margin:0in;font-size:14px;font-family:Calibri,sans-serif;color:#1F3864;"
    )
    sig_txt = "margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;"
    sig_img = "margin:0in;"
