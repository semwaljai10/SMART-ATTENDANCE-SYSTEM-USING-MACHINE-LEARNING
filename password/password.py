import pandas as pd
import hashlib
import os
import streamlit as st

# Function to hash the password
def hash_password(password):
    # Use SHA-256 hashing algorithm
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

# Function to store username and hashed password in CSV file
def store_user_in_csv(username, hashed_password):
    file_name = 'C:/Users/324ja/OneDrive/Desktop/Prenita/password/teachers_database.csv'
    
    # Check if the file exists
    if os.path.exists(file_name):
        # Load the existing CSV file
        df = pd.read_csv(file_name)
    else:
        # Create a new dataframe if the file does not exist
        df = pd.DataFrame(columns=['Username', 'PASSWORD'])
    
    # Create a new DataFrame for the new entry with the column name 'PASSWORD'
    new_entry = pd.DataFrame([[username, hashed_password]], columns=['Username', 'PASSWORD'])
    
    # Concatenate the new entry with the existing DataFrame
    df = pd.concat([df, new_entry], ignore_index=True)
    
    # Save the updated dataframe back to the CSV file
    df.to_csv(file_name, index=False)

# Streamlit app
def main():
    st.title("Teacher's Database")

    # Input username and password
    username = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:", type="password")

    # If the form is submitted
    if st.button("Submit"):
        if username and password:
            # Hash the password
            hashed_password = hash_password(password)
            
            # Store username and hashed password in CSV
            store_user_in_csv(username, hashed_password)
            
            st.success(f"Username and hashed password for {username} stored successfully in 'teachers_database.csv'.")
        else:
            st.warning("Please enter both username and password.")

# Run the app
if __name__ == '__main__':
    main()
