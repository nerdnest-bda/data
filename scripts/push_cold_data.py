
import pandas as pd
import pathlib
import os
import requests

def assign_us_quadrant(lat, lon):
    us_center_lat = 39.8
    us_center_lon = -98.6
    if lat > us_center_lat and lon < us_center_lon:
        return "q1"  # Northwest (Top Left)
    elif lat > us_center_lat and lon > us_center_lon:
        return "q2"  # Northeast (Top Right)
    elif lat < us_center_lat and lon < us_center_lon:
        return "q3"  # Southwest (Bottom Left)
    else:
        return "q4"  # Southeast (Bottom Right)

uri = "mongodb+srv://prajwalknaik7:prajwal@nerdnestcluster.ytkjd.mongodb.net/?retryWrites=true&w=majority&appName=nerdnestcluster"

df = pd.read_csv(os.path.join(pathlib.Path(__file__).parent.parent, "cold_data_store.csv"))

result = []
for index, row in df.iterrows():
    print("working")
    result.append({
        "name": row["INSTNM"],
        "address": row["ADDR_STR"],
        "coordinates": {
            "latitude": row["LATITUDE"],
            "longitude": row["LONGITUD"]
        },
        "mascot_photo": f"https://picsum.photos/400/300?random={index}",
        "website": row["WEBADDR"],
        "quadrant": assign_us_quadrant(row["LATITUDE"], row["LONGITUD"])
    })
response = requests.post("http://127.0.0.1:5000/api/universities/insert_universities", json={"universities": result})
print("Response:", response.json())

