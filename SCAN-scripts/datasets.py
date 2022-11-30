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
import os
import glob
#SCAN station data 
SCAN_ALL = '../data/SCAN_DEPTHS_ALL.csv'
SCAN_READ = pd.read_csv(SCAN_ALL)

#SCAN METADATA
SCAN_META = '../data/SCAN_METADATA.csv'
SCAN_META_READ = pd.read_csv(SCAN_META)
SCAN_META_READ.rename(columns={'stationTriplet':'station'}, inplace=True)

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
station_coverter = lambda x: x[-4:] + ':'+ 'AL'+':'+x[0:4]
TREE_READ['station'] = TREE_READ['station'].apply(station_coverter)

#data for the sm anomalies vs ESI bin
SM_ANOM_ESI_BIN = '../data/Mean_SM_anomalies_for_ESI_bin.csv'
SM_ANOM_ESI_BIN_READ = pd.read_csv(SM_ANOM_ESI_BIN)
SM_ANOM_ESI_BIN_READ.drop('Unnamed: 0', axis=1, inplace=True)

#data for average stdev and mean for each stn
SM_MEAN_STD = '../data/ALL_STN_Means_STDevs.csv'
SM_MEAN_STD_READ = pd.read_csv(SM_MEAN_STD)

#folder on local linux machine for ESI data:
here = os.getcwd()
path = '/rhome/cwalker/Downloads/ALEXI' #will need to be changed for ESI datasets stored on other computers
DataPath = os.path.join(here, path)

#folder for CPC_SM
cpc_path = '/rhome/cwalker/Downloads/CPC_SM/w.rank.20150917.tif'

#Alabama Counties
ALShape = '/rhome/cwalker/Desktop/repositories/SCANAnalysis/shapefiles/StateAlabama/tl_2016_01_cousub.shp'
ALShape2 = '/rhome/cwalker/Desktop/repositories/SCANAnalysis/shapefiles/StateAlabama/Alabama_State_Boundary.shp'
USCounties = '/rhome/cwalker/Desktop/repositories/SCANAnalysis/shapefiles/Counties/tl_2016_01_cousub.shp'

#scan shapes 
scan_shape_path = '../shapefiles/'
scan_shape_path = os.path.join(here, scan_shape_path)
scan_shape_files_list = []
for file in glob.glob(scan_shape_path+"*.shp"):
    scan_shape_files_list.append(file)

#NLCD data
NLCD_geotiffs_path = '/rhome/cwalker/Downloads/LAND_COVER/'
NLCD_geotiffs_path = os.path.join(here, NLCD_geotiffs_path)
NLCD_list = []
for file in glob.glob(NLCD_geotiffs_path+"*.tiff"):
    if file == '/rhome/cwalker/Downloads/LAND_COVER/NLCD_2001_2019_change_index_L48_20210604_H2RcUt3qX2gydjAF1lPp.tiff':
        pass
    else:
        NLCD_list.append(file)
