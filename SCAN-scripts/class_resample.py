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
from datasets import GOES_READ
import pandas as pd

dfgoes = GOES_READ[['StationTriplet', 'Date', 'ESI']]
dfgoes.set_index('Date', inplace=True)
dfgoes.rename(columns={'StationTriplet':'station'}, inplace=True)


class resample(SCAN):

    def __init__(self, data):
        
        self.sms_one_week_resampled = pd.DataFrame() #dataframe containing the one week resampled soil moisture data (rolling mean)
        self.sms_two_week_resampled = pd.DataFrame() #dataframe containing the two week resampled soil moisture data (rolling mean)
        self.sms_three_week_resampled = pd.DataFrame() #dataframe containing the three week resampled soil moisture data (rolling mean)
        self.sms_four_week_resampled = pd.DataFrame() #dataframe containing the four week resampled soil moisture data (rolling mean)
        self.ALEXI = dfgoes
        self.ALEXI_two_week_resampled = pd.DataFrame() #dataframe containing the two week resampled ALEXI data (using resample function)
        self.ALEXI_three_week_resampled = pd.DataFrame() #dataframe containing the three week resampled ALEXI data (using resample function)
        self.ALEXI_four_week_resampled = pd.DataFrame() #dataframe containing the four week resampled ALEXI data (using resample function)
        
        SCAN.__init__(self, data)
    
      
    
        
    ##class resamplers
    def soil_moisture_one_week_resample(self):
        print('\n')
        print('Resampling to 1w now!')
        
        df = self.clean[['station', 'SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in', 'SMS-40.0in']]
        #compute the resample for each station in the dataframe:
        store={}
        for i in df['station'].unique():
            new_df = df[df['station']==i]
            one_week_resample = new_df.rolling(7, min_periods=3).mean()
            one_week_resample['station'] = i
            store[i] = one_week_resample
        
        #create a newdataframe with the resample from store
        new_df = pd.concat(store, axis=0)
        new_df.index = new_df.index.get_level_values('Date')
        self.sms_one_week_resampled = new_df
        
        print('Stored 1w resample in resample class attributes called self.one_week_resampled')
        
    def soil_moisture_two_week_resample(self):
        print('\n')
        print('Resampling to 2w now!')
        
        df = self.clean[['station', 'SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in', 'SMS-40.0in']]
        #compute the resample for each station in the dataframe:
        store={}
        for i in df['station'].unique():
            new_df = df[df['station']==i]
            two_week_resample = new_df.rolling(14, min_periods=6).mean()
            two_week_resample['station'] = i
            store[i] = two_week_resample
        
        #create a newdataframe with the resample from store
        new_df = pd.concat(store, axis=0)
        new_df.index = new_df.index.get_level_values('Date')
        self.sms_two_week_resampled = new_df
        print('Stored 2w resample in resample class attributes called self.two_week_resampled')
        
    def soil_moisture_three_week_resample(self):
        print('\n')
        print('Resampling to 3w now!')
        
        df = self.clean[['station', 'SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in', 'SMS-40.0in']]
        #compute the resample for each station in the dataframe:
        store={}
        for i in df['station'].unique():
            new_df = df[df['station']==i]
            three_week_resample = new_df.rolling(21, min_periods=9).mean()
            three_week_resample['station'] = i
            store[i] = three_week_resample
        
        #create a newdataframe with the resample from store
        new_df = pd.concat(store, axis=0)
        new_df.index = new_df.index.get_level_values('Date')
        self.sms_three_week_resampled = new_df
        
        print('Stored 3w resample in resample class attributes called self.three_week_resampled')
        
    def soil_moisture_four_week_resample(self):
        print('\n')
        print('Resampling to 4w now!')
        
        df = self.clean[['station', 'SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in', 'SMS-40.0in']]
        #compute the resample for each station in the dataframe:
        store={}
        for i in df['station'].unique():
            new_df = df[df['station']==i]
            four_week_resample = new_df.rolling(28, min_periods=12).mean()
            four_week_resample['station'] = i
            store[i] = four_week_resample
        
        #create a newdataframe with the resample from store
        new_df = pd.concat(store, axis=0)
        new_df.index = new_df.index.get_level_values('Date')
        self.sms_four_week_resampled = new_df
    
        print('Stored 4w resample in resample class attributes called self.four_week_resampled')

        
        
    def ALEXI_two_week_resample(self):
        print('\n')
        print('Resampling ALEXI data to two weeks now!')
        df = self.ALEXI
        
        store = {}
        for i in df['station'].unique():
            new_df = df[df['station']==i]
            two_week_resample = new_df.resample('2w').mean()
            two_week_resample['station'] = i
            store[i] = two_week_resample

        new_df = pd.concat(store, axis=0)
        new_df.index = new_df.index.get_level_values('Date')
        new_df.reset_index(inplace=True)
        self.ALEXI_two_week_resampled = new_df
     
        print('Stored 2w resample in resample class attributes called self.ALEXI_two_week_resampled')
        
    def ALEXI_three_week_resample(self):
        print('\n')
        print('Resampling ALEXI data to three weeks now!')
        df = self.ALEXI
        
        store = {}
        for i in df['station'].unique():
            new_df = df[df['station']==i]
            three_week_resample = new_df.resample('3w').mean()
            three_week_resample['station'] = i
            store[i] = three_week_resample

        new_df = pd.concat(store, axis=0)
        new_df.index = new_df.index.get_level_values('Date')
        new_df.reset_index(inplace=True)
        self.ALEXI_three_week_resampled = new_df
     
        print('Stored 3w resample in resample class attributes called self.ALEXI_three_week_resampled')
        
    def ALEXI_four_week_resample(self):
        
        print('\n')
        print('Resampling ALEXI data to four weeks now!')
        df = self.ALEXI
        
        store = {}
        for i in df['station'].unique():
            new_df = df[df['station']==i]
            four_week_resample = new_df.resample('3w').mean()
            four_week_resample['station'] = i
            store[i] = four_week_resample

        new_df = pd.concat(store, axis=0)
        new_df.index = new_df.index.get_level_values('Date')
        new_df.reset_index(inplace=True)
        self.ALEXI_four_week_resampled = new_df
     
        print('Stored 4w resample in resample class attributes called self.ALEXI_four_week_resampled')