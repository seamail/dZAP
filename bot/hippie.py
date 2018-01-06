#!/bin/python

def retrieve_locality(Ilat,Ilng):
    mult = [-1,1]
    V = randrange(0,1)
    lat = Ilat + uniform(0,2)*mult[V]
    V = randrange(0,1)
    lng = Ilng + uniform(0,2)*mult[V]

    URL = "http://maps.googleapis.com/maps/api/geocode/json?latlng="+str(lat)+','+str(lng)+"&sensor=false"
    Content = urllib.request.urlopen(URL).read().decode('utf-8')
    jsondata = json.loads(Content)

    Result = []
    
    if len(jsondata["results"]) ==0:
        return retrieve_locality(Ilat,Ilng)
    
    result = jsondata["results"][0]

    if len(result["address_components"]) < 2:
        return retrieve_locality(Ilat,Ilng)        
        
    for component in result["address_components"]:
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
        return retrieve_locality(Ilat,Ilng)
    Result.append([lat,lng])

    middlelat = (Ilat - lat)/2
    middlelat = middlelat + lat
    middlelng = (Ilng - lng)/2
    middlelng = middlelng + lng

    print("Coord Origin: %f,%f   Middle: %f,%f   Destination: %f,%f" %
          (Ilat,Ilng,middlelat,middlelng,lat,lng))
    
    Result.append([middlelat,middlelng])
    
    return Result
