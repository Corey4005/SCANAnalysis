# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 12:30:50 2021

@author: cwalker
"""
# import packages
import pandas as pd
import numpy as np

#read in the ESI data
GOES_ESI_ALL = '../data/1_wk_ESI_all.csv'
GOES_READ = pd.read_csv(GOES_ESI_ALL)

#read in the SCAN data
SCAN_ALL = '../data/SCAN_DEPTHS_ALL.csv'
SCAN_READ = pd.read_csv(SCAN_ALL)

# Just get the columns we are interested in and convert dates to datetime
SMS = SCAN_READ[['Date', 'station','SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in','SMS-40.0in']].copy()
SMS['Date'] = pd.to_datetime(SMS['Date'])

#create a test variable to run the code on to see if it works 
TEST = SMS[SMS['station'] == '2057:AL:SCAN']
#TEST.dropna(inplace=True)

# #effective SM
# (convert_column - theta_r)/(Porosity - theta_r)

#Calculate particle density 
#Dp = 100 / (((1.7 * OC) / Dp1) + ((1.6 * FE)/Dp2) + ((100 - ((1/7 * OC) + (1.6 * FE)))/ Dp3))
def SoilType(SMS):
    dict_list = []
    for i in SMS['station']:
        if i == '2057:AL:SCAN':
            soil_dict = {'two':'silty clay loam', 'four':'silty clay loam', 
                         'eight':'silty clay loam', 'twenty':'silty clay loam', 
                         'forty':'silty clay loam', 'OC2in': 1.9, 'OC4in': 1.1, 
                         'OC8in': 1.1, 'OC20in': 0.2, 'OC40in': 0.2, 'FE2in': 2.3,
                         'FE4in': 1.5, 'FE8in': 1.5, 'FE20in': 2.2, 'FE40in': 3.8, 
                         'Db2in': 1.53, 'Db4in': 1.55, 'Db8in': 1.55, 'Db20in': 1.39,
                         'Db40in': 1.49, 'Kpa2in': 13.5, 'Kpa4in': 10.4, 
                         'Kpa8in': 10.4, 'Kpa20in': 15.2, 'Kpa40in': 20.7}
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
            soil_dict = {}
            dict_list.append(soil_dict)
        
    SMS['Soil Class Dictionary'] = dict_list
    return SMS

def CalculateESM(SMS):
    #set some knowns for conversion
    Dp1 = 1.4
    Dp2 = 4.2 
    Dp3 = 2.65
    lis_dict = []
    station = []
    #station is an object and will not be preserved in numerical calculations
    #therefore we will store it in a list to append it back to df later
    for i in SMS['station']:
        station.append(i)
        
    for i in SMS['Soil Class Dictionary']:
        #get all the variables we need for soil column calculations
        OC2in = i.get('OC2in')
        OC4in = i.get('OC4in')
        OC8in = i.get('OC8in')
        OC20in = i.get('OC20in')
        OC40in = i.get('OC40in')
        FE2in = i.get('FE2in')
        FE4in = i.get('FE4in')
        FE8in = i.get('FE8in')
        FE20in = i.get('FE20in')
        FE40in = i.get('FE40in')
        Kpa2in = i.get('Kpa2in')
        Kpa4in = i.get('Kpa4in')
        Kpa8in = i.get('Kpa8in')
        Kpa20in = i.get('Kpa20in')
        Kpa40in = i.get('Kpa40in')
        Db2in = i.get('Db2in')
        Db4in = i.get('Db4in')
        Db8in = i.get('Db8in')
        Db20in = i.get('Db20in')
        Db40in = i.get('Db40in')
        
        #we need to preserve the soil class dictionary for later as well so 
        #that it is not lost
        lis_dict.append(i)
        
        
        #calculate particle density for each level in soil column 
        Dp2in = 100 / (((1.7 * OC2in) / Dp1) + ((1.6 * FE2in)/Dp2) + 
                     ((100 - ((1/7 * OC2in) + (1.6 * FE2in)))/ Dp3))
        
        Dp4in = 100 / (((1.7 * OC4in) / Dp1) + ((1.6 * FE4in)/Dp2) + 
                     ((100 - ((1/7 * OC4in) + (1.6 * FE4in)))/ Dp3))
        
        Dp8in = 100 / (((1.7 * OC8in) / Dp1) + ((1.6 * FE8in)/Dp2) + 
                     ((100 - ((1/7 * OC8in) + (1.6 * FE8in)))/ Dp3))
        
        Dp20in = 100 / (((1.7 * OC20in) / Dp1) + ((1.6 * FE20in)/Dp2) + 
                     ((100 - ((1/7 * OC20in) + (1.6 * FE20in)))/ Dp3))
        
        Dp40in = 100 / (((1.7 * OC40in) / Dp1) + ((1.6 * FE40in)/Dp2) + 
                     ((100 - ((1/7 * OC40in) + (1.6 * FE40in)))/ Dp3))
        
        #calculate porosity for each level
        #Calculate Porosity
        P2in = 100 - (100 * Db2in/Dp2in)
        P4in = 100 - (100 * Db4in/Dp4in)
        P8in = 100 - (100 * Db8in/Dp8in)
        P20in = 100 - (100 * Db20in/Dp20in)
        P40in = 100 - (100 * Db40in/Dp40in)
        #calculate thetar for each level in soil column
        theta_r_two = 0.35 * Kpa2in
        theta_r_four = 0.35 * Kpa4in
        theta_r_eight = 0.35 * Kpa8in 
        theta_r_twenty = 0.35 * Kpa20in 
        theta_r_forty = 0.35 * Kpa40in 
        
        #calculate esm 
        SMS['2in_esm'] = (SMS['SMS-2.0in'] - theta_r_two)/(P2in - theta_r_two)
        SMS['4in_esm'] = (SMS['SMS-4.0in'] - theta_r_four)/(P4in - theta_r_four)
        SMS['8in_esm'] = (SMS['SMS-8.0in'] - theta_r_eight)/(P8in - theta_r_eight)
        SMS['20in_esm'] = (SMS['SMS-20.0in'] - theta_r_twenty)/(P20in - theta_r_twenty)
        SMS['40in_esm'] = (SMS['SMS-40.0in'] - theta_r_forty)/(P40in - theta_r_forty)
    
    SMS['station'] = station
    SMS['Soil Dictionary'] = lis_dict
    NEW_DF = SMS[['Date', 'station', 'Soil Dictionary', '2in_esm', '4in_esm', '8in_esm', '20in_esm', '40in_esm']]
    return NEW_DF
        
        
    
    
    
    
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