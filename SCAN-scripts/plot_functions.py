#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:46:44 2022

@author: cwalker
"""
from datasets import SM_ANOM_ESI_BIN_READ
from datasets import SM_MEAN_STD_READ
from datasets import ALShape
from datasets import ALShape2
from datasets import cpc_path

from datasets import DataPath
import datetime
import os
import pandas as pd
import numpy as np
import rasterio
import fiona 
import rasterio.mask
from rasterio.plot import show
from rasterio.plot import show_hist
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
from descartes import PolygonPatch

getJDate = lambda x: x[-11:-4]


def make_filepaths_frame():
    """
    

    Returns
    -------
    dataframe containing the filepaths for each .tif folder and associated jdate
    
    Use
    -------
    df = make_filepaths_frame()

    """
    fileFrame = pd.DataFrame()
    data = DataPath
    fileList = []
    for root, dirs, files in os.walk(data):
        for f in files:
            filepath = root+'/'+f
            fileList.append(filepath)
    fileFrame['file'] = fileList
    fileFrame['jdate'] = fileFrame['file'].apply(getJDate)
    return fileFrame

def plot_SM_ANOM_for_ESI_date(df, year, month, day, volumetric=False, percentiles=False, droughtmonitor=False, SM_ANOM='4inANOM'):
      """
      

      Parameters
      ----------
      df : Pandas DataFrame
          Use make_filepaths_frame()
          ex: 
              df = make_filepaths_frame()
      year : int
          Four digit year.
      month : int
          two digit month
      day : int
          two digit day

      Returns
      -------
      Plot of soil moisture for ESI dataset at year, month, day. Requires data
      to be stored locally on the computer

      """
      df.sort_values('jdate', inplace=True) #sort the values so that you have them in correct order for comparison
      length = len(df)
      fmt = '%Y.%m.%d'
      year = str(year)
      month = str(month)
      day = str(day)
      s = year+'.'+month+'.'+day
      dt = datetime.datetime.strptime(s, fmt)
      tt = dt.timetuple()
      day = tt.tm_yday
      
      #here we are checking day types and assigning correct file structure number
      if day == 366:
          day = str(365)
          
      elif day < 10:
          day = '0'+str(day)+'0'
          
      elif day < 100: 
          day = '0'+str(day)
      elif day > 100:
          day = str(day)
    
      time = year+day
      if df[df['jdate']==time].empty==False: #if the data is availiable, plot it
          path = '/rhome/cwalker/Downloads/ALEXI/'+year+'/DFPPM_1WK_'+time+'.tif'
          outpath = '/rhome/cwalker/Downloads/ALEXI/'+year+'/masked_DFPPM_1WK_'+time+'.tif'
          print(path + " " + 'Here')
          
          
          with fiona.open(ALShape2) as shapefile:
              shapes = [feature["geometry"] for feature in shapefile]
              
          with rasterio.open(path) as src:
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
          clipped_read[clipped_read==-9999]=np.nan #set the no data values to nan
          height = clipped_read.shape[0]
          width = clipped_read.shape[1]
          cols, rows = np.meshgrid(np.arange(width), np.arange(height))
          xs, ys = rasterio.transform.xy(src.transform, rows, cols)
          
          if volumetric ==False: #if it is false, plot the anomalies 
          #go get values in the clipped array
              new_array = np.zeros(clipped_read.shape)
              for i in range(clipped_read.shape[0]):
                  for j in range(clipped_read.shape[1]):
                      value = clipped_read[i, j]
                      if value == 0.0:
                          new_array[i,j]=0.0
                      elif np.isnan(value):
                          new_array[i,j]=np.nan
                      elif value < -3:
                          new_array[i, j]=np.nan
                      elif value > 3: 
                          new_array[i, j]=np.nan
                      else:
                          new_array[i, j] = SM_ANOM_ESI_BIN_READ[(SM_ANOM_ESI_BIN_READ['upper bin']>value)&(SM_ANOM_ESI_BIN_READ['lower bin']<=value)][SM_ANOM].item()
              vMin=-0.6
              vMax=0.6
          
          elif volumetric ==True:
              if SM_ANOM == '2inANOM' or SM_ANOM == '4inANOM' or SM_ANOM == '8inANOM':
                  SM_ANOM_Depth = SM_ANOM[0:3]
                  SM_ANOM_Label = "Mean Volumetric " + SM_ANOM[0:3]
              else: 
                  SM_ANOM_Depth = SM_ANOM[0:4]
                  SM_ANOM_Label = "Mean Volumetric " + SM_ANOM[0:4]
                  
              new_array = np.zeros(clipped_read.shape)

              for i in range(clipped_read.shape[0]):
                  for j in range(clipped_read.shape[1]):
                      value = clipped_read[i, j]
                      if value == 0.0:
                          new_array[i,j] = np.nan
                      elif np.isnan(value):
                          new_array[i,j] = np.nan
                      else:
                          new_array[i,j] = (value*SM_MEAN_STD_READ[SM_ANOM_Depth+'AllWeeksSTDev'])+SM_MEAN_STD_READ[SM_ANOM_Depth+'AllWeeksMean']
              vMin=0.0
              vMax=60.0
              # maximum = np.nanmax(new_array)
              # minimum = np.nanmin(new_array)
              #  textstr = '\n'.join(( r'$\maximum=%.2f$' % (maximum, ), r'$\mathrm{minimum}=%.2f$' % (minimum, )))
              
              #  props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
              #  x = 0.35
              #  y = 0.15
              #  font = 12
          
                      
          if percentiles==True:
              
              percentiles_df = pd.DataFrame()
              location_list = []
              values = []
              index = []
              count = 0
              #get rid of 0 values in the new array and plot
              for i in range(new_array.shape[0]):
                  for j in range(new_array.shape[1]):
                      location_list.append([i,j])
                      value = new_array[i,j]
                      index.append(count)
                      count+=1
                      if value == 0.0:
                          new_array[i,j] = np.nan
                          values.append(np.nan)
                      elif value == np.nan:
                          new_array[i, j] = np.nan
                          values.append(np.nan)
                      else:
                          new_array[i, j] = value
                          values.append(value)
              
              if SM_ANOM == '2inANOM' or SM_ANOM == '4inANOM' or SM_ANOM == '8inANOM':
                  SM_ANOM_Depth = SM_ANOM[0:3]
                  SM_ANOM_Label = "Rank Percentile " + SM_ANOM[0:3]
              else: 
                  SM_ANOM_Depth = SM_ANOM[0:4]
                  SM_ANOM_Label = "Rank Percentile " + SM_ANOM[0:4]
                  
              percentiles_df['index'] = index
              percentiles_df['location']=location_list
              percentiles_df['values']=values
              percentiles_df['depth']=SM_ANOM
              percentiles_df['percentiles_rank'] = percentiles_df['values'].rank(pct=True)
              percentiles_df.set_index('index', inplace=True)
          
              for i in percentiles_df.index:
                  index = percentiles_df[percentiles_df.index==i]
                  location = index['location'].item()
                  percentile = index['percentiles_rank'].item()
                  new_array[location[0], location[1]] = percentile
                  
              vMin=0.0
              vMax=1.0
              
              if droughtmonitor==True:
                  countNone = 0
                  countD0 = 0
                  countD1 = 0
                  countD2 = 0
                  countD3 = 0
                  countD4 = 0
                  for i in range(new_array.shape[0]):
                      for j in range(new_array.shape[1]):
                          value = new_array[i, j]
                          if value >0.30:
                              countNone+=1
                          elif (value<=0.30)&(value>=0.21):
                              countD0+=1
                          elif(value<=0.20)&(value>=0.11):
                              countD1+=1
                          elif(value<=0.10)&(value>=0.06):
                              countD2+=1
                          elif(value<=0.03)&(value>=0.05):
                              countD3+=1
                          elif(value<=0.0)&(value>=0.02):
                              countD4+=1
                  for i in range(new_array.shape[0]):
                      for j in range(new_array.shape[1]):
                          value = new_array[i, j]
                          if(value >= 0.21) & (value<=0.30):
                              new_array[i, j]=0
                          elif(value >= 0.11) & (value<=0.21):
                              new_array[i, j]=1
                          elif(value >=0.06) & (value<=0.10):
                              new_array[i, j]=2
                          elif(value>=0.03)&(value<=0.05):
                              new_array[i, j]=3
                          elif(value>=0.00)&(value<=0.02):
                              new_array[i, j]=4
                          elif(value>0.30):
                              new_array[i, j]=np.nan
                              
                  for i in range(new_array.shape[0]):
                      for j in range(new_array.shape[1]):
                          print(new_array[i, j])
                 
              vMin=0
              vMax=4
              percentNone = countNone/new_array.size*100.0
              format_None = "{:.2f}".format(percentNone)
              percentD0 = countD0/new_array.size*100.0
              format_D0 = "{:.2f}".format(percentD0)
              percentD1= countD1/new_array.size*100.0
              format_D1 = "{:.2f}".format(percentD1)
              percentD2 = countD2/new_array.size*100.0
              format_D2 = "{:.2f}".format(percentD2)
              percentD3 = countD3/new_array.size*100.0
              format_D3 = "{:.2f}".format(percentD3)
              percentD4 = countD4/new_array.size*100.0
              format_D4 = "{:.2f}".format(percentD4)
              percentFrame = pd.DataFrame()
              percentFrame['cols']=['None', 'D0', 'D1', 'D2', 'D3', 'D4']
              percentFrame['percents']=[format_None, format_D0, format_D1, format_D2, format_D3, format_D4]
              print(percentFrame.transpose())
          #values for drought monitor - website: https://droughtmonitor.unl.edu/About/WhatistheUSDM.aspx
          # Dzero = np.nanpercentile(new_array, [21, 30]) #percentile 
          # Done = np.nanpercentile(new_array, [11, 20])
          # Dtwo = np.nanpercentile(new_array, [6, 10])
          # Dthree = np.nanpercentile(new_array, [3, 5])
          # Dfour = np.nanpercentile(new_array, [0, 2])
          if droughtmonitor==False:
              fig, ax = plt.subplots(figsize=(5, 5))
          # new_array=new
          # use imshow so that we have something to map the colorbar to
              image_hidden = ax.imshow(new_array, 
                                       cmap='jet_r', 
                                       vmin=vMin, 
                                       vmax=vMax)

          # plot on the same axis with raterio.plot.show
              rasterio.plot.show(new_array, 
                                 transform=out_meta.get('transform'), 
                                 ax=ax, 
                                 cmap='jet_r', 
                                 vmin=vMin, 
                                 vmax=vMax)
        

          # add colorbar using the now hidden image
              fig.colorbar(image_hidden, ax=ax)
              parsed = datetime.datetime.strptime(str(time), "%Y%j")
              ax.set_title(SM_ANOM_Label + " " + datetime.datetime.strftime(parsed, "%Y-%m-%d"))
              return new_array
          else:
              fig, ax = plt.subplots(figsize=(5, 5))
          # new_array=new
          # use imshow so that we have something to map the colorbar to
              image_hidden = ax.imshow(new_array, 
                                       cmap='hot_r', 
                                       vmin=vMin, 
                                       vmax=vMax)

          # plot on the same axis with raterio.plot.show
              rasterio.plot.show(new_array, 
                                 transform=out_meta.get('transform'), 
                                 ax=ax, 
                                 cmap='hot_r', 
                                 vmin=vMin, 
                                 vmax=vMax)
              ax = mpl.pyplot.gca()

              patches = [PolygonPatch(shape) for shape in shapes]
              ax.add_collection(mpl.collections.PatchCollection(patches, facecolor="none", edgecolor="black", alpha=0.5))
              cmap = mpl.cm.hot_r
              bounds = [0, 1, 2, 3, 4]
              norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend="min")
              # add colorbar using the now hidden image
              fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
              parsed = datetime.datetime.strptime(str(time), "%Y%j")
              ax.set_title("ESI Model to Drought Monitor" + " " + " " + datetime.datetime.strftime(parsed, "%Y-%m-%d"))
              return new_array
              
      else: #else if the data is not available, offer two other .tifs that are nearby in date
          print('{} not in file path as a .tif'.format(time))
          values = np.array(df['jdate'])
          count = 0
          # here we will use an algorithm to find the next best values if .tif does not exist and print to console
          for i in range(count, length):
              if i != length-1:
                  first = values[count]
                  count = count+1
                  second = values[count]
                  first = int(first)
                  second = int(second)
                  
                  if (first<int(time))&(second>int(time)):
                      parsedF = datetime.datetime.strptime(str(first), "%Y%j")
                      parsedS = datetime.datetime.strptime(str(second), "%Y%j")
                      print(datetime.datetime.strftime(parsedF, "%Y-%m-%d")+" "+'exists')
                      print(datetime.datetime.strftime(parsedS, "%Y-%m-%d")+" "+'exists')
                      break
                 

def plot_tif(tif):
    date_str = str(tif[-12:-4])
    datestr = datetime.datetime.strptime(date_str, '%Y%m%d')
   
    outpath = '/rhome/cwalker/Downloads/CPC_SM/masked.tif'
    with fiona.open(ALShape2) as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]
    
    with rasterio.open(tif) as src:
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
    
    new_array = np.zeros(clipped_read.shape)
    for i in range(clipped_read.shape[0]):
        for j in range(clipped_read.shape[1]):
            value = clipped_read[i, j]
            if value == 0.0:
                new_array[i, j]=np.nan
            else:
                new_array[i, j]=value/100
                
    height = clipped_read.shape[0]
    width = clipped_read.shape[1]
    cols, rows = np.meshgrid(np.arange(width), np.arange(height))
    xs, ys = rasterio.transform.xy(src.transform, rows, cols)
    
    fig, ax = plt.subplots(figsize=(5, 5))
    # new_array=new
    # use imshow so that we have something to map the colorbar to
    for i in range(new_array.shape[0]):
        for j in range(new_array.shape[1]):
            value = new_array[i, j]
            if(value >= 0.21) & (value<=0.30):
                new_array[i, j]=0
            elif(value >= 0.11) & (value<=0.21):
                new_array[i, j]=1
            elif(value >=0.06) & (value<=0.10):
                new_array[i, j]=2
            elif(value>=0.03)&(value<=0.05):
                new_array[i, j]=3
            elif(value>=0.00)&(value<=0.02):
                new_array[i, j]=4
            elif(value>0.30):
                new_array[i, j]=np.nan
    vMin=0
    vMax=4
    # image_hidden = ax.imshow(new_array, 
    #                          cmap='hot', 
    #                          vmin=vMin, 
    #                          vmax=vMax)

    # plot on the same axis with raterio.plot.show
    rasterio.plot.show(new_array, 
                           transform=out_meta.get('transform'), 
                           ax=ax, 
                           cmap='hot_r', 
                           vmin=vMin, 
                           vmax=vMax)
    
    
    ax = mpl.pyplot.gca()

    patches = [PolygonPatch(shape) for shape in shapes]
    ax.add_collection(mpl.collections.PatchCollection(patches, facecolor="none", edgecolor="black", alpha=0.5))
    cmap = mpl.cm.hot_r
    bounds = [0, 1, 2, 3, 4]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend="min")
    # add colorbar using the now hidden image
    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
    ax.set_title("CPC Model to Drought Monitor" + " " + str(datestr.year) + "-" + str(datestr.month)+ "-" + str(datestr.day))
    return new_array
    