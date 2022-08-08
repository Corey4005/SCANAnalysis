#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 14:33:21 2022

@author: cwalker
"""

from class_resample import resample
import pandas as pd
import numpy as np

#just to get the data
from datasets import SCAN_READ

class soils(resample):
    
    def __init__(self, data):
        
        resample.__init__(self, data)
        
        
    
    def create_soil_columns(self, data_option=False):
        
        ##check to see if the data parameter is true
        while data_option==False: 
            print('pass a data option: 1d, 1w, 2w, 3w, 4w')
            print('d="day", \n w="week"')
            break
        
        if data_option == '1d':
            self.append_soils(self.clean)
            print('The 1d soils dataframe can be accessed now with class method: get_soil_df()')
        
        if data_option == '1w':
            if self.one_week_resampled.empty:
                self.one_week_resample()
                self.__append_soils(self.one_week_resampled)
                print('The 1w soils dataframe can be accessed now with class method: get_soil_df()')
            else:
                self.__append_soils(self.one_week_resampled)
                print('The 1w soils dataframe can be accessed now with class method: get_soil_df()')
         
        if data_option == '2w':
             if self.two_week_resampled.empty:
                 self.two_week_resample()
                 self.__append_soils(self.two_week_resampled)
                 print('The 2w soils dataframe can be accessed now with class method: get_soil_df()')
             else:
                 self.__append_soils(self.two_week_resampled)
                 print('The 2w soils dataframe can be accessed now with class method: get_soil_df()')
                 
        if data_option == '3w':
             if self.three_week_resampled.empty:
                 self.three_week_resample()
                 self.__append_soils(self.three_week_resampled)
                 print('The 3w soils dataframe can be accessed now with class method: get_soil_df()')
             else:
                 self.__append_soils(self.three_week_resampled)
                 print('The 3w soils dataframe can be accessed now with class method: get_soil_df()')
                 
        if data_option == '4w':
             if self.three_week_resampled.empty:
                 self.three_week_resample()
                 self.__append_soils(self.three_week_resampled)
                 print('The 3w soils dataframe can be accessed now with class method: get_soil_df()')
             else:
                 self.__append_soils(self.three_week_resampled)
                 print('The 3w soils dataframe can be accessed now with class method: get_soil_df()')
    
    def get_soil_df(self):
        df = self.soil
        if df.empty:
            print('Dataframe is empty. Use a resample function, then the create_soil_columns() function.')
        else:
            return self.soil
        
    ########## PRIVATE HELPER METHODS
    def __append_soils(self, df):
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
        
    def reclassify_soils(self):
        
        #lookup function
        def lookup(x):
            if (x == 'S') or (x=='LS') or (x=='SL') or (x=='FSL') or (x=='FS'):
                return 'A' ## Sands
            
            elif (x == 'SIL') or (x=='SI') or (x=='GRSIL') or (x=='L'):
                return 'B' ## Silts and Loam
            
            elif x == 'SCL':
                return 'C' ## Sandy Clay Loam
            
            elif (x == 'C') or (x=='CL') or (x=='SICL') or (x=='SC') or (x=='SIC'):
                return 'D' ## Clays
            
            elif (x=='BRCK'):
                return np.nan
            
        ##return the new soil classifications to a list
        two = [lookup(x) for x in self.soil['Two Soil']]
        four = [lookup(x) for x in self.soil['Four Soil']]
        eight = [lookup(x) for x in self.soil['Eight Soil']]
        twenty = [lookup(x) for x in self.soil['Twenty Soil']]
        forty = [lookup(x) for x in self.soil['Forty Soil']]
        
        ##create the new columns
        self.soil['Two Soil Reclassified'] = two
        self.soil['Four Soil Reclassified'] = four
        self.soil['Eight Soil Reclassified'] = eight
        self.soil['Twenty Soil Reclassified'] = twenty
        self.soil['Forty Soil Reclassified'] = forty
        
    def soils_csv(self):
        df = self.soil
        store = {}
        for i in df['station'].unique():
            new_df = df[df['station'] == i]
            new_df = new_df[['Two Soil', 'Four Soil',
            'Eight Soil', 'Twenty Soil', 'Forty Soil', 'Two Soil Reclassified',
            'Four Soil Reclassified', 'Eight Soil Reclassified',
            'Twenty Soil Reclassified', 'Forty Soil Reclassified']]
            soils_list = []
            for j in new_df:
                soil = new_df[j].unique().item()
                soils_list.append(soil)
            store[i] = soils_list
        
        concat = pd.DataFrame(store)
        concat.to_csv('soil_class.csv')