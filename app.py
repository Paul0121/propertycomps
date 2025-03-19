import streamlit as st
import pandas as pd
import requests

# RentCast API Key (Replace with an environment variable in production)
API_KEY = "4c51677e91764ccb8209425467819153"

def get_comps(address):
    """Fetch comparable properties from RentCast API"""
    api_url = "https://api.rentcast.io/v1/properties"
    headers = {"X-Api-Key": API_KEY}
    params = {"address": address}  # RentCast requires the 'address' parameter

    try:
        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract comps from API response (adjust based on RentCast response format)
        return data.get("comparable_properties", [])  
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching property data: {e}")
        return []

# Streamlit UI
st.title("🏡 AI Real Estate Comps & Valuation")
address = st.text_input("📍 Enter Property Address:")

if st.button("🔍 Run Comps"):
    comps = get_comps(address)

    if comps:
        st.subheader("📊 Comparable Properties")
        st.write(pd.DataFrame(comps))  # Display comps in a table
    else:
        st.error("⚠ No comparable properties found. Please try another address.")
