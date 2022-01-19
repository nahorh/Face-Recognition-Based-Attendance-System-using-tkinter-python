else:
    df = pd.read_csv(os.path.join(
        root_path, 'StudentDetails/StudentDetails.csv'))
    df = pd.DataFrame(df)
    ids = df['Id']
    names = df['Name']
    for i in range(len(ids)):
        id = str(ids[i])
        name = str(names[i])
        if uname == name and passwd == id:
            # render the studenttask.py
            def goBack():
                signinWindow.deiconify()
                studentTaskWindow.destroy()

            def markAttendance():
                # this function is same as the function present in the admin window
                # just it is associated with the student window and its controls so
                # defined separately here
                studentTaskWindow.attributes('-disabled', True)
                try:
                    cam.start()
                    pass
                except:
                    messagebox.showerror(
                        'Camera access error', 'Please check that camera privacy settings have enabled camera access for applications')
                    studentTaskWindow.attributes(
                        '-disabled', False)
                    return
                try:
                    recognizer = cv2.face.LBPHFaceRecognizer_create()
                except:
                    messagebox.showerror(
                        'Recognizer object creation error', 'Unable to create recognizer object for loading trained model')
                    studentTaskWindow.attributes(
                        '-disabled', False)
                    return
                try:
                    recognizer.read("Model/model.yml")
                except:
                    messagebox.showerror(
                        'Model not readable', 'The trained model is either deleted from the system or unable to access. Please try again by trainig the model again.')
                    studentTaskWindow.attributes(
                        '-disabled', False)
                    return
                harcascadePath = os.path.join(
                    root_path, "haarcascade_frontalface_default.xml")
                try:
                    faceCascade = cv2.CascadeClassifier(
                        harcascadePath)
                except:
                    messagebox.showerror(
                        'Haar XML file not found', 'Please check that the "haarcascade_frontalface_default.xml" file is present at the location of exe file')
                    studentTaskWindow.attributes(
                        '-disabled', False)
                    return
                df = pd.read_csv(
                    "StudentDetails/StudentDetails.csv")
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ['Id', 'Name', 'Date',
                                'Time', 'StudentEmail', 'ParentEmail']
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    try:
                        faces = faceCascade.detectMultiScale(
                            gray, 1.3, 5)
                    except:
                        messagebox.showerror(
                            'Haar XML file not found', 'Please check that the "haarcascade_frontalface_default.xml" file is present at the location of exe file')
                        studentTaskWindow.attributes(
                            '-disabled', False)
                        return
                    for(x, y, w, h) in faces:
                        cv2.rectangle(
                            im, (x, y), (x+w, y+h), (225, 0, 0), 2)
                        Id, conf = recognizer.predict(
                            gray[y:y+h, x:x+w])
                        if(conf < 50):
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(
                                ts).strftime('%Y-%m-%d')
                            timeStamp = datetime.datetime.fromtimestamp(
                                ts).strftime('%H:%M:%S')
                            aa = df.loc[df['Id'] ==
                                        Id]['Name'].values
                            stuEmail = df.loc[df['Id'] ==
                                                Id]['StudentEmail'].values
                            print(stuEmail)
                            parEmail = df.loc[df['Id'] ==
                                                Id]['ParentEmail'].values
                            print(parEmail)
                            tt = str(Id)+"-"+aa
                            attendance.loc[len(attendance)] = [
                                Id, aa, date, timeStamp, stuEmail, parEmail]
                        else:
                            Id = 'Unknown'
                            tt = str(Id)
                        cv2.putText(im, str(tt), (x, y+h),
                                    font, 1, (255, 255, 255), 2)
                    cv2.putText(im, 'Press "q" to close camera', (50, 50),
                                cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 2)
                    attendance = attendance.drop_duplicates(
                        subset=['Id'], keep='first')
                    cv2.imshow('im', im)
                    cv2.moveWindow('im', 15, 15)
                    key = cv2.waitKey(1) & 0xFF
                    if (key == ord('q')):
                        cv2.destroyAllWindows()
                        messagebox.showinfo(
                            'Attendance Marked', 'Attendance of the recognized students has been marked successfully')
                        studentTaskWindow.attributes(
                            '-disabled', False)
                        break
                ts = time.time()
                date = datetime.datetime.fromtimestamp(
                    ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(
                    ts).strftime('%H:%M:%S')
                Hour, Minute, Second = timeStamp.split(":")
                fileName = "Attendance/Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
                attendance.to_csv(fileName, index=False)

            studentTaskWindow = Toplevel(signinWindow)
            studentTaskWindow.protocol(
                'WM_DELETE_WINDOW', disableButton)
            signinWindow.withdraw()
            studentTaskWindow.grab_set()

            studentTaskWindow.configure(background='white')

            studentTaskWindow_width = 800
            studentTaskWindow_height = 400

            x_Left = int(studentTaskWindow.winfo_screenwidth(
            )/2 - studentTaskWindow_width/2)
            y_Top = int(studentTaskWindow.winfo_screenheight(
            )/2 - studentTaskWindow_height/2)

            studentTaskWindow.geometry(
                f'{studentTaskWindow_width}x{studentTaskWindow_height}+{x_Left}+{y_Top}')

            studentTaskWindow.resizable(False, False)

            # giving the heading
            message = Label(studentTaskWindow, text="Face-Recognition-Based-Attendance-System",
                            bg="white", fg="black", width=100, height=2, font=('calibri', 30, 'bold'))
            message.pack(side='top', anchor='center')

            LoginLabel = ttk.Label(studentTaskWindow, text='Logged in as student',
                                    background='white', foreground='black', font=('calibri', 15, 'bold'))
            LoginLabel.pack(side='top', pady=0)

            markAttendanceBtn = Button(studentTaskWindow, command=markAttendance,
                                        image=markAttendanceBtnImg, borderwidth=0, bg='white', activebackground='white')
            markAttendanceBtn.pack(side='top', pady=80)

            # defining the back button
            BackBtn = Button(studentTaskWindow, command=goBack, image=backBtnImg,
                                borderwidth=0, bg='white', activebackground='white')
            BackBtn.pack(side='left', anchor='s', pady=5)

            # defining the quit button
            quitBtn = Button(studentTaskWindow, command=quitBtnFunction,
                                image=quitBtnImg, borderwidth=0, bg='white', activebackground='white')
            quitBtn.pack(side='right', anchor='s', pady=5)

            studentTaskWindow.mainloop()
            print(True)
    else:
        messagebox.showerror(
            'Wrong Credentials', 'Please enter correct credentials')
        print(False)
        pass
