from QuickDraw.helper import open_config, Carrier

class EmailContent:
    def __init__(self, carrier: Carrier):
        self.carrier = carrier
    
    def get_config_values(self, sig_img: bool = False):
        self._get_body()
        self._get_signature(sig_img)
        
    def _get_body(self):
        # need extra_notes!!
        vars = [
            "greeting",
            "body",
            "outro",
            "salutation",
            ]
        conf = open_config()
        try:
            for var in vars:
                setattr(self, var, conf.get(self.carrier.name, var).value)
        except TypeError as te:
            print(f"Check template settings to ensure all required parts have something assigned to them!\nparts needed: {vars}\n{e}")
    
    def _get_signature(self, sig_img: bool = False)
        vars = [
            "username"
            "logo_img",
            "office_phone",
            "office_fax",
            "office_street",
            "office_city_st_zip",
            ]
        if sig_img:
            vars.append("sig_img_url")
            
        conf = open_config()
        try:
            for var in vars:
                setattr(self, var, config.get("Email", var).value)
        except TypeError as te:
            print(f"Check email settings to ensure all required parts have something assigned to them!\nparts needed: {vars}\n{e}")
            
    def get_attachments(self):
        pass
        
    def get_subject_line(self, submission: Submission):
        pass
        
    def get_recipients(self):
        pass
