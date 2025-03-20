import streamlit as st
import requests
import json

# Oxylabs API Credentials
USERNAME = "dylan_aa8eN"
PASSWORD = "DylanPogi1o+"

# Function to fetch property data using Oxylabs
def fetch_property_data(target_url):
    url = "https://realtime.oxylabs.io/v1/queries"
    headers = {"Content-Type": "application/json"}
    data = {
        "source": "zillow",  # Using Zillow as the data source
        "url": target_url,
        "parse": True  # Enable parsing for structured output
    }
    
    response = requests.post(url, auth=(USERNAME, PASSWORD), headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching property data: {response.status_code} {response.reason}")
        st.write(response.text)  # Debugging output
        return None

# Streamlit UI
st.title("Real Estate Valuation Tool")

full_address = st.text_input("Enter Zillow Property URL (e.g., https://www.zillow.com/...)")
repair_costs = st.number_input("Estimated Repair Costs", min_value=0, step=1000)

if st.button("Analyze Property"):
    if full_address.startswith("https://www.zillow.com/"):  # Validate URL
        property_data = fetch_property_data(full_address)
        if property_data:
            st.subheader("Scraped Property Data")
            st.json(property_data)  # Display raw scraped data
        else:
            st.error("Failed to retrieve property data.")
    else:
        st.error("Please enter a valid Zillow property URL.")
