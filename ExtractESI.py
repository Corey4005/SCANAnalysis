# -*- coding: utf-8 -*-
"""
Parameters:
    filepath is set to my local computer. 
    metadata is set to my local computer. 

Note: 
    if you want the files to work on your computer, set the path variables to your local machine. I am working on 
    a couple of sys.argv arguments in a few days to make the files work more fluidly with different filepaths. 
    My next goal is to figure out a way to allow people to key in certain years and be able to pull down whichever
    data they would like. 

    
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
filepath = r'C:\\Users\cwalker\Desktop\Data\ESI_Data\esi_1wk_tif\2020'
metadata = r'C:\\Users\cwalker\Desktop\Data\Metadata\SCAN_Metadata_AL.csv'

#check to see if len of sys.argv is good. 
# if len(sys.argv) != 3:
#     print('usage: run ExtractESI.py [insert filepath as str], [insert metadata as str]')
#     sys.exit()
# else:
#     pass

#look for all files in filepath
files = glob2.glob(filepath + '/*.tif')
print(len(files))

#read int the metadata
import_csv = pd.read_csv(metadata)
df = pd.DataFrame(import_csv)
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
        
#extract the ESI, datestring, lon and lat for file in filepath
def ExtractESI(files):
    ESI = []
    Date = []
    Lat = []
    Lon = []
    for file in files:
        file_split = file.split('_')
        file_date = file_split[5].split('.tif')[0]
        when = dt.datetime.strptime(file_date, '%Y%j').date()
        raster = rasterio.open(file)
        for point in gdf['geometry']:
            x = point.xy[0][0]
            y = point.xy[1][0]
            index = raster.index(x, y)
            values = raster.read(1)[index]
            values_list = [values for value in index]
            ESI_values = values_list[0]
            formated = float("{:.3f}".format(ESI_values))
            ESI.append(formated)
            longitude = np.array(x)
            latitude = np.array(y)
            Date.append(when)
            Lon.append(longitude)
            Lat.append(latitude)
    df = pd.DataFrame(data={'ESI':ESI, 'Latitude':Lat, 'Longitude':Lon, 'Date':Date})
    df.to_csv('/Users/cwalker/Desktop/Data/Processed_ESI/1_wk_ESI_2020.csv')
    return
        
def main():
    ExtractESI(files)
    
if __name__ == '__main__':
    main()