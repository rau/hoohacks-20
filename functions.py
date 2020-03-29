from keys import API_KEY
import sys
import googlemaps
import json

def address_to_latlng():
    str_value = sys.argv[1]
    MAPS_API_KEY = API_KEY
    gmaps = googlemaps.Client(key=MAPS_API_KEY)
    geocode_result = gmaps.geocode(str_value)[0]
    lat, lng = geocode_result['geometry']['location']['lat'], geocode_result['geometry']['location']['lng']
    return lat, lng

def add_latlng_json(lat, lng, city):
    with open('static/latlng.json') as file:
            latlng = json.load(file)
            features = latlng['features']
            new_address = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [int(lat), int(lng)]
                },
                "properties": {
                    "title": "Request",
                    "description": city
                }
            }
            features.append(new_address)
            latlng['features'] = features
            with open('static/latlng.json', 'w') as f:
                json.dump(latlng, f, indent=4) # sort_keys=True

def get_json():
    with open('static/latlng.json') as file:
            latlng = json.load(file)
            return latlng