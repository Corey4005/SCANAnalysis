#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 16:20:45 2022

@author: cwalker
"""

#imports 
from get_landcover_arrays import landCoverDict
import numpy as np
import pandas as pd

#class dictionary for each subclass
classDict = {0:"Water", 1:"Developed", 2:"Barren", 3:"Forest", 4:"Shrubland", 
             5:"Herbaceous", 6:"Planted/Cultivated", 7:"Wetlands"}


#landcover df
landDf = pd.DataFrame()

#lists to get data with
nanlist = []
waterlist = []
developedlist = []
barrenlist = []
forestlist = []
shrublist = []
herbaceouslist = []
aglist = []
wetlandlist = []
stations = []
yearlist = []

for i in landCoverDict.keys():
    nanCount = 0
    waterCount = 0
    developedCount = 0
    barrenCount = 0
    forestCount = 0
    shrubCount = 0
    herbaceousCount = 0
    agCount = 0
    wetlandCount = 0
    keyName = i
    year = keyName[0:4]
    station = keyName[-4:]
    station_id = station+":AL:SCAN"
    array = landCoverDict.get(keyName)
    print("counting pixels for {}".format(i))
    for j in range(array.shape[0]):
        for k in range(array.shape[1]):
            if array[j, k]==0:
                waterCount+=1
            elif array[j, k]==1:
                developedCount+=1
            elif array[j, k]==2:
                barrenCount+=1
            elif array[j, k]==3:
                forestCount+=1
            elif array[j, k]==4:
                shrubCount+=1
            elif array[j, k]==5:
                herbaceousCount+=1
            elif array[j, k]==6:
                agCount+=1
            elif array[j, k]==7:
                wetlandCount+=1
            elif np.isnan(array[j, k]):
                nanCount+=1
    
    stations.append(station_id)
    yearlist.append(year)
    nanlist.append(nanCount)
    waterlist.append(waterCount)
    developedlist.append(developedCount)
    barrenlist.append(barrenCount)
    forestlist.append(forestCount)
    shrublist.append(shrubCount)
    herbaceouslist.append(herbaceousCount)
    aglist.append(agCount)
    wetlandlist.append(wetlandCount)
    

#creating df and calculating for percent of landcover
landDf['station']=stations
landDf['year']=yearlist
landDf['nan count']=nanlist
landDf['water count']=waterlist
landDf['shrub count']=shrublist
landDf['forest count']=forestlist
landDf['barren count']=barrenlist
landDf['herbaceous count']=herbaceouslist
landDf['agland count']=aglist
landDf['wetland count']=wetlandlist
landDf['developed count']=developedlist
landDf['total']=landDf['water count']+landDf['shrub count']+landDf['forest count']+landDf['barren count']+landDf['herbaceous count']+landDf['agland count']+landDf['wetland count']+landDf['developed count']
landDf['Agland percent']=landDf['agland count']/landDf['total']
landDf['Water percent']=landDf['water count']/landDf['total']
landDf['Shrub percent']=landDf['shrub count']/landDf['total']
landDf['Forest percent']=landDf['forest count']/landDf['total']
landDf['Barren percent']=landDf['barren count']/landDf['total']
landDf['Herbaceous percent']=landDf['herbaceous count']/landDf['total']
landDf['Wetland percent']=landDf['wetland count']/landDf['total']
landDf['Developed percent']=landDf['developed count']/landDf['total']
landDf = landDf[['station', 'year', 'Agland percent', 'Water percent', 'Shrub percent', 'Forest percent', 'Barren percent', 'Herbaceous percent', 'Wetland percent', 'Developed percent']]
landDf.set_index('year', inplace=True)
landDf.sort_index(inplace=True)
