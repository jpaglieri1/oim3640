import os
from dotenv import load_dotenv
import requests
##from flask import Flask

load_dotenv()

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

def find_station(latitude, longitude):
    API_KEY = os.getenv('MBTA_API_KEY')
    
    url = "https://api-v3.mbta.com/stops"

    lat = latitude
    lon = longitude
    
    params = {
        "filter[latitude]": lat,
        "filter[longitude]": lon,
        "filter[radius]": 0.1
    }

    headers = {
        "x-api-key": API_KEY
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    return(data)

address_data = address()
coordinates = address_data[0]["center"]

longitude = coordinates[0]
latitude = coordinates[1]

print(latitude, longitude)

nearest_stations = find_station(latitude, longitude)

print(nearest_stations)

if len(nearest_stations['data']) == 0:
    print("Too far")