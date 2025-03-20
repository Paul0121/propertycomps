import streamlit as st
import requests
import pandas as pd

def fetch_property_data(address1, address2, api_key):
    base_url = "https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/detail"
    headers = {"apikey": api_key}
    params = {"address1": address1, "address2": address2}
    
    response = requests.get(base_url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if "property" in data:
            return data["property"][0]
        else:
            st.warning("No property details found for the given address.")
    else:
        st.error(f"Error fetching property data: {response.status_code} {response.reason}")
        st.write(response.text)  # Debugging output
    return None

def fetch_comps(lat, lon, api_key):
    base_url = "https://api.gateway.attomdata.com/propertyapi/v1.0.0/sales/comp"
    headers = {"apikey": api_key}
    params = {
        "latitude": lat,
        "longitude": lon,
        "radius": "1",
        "minSalesPrice": "50000",
        "maxSalesPrice": "1000000",
        "propertytype": "SFR",
        "pagesize": "10"
    }
    
    response = requests.get(base_url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if "property" in data:
            return data["property"]
        else:
            st.warning("No comparable properties found.")
    else:
        st.error(f"Error fetching comps: {response.status_code} {response.reason}")
        st.write(response.text)  # Debugging output
    return []

def calculate_arv(comps):
    prices = [comp.get("sale", {}).get("amount") for comp in comps if comp.get("sale", {}).get("amount")]
    return sum(prices) / len(prices) if prices else 0

def calculate_mao(arv, repair_costs, percentage=0.6):
    return (arv * percentage) - repair_costs

st.title("Real Estate Valuation Tool")

api_key = st.text_input("Enter Attom Data API Key", type="password")
full_address = st.text_input("Enter Property Address (Street, City, State ZIP)")
repair_costs = st.number_input("Estimated Repair Costs", min_value=0, step=1000)

if st.button("Analyze Property"):
    if api_key and full_address:
        address_parts = full_address.split(",")
        if len(address_parts) < 3:
            st.error("Please enter a full address in the format: Street, City, State ZIP")
        else:
            address1 = address_parts[0].strip()
            address2 = ",".join(address_parts[1:]).strip()
            
            property_data = fetch_property_data(address1, address2, api_key)
            if property_data:
                lat = property_data.get("location", {}).get("latitude")
                lon = property_data.get("location", {}).get("longitude")
                if lat and lon:
                    comps = fetch_comps(lat, lon, api_key)
                    
                    arv = calculate_arv(comps)
                    mao = calculate_mao(arv, repair_costs)
                    
                    st.subheader("Property Valuation")
                    st.write(f"**ARV (After Repair Value):** ${arv:,.2f}")
                    st.write(f"**Maximum Allowable Offer (MAO):** ${mao:,.2f}")
                    
                    if comps:
                        st.subheader("Comparable Properties")
                        comp_df = pd.DataFrame([{
                            "Address": comp.get("address", {}).get("oneLine", "N/A"),
                            "Sale Price": comp.get("sale", {}).get("amount", "N/A")
                        } for comp in comps])
                        st.dataframe(comp_df)
                else:
                    st.error("Could not retrieve latitude and longitude for the property.")
    else:
        st.error("Please enter both API key and property address.")
