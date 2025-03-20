import streamlit as st
import requests
import pandas as pd
import json

# Oxylabs API Credentials
USERNAME = "dylan_aa8eN"
PASSWORD = "DylanPogi1o+"

# Function to fetch property data using Oxylabs
def fetch_property_data(target_url):
    url = "https://realtime.oxylabs.io/v1/queries"
    headers = {"Content-Type": "application/json"}
    data = {
        "source": "zillow",  # Try specifying Zillow as the source
        "url": target_url
    }
    
    response = requests.post(url, auth=(USERNAME, PASSWORD), headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching property data: {response.status_code} {response.reason}")
        st.write(response.text)  # Debugging output
        return None

st.title("Real Estate Valuation Tool")

full_address = st.text_input("Enter Zillow Property URL")  # Ensure URL format
repair_costs = st.number_input("Estimated Repair Costs", min_value=0, step=1000)

if st.button("Analyze Property"):
    if full_address.startswith("http"):  # Validate URL
        property_data = fetch_property_data(full_address)
        if property_data:
            st.subheader("Scraped Property Data")
            st.json(property_data)  # Display raw scraped data for debugging
        else:
            st.error("Failed to retrieve property data.")
    else:
        st.error("Please enter a valid property URL (e.g., https://www.zillow.com/...).")
