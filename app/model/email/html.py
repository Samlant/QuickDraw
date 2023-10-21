def organize_inputs(email_handler, carrier_section) -> tuple[dict, dict, str]:
    greeting = carrier_section.get("greeting").value
    body = carrier_section.get("body").value
    outro = carrier_section.get("outro").value
    salutation = carrier_section.get("salutation").value
    sig_img = email_handler.img_sig_url
    styles: dict[str, str] = {
        "greeting": email_handler.greeting_style,
        "body": email_handler.body_style,
        "salutation": email_handler.salutation_style,
        # "signature": email_handler.signature_style,
        "username": email_handler.username_style,
    }
    wordings: dict[str, str] = {
        "greeting": greeting,
        "body": body,
        "outro": outro,
        "extra notes": email_handler.extra_notes,
        "salutation": salutation,
        "username": email_handler.username,
    }
    return styles, wordings, sig_img


def make_body(
    styles: dict[str, str],
    wordings: dict[str, str],
    signature: str,
) -> str:
    style_greeting = styles["greeting"]
    style_body = styles["body"]
    style_salutation = styles["salutation"]
    style_username = styles["username"]
    # style_signature = styles["signature"] # not implemented yet
    greeting = wordings["greeting"]
    body = wordings["body"]
    outro = wordings["outro"]
    extra_notes = wordings["extra notes"]
    salutation = wordings["salutation"]
    username = wordings["username"]
    html_msg = f"""
        <html>
            <head>
                <title>New Quote Submission</title>
                <meta http-equiv='Content-Type' content='text/html; charset=windows-1252'>
                <meta name='ProgId' content='Word.Document'>
                <meta name='Generator' content='Microsoft Word 15'>
                <meta name='Originator' content='Microsoft Word 15'>
            </head>
            <body>
                <p style={style_greeting}>{greeting}</p>
                <p style={style_body}>{body}</p> 
                <p style={style_body}>{extra_notes}</p>
                <p style={style_body}>{outro}</p>
            </body>
            <footer>
            <p style={style_salutation}>{salutation}</p>
            <p style={style_username}>{username}</p>
            {signature}
            </footer>
        </html>
        """
    return html_msg


def make_signature(sig_img: str, signature_settings: dict[str, str]) -> str:
    logo_img = "https://i.postimg.cc/yWCHTYjJ/novamar.png"
    office_phone = signature_settings["office_phone"]
    office_street = signature_settings["office_street"]
    office_city_st_zip = signature_settings["office_city_st_zip"]
    signature = f"""
        <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>NOVAMAR INSURANCE GROUP</p>
        <img src='{logo_img}'>
        <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Main:(800)-823-2798</p>
        <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Office :{office_phone}</p>
        <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Fax:(941)-328-3598</p><br>
        <p style='margin:0in;color:#0563C1;text-decoration:underline;text-underline:single;font-size:12px;font-family:Georgia Pro,serif;'>{office_street}</p>
        <p style='margin:0in;color:#0563C1;text-decoration:underline;text-underline:single;font-size:12px;font-family:Georgia Pro,serif;'>{office_city_st_zip}</p><br>
        <p style='margin:0in;color:#1F3864;font-size:10.0pt;font-family:Georgia Pro,serif;color:blue;'><a href='http://www.novamarinsurance.com/' target='_blank'>www.novamarinsurance.com</a></p>
        <p style='margin:0in;color:#1F3864;font-size:10.0pt;font-family:Georgia Pro,serif;color:blue;'><a href='http://www.novamarinsurance.com.mx/' target='_blank'>www.novamarinsurance.com.mx</a></p>

        <p style='margin:0in;'><a href='https://www.facebook.com/NovamarInsurance' target='_blank'><img width=24 height=24 src='https://cdn1.iconfinder.com/data/icons/social-media-2285/512/Colored_Facebook3_svg-512.png'></a>  <a href='https://www.instagram.com/novamar_insurance/' target='_blank'><img width=24 height=24 src='https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Instagram_colored_svg_1-512.png' style='display:block'></a>  <a href='https://twitter.com/NovamarIns' target='_blank'><img width=24 height=24 src='https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Twitter3_colored_svg-512.png' style='display:block'></a>  <a href='https://www.linkedin.com/company/novamar-insurance-group-inc' target='_blank'><img width=24 height=24 src='https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Linkedin_unofficial_colored_svg-512.png' style='display:block'></a></p>
        <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Established in 1987 with offices in: Seattle | Newport Beach | San Diego | Sarasota | Jacksonville | Puerto Vallarta | Cancun | San Miguel de Allende</p>
        <p style='margin:0in;font-size:12px;font-family:Georgia Pro,serif;color:#1F3864;'>Please be advised that coverage is not bound, renewed, amended or in force unless confirmed in writing by a Novamar Insurance Group agent or by the represented company.</p>
        """
    if sig_img != "":
        signature = f"<img src='{sig_img}'>" + signature
    return signature


def build_HTML_message(
    email_handler,
    carrier_section,
    signature_settings,
) -> str:
    styles, wordings, sig_img = organize_inputs(
        email_handler,
        carrier_section,
    )
    signature = make_signature(
        sig_img,
        signature_settings,
    )
    html_msg = make_body(
        styles,
        wordings,
        signature,
    )
    return html_msg
