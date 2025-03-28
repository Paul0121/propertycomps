from homeharvest import scrape_property
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd
from datetime import datetime

def get_coordinates(address):
    """Get latitude and longitude of a given address."""
    try:
        geolocator = Nominatim(user_agent="ai_comps_system")
        location = geolocator.geocode(address, timeout=10)
        if location:
            return (location.latitude, location.longitude)
        else:
            print("Error: Could not find the location. Please check the address.")
            return None
    except Exception as e:
        print(f"Geolocation error: {e}")
        return None

def filter_comps(properties, target_coords, min_distance=0.5, max_distance=1.0):
    """Filter comparable properties based on distance range."""
    if properties.empty:
        print("No properties found for comps.")
        return pd.DataFrame()

    filtered = []
    for _, row in properties.iterrows():
        try:
            prop_coords = (row['latitude'], row['longitude'])
            distance = geodesic(target_coords, prop_coords).miles
            if min_distance <= distance <= max_distance:
                filtered.append(row)
        except Exception as e:
            print(f"Error processing property: {e}")

    return pd.DataFrame(filtered)

def calculate_arv(comps):
    """Calculate the After Repair Value (ARV) based on median price per square foot."""
    if comps.empty:
        print("No comps available to calculate ARV.")
        return 0

    try:
        comps['price_per_sqft'] = comps['price'] / comps['sqft']
        median_ppsqft = comps['price_per_sqft'].median()
        avg_sqft = comps['sqft'].median()

        if pd.isna(median_ppsqft) or pd.isna(avg_sqft):
            print("Insufficient data to calculate ARV.")
            return 0

        return median_ppsqft * avg_sqft
    except Exception as e:
        print(f"Error calculating ARV: {e}")
        return 0

def estimate_repairs(avg_sqft):
    """Estimate repair costs based on square footage."""
    if pd.isna(avg_sqft) or avg_sqft <= 0:
        return 0
    return avg_sqft * 50  # Rough estimate: $50 per sqft repair cost

def calculate_mao(arv, repair_costs):
    """Calculate the Maximum Allowable Offer (MAO)."""
    if arv <= 0:
        return 0
    return (arv * 0.6) - repair_costs

def main():
    address = input("Enter property address: ").strip()
    coords = get_coordinates(address)
    if not coords:
        return

    print("\nFetching comparable properties...")
    properties = scrape_property_
