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

#%% Loads json file
with open ("180401-50mi.json") as json_file:
        flightData = json.load(json_file)
        flights = flightData["aircraft"] #Assigns aircraft key to flights
#%% Loads starting and ending times of data recording.
        startUnix = flightData["tmin"]
        endUnix = flightData["tmax"]
        startTime = dt.datetime.fromtimestamp(startUnix).strftime('%d-%m-%Y %H:%M:%S')
        endTime = dt.datetime.fromtimestamp(endUnix).strftime('%d-%m-%Y %H:%M:%S')
        print("Start:" + startTime)#Local time
        print("End:" + endTime)
        
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
              "visState": {
                "filters": [
                  {
                    "dataId": "va7iz64sd",
                    "id": "2hf8iuq2",
                    "name": "time",
                    "type": "timeRange",
                    "value": [
              (startUnix * 1000),
              (startUnix + 300) * 1000 #kepler apparently uses millis
            ],
                    "enlarged": True,
                    "plotType": "histogram",
                    "yAxis": None
                  }
                ],
                "layers": [
                  {
                    "id": "esd5s7",
                    "type": "line",
                    "config": {
                      "dataId": "va7iz64sd",
                      "label": "Line",
                      "color": [
                        253,
                        236,
                        0
                      ],
                      "columns": {
                        "lat0": "latitude",
                        "lng0": "longitude",
                        "lat1": "nextLat",
                        "lng1": "nextLong"
                      },
                      "isVisible": True,
                      "visConfig": {
                        "opacity": 0.41,
                        "thickness": 2,
                        "colorRange": {
                          "name": "Global Warming",
                          "type": "sequential",
                          "category": "Uber",
                          "colors": [
                            "#5A1846",
                            "#900C3F",
                            "#C70039",
                            "#E3611C",
                            "#F1920E",
                            "#FFC300"
                          ]
                        },
                        "sizeRange": [
                          1,
                          4
                        ],
                        "targetColor": [
                          114,
                          12,
                          157
                        ],
                        "hi-precision": False
                      }
                    },
                    "visualChannels": {
                      "colorField": {
                        "name": "destination",
                        "type": "string"
                      },
                      "colorScale": "ordinal",
                      "sizeField": {
                        "name": "altitude",
                        "type": "integer"
                      },
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
                "bearing": 40.96875,
                "dragRotate": True,
                "latitude": 37.63650131632762,
                "longitude": -122.29499536335629,
                "pitch": 46.964285714285715,
                "zoom": 9.467365715011885,
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
with open('flightPlotLines.json', 'w', ) as outfile:
    json.dump(keplergl, outfile, indent=4)
            
            