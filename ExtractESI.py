# -*- coding: utf-8 -*-
"""
Parameters:
    sys.argv[1] = filepath to the ESI data as a str. 
    sys.argv[2] = filepath to the metadata as a str.

Example Usage: 
    run ExtractESI.py [ESI data] [metadata]

Questions: 
    I am unsure at the moment of how to get the dates to convert from julian time using the datetime variable. 
    I am also unsure of how to store the printed variables into a dataframe. 
    
author: Corey 

"""
import rasterio
import glob2
import sys 
import datetime as dt
import pandas as pd
import geopandas as gpd
import numpy as np

#read in the filepath and metadata
filepath = 'r' + sys.argv[1]
metadata = 'r' + sys.argv[2]

#check to see if len of sys.argv is good. 
if len(sys.arg) != 3:
    print('usage: run ExtractESI.py [insert filepath as str], [insert metadata as str]')
    sys.exit()
else:
    pass

#look for all files in filepath
files = glob2.glob(filepath + '/*tif')
print(len(files))

#read int the metadata
import_csv = pd.read_csv(metadata)
df = pd.DataFrame(import_csv)
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
        
#extract the ESI, datestring, lon and lat for file in filepath
def ExtractESI(files):
    for file in files:
        file_split = file.split('_')
        file_date = file_split[6].split('.tif')[0]
        raster = rasterio.open(file)
        for point in gdf['geometry']:
            x = point.xy[0][0]
            y = point.xy[1][0]
            index = raster.index(x, y)
            values = raster.read(1)[index]
            values_list = [values for value in index]
            ESI_values = values_list[0].tolist()
            formated = float("{:.3f}".format(ESI_values))
            dates = np.array(file_date)
            longitude = np.array(x)
            latitude = np.array(y)
            print(formated, dates, longitude, latitude)
        
def main():
    ExtractESI(files)
    
if __name__ == '__main__':
    main()