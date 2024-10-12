import streamlit as st
import cv2
import pickle
import numpy as np
import os
import pandas as pd
import hashlib

# Function to hash the password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load the CSV file for authentication
csv_path = 'C:/Users/324ja/OneDrive/Desktop/Prenita/password/teachers_database.csv'

# Ensure the CSV file loads properly
try:
    teachers_data = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error(f"File not found: {csv_path}")
    st.stop()

# Strip whitespaces and handle potential issues in the data
teachers_data['Username'] = teachers_data['Username'].str.strip()
teachers_data['PASSWORD'] = teachers_data['PASSWORD'].str.strip()

# Function for user authentication
def authenticate(username, password):
    username = username.strip()
    password_hash = hash_password(password.strip())  # Hash the entered password

    user = teachers_data[teachers_data['Username'].str.lower() == username.lower()]
    if not user.empty and user.iloc[0]['PASSWORD'] == password_hash:
        return True
    return False

# Function to capture and save faces
def capture_faces(name):
    faces_data = []
    i = 0

    # Initialize video capture and check if the camera is accessible
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        st.error("Unable to access the camera.")
        return

    # Load the Haar Cascade for face detection
    facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Set up a placeholder for displaying frames
    stframe = st.empty()

    # Capture 200 images instead of 100
    while len(faces_data) < 200:
        ret, frame = video.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            crop_img = frame[y:y+h, x:x+w, :]
            resized_img = cv2.resize(crop_img, (50, 50))
            if i % 10 == 0:
                faces_data.append(resized_img)
            i += 1
            # Draw a rectangle and display the face count on the frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)
            cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)

        # Display the frame in the Streamlit app
        stframe.image(frame, channels="BGR")

        # Stop if 200 images are captured
        if len(faces_data) == 200:
            break

    video.release()
    cv2.destroyAllWindows()

    if len(faces_data) == 0:
        return

    # Convert face data to numpy array and reshape it
    faces_data = np.asarray(faces_data)
    faces_data = faces_data.reshape(200, -1)  # Update to reshape for 200 images

    # Save the name and face data using pickle
    if 'names.pkl' not in os.listdir('data/'):
        names = [name] * 200  # Update for 200 images
        with open('data/names.pkl', 'wb') as f:
            pickle.dump(names, f)
    else:
        with open('data/names.pkl', 'rb') as f:
            names = pickle.load(f)
        names = names + [name] * 200  # Update for 200 images
        with open('data/names.pkl', 'wb') as f:
            pickle.dump(names, f)

    if 'faces_data.pkl' not in os.listdir('data/'):
        with open('data/faces_data.pkl', 'wb') as f:
            pickle.dump(faces_data, f)
    else:
        with open('data/faces_data.pkl', 'rb') as f:
            faces = pickle.load(f)
        faces = np.append(faces, faces_data, axis=0)
        with open('data/faces_data.pkl', 'wb') as f:
            pickle.dump(faces, f)

    st.success(f"Data captured for {name} and saved successfully.")

# Authentication section
st.title("Teacher Login")

# Session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

username = st.text_input("Username")
password = st.text_input("Password", type="password")

login_button = st.button("Login")

if login_button and not st.session_state.logged_in:
    if authenticate(username, password):
        st.session_state.logged_in = True
        st.success("Login successful!")
    else:
        st.error("Invalid username or password.")

if st.session_state.logged_in:
    # Set up directories for storing data
    if not os.path.exists('data'):
        os.makedirs('data')

    st.title("Face Data Capture")

    # Input field for user's name
    name = st.text_input("Enter your name:")

    # Button to start capturing
    start_capture = st.button("Start Capture")
    
    add_another_face = st.button("Add Another Face")

    if start_capture and name != "":
        capture_faces(name)
    if add_another_face:
        st.rerun()
    elif start_capture and name == "":
        st.warning("Please enter your name to start capturing.")
