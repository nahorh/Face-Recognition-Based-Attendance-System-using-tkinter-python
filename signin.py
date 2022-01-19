cam = VideoStream(src=0)
root_path = os.getcwd()
# sign up window button styles
signUpAndTakeImagesBtnImg = PhotoImage(
    file='buttonImages/signupandtakeimagesButton.png')
# student task window button styles
markAttendanceBtnImg = PhotoImage(
    file='buttonImages/markattendanceButton.png')
# admin task window button styles
sendEmailBtnImg = PhotoImage(file='buttonImages/sendemailButton.png')
trainModelBtnImg = PhotoImage(file='buttonImages/trainmodelButton.png')
viewExcelFileBtnImg = PhotoImage(
    file='buttonImages/viewattendanceButton.png')
viewLatestAttendanceSheetBtnImg = PhotoImage(
    file='buttonImages/viewlatestattendanceButton.png')
initializeBtnImg = PhotoImage(file='buttonImages/createfoldersButton.png')
viewStudentDataFileBtnImg = PhotoImage(
    file='buttonImages/viewstudentdetailsButton.png')
viewAllTrainingImagesBtnImg = PhotoImage(
    file='buttonImages/viewtrainingimagesButton.png')
resetBtnImg = PhotoImage(file='buttonImages/fullresetButton.png')
deleteModelBtnImg = PhotoImage(file='buttonImages/deletemodelButton.png')
deleteAllStudentDataBtnImg = PhotoImage(
    file='buttonImages/deleteallstudentdataButton.png')
deleteAllAttendanceFilesBtnImg = PhotoImage(
    file='buttonImages/deleteallattendancedataButton.png')
def SignIn():
    def disableButton():
        pass
    def verifyCred():
        # this function will verify the credentials entered by the user
        # it will access the StudentDetails.csv file for verification
        # getting the username and password from their respective entry boxes
        uname = unameEntry.get().title()
        unameEntry.delete(0, END)
        passwd = passwdEntry.get()
        passwdEntry.delete(0, END)
        print(uname, passwd)
        # if username=='Admin' and password=='admin'
        # then render the admin/task window template
        # else:
        #   render the student window/task template
    def goBack():
        homeWindow.deiconify()
        signinWindow.destroy()

    signinWindow = Toplevel(homeWindow)
    signinWindow.protocol('WM_DELETE_WINDOW', disableButton)
    homeWindow.withdraw()
    signinWindow.grab_set()
    signinWindow.title("Face Recognition Attendance System")
    signinWindow.configure(background='white')
    window_width = 800
    window_height = 400

    x_Left = int(signinWindow.winfo_screenwidth()/2 - window_width/2)
    y_Top = int(signinWindow.winfo_screenheight()/2 - window_height/2)

    signinWindow.geometry(
        f'{window_width}x{window_height}+{x_Left}+{y_Top}')

    signinWindow.resizable(False, False)

    # giving the heading
    message = Label(signinWindow, text="Face-Recognition-Based-Attendance-System",
                    bg="white", fg="black", width=100, height=2, font=('calibri', 30, 'bold'))
    message.pack(side='top', anchor='center')

    # defining the top frame
    topFrame = Frame(signinWindow, bg='white')
    topFrame.pack(side='top', anchor='n')

    # defining the bottom frame
    bottomFrame = Frame(signinWindow, bg='white')
    bottomFrame.pack(side='top', anchor='n')

    # defining the bottommost frame
    bottommostFrame = Frame(signinWindow, bg='white')
    bottommostFrame.pack(side='top', anchor='n')

    # creating the login form
    unameLabel = Label(topFrame, text='Username', font=(
        'calibri', 15, 'bold'), anchor='w', background='white', width=10)
    unameLabel.pack(side='left', pady=10)

    unameEntry = Entry(topFrame, bg='white', font=(
        'calibri', 15, 'bold'), width=20)
    unameEntry.pack(side='left', pady=10)

    passwdLabel = Label(bottomFrame, text='Password', font=(
        'calibri', 15, 'bold'), anchor='w', background='white', width=10)
    passwdLabel.pack(side='left', pady=10)

    passwdEntry = Entry(bottomFrame, bg='white', font=(
        'calibri', 15, 'bold'), width=20, show='*')
    passwdEntry.pack(side='left', pady=10)

    # defining the login button
    loginBtn = Button(bottommostFrame, command=verifyCred, image=loginBtnImg,
                        borderwidth=0, bg='white', activebackground='white')
    loginBtn.pack(side='left', pady=20)

    # defining the back button
    BackBtn = Button(signinWindow, command=goBack, image=backBtnImg,
                        borderwidth=0, bg='white', activebackground='white')
    BackBtn.pack(side='left', anchor='s')

    # defining the quit button
    quitBtn = Button(signinWindow, command=quitBtnFunction, image=quitBtnImg,
                        borderwidth=0, bg='white', activebackground='white')
    quitBtn.pack(side='right', anchor='s')

    signinWindow.mainloop()