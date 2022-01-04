# import smtplib
# print.configure(text='Logging in to account...')
# sender='haburohantesting@gmail.com'
# receiver='haburohan@gmail.com'
# password='rohantestemail@2021'
# msg="this is a test mail."
# server=smtplib.SMTP('smtp.gmail.com',587)
# server.starttls()
# server.login(sender,password)
# print.configure(text='Logged in')
# server.sendmail(sender,receiver,msg)
# print.configure(text='Email sent.')
# server.quit()


# import smtplib
# from email.message import EmailMessage

# msg = EmailMessage()
# msg['Subject'] = 'Sample invitation'
# msg['From'] = 'haburohantesting@gmail.com'
# msg['To'] = 'haburohan@gmail.com'
# msg.set_content("test email from attahcment email.")

# with open('Attendance/Attendance_2021-12-06_21-18-26.csv', 'rb') as file:
#     data = file.read()
#     print('binary data')
#     print(data)
#     filename = file.name
#     print(filename)
#     msg.add_attachment(data, maintype='application',
#                        subtype='csv', filename=filename)

# server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
# server.login('haburohantesting@gmail.com', 'rohantestemail@2021')
# server.send_message(msg)
# server.quit()


# from tkinter import *
# from PIL import ImageTk,Image
# from tkinter import filedialog

# window=Tk()
# window.title('Sample app')

# window.filename=filedialog.askopenfile(initialdir='A:\\mitwpu\\ty\\tri 2\\Internship\\Canspirit\\face_recognition\\Face-recognition-based-attendance-system-master\\Face-Recognition-Based-Attendance-System-master\\Attendance',title='Select a file')

# label=Label(window,text=window.filename).pack()
# img=ImageTk.PhotoImage(Image.open(window.filename))

# window.mainloop()




import os

f=[]
print(type(os.listdir('Attendance/')[-1]))