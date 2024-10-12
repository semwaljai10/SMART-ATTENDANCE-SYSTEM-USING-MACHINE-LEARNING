import cv2
import streamlit as st
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pickle
import time
import csv
import os
from datetime import datetime
from win32com.client import Dispatch
import pandas as pd

# Load KNN classifier and face data
with open('data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

# Initialize KNN Classifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

# Initialize face detector (Haarcascade)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# Initialize voice assistant
def speak(str1):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

# Set up Streamlit UI
st.title("Real-Time Face Recognition and Attendance System")

# Sidebar to display attendance CSV files
st.sidebar.title("Attendance Files")

# Get the list of CSV files in the 'Attendance' directory
attendance_files = [f for f in os.listdir("Attendance") if f.endswith('.csv')]

# Display the files in the sidebar
selected_file = st.sidebar.selectbox("Select a file to view", attendance_files)

# Show the selected CSV file content
if selected_file:
    st.sidebar.write(f"Displaying content of: {selected_file}")
    file_path = os.path.join("Attendance", selected_file)
    df = pd.read_csv(file_path)
    st.sidebar.dataframe(df)

# Option to start/stop video feed
run = st.checkbox('Start Webcam')

# Initialize session state for attendance button and attendance taken flag
if 'take_attendance' not in st.session_state:
    st.session_state['take_attendance'] = False

if 'end_session' not in st.session_state:
    st.session_state['end_session'] = False

# Add a flag to check if attendance has already been taken for the session
if 'attendance_taken' not in st.session_state:
    st.session_state['attendance_taken'] = False

# Button to trigger attendance
if st.button('Take Attendance'):
    if st.session_state['attendance_taken']:
        speak("ATTENDANCE ALREADY TAKEN")
    else:
        st.session_state['take_attendance'] = True

if st.button('End Session'):
    st.session_state['end_session'] = True

# Function to process video and detect faces
def process_video():
    # Open a video capture object for the webcam
    video = cv2.VideoCapture(0)
    COL_NAMES = ['NAME', 'TIME', 'DAY']

    # Create a placeholder in Streamlit for the video feed
    video_placeholder = st.empty()

    while run:
        ret, frame = video.read()  # Read video frames from webcam
        if not ret:
            st.write("Failed to capture video")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale
        faces = facedetect.detectMultiScale(gray, 1.3, 5)  # Detect faces

        for (x, y, w, h) in faces:
            # Extract the region of interest (ROI) containing the face
            crop_img = frame[y:y + h, x:x + w, :]
            resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
            output = knn.predict(resized_img)  # Predict the face using KNN classifier

            ts = time.time()
            date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
            timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
            day_of_week = datetime.fromtimestamp(ts).strftime("%A")  # Get the day of the week
            exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")

            # Display prediction on the frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, str(output[0]), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            attendance = [str(output[0]), str(timestamp), str(day_of_week)]

            # Save attendance if button is clicked
            if st.session_state['take_attendance']:
                if not st.session_state['attendance_taken']:  # Check if attendance is already taken
                    speak("Attendance Taken")
                    if exist:
                        with open("Attendance/Attendance_" + date + ".csv", "a") as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(attendance)
                    else:
                        with open("Attendance/Attendance_" + date + ".csv", "a") as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(COL_NAMES)
                            writer.writerow(attendance)
                    st.session_state['attendance_taken'] = True  # Set the flag after attendance is taken
                else:
                    speak("ATTENDANCE ALREADY TAKEN")
                st.session_state['take_attendance'] = False  # Reset the state

        if st.session_state['end_session']:
            st.session_state['end_session'] = False
            break

        # Convert frame to RGB for display in Streamlit
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)

    # Release the video feed
    video.release()

# Start processing if webcam is enabled
if run:
    process_video()
else:
    st.write("Webcam feed stopped.")
