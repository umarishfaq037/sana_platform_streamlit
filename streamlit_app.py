import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit UI
st.title("Deepseek R1 Finance Model")

# User input
query = st.text_input("Enter your query (e.g., 'Top performing stocks in Saudi Arabia'):")

if st.button("Submit"):
    # Call Lambda function via API Gateway
    response = requests.post(
        'https://your-api-gateway-url/query',
        json={'query': query}
    )
    result = pd.read_json(response.json()['body'])
    
    # Display results in charts
    if not result.empty:
        if "compare" in query.lower():
            # Line chart for comparison
            st.write("Performance Comparison:")
            plt.figure(figsize=(10, 6))
            plt.plot(result['stock'], result['performance'], marker='o')
            plt.xlabel('Stocks')
            plt.ylabel('Performance (%)')
            plt.title('Top 5 Banks vs Index')
            st.pyplot(plt)
        else:
            # Bar chart for top stocks
            st.write("Top Stocks:")
            plt.figure(figsize=(10, 6))
            plt.bar(result['stock'], result['performance' if 'performing' in query.lower() else 'dividend_yield'])
            plt.xlabel('Stocks')
            plt.ylabel('Performance (%)' if 'performing' in query.lower() else 'Dividend Yield (%)')
            plt.title('Top Performing Stocks' if 'performing' in query.lower() else 'Top Dividend Paying Stocks')
            st.pyplot(plt)
    else:
        st.write("No results found for your query.")