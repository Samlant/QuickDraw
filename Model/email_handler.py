import win32com.client as win32


class EmailHandler:
    """ This class is responsible for interfacing with Outlook in creating email envelopes to send.  Once called,  data is gathered from the Presenter and applied to an email envelope,  then once complete,  it is sent out.
    NOTE: This will be looped through for each envelope every button press.
    """
    self.application = 'outlook.application'

    def __init__(self) -> None:
        self.outlook = win32.Dispatch(self.application)
        self.envelope = self.outlook.CreateItem(0)
        
    def create_envelope(self): #Re-EXAMINE and investigate
        """ This creates the model,  which secures, validates, stores, and ultimately allocates data into an email object for sending away.
        """

    def assign_recipient(self, recipient: str) -> None:
        self.envelope.To = recipient

    def assign_CC(self, cc_addresses: str) -> None:
        self.envelope.CC = cc_addresses

    def assign_subject(self, subject: str) - None:
        self.envelope.Subject = subject

    def assign_body_text(self, body: str) -> None:
        self.envelope.Body = body

    def assignAttachments(self, attachments: str) -> None:
        self.envelope.Attachments.Add(attachments)

    def send_envelope(self) -> None:
        try
            self.envelope.Send()
        except 
            error_msg = f"Failed to send envelope to {self.envelope.To}."
            raise Exception(error_msg)
        else:
            print('Sent message successfully.')
        finally:
            print('Moving on to the next envelope...')
        
