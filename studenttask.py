from tkinter import *
from tkinter import font
from tkinter.messagebox import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
# import os
import cv2
import csv
import time
import datetime
import numpy as np

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

studentTaskWindow = Tk()
studentTaskWindow.title("Face Recognition Attendance System")

style=ttk.Style()
style.configure('TButton',font=('times',15,'bold'),borderwidth='4')
style.map('TButton',foreground=[('active','!disabled','black')],background=[('active','gray')])

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