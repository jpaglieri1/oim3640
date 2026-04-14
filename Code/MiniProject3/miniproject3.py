import os
from dotenv import load_dotenv
import requests
import math
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

nearest_stations = find_station(latitude, longitude)
x=0
mindist = 100
for station in nearest_stations["data"]:
    stat_long = nearest_stations["data"][x]["attributes"]["longitude"]
    stat_lat = nearest_stations["data"][x]["attributes"]["latitude"]
    dist = math.sqrt(((stat_long-longitude)**2)+((stat_lat-latitude)**2))
    if mindist > dist:
        closest_station = (station["attributes"])
        mindist = dist
    x += 1

