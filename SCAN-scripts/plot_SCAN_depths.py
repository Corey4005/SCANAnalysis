#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 16:51:50 2022

@author: cwalker
"""

#imports 
import pandas as pd
from climatology_assumption import SCAN
from climatology_assumption import SCAN_READ
from climatology_assumption import theta_table
import matplotlib.pyplot as plt
import numpy as np


#data from theta_table sorted by negative r values
path = '../data/climatology_vs_Carsel_Parish.csv'
data = pd.read_csv(path)
negatives = data[data['theta_r_difference']<0]

#create an instance 
I = SCAN(data=SCAN_READ)

#clean the data
cleaned_df = I.standard_deviation_by_month().mean_soil_moisture_by_month().z_score().quality_z_score(std=3.5).clean_data().show()
cleaned_df = cleaned_df[['station', 'SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in',
                         'SMS-40.0in']]

#create theta table to index with
theta_tab = theta_table(cleaned_df)


def plot(df, station=None, depth=None, save_fig=False):
    '''
    

    Parameters
    ----------
    df : Pandas Dataframe
        Pass the cleaned_df variable from the climatology_assumption_effective_SM_conversion.py script. 
    station : str, not optional
        Set the station to the SCAN site you would like to plot.
        ex:
            station='2173:AL:SCAN'
    depth : str, not optional
        Set the depth by calling the column. You may call 2, 4, 8, 20 and 40 inches below the surface. 
        ex:
            depth='SMS-2.0in'

    Returns
    -------
    Lineplot of climatology with labeled theta_r, theta_s as well as a comparison to Parish et. al. lookup
    table and save to relevant filepath
    

    '''
    station_df = df[df['station'] == station][depth]
    tt = theta_tab[theta_tab['station'] == station]
    climate_theta_r = float(tt[tt['depths'] == depth]['assumed_climatology_theta_r'].item())
    climate_theta_s = float(tt[tt['depths'] == depth]['assumed_climatology_theta_s'].item())
    physical_theta_r = float(tt[tt['depths'] == depth]['physical_theta_r'].item())
    physcial_theta_s = float(tt[tt['depths'] == depth]['physical_theta_s'].item())
    fig, ax = plt.subplots(nrows=1,ncols=1)
    station_df.plot(ax=ax)
    ax.annotate('climate_r: {} \nphysical_r: {} \nclimate_s: {} \nphysical_s {}'
                .format(climate_theta_r, physical_theta_r, climate_theta_s, physcial_theta_s), 
                xy=(1.05,0), xycoords="axes fraction", bbox=dict(boxstyle="round", fc="w"))
    ax.set_title(station + ' ' + depth)
    figname = station[0:4] + '_' + depth[4:6]
    if save_fig == False:
        pass
    else:
        plt.savefig('../../SCANAnalysis/images/SCAN_CHECKS/' + figname, bbox_inches='tight')
    


def trend_plots(df, station, depth, save_fig=False):
    '''
    

    Parameters
    ----------
    df : Pandas Dataframe
        Pass the cleaned_df variable from the climatology_assumption_effective_SM_conversion.py script.
        
    station : str, not optional
        Set the station to the SCAN site you would like to plot.
        ex:
            station='2057:AL:SCAN'
            
    depth : str, not optional
        Set the depth by calling the column. You may call 2, 4, 8, 20 and 40 inches below the surface. 
        ex:
            depth='SMS-4.0in'
        
    save_fig : bool, optional
        Set this to true to save images to the filepath referenced in the code below. The default is False.

    Returns
    -------
    Scatterplot of monthly averaged SCAN site data with trendline with important 
    annotations like slope, soil, and look-up table comparisons with the
    theta-r and theta-s for climatology. 
    
    '''
    
    #create storage location to concat data to
    store = {}
    
    #this piece of code grabs the df at the passed station and returns 
    #each month mean for each year and stores it in a dictionary
    df = df[df['station']==station]
    for y in df.index.year:
        year_frame = df[df.index.year==y]
        month_frame = year_frame.groupby(year_frame.index.month).mean()
        store[y] = month_frame
    
    #concat all the storage variables together to get one dataframe of month
    #means by year
    avg_frame = pd.concat(store, axis=0)
    
    #storage for date variables
    dates = []
    
    #this grabs the year and the month from the index and returns the month
    #and year so that we can set a column in the dataframe that drops the day
    #variable
    for i in avg_frame.index:
        year = str(i[0])
        month = str(i[1])
        dates.append(year+'-'+month)
    
    #this piece of code sets the column and coverts it to datetime so that 
    #months and dates can be called. 
    avg_frame['Year-Month'] = dates
    avg_frame['Year-Month'] = pd.to_datetime(avg_frame['Year-Month'])

    avg_frame.set_index('Year-Month', inplace=True)
    avg_frame = avg_frame[['SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in', 
                           'SMS-40.0in']]
    
    avg_frame.dropna(axis=0, inplace=True)
    length = range(0,len(avg_frame))
    avg_frame['length'] = length
    
    fig, ax = plt.subplots()
    x = avg_frame['length'] 
    y = avg_frame[depth]
    ax.plot(x,y,'o', markersize=4)
    
    z = np.polyfit(x,y,deg=1)
    p = np.poly1d(z)
    ax.plot(x, p(x), 'r-')
    
    
    #load in theta table for station to get climate variables
    tt = theta_tab[theta_tab['station'] == station]
    
    #variables we want to annotate on plots
    climate_theta_r = '{:.3f}'.format(avg_frame[depth].min()/100)
    climate_theta_s = '{:.3f}'.format(avg_frame[depth].max()/100)
    physical_theta_r = float(tt[tt['depths'] == depth]['physical_theta_r'].item())
    physcial_theta_s = float(tt[tt['depths'] == depth]['physical_theta_s'].item())
    soiltype = tt[tt['depths'] == depth]['soiltype'].item()
    slope = '{:.3f}'.format(z[0])
    ax.annotate('slope: {} \nsoil: {} \nclimate_r: {} \nphysical_r: {} \nclimate_s: {} \nphysical_s {}'
                .format(slope, soiltype, climate_theta_r, physical_theta_r, climate_theta_s, physcial_theta_s), 
                xy=(1.05,0), xycoords="axes fraction", bbox=dict(boxstyle="round", fc="w"))
    ax.set_title(station + ' ' + depth)
    
    #save
    figname = station[0:4] + '_' + depth[4:6]
    if save_fig == False:
        pass
    else:
        plt.savefig('../../SCANAnalysis/images/trend_plots/' + figname, bbox_inches='tight')
    
    

def plot_all_stns_trend():
    '''
    

    Returns
    -------
    Plots all the stations at each depth from the clean 3.5 standard deviation 
    dataframe and saves it to the filepath referenced in trendplots() function. 

    '''
    for i in cleaned_df['station'].unique():
        count = 0
        print('Plotting trends for station {}'.format(i) + ' ' + 'now!')
        count = count + 1
        for j in cleaned_df[['SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in', 'SMS-40.0in']]:
            trend_plots(cleaned_df, i, j, save_fig=False)
        