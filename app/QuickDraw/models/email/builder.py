from QuickDraw.helper import open_config
from QuickDraw.models.email.content import EmailContent
from QuickDraw.models.email.job import EmailJob
from QuickDraw.models.email.options import EmailOptions
from QuickDraw.models.email.format import EmailFormat


class EmailBuilder:
    def __init__(self, carrier: Carrier):
        self.content = EmailContent(carrier)
        self.format = EmailFormat()
        self.job = EmailJob()
        self.options = EmailOptions()
    
    def make_body(self)
        self.content.get_body_vars()
        self.content.get_signature_vars(self.options.use_sig_img)
    
    
        
    
