import streamlit as st
import requests
import pandas as pd

def fetch_state_data():
    """Fetches state data from the given JSON response."""
    url = "https://api.yourrealestate.com/state_lookup"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def extract_state_info(state_data):
    """Extracts relevant state details from the API response."""
    states = state_data.get("response", {}).get("data", {}).get("rows", [])
    state_dict = {state["geo_key"]: state for state in states}
    return state_dict

def calculate_arv(comps):
    """Calculates After Repair Value (ARV) based on comparable properties."""
    arv = sum(comp['price'] for comp in comps) / len(comps) if comps else 0
    return arv

def calculate_mao(arv, repair_costs):
    """Calculates Maximum Allowable Offer (MAO)."""
    mao = arv * 0.6 - repair_costs
    return mao

def fetch_comps(property_address):
    """Fetches comparable properties from an external API."""
    url = f"https://api.yourrealestate.com/comps?address={property_address}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("comps", [])
    return []

def main():
    st.title("Real Estate ARV & MAO Calculator")
    property_address = st.text_input("Enter Property Address:")
    repair_costs = st.number_input("Estimated Repair Costs ($):", min_value=0, step=500)
    
    if st.button("Calculate ARV & MAO"):
        state_data = fetch_state_data()
        if state_data:
            states = extract_state_info(state_data)
            comps = fetch_comps(property_address)
            if comps:
                arv = calculate_arv(comps)
                mao = calculate_mao(arv, repair_costs)
                st.write(f"**After Repair Value (ARV):** ${arv:,.2f}")
                st.write(f"**Maximum Allowable Offer (MAO):** ${mao:,.2f}")
                st.write("### Comparable Properties:")
                st.dataframe(pd.DataFrame(comps))
            else:
                st.error("No comparable properties found.")
        else:
            st.error("Failed to fetch state data.")

if __name__ == "__main__":
    main()
