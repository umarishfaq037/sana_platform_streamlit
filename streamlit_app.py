import streamlit as st
import requests
import json
from PIL import Image
import io
import base64

# Define Flask API URL
FLASK_API_URL = "http://3.215.242.69:5000/finance_chat"  # Update with the correct API URL if hosted remotely

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
                
                # Display the response text
                st.subheader("Response from the Model:")
                st.write(response_data.get("response"))
                
                # Check if a chart is included in the response
                chart_data = response_data.get("chart")
                if chart_data:
                    # Decode the base64 chart image and display it
                    chart_image = Image.open(io.BytesIO(base64.b64decode(chart_data.split(',')[1])))
                    st.image(chart_image, caption="Stock Chart")
            else:
                st.error(f"Error from API: {response.json().get('error')}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
