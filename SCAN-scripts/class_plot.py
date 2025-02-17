#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 15:21:43 2022

@author: cwalker
"""

from class_correlate import Correlate
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from datasets import SCAN_META_READ
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np
import datetime


class Plot(Correlate):

  def __init__(self, data):
      
      Correlate.__init__(self, data)
      self.stations_corr_by_month = pd.DataFrame()
      self.time_series_box_plot_df = pd.DataFrame()
      self.tree_cover_sig_df = pd.DataFrame()
      self.station_sig_by_month = pd.DataFrame()
    
  def plot_stations_corr_by_depth(self, depth=None, resample_type='1w', hue=False):
      while depth==None:
          print('Pass the depth you would like to get. For example: \n')
          print('SMS-2.0in, SMS-4.0in, SMS-8.0in, SMS-20.0in, SMS-40.0in')
          break
          
      if resample_type == '1w':
          df = self.merge1wALEXI
      
      elif resample_type == '2w':
          df = self.merge2wALEXI
      elif resample_type == '3w':
          df = self.merge3wALEXI
      elif resample_type == '4w':
          df = self.merge4wALEXI

      correlation = []
      month = []
      station = []
      num_observations = []
      soil_types = []
      soil_key = {'SMS-2.0in':'Two Soil Reclassified', 'SMS-4.0in':'Four Soil Reclassified', 'SMS-8.0in':'Eight Soil Reclassified', 
                  'SMS-20.0in':'Twenty Soil Reclassified', 'SMS-40.0in':'Forty Soil Reclassified'}
      for s in df['station'].unique():
          new_df = df[df['station'] ==s]
          for m in new_df['Date'].dt.month.unique():
              month_frame = new_df[new_df['Date'].dt.month == m]
              count = month_frame[depth].count()
              corr = month_frame.corr()['ESI'][depth]
              soil = month_frame[soil_key.get(depth)].unique().item()
              soil_types.append(soil)
              num_observations.append(count)
              correlation.append(corr)
              month.append(m)
              station.append(s)
              
      self.stations_corr_by_month['Correlation'] = correlation
      self.stations_corr_by_month['Month'] = month
      self.stations_corr_by_month['Station'] = station
      self.stations_corr_by_month['Observations'] = num_observations
      self.stations_corr_by_month['Soil'] = soil_types
          
      #plot
      self.__plot_corr_by_month(depth_input=depth, resample_input=resample_type, hue=hue)
  
  def create_time_series_box_plot_df(self):
      
      soil_key = {'SMS-2.0in': 'Two Soil Reclassified',
       'SMS-4.0in': 'Four Soil Reclassified',
       'SMS-8.0in': 'Eight Soil Reclassified',
       'SMS-20.0in': 'Twenty Soil Reclassified',
       'SMS-40.0in': 'Forty Soil Reclassified'}
      
      df_list = [self.merge1wALEXI, self.merge2wALEXI, self.merge3wALEXI, self.merge4wALEXI]
      count = 0
      month_list = []
      station_list = []
      corr_list = []
      sig_list = []
      soil_list = []
      resample_list = []
      depth_list = []
      num_observations = []
      
      for x, y in enumerate(df_list): 
          df = df_list[x]
          count += 1
          if count == 1:
              r = '1w'
          elif count == 2:
              r = '2w'
          elif count == 3:
              r = '3w'
          elif count == 4:
              r = '4w'
              
          for i in df['Date'].dt.month.unique():
              monthframe = df[df['Date'].dt.month == i]
              for s in monthframe['station'].unique():
                  stationframe = monthframe[monthframe['station'] == s]
                  for j in ['SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in', 'SMS-40.0in']:
                      
                      if stationframe[j].count() < 2:
                          print(str(s) + ' ' + str(j) + ' ' + 'does not have enough samples to test for correlation')
                      else:
                          newframe = stationframe[['ESI', j]].dropna()
                          observation_count = len(newframe)
                          R, p = stats.pearsonr(newframe[j], newframe['ESI'])
                          soil = stationframe[soil_key.get(j)].unique().item()
                          num_observations.append(observation_count)
                          month_list.append(i)
                          station_list.append(s)
                          corr_list.append(R)
                          sig_list.append(p)
                          soil_list.append(soil)
                          resample_list.append(r)
                          depth_list.append(j)
                          
      
      self.time_series_box_plot_df['Month'] = month_list
      self.time_series_box_plot_df['station'] = station_list
      self.time_series_box_plot_df['correlation'] = corr_list
      self.time_series_box_plot_df['signifigance'] = sig_list
      self.time_series_box_plot_df['soil'] = soil_list
      self.time_series_box_plot_df['resample list'] = resample_list
      self.time_series_box_plot_df['depth'] = depth_list
      self.time_series_box_plot_df['observations'] = num_observations
      
  def plot_time_series_boxplot(self, resample_input=None, soil_type=None, depth_input=None):
      
      depth_input_color = {'SMS-2.0in':'red', 'SMS-4.0in':'royalblue', 'SMS-8.0in':'seagreen', 'SMS-20.0in':'darkorange', 'SMS-40.0in':'black'}
      if (resample_input==None) and (soil_type==None) and (depth_input==None):
          df = self.time_series_box_plot_df
          fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, sharey=True, figsize=(15, 20))
          sns.boxplot(x='Month', y='correlation', hue='depth', ax=ax1, data=df)
          ax1.legend(bbox_to_anchor=(1.0, 1.0))
          ax1.set_title('18 Alabama SCAN Stations by Depth and Month vs ALEXI Correlation')
          sns.boxplot(x='Month', y='correlation', hue='soil', ax=ax2, data=df)
          ax2.set_title('18 Alabama SCAN Stations by Hydrologic Soil Type and Month vs ALEXI Correlation')
          ax2.legend(bbox_to_anchor=(1.0, 1.0))
          sns.boxplot(x='Month', y='correlation', hue='resample list', ax=ax3, data=df)
          ax3.set_title('18 Alabama SCAN Stations by Resample Type and Month vs ALEXI Correlation')
          ax3.legend(bbox_to_anchor=(1.0, 1.0))
      elif (resample_input!=None) and (soil_type==None) and (depth_input==None):
          df = self.time_series_box_plot_df[self.time_series_box_plot_df['resample list']==resample_input]
          fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, sharey=True, figsize=(15, 20))
          sns.boxplot(x='Month', y='correlation', hue='depth', ax=ax1, data=df, notch=True)
          ax1.legend(bbox_to_anchor=(1.0, 1.0))
          ax1.set_title(str(resample_input) + ' ' + 'resampled Alabama SCAN vs ALEXI by Depth and Month Correlations')
          sns.boxplot(x='Month', y='correlation', hue='soil', ax=ax2, data=df, notch=True)
          ax2.set_title(str(resample_input) + ' ' + 'resampled Alabama SCAN vs ALEXI by Hydrologic Soil Type and Month Correlations')
          ax2.legend(bbox_to_anchor=(1.0, 1.0))
      elif (resample_input!=None) and (soil_type!=None) and (depth_input==None):
          df = self.time_series_box_plot_df[(self.time_series_box_plot_df['resample list']==resample_input) & (self.time_series_box_plot_df['soil']==soil_type)]
          fig, ax1 = plt.subplots(sharex=True, sharey=True, figsize=(15, 10))
          sns.boxplot(x='Month', y='correlation', hue='depth', ax=ax1, data=df, notch=True)
          ax1.legend(bbox_to_anchor=(1.0, 1.0))
          ax1.set_title(str(resample_input) + ' ' + 'resampled Alabama SCAN vs ALEXI by' + ' ' + str(soil_type) + ' '+ 'Hydrologic Soil Type and Month Correlations')
      
      elif (resample_input!=None) and (soil_type!=None) and (depth_input!=None):
          df = self.time_series_box_plot_df[(self.time_series_box_plot_df['resample list']==resample_input) & (self.time_series_box_plot_df['soil']==soil_type) & (self.time_series_box_plot_df['depth']==depth_input)]
          fig, ax1 = plt.subplots(sharex=True, sharey=True, figsize=(15, 10))
          sns.boxplot(x='Month', y='correlation', ax=ax1, data=df, color=depth_input_color.get(depth_input))
          ax1.legend(bbox_to_anchor=(1.0, 1.0))
          ax1.set_title(str(resample_input) + ' ' + 'resampled Alabama SCAN vs ALEXI by' + ' '+ 'Hydrologic Soil Type' + ' ' + str(soil_type) + ' ' + 'and Month at'+ ' '+ str(depth_input) + ' '+ 'Correlations')
  
  def plot_sig_box_plot_stations_by_month(self, resample_input=None, depth_input=None):

      sig_df = self.time_series_box_plot_df[(self.time_series_box_plot_df['signifigance']<0.05) & (self.time_series_box_plot_df['resample list']==resample_input) & (self.time_series_box_plot_df['depth']==depth_input)]
      
      fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15,10))
      sig_df_p = sig_df[sig_df['correlation']>0]
      sns.boxplot(x='Month',y='correlation', data=sig_df_p, ax=ax1)
      ax1.set_title(str(resample_input) + ' ' + str(depth_input)+ ' ' + '<0.05 p-value Station Correlations', fontsize=15, fontweight='bold')
      ax1.set_xlabel('Month', fontsize=15, fontweight='bold')
      ax1.set_ylabel('Correlation', fontsize=15, fontweight='bold')
      for l in ax1.get_xticklabels():
          l.set_weight('bold')
          l.set_fontsize(15)
      for l in ax1.get_yticklabels():
          l.set_weight('bold')
          l.set_fontsize(15)
      
      count_list = []
      month_list = []
      for i in sig_df_p['Month'].unique():
          df = sig_df_p[sig_df_p['Month']==i]
          count = len(df['station'].unique())
          month_list.append(i)
          count_list.append(count)
      
      station_count_df = pd.DataFrame()
      station_count_df['station count'] = count_list
      station_count_df['month'] = month_list
      sns.barplot(x='month', y='station count', data=station_count_df, ax=ax2)
      ax2.set_xlabel('Month', fontsize=15, fontweight='bold')
      ax2.set_ylabel('Station Count', fontsize=15, fontweight='bold')
      for l in ax2.get_xticklabels():
          l.set_weight('bold')
          l.set_fontsize(15)
      for l in ax2.get_yticklabels():
          l.set_weight('bold')
          l.set_fontsize(15)
          
  def station_signifigance_plots_lat_lon_month(self, resample_input=None, depth_input=None):
      sig_df = self.time_series_box_plot_df[(self.time_series_box_plot_df['signifigance']<0.05) & (self.time_series_box_plot_df['resample list']==resample_input) & (self.time_series_box_plot_df['depth']==depth_input)]
      final_df = sig_df.merge(SCAN_META_READ, on='station')
      
      fig = plt.figure()
      ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree())
      ax.set_extent([final_df['Longitude'].min()-0.5, final_df['Longitude'].max()+0.5, final_df['Latitude'].min()-0.5, final_df['Latitude'].max()+0.5], 
                    ccrs.PlateCarree())
      
      states_provinces = cfeature.NaturalEarthFeature(
          category='cultural',
          name='admin_1_states_provinces_lines',
          scale='10m',
          facecolor='none')
      
      ax.coastlines(resolution='10m')
      ax.add_feature(cfeature.LAND)
      ax.add_feature(cfeature.COASTLINE)
      ax.add_feature(states_provinces, edgecolor='k')
      ax.add_feature(cfeature.BORDERS)
      gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                    linewidth=1.0, color='gray', alpha=0.5, linestyle='--')
      gl.xlabels_top = False
      gl.ylabels_left = True
      gl.ylabels_right = False
      gl.xlines = True
      gl.xlocator = mticker.FixedLocator(np.linspace(final_df['Longitude'].min()-0.5, final_df['Longitude'].max()+0.5, 8))
      gl.ylocator = mticker.FixedLocator(np.linspace(final_df['Latitude'].min()-0.5, final_df['Latitude'].max()+0.5, 8))
      gl.xformatter = LONGITUDE_FORMATTER
      gl.yformatter = LATITUDE_FORMATTER
      gl.xlabel_style = {'size': 15, 'color': 'gray'}
      gl.xlabel_style = {'color': 'black', 'weight': 'bold'}
      gl.ylabel_style = {'size': 15, 'color': 'gray'}
      gl.ylabel_style = {'color': 'black', 'weight': 'bold'}
      
      lat = final_df['Latitude'].unique()
      lon = final_df['Longitude'].unique()
      ax.scatter(lon, lat, s=50, color='red', transform=ccrs.PlateCarree())
      plt.show()
      self.station_sig_by_month = final_df
      

      
  #helper function
  def __plot_corr_by_month(self, depth_input, resample_input, hue):
      
      df = self.stations_corr_by_month
      
      
      if hue==False:
          
          fig, ax = plt.subplots()
          
          for i in df['Station'].unique():
          
              new_df = df[df['Station'] == i]
              plot = sns.scatterplot(x='Month', y='Correlation', data=new_df, label=new_df['Station'].unique().item(), palette='coolwarm', ax=ax)
              plot.set_title(str(resample_input) + ' ' + 'SCAN Data vs' + ' ' + str(resample_input) + ' '+ 'ALEXI by Month and Station at' + ' ' + str(depth_input))
          
          plt.legend(bbox_to_anchor=(1.02, 1), borderaxespad=0)
      else: 
          
          my_colors = {'A': 'red', 'B': 'green', 'C': 'blue', 'D': 'yellow'}
          
          fig, ax = plt.subplots()
          
          for i in df['Station'].unique():
              new_df = df[df['Station'] == i]
              for j in new_df.iterrows():
                  soil_type = my_colors.get(j[1][4])
                  print(soil_type)
                  if soil_type =='yellow':
                      plot = ax.scatter(j[1][1], j[1][0], color=my_colors.get(j[1][4]), label='D')
                  elif soil_type =='red':
                      plot = ax.scatter(j[1][1], j[1][0], color=my_colors.get(j[1][4]), label='A')
                  elif soil_type=='blue':
                      plot = ax.scatter(j[1][1], j[1][0], color=my_colors.get(j[1][4]), label='C')
                  elif soil_type=='green':
                      plot = ax.scatter(j[1][1], j[1][0], color=my_colors.get(j[1][4]), label='B')
              
              handles, labels = plt.gca().get_legend_handles_labels()
              by_label = dict(zip(labels, handles))
              plt.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.15, 1), borderaxespad=0)
          
          ax.set_title(str(resample_input) + ' ' + 'Alabama SCAN Data vs' + ' ' + str(resample_input) + ' '+ 'ALEXI, hued by Soil Type at' + ' ' + str(depth_input))
          plt.xlabel('Month')
          plt.ylabel('Correlation')