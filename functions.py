from keys import GOOGLE_API_KEY, ACCOUNT_SID, AUTH_TOKEN
from twilio.rest import Client
from flask import session
import sys
import googlemaps
import json
import string
import random
import requests

def address_to_lnglat(address):
    str_value = address
    MAPS_API_KEY = GOOGLE_API_KEY
    gmaps = googlemaps.Client(key=MAPS_API_KEY)
    geocode_result = gmaps.geocode(str_value)[0]
    lat, lng = geocode_result['geometry']['location']['lat'], geocode_result['geometry']['location']['lng']
    city = geocode_result['address_components'][2]['long_name']
    return lng, lat, city

def add_to_json(lng, lat, name, city, desc, address):
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
                "identifier": ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)),
                "address": address,
                "name": name
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
            new_list.append(feature['properties']['identifier'])
            # if 'origin' in session:
            #     url = "https://maps.googleapis.com/maps/api/distancematrix/json"
            #     r = requests.get(url + 'origins = ' + session['origin'] + '&destinations = ' + feature['properties']['address'] + '&key = ' + GOOGLE_API_KEY)
            #     new_list.append(distance)
            list_pass.append(new_list)
        return list_pass

def remove_from_list(identifier_compare):
    with open('static/latlng.json') as file:
        latlng = json.load(file)
        features = latlng['features']
        for feature_index in range(len(features)):
            if features[feature_index]['properties']['identifier'] == identifier_compare:
                del features[feature_index]
                break
        latlng['features'] = features
        with open('static/latlng.json', 'w') as f:
            json.dump(latlng, f, indent=4) # sort_keys=True

def add_to_list(request):
    name = request.form['name']
    address = request.form['street'] + ', ' + request.form['city'] + ', ' + request.form['state'] + ', ' + request.form['zip']
    description = request.form['itemneeded']
    # name = 'Rashad Philizaire'
    # address = '6518 Trask Terrace, Alexandria, VA, 22315'
    # description = 'I need toilet paper ASAP'

    lng, lat, city = address_to_lnglat(address)
    add_to_json(lng, lat, name, city, description, address)

def text_info(identifier_compare, phone_number):
    account_sid = ACCOUNT_SID
    auth_token  = AUTH_TOKEN

    client = Client(account_sid, auth_token)

    name = address = desc = ''

    with open('static/latlng.json') as file:
        latlng = json.load(file)
        features = latlng['features']
        for feature_index in range(len(features)):
            if features[feature_index]['properties']['identifier'] == identifier_compare:
                name = features[feature_index]['properties']['name']
                address = features[feature_index]['properties']['address']
                desc = features[feature_index]['properties']['description']

    body_of_text = f'''
    Thank you Good Samaritan!\n\n{name} is waiting for you at {address}.\n\nHere's their request: {desc}\n\nThank you for everything you do, and remember to stay safe and take the proper precautions.
    '''

    to_number = phone_number
    message = client.messages.create(
        to=str(to_number), 
        from_="+17147939326",
        body=body_of_text
    )


def set_session_keys(request):
    session['origin'] = request.form['street_origin'] + ', ' + request.form['city_origin'] + ', ' + request.form['state_origin'] + request.form['zip_origin'] 