#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 16:20:08 2022

Class resample: 
    
    a class to resample the daily data from a dataframe and correlate the result
    to its corresponding GOES ESI data. 

@author: cwalker
"""
from class_SCAN import SCAN
import pandas as pd

##to get the data
from datasets import SCAN_READ

class resample(SCAN):
    
    def __init__(self, data):
        
        self.one_week_resampled = pd.DataFrame()
        self.two_week_resampled = pd.DataFrame()
        self.three_week_resampled = pd.DataFrame()
        self.four_week_resampled = pd.DataFrame()
        SCAN.__init__(self, data)

    
    
      
  
    
        
    ##class resamplers
    def one_week_resample(self):
        df = self.clean[['station', 'SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in', 'SMS-40.0in']]
        #compute the resample for each station in the dataframe:
        store={}
        for i in df['station'].unique():
            new_df = df[df['station']==i]
            one_week_resample = new_df.resample('1w').mean()
            one_week_resample['station'] = i
            one_week_resample
            store[i] = one_week_resample
        
        #create a newdataframe with the resample from store
        new_df = pd.concat(store, axis=0)
        new_df.index = new_df.index.get_level_values('Date')
        self.one_week_resampled = new_df
    
    def two_week_resample(self):
        df = self.clean[['station', 'SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in', 'SMS-40.0in']]
        #compute the resample for each station in the dataframe:
        store={}
        for i in df['station'].unique():
            new_df = df[df['station']==i]
            one_week_resample = new_df.resample('2w').mean()
            one_week_resample['station'] = i
            one_week_resample
            store[i] = one_week_resample
        
        #create a newdataframe with the resample from store
        new_df = pd.concat(store, axis=0)
        new_df.index = new_df.index.get_level_values('Date')
        self.two_week_resampled = new_df
    
    def three_week_resample(self):
        df = self.clean[['station', 'SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in', 'SMS-40.0in']]
        #compute the resample for each station in the dataframe:
        store={}
        for i in df['station'].unique():
            new_df = df[df['station']==i]
            one_week_resample = new_df.resample('3w').mean()
            one_week_resample['station'] = i
            one_week_resample
            store[i] = one_week_resample
        
        #create a newdataframe with the resample from store
        new_df = pd.concat(store, axis=0)
        new_df.index = new_df.index.get_level_values('Date')
        self.three_week_resampled = new_df
    
    def four_week_resample(self):
        df = self.clean[['station', 'SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in', 'SMS-40.0in']]
        #compute the resample for each station in the dataframe:
        store={}
        for i in df['station'].unique():
            new_df = df[df['station']==i]
            one_week_resample = new_df.resample('4w').mean()
            one_week_resample['station'] = i
            one_week_resample
            store[i] = one_week_resample
        
        #create a newdataframe with the resample from store
        new_df = pd.concat(store, axis=0)
        new_df.index = new_df.index.get_level_values('Date')
        self.four_week_resampled = new_df
    
        

        
        


