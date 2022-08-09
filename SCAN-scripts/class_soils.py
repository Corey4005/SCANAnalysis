#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 14:33:21 2022

@author: cwalker
"""

from class_resample import resample
import pandas as pd
import numpy as np

class soils(resample):
    
    def __init__(self, data):
        
        resample.__init__(self, data)
        self.one_w_soil_df = pd.DataFrame()
        self.two_w_soil_df = pd.DataFrame()
        self.three_w_soil_df = pd.DataFrame()
        self.four_w_soil_df = pd.DataFrame()
    
    def create_1w_soil_columns(self, data_option='1w'): 
        
        self.__append_soils(self.one_week_resampled, data_option)
        self.__reclassify_soils(which_dataframe=data_option)
        print('The 1w soils dataframe have been appended, reclassified and stored in the self.one_w_soil_df class_attribute!')
        print('\n')
        
    def create_2w_soil_columns(self, data_option='2w'): 
         
        self.__append_soils(self.two_week_resampled, data_option)
        self.__reclassify_soils(which_dataframe=data_option)
        print('The 2w soils dataframe have been appended, reclassified and stored in the self.two_w_soil_df class_attribute!')
        print('\n')
        
    def create_3w_soil_columns(self, data_option='3w'):
        
        self.__append_soils(self.three_week_resampled, data_option)
        self.__reclassify_soils(which_dataframe=data_option)
        print('The 3w soils dataframe have been appended, reclassified and stored in the self.three_w_soil_df class_attribute!')
        print('\n')
        
    def create_4w_soil_columns(self, data_option='4w'):
        
        self.__append_soils(self.four_week_resampled, data_option)
        self.__reclassify_soils(which_dataframe=data_option)
        print('The 4w soils dataframe have been appended, reclassified and stored in the self.four_w_soil_df class_attribute!')
        print('\n')
        
    def get_soil_df(self, data_option=None):
        if data_option == '1w':
            df = self.one_w_soil_df
        elif data_option == '2w':
            df = self.two_w_soil_df
        elif data_option == '3w':
            df = self.three_w_soil_df
        else: 
            df = self.four_w_soil_df
            
        if df.empty:
            print('Dataframe is empty. Use a resample function, then the create_soil_columns() function.')
        else:
            return df
        
    ########## PRIVATE HELPER METHODS
    def __append_soils(self, df, data_option):
        print('Appending soils to', data_option, 'data!')
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
        
        if data_option=='1w':
            self.one_w_soil_df = df
        elif data_option=='2w':
            self.two_w_soil_df = df
        elif data_option=='3w':
            self.three_w_soil_df = df
        else:
            self.four_w_soil_df = df
            
        
    def __reclassify_soils(self, which_dataframe=None):
        
        if which_dataframe == '1w':
            df = self.one_w_soil_df
        elif which_dataframe == '2w':
            df = self.two_w_soil_df
        elif which_dataframe == '3w':
            df = self.three_w_soil_df
        else: 
            df = self.four_w_soil_df
            
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
        two = [lookup(x) for x in df['Two Soil']]
        four = [lookup(x) for x in df['Four Soil']]
        eight = [lookup(x) for x in df['Eight Soil']]
        twenty = [lookup(x) for x in df['Twenty Soil']]
        forty = [lookup(x) for x in df['Forty Soil']]
        
        ##create the new columns
        df['Two Soil Reclassified'] = two
        df['Four Soil Reclassified'] = four
        df['Eight Soil Reclassified'] = eight
        df['Twenty Soil Reclassified'] = twenty
        df['Forty Soil Reclassified'] = forty
        
        if which_dataframe == '1w':
            self.one_w_soil_df == df
        elif which_dataframe == '2w':
            self.two_w_soil_df == df
        elif which_dataframe == '3w':
            self.three_w_soil_df == df
        else: 
            self.four_w_soil_df == df
        
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