import os
from dotenv import load_dotenv
import requests
##from flask import Flask

load_dotenv()
API_KEY = os.getenv('MBTA_API_KEY')

def address():
    TOKEN = os.getenv('MAPBOX_API_KEY')

    address = input("Input Address: ")

    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json"

    params = {
        "access_token": TOKEN
        }

    response = requests.get(url, params=params)
    data = response.json()
    return data['features']

add_data = address()

coordinates = add_data[0]["center"]

longitude = coordinates[0]
latitude = coordinates[1]

print(latitude, longitude)