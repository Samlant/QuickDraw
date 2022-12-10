import win32com.client as win32
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'To address'
mail.Subject = 'Message subject'
mail.Body = 'Message body'
mail.HTMLBody = '<h2>Message_set_as_variable</h2>' #this field is optional

# To attach a file to the email (optional):
attachment  = "Path-to-attachment"
mail.Attachments.Add(attachment)

mail.Send()
