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
    
    '''

    def __init__(self, data):
        self.df = data
        self.new_df = self.df[['Date', 'station','SMS-2.0in', 'SMS-4.0in', 
                               'SMS-8.0in', 'SMS-20.0in','SMS-40.0in']].copy()
        self.new_df = self.new_df[(self.new_df['station'] == '2057:AL:SCAN') | 
                   (self.new_df['station'] == '2113:AL:SCAN') | 
                   (self.new_df['station'] == '2055:AL:SCAN') |
                   (self.new_df['station'] == '2180:AL:SCAN') |
                   (self.new_df['station'] == '2114:AL:SCAN') |
                   (self.new_df['station'] == '2056:AL:SCAN') |
                   (self.new_df['station'] == '2115:AL:SCAN') |
                   (self.new_df['station'] == '2053:AL:SCAN')]
    
    def soil_class(self): 
        dict_list = []
        for i in self.new_df['station']:
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
                              'eight':'CL', 'twenty': 'C'}
                    
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
                
        self.new_df['Soil Class Dictionary'] = dict_list
        
        return self.new_df
    
    def unpack(self.new_df): 
        



