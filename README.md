# Face-Recognition-Based-Attendance-System-using-tkinter-python.

Please make sure that before using this system the machine is connected to the internet as it requires to send emails to users about crednetails and attendance status.

This attendance marking system makes use of machine learning model for face recognition. It makes use of the LBPHFaceRecognizer of opencv which is fast and effcient to run on most of the machines.

The response of the system for recognizing the person in front of the camera depends how the model is trained i.e. you should give your face images from all the angles during capturing images at the time of signup.

The system makes use of the opencv's frontal face detector which is also fast and efficient (may also detect false objects as faces but fit for this application) that returns the coordinates of the faces in the images spontaneously.

Working of the system:
The system is divided in to 3 sections namely: Signup, Signin and Forgot Password.

Signup section:
From the name itself, one can infer that one has to fill the details for registering in the system.
After clicking on the signup and take images button, the camera window opens up and start detecting faces in front of the camera.
If faces are detected, then it prints 'press c to capture image' and when the user presses c the image is captured and stored on the local disk.
There is also an option for quitting the process forcefully by pressing 'q' key.
If there are no images taken and the user quits from taking images, then there is a prompt of no images taken by user and thus signup process discarded.
If there are some images taken, then those images are stored on the local disk, then trained for future recognition of the user and also a welcome email is sent to the user consisting of the sign in credentials for future attendance marking.
If the user is existing in the system, then the images taken are retrained for that user and a prompt is shown of user already existing and no email is sent to that user as the user is not new.

Signin section:
This is the common login interface for both, the user and the admin.
The admin has been alloted separate credentials for login and each user signned up on the system has their own login credentials.
When the user enters the login credentials and clicks on the sign in button, the credentials are checked whether they are of admin or of user.
If the creds are of admin then the admin window is rendered on the screen which consists of various options listed below:
  a) Send email
  b) Train model
  c) View attendance
  d) View latest attendance
  e) Create folders
  f) Attendance
  g) View student details
  h) View training images
  i) Full reset
  j) Delete model
  k) Delete all student data
  l) Delete all attendance data
  m) Go back
  n) Quit
If the creds are of student then the student window is rendered on the screen which consists of options listed below:
  a) Attendance
  b) Go back
  c) Quit

Forgot password section:
In case the user forgots the login credentials, then they can be retrived using this functionality of the system.
The user needs to enter the name and email that was provided during the time of signup.
Then these details are verified from the student data file and if correct, an email is sent to that user consisting of the creds of that user.

In this way this attendance system has been designed for ease in marking and viewing attendance of particular class.

This application has a setup exe file that can be installed on windows machines.

So running this application will not require python as a prerequisite on any machine after installing the exe file.

#NOTE:
Before running the code do the following:
1) create a gmail account for the attendance system that will send emails to the users.
2) go to account setup and search for access for less secure apps.
3) enable access to less secure apps.
4) the account is now setup to allow python login to the account.
5) now open smtpcred.txt file in project folder.
6) type the gmail account name and password seperated by a comma.
7) save the file.
8) now, the code is able to run with all functionalities.

#If code doesn't run
create a virtual environment
install all dependies
install opencv-contrib-python
then run the code in virtual environment
