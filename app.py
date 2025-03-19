import streamlit as st
import pandas as pd
import requests

# ATTOM API Configuration
API_KEY = "52e5fa8a3624dd87c762f5e8e648ae1b"
BASE_URL = "https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/detail"

# Function to fetch property details from ATTOM API
def get_comps(address):
    headers = {"Accept": "application/json", "apikey": API_KEY}
    params = {"address": address}
    
    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("property", [])
    except requests.exceptions.SSLError:
        st.error("SSL Error: Unable to verify the certificate. Check the API URL.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching property data: {e}")
    
    return []

# Function to calculate ARV
def calculate_arv(comps):
    prices = [comp.get("lastSaleAmount", 0) for comp in comps if "lastSaleAmount" in comp]
    return sum(prices) / len(prices) if prices else 0

# Function to estimate repair costs
def estimate_repairs(sqft):
    return sqft * 30  # Assume $30 per sqft repair cost

# Function to calculate MAO
def calculate_mao(arv, repair_costs):
    return 0.6 * arv - repair_costs

# Streamlit UI
st.title("AI Real Estate Comps & Valuation")
address = st.text_input("Enter Property Address:")

if st.button("Run Comps"):
    comps = get_comps(address)
    if comps:
        arv = calculate_arv(comps)
        repair_costs = estimate_repairs(1500)  # Placeholder value
        mao = calculate_mao(arv, repair_costs)
        
        st.subheader("Comparable Properties")
        st.write(pd.DataFrame(comps))
        
        st.subheader("Valuation Summary")
        st.write(f"**ARV (After Repair Value):** ${arv:,.2f}")
        st.write(f"**Estimated Repair Costs:** ${repair_costs:,.2f}")
        st.write(f"**Maximum Allowable Offer (MAO):** ${mao:,.2f}")
        
        st.subheader("How We Calculated This:")
        st.write("ARV is determined by averaging the sale prices of comparable properties within a 0.5 to 1-mile radius.")
        st.write("Repair costs are estimated based on an average cost per square foot.")
        st.write("MAO is calculated using 60% of ARV minus estimated repair costs.")
    else:
        st.error("No comparable properties found. Please try another address.")
