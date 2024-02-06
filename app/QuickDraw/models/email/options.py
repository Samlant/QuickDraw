

class EmailOptions:
    def __init__(self, settings: dict[str, str]):
        self.use_default_cc_addresses = settings.pop("use_default_cc_addresses")
        if settings["signature_image"] != "":
            self.use_custom_sig_img = True
        else:
            self.use_custom_sig_img = False