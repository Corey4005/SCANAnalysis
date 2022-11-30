#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 15:08:20 2022

This is a module to create a dataframe with NLCD land cover data for each SCAN site location. 
@author: cwalker
"""

#imports 
from datasets import scan_shape_files_list
from datasets import NLCD_geotiffs_path
from datasets import NLCD_list
import matplotlib.pyplot as plt
import rasterio
import rasterio.mask
from rasterio.plot import show
from rasterio.plot import show_hist
import pandas 
import fiona
import numpy as np

#set an outpath
nlcd_test = NLCD_list[0]
outpath = nlcd_test[:-5] + "_masked.tiff"
shape_test = scan_shape_files_list[1]

def open_raster(nlcd, shape):
    
    with fiona.open(shape) as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]
        
    
    with rasterio.open(nlcd) as src:
        print(src.crs)
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta
        
        
        
    out_meta.update({"driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform})
   
    with rasterio.open(outpath, "w", **out_meta) as dest:
        dest.write(out_image)
        
    clipped = rasterio.open(outpath)
    clipped_read = clipped.read(1)
    height = clipped_read.shape[0]
    width = clipped_read.shape[1]
    cols, rows = np.meshgrid(np.arange(width), np.arange(height))
    xs, ys = rasterio.transform.xy(src.transform, rows, cols)
    
    vMin = 0
    vMax = 100
    
    fig, ax = plt.subplots(figsize=(5, 5))
    rasterio.plot.show(clipped_read, 
                            transform=out_meta.get('transform'), 
                            ax=ax, 
                            cmap='hot_r', 
                            vmin=vMin, 
                            vmax=vMax)
    
    
    ax = plt.gca()
    
    return clipped_read