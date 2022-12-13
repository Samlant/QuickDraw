#Code to define GUI Launcher
#above code placeholder here

#Code to launch GUI Launcher
#above code placeholder here

#Code to save exported values upon clicking submit button to variables
#above code placeholder here

#Defining Sending email PARENT class,  containing the mail.Send() function call
class send_it(submission_address, last_name, first_name, year_of_boat, boat_make, boat_length, carrier_to_submit_to):
    to_address = submission_address
    last_nm = last_name
    first_nm = first_name
    year = year_of_boat
    boat = boat_make
    length = boat_length
    carrier = carrier_to_submit_to
    
    import win32com.client as win32
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'sam@novamar.net'
    mail.Subject = (last_nm + ', ' + first_nm + ' | ' + year + ' ' + boat + ' ' + length + ' | New Quote Submission for ' + carrier )
    mail.Body = 'This is the plain text body message'
    mail.HTMLBody = '<h2>This is the HTML body <strong>that should work...</strong>else I am a <i>COMPLETE FAILURE</i> haha</h2>' #this field is optional
    mail.Send()
#attachment  = "Path-to-attachment"  To attach a file to the email (optional):
#mail.Attachments.Add(attachment)

#Code for child classes for each carrier
class Seawave_Insurance(send_it):
    if seawave_check = True :
        carrier = Seawave Insurance
        send_it('sam@novamar.net', 'LANTEIGNE', 'Samuel', '2020', 'Regal', '28ft', 'Concept Special Risks')
    else
      pass
#The above code to be debugged first,  then expanded on to include other carriers within separate child classes.

