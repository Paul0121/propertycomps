import streamlit as st
import requests
import json

def fetch_property_data(address, api_key):
    base_url = "https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/detail"
    params = {"address": address}
    headers = {
        "accept": "application/json",
        "apikey": api_key
    }
    
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Request error occurred: {req_err}")
    return None

def main():
    st.title("Real Estate Property Data Fetcher")
    api_key = st.text_input("Enter your Attom API Key", type="password")
    address = st.text_input("Enter property address")
    
    if st.button("Fetch Data"):
        if not api_key:
            st.error("API key is required!")
        elif not address:
            st.error("Property address is required!")
        else:
            data = fetch_property_data(address, api_key)
            if data:
                st.json(data)

if __name__ == "__main__":
    main()
