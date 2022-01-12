from enum import auto
import tkinter as tk
from tkinter import messagebox
import smtplib
from tkinter import Frame, Message, PhotoImage, Text
from tkinter.constants import CENTER, LEFT, N, TOP
import cv2
import os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
from email.message import EmailMessage
from tkinter.ttk import *



def main_function():
    # getting the root path of the application
    root_path=os.getcwd()

    # creating an instance of tkinter signUpWindow
    signUpWindow = tk.Tk()
    signUpWindow.title("Face Recognition Attendance System")

    # signUpWindow.overrideredirect(True)
    # signUpWindow.attributes('-topmost',True)
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
            else:
                with open('StudentDetails\\StudentDetails.csv', 'a+') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
                csvFile.close()
            
        elif str(Id)=='' or str(name)=='' or not is_number(Id) or not name.isalpha():
            tk.messagebox.showerror('Value Error','Please enter correct details')

    # defining the style for the buttons
    # style=Style()
    # style.configure('TButton',font=('times',15,'bold'),borderwidth='4')
    # style.map('TButton',foreground=[('active','!disabled','black')],background=[('active','gray')])

    # defining the top frame
    topFrame=tk.Frame(signUpWindow,bg='yellow')
    topFrame.pack(side='top',anchor='n')

    # defining the left frame
    leftFrame=tk.Frame(signUpWindow,bg='white',highlightbackground='black',highlightthickness=2)
    leftFrame.pack(side='top',anchor='center',padx=50,pady=50)

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
    message = tk.Label(topFrame, text="Face-Recognition-Based-Attendance-System", bg="white",fg="black", width=100, height=2, font=('times', 30, 'bold'))
    message.pack(side='top',anchor='center')

    # creating the signup form
    lbl = tk.Label(leftFrame, text="Roll Id", width=12, height=1,fg="black", bg="white", font=('times', 15, ' bold '),anchor='w')
    lbl.grid(row=1,column=0)

    txt = tk.Entry(leftFrame, width=25, bg="white",fg="black", font=('times', 15, ' bold '))
    txt.grid(row=1,column=1)

    lbl2 = tk.Label(leftFrame, text="Name", width=12, fg="black",bg="white", height=1, font=('times', 15, ' bold '),anchor='w')
    lbl2.grid(row=0,column=0)

    txt2 = tk.Entry(leftFrame, width=25, bg="white",fg="black", font=('times', 15, ' bold '))
    txt2.grid(row=0,column=1)

    lbl3=tk.Label(leftFrame,text='Student Email',bg='white',fg='black',font=('times',15,'bold'),width=12,anchor='w')
    lbl3.grid(row=2,column=0)

    txt3=tk.Entry(leftFrame,width=25,bg='white',fg='black',font=('times',15,'bold'))
    txt3.grid(row=2,column=1)

    lbl4=tk.Label(leftFrame,width=12,text='Parent Email',font=('times',15,'bold'),bg='white',fg='black',anchor='w')
    lbl4.grid(row=3,column=0)

    txt4=tk.Entry(leftFrame,width=25,bg='white',fg='black',font=('times',15,'bold'))
    txt4.grid(row=3,column=1)






    # defining the signup button
    SignUpBtn=ttk.Button(leftFrame,text='SignUp & Take Images',style='TButton',command=TakeImages)
    SignUpBtn.grid(row=4,column=1)

    # defining the back button
    BackBtn=ttk.Button(signUpWindow,text='Back',style='TButton',command=goBack)
    BackBtn.pack(side='left',anchor='s')

    # defining the quit button
    quitBtn=ttk.Button(signUpWindow,text='Quit',command=lambda:exit(),style='TButton')
    quitBtn.pack(side='right',anchor='s')

    signUpWindow.mainloop()

# main_function()