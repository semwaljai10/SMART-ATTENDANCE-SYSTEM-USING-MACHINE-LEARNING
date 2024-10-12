# SMART-ATTENDANCE-SYSTEM-USING-MACHINE-LEARNING
A smart attendance system using machine learning automates attendance tracking by recognizing faces or voice patterns, ensuring accuracy and reducing manual work. It utilizes ML algorithms to identify individuals, mark their presence, and store data securely. This system improves efficiency in educational or workplace environments.

Overview :


The Smart Attendance System leverages machine learning to automate and streamline the process of attendance tracking. This system can recognize individuals through facial recognition or voice pattern analysis and automatically mark their attendance, reducing manual errors and improving efficiency in educational institutions, workplaces, and events.

Why This Project Is Useful?


Manual attendance tracking can be time-consuming and prone to errors. The Smart Attendance System:

1.Ensures high accuracy using machine learning algorithms.

2.Reduces the need for manual intervention, improving productivity.

3.Provides real-time attendance reports and insights.

4.Can be adapted for various settings such as schools, universities, and corporate offices.


Features:


Facial Recognition/Voice Pattern Analysis: Uses machine learning to recognize and identify individuals.
Automated Attendance Logging: Automatically records attendance upon recognition.
Real-Time Data Storage: Attendance is stored securely in a database for easy access and reporting.
User-Friendly Interface: Simple interface for users to register, log in, and view attendance.
Notifications and Alerts: Option for sending alerts for absentees or irregular attendance patterns.


Models Used:

1.  Face Recognition Model

    Model Type: Convolutional Neural Networks (CNN)

    Pretrained Models: OpenCV’s Haar Cascade or Dlib with a pretrained model for face detection, followed by FaceNet or DeepFace for facial recognition.

    Purpose: Detect and recognize faces in real time for marking attendance.
    
2.  Attendance Prediction/Analysis Model

  Model Type: Decision Trees or Random Forest Classifier
  
  Purpose: Analyzes attendance trends, predicts irregularities, and helps administrators get insights into absenteeism or attendance patterns.

3.  Data Preprocessing Models

  Purpose: Models such as Principal Component Analysis (PCA) are used to reduce the dimensionality of the face embeddings for faster recognition.  


"This model includes two sub folders: `password` and `attendance`. The `password` folder contains three files: `signup.py`, `signin.py`, and `db.csv`, which is used to store the teachers' credentials. The `attendance` folder contains the `attendance.csv` file, which holds the attendance data for the corresponding date."


