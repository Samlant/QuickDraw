import win32com.client as win32

zipped_tuple = ()
zipped_tuple = ((1, 'Seawave', 'sam@novamar.net', 'html_message_here'), (1, 'Kemah Marine', 'sam@novamar.net', 'html_message_here'))

def tuple_send():
    for submit_check, carrier, carrier_address, html_message in zipped_tuple:
        if submit_check == 1:
            print(submit_check, carrier, carrier_address, html_message)
            outlook = win32.Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
            mail.To = carrier_address
#            mail.CC = CC_recipients
            mail.Subject = (f"this is a test from my GUI-launcher script from my work laptop for {carrier}.")
            mail.HTMLBody = '''<html>
            <head>
            <title>Title</title>
            </head>
            <body>
            <p>This is my first paragraph.</p>
            <p>This is my secod paragraph.</p>
            </body>
            </html>
            '''
            mail.Send()
        else:
            print('no thanks~!')
        
 #           print('No') attachment = "Path-to-attachment"
        # To attach a file to the email (optional):
#        mail.Attachments.Add(attachment)
        
            #include the html message within same python script

tuple_send()
