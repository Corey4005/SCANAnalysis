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

SCAN_ALL = '../data/SCAN_DEPTHS_ALL.csv'
SCAN_READ = pd.read_csv(SCAN_ALL)

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
                   (self.new_df['station'] == '2053:AL:SCAN')]
    
    def soil_class(self): 
        
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
                
                #I would not trust the 2in soil moisture caluculations here for now because 
                #np.nans in iron measurement. I am not sure how it still calculates, even when 2in FE is nan. 
                
                soil_dict = {'two': 'LS', 'four': 'LS', 
                              'eight':'SL', 'twenty': 'SCLGR', 'forty': 'GRCL'}
                
                dict_list.append(soil_dict)
                
            elif i == '2053:AL:SCAN':
                
                soil_dict = {'two': 'SICL', 'four': 'SIL', 
                              'eight':'SIL', 'twenty': 'SICL', 
                              'forty': 'CL'}
            
            
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
            #silty clay loam
            if self.stations['two_in_soil'][i] == 'SICL':
                ES = ((self.stations['SMS-2.0in'][i] / 100)- 0.089) / (0.43 - 0.089)
                ES_2.append(ES)
            
            elif self.stations['two_in_soi'][i] == '': 
                pass
        print(ES_2)
                
                #(self.stations['two_in_soil'])
                       #- 0.089) / (0.43 - 0.089))
                #ES_2.append(ES)
        
        #self.stations['ES_2in'] = ES_2
            
    def show(self):
         '''
         Purpose: 
             return the self.stations property in its current form. 
             
         returns: 
             printed dataframe
         '''
         return self.stations
     