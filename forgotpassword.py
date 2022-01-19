def forgotPasswd():
    # if the existing user forgots the login credentials, then they can be recovered
    # by entering the basic details of the user

    forgotPasswordWindow = Toplevel(homeWindow)
    forgotPasswordWindow.protocol('WM_DELETE_WINDOW', disableButton)
    homeWindow.withdraw()
    forgotPasswordWindow.grab_set()
    forgotPasswordWindow.configure(background='white')

    window_width = 800
    window_height = 400

    x_Left = int(forgotPasswordWindow.winfo_screenwidth() /
                    2 - window_width/2)
    y_Top = int(forgotPasswordWindow.winfo_screenheight() /
                2 - window_height/2)

    # setting the geometry of the homeWindow and align it to the center
    forgotPasswordWindow.geometry(
        f'{window_width}x{window_height}+{x_Left}+{y_Top}')

    # disable homeWindow resizing option
    forgotPasswordWindow.resizable(False, False)

    # giving the heading
    message = Label(forgotPasswordWindow, text="Face-Recognition-Based-Attendance-System",
                    bg="white", fg="black", width=100, height=2, font=('calibri', 30, 'bold'))
    message.pack(side='top', anchor='center')

    # defining the top frame
    topFrame = Frame(forgotPasswordWindow, bg='white')
    topFrame.pack(side='top', anchor='center')

    # defining the bottom frame
    bottomFrame = Frame(forgotPasswordWindow, bg='white')
    bottomFrame.pack(side='top', anchor='center')

    # defining name entry
    unameLabel = Label(topFrame, text='Name', bg='white', fg='black', height=1, font=(
        'calibri', 14, 'bold'), width=10, anchor='w')
    unameLabel.pack(side='left', anchor='center')

    unameEntry = Entry(topFrame, bg='white', fg='black',
                        width=20, font=('calibri', 14, 'bold'))
    unameEntry.pack(side='left', anchor='center')

    # defining email entry field
    uemailLabel = Label(bottomFrame, text='Email', bg='white', fg='black', height=1, font=(
        'calibri', 14, 'bold'), width=10, anchor='w')
    uemailLabel.pack(side='left', anchor='center')

    uemailLabelEntry = Entry(
        bottomFrame, bg='white', fg='black', width=20, font=('calibri', 14, 'bold'))
    uemailLabelEntry.pack(side='left', anchor='center')

    # defining the submit button
    submitBtn = Button(forgotPasswordWindow, command=sendCreds,
                        image=submitBtnImg, borderwidth=0, bg='white', activebackground='white')
    submitBtn.pack(side='top', pady=20, anchor='center')

    # defining the back button
    backBtn = Button(forgotPasswordWindow, command=goBack, image=backBtnImg,
                        borderwidth=0, bg='white', activebackground='white')
    backBtn.pack(side='left', anchor='s')

    # defining the quit button
    quitBtn = Button(forgotPasswordWindow, command=quitBtnFunction,
                        image=quitBtnImg, borderwidth=0, bg='white', activebackground='white')
    quitBtn.pack(side='right', anchor='s')

    forgotPasswordWindow.mainloop()