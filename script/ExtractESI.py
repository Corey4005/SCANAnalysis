# -*- coding: utf-8 -*-
"""
Script Decsription:
    Note:
        
    The filepath below is the location of the year sub-directories you want to grab 
    GOES .tif files from. The filepath in this script is set to my local 
    computer. This is because at the time of my use of this function, there
    was 80 GB worth of GOES sattelite images (20 years of daily data) to 
    process that cannot be uploaded to GitHub (too much space required). If 
    using this script, you will need to create your own filepath. It needs to 
    be the filepath to the rootfile containing the GOES (daily data for each 
    year) subdirectories. 
    
    metadata: 
    
    This is the file from USDA SCAN contatining the 
    station info for sites you are interested in comparing ESI from GOES too. 
    Example metadata columns:
    (['actonId', 'beginDate', 'countyName', 'elevation', 'endDate',
       'fipsCountryCd', 'fipsCountyCd', 'fipsStateNumber', 'huc', 'hud',
       'latitude', 'longitude', 'name', 'shefId', 'stationDataTimeZone',
       'stationTimeZone', 'stationTriplet', 'START_Date', 'geometry'],
      dtype='object')

Note:
    This script uses lat, lon and stationTriplet for each ESI pixel you are
    interested in grabing to compare to known soil moisture. 

   
author: Corey Walker - University of Alabama at Huntsville

"""
import rasterio
import glob2
import datetime as dt
import pandas as pd
import geopandas as gpd
import os
import itertools

#read in the filepath and metadata

filepath = r'C:\\Users\cwalker\Desktop\Data\ESI_Data\esi_1wk_tif'
metadata = r'C:\\Users\cwalker\Desktop\Data\Metadata\SCAN_Metadata_AL.csv'


#read int the metadata and make a geodataframe
meta_df = pd.read_csv(metadata)
gdf = gpd.GeoDataFrame(meta_df, geometry=gpd.points_from_xy(meta_df.longitude, meta_df.latitude))

#create a list of filepaths to extract the ESI data from
lis = [glob2.glob(root + '/*.tif') for (root, dirs, files) in os.walk(filepath)]
flat_list = itertools.chain(*lis)
files = list(flat_list)

#extract the ESI, datestring, lon and lat for files in the list
def ExtractESI(files):
    """
    Notes for using this function in a seperate script other than its original
    (for example: when importing function into another script)
    ----------------------------------------------------------------------
    
    Parameters: files - (list). This is the list of files from the filepath
    you want to iterate over. The filepaths must be raster files (.tif) to work. 
    Example code to create a 'files' variable:
        
        #bring in os and itertools
        import os
        import itertools
        
        #sample filepath to yearly subdirectories of 1wk GOES
        filepath = r'C:\\Users\cwalker\Desktop\Data\ESI_Data\esi_1wk_tif'
        
        #create a list of files to extract the ESI data from
        lis = [glob2.glob(root + '/*.tif') for (root, dirs, files) in os.walk(filepath)]
        flat_list = itertools.chain(*lis)
        files = list(flat_list)
        
        Sample Output 'files': 
            
            [...'C:\\\\Users\\cwalker\\Desktop\\Data\\ESI_Data\\esi_1wk_tif\\2001\\DFPPM_1WK_2001001.tif',
             'C:\\\\Users\\cwalker\\Desktop\\Data\\ESI_Data\\esi_1wk_tif\\2001\\DFPPM_1WK_2001008.tif',
             'C:\\\\Users\\cwalker\\Desktop\\Data\\ESI_Data\\esi_1wk_tif\\2001\\DFPPM_1WK_2001015.tif',
             'C:\\\\Users\\cwalker\\Desktop\\Data\\ESI_Data\\esi_1wk_tif\\2001\\DFPPM_1WK_2001022.tif',
             'C:\\\\Users\\cwalker\\Desktop\\Data\\ESI_Data\\esi_1wk_tif\\2001\\DFPPM_1WK_2001029.tif'...]
            
    Important: This function requires a global 'gdf' variable. Sample code to make 
    a gdf variable yourself: 
        
        # bring in pandas and GeoPandas
        import pandas as pd
        import geopandas as gpd
        
        # set the metadata filepath
        metadata = r'C:\\Users\cwalker\Desktop\Data\Metadata\SCAN_Metadata_AL.csv'
        
        #create the metadata dataframe
        meta_df = pd.read_csv(metadata)
        
        #make geometric points to use as an index for reading .tif files
        gdf = gpd.GeoDataFrame(meta_df, geometry=gpd.points_from_xy(meta_df.longitude, meta_df.latitude))
        
            
    
    Output: Returns a dataframe containing ESI, Lat, Lon, Date and 
    StationTriplet associated with Pixel. 
    
    """
    ESI = []
    Date = []
    Lat = []
    Lon = []
    Station = []
    for file in files:
        file_split = file.split('_')
        file_date = file_split[5].split('.tif')[0]
        when = dt.datetime.strptime(file_date, '%Y%j').date()
        raster = rasterio.open(file)
        print('processesing:', file)
        for point in gdf['geometry']:
            x = point.xy[0][0]
            y = point.xy[1][0]
            index = raster.index(x, y)
            values = raster.read(1)[index]
            formated = float("{:.3f}".format(values))
            ESI.append(formated)
            Date.append(when)
            Lon.append(x)
            Lat.append(y)
        for station in gdf['stationTriplet']:
            Station.append(station)
    ESI_data = pd.DataFrame(data={'ESI':ESI, 'Latitude':Lat, 'Longitude':Lon, 'Date':Date, 'StationTriplet':Station})
    ESI_data.to_csv('/Users/cwalker/Desktop/Data/Processed_ESI/1_wk_ESI_all.csv')
    print('Job Done!')
    return ESI_data

DataFrame = ExtractESI(files)
