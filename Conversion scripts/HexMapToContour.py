# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 14:33:12 2018

@author: lucab
"""
#%%
import csv
import numpy as np
import matplotlib.pyplot as plt
import geojsoncontour as gjc
import matplotlib.cm as cm

#plt.clf()
monitorData = []
lat = []
lon = []
level = []

with open( "180502-HexbinNoise.txt") as tsvFile:
    next(tsvFile)
    next(tsvFile)#skip header
    fileReader = csv.DictReader(tsvFile, delimiter='\t')
    for row in fileReader:
        monitorData.append(dict(row))
    for monitor in monitorData:
        lat.append(float(monitor['Latitude']))
        lon.append(float(monitor['Longitude']))
        level.append(float(monitor['DNL 24 hr']))
        
ax = plt.figure(figsize=(12,8)).add_subplot(111)
contour = ax.tricontour(lon, lat, level, 200, linewidths=2, extend='neither', cmap=cm.nipy_spectral)
plt.colorbar(contour, shrink=1.2, extend='neither', extendrect='true', orientation='vertical', drawedges='false')
# Default contour converison settings
gjc.contour_to_geojson(
    contour=contour,
    geojson_filepath='noiseMap.geojson',
    min_angle_deg=10.0,
    ndigits=4,
    unit='m'
)