import streamlit as st
import pandas as pd
import requests

# Function to fetch live real estate data based on the input address
def get_comps(address):
    # Replace with an actual API call to fetch comps within 0.5 to 1 mile
    # Example: Using an external real estate API
    try:
        response = requests.get(f"https://realestateapi.com/comps?address={address}&radius=1")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching property data: {e}")
        return []

# Function to calculate ARV
def calculate_arv(comps):
    prices = [comp.get("Price", 0) for comp in comps if "Price" in comp]
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
