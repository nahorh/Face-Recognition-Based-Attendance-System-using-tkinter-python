import shutil
import tkinter as tk
import os
from tkinter import messagebox,filedialog
import numpy as np
from tkinter import font
from tkinter import ttk
from tkinter import *
import admintasks
import pandas as pd
from PIL import Image
from email.message import EmailMessage
import smtplib
import cv2
import csv
import time
import datetime
import shutil

def main_function():
    def goBack():
        signinWindow.destroy()

    def disableButton():
        pass

    root_path=os.getcwd()

    signinWindow = Tk()
    signinWindow.title("Face Recognition Attendance System")

    # signinWindow.overrideredirect(True)
    # signinWindow.attributes('-topmost',True)

    # style=ttk.Style()
    # style.configure('TButton',font=('times',15,'bold'),borderwidth='4')
    # style.map('TButton',foreground=[('active','!disabled','black')],background=[('active','gray')])

    signinWindow.configure(background='white')

    signinWindow.protocol('WM_DELETE_WINDOW',disableButton)

    window_width = 800
    window_height = 400

    x_Left = int(signinWindow.winfo_screenwidth()/2 - window_width/2)
    y_Top = int(signinWindow.winfo_screenheight()/2 - window_height/2)

    signinWindow.geometry(f'{window_width}x{window_height}+{x_Left}+{y_Top}')

    signinWindow.resizable(False,False)

    # giving the heading
    message = Label(signinWindow, text="Face-Recognition-Based-Attendance-System", bg="white",fg="black", width=100, height=2, font=('times', 30, 'bold'))
    message.pack(side='top',anchor='center')

    def verifyCred():
        uname=unameEntry.get()
        unameEntry.delete(0,END)
        passwd=passwdEntry.get()
        passwdEntry.delete(0,END)
        print(uname,passwd)
        if uname=='admin' and passwd=='admin':
            # render the admintask.py file
            def getImagesAndLabels(path):
                # get the path of all the files in the folder
                imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
                # create empty face list
                faces = []
                # create empty ID list
                Ids = []
                # now looping through all the image paths and loading the Ids and the images
                for imagePath in imagePaths:
                    # loading the image and converting it to gray scale
                    pilImage = Image.open(imagePath).convert('L')
                    # Now we are converting the PIL image into numpy array
                    imageNp = np.array(pilImage, 'uint8')
                    # getting the Id from the image
                    Id = int(os.path.split(imagePath)[-1].split(".")[1])
                    # extract the face from the training image sample
                    faces.append(imageNp)
                    Ids.append(Id)
                return faces, Ids

            # left frame button functions
            def send_email():
                adminTasksWindow.attributes('-topmost',True)
                print('Send email invoked')
                filetype=(('csv files','*.csv'),('All files','*.*'))
                # messagebox.showinfo('abc','After clicking on OK, a file dialogbox will open. Kindly select the file you want to email. The emails for present students and their parents will be extracted and attendance sheet will be sent as an attachment.')
                proceed=messagebox.askokcancel('Send email','After clicking on OK, a file dialogbox will open. Kindly select the file you want to email. The emails for present students and their parents will be extracted and attendance sheet will be sent as an attachment.')
                if proceed:
                    fileDialog=filedialog.askopenfilename(initialdir=f'{root_path}/Attendance',filetypes=filetype)
                #     print(fileDialog)
                #     # print(file)
                    file=pd.read_csv(fileDialog)
                    file=pd.DataFrame(file)
                    stuEmails=file['StudentEmail']
                    for stuEmail in stuEmails:
                        file=pd.read_csv(fileDialog)
                        file=pd.DataFrame(file)
                        stuName=file.loc[file['StudentEmail']==stuEmail]['Name'].values[0]
                        stuName=str(stuName).replace('[\'','').replace('\']','')
                        parEmail=file.loc[file['StudentEmail']==stuEmail]['ParentEmail'].values[0]
                        # print(stuName)
                        # print(stuEmail)
                        # print(parEmail)
                        msg1=EmailMessage()
                        msg1['Subject']='Attendance for the day.'
                        msg1['From']='Attendance system.'
                        msg1['To']=str(stuEmail).replace('[\'','').replace('\']','')
                        msg1.set_content(f'''
                            Dear {stuName},
                            Please find the below attached csv file of attendees.
                            You are marked present!
                            ''')
                        with open(fileDialog,'rb') as file:
                            data=file.read()
                        nameOfFile=file.name
                        msg1.add_attachment(data,maintype='application',subtype='csv',filename=nameOfFile)

                        msg2=EmailMessage()
                        msg2['Subject']='Attendance for the day.'
                        msg2['From']='Attendance system.'
                        msg2['To']=str(parEmail).replace('[\'','').replace('\']','')
                        msg2.set_content(f'''
                            Dear {stuName}'s Parent,
                            Please find the below attached csv file of attendees.
                            Your child is marked present!
                            ''')
                        with open(fileDialog,'rb') as file:
                            data=file.read()
                        nameOfFile=file.name
                        msg2.add_attachment(data,maintype='application',subtype='csv',filename=nameOfFile)

                        try:
                            with open('smtpcred.txt','r') as file:
                                cred=file.read()
                                cred=str(cred)
                                # print(cred)
                            cred=cred.split(',')
                            adminEmail=cred[0]
                            adminEmail=adminEmail.replace(' ','')
                            adminPwd=cred[1]
                            adminPwd=adminPwd.replace(' ','')
                        except:
                            messagebox.showerror('SMTP credentials error','Please check the "smtpcred.txt" file is in the root path of application. Please make sure that {username,password} are included in the file')
                            return
                        try:
                            server=smtplib.SMTP_SSL('smtp.gmail.com',465)
                        except:
                            messagebox.showerror('Server Setup Error','Unable to create instance of SMTP server. Please try again.')
                            return
                        try:
                            server.login(adminEmail,adminPwd)
                        except:
                            messagebox.showerror('Login Error','Unable to login in to email account due to incorrect credentials or bad internet connection.')
                            return
                        try:
                            server.send_message(msg1)
                            server.send_message(msg2)
                        except:
                            messagebox.showerror('Message Not Sent','Unable to send message. Server busy. Please try again.')
                            return
                        server.quit()
                    messagebox.showinfo('Email Sent','Email sent successfully to all present students and their respective parents')

            def TrainImages():
                try:
                    recognizer = cv2.face.LBPHFaceRecognizer_create()
                    print(recognizer)
                    # recognizer=cv2.face.createLBPHFaceRecognizer()
                    harcascadePath = "haarcascade_frontalface_default.xml"
                    # detector = cv2.CascadeClassifier(harcascadePath)
                    faces, Id = getImagesAndLabels("TrainingImage")
                    print(faces)
                    print(Id)
                    recognizer.train(faces, np.array(Id))
                    recognizer.save("Model/model.yml")
                    # res = "Image Trained"
                    # message.configure(text=res)
                    messagebox.showinfo('Training complete','Model trained successfully!')
                except Exception as e:
                    print(e)
                    messagebox.showerror('Recognizer object creation error','Please check that you have "opencv-contrib-python" installed on your system. If not then run this command in cmd "pip install opencv-contrib-python"')

            def viewExcelFile():
                fileType=(('csv files','*.csv'),('all files','*.*'))
                fileDialog=filedialog.askopenfilename(title='Select a csv file to open',initialdir=os.path.join(root_path,'Attendance'),filetypes=fileType)
                if '.csv' in fileDialog:
                    os.startfile(fileDialog)

            def viewLatestAttendanceSheet():
                sheetPath=os.path.join(root_path,'Attendance')
                allFilesList=[]
                for file in os.listdir(sheetPath):
                    allFilesList.append(file)
                file=allFilesList[-1]
                os.startfile(os.path.join(root_path,f'Attendance/{file}'))

            # middle frame button functions
            def initialize():
                def AttendanceDir():
                    if not os.path.exists(os.path.join(root_path,'Attendance')):
                        print(os.path.join(root_path,'Attendance'))
                        os.mkdir(os.path.join(root_path,'Attendance'))

                def StudentDetails():
                    if not os.path.exists(os.path.join(root_path,'StudentDetails')):
                        os.mkdir(os.path.join(root_path,'StudentDetails'))
                    if not os.path.isfile(os.path.join(root_path,'StudentDetails/StudentDetails.csv')):
                        StudentDetailsFilePath=os.path.join(root_path,'StudentDetails\\StudentDetails.csv')
                        # print(StudentDetailsFilePath)
                        with open(StudentDetailsFilePath,'w') as file:
                            row=['Id','Name','StudentEmail','ParentEmail']
                            writer=csv.writer(file)
                            writer.writerow(row)

                def ModelDir():
                    if not os.path.exists(os.path.join(root_path,'Model')):
                        os.mkdir(os.path.join(root_path,'Model'))

                def TrainingImageDir():
                    if not os.path.exists(os.path.join(root_path,'TrainingImage')):
                        os.mkdir(os.path.join(root_path,'TrainingImage'))
                AttendanceDir()
                StudentDetails()
                ModelDir()
                TrainingImageDir()
                messagebox.showinfo('Initializatio Successful','Everything initialized successfully')

            def markAttendance():
                    try:
                        recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
                    except:
                        messagebox.showerror('Recognizer object creation error','Please check that you have "opencv-contrib-python" installed on your system. If not then run this command in cmd "pip install opencv-contrib-python"')
                        return
                    try:
                        recognizer.read("Model/model.yml")
                    except:
                        messagebox.showerror('Model not readable','The trained model is either deleted from the system or unable to access. Please try again by trainig the model again.')
                        return
                    harcascadePath = "haarcascade_frontalface_default.xml"
                    try:
                        faceCascade = cv2.CascadeClassifier(harcascadePath)
                    except:
                        messagebox.showerror('Haar XML file not found','Please check that the "haarcascade_frontalface_default.xml" file is present at the location of exe file')
                        return
                    df = pd.read_csv("StudentDetails/StudentDetails.csv")
                    try:
                        cam = cv2.VideoCapture(0)
                        cam.set(cv2.CAP_PROP_FRAME_WIDTH,640)
                        cam.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
                    except:
                        messagebox.showerror('Camera access error','Please check that camera privacy settings have enabled camera access for applications')
                        return
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    col_names = ['Id', 'Name', 'Date', 'Time','StudentEmail','ParentEmail']
                    attendance = pd.DataFrame(columns=col_names)
                    while True:
                        ret, im = cam.read()
                        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                        try:
                            faces = faceCascade.detectMultiScale(gray, 1.3, 5)
                        except:
                            messagebox.showerror('Haar XML file not found','Please check that the "haarcascade_frontalface_default.xml" file is present at the location of exe file')
                            return
                        for(x, y, w, h) in faces:
                            cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
                            Id,conf= recognizer.predict(gray[y:y+h, x:x+w])
                            if(conf < 50):
                                ts = time.time()
                                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                                aa = df.loc[df['Id'] == Id]['Name'].values
                                stuEmail=df.loc[df['Id']==Id]['StudentEmail'].values
                                print(stuEmail)
                                parEmail=df.loc[df['Id']==Id]['ParentEmail'].values
                                print(parEmail)
                                tt = str(Id)+"-"+aa
                                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp,stuEmail,parEmail]
                            else:
                                Id = 'Unknown'
                                tt = str(Id)
                            cv2.putText(im, str(tt), (x, y+h), font, 1, (255, 255, 255), 2)
                        cv2.putText(im,'Press "q" to close camera',(50,50),cv2.FONT_HERSHEY_TRIPLEX,1,(0,0,255),2)
                        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
                        cv2.imshow('im', im)
                        cv2.moveWindow('im',15,15)
                        if (cv2.waitKey(1) == ord('q')):
                            messagebox.showinfo('Attendance Marked','Attendance of the recognized students has been marked successfully')
                            break
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    Hour, Minute, Second = timeStamp.split(":")
                    fileName = "Attendance/Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
                    attendance.to_csv(fileName, index=False)
                    cam.release()
                    cv2.destroyAllWindows()

            def viewStudentDataFile():
                    # adminTasksWindow.attributes('-topmost',False)
                    dataFilePath=os.path.join(root_path,'StudentDetails/StudentDetails.csv')
                    os.startfile(dataFilePath)
                    pass

            def viewAllTrainingImages():
                    imagesPath=os.path.join(root_path,'TrainingImage')
                    # os.open(imagesPath,mode=0o666,flags=os.O_RDWR | os.O_CREAT)
                    os.startfile(imagesPath)
                    pass

            # right frame button functions
            def reset_all():
                print('reset all invoked')
                proceed=messagebox.askyesno('Reset everything','This will delete all the data associated with this system and can\'t be undone. Are you sure ?')
                if proceed:
                    # delete all attendance files
                    try:
                        shutil.rmtree(os.path.join(root_path,'Attendance'))
                        os.mkdir(os.path.join(root_path,'Attendance'))
                    except:
                        os.mkdir(os.path.join(root_path,'Attendance'))
                        pass
                    # delete all student details
                    try:
                        shutil.rmtree(os.path.join(root_path,'StudentDetails'))
                        os.mkdir(os.path.join(root_path,'StudentDetails'))
                        if not os.path.isfile(os.path.join(root_path,'StudentDetails/StudentDetails.csv')):
                            StudentDetailsFilePath=os.path.join(root_path,'StudentDetails\\StudentDetails.csv')
                            # print(StudentDetailsFilePath)
                            with open(StudentDetailsFilePath,'w') as file:
                                row=['Id','Name','StudentEmail','ParentEmail']
                                writer=csv.writer(file)
                                writer.writerow(row)
                    except:
                        os.mkdir(os.path.join(root_path,'StudentDetails'))
                        if not os.path.isfile(os.path.join(root_path,'StudentDetails/StudentDetails.csv')):
                            StudentDetailsFilePath=os.path.join(root_path,'StudentDetails\\StudentDetails.csv')
                            # print(StudentDetailsFilePath)
                            with open(StudentDetailsFilePath,'w') as file:
                                row=['Id','Name','StudentEmail','ParentEmail']
                                writer=csv.writer(file)
                                writer.writerow(row)
                        pass
                    # delete all training images
                    try:
                        shutil.rmtree(os.path.join(root_path,'TrainingImage'))
                        os.mkdir(os.path.join(root_path,'TrainingImage'))
                    except:
                        os.mkdir(os.path.join(root_path,'TrainingImage'))
                        pass
                    # delete trained model
                    try:
                        shutil.rmtree(os.path.join(root_path,'Model'))
                        os.mkdir(os.path.join(root_path,'Model'))
                    except:
                        os.mkdir(os.path.join(root_path,'Model'))
                        pass
                    messagebox.showinfo('Reset Successful','Everything deleted from the system successfully')
                    pass

            def deleteModel():
                print('deleteModel invoked')
                proceed=messagebox.askyesno('Delete Model','Are you sure you want to delete the trained model ? This cannot be undone')
                # delete trained model
                if proceed:
                    try:
                        shutil.rmtree(os.path.join(root_path,'Model'))
                        os.mkdir(os.path.join(root_path,'Model'))
                    except:
                        os.mkdir(os.path.join(root_path,'Model'))
                        # messagebox.showerror('No Model Found Error','No trained model exists in the system')
                        pass
                    messagebox.showinfo('Model Deleted','Model deleted successfully')
                    pass

            def deleteAllStudentData():
                print('deleteAllStudentData invoked')
                proceed=messagebox.askyesno('Delete All Student Record','Are you sure you want to clear all student records ? This cannot be undone')
                if proceed:
                    # delete all student details
                    try:
                        shutil.rmtree(os.path.join(root_path,'StudentDetails'))
                        os.mkdir(os.path.join(root_path,'StudentDetails'))
                        if not os.path.isfile(os.path.join(root_path,'StudentDetails/StudentDetails.csv')):
                            StudentDetailsFilePath=os.path.join(root_path,'StudentDetails\\StudentDetails.csv')
                            # print(StudentDetailsFilePath)
                            with open(StudentDetailsFilePath,'w') as file:
                                row=['Id','Name','StudentEmail','ParentEmail']
                                writer=csv.writer(file)
                                writer.writerow(row)
                    except:
                        os.mkdir(os.path.join(root_path,'StudentDetails'))
                        if not os.path.isfile(os.path.join(root_path,'StudentDetails/StudentDetails.csv')):
                            StudentDetailsFilePath=os.path.join(root_path,'StudentDetails\\StudentDetails.csv')
                            # print(StudentDetailsFilePath)
                            with open(StudentDetailsFilePath,'w') as file:
                                row=['Id','Name','StudentEmail','ParentEmail']
                                writer=csv.writer(file)
                                writer.writerow(row)
                    messagebox.showinfo('Student Data Deleted','All student data deleted successfully')
                    # delete all training images
                    try:
                        shutil.rmtree(os.path.join(root_path,'TrainingImage'))
                        os.mkdir(os.path.join(root_path,'TrainingImage'))
                    except:
                        os.mkdir(os.path.join(root_path,'TrainingImage'))
                        pass

            def deleteAllAttendanceFiles():
                print('deleteAllAttendanceFiles invoked')
                proceed=messagebox.askyesno('Delete All Attendance Record','Are you sure you want to clear all attendance records ? This cannot be undone')
                if proceed:
                    # delete all attendance files
                    try:
                        shutil.rmtree(os.path.join(root_path,'Attendance'))
                        os.mkdir(os.path.join(root_path,'Attendance'))
                    except:
                        os.mkdir(os.path.join(root_path,'Attendance'))
                        pass
                    messagebox.showinfo('All Attendance Cleared','All attendance files cleared successfully from the system')

            # defining the window button functions
            def goBack():
                adminTasksWindow.destroy()

            adminTasksWindow=Toplevel(signinWindow)
            adminTasksWindow.grab_set()

            adminTasksWindow.configure(background='white')

            adminTasksWindow_width = 800
            adminTasksWindow_height = 400

            x_Left = int(adminTasksWindow.winfo_screenwidth()/2 - adminTasksWindow_width/2)
            y_Top = int(adminTasksWindow.winfo_screenheight()/2 - adminTasksWindow_height/2)

            adminTasksWindow.geometry(f'{adminTasksWindow_width}x{adminTasksWindow_height}+{x_Left}+{y_Top}')

            # disabling the window resize option
            adminTasksWindow.resizable(False,False)

            # giving the heading
            message = Label(adminTasksWindow, text="Face-Recognition-Based-Attendance-System", bg="white",fg="black", width=100, height=2, font=('times', 30, 'bold'))
            message.pack(side='top',anchor='center')


            # defining the left frame
            leftFrame=Frame(adminTasksWindow,bg='white')
            leftFrame.pack(side='left',anchor='center',padx=20)

            # defining middle frame
            middleFrame=Frame(adminTasksWindow,bg='white')
            middleFrame.pack(side='left',anchor='center',padx=95)

            # middleFrame2=Frame(adminTasksWindow,bg='white')
            # middleFrame2.pack(side='left',anchor='center',padx=10)
            # defining the right frame
            rightFrame=Frame(adminTasksWindow,bg='white')
            rightFrame.pack(side='right',anchor='center',padx=20)

            # left frame buttons
            sendEmailBtn=ttk.Button(leftFrame,text='Send Email',style='W.TButton',command=send_email)
            sendEmailBtn.pack(side='top',pady=10)

            trainModelBtn=ttk.Button(leftFrame,text='Train Model',style='W.TButton',command=TrainImages)
            trainModelBtn.pack(side='top',pady=10)

            viewExcelFileBtn=ttk.Button(leftFrame,text='View Attendance',style='W.TButton',command=viewExcelFile)
            viewExcelFileBtn.pack(side='top',pady=10)

            viewLatestAttendanceSheetBtn=ttk.Button(leftFrame,text='View Latest Attendance Sheet',style='W.TButton',command=viewLatestAttendanceSheet)
            viewLatestAttendanceSheetBtn.pack(side='top',pady=10)

            # defining the back button
            BackBtn=ttk.Button(leftFrame,text='Back',style='TButton',command=goBack)
            BackBtn.pack(side='bottom',anchor='w',pady=10)

            # middle frame buttons
            LoginLabel=ttk.Label(middleFrame,text='Logged in as admin',background='white',foreground='black',font=('times', 15))
            LoginLabel.pack(side='top',pady=10)
            
            initializeBtn=ttk.Button(middleFrame,text='Initialize Folders',style='W.TButton',command=initialize)
            initializeBtn.pack(side='top',pady=10)

            markAttendanceBtn=ttk.Button(middleFrame,text='Mark Attendance',style='W.TButton',command=markAttendance)
            markAttendanceBtn.pack(side='top',pady=10)

            viewStudentDataFileBtn=ttk.Button(middleFrame,text='View Student Data File',style='W.TButton',command=viewStudentDataFile)
            viewStudentDataFileBtn.pack(side='top',pady=10)

            viewAllTrainingImagesBtn=ttk.Button(middleFrame,text='View All Training Images',style='W.TButton',command=viewAllTrainingImages)
            viewAllTrainingImagesBtn.pack(side='top',pady=10)


            # right frame buttons
            resetBtn=ttk.Button(rightFrame,text='Reset',style='W.TButton',command=reset_all)
            resetBtn.pack(side='top',anchor='center',pady=10)

            deleteModelBtn=ttk.Button(rightFrame,text='Delete Model',style='W.TButton',command=deleteModel)
            deleteModelBtn.pack(side='top',anchor='center',pady=10)

            deleteAllStudentDataBtn=ttk.Button(rightFrame,text='Delete All Student Data',style='W.TButton',command=deleteAllStudentData)
            deleteAllStudentDataBtn.pack(side='top',anchor='center',pady=10)

            deleteAllAttendanceFiles=ttk.Button(rightFrame,text='Delete All Attendance Files',style='W.TButton',command=deleteAllAttendanceFiles)
            deleteAllAttendanceFiles.pack(side='top',anchor='center',pady=10)

            # defining the quit button
            quitBtn=ttk.Button(rightFrame,text='Quit',command=lambda:exit(),style='TButton')
            quitBtn.pack(side='right',anchor='s',pady=10)

            adminTasksWindow.mainloop()

            pass
        else:
            df=pd.read_csv(os.path.join(root_path,'StudentDetails/StudentDetails.csv'))
            df=pd.DataFrame(df)
            ids=df['Id']
            names=df['Name']
            for i in range(len(ids)):
                id=str(ids[i])
                name=str(names[i])
                if uname==name and passwd==id:
                    # render the studenttask.py
                    def goBack():
                        studentTaskWindow.destroy()

                    def markAttendance():
                        try:
                            recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
                        except:
                            messagebox.showerror('Recognizer object creation error','Please check that you have "opencv-contrib-python" installed on your system. If not then run this command in cmd "pip install opencv-contrib-python"')
                            return
                        try:
                            recognizer.read("Model/model.yml")
                        except:
                            messagebox.showerror('Model not readable','The trained model is either deleted from the system or unable to access. Please try again by trainig the model again.')
                            return
                        harcascadePath = "haarcascade_frontalface_default.xml"
                        try:
                            faceCascade = cv2.CascadeClassifier(harcascadePath)
                        except:
                            messagebox.showerror('Haar XML file not found','Please check that the "haarcascade_frontalface_default.xml" file is present at the location of exe file')
                            return
                        df = pd.read_csv("StudentDetails/StudentDetails.csv")
                        try:
                            cam = cv2.VideoCapture(0)
                            cam.set(cv2.CAP_PROP_FRAME_WIDTH,640)
                            cam.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
                        except:
                            messagebox.showerror('Camera access error','Please check that camera privacy settings have enabled camera access for applications')
                            return
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        col_names = ['Id', 'Name', 'Date', 'Time','StudentEmail','ParentEmail']
                        attendance = pd.DataFrame(columns=col_names)
                        while True:
                            ret, im = cam.read()
                            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                            try:
                                faces = faceCascade.detectMultiScale(gray, 1.3, 5)
                            except:
                                messagebox.showerror('Haar XML file not found','Please check that the "haarcascade_frontalface_default.xml" file is present at the location of exe file')
                                return
                            for(x, y, w, h) in faces:
                                cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
                                Id,conf= recognizer.predict(gray[y:y+h, x:x+w])
                                if(conf < 50):
                                    ts = time.time()
                                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                                    aa = df.loc[df['Id'] == Id]['Name'].values
                                    stuEmail=df.loc[df['Id']==Id]['StudentEmail'].values
                                    print(stuEmail)
                                    parEmail=df.loc[df['Id']==Id]['ParentEmail'].values
                                    print(parEmail)
                                    tt = str(Id)+"-"+aa
                                    attendance.loc[len(attendance)] = [Id, aa, date, timeStamp,stuEmail,parEmail]
                                else:
                                    Id = 'Unknown'
                                    tt = str(Id)
                                cv2.putText(im, str(tt), (x, y+h), font, 1, (255, 255, 255), 2)
                            cv2.putText(im,'Press "q" to close camera',(50,50),cv2.FONT_HERSHEY_TRIPLEX,1,(0,0,255),2)
                            attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
                            cv2.imshow('im', im)
                            cv2.moveWindow('im',15,15)
                            if (cv2.waitKey(1) == ord('q')):
                                messagebox.showinfo('Attendance Marked','Attendance of the recognized students has been marked successfully')
                                break
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        Hour, Minute, Second = timeStamp.split(":")
                        fileName = "Attendance/Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
                        attendance.to_csv(fileName, index=False)
                        cam.release()
                        cv2.destroyAllWindows()

                    studentTaskWindow=Toplevel(signinWindow)
                    studentTaskWindow.grab_set()

                    studentTaskWindow.configure(background='white')

                    studentTaskWindow_width = 800
                    studentTaskWindow_height = 400

                    x_Left = int(studentTaskWindow.winfo_screenwidth()/2 - studentTaskWindow_width/2)
                    y_Top = int(studentTaskWindow.winfo_screenheight()/2 - studentTaskWindow_height/2)

                    studentTaskWindow.geometry(f'{studentTaskWindow_width}x{studentTaskWindow_height}+{x_Left}+{y_Top}')

                    studentTaskWindow.resizable(False,False)

                    # giving the heading
                    message = Label(studentTaskWindow, text="Face-Recognition-Based-Attendance-System", bg="white",fg="black", width=100, height=2, font=('times', 30, 'bold'))
                    message.pack(side='top',anchor='center')

                    LoginLabel=ttk.Label(studentTaskWindow,text='Logged in as student',background='white',foreground='black',font=('times', 15))
                    LoginLabel.pack(side='top',pady=20)

                    markAttendanceBtn=ttk.Button(studentTaskWindow,text='Mark Attendance',width=50,style='W.TButton',command=markAttendance)
                    markAttendanceBtn.pack(side='top',pady=70)

                    # defining the back button
                    BackBtn=ttk.Button(studentTaskWindow,text='Back',style='TButton',command=goBack)
                    BackBtn.pack(side='left',anchor='s',pady=10)

                    # defining the quit button
                    quitBtn=ttk.Button(studentTaskWindow,text='Quit',command=lambda:exit(),style='TButton')
                    quitBtn.pack(side='right',anchor='s',pady=10)

                    studentTaskWindow.mainloop()
                    print(True)
                else:
                    messagebox.showerror('Wrong Credentials','Please enter correct credentials')
                    print(False)
                print(id,name)
                pass

    

    # defining the top frame
    topFrame=Frame(signinWindow,bg='white')
    topFrame.pack(side='top',anchor='n')

    # defining the bottom frame
    bottomFrame=Frame(signinWindow,bg='white')
    bottomFrame.pack(side='top',anchor='n')

    # defining the bottommost frame
    bottommostFrame=Frame(signinWindow,bg='white')
    bottommostFrame.pack(side='top',anchor='n')

    # creating the login form
    unameLabel=Label(topFrame,text='Username',font=('times', 15, 'bold'),anchor='w',background='white',width=10)
    unameLabel.pack(side='left',pady=10)

    unameEntry=Entry(topFrame,bg='white',font=('times', 15, 'bold'),width=20)
    unameEntry.pack(side='left',pady=10)

    passwdLabel=Label(bottomFrame,text='Password',font=('times', 15, 'bold'),anchor='w',background='white',width=10)
    passwdLabel.pack(side='left',pady=10)

    passwdEntry=Entry(bottomFrame,bg='white',font=('times', 15, 'bold'),width=20,show='*')
    passwdEntry.pack(side='left',pady=10)

    # defining the login button
    loginBtn=ttk.Button(bottommostFrame,text='Login',style='TButton',command=verifyCred)
    loginBtn.pack(side='left',pady=20)

    # defining the back button
    BackBtn=ttk.Button(signinWindow,text='Back',style='TButton',command=goBack)
    BackBtn.pack(side='left',anchor='s')

    # defining the quit button
    quitBtn=ttk.Button(signinWindow,text='Quit',command=lambda:exit(),style='TButton')
    quitBtn.pack(side='right',anchor='s')

    signinWindow.mainloop()

main_function()