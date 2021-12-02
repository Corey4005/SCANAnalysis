# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 12:30:50 2021

@author: cwalker
"""
# import packages
import pandas as pd
import numpy as np

#read in the ESI data
GOES_ESI_ALL = '../../Data/Processed_ESI/1_wk_ESI_all.csv'
GOES_READ = pd.read_csv(GOES_ESI_ALL)

#read in the SCAN data
SCAN_ALL = '../data/SCAN_DEPTHS_ALL.csv'
SCAN_READ = pd.read_csv(SCAN_ALL)

# Just get the columns we are interested in and convert dates to datetime
SMS = SCAN_READ[['Date', 'station','SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in','SMS-40.0in']].copy()
SMS['Date'] = pd.to_datetime(SMS['Date'])


# #effective SM
# (convert_column - theta_r)/(Porosity - theta_r)

def SoilType(SMS):
    dict_list = []
    for i in SMS['station']:
        if i == '2057:AL:SCAN':
            soil_dict = {'two':'silty clay loam', 'four':'silty clay loam', 
                         'eight':'silty clay loam', 'twenty':'silty clay loam', 
                         'forty':'silty clay loam'}
            dict_list.append(soil_dict)
        elif i == '2078:AL:SCAN':
            soil_dict = {'two':'silty clay loam', 'four':'silty clay', 
                         'eight':'clay', 'twenty':'clay', 
                         'forty':'clay'}
            dict_list.append(soil_dict)
        elif i == '2177:AL:SCAN':
            #used lab measurements because field were missing from Pedon. 
            soil_dict = {'two':'silty clay', 'four':'silty clay', 
                         'eight':'silty clay', 'twenty':'clay', 
                         'forty':'clay'}
            dict_list.append(soil_dict)
        elif i == '2113:AL:SCAN':
            #two in and four in are fine sandy loam
            soil_dict = {'two':'sandy loam', 'four':'sandy loam', 
                         'eight':'sandy loam', 'twenty':'loam', 
                         'forty':'loam'}
            dict_list.append(soil_dict)
        elif i == '2174:AL:SCAN':
            #This station does not have soil classification data on USDA SCAN. 
            soil_dict = {'two': np.nan, 'four': np.nan, 
                         'eight': np.nan, 'twenty': np.nan, 
                         'forty': np.nan}
            dict_list.append(soil_dict)
        elif i == '2055:AL:SCAN':
            #two and four in are gravelly
            soil_dict = {'two': 'silt loam', 'four': 'silt loam', 
                         'eight':'silt loam', 'twenty': 'silty clay', 
                         'forty': 'silty clay'}
            dict_list.append(soil_dict)
        elif i == '2173:AL:SCAN': 
            
    SMS['Soil Class Dictionary'] = dict_list
    return SMS

def GetThetar_Two(SMS):
    two_list = []
    two_thetar = []
    
    for i in SMS['Soil Dictionary']:
        twoin = i.get('two')
        two_list.append(twoin)
    for i in two_list: 
        if i == 'silty clay loam':
            theta_r = 0.070
            two_thetar.append(theta_r)
    return SMS['2in Theta_r']
    
    
# 2173:AL:SCAN
# 2180:AL:SCAN
# 2114:AL:SCAN
# 2178:AL:SCAN
# 2181:AL:SCAN
# 2182:AL:SCAN
# 2176:AL:SCAN
# 2056:AL:SCAN
# 2179:AL:SCAN
# 2115:AL:SCAN
# 2175:AL:SCAN
# 2053:AL:SCAN