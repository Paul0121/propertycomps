from homeharvest import scrape_property
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd
from datetime import datetime

def get_coordinates(address):
    geolocator = Nominatim(user_agent="ai_comps_system")
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    return None

def filter_comps(properties, target_coords, max_distance=1.0):
    filtered = []
    for _, row in properties.iterrows():
        prop_coords = (row['latitude'], row['longitude'])
        distance = geodesic(target_coords, prop_coords).miles
        if 0.5 <= distance <= max_distance:
            filtered.append(row)
    return pd.DataFrame(filtered)

def calculate_arv(comps):
    if comps.empty:
        return 0
    comps['price_per_sqft'] = comps['price'] / comps['sqft']
    median_ppsqft = comps['price_per_sqft'].median()
    avg_sqft = comps['sqft'].median()
    return median_ppsqft * avg_sqft

def estimate_repairs(avg_sqft):
    return avg_sqft * 50  # Rough estimate: $50 per sqft repair cost

def calculate_mao(arv, repair_costs):
    return (arv * 0.6) - repair_costs

def main():
    address = input("Enter property address: ")
    coords = get_coordinates(address)
    if not coords:
        print("Error: Could not find the location.")
        return
    
    properties = scrape_property(location=address, listing_type="sold", past_days=90)
    comps = filter_comps(properties, coords)
    
    arv = calculate_arv(comps)
    repair_costs = estimate_repairs(comps['sqft'].median())
    mao = calculate_mao(arv, repair_costs)
    
    print(f"ARV: ${arv:,.2f}")
    print(f"Estimated Repairs: ${repair_costs:,.2f}")
    print(f"MAO: ${mao:,.2f}")
    
    # Export results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Comps_Report_{timestamp}.csv"
    comps.to_csv(filename, index=False)
    print(f"Comps saved to {filename}")

if __name__ == "__main__":
    main()
