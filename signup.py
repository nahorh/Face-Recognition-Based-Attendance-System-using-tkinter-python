
    def SignUp():
        print('Sign Up invoked')
        signUpWindow = Toplevel(homeWindow)
        signUpWindow.protocol('WM_DELETE_WINDOW', disableButton)
        homeWindow.withdraw()

        signUpWindow.grab_set()

        signUpWindow.title("Face Recognition Attendance System")

        # defining the top frame
        topFrame = tk.Frame(signUpWindow, bg='yellow')
        topFrame.pack(side='top', anchor='n')

        # defining the left frame
        leftFrame = tk.Frame(signUpWindow, bg='white',
                             highlightbackground='black', highlightthickness=2)
        leftFrame.pack(side='top', anchor='center', padx=50, pady=40)

        signUpWindow.configure(background='white')

        window_width = 800
        window_height = 400

        # calculate coordinates of screen and signUpWindow position
        x_Left = int(signUpWindow.winfo_screenwidth()/2 - window_width/2)
        y_Top = int(signUpWindow.winfo_screenheight()/2 - window_height/2)

        # defining the geomtry of signUpWindow and centering it on the screen
        signUpWindow.geometry(
            f'{window_width}x{window_height}+{x_Left}+{y_Top}')

        # disabling the signUpWindow resize option
        signUpWindow.resizable(False, False)

        signUpWindow.grid_rowconfigure(0, weight=1)
        signUpWindow.grid_columnconfigure(0, weight=1)

        # defining the header of the signUpWindow
        message = tk.Label(topFrame, text="Face-Recognition-Based-Attendance-System",
                           bg="white", fg="black", width=100, height=2, font=('calibri', 30, 'bold'))
        message.pack(side='top', anchor='center')

        # creating the signup form
        lbl2 = tk.Label(leftFrame, text="Name", width=12, fg="black",
                        bg="white", height=1, font=('calibri', 15, ' bold '), anchor='w')
        lbl2.grid(row=0, column=0)

        txt2 = tk.Entry(leftFrame, width=25, bg="white",
                        fg="black", font=('calibri', 15, ' bold '))
        txt2.grid(row=0, column=1)

        lbl = tk.Label(leftFrame, text="Roll Id", width=12, height=1,
                       fg="black", bg="white", font=('calibri', 15, ' bold '), anchor='w')
        lbl.grid(row=1, column=0)

        txt = tk.Entry(leftFrame, width=25, bg="white",
                       fg="black", font=('calibri', 15, ' bold '))
        txt.grid(row=1, column=1)

        lbl3 = tk.Label(leftFrame, text='Student Email', bg='white', fg='black', font=(
            'calibri', 15, 'bold'), width=12, anchor='w')
        lbl3.grid(row=2, column=0)

        txt3 = tk.Entry(leftFrame, width=25, bg='white',
                        fg='black', font=('calibri', 15, 'bold'))
        txt3.grid(row=2, column=1)

        lbl4 = tk.Label(leftFrame, width=12, text='Parent Email', font=(
            'calibri', 15, 'bold'), bg='white', fg='black', anchor='w')
        lbl4.grid(row=3, column=0)

        txt4 = tk.Entry(leftFrame, width=25, bg='white',
                        fg='black', font=('calibri', 15, 'bold'))
        txt4.grid(row=3, column=1)

        # defining the signup button
        SignUpBtn = Button(leftFrame, command=TakeImages, image=signUpAndTakeImagesBtnImg,
                           borderwidth=0, bg='white', activebackground='white')
        SignUpBtn.grid(row=4, column=1)

        # defining the back button
        BackBtn = Button(signUpWindow, command=goBack, image=backBtnImg,
                         borderwidth=0, bg='white', activebackground='white')
        BackBtn.pack(side='left', anchor='s')

        # defining the quit button
        quitBtn = Button(signUpWindow, text='Quit', command=quitBtnFunction,
                         image=quitBtnImg, borderwidth=0, bg='white', activebackground='white')
        quitBtn.pack(side='right', anchor='s')

        signUpWindow.mainloop()