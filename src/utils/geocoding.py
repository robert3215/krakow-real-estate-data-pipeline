import pandas as pd
import time 
import requests 
import os 
from data_cleaning import clean_data

token_locationiq = os.environ.get('locationiq')

df = clean_data("data/raw/apartments_raw.csv")

url = "https://eu1.locationiq.com/v1/search.php"

unique_pairs = df[["Neighborhood", "District"]].drop_duplicates()

coords_dict = {}

for _, row in unique_pairs.iterrows():
    neighborhood = row["Neighborhood"]
    district = row["District"]

    address = f"{neighborhood}, {district}, Kraków, Poland"

    params = {
        "key": token_locationiq,
        "q": address,
        "format": "json",
        "limit": 1 }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            coords_dict[(neighborhood, district)] = (lat, lon)
        else:
            coords_dict[(neighborhood, district)] = (None, None)
        time.sleep(0.5)
    except Exception as e:
        print(f"Error for {address}: {e}")
        coords_dict[(neighborhood, district)] = (None, None)
        

df["Latitude"] = df.apply(lambda row: coords_dict.get((row["Neighborhood"], row["District"]),(None, None))[0],axis=1)
df["Longitude"] = df.apply(lambda row: coords_dict.get((row["Neighborhood"], row["District"]),(None, None))[1],axis=1)


neigh_coords = df[['District','Neighborhood','Latitude','Longitude']].drop_duplicates(subset=['District', 'Neighborhood'])
neigh_coords.to_csv("neighborhood_coordinates.csv", index = False)