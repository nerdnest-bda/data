
import pymongo
from pymongo import MongoClient
import pandas as pd
import pathlib
import os
import requests

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
        "mascot_photo": f"https://picsum.photos/400/300?random={index}"
    })
response = requests.post("http://127.0.0.1:5000/api/universities/insert_universities", json={"universities": result})

