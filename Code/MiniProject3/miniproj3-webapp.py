import os
from dotenv import load_dotenv
import requests
import math
from flask import Flask, render_template, request, jsonify

load_dotenv()

app = Flask(__name__)

def geocode_address(address):
    """Convert address to coordinates using Mapbox API"""
    TOKEN = os.getenv('MAPBOX_API_KEY')

    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json"

    params = {
        "access_token": TOKEN
    }

    response = requests.get(url, params=params)
    data = response.json()
    
    if not data['features']:
        return None
    
    return data['features']

def find_station(latitude, longitude, route_types=None):
    """Find nearby MBTA stations, optionally filtered by route type"""
    API_KEY = os.getenv('MBTA_API_KEY')
    
    url = "https://api-v3.mbta.com/stops"

    params = {
        "filter[latitude]": latitude,
        "filter[longitude]": longitude,
        "filter[radius]": 100
    }
    
    # Add route type filter if provided
    if route_types:
        params["filter[route_type]"] = ",".join(map(str, route_types))

    headers = {
        "x-api-key": API_KEY
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    return data

def find_closest_station(latitude, longitude, nearest_stations):
    """Find the closest station from the list"""
    if not nearest_stations.get("data"):
        return None
    
    mindist = 100
    closest_station = None
    
    for x, station in enumerate(nearest_stations["data"]):
        stat_long = nearest_stations["data"][x]["attributes"]["longitude"]
        stat_lat = nearest_stations["data"][x]["attributes"]["latitude"]
        dist = math.sqrt(((stat_long-longitude)**2)+((stat_lat-latitude)**2))
        
        if mindist > dist:
            closest_station = station["attributes"]
            mindist = dist
    
    return closest_station

@app.route("/")
def home():
    return render_template("station_finder.html")

@app.route("/find-station", methods=["POST"])
def find_nearest():
    """API endpoint to find nearest station"""
    try:
        data = request.get_json()
        address = data.get("address")
        route_types = data.get("route_types", [])
        
        if not address:
            return jsonify({"error": "Address is required"}), 400
        
        # Get coordinates from address
        address_data = geocode_address(address)
        if not address_data:
            return jsonify({"error": "Address not found"}), 404
        
        coordinates = address_data[0]["center"]
        longitude = coordinates[0]
        latitude = coordinates[1]
        
        # Find nearby stations, optionally filtered by route type
        nearest_stations = find_station(latitude, longitude, route_types if route_types else None)
        closest_station = find_closest_station(latitude, longitude, nearest_stations)
        
        if not closest_station:
            return jsonify({"error": "No stations found nearby with selected filters"}), 404
        
        return jsonify({
            "success": True,
            "station": {
                "name": closest_station["name"],
                "municipality": closest_station["municipality"],
                "latitude": closest_station["latitude"],
                "longitude": closest_station["longitude"]
            },
            "input_address": address_data[0]["place_name"]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)