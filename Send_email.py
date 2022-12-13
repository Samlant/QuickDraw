#Code to define GUI Launcher
#above code placeholder here

#Code to launch GUI Launcher
#above code placeholder here

#Code to save exported values upon clicking submit button to variables
#above code placeholder here

#Defining Sending email PARENT class,  containing the mail.send() call under the function send_it(). can condense once debugged.
class Send_email:
    def __init__(self, fname, lname, byear, bmake, blength, carrier, recipient, cc_address, html_message)
    self.fname = fname
    self.lname = lname
    self.byear = byear
    self.bmake = bmake
    self.blength = blength
    self.carrier = carrier
    self.recipient = recipient
    self.cc_address = cc_address
    
    import win32com.client as win32
    
    def create_msg(self):
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = self.recipient
        if self.cc_address != "null":
            mail.CC = self.cc_address
        else:
            pass
        mail.Subject = (lname + ', ' + fname + ' | ' + byear + ' ' + bmake + ' ' + blength + ' | ' + 'New Quote Submission for ' + carrier)
        mail.HTMLBody = html_message #body and signature in HTML
        #attachment  = "Path-to-attachment" #need to insert from gui launcher
        #mail.Attachments.Add(attachment) 

    def send_it(self):
        try:
          mail.Send()
        except:
            print(cannot send email)
        else:
          print("Email sent")
          return True
                    
#code to create instances
if seawave_check == True:
    recipient = 'boatprograms@one80intermediaries.com'
    carrier = seawave
    html_message = 'tba'
    seawave = Send_email(fname, lname, byear, bmake, blength, carrier, recipient, cc_address, html_message)
    seawave.send_it()
else:
    pass

if primetime_check == True
    recipient = 'boatprograms@one80intermediaries.com'
    carrier = Prime Time Insurance'
    html_message = 'tba'
    primetime = Send_email(fname, lname, byear, bmake, blength, carrier, recipient, cc_address, html_message)
    primetime.send_it()
else:
    pass
    
if americanmodern_check == True:
    recipient = 'boatbrokerage@one80intermediaries.com'
    carrier = 'American Modern'
    html_message = 'tba'
    americanmodern = Send_email(fname, lname, byear, bmake, blength, carrier, recipient, cc_address, html_message)
    americanmodern.send_it()
else:
    pass
    
if kemah_check == True:
    recipient = 'tom.carroll@kemahcapital.com'
    carrier = 'Kemah Marine'
    html_message = 'tba'
    kemah = Send_email(fname, lname, byear, bmake, blength, carrier, recipient, cc_address, html_message)
    kemah.send_it()
else:
    pass
    
if concept_check == True:
    recipient = 'quote.team@special-risks.co.uk'
    carrier = 'Concept'
    html_message = 'tba'
    concept = Send_email(fname, lname, byear, bmake, blength, carrier, recipient, cc_address, html_message)
    concept.send_it()
else:
    pass
    
if yachtinsure_check == True:
    recipient = 'quotes@yachtinsure.uk.com'
    carrier = 'Yachtinsure'
    html_message = 'tba'
    yachtinsure = Send_email(fname, lname, byear, bmake, blength, carrier, recipient, cc_address, html_message)
    yachtinsure.send_it()
else:
    pass
    
if intact_check == True:
    recipient = 'yucusa@intactinsurance.com'
    carrier = 'Intact Insurance'
    html_message = 'tba'
    intact = Send_email(fname, lname, byear, bmake, blength, carrier, recipient, cc_address, html_message)
    intact.send_it()
else:
    pass

if travelers_check == True:
    recipient = 'ytquote@travelers.com'
    html_message = 'tba'
    travelers = Send_email(fname, lname, byear, bmake, blength, carrier, recipient, cc_address, html_message)
    travelers.send_it()
else:
    pass
    
if newhampshire_check == True:
    recipient = 'boatprograms@one80intermediaries.com'
    carrier = 'New Hampshire'
    html_message = 'tba'
    newhampshire = Send_email(fname, lname, byear, bmake, blength, carrier, recipient, cc_address, html_message)
    newhampshire.send_it()
else:
    pass
    
#EoF
                    
    
