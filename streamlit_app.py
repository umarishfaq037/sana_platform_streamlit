import streamlit as st
import requests
import base64
from PIL import Image
import io

# ✅ Move this line to the top before any other Streamlit commands
st.set_page_config(page_title="Stock Insights", layout="wide")

# Flask API URL
FLASK_API_URL = "http://3.88.112.156:5000/generate"  # Replace with your EC2 IP or domain

# Streamlit UI
st.title("AI-Powered Stock Insights")

# User query input
query = st.text_input("Ask R1 about stocks:", 
                      placeholder="e.g., What are the top performing stocks in Saudi Arabia?")

if st.button("Get Insights"):
    if query:
        with st.spinner("Fetching insights..."):
            # Send request to Flask API
            response = requests.post(FLASK_API_URL, json={"prompt": query})
            data = response.json()

            # Display text response
            if "query" in data:
                st.subheader(f"Response: {data['query'].capitalize()}")
                st.success(f"Here are the insights for {data['query']}.")

            if "response" in data:
                st.subheader("AI Response")
                st.write(data["response"])

            # Display Chart
            if "chart" in data:
                chart_base64 = data["chart"]
                image_data = base64.b64decode(chart_base64)
                image = Image.open(io.BytesIO(image_data))
                st.image(image, caption="Stock Performance Chart", use_column_width=True)

    else:
        st.warning("Please enter a query.")