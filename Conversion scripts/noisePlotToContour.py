# -*- coding: utf-8 -*-
"""
Plotting geojson contours
Created on Tue Jul 17 13:57:23 2018

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
with open( "4-1-18 noise plot.csv") as csvfile:
    fileReader = csv.DictReader(csvfile, dialect='excel')
    for row in fileReader:
        monitorData.append(dict(row))
    for monitor in monitorData:
        lat.append(float(monitor['Latitude']))
        lon.append(float(monitor['Longitude']))
        level.append(float(monitor['dB']))
ax = plt.figure(figsize=(12,8)).add_subplot(111)
contour = ax.tricontour(lon, lat, level, 6, linewidths=2, extend='both', cmap=cm.nipy_spectral)
plt.colorbar(contour, shrink=1.2, extend='both', extendrect='true', orientation='vertical', drawedges='false')
# Default contour converison settings
gjc.contour_to_geojson(
    contour=contour,
    geojson_filepath='noiseMap.geojson',
    min_angle_deg=10.0,
    ndigits=4,
    unit='m'
)
#%% Convert matplotlib tricontourf to geojson -- doesn't work
#gjc.contourf_to_geojson(
#    contourf=contour,
#    min_angle_deg=3.0,
#    ndigits=3,
#    stroke_width=2,
#    fill_opacity=0.5,
#    geojson_filepath='noiseMapFill.geojson',
#)