#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 15:08:20 2022

This is a module to create a dataframe with NLCD land cover data for each SCAN site location. 
@author: cwalker
"""


# functions ------------------------------------------------------------------

#imports 
from datasets import scan_shape_files_list
print()
from datasets import NLCD_list
from datasets import SCAN_META_READ
import matplotlib.pyplot as plt
import rasterio
import rasterio.plot
import rasterio.mask
import geopandas as geo
import matplotlib as mpl
import geopandas as gpd
import numpy as np

#get the gdf of the scan site points
gdf = geo.GeoDataFrame(SCAN_META_READ, 
                       geometry=geo.points_from_xy(SCAN_META_READ.Longitude, 
                                                   SCAN_META_READ.Latitude), 
                       crs=4326)

gdf.to_crs(5070, inplace=True)


#class dictionary for each subclass
classDict = {0:"Water", 1:"Developed", 2:"Barren", 3:"Forest", 4:"Shrubland", 
             5:"Herbaceous", 6:"Planted/Cultivated", 7:"Wetlands"}

#function to open and return landcover array
def get_array(nlcd, shape, plot=False):
    outpath = nlcd[:-5]  + "_masked.tiff"
    year = nlcd[41:45]
    shape_name = shape[-12:-4]
    station_id = shape_name[-4:] + ":AL:SCAN"
    shape_read = geo.read_file(shape)
    shape = shape_read.to_crs(5070)
    with rasterio.open(nlcd) as src:
        
        out_image, out_transform = rasterio.mask.mask(src, shape.geometry, crop=True)
        out_meta = src.meta
        
        
        
    out_meta.update({"driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform})
   
    with rasterio.open(outpath, "w", **out_meta) as dest:
        dest.write(out_image)
        
    clipped = rasterio.open(outpath)
    clipped_read = clipped.read(1)
    
        
    #return a new array that removes zero values 
    new_array = np.zeros(clipped_read.shape)
    
    #clean up the array and get rid of zero values
    for i in range(clipped_read.shape[0]):
        for j in range(clipped_read.shape[1]):
            if clipped_read[i, j] == 0:
                new_array[i, j]=np.nan
            else:
                new_array[i, j]=clipped_read[i, j]
    
    #reclassify to shortened classes
    new_array = reclassify(new_array)
    
    if plot==True:
        
        vMin=0
        vMax=7
        
        fig, ax = plt.subplots(figsize=(15, 10))
        

    # plot on the same axis with raterio.plot.show
        
  
        
        rasterio.plot.show(new_array, 
                            transform=out_meta.get('transform'), 
                            ax=ax, 
                            cmap='jet',
                            vmin=vMin, 
                            vmax=vMax)
        
       
        
        cmap = mpl.cm.jet
        bounds = [0, 1, 2, 3, 4, 5, 6, 7]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend="min")
        
        # add colorbar using the now hidden image
        cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
        cbar.ax.set_yticklabels([classDict.get(i) for i in bounds])
   
        ax.set_title("NLCD {}".format(year))
        
        
        #plot the station 
        point = gdf[gdf['station']==station_id]['geometry'].values[0]
        x = point.x
        y = point.y
        
        ax.scatter(x, y, color='black', marker=".", s=800, label=station_id)
        
        ax.legend()
        ax.set_title('Example of Land Cover Class Diversity at {}'.format(station_id), fontsize=15)
        ax.yaxis.set_tick_params(labelsize=15)
        ax.xaxis.set_tick_params(labelsize=15)
        # print(shape_name, point)
    return new_array

#this function reclassifies the array into subclasses
def reclassify(array):
    new_array = np.zeros(array.shape)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if np.isnan(array[i, j]):
                new_array[i, j]=np.nan
            elif (array[i, j]== 11.0) | (array[i,j]==12.0):
                new_array[i, j]=0 #water
            elif (array[i, j]==21.0) | (array[i, j]==22.0) | (array[i, j]== 23.0) | (array[i, j]==24.0):
                new_array[i, j]=1 #Developed
            elif array[i, j]==31.0:
                new_array[i, j]=2 #barren
            elif (array[i, j]==41.0) | (array[i, j]==42.0) | (array[i, j]==43.0):
                new_array[i, j]=3 #forest
            elif (array[i, j]==51.0) | (array[i, j]==52.0):
                new_array[i, j]=4 #shrubland
            elif (array[i, j]==71.0) | (array[i, j]==72.0) | (array[i, j]==73.0) | (array[i,j]==74.0):
                 new_array[i, j]=5 #herbaceous
            elif (array[i,j]==81.0) | (array[i,j]==82.0):
                 new_array[i, j]=6 #Planted/Cultivated
            elif (array[i, j]==90.0) | (array[i, j]==95.0):
                 new_array[i, j]=7 #wetlands
    return new_array



#main ------------------------------------------------------------------------

# if you want to get all arrays do this section:
# #create a dictionary to hold arrays of landcover for each station
# landCoverDict = {}

# for i in range(len(NLCD_list)):
#     #get the year and the filepath
#     year = NLCD_list[i][41:45]
#     NLCD_file_path = NLCD_list[i]
    
#     for j in range(len(scan_shape_files_list)):
#         #get the shape name, read the shapefile, reproject it to NLCD, and get the landcover array
#         shape_name = scan_shape_files_list[j][-12:-4]
#         shapepath = scan_shape_files_list[j]
#         array = get_array(NLCD_file_path, shapepath, plot=False)
#         landCoverDict[year+shape_name]=array
#         print("Storing NLCD {} for {} in landCoverDict!".format(year, shape_name))

#plotting one 
shape_name = scan_shape_files_list[7][-12:-4] #2115
shapepath = scan_shape_files_list[7]
array = get_array(NLCD_list[0], shapepath, plot=True)