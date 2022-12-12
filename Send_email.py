#Code to define GUI Launcher
#above code placeholder here

#Code to launch GUI Launcher
#above code placeholder here

#Code to save exported values upon clicking submit button to variables
#above code placeholder here

#Defining Sending email PARENT class,  containing the mail.Send() function callclass Send_email:
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
                    
#Code for child classes for each carrier
class Seawave(Send_email):
    if seawave_check = True :
      send_to_seawave = Seawave
      mail.to = 'boatprograms@one80intermediaries.com'
      mail.HTMLBody = 
      '<p><span style="color: #000080;">Hey BoatPrograms,</span></p>
      <p>&nbsp;</p>
      <p><span style="color: #000080;">Please see the attached for a new quote submission for the SeaWave market. Thanks in advance for your consideration.</span></p>
      <p>&nbsp;</p>
#Insert my below signature into the parent email HTML body,  unless there's a specific command to insert specific signature from Outlook (mail.InsertSig for example?)
      <p><span style="color: #000080;">With Pleasure,</span></p>
      <p><span style="color: #000080;"><strong>Samuel Alexander Lanteigne</strong></span></p>
      <p><span style="color: #000080;">NOVAMAR INSURANCE GROUP</span></p>
      <p><span style="color: #000080;">Main :&nbsp;(800)-823-2798</span></p>
      <p><span style="color: #000080;">Office : (941)-444-5099</span></p>
      <p><span style="color: #000080;">Fax : (941)-328-3598</span></p>
      <p><span style="color: #000080;">1549 Ringling Blvd., Suite 101</span></p>
      <p><span style="color: #000080;">Sarasota, FL 34236&nbsp;</span></p>
      <p><span style="color: #000080;"><a style="color: #000080;" href="http://www.novamarinsurance.com/">www.novamarinsurance.com</a></span></p>
      <p><span style="color: #000080;"><a style="color: #000080;" href="http://www.novamarinsurance.com.mx/">www.novamarinsurance.com.mx</a></span></p>
      <p><span style="color: #000080;">Established in 1987 with offices in: Seattle | Newport Beach | San Diego | Sarasota | Jacksonville | Puerto Vallarta | Cancun | San Miguel de Allende&nbsp;</span></p>
      <p><span style="color: #000080;">Please be advised that coverage is not bound, renewed, amended or in force unless confirmed in writing by a Novamar Insurance Group agent or by the represented company.</span></p>'
    else :
      pass
#The above code to be debugged first,  then expanded on to include other carriers within separate child classes.
                    
    
