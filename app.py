import streamlit as st
import requests
import json
import re
import pandas as pd

# Oxylabs API Credentials
USERNAME = "dylan_aa8eN"
PASSWORD = "DylanPogi1o+"

# Function to validate Zillow URL
def is_valid_zillow_url(url):
    pattern = r"^https://www\.zillow\.com/homedetails/.*"
    return re.match(pattern, url)

# Function to fetch property data using Oxylabs
def fetch_property_data(target_url):
    url = "https://realtime.oxylabs.io/v1/queries"
    headers = {"Content-Type": "application/json"}
    data = {
        "source": "zillow",  # Use Zillow-specific scraper
        "url": target_url
    }
    
    response = requests.post(url, auth=(USERNAME, PASSWORD), headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching property data: {response.status_code} {response.reason}")
        st.write(response.text)  # Debugging output
        return None

# Function to fetch comparable sales data
def fetch_comps(property_data):
    try:
        zpid = property_data["zpid"]  # Extract Zillow Property ID
    except KeyError:
        st.error("Failed to extract property ID from Zillow data.")
        return None
    
    url = "https://realtime.oxylabs.io/v1/queries"
    headers = {"Content-Type": "application/json"}
    data = {
        "source": "zillow",  # Use Zillow-specific scraper
        "url": f"https://www.zillow.com/homes/comps/{zpid}_zpid/"
    }
    
    response = requests.post(url, auth=(USERNAME, PASSWORD), headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching comps: {response.status_code} {response.reason}")
        st.write(response.text)  # Debugging output
        return None

# Function to calculate ARV
def calculate_arv(comps):
    if not comps:
        return 0
    
    prices = [comp["price"] for comp in comps if "price" in comp]
    return sum(prices) / len(prices) if prices else 0

# Function to calculate MAO
def calculate_mao(arv, repair_costs, percentage=0.6):
    return (arv * percentage) - repair_costs

# Streamlit UI
st.title("Real Estate Valuation Tool")

full_address = st.text_input("Enter Zillow Property URL (e.g., https://www.zillow.com/homedetails/...)")
repair_costs = st.number_input("Estimated Repair Costs", min_value=0, step=1000)

if st.button("Analyze Property"):
    if is_valid_zillow_url(full_address):
        property_data = fetch_property_data(full_address)
        if property_data:
            comps = fetch_comps(property_data)
            arv = calculate_arv(comps)
            mao = calculate_mao(arv, repair_costs)
            
            st.subheader("Property Valuation")
            st.write(f"**ARV (After Repair Value):** ${arv:,.2f}")
            st.write(f"**Maximum Allowable Offer (MAO):** ${mao:,.2f}")
            
            if comps:
                st.subheader("Comparable Properties")
                comp_df = pd.DataFrame([{ "Address": comp["address"], "Sale Price": comp["price"] } for comp in comps if "address" in comp and "price" in comp])
                st.dataframe(comp_df)
        else:
            st.error("Failed to retrieve property data.")
    else:
        st.error("Please enter a valid Zillow property URL (e.g., https://www.zillow.com/homedetails/...)")
