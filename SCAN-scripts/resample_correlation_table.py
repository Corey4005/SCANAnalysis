#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 16:20:08 2022

Class resample: 
    
    a class to resample the daily data from a dataframe and correlate the result
    to its corresponding GOES ESI data. 

@author: cwalker
"""
from climatology_assumption import SCAN, SCAN_READ
import pandas as pd

class resample:
    
    def __init__(self, data):
        """
        Purpose: 
            resample class constructor.

        Parameters
        ----------
        data : Pandas DataFrame
            Pass the SCAN_READ object from the SCAN class in class_SCAN.py

        Returns
        -------
        self.scan_instance - constructed SCAN object
        self.stdev - monthly standard deviation dataframe for each SCAN station
        self.mean - monthly mean dataframe for each SCAN station
        self.z_score - dataframe containing the z_score for each SCAN observation
        self.quality - dataframe containing the quality of each SCAN observation
        self.clean - dataframe containing the cleaned data.
        self.resampled - dataframe of resampled data (can be empty, 1w, 2w, 3w, and 4w resamples).
        self.soil - dataframe containing the 
        

        """
        #data from scan object
        self.scan_instance = SCAN(data=SCAN_READ)
        self.stdev = self.scan_instance.standard_deviation_by_month()
        self.mean = self.scan_instance.mean_soil_moisture_by_month()
        self.z_score = self.scan_instance.z_score()
        self.quality = self.scan_instance.quality_z_score(std=3.5) ## 'good data' is 3.5 standard deviations
        self.clean = self.scan_instance.clean_data().show()
        self.resampled = pd.DataFrame()   
        self.soil = pd.DataFrame()
    
    ## class getters 
    def get_stdev_df(self):
        return self.stdev
    
    def get_mean_df(self):
        return self.mean
    
    def get_z_score_df(self):
        return self.z_score
    
    def get_quality_df(self):
        return self.quality
    
    def get_clean_data(self):
        return self.clean
    
    def get_resampled_df(self):
        df = self.resampled
        if df.empty:
            print('Dataframe is empty. Use a resample function.')
        else:
            return self.resampled
    
    def get_soil_df(self):
        df = self.soil
        if df.empty:
            print('Dataframe is empty. Use a resample function, then the soils function.')
        else:
            return self.soil
        
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
        self.resampled = new_df
    
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
        self.resampled = new_df
    
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
        self.resampled = new_df
    
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
        self.resampled = new_df
    
    def append_soils(self, df):
        dict_list = []
        for i in df['station']:
            if i == '2057:AL:SCAN':
                soil_dict = {'two':'SICL', 'four':'SICL', 
                         'eight':'SICL', 'twenty':'SICL', 
                         'forty':'SICL'}
                dict_list.append(soil_dict)
    
            elif i == '2113:AL:SCAN':
                #two in and four in are fine sandy loam
                soil_dict = {'two':'FSL', 'four':'FSL', 
                         'eight':'FSL', 'twenty':'L', 
                         'forty':'L'}
                dict_list.append(soil_dict)
    
            elif i == '2055:AL:SCAN':
                #two and four in are gravelly
                soil_dict = {'two': 'GRSIL', 'four': 'GRSIL', 
                         'eight':'GRSIL', 'twenty': 'SICL', 
                         'forty': 'SICL'}
                dict_list.append(soil_dict)
            
            elif i == '2180:AL:SCAN':
                soil_dict = {'two': 'SL', 'four': 'SL', 
                         'eight':'SL', 'twenty': 'SL', 
                         'forty': 'SCL'}
            
                dict_list.append(soil_dict)
            
            elif i == '2114:AL:SCAN': 
                soil_dict = {'two': 'SIL', 'four': 'SIC', 
                         'eight':'C', 'twenty': 'C', 
                         'forty': 'C'}
            
                dict_list.append(soil_dict)
        
            elif i == '2056:AL:SCAN':
                soil_dict = {'two': 'L', 'four': 'L', 
                          'eight':'CL', 'twenty': 'C', 
                          'forty':'C'}
                
                dict_list.append(soil_dict)
            
            elif i == '2115:AL:SCAN':
            
                soil_dict = {'two': 'LS', 'four': 'LS', 
                          'eight':'SL', 'twenty': 'SCL', 'forty': 'CL'}
            
                dict_list.append(soil_dict)
            
            elif i == '2053:AL:SCAN':
            
                soil_dict = {'two': 'SICL', 'four': 'SIL', 
                          'eight':'SIL', 'twenty': 'SICL', 
                          'forty': 'CL'}
        
        
                dict_list.append(soil_dict)
        
                #new stations with assumptions
            elif i == '2078:AL:SCAN':
            
                soil_dict = {'two': 'SICL', 'four': 'SIL', 
                         'eight': 'SICL', 'twenty': 'SICL', 
                         'forty': 'CL'}
            
                dict_list.append(soil_dict)
            
            elif i == '2177:AL:SCAN':
                #using lab measurements
            
                soil_dict = {'two': 'SIC', 'four': 'SIC',
                         'eight': 'SIC', 'twenty': 'SIC', 
                         'forty': 'SIC'}
            
                dict_list.append(soil_dict)
            
            elif i == '2173:AL:SCAN':
                #using lab measurements
                soil_dict = {'two': 'SIL', 'four': 'SIL',
                         'eight': 'SICL', 'twenty': 'SICL', 
                         'forty': 'C'}
            
                dict_list.append(soil_dict)
        
            elif i == '2178:AL:SCAN':
                #using lab measures
                soil_dict = {'two': 'FSL', 'four': 'FSL', 
                         'eight': 'FSL', 'twenty': 'FSL', 
                         'forty': 'L'}
            
                dict_list.append(soil_dict)
        
            elif i == '2175:AL:SCAN':
                #using lab measures
                soil_dict = {'two': 'L', 'four': 'L', 
                         'eight': 'L', 'twenty': 'L', 
                         'forty': 'C'}
            
                dict_list.append(soil_dict)
            
            elif i == '2174:AL:SCAN':
                #using web soil survey
                soil_dict = {'two': 'SIC', 'four': 'SIC', 
                         'eight': 'C', 'twenty': 'C',
                         'forty': 'C'}
        
                dict_list.append(soil_dict)
            elif i == '2182:AL:SCAN':
                #using web soil survey
            
                soil_dict = {'two': 'LS', 'four': 'LS',
                         'eight': 'LS', 'twenty': 'FS',
                         'forty': 'SL'}
        
                dict_list.append(soil_dict)
            
            elif i == '2179:AL:SCAN':
                #lab measures and websoil survey
        
                soil_dict = {'two': 'FSL', 'four': 'FSL', 
                         'eight': 'FSL', 'twenty': 'FSL',
                         'forty': 'BRCK'}
            
                dict_list.append(soil_dict)
        
            elif i == '2181:AL:SCAN':
                #using websoil survey
        
                soil_dict = {'two': 'FSL', 'four': 'FSL', 
                         'eight': 'FSL', 'twenty': 'SL',
                         'forty': 'SCL'}
            
                dict_list.append(soil_dict)
            
            elif i == '2176:AL:SCAN':
                #using websoil survey
        
                soil_dict = {'two': 'FS', 'four': 'FS', 
                         'eight': 'FS', 'twenty': 'S',
                         'forty': 'S'}
            
                dict_list.append(soil_dict)
            
        df['Soil Class Dictionary'] = dict_list
        
        ################# UNPACK ####################
        
        ##lists to store value objects
        two_soil = []
        four_soil = []
        eight_soil = []
        twenty_soil = []
        forty_soil = []
        
        #for loop to get key from each entry and append to value list
        for i in df['Soil Class Dictionary']:
            two = i.get('two')
            four = i.get('four')
            eight = i.get('eight')
            twenty = i.get('twenty')
            forty = i.get('forty')
            two_soil.append(two)
            four_soil.append(four)
            eight_soil.append(eight)
            twenty_soil.append(twenty)
            forty_soil.append(forty)
        
        ##create dataframe columns with the lists of data
        df['Two Soil'] = two_soil
        df['Four Soil'] = four_soil
        df['Eight Soil'] = eight_soil
        df['Twenty Soil'] = twenty_soil
        df['Forty Soil'] = forty_soil
            
        self.soil = df
        
    def create_soil_columns(self):
    
        resampled = self.resampled
        clean = self.clean
        if resampled.empty:
            self.append_soils(clean)
            print('self.soil attribute has been updated with self.clean data and appended soil columns')
        else:
            self.append_soils(resampled)
            print('self.soil attribute has been updated with self.resampled data and appended soil columns')
            
            
        
        
        


