import pandas as pd
import hashlib
import streamlit as st

# Function to hash the password
def hash_password(password):
    # Use SHA-256 hashing algorithm
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

# Function to check login credentials
def verify_login(username, password):
    file_name = 'C:/Users/324ja/OneDrive/Desktop/Prenita/password/teachers_database.csv'
    
    # Check if the CSV file exists
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        st.error(f"The file '{file_name}' does not exist. Please create a user first.")
        return False
    
    # Check if the username exists in the DataFrame
    if username in df['Username'].values:
        # Retrieve the corresponding hashed password from the DataFrame
        stored_hashed_password = df.loc[df['Username'] == username, 'PASSWORD'].values[0]
        
        # Hash the entered password and compare with the stored hash
        if hash_password(password) == stored_hashed_password:
            return True
        else:
            return False
    else:
        return False

# Streamlit app for login
def main():
    st.title("Login Page")
    
    # Input username and password
    username = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:", type="password")

    # Login button
    if st.button("Login"):
        if username and password:
            if verify_login(username, password):
                st.success("Login successful!")
            else:
                st.error("Incorrect username or password.")
        else:
            st.warning("Please enter both username and password.")

# Run the Streamlit app
if __name__ == '__main__':
    main()
