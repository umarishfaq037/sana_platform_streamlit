import streamlit as st
import requests
import json

# Define Flask API URL
FLASK_API_URL = "http://3.88.112.156:5000/finance_chat"  # Update with the correct API URL if hosted remotely

# Streamlit UI
st.title("Financial Insights Chatbot")
st.header("Ask about global stock market trends, top performers, and more!")

# Define the user input form
with st.form(key='finance_form'):
    user_message = st.text_area("Enter your financial query:")
    model_type = st.selectbox("Choose the model:", ["deepseek", "gpt", "gemini"])
    submit_button = st.form_submit_button(label="Submit")

# When the user submits a question
if submit_button:
    if not user_message:
        st.error("Please enter a message to proceed.")
    else:
        try:
            # Prepare the request payload
            payload = {
                "message": user_message,
                "model_type": model_type
            }
            
            # Make POST request to Flask API
            response = requests.post(FLASK_API_URL, json=payload)
            
            if response.status_code == 200:
                response_data = response.json()
                st.subheader("Response from the Model:")
                st.write(response_data.get("response"))
            else:
                st.error(f"Error from API: {response.json().get('error')}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
