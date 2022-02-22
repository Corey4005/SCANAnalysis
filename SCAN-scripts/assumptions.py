#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project: 
    This is a project for calculating effective saturation at
    USDA SCAN sites given soil class and assumptions about the physical 
    characteristics for each. 

Created on Wed Jan 26 11:41:36 2022

@author: coreywalker
contact: 
    cdw0063@uah.edu
    
note: 
    Please site this repository if the functions are used in another analysis. 
    
"""
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


SCAN_ALL = '../data/SCAN_DEPTHS_ALL.csv'
SCAN_READ = pd.read_csv(SCAN_ALL)

GOES_ESI_ALL = '../data/1_wk_ESI_all.csv'
GOES_READ = pd.read_csv(GOES_ESI_ALL)
GOES_READ['Date'] = pd.to_datetime(GOES_READ['Date'])
GOES_READ.drop('Unnamed: 0', axis=1, inplace=True)

class SCAN:
    '''
    SCAN CLASS - used to set Alabama SCAN sites with assumed soil 
    characteristics based on soil classes. 
    
    functions: 
        __init__ - create new_df attribute used in functions set on 
        SCAN_READ variable (raw import) in assumptions.py. 
        
        properties of __init__:
            self.df - pandas dataframe of SCAN_READ
            
            self.new_df - pandas dataframe with correct soil depths, station, 
                and dates.
                
            self.stations - pandas dataframe with all stations that have soil
                texture characteristics listed in Pedon Report
    
    '''

    def __init__(self, data):
        self.df = data
        self.new_df = self.df[['Date', 'station','SMS-2.0in', 'SMS-4.0in', 
                               'SMS-8.0in', 'SMS-20.0in','SMS-40.0in']].copy()
        self.stations = self.new_df[(self.new_df['station'] == '2057:AL:SCAN') | 
                   (self.new_df['station'] == '2113:AL:SCAN') | 
                   (self.new_df['station'] == '2055:AL:SCAN') |
                   (self.new_df['station'] == '2180:AL:SCAN') |
                   (self.new_df['station'] == '2114:AL:SCAN') |
                   (self.new_df['station'] == '2056:AL:SCAN') |
                   (self.new_df['station'] == '2115:AL:SCAN') |
                   (self.new_df['station'] == '2053:AL:SCAN') |
                   (self.new_df['station'] == '2078:AL:SCAN') |
                   (self.new_df['station'] == '2177:AL:SCAN') |
                   (self.new_df['station'] == '2173:AL:SCAN') |
                   (self.new_df['station'] == '2178:AL:SCAN') |
                   (self.new_df['station'] == '2175:AL:SCAN') |
                   (self.new_df['station'] == '2174:AL:SCAN') |
                   (self.new_df['station'] == '2182:AL:SCAN') |
                   (self.new_df['station'] == '2179:AL:SCAN') |
                   (self.new_df['station'] == '2181:AL:SCAN') |
                   (self.new_df['station'] == '2176:AL:SCAN')]
    
    def soil_class(self): 
        #stations notes
        #2177 no field measurements of soil texture, will use lab measurements 
            #in calculation. 
        #2174 station pedon report missing. Will get info from web soil survey. 
        #2173 missing field measurements of soil texture, will use lab measures
            #in calculation.
        #2178 - missing soil characterization 'field texture', will use lab 
            #measures instead. 
        #2181 - No field or lab texture measurements. 
        #2182 - No pedon report. 
        #2176 - Unable to read soil characteristics due to inadequate depth
            #measures for each type. Therefore, this station will not be
            #included. 
        #2179 - Mising forty in soil characteristics due to inadequate depth
            #measure. Will use lab reports and web soil survey
        #2175 -
        
        '''
        Purpose:
            append the soil dictionary for each station that has an
            available pedon report in Alabama.
        
        Returns: 
            self.stations property with updated dataframe. 
        '''
        dict_list = []
        
        for i in self.stations['station']:
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
                
        self.stations['Soil Class Dictionary'] = dict_list
        
        return self
    
    def unpack(self):
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
        for i in self.stations['Soil Class Dictionary']:
            two = i.get('two')
            two_in.append(two)
        
        self.stations['two_in_soil'] = two_in
        
        #get four
        for i in self.stations['Soil Class Dictionary']:
            four = i.get('four')
            four_in.append(four)
        
        self.stations['four_in_soil'] = four_in
                
        for i in self.stations['Soil Class Dictionary']:
            eight = i.get('eight')
            eight_in.append(eight)
        
        self.stations['eight_in_soil'] = eight_in
        
        for i in self.stations['Soil Class Dictionary']:
            twenty = i.get('twenty')
            twenty_in.append(twenty)
        
        self.stations['twenty_in_soil'] = twenty_in
        
        for i in self.stations['Soil Class Dictionary']:
            forty = i.get('forty')
            forty_in.append(forty)
        
        self.stations['forty_in_soil'] = forty_in
            
        return self

    def Calculate_ESM(self):
        '''
        Purpose: 
            Calcualte effective saturation given soil class textures.
        
        returns: 
            Pandas dataframe containing the columns necessary for 
        
        '''
        #two inch calculations
        ES_2 = []
        for i in self.stations.index:
           #two inch soil 
            if self.stations['two_in_soil'][i] == 'SICL':
                ES = ((self.stations['SMS-2.0in'][i] / 100)- 0.089) / (0.43 - 0.089)
                ES_2.append(ES)
            
            elif self.stations['two_in_soil'][i] == 'SIC': 
                ES = ((self.stations['SMS-2.0in'][i] / 100)- 0.070) / (0.36 - 0.070)
                ES_2.append(ES)
                
            elif self.stations['two_in_soil'][i] == 'FSL': 
                ES = ((self.stations['SMS-2.0in'][i] / 100)- 0.065) / (0.41 - 0.065)
                ES_2.append(ES)
                
            elif self.stations['two_in_soil'][i] == 'GRSIL': 
                ES = ((self.stations['SMS-2.0in'][i] / 100)- 0.067) / (0.45 - 0.067)
                ES_2.append(ES)
                
            elif self.stations['two_in_soil'][i] == 'SIL': 
                ES = ((self.stations['SMS-2.0in'][i] / 100)- 0.067) / (0.45 - 0.067)
                ES_2.append(ES)
                
            elif self.stations['two_in_soil'][i] == 'SL': 
                ES = ((self.stations['SMS-2.0in'][i] / 100)- 0.065) / (0.41 - 0.065)
                ES_2.append(ES)
                
            elif self.stations['two_in_soil'][i] == 'LS':
                ES = ((self.stations['SMS-2.0in'][i] / 100)- 0.057) / (0.41 - 0.057)
                ES_2.append(ES)
                
            elif self.stations['two_in_soil'][i] == 'FS': 
                ES = ((self.stations['SMS-2.0in'][i] / 100)- 0.045) / (0.43 - 0.045)
                ES_2.append(ES)
            
            elif self.stations['two_in_soil'][i] == 'L':
                ES = ((self.stations['SMS-2.0in'][i] / 100)- 0.078) / (0.43 - 0.078)
                ES_2.append(ES)
        
        #four inch calculations
        ES_4 = []
        for i in self.stations.index:
       
            if self.stations['four_in_soil'][i] == 'SICL':
                ES = ((self.stations['SMS-4.0in'][i] / 100)- 0.089) / (0.43 - 0.089)
                ES_4.append(ES)
                
            elif self.stations['four_in_soil'][i] == 'SIL': 
                ES = ((self.stations['SMS-4.0in'][i] / 100)- 0.067) / (0.45 - 0.067)
                ES_4.append(ES)
        
            elif self.stations['four_in_soil'][i] == 'SIC': 
                ES = ((self.stations['SMS-4.0in'][i] / 100)- 0.070) / (0.36 - 0.070)
                ES_4.append(ES)
            
            elif self.stations['four_in_soil'][i] == 'FSL': 
                ES = ((self.stations['SMS-4.0in'][i] / 100)- 0.065) / (0.41 - 0.065)
                ES_4.append(ES)
            
            elif self.stations['four_in_soil'][i] == 'GRSIL': 
                ES = ((self.stations['SMS-4.0in'][i] / 100)- 0.067) / (0.45 - 0.067)
                ES_4.append(ES)
            
            
            elif self.stations['four_in_soil'][i] == 'SL': 
                ES = ((self.stations['SMS-4.0in'][i] / 100)- 0.065) / (0.41 - 0.065)
                ES_4.append(ES)
            
            elif self.stations['four_in_soil'][i] == 'LS':
                ES = ((self.stations['SMS-4.0in'][i] / 100)- 0.057) / (0.41 - 0.057)
                ES_4.append(ES)
            
            elif self.stations['four_in_soil'][i] == 'FS': 
                ES = ((self.stations['SMS-4.0in'][i] / 100)- 0.045) / (0.43 - 0.045)
                ES_4.append(ES)
        
            elif self.stations['four_in_soil'][i] == 'L': 
                ES = ((self.stations['SMS-4.0in'][i] / 100)- 0.078) / (0.43 - 0.078)
                ES_4.append(ES)
        
                
        ES_8 = []
        for i in self.stations.index:
            
            if self.stations['eight_in_soil'][i] == 'SICL':
                ES = ((self.stations['SMS-8.0in'][i] / 100)- 0.089) / (0.43 - 0.089)
                ES_8.append(ES)
                
            elif self.stations['eight_in_soil'][i] == 'SIC': 
                ES = ((self.stations['SMS-8.0in'][i] / 100)- 0.070) / (0.36 - 0.070)
                ES_8.append(ES)
                
            elif self.stations['eight_in_soil'][i] == 'FSL': 
                ES = ((self.stations['SMS-8.0in'][i] / 100)- 0.065) / (0.41 - 0.065)
                ES_8.append(ES)
                
            elif self.stations['eight_in_soil'][i] == 'C': 
                ES = ((self.stations['SMS-8.0in'][i] / 100)- 0.068) / (0.38 - 0.068)
                ES_8.append(ES)
            
            elif self.stations['eight_in_soil'][i] == 'GRSIL': 
                ES = ((self.stations['SMS-8.0in'][i] / 100)- 0.067) / (0.45 - 0.067)
                ES_8.append(ES)
            
            elif self.stations['eight_in_soil'][i] == 'SL': 
                ES = ((self.stations['SMS-8.0in'][i] / 100)- 0.065) / (0.41 - 0.065)
                ES_8.append(ES)
            
            elif self.stations['eight_in_soil'][i] == 'LS':
                ES = ((self.stations['SMS-8.0in'][i] / 100)- 0.057) / (0.41 - 0.057)
                ES_8.append(ES)
            
            elif self.stations['eight_in_soil'][i] == 'FS': 
                ES = ((self.stations['SMS-8.0in'][i] / 100)- 0.045) / (0.43 - 0.045)
                ES_8.append(ES)
                
            elif self.stations['eight_in_soil'][i] == 'CL': 
                ES = ((self.stations['SMS-8.0in'][i] / 100)- 0.095) / (0.41 - 0.095)
                ES_8.append(ES)
            
            elif self.stations['eight_in_soil'][i] == 'L': 
                ES = ((self.stations['SMS-8.0in'][i] / 100)- 0.078) / (0.43 - 0.078)
                ES_8.append(ES)
                
            elif self.stations['eight_in_soil'][i] == 'SIL': 
                ES = ((self.stations['SMS-8.0in'][i] / 100)- 0.067) / (0.45 - 0.067)
                ES_8.append(ES)
            
        
        ES_20 = []
        for i in self.stations.index:
            
            if self.stations['twenty_in_soil'][i] == 'SICL':
                ES = ((self.stations['SMS-20.0in'][i] / 100)- 0.089) / (0.43 - 0.089)
                ES_20.append(ES)
                
            elif self.stations['twenty_in_soil'][i] == 'SIC': 
                ES = ((self.stations['SMS-20.0in'][i] / 100)- 0.070) / (0.36 - 0.070)
                ES_20.append(ES)
                
            elif self.stations['twenty_in_soil'][i] == 'L': 
                ES = ((self.stations['SMS-20.0in'][i] / 100)- 0.078) / (0.43 - 0.078)
                ES_20.append(ES)
            
            elif self.stations['twenty_in_soil'][i] == 'C': 
                ES = ((self.stations['SMS-20.0in'][i] / 100)- 0.068) / (0.38 - 0.068)
                ES_20.append(ES)
            
            elif self.stations['twenty_in_soil'][i] == 'SL': 
                ES = ((self.stations['SMS-20.0in'][i] / 100)- 0.065) / (0.41 - 0.065)
                ES_20.append(ES)
                
            elif self.stations['twenty_in_soil'][i] == 'FSL': 
                ES = ((self.stations['SMS-20.0in'][i] / 100)- 0.065) / (0.41 - 0.065)
                ES_20.append(ES)
                
            elif self.stations['twenty_in_soil'][i] == 'FS': 
                ES = ((self.stations['SMS-20.0in'][i] / 100)- 0.045) / (0.43 - 0.045)
                ES_20.append(ES)
            
            elif self.stations['twenty_in_soil'][i] == 'S': 
                ES = ((self.stations['SMS-20.0in'][i] / 100)- 0.045) / (0.43 - 0.045)
                ES_20.append(ES)
            
            elif self.stations['twenty_in_soil'][i] == 'SCL': 
                ES = ((self.stations['SMS-20.0in'][i] / 100)- 0.100) / (0.38 - 0.100)
                ES_20.append(ES)
            
        ES_40 = []
        #START HERE 
        for i in self.stations.index:
            
            if self.stations['forty_in_soil'][i] == 'SICL':
                ES = ((self.stations['SMS-40.0in'][i] / 100)- 0.089) / (0.43 - 0.089)
                ES_40.append(ES)
                
            elif self.stations['forty_in_soil'][i] == 'CL': 
                ES = ((self.stations['SMS-40.0in'][i] / 100)- 0.095) / (0.41 - 0.095)
                ES_40.append(ES)
                
            elif self.stations['forty_in_soil'][i] == 'SIC': 
                ES = ((self.stations['SMS-40.0in'][i] / 100)- 0.070) / (0.36 - 0.070)
                ES_40.append(ES)
                
            elif self.stations['forty_in_soil'][i] == 'L': 
                ES = ((self.stations['SMS-40.0in'][i] / 100)- 0.078) / (0.43 - 0.078)
                ES_40.append(ES)
            
            elif self.stations['forty_in_soil'][i] == 'C': 
                ES = ((self.stations['SMS-40.0in'][i] / 100)- 0.068) / (0.38 - 0.068)
                ES_40.append(ES)
            
            elif self.stations['forty_in_soil'][i] == 'SCL': 
                ES = ((self.stations['SMS-40.0in'][i] / 100)- 0.100) / (0.38 - 0.100)
                ES_40.append(ES)
            
            elif self.stations['forty_in_soil'][i] == 'SL': 
                ES = ((self.stations['SMS-40.0in'][i] / 100)- 0.065) / (0.41 - 0.065)
                ES_40.append(ES)
            
            elif self.stations['forty_in_soil'][i] == 'S': 
                ES = ((self.stations['SMS-40.0in'][i] / 100)- 0.045) / (0.43 - 0.045)
                ES_40.append(ES)
            
            elif self.stations['forty_in_soil'][i] == 'BRCK':
                ES = np.nan
                ES_40.append(ES)
            
                

        self.stations['ES_2in'] = ES_2
        self.stations['ES_4in'] = ES_4
        self.stations['ES_8in'] = ES_8
        self.stations['ES_20in'] = ES_20
        self.stations['ES_40in'] = ES_40
        return self
    

    def OTHER_ESM(self):
        
        store = {}
        for i in self.stations['station'].unique():
            new_df = self.stations[self.stations['station'] == i]
            new_df.set_index('Date', inplace=True)
            new_df.index = pd.to_datetime(new_df.index)
            new_df.sort_index(inplace=True)
            
            
            if i == '2057:AL:SCAN':
            #two in - SICL
                ES_2in = ((new_df['SMS-2.0in'] / 100)- 0.089) / (0.475 - 0.089)
                new_df['ES_2in'] = ES_2in
                
            #four in - SICL
                ES_4in = ((new_df['SMS-4.0in'] / 100)- 0.089) / (0.49 - 0.089)
                new_df['ES_4in'] = ES_4in
            
            #eight in - SICL
                ES_8in = ((new_df['SMS-8.0in'] / 100)- 0.089) / (0.465 - 0.089)
                new_df['ES_8in'] = ES_8in
            #twenty in - SICL
                ES_20in = ((new_df['SMS-20.0in'] / 100)- 0.089) / (0.47 - 0.089)
                new_df['ES_20in'] = ES_20in
            #forty in - SICL
                ES_40in = ((new_df['SMS-40.0in'] / 100)- 0.089) / (0.55 - 0.089)
                new_df['ES_40in'] = ES_40in
                
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                    
            #store it 
                store[i] = new_df
                
            elif i =='2113:AL:SCAN':
            #two - FSL
                ES_2in = ((new_df['SMS-2.0in'] / 100)- 0.022) / (0.405 - 0.022)
                new_df['ES_2in'] = ES_2in
                
                
            #four - FSL 
                ES_4in = ((new_df['SMS-4.0in'] / 100)- 0.022) / (0.415 - 0.022)
                new_df['ES_4in'] = ES_4in
                
            #eight - FSL
                ES_8in = ((new_df['SMS-8.0in'] / 100)- 0.022) / (0.37 - 0.022)
                new_df['ES_8in'] = ES_8in
                
            #twenty - L
                ES_20in = ((new_df['SMS-20.0in'] / 100)- 0.061) / (0.44 - 0.061)
                new_df['ES_20in'] = ES_20in
            
            #forty - L
                ES_40in = ((new_df['SMS-40.0in'] / 100)- 0.061) / (0.45 - 0.061)
                new_df['ES_40in'] = ES_40in
                
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                
                
            #store it 
                store[i] = new_df
            
            elif i =='2055:AL:SCAN':
            #two - GRSIL
                ES_2in = ((new_df['SMS-2.0in'] / 100)- 0.033) / (0.48 - 0.033)
                new_df['ES_2in'] = ES_2in
            
            # #four - GRSIL
                ES_4in = ((new_df['SMS-4.0in'] / 100)- 0.033) / (0.44 - 0.02)
                new_df['ES_4in'] = ES_4in
                
                
            # #eight - GRSIL
                ES_8in = ((new_df['SMS-8.0in'] / 100)- 0.033) / (0.45 - 0.033)
                new_df['ES_8in'] = ES_4in
                
        
            # #twenty - SICL
                ES_20in = ((new_df['SMS-20.0in'] / 100)- 0.089) / (0.49 - 0.089)
                new_df['ES_20in'] = ES_20in
                
            # #forty - SICL
                ES_40in = ((new_df['SMS-40.0in'] / 100)- 0.035) / (0.57 - 0.035)
                new_df['ES_40in'] = ES_40in
                
            #create new dataframe
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                
            # #store it 
                store[i] = new_df
            
            elif i == '2180:AL:SCAN':
            #two - SL
                ES_2in = ((new_df['SMS-2.0in'] / 100)- 0.005) / (0.37 - 0.001)
                new_df['ES_2in'] = ES_2in
                
            #four - SL
                ES_4in = ((new_df['SMS-4.0in'] / 100)- 0.005) / (0.31 - 0.005)
                new_df['ES_4in'] = ES_4in
                
            #eight - SL
                ES_8in = ((new_df['SMS-8.0in'] / 100)- 0.005) / (0.34 - 0.005)
                new_df['ES_8in'] = ES_8in
                
            
            #twenty - SL
                ES_20in = ((new_df['SMS-20.0in'] / 100)- 0.005) / (0.31 - 0.005)
                new_df['ES_20in'] = ES_20in
                
            
            #forty - SCL
                ES_40in = ((new_df['SMS-40.0in'] / 100)- 0.100) / (0.355 - 0.100)
                new_df['ES_40in'] = ES_40in
                
            #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                
            # #store it 
                store[i] = new_df
            
            elif i == '2114:AL:SCAN':
            # two - SIL
                ES_2in = ((new_df['SMS-2.0in'] / 100)- 0.040) / (0.45 - 0.040)
                new_df['ES_2in'] = ES_2in
            
            # four - SIC
                ES_4in = ((new_df['SMS-4.0in'] / 100)- 0.070) / (0.41 - 0.070)
                new_df['ES_4in'] = ES_4in
            
            #eight - C
                ES_8in = ((new_df['SMS-8.0in'] / 100)- 0.068) / (0.41 - 0.068)
                new_df['ES_8in'] = ES_8in
            
            #twenty - C 
                ES_20in = ((new_df['SMS-20.0in'] / 100)- 0.068) / (0.41 - 0.068)
                new_df['ES_20in'] = ES_20in
                
            #forty - C
                ES_40in = ((new_df['SMS-40.0in'] / 100)- 0.068) / (0.48 - 0.068)
                new_df['ES_40in'] = ES_40in
                
            #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                
            # #store it 
                store[i] = new_df
            
            elif i == '2056:AL:SCAN':
            #two - L
                ES_2in = ((new_df['SMS-2.0in'] / 100)- 0.078) / (0.52 - 0.078)
                new_df['ES_2in'] = ES_2in
                
            #four - L
                ES_4in = ((new_df['SMS-4.0in'] / 100)- 0.078) / (0.52 - 0.078)
                new_df['ES_4in'] = ES_2in
                
            #eight - CL
                ES_8in = ((new_df['SMS-8.0in'] / 100)- 0.095) / (0.50 - 0.095)
                new_df['ES_8in'] = ES_8in
            
            #twenty - C
                ES_20in = ((new_df['SMS-20.0in'] / 100)- 0.068) / (0.41 - 0.068)
                new_df['ES_20in'] = ES_20in
            
            #forty - C 
                ES_40in = ((new_df['SMS-40.0in'] / 100)- 0.068) / (0.53 - 0.068)
                new_df['ES_40in'] = ES_40in
            
            #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]

            # #store it 
                store[i] = new_df
            
            elif i == '2115:AL:SCAN':
                #two - LS
                ES_2in = ((new_df['SMS-2.0in'] / 100)- 0.001) / (0.44 - 0.001)
                new_df['ES_2in'] = ES_2in
                
                #four - LS
                ES_4in = ((new_df['SMS-4.0in'] / 100)- 0.001) / (0.44 - 0.001)
                new_df['ES_4in'] = ES_2in
                
                #eight - SL
                ES_8in = ((new_df['SMS-8.0in'] / 100)- 0.005) / (0.41 - 0.005)
                new_df['ES_8in'] = ES_8in
                
                #twenty - SCL
                ES_20in = ((new_df['SMS-20.0in'] / 100) - 0.100) / (0.40 - 0.100)
                new_df['ES_20in'] = ES_20in
                
                #forty - CL
                ES_40in = ((new_df['SMS-40.0in'] / 100)- 0.02) / (0.43 - 0.02)
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                    
                # #store it 
                store[i] = new_df
                 
            elif i == '2053:AL:SCAN':
                #two - SICL
                ES_2in = ((new_df['SMS-2.0in'] / 100)- 0.035) / (0.41 - 0.035)
                new_df['ES_2in'] = ES_2in
                
                #four - SIL
                ES_4in = ((new_df['SMS-4.0in'] /  100)- 0.070) / (0.40 - 0.070)
                new_df['ES_4in'] = ES_4in
                
                #eight - SIL
                ES_8in = ((new_df['SMS-8.0in'] / 100)- 0.070) / (0.41 - 0.070)
                new_df['ES_8in'] = ES_8in
                
                #twenty - SICL
                ES_20in = ((new_df['SMS-20.0in'] / 100)- 0.050) / (0.59 - 0.050)
                new_df['ES_20in'] = ES_20in
                
                #forty - CL
                ES_40in = ((new_df['SMS-40.0in'] / 100)- 0.02) / (0.41 - 0.02)
                new_df['ES_40in'] = ES_40in
            
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                
                # #store it 
                store[i] = new_df
                
            elif i == '2078:AL:SCAN':
                #two - SICL
                ES_2in = ((new_df['SMS-2.0in'] / 100)- 0.017) / (0.56 - 0.017)
                new_df['ES_2in'] = ES_2in
                
                #four - SIL
                ES_4in = ((new_df['SMS-4.0in'] /  100)- 0.070) / (0.51 - 0.070)
                new_df['ES_4in'] = ES_4in
                
                #eight - SICL
                ES_8in = ((new_df['SMS-8.0in'] / 100)- 0.040) / (0.87 - 0.040)
                new_df['ES_8in'] = ES_8in
               
                #twenty - SCIL 
                ES_20in = ((new_df['SMS-20.0in'] / 100)- 0.089) / (1.57 - 0.089)
                new_df['ES_20in'] = ES_20in
                
                #forty - CL
                ES_40in = ((new_df['SMS-40.0in'] / 100)- 0.095) / (0.58 - 0.095)
                new_df['ES_40in'] = ES_40in
            
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                    
                # #store it 
                store[i] = new_df
                
            elif i == '2177:AL:SCAN':
                #two - SIC
                ES_2in = ((new_df['SMS-2.0in'] / 100)- 0.035) / (0.69 - 0.035)
                new_df['ES_2in'] = ES_2in
                
                #four - SIC
                ES_4in = ((new_df['SMS-4.0in'] / 100)- 0.070) / (0.66 - 0.070)
                new_df['ES_4in'] = ES_4in
               
                #eight - SIC
                ES_8in = ((new_df['SMS-8.0in'] / 100)- 0.070) / (0.69 - 0.070)
                new_df['ES_8in'] = ES_8in
                
                #twenty - SIC
                ES_20in = ((new_df['SMS-20.0in'] / 100)- 0.070) / (0.73 - 0.070)
                new_df['ES_20in'] = ES_20in
                
                #forty - SIC
                ES_40in = ((new_df['SMS-40.0in'] / 100)- 0.070) / (0.71 - 0.070)
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                    
                # #store it 
                store[i] = new_df
            
            elif i == '2173:AL:SCAN':
                #two - SIL
                ES_2in = ((new_df['SMS-2.0in'] /  100)- 0.001) / (0.49 - 0.001)
                new_df['ES_2in'] = ES_2in
                
                #four - SIL
                ES_4in = ((new_df['SMS-4.0in'] /  100)- 0.001) / (0.50 - 0.001)
                new_df['ES_4in'] = ES_4in
                
                #eight - SICL
                ES_8in = ((new_df['SMS-8.0in'] / 100)- 0.089) / (0.52 - 0.089)
                new_df['ES_8in'] = ES_8in
                
                #twenty - SICL
                ES_20in = ((new_df['SMS-20.0in'] / 100)- 0.089) / (0.59 - 0.089)
                new_df['ES_20in'] = ES_20in
                
                #forty - C 
                ES_40in = ((new_df['SMS-40.0in'] / 100)- 0.068) / (0.70 - 0.068)
                new_df['ES_40in'] = ES_40in
            
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                    
                # #store it 
                store[i] = new_df
                
            elif i == '2178:AL:SCAN':
                #two - FSL
                ES_2in = ((new_df['SMS-2.0in'] / 100)- 0.005) / (0.50 - 0.005)
                new_df['ES_2in'] = ES_2in
                
                #four - FSL
                ES_4in = ((new_df['SMS-4.0in'] / 100)- 0.022) / (0.48 - 0.022)
                new_df['ES_4in'] = ES_4in
                
                #eight - FSL
                ES_8in = ((new_df['SMS-8.0in'] / 100)- 0.022) / (0.54 - 0.022)
                new_df['ES_8in'] = ES_8in
                
                #twenty - FSL
                ES_20in = ((new_df['SMS-20.0in'] / 100)- 0.022) / (0.59 - 0.022)
                new_df['ES_20in'] = ES_20in
                
                #forty - L
                ES_40in = ((new_df['SMS-40.0in'] / 100)- 0.078) / (0.56 - 0.078)
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                    
                # #store it 
                store[i] = new_df
                
            elif i == '2175:AL:SCAN':
                #two - L
                ES_2in = ((new_df['SMS-2.0in'] / 100)- 0.001) / (0.46 - 0.001)
                new_df['ES_2in'] = ES_2in
                
                #four - L
                ES_4in = ((new_df['SMS-4.0in'] / 100)- 0.001) / (0.42 - 0.001)
                new_df['ES_4in'] = ES_4in
                
                #eight - L
                ES_8in = ((new_df['SMS-8.0in'] / 100)- 0.001) / (0.46 - 0.001)
                new_df['ES_8in'] = ES_8in
                
                #twenty - L
                ES_20in = ((new_df['SMS-20.0in'] / 100)- 0.001) / (0.59 - 0.001)
                new_df['ES_20in'] = ES_20in
                
                #forty - C
                ES_40in = ((new_df['SMS-40.0in'] / 100)- 0.068) / (0.58 - 0.068)
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                
                    
                # #store it 
                store[i] = new_df
                
            elif i == '2174:AL:SCAN':
                #two - SIC
                ES_2in = ((new_df['SMS-2.0in'] / 100)- 0.042) / (0.64 - 0.042)
                new_df['ES_2in'] = ES_2in
                
                #four - SIC
                ES_4in = ((new_df['SMS-4.0in'] / 100)- 0.042) / (0.74 - 0.042)
                new_df['ES_4in'] = ES_4in
                
                #eight - C
                ES_8in = ((new_df['SMS-8.0in'] / 100)- 0.068) / (0.73 - 0.068)
                new_df['ES_8in'] = ES_8in
                
                #twenty - C
                ES_20in = ((new_df['SMS-20.0in'] / 100)- 0.068) / (0.70 - 0.068)
                new_df['ES_20in'] = ES_20in
                
                #forty - C
                ES_40in = ((new_df['SMS-40.0in'] / 100)- 0.005) / (0.71 - 0.005)
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                    
                # #store it 
                store[i] = new_df
            
            elif i == '2182:AL:SCAN':
                #two - LS
                ES_2in = ((new_df['SMS-2.0in'] / 100)- 0.001) / (0.44 - 0.001)
                new_df['ES_2in'] = ES_2in
                
                #four - LS
                ES_4in = ((new_df['SMS-4.0in'] / 100)- 0.001) / (0.33 - 0.001)
                new_df['ES_4in'] = ES_4in
                
                #eight - LS
                ES_8in = ((new_df['SMS-8.0in'] / 100)- 0.001) / (0.38 - 0.001)
                new_df['ES_8in'] = ES_8in
                
                #twenty - FS
                ES_20in = ((new_df['SMS-20.0in'] / 100)- 0.005) / (0.40 - 0.045)
                new_df['ES_20in'] = ES_20in
                
                #forty - SL
                ES_40in = ((new_df['SMS-40.0in'] / 100)- 0.005) / (0.60 - 0.065)
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                    
                # #store it 
                store[i] = new_df
                
            elif i == '2179:AL:SCAN':
                #two - FSL
                ES_2in = ((new_df['SMS-2.0in'] / 100)- 0.005) / (0.50 - 0.065)
                new_df['ES_2in'] = ES_2in
                
                #four - FSL
                ES_4in = ((new_df['SMS-4.0in'] / 100)- 0.005) / (2.23 - 0.065)
                new_df['ES_4in'] = ES_4in
                
                #eight - FSL
                ES_8in = ((new_df['SMS-8.0in'] / 100)- 0.005) / (0.45 - 0.065)
                new_df['ES_8in'] = ES_8in
                
                #twenty - FSL
                ES_20in = ((new_df['SMS-20.0in'] / 100)- 0.005) / (0.43 - 0.065)
                new_df['ES_20in'] = ES_20in
                
                #forty - BRCK
                ES_40in = np.nan
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                
                # #store it 
                store[i] = new_df
                
            elif i == '2181:AL:SCAN':
                #two - FSL
                ES_2in = ((new_df['SMS-2.0in'] / 100)- 0.063) / (0.40 - 0.063)
                new_df['ES_2in'] = ES_2in
                
                #four - FSL
                ES_4in = ((new_df['SMS-4.0in'] / 100)- 0.065) / (0.435 - 0.065)
                new_df['ES_4in'] = ES_4in
                
                #eight - FSL
                ES_8in = ((new_df['SMS-8.0in'] / 100)- 0.065) / (0.35 - 0.065)
                new_df['ES_8in'] = ES_8in
                
                #twenty - SL
                ES_20in = ((new_df['SMS-20.0in'] / 100) - 0.065) / (0.37 - 0.065)
                new_df['ES_20in'] = ES_20in
                
                #forty - SCL
                ES_40in = ((new_df['SMS-40.0in'] / 100)- 0.100) / (0.36 - 0.100)
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                    
                # #store it 
                store[i] = new_df
                
            elif i == '2176:AL:SCAN': 
                #two - FS
                ES_2in = ((new_df['SMS-2.0in'] / 100)-0.001) / (0.245 - 0.001)
                new_df['ES_2in'] = ES_2in
                
                #four - FS
                ES_4in = ((new_df['SMS-4.0in'] / 100)-0.001) / (0.27 - 0.001)
                new_df['ES_4in'] = ES_4in
                
                #eight - FS
                ES_8in = ((new_df['SMS-8.0in'] / 100)-0.001) / (0.22 - 0.001)
                new_df['ES_8in'] = ES_8in
                
                #twenty - S
                ES_20in = ((new_df['SMS-20.0in'] / 100)-0.020) / (0.22 - 0.020)
                new_df['ES_20in'] = ES_20in
                
                #forty - S
                ES_40in = ((new_df['SMS-40.0in'] / 100)-0.020) / (0.225 - 0.030)
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                    
                # #store it 
                store[i] = new_df
            
        return store
    
    def AVG(df):
        '''
        

        Parameters
        ----------
        df : pandas df
            Pass the df from OTHER_ESM in the assumptions.py script.

        Returns
        -------
        store : pandas df
            contains seven day avereages of the effective satuaration.

        '''
        store = {}
        
        for i in df:
            f = df[i]
            f.sort_index(inplace=True)
            f = f.rolling('7D', min_periods=3).mean()
            store[i] = f
            
        return store
    
    def JULIAN(df):
        store = {}
        
        for i in df:
            f = df[i]
            f.asfreq('D')
            f['jday'] = f.index.strftime('%j')
            f.reset_index(inplace=True)
            MASK = f.loc[f['jday'] == '366'].index
            NEW_DF = f.drop(MASK)
            store[i] = NEW_DF
            
        return store
    
    def ANOM(df):
        store = {}
        
        for i in df:
            f = df[i]
            day_mean = f.groupby(f.jday).mean()
            merge = f.merge(day_mean, on='jday', how='left', sort=False)
            merge.set_index('Date', inplace=True)
            merge.sort_index()
            merge['ANOM_2in'] = (merge['ES_2in_x'] - merge['ES_2in_y'])
            merge['ANOM_4in'] = (merge['ES_4in_x'] - merge['ES_4in_y'])
            merge['ANOM_8in'] = (merge['ES_8in_x'] - merge['ES_8in_y'])
            merge['ANOM_20in'] = (merge['ES_20in_x'] - merge['ES_20in_y'])
            merge['ANOM_40in'] = (merge['ES_40in_x'] - merge['ES_40in_y'])
            merge['StationTriplet'] = i
            merge = merge[['jday', 'ANOM_2in', 'ANOM_4in', 'ANOM_8in', 
                              'ANOM_20in', 'ANOM_40in', 'StationTriplet']]
            store[i] = merge
            
        return store
    
    def MERGE(df):
        
        values = pd.concat(df.values())
        merge = values.merge(GOES_READ, )
        
        return store
    
    def RUN(data=None):
        '''
        

        Parameters
        ----------
        data : type = pandas dataframe
            SCAN_READ. The default is None.

        Returns
        -------
        Effective Saturation anomaly dataframe for each station in Alabama as a dictionary.

        '''
        I = SCAN(data=data)
        soils = I.soil_class().unpack().OTHER_ESM()
        avg = AVG(soils)
        jul = JULIAN(avg)
        anom = ANOM(jul)
        #merge = MERGE(anom)
        
        return anom
    
    def STATION(station=None):
        '''

        Parameters
        ----------
        station : type = str
            Input the desired alabama station triplet as a string. The default is None.

        Returns
        -------
        Print Statement 
            (Station, [list of soil types by depth]).

        '''
        I = SCAN(data=SCAN_READ)
        soils = I.soil_class().unpack().show()
        st = soils[soils['station'] == station]
        two = st['two_in_soil'].unique()[0]
        four = st['four_in_soil'].unique()[0]
        eight = st['eight_in_soil'].unique()[0]
        twenty = st['twenty_in_soil'].unique()[0]
        forty = st['forty_in_soil'].unique()[0]
        statement = (station + ' ', 'two: {}'.format(two), 'four: {}'.format(four), 
              'eight: {}'.format(eight), 'twenty: {}'.format(twenty), 
              'forty: {}'.format(forty))
        return print(statement)
        
    def show(self):
         '''
         Purpose: 
             return the self.stations property in its current form. 
             
         returns: 
             printed dataframe
         '''
         return self.stations
     