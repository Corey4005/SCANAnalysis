#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 18:45:08 2022

a module for importing data. 

datasets: 
    
    Soil Climate Analysis Network Soil Moisture data 
    Geospatial Orbiting Evironmental Sattelite Environmental Stress Index data
    National Land Cover Tree Data from Google Earth Engine:
        Script link: https://code.earthengine.google.com/e69616eae671012a18a2a954da7bc233?accept_repo=users%2Femaprlab%2Fpublic
        
    

@author: cwalker
"""
import pandas as pd
#SCAN station data 
SCAN_ALL = '../data/SCAN_DEPTHS_ALL.csv'
SCAN_READ = pd.read_csv(SCAN_ALL)
# SCAN_READ.replace(0, np.nan)
# SCAN_READ.dropna(inplace=True)

#GOES ESI data
GOES_ESI_ALL = '../data/1_wk_ESI_all.csv'
GOES_READ = pd.read_csv(GOES_ESI_ALL)
GOES_READ['Date'] = pd.to_datetime(GOES_READ['Date'])
GOES_READ.drop('Unnamed: 0', axis=1, inplace=True)
GOES_READ = GOES_READ[GOES_READ['ESI'] > -9999]
GOES_READ.dropna(inplace=True)

#treecover data 
TREE_COVER = '../data/tree_cover_by_station_pixel.csv'
TREE_READ = pd.read_csv(TREE_COVER)
TREE_READ.drop('Unnamed: 0', axis=1, inplace=True)