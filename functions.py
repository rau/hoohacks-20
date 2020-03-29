from keys import API_KEY
import sys
import googlemaps
import json
import string
import random

def address_to_latlng():
    str_value = sys.argv[1]
    MAPS_API_KEY = API_KEY
    gmaps = googlemaps.Client(key=MAPS_API_KEY)
    geocode_result = gmaps.geocode(str_value)[0]
    lat, lng = geocode_result['geometry']['location']['lat'], geocode_result['geometry']['location']['lng']
    return lat, lng

def add_latlng_json(lat, lng, name, city, desc):
    with open('static/latlng.json') as file:
            latlng = json.load(file)
            features = latlng['features']
            new_address = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(lng), float(lat)]
                },
                "properties": {
                    "title": name + " @ " + city,
                    "description": desc,
                    "identifier": ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
                }
            }
            features.append(new_address)
            latlng['features'] = features
            with open('static/latlng.json', 'w') as f:
                json.dump(latlng, f, indent=4) # sort_keys=True

def json_to_list():
    with open('static/latlng.json') as file:
        latlng = json.load(file)
        features = latlng['features']
        list_pass = []
        for feature in features:
            new_list = []
            new_list.append(feature['geometry']['coordinates'])
            new_list.append(feature['properties']['title'])
            new_list.append(feature['properties']['description'])
            list_pass.append(new_list)
        return list_pass
            
add_latlng_json("38.907362", "-77.3967888", "Raunak Daga", "Oak Hill", "I need toiler paper")