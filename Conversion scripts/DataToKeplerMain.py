# -*- coding: utf-8 -*-
"""
Created on Friday June 29, 2018

@author: Luca B
"""
import json #import json library
import time as tt #time lib
import datetime as dt #datetime 

#%% Loads json file
with open ("180401-50mi.json") as json_file: #define input file name
        flightData = json.load(json_file)
        flights = flightData["aircraft"] #Assigns aircraft key to flights
#%% Loads starting and ending times of data recording.
        startUnix = flightData["tmin"]
        endUnix = flightData["tmax"]
        startTime = dt.datetime.fromtimestamp(startUnix).strftime('%d-%m-%Y %H:%M:%S')
        endTime = dt.datetime.fromtimestamp(endUnix).strftime('%d-%m-%Y %H:%M:%S')
        print(startTime)#not yet sure what time zone this is in.
        print(endTime)
#%% Sets up keplergl dictionary: will later be converted to json
#config dictionary contains default configuration data for kepler.gl
currentTime = str(dt.datetime.now()) #used to timestamp the exported json
keplergl =  {}                      #define kepler
keplergl['datasets'] = []           #define dataset array
keplergl['datasets'].append({       #append dataset with blank data and field info
                "version" : "v1",
                "data":
                    {
                            "id": "va7iz64sd", #I dont really know how important this is
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
                                  "type": "int"
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
                        ]
                     }
                })

#basic kepler config settings below
keplergl['config'] = {
    "version": "v1",
    "config": {
      "visState": {
        "filters": [{
            "dataId": "va7iz64sd",
            "id": "2hf8iuq2",
            "name": "time",
            "type": "timeRange",
            "value": [
              (startUnix * 1000),
              (endUnix) #kepler apparently uses millis
            ],
            "enlarged": True,
            "plotType": "histogram",
            "yAxis": None
      }],
        "layers": [
          {
            "id": "iz02ex",
            "type": "point",
            "config": {
              "dataId": "va7iz64sd",
              "label": "Point",
              "color": [
                119,
                110,
                87
              ],
              "columns": {
                "lat": "latitude",
                "lng": "longitude",
                "altitude": "altitude"
              },
              "isVisible": True,
              "visConfig": {
                "radius": 0.9,
                "fixedRadius": False,
                "opacity": 0.01,
                "outline": False,
                "thickness": 2,
                "colorRange": {
                  "name": "Custom",
                  "type": "Custom",
                  "category": "Custom",
                  "colors": [
                    "#FFFFFF",
                    "#8cff00",
                    "#00ff6a",
                    "#00ffd8",
                    "#ff00ff",
                    "#ff007b",
                    "#ff0000"
                  ]
                },
                "radiusRange": [
                  0,
                  50
                ],
                "hi-precision": False
              }
            },
            "visualChannels": {
              "colorField": {
                "name": "altitude",
                "type": "integer"
              },
              "colorScale": "quantile",
              "sizeField": None,
              "sizeScale": "linear"
            }
          }
        ],
        "interactionConfig": {
          "tooltip": {
            "fieldsToShow": {
              "va7iz64sd": [
                "icao",
                "flight",
                "altitude",
                "segment",
                "time"
              ]
            },
            "enabled": True
          },
          "brush": {
            "size": 0.5,
            "enabled": False
          }
        },
        "layerBlending": "normal",
        "splitMaps": []
      },
      "mapState": {
        "bearing": 0,
        "dragRotate": False,
        "latitude": 37.53824292597814,
        "longitude": -122.8121695747103,
        "pitch": 0,
        "zoom": 7.429932582298195,
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

#The bulk: loads each flight and structures it as a different dataset for kepler.gl
for icao in flights:
    plane = flights[icao]
    metaData = plane[0] 
    for segment in range(1, len(plane)): #don't include metadata
        for sighting in plane[segment][1]: #don't include segment HDR data
            sightData = [
                    sighting['hex'], #icao 
                    sighting['flight'], #flightID
                    sighting['lat'], #latitude
                    sighting['lon'], #longitude
                    sighting['altitude'], #altitude
                    plane[segment][0]['segment'], #segment number
                    sighting['seen_pos'], #time
                    plane[segment][0]['destination'], #destination airport
                    plane[segment][0]['origin']
                    ]
                    
            keplergl['datasets'][0]["data"]['allData'].append(sightData)
with open('flightPlotPoints.json', 'w') as outfile:
     json.dump(keplergl, outfile)
#%%Single case test
#        flight1 = flights["0c20ab"]
#        metaData = flight1[0]
#        for segment in range(1, len(flight1)): #don't include metadata
#            for sighting in flight1[segment][1]: #don't include segment HDR data
#                sightData = [sighting['hex'], #icao
#                             sighting['flight'], #flightID
#                             sighting['lat'], #latitude
#                             sighting['lon'], #longitude
#                             sighting['altitude'], #altitude
#                             flight1[segment][0]['segment'], #not sure if segments are always increased by one, so I used the given segment value. 
#                             sighting['seen_pos'] #time
#                             ]
#                keplergl['datasets'][0]["data"]['allData'].append(sightData)
# with open('data.json', 'w') as outfile:
#     json.dump(keplergl, outfile)
#%% More Tester code
#       for icao in flights:
#            plane = flights[icao]
#            metaData = plane[0] 
#            for segment in range(1, len(plane)): #don't include metadata
#                for sighting in plane[segment][1]: #don't include segment HDR data
#                    print (plane[segment][0]['destination'])

            
            