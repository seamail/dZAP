#!/bin/python

import requests
import json
from random import randrange, uniform

def retrieve_locality(originLatitude,originLongitude):
    mult = [-1,1]
    V = randrange(0,1)
    lat = originLatitude + uniform(0,2)*mult[V]
    V = randrange(0,1)
    lng = originLongitude + uniform(0,2)*mult[V]

    URL = "http://maps.googleapis.com/maps/api/geocode/json"

    Parameters = {'latlng': "%f,%f" % (lat,lng),
                  'sensor': 'false'}

    Request = requests.get(URL, params=Parameters)

    jsondata = json.loads(Request.text)

    Result = []
    print(jsondata)
    if len(jsondata["results"]) ==0:
        return retrieve_locality(originLatitude,originLongitude)

    result = jsondata["results"][0]

    ac = result["address_components"]
    print(ac)
    if len(ac) < 2:
        return retrieve_locality(originLatitude, originLongitude)

    for component in ac:
        #if 'administrative_area_level_2' in component["types"]:
            #print('>>> %s' % component['short_name'])
            #Result.append(component['short_name'])
        if 'administrative_area_level_1' in component["types"]:
            #print('>>> %s' % component['short_name'])
            Result.append(component['short_name'])
        if 'locality' in component["types"]:
            #print('>> %s' % component['short_name'])
            Result.append(component['short_name'])
    if len(Result) < 2:
        return retrieve_locality(originLatitude,originLongitude)
    Result.append([lat,lng])

    middlelat = (originLatitude - lat)/2
    middlelat = middlelat + lat
    middlelng = (originLongitude - lng)/2
    middlelng = middlelng + lng

    print("Coord Origin: %f,%f   Middle: %f,%f   Destination: %f,%f" %
          (originLatitude,originLongitude,middlelat,middlelng,lat,lng))
    
    Result.append([middlelat,middlelng])
    
    return Result
