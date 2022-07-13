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
from datasets import GOES_READ, SCAN_READ


class resample(SCAN):
    
    def __init__(self, data):
       #this initializes the resample class with a clean dataset by inheriting from SCAN and calling the methods
       #from the class
        SCAN.__init__(self, data)
        SCAN.standard_deviation_by_month(self)
        SCAN.mean_soil_moisture_by_month(self)
        SCAN.z_score(self)
        SCAN.quality_z_score(self, std=3.5)
        SCAN.clean_data(self)
        self.resampled = pd.DataFrame()
        self.soil = pd.DataFrame()
        self.merged = pd.DataFrame()
        
    def get_clean_data(self):
        "return the clean data from SCAN and print to terminal"
        return self.stations
    
    def get_resampled(self):
        return self.resampled
    
    def get_soils(self):
        return self.soil
    
    def one_week_resample(self):
        df = self.stations[['station', 'SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in', 'SMS-40.0in']]
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
        df = self.stations[['station', 'SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in', 'SMS-40.0in']]
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
        df = self.stations[['station', 'SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in', 'SMS-40.0in']]
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
        df = self.stations[['station', 'SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in', 'SMS-40.0in']]
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
        
    def append_soils(self, resampled=False):
        dict_list = []
        if resampled:
            df = self.resampled
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
            self.soil = df
        
        else:
            df = self.stations
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
            self.soil = df
                
        
    
    def unpack_soils(self):
        '''
        Purpose: Unpack the self.stations dataframe containing the soil texture
            class dictionaries and return pandas column with the soil
            texture class for each depth. 
            
        returns: updated self.stations dataframe. 
        '''
        
    
        #lists 
        two_in = []
        four_in = []
        eight_in = []
        twenty_in = []
        forty_in = []
        
        #get two
        for i in self.soil['Soil Class Dictionary']:
            two = i.get('two')
            two_in.append(two)
        
        self.soil['two_in_soil'] = two_in
        
        #get four
        for i in self.soil['Soil Class Dictionary']:
            four = i.get('four')
            four_in.append(four)
        
        self.soil['four_in_soil'] = four_in
                
        for i in self.soil['Soil Class Dictionary']:
            eight = i.get('eight')
            eight_in.append(eight)
        
        self.soil['eight_in_soil'] = eight_in
        
        for i in self.soil['Soil Class Dictionary']:
            twenty = i.get('twenty')
            twenty_in.append(twenty)
        
        self.soil['twenty_in_soil'] = twenty_in
        
        for i in self.soil['Soil Class Dictionary']:
            forty = i.get('forty')
            forty_in.append(forty)
        
        self.soil['forty_in_soil'] = forty_in
            
    def merge_goes(self, soils=False):
        if soils:
            soildf = self.soil
            soildf.reset_index(inplace=True)
            GOES_READ.rename(columns={'StationTriplet':'station'}, inplace=True)
            df_merged = pd.merge(soildf, GOES_READ, on=['Date', 'station'], how='inner')
            self.merged = df_merged
            
############ non-class function
def doall():
    instance = resample(SCAN_READ)
    instance.one_week_resample()
    instance.append_soils()
    instance.unpack_soils()
    instance.merge_goes(soils=True)
              
