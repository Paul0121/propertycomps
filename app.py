import streamlit as st
import pandas as pd
import requests
import os

# Secure API Key Storage - Use an environment variable in production
API_KEY = "4c51677e91764ccb8209425467819153"  # Store this securely in production!

def get_comps(address):
    """Fetch comparable properties from RentCast API based on user input"""
    api_url = "https://api.rentcast.io/v1/properties"
    headers = {"X-Api-Key": API_KEY}
    params = {"address": address}

    try:
        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract comparable properties
        return data.get("comparable_properties", [])  # Adjust based on actual RentCast API response
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching property data: {e}")
        return []

def calculate_arv(comps):
    """Calculate ARV based on average price of comps"""
    prices = [comp.get("price", 0) for comp in comps if "price" in comp]
    return sum(prices) / len(prices) if prices else 0

def estimate_repairs(sqft):
    """Estimate repair costs based on property square footage"""
    return sqft * 30  # Assume $30 per sqft repair cost

def calculate_mao(arv, repair_costs):
    """Calculate Maximum Allowable Offer (MAO)"""
    return 0.6 * arv - repair_costs  # Fixed at 60% of ARV

# Streamlit UI
st.title("🏡 AI Real Estate Comps & Valuation")
address = st.text_input("📍 Enter Property Address:")

if st.button("🔍 Run Comps"):
    comps = get_comps(address)

    if comps:
        # Calculate ARV and MAO
        arv = calculate_arv(comps)
        repair_costs = estimate_repairs(1500)  # Placeholder square footage
        mao = calculate_mao(arv, repair_costs)

        # Display Results
        st.subheader("📊 Comparable Properties")
        st.write(pd.DataFrame(comps))  # Show property comps in a table

        st.subheader("💰 Valuation Summary")
        st.write(f"**ARV (After Repair Value):** ${arv:,.2f}")
        st.write(f"**Estimated Repair Costs:** ${repair_costs:,.2f}")
        st.write(f"**Maximum Allowable Offer (MAO):** ${mao:,.2f}")

        st.subheader("📌 How We Calculated This:")
        st.write("✔ **ARV** is determined by averaging the sale prices of comparable properties within a **0.5 to 1-mile radius**.")
        st.write("✔ **Repair costs** are estimated based on **$30 per sqft** repair cost.")
        st.write("✔ **MAO** is calculated as **60% of ARV minus repair costs**.")
    else:
        st.error("⚠ No comparable properties found. Please try another address.")
