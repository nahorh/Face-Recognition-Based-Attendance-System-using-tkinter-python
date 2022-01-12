import datetime
import shutil
import os
import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from email.message import EmailMessage
import smtplib
import cv2
import csv
import pandas as pd
import numpy as np
from PIL import Image
import time
import sys

def main_function():

    root_path=os.getcwd()
    def disableButton():
        pass
    def quitBtnFunction():
        proceed=messagebox.askyesno('Close Application','Are you sure you want to exit the application?')
        if proceed:
            sys.exit()
        else:
            pass

    # creating an instance of homeWindow
    homeWindow = Tk()
    homeWindow.title("Face Recognition Attendance System")

    # defining the style of buttons designed
    # default buttons styles
    backBtnImg=PhotoImage(file='buttonDrawingFiles/backButton.png')
    quitBtnImg=PhotoImage(file='buttonDrawingFiles/quitButton.png')

    # home window button styles
    signInBtnImg=PhotoImage(file='buttonDrawingFiles/signinButton.png')
    signUpBtnImg=PhotoImage(file='buttonDrawingFiles/signupButton.png')
    forgotPasswordBtnImg=PhotoImage(file='buttonDrawingFiles/forgotpasswordButton.png')

    # sign in window button styles
    loginBtnImg=PhotoImage(file='buttonDrawingFiles/loginButton.png')

    # sign up window button styles
    signUpAndTakeImagesBtnImg=PhotoImage(file='buttonDrawingFiles/signupandtakeimagesButton.png')
    
    # student task window button styles
    markAttendanceBtnImg=PhotoImage(file='buttonDrawingFiles/markattendanceButton.png')

    # admin task window button styles
    sendEmailBtnImg=PhotoImage(file='buttonDrawingFiles/sendemailButton.png')
    trainModelBtnImg=PhotoImage(file='buttonDrawingFiles/trainmodelButton.png')
    viewExcelFileBtnImg=PhotoImage(file='buttonDrawingFiles/viewattendanceButton.png')
    viewLatestAttendanceSheetBtnImg=PhotoImage(file='buttonDrawingFiles/viewlatestattendanceButton.png')
    initializeBtnImg=PhotoImage(file='buttonDrawingFiles/createfoldersButton.png')
    viewStudentDataFileBtnImg=PhotoImage(file='buttonDrawingFiles/viewstudentdetailsButton.png')
    viewAllTrainingImagesBtnImg=PhotoImage(file='buttonDrawingFiles/viewtrainingimagesButton.png')
    resetBtnImg=PhotoImage(file='buttonDrawingFiles/fullresetButton.png')
    deleteModelBtnImg=PhotoImage(file='buttonDrawingFiles/deletemodelButton.png')
    deleteAllStudentDataBtnImg=PhotoImage(file='buttonDrawingFiles/deleteallstudentdataButton.png')
    deleteAllAttendanceFilesBtnImg=PhotoImage(file='buttonDrawingFiles/deleteallattendancedataButton.png')
    
    # forgot password window button styles
    submitBtnImg=PhotoImage(file='buttonDrawingFiles/submitButton.png')
    
    # homeWindow.protocol('WM_DELETE_WINDOW',disableButton)
    # homeWindow.overrideredirect(True)
    # homeWindow.attributes('-topmost',True)

    # defining the style for buttons
    # style=ttk.Style()
    # style.configure('TButton',font=('calibri',12,'bold'),borderwidth='4',foreground='black',background='#0075BA')
    # style.map('TButton',foreground=[('active','!disabled','black')],background=[('active','#0075BA')])

    homeWindow.configure(background='white')

    window_width = 800
    window_height = 400

    x_Left = int(homeWindow.winfo_screenwidth()/2 - window_width/2)
    y_Top = int(homeWindow.winfo_screenheight()/2 - window_height/2)

    # setting the geometry of the homeWindow and align it to the center
    homeWindow.geometry(f'{window_width}x{window_height}+{x_Left}+{y_Top}')

    # disable homeWindow resizing option
    homeWindow.resizable(False,False)

    # defining button functions
    def SignIn():
        # homeWindow.attributes('-topmost',False)
        # print('Sign In invoked')
        # Toplevel(signin.main_function())
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
                    # adminTasksWindow.attributes('-topmost',True)
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
                message = Label(adminTasksWindow, text="Face-Recognition-Based-Attendance-System", bg="white",fg="black", width=100, height=2, font=('calibri', 30, 'bold'))
                message.pack(side='top',anchor='center')

                LoginLabel=ttk.Label(adminTasksWindow,text='Logged in as admin',background='white',foreground='black',font=('calibri', 15,'bold'),width=25,anchor='center')
                LoginLabel.pack(side='top',anchor='center',pady=0)

                # defining the left frame
                leftFrame=Frame(adminTasksWindow,bg='white')
                leftFrame.pack(side='left',anchor='center',padx=50)

                # defining middle frame
                middleFrame=Frame(adminTasksWindow,bg='white')
                middleFrame.pack(side='left',anchor='center',padx=60)

                # middleFrame2=Frame(adminTasksWindow,bg='white')
                # middleFrame2.pack(side='left',anchor='center',padx=10)
                # defining the right frame
                rightFrame=Frame(adminTasksWindow,bg='white')
                rightFrame.pack(side='left',anchor='center',padx=40)

                # left frame buttons
                # sendEmailBtn=ttk.Button(leftFrame,text='Send Email',style='TButton',command=send_email,width=25)
                # sendEmailBtn.pack(side='top',pady=10)

                sendEmailBtn=Button(leftFrame,command=send_email,image=sendEmailBtnImg,borderwidth=0,bg='white',activebackground='white')
                sendEmailBtn.pack(side='top',pady=5)

                # trainModelBtn=ttk.Button(leftFrame,text='Train Model',style='TButton',command=TrainImages,width=25)
                # trainModelBtn.pack(side='top',pady=10)

                trainModelBtn=Button(leftFrame,command=TrainImages,image=trainModelBtnImg,borderwidth=0,bg='white',activebackground='white')
                trainModelBtn.pack(side='top',pady=5)

                # viewExcelFileBtn=ttk.Button(leftFrame,text='View Attendance',style='TButton',command=viewExcelFile,width=25)
                # viewExcelFileBtn.pack(side='top',pady=10)
                viewExcelFileBtn=Button(leftFrame,command=viewExcelFile,image=viewExcelFileBtnImg,borderwidth=0,bg='white',activebackground='white')
                viewExcelFileBtn.pack(side='top',pady=5)

                # viewLatestAttendanceSheetBtn=ttk.Button(leftFrame,text='View Latest Attendance Sheet',style='TButton',command=viewLatestAttendanceSheet,width=25)
                # viewLatestAttendanceSheetBtn.pack(side='top',pady=10)
                viewLatestAttendanceSheetBtn=Button(leftFrame,command=viewLatestAttendanceSheet,image=viewLatestAttendanceSheetBtnImg,borderwidth=0,bg='white',activebackground='white')
                viewLatestAttendanceSheetBtn.pack(side='top',pady=5)

                # defining the back button
                BackBtn=Button(leftFrame,command=goBack,image=backBtnImg,borderwidth=0,bg='white',activebackground='white')
                BackBtn.pack(side='bottom',anchor='w',pady=5)

                # middle frame buttons

                
                initializeBtn=Button(middleFrame,command=initialize,image=initializeBtnImg,borderwidth=0,bg='white',activebackground='white')
                initializeBtn.pack(side='top',pady=5)

                markAttendanceBtn=Button(middleFrame,command=markAttendance,image=markAttendanceBtnImg,borderwidth=0,bg='white',activebackground='white')
                markAttendanceBtn.pack(side='top',pady=5)

                viewStudentDataFileBtn=Button(middleFrame,command=viewStudentDataFile,image=viewStudentDataFileBtnImg,borderwidth=0,bg='white',activebackground='white')
                viewStudentDataFileBtn.pack(side='top',pady=5)

                viewAllTrainingImagesBtn=Button(middleFrame,command=viewAllTrainingImages,image=viewAllTrainingImagesBtnImg,borderwidth=0,bg='white',activebackground='white')
                viewAllTrainingImagesBtn.pack(side='top',pady=5)


                # right frame buttons
                resetBtn=Button(rightFrame,command=reset_all,image=resetBtnImg,borderwidth=0,bg='white',activebackground='white')
                resetBtn.pack(side='top',anchor='center',pady=5)

                deleteModelBtn=Button(rightFrame,command=deleteModel,image=deleteModelBtnImg,borderwidth=0,bg='white',activebackground='white')
                deleteModelBtn.pack(side='top',anchor='center',pady=5)

                deleteAllStudentDataBtn=Button(rightFrame,command=deleteAllStudentData,image=deleteAllStudentDataBtnImg,borderwidth=0,bg='white',activebackground='white')
                deleteAllStudentDataBtn.pack(side='top',anchor='center',pady=5)

                deleteAllAttendanceFiles=Button(rightFrame,command=deleteAllAttendanceFiles,image=deleteAllAttendanceFilesBtnImg,borderwidth=0,bg='white',activebackground='white')
                deleteAllAttendanceFiles.pack(side='top',anchor='center',pady=5)

                # defining the quit button
                quitBtn=Button(rightFrame,command=quitBtnFunction,image=quitBtnImg,borderwidth=0,bg='white',activebackground='white')
                quitBtn.pack(side='right',anchor='s',pady=5)

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
                        message = Label(studentTaskWindow, text="Face-Recognition-Based-Attendance-System", bg="white",fg="black", width=100, height=2, font=('calibri', 30, 'bold'))
                        message.pack(side='top',anchor='center')

                        LoginLabel=ttk.Label(studentTaskWindow,text='Logged in as student',background='white',foreground='black',font=('calibri', 15,'bold'))
                        LoginLabel.pack(side='top',pady=0)

                        # markAttendanceBtn=ttk.Button(studentTaskWindow,text='Mark Attendance',width=50,style='TButton',command=markAttendance)
                        # markAttendanceBtn.pack(side='top',pady=70)

                        markAttendanceBtn=Button(studentTaskWindow,command=markAttendance,image=markAttendanceBtnImg,borderwidth=0,bg='white',activebackground='white')
                        markAttendanceBtn.pack(side='top',pady=80)

                        # defining the back button
                        # BackBtn=ttk.Button(studentTaskWindow,text='Back',style='TButton',command=goBack)
                        # BackBtn.pack(side='left',anchor='s',pady=10)

                        BackBtn=Button(studentTaskWindow,command=goBack,image=backBtnImg,borderwidth=0,bg='white',activebackground='white')
                        BackBtn.pack(side='left',anchor='s',pady=5)

                        # defining the quit button
                        # quitBtn=ttk.Button(studentTaskWindow,text='Quit',command=quitBtnFunction,style='TButton')
                        # quitBtn.pack(side='right',anchor='s',pady=10)

                        quitBtn=Button(studentTaskWindow,command=quitBtnFunction,image=quitBtnImg,borderwidth=0,bg='white',activebackground='white')
                        quitBtn.pack(side='right',anchor='s',pady=5)

                        studentTaskWindow.mainloop()
                        print(True)
                else:
                    messagebox.showerror('Wrong Credentials','Please enter correct credentials')
                    print(False)
                    # print(id,name)
                    pass

        def goBack():
            signinWindow.destroy()

        def disableButton():
            pass
        signinWindow=Toplevel(homeWindow)
        signinWindow.grab_set()
        signinWindow.title("Face Recognition Attendance System")
        signinWindow.configure(background='white')
        signinWindow.protocol('WM_DELETE_WINDOW',disableButton)
        window_width = 800
        window_height = 400

        x_Left = int(signinWindow.winfo_screenwidth()/2 - window_width/2)
        y_Top = int(signinWindow.winfo_screenheight()/2 - window_height/2)

        signinWindow.geometry(f'{window_width}x{window_height}+{x_Left}+{y_Top}')

        signinWindow.resizable(False,False)

        # giving the heading
        message = Label(signinWindow, text="Face-Recognition-Based-Attendance-System", bg="white",fg="black", width=100, height=2, font=('calibri', 30, 'bold'))
        message.pack(side='top',anchor='center')

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
        unameLabel=Label(topFrame,text='Username',font=('calibri', 15, 'bold'),anchor='w',background='white',width=10)
        unameLabel.pack(side='left',pady=10)

        unameEntry=Entry(topFrame,bg='white',font=('calibri', 15, 'bold'),width=20)
        unameEntry.pack(side='left',pady=10)

        passwdLabel=Label(bottomFrame,text='Password',font=('calibri', 15, 'bold'),anchor='w',background='white',width=10)
        passwdLabel.pack(side='left',pady=10)

        passwdEntry=Entry(bottomFrame,bg='white',font=('calibri', 15, 'bold'),width=20,show='*')
        passwdEntry.pack(side='left',pady=10)

        # defining the login button
        # loginBtn=ttk.Button(bottommostFrame,text='Login',style='TButton',command=verifyCred)
        # loginBtn.pack(side='left',pady=20)
        
        loginBtn=Button(bottommostFrame,command=verifyCred,image=loginBtnImg,borderwidth=0,bg='white',activebackground='white')
        loginBtn.pack(side='left',pady=20)

        # defining the back button
        BackBtn=Button(signinWindow,command=goBack,image=backBtnImg,borderwidth=0,bg='white',activebackground='white')
        BackBtn.pack(side='left',anchor='s')

        # defining the quit button
        quitBtn=Button(signinWindow,command=quitBtnFunction,image=quitBtnImg,borderwidth=0,bg='white',activebackground='white')
        quitBtn.pack(side='right',anchor='s')

        signinWindow.mainloop()


    def SignUp():
        # homeWindow.attributes('-topmost',False)
        print('Sign Up invoked')
        # Toplevel(signup.main_function())
        # import signup
        # signup.mainFunction()
        signUpWindow=Toplevel(homeWindow)

        signUpWindow.grab_set()

        signUpWindow.title("Face Recognition Attendance System")

        def goBack():
            signUpWindow.destroy()
        
        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                pass

            try:
                import unicodedata
                unicodedata.numeric(s)
                return True
            except (TypeError, ValueError):
                pass

            return False

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

        def TakeImages():
            Id = (txt.get())
            name = (txt2.get())
            student_email=txt3.get()
            parent_email=txt4.get()
            symbol='@'
            if(is_number(Id) and name.isalpha() and symbol in str(student_email) and symbol in str(parent_email)):
                try:
                    cam = cv2.VideoCapture(0)
                    cam.set(cv2.CAP_PROP_FRAME_WIDTH,640)
                    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
                except:
                    tk.messagebox.showerror('Camera access error','Please check that camera privacy settings have enabled camera access for applications')
                    return
                harcascadePath = "haarcascade_frontalface_default.xml"
                try:
                    detector = cv2.CascadeClassifier(harcascadePath)
                except:
                    tk.messagebox.showerror('Haar XML file not found','Please check that the "haarcascade_frontalface_default.xml" file is present at the location of exe file')
                    return
                sampleNum = 0
                while(True):
                    ret, img = cam.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    try:
                        faces = detector.detectMultiScale(gray, 1.3, 5)
                    except:
                        tk.messagebox.showerror('Haar XML file not found','Please check that the "haarcascade_frontalface_default.xml" file is present at the location of exe file')
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                        # incrementing sample number
                        sampleNum = sampleNum+1
                        # saving the captured face in the dataset folder TrainingImage
                        # display the frame
                        cv2.putText(img,'Press any key to capture next image',(0,20),cv2.FONT_HERSHEY_TRIPLEX,0.5,(0,0,255),1)
                        windowName=f'Image No: {sampleNum}, Name: {name}, Id:{Id}'
                        cv2.imshow(windowName, img)
                        cv2.moveWindow(windowName,15,15)
                        cv2.waitKey(0)
                        cv2.imwrite("TrainingImage/"+name + "."+Id + '.' +str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                    # wait for 500 miliseconds
                    # if cv2.waitKey(500) & 0xFF == ord('q'):
                    #     break
                    # break if the sample number is morethan 100
                    if sampleNum > 9:
                        break
                cam.release()
                cv2.destroyAllWindows()
                # res = "Images Saved for ID : " + Id + " Name : " + name
                row = [Id, name,student_email,parent_email]
                with open('StudentDetails/StudentDetails.csv', 'r') as file:
                    data=file.read()
                    print(data)
                if f'{Id},{name}' in data:
                    print('user present already')
                    messagebox.showwarning('User already present',f'User {name} already exists in the database. The captured images will be replaced with the previous ones')
                    TrainImages()
                else:
                    with open('StudentDetails\\StudentDetails.csv', 'a+') as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerow(row)
                    csvFile.close()
                    TrainImages()
                    msg=EmailMessage()
                    msg['Subject']='Welcome Email'
                    msg['From']='Attendance System'
                    msg['To']=student_email
                    msg.set_content(f'''
                    Dear {name},
                                Thanks for signing up in Attendance System. Your credentials for marking attendance are given below.
                    Username: {name}
                    Password: {Id}
                    
                    Thank you.
                    ''')

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

                    try:
                        server=smtplib.SMTP_SSL('smtp.gmail.com',465)
                    except:
                        messagebox.showerror('Server Setup Error','Unable to create instance of SMTP server. Please try again.')
                        return
                    try:
                        server.login(adminEmail,adminPwd)
                    except:
                        messagebox.showerror('Login Error','Unable to login in to email account due to incorrect credentials or bad internet connection.')
                    server.send_message(msg)
                    server.quit()
                    messagebox.showinfo('Email Sent','Your credentials have been sent to your email successfully. Kindly check that and login with the same next time')
                
                
                
            elif str(Id)=='' or str(name)=='' or not is_number(Id) or not name.isalpha():
                tk.messagebox.showerror('Value Error','Please enter correct details')

        # defining the top frame
        topFrame=tk.Frame(signUpWindow,bg='yellow')
        topFrame.pack(side='top',anchor='n')

        # defining the left frame
        leftFrame=tk.Frame(signUpWindow,bg='white',highlightbackground='black',highlightthickness=2)
        leftFrame.pack(side='top',anchor='center',padx=50,pady=40)

        signUpWindow.configure(background='white')

        window_width = 800
        window_height = 400

        #calculate coordinates of screen and signUpWindow position
        x_Left = int(signUpWindow.winfo_screenwidth()/2 - window_width/2)
        y_Top = int(signUpWindow.winfo_screenheight()/2 - window_height/2)

        # defining the geomtry of signUpWindow and centering it on the screen
        signUpWindow.geometry(f'{window_width}x{window_height}+{x_Left}+{y_Top}')

        # disabling the signUpWindow resize option
        signUpWindow.resizable(False,False)

        signUpWindow.grid_rowconfigure(0, weight=1)
        signUpWindow.grid_columnconfigure(0, weight=1)

        # defining the header of the signUpWindow
        message = tk.Label(topFrame, text="Face-Recognition-Based-Attendance-System", bg="white",fg="black", width=100, height=2, font=('calibri', 30, 'bold'))
        message.pack(side='top',anchor='center')

        # creating the signup form
        lbl = tk.Label(leftFrame, text="Roll Id", width=12, height=1,fg="black", bg="white", font=('calibri', 15, ' bold '),anchor='w')
        lbl.grid(row=1,column=0)

        txt = tk.Entry(leftFrame, width=25, bg="white",fg="black", font=('calibri', 15, ' bold '))
        txt.grid(row=1,column=1)

        lbl2 = tk.Label(leftFrame, text="Name", width=12, fg="black",bg="white", height=1, font=('calibri', 15, ' bold '),anchor='w')
        lbl2.grid(row=0,column=0)

        txt2 = tk.Entry(leftFrame, width=25, bg="white",fg="black", font=('calibri', 15, ' bold '))
        txt2.grid(row=0,column=1)

        lbl3=tk.Label(leftFrame,text='Student Email',bg='white',fg='black',font=('calibri',15,'bold'),width=12,anchor='w')
        lbl3.grid(row=2,column=0)

        txt3=tk.Entry(leftFrame,width=25,bg='white',fg='black',font=('calibri',15,'bold'))
        txt3.grid(row=2,column=1)

        lbl4=tk.Label(leftFrame,width=12,text='Parent Email',font=('calibri',15,'bold'),bg='white',fg='black',anchor='w')
        lbl4.grid(row=3,column=0)

        txt4=tk.Entry(leftFrame,width=25,bg='white',fg='black',font=('calibri',15,'bold'))
        txt4.grid(row=3,column=1)

        # defining the signup button
        # SignUpBtn=ttk.Button(leftFrame,text='SignUp & Take Images',style='TButton',command=TakeImages)
        # SignUpBtn.grid(row=4,column=1)
        SignUpBtn=Button(leftFrame,command=TakeImages,image=signUpAndTakeImagesBtnImg,borderwidth=0,bg='white',activebackground='white')
        SignUpBtn.grid(row=4,column=1)

        # defining the back button
        BackBtn=Button(signUpWindow,command=goBack,image=backBtnImg,borderwidth=0,bg='white',activebackground='white')
        BackBtn.pack(side='left',anchor='s')

        # defining the quit button
        quitBtn=Button(signUpWindow,text='Quit',command=quitBtnFunction,image=quitBtnImg,borderwidth=0,bg='white',activebackground='white')
        quitBtn.pack(side='right',anchor='s')

        signUpWindow.mainloop()

    def forgotPasswd():
        def sendCreds():
            uname=unameEntry.get()
            uemail=uemailLabelEntry.get()
            df=pd.read_csv(os.path.join(root_path,'StudentDetails/StudentDetails.csv'))
            df=pd.DataFrame(df)
            try:
                extractedEmail=df.loc[df['Name']==uname]['StudentEmail'].values[0]
                extractedId=df.loc[df['Name']==uname]['Id'].values[0]
            except:
                messagebox.showerror('Record Not Found','No record for this user exists in the system. Please enter correct details')
            if extractedEmail==uemail:
                # email the credentials
                msg=EmailMessage()
                msg['Subject']='Attendance System Credentials'
                msg['From']='Attendance System'
                msg['To']=str(uemail)
                msg.set_content(f'''
                Dear {uname},
                            Your credentials for logging into attendance system are given below.
                Username: {uname}
                Password: {extractedId}

                Thank you.
                ''')
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

                try:
                    server=smtplib.SMTP_SSL('smtp.gmail.com',465)
                except:
                    messagebox.showerror('Server Setup Error','Unable to create instance of SMTP server. Please try again.')
                    return
                try:
                    server.login(adminEmail,adminPwd)
                except:
                    messagebox.showerror('Login Error','Unable to login in to email account due to incorrect credentials or bad internet connection.')
                server.send_message(msg)
                server.quit()
                messagebox.showinfo('Email Sent','Your credentials have been sent to your email successfully. Kindly check that and login with the same next time')
            else:
                messagebox.showerror('Incorrect email','Please enter the email correctly')

        def goBack():
            forgotPasswordWindow.destroy()

        forgotPasswordWindow=Toplevel(homeWindow)
        forgotPasswordWindow.grab_set()
        forgotPasswordWindow.configure(background='white')

        window_width = 800
        window_height = 400

        x_Left = int(forgotPasswordWindow.winfo_screenwidth()/2 - window_width/2)
        y_Top = int(forgotPasswordWindow.winfo_screenheight()/2 - window_height/2)

        # setting the geometry of the homeWindow and align it to the center
        forgotPasswordWindow.geometry(f'{window_width}x{window_height}+{x_Left}+{y_Top}')

        # disable homeWindow resizing option
        forgotPasswordWindow.resizable(False,False)


        # giving the heading
        message = Label(forgotPasswordWindow, text="Face-Recognition-Based-Attendance-System", bg="white",fg="black", width=100, height=2, font=('calibri', 30, 'bold'))
        message.pack(side='top',anchor='center')

        # defining the top frame
        topFrame=Frame(forgotPasswordWindow,bg='white')
        topFrame.pack(side='top',anchor='center')

        # defining the bottom frame
        bottomFrame=Frame(forgotPasswordWindow,bg='white')
        bottomFrame.pack(side='top',anchor='center')

        # defining name entry
        unameLabel=Label(topFrame,text='Name',bg='white',fg='black',height=1,font=('calibri',14,'bold'),width=10,anchor='w')
        unameLabel.pack(side='left',anchor='center')

        unameEntry=Entry(topFrame,bg='white',fg='black',width=20,font=('calibri',14,'bold'))
        unameEntry.pack(side='left',anchor='center')

        # defining email entry field
        uemailLabel=Label(bottomFrame,text='Email',bg='white',fg='black',height=1,font=('calibri',14,'bold'),width=10,anchor='w')
        uemailLabel.pack(side='left',anchor='center')

        uemailLabelEntry=Entry(bottomFrame,bg='white',fg='black',width=20,font=('calibri',14,'bold'))
        uemailLabelEntry.pack(side='left',anchor='center')

        # defining the submit button
        submitBtn=Button(forgotPasswordWindow,command=sendCreds,image=submitBtnImg,borderwidth=0,bg='white',activebackground='white')
        submitBtn.pack(side='top',pady=20,anchor='center')

        # defining the back button
        backBtn=Button(forgotPasswordWindow,command=goBack,image=backBtnImg,borderwidth=0,bg='white',activebackground='white')
        backBtn.pack(side='left',anchor='s')

        # defining the quit button
        quitBtn=Button(forgotPasswordWindow,command=quitBtnFunction,image=quitBtnImg,borderwidth=0,bg='white',activebackground='white')
        quitBtn.pack(side='right',anchor='s')




        forgotPasswordWindow.mainloop()

    # giving the heading
    message = Label(homeWindow, text="Face-Recognition-Based-Attendance-System", bg="white",fg="black", width=100, height=2, font=('calibri', 30, 'bold'))
    message.pack(side='top',anchor='center')

    # defining the frame
    topFrame=Frame(homeWindow,bg='white')
    topFrame.pack(side='top',anchor='n')

    # defining and placing the buttons in the frame
    # signInBtn=ttk.Button(topFrame,text='Sign In',style='TButton',command=SignIn)
    # signInBtn.pack(side='top',pady=20)

    signInBtn=Button(topFrame,command=SignIn,image=signInBtnImg,borderwidth=0,bg='white',activebackground='white')
    signInBtn.pack(side='top',pady=15)

    # signUpBtn=ttk.Button(topFrame,text='Sign Up',style='TButton',command=SignUp)
    # signUpBtn.pack(side='top',pady=20)

    signUpBtn=Button(topFrame,command=SignUp,image=signUpBtnImg,borderwidth=0,bg='white',activebackground='white')
    signUpBtn.pack(side='top',pady=15)

    # quitBtn=ttk.Button(topFrame,text='Quit',command=quitBtnFunction,style='TButton')
    # quitBtn.pack(side='bottom',pady=20)
    forgotPasswordBtn=Button(topFrame,command=forgotPasswd,image=forgotPasswordBtnImg,borderwidth=0,bg='white',activebackground='white')
    forgotPasswordBtn.pack(side='top',pady=15)

    quitBtn=Button(topFrame,command=quitBtnFunction,image=quitBtnImg,borderwidth=0,bg='white',activebackground='white')
    quitBtn.pack(side='bottom',pady=15)

    homeWindow.mainloop()

main_function()