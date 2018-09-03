# -*- coding: utf-8 -*-
"""
Created on Friday June 29, 2018

@author: Luca B
"""
import json #import json library
import time as tt #time lib
import datetime as dt #datetime 

#%% Sets up keplergl dict: will later be converted to json
#config contains default configuration data for kepler.gl
currentTime = str(dt.datetime.now())
deckPlot = []
#deckPlot['flights'] = {}
#%% Loads json file
with open ("180502-50mi.json") as json_file:
        flightData = json.load(json_file)
        flights = flightData["aircraft"] #Assigns aircraft key to flights
#%% Loads starting and ending times of data recording.
        startUnix = flightData["tmin"]
        endUnix = flightData["tmax"]
        startTime = dt.datetime.fromtimestamp(startUnix).strftime('%d-%m-%Y %H:%M:%S')
        endTime = dt.datetime.fromtimestamp(endUnix).strftime('%d-%m-%Y %H:%M:%S')
        print(startTime)#not yet sure what time zone this is in.
        print(endTime)
#%% Tester code
#%%Single case
#        flight1 = flights["0c20ab"]
#        metaData = flight1[0]
#        #deckPlot['flights']['sightings'] = []
#        for segment in range(1, len(flight1)): #don't include metadata
#            for sighting in flight1[segment][1]: #don't include segment HDR dat
#                sightData = {}
#                sightData['identifier'] = sighting['hex']
#                sightData['position'] = [
#                    sighting['lon'], #longitude 
#                    sighting['lat']#latitude
#                ]
#                sightData['color'] = [255, 0, 0]
#                sightData['radius'] = 100
#                sightData['altitude'] = sighting['altitude']
#                deckPlot.append(sightData)
#with open('singleFlight.json', 'w') as outfile:
#     json.dump(deckPlot, outfile, indent = 4)

#%% The bulk: loads each flight and structures it as a different dataset for kepler.gl
        for icao in flights:
            plane = flights[icao]
            metaData = plane[0] 
            for segment in range(1, len(plane)): #don't include metadata
                totalSightings = len(plane[segment][1]) 
                for sighting in range(1, totalSightings - 1): #don't include segment HDR data, goes to end -1 as each point contains the next segment's data as well. Meant for lines. 
                    current = plane[segment][1][sighting]
                    nextSight = plane[segment][1][sighting + 1]
                    sightData = {}
                    sightData['identifier'] = current['hex']
                    sightData['position'] = [
                        current['lon'], #longitude 
                        current['lat']#latitude
                    ]
                    sightData['nextPos'] = [
                        nextSight['lon'], #longitude 
                        nextSight['lat']#latitude
                    ]
                    sightData['altitude'] = current['altitude']
                    sightData['nextAlt'] = nextSight['altitude']
                    sightData['time'] = current['seen_pos']
                    deckPlot.append(sightData)
           # print (flights[icao][0]) #code for locating where I was in the json
with open('deckLineVis.json', 'w') as outfile:
     json.dump(deckPlot, outfile, indent = 4)
            
            