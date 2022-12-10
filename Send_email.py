class Send_email:
    sender_address = 'blank'
    import win32com.client as win32
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'To address'
    mail.Subject = (last_name, + ' ' + first_name + ' | ' + boat_year + ' ' + boat_make + ' ' + boat_length + ' | ' + New Quote Submission')
    mail.Body = 'Message body'
    mail.HTMLBody = '<h2>Message_set_as_variable</h2>' #this field is optional
    attachment  = "Path-to-attachment" # To attach a file to the email (optional):
    mail.Attachments.Add(attachment)

    def send_it(self):
        mail.Send()
        return True

class Seawave(Send_email):
    send_to_seawave = Seawave
    mail.to = 'boatprograms@one80intermediaries.com'
    mail.HTMLBody = '<h2><p>Hey BoatPrograms,</p><p>Please see the attached for a new quote submission for the Seawave market.  Thanks in advance for your consideration.</p></h2>
    
    
