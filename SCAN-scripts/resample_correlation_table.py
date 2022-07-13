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
        #data from scan object
        self.scan_instance = SCAN(data=SCAN_READ)
        self.stdev = self.scan_instance.standard_deviation_by_month()
        self.mean = self.scan_instance.mean_soil_moisture_by_month()
        self.z_score = self.scan_instance.z_score()
        self.quality = self.scan_instance.quality_z_score(std=3.5)
        self.clean = self.scan_instance.clean_data().show()
        self.resampled = pd.DataFrame()   
        self.soil = pd.DataFrame()
        
    def get_clean_data(self):
        return self.clean
    
    def get_resampled(self):
        return self.resampled
    
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
        
        
    def soils(self):
        dict_list = []
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
        
        


