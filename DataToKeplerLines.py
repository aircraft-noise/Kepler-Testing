# -*- coding: utf-8 -*-
"""
Created on Friday July 5, 2018

@author: Luca B

Because it's meant for lines, 
a more aestheticly pleasing visualizaiton,
This version has slightly modified loops 
and storage of data. 

"""
import json #import json library
import time as tt #time lib
import datetime as dt #datetime 

#%% Sets up keplergl dictionary: will later be converted to json
#config dictionary contains default configuration data for kepler.gl
currentTime = str(dt.datetime.now()) #used to timestamp the exported json
keplergl =  {}                      #define kepler
keplergl['datasets'] = []           #define dataset array
keplergl['datasets'].append({       #append dataset with blank data and field info
                "version" : "v1",
                "data":
                    {
                            "id": 1, #I dont really know how important this is
                            "label": "flights", #name on kepler gui
                             "color" : [143, 47, 91],  #random rgb
                             "allData" : [],    #kepler's main method of storing data, left blank here for setup.
                             "fields": [        #fields that kepler uses for "column" names: data array must correspond to this order.
                            {
                                  "name": "icao",
                                  "type": "string"
                            },
#                            {
#                                  "name": "Aircraft Type",
#                                  "type": "int"
#                            },
                            {
                                  "name": "flight",
                                  "type": "string"
                            },
                            {
                                  "name": "latitude",
                                  "type": "float"
                            },
                            {
                                  "name": "longitude",
                                  "type": "float"
                            },
                            {
                                  "name": "altitude",
                                  "type": "float"
                            },
                            {
                                  "name": "segment",
                                  "type": "int"
                            },
                            {
                                  "name": "time",
                                  "type": "time"
                            },
                            {
                                  "name": "destination",
                                  "type": "string"
                            },                            
                            {
                                  "name": "origin",
                                  "type": "string"
                            },
                            {
                                  "name": "nextLat",
                                  "type": "float"
                            },
                            {
                                  "name": "nextLong",
                                  "type": "float"
                            }
                            
                        ]
                     }
                })

#basic kepler config settings below
keplergl['config'] = { 
                    "version": "v1",
                    "config": {
                        "visState":{
                            "filters": [],
                            "layers": [],
                            "interactionConfig": {
                                "tooltip": {
                                    "fieldsToShow": {},
                                "enabled": False
                                },
                                "brush": {
                                    "size": 0.5,
                                    "enabled": False
                                }
                            },
                            "layerBlending": "normal",
                            "splitMaps":[]
                        },
                        "mapState": {
                            "bearing": 0,
                            "dragRotate": False,
                            "latitude": 37.75403,
                            "pitch": 0,
                            "zoom": 9,
                            "isSplit": False
                        },
                        "mapStyle": {
                            "styleType": "dark",
                            "topLayerGroups": {},
                            "visibleLayerGroups": {
                                    "label": True,
                                    "road": True,
                                    "border": False,
                                    "building": True,
                                    "water": True,
                                    "land": True
                        },
                        "mapStyles": {}
                    }
                }
            }   
keplergl['info'] = {
                    "app": "kepler.gl",
                    "created_at": "" + currentTime + "GMT-0700 (Pacific Daylight Time)"
                }
#%% Loads json file
with open ("FATEST180624.json") as json_file:
        flightData = json.load(json_file)
        flights = flightData["aircraft"] #Assigns aircraft key to flights
#%% Loads starting and ending times of data recording.
        startUnix = flightData["tmin"]
        endUnix = flightData["tmax"]
        startTime = dt.datetime.fromtimestamp(startUnix).strftime('%d-%m-%Y %H:%M:%S')
        endTime = dt.datetime.fromtimestamp(endUnix).strftime('%d-%m-%Y %H:%M:%S')
        print("Start:" + startTime)#Local time
        print("End:" + endTime)
#%% The bulk: loads each flight and structures it as a different dataset for kepler.gl
        for icao in flights:
            plane = flights[icao]
            metaData = plane[0] 
            for segment in range(1, len(plane)): #don't include metadata
                totalSightings = len(plane[segment][1]) 
                for sighting in range(1, totalSightings - 1): #don't include segment HDR data, goes to end -1 as each point contains the next segment's data as well. Meant for lines. 
                    current = plane[segment][1][sighting]
                    nextSight = plane[segment][1][sighting + 1]
                    sightData = [
                        current['hex'], #icao
                        current['flight'], #flightID
                        current['lat'], #latitude
                        current['lon'], #longitude
                        current['altitude'], #altitude
                        plane[segment][0]['segment'], #segment number
                        current['seen_pos'], #time
                        plane[segment][0]['destination'], #destination airport
                        plane[segment][0]['origin'],
                        nextSight['lat'], #next position latitude
                        nextSight['lon'] #next position longitude
                            ]
                    keplergl['datasets'][0]["data"]['allData'].append(sightData) #appends data in list above.
with open('keplerdata.json', 'w') as outfile:
    json.dump(keplergl, outfile)
            
            