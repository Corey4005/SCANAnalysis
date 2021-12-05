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
TEST = SMS[(SMS['station'] == '2057:AL:SCAN') | (SMS['station'] == '2113:AL:SCAN')]

def SoilType(SMS):
    dict_list = []
    
    for i in SMS['station']:
        if i == '2057:AL:SCAN':
            soil_dict = {'two':'SICL', 'four':'SICL', 
                         'eight':'SICL', 'twenty':'SICL', 
                         'forty':'SICL', 'OC2in': 2.5, 'OC4in': 2.5, 
                         'OC8in': 0.4, 'OC20in': 0.2, 'OC40in': 0.2, 'FE2in': 3.1,
                         'FE4in': 3.1, 'FE8in': 2.4, 'FE20in': 3.2, 'FE40in': 4.3, 
                         'Db2in': 1.03, 'Db4in': 1.03, 'Db8in': 1.42, 'Db20in': 1.44,
                         'Db40in': 1.32, 'Kpa2in': 11.4, 'Kpa4in': 11.4, 
                         'Kpa8in': 13.2, 'Kpa20in': 16.9, 'Kpa40in': 21.6}
            dict_list.append(soil_dict)
    
        elif i == '2113:AL:SCAN':
            #two in and four in are fine sandy loam
            soil_dict = {'two':'FSL', 'four':'FSL', 
                         'eight':'FSL', 'twenty':'L', 
                         'forty':'L',  'OC2in': 1.3, 'OC4in': 1.3, 
                         'OC8in': 0.4, 'OC20in': 0.2, 'OC40in': 0.1, 'FE2in': 0.5,
                         'FE4in': 0.5, 'FE8in': 0.9, 'FE20in': 1.9, 'FE40in': 2.6, 
                         'Db2in': 1.57, 'Db4in': 1.57, 'Db8in': 1.54, 'Db20in': 1.68,
                         'Db40in': 1.62, 'Kpa2in': 5.6, 'Kpa4in': 5.6, 
                         'Kpa8in': 6.2, 'Kpa20in': 10.2, 'Kpa40in': 10.8}
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
    
    #create some storage lists for the dataframe
    station = []
    lis_dict = []
    Date = []
    
    #station is an object and will not be preserved in numerical calculations
    #therefore we will store it in a list to append it back to df later
    for i in SMS['station']:
        station.append(i)
    
    for i in SMS['Date']:
        Date.append(i)
        
    for i in SMS['Soil Class Dictionary']:
        lis_dict.append(i)
        
    for i in SMS['Soil Class Dictionary']:
        #get all the variables we need for soil column calculations
        #two inch
        OC2in = i.get('OC2in')
        FE2in = i.get('FE2in')
        Kpa2in = i.get('Kpa2in')
        Db2in = i.get('Db2in')
        
        #calculate particle density for each level in soil column 
        Dp2in = 100 / (((1.7 * OC2in) / Dp1) + ((1.6 * FE2in)/Dp2) + 
                     ((100 - ((1/7 * OC2in) + (1.6 * FE2in)))/ Dp3))
        
        #calculate porosity two inch
        P2in = 100 - (100 * Db2in/Dp2in)
        
        #calculate Theta R two inch
        theta_r_two = 0.35 * Kpa2in
        
        #make the new column
        SMS['2in_esm'] = (SMS['SMS-2.0in'] - theta_r_two)/(P2in - theta_r_two)
    
    #now we make the four in column 
    for i in SMS['Soil Class Dictionary']:
        #four inch
        OC4in = i.get('OC4in')
        FE4in = i.get('FE4in')
        Kpa4in = i.get('Kpa4in')
        Db4in = i.get('Db4in')
        
        #particle density four inch
        Dp4in = 100 / (((1.7 * OC4in) / Dp1) + ((1.6 * FE4in)/Dp2) + 
                     ((100 - ((1/7 * OC4in) + (1.6 * FE4in)))/ Dp3))
        
        #porosity four in
        P4in = 100 - (100 * Db4in/Dp4in)
        
        #theta r four in
        theta_r_four = 0.35 * Kpa4in
        
        #make the column four in 
        SMS['4in_esm'] = (SMS['SMS-4.0in'] - theta_r_four)/(P4in - theta_r_four)
        
    #now we make the eight in column 
    for i in SMS['Soil Class Dictionary']:
    
        #eight inch
        OC8in = i.get('OC8in')
        FE8in = i.get('FE8in')
        Db8in = i.get('Db8in')
        Kpa8in = i.get('Kpa8in')
        
        #particle density eight in 
        Dp8in = 100 / (((1.7 * OC8in) / Dp1) + ((1.6 * FE8in)/Dp2) + 
                     ((100 - ((1/7 * OC8in) + (1.6 * FE8in)))/ Dp3))
        
        #porosity eight in 
        P8in = 100 - (100 * Db8in/Dp8in)
        
        #theta r eight in 
        theta_r_eight = 0.35 * Kpa8in 
        
        #new column eight 
        SMS['8in_esm'] = (SMS['SMS-8.0in'] - theta_r_eight)/(P8in - theta_r_eight)
    
    #now the twenty in column 
    for i in SMS['Soil Class Dictionary']:
        
        #twenty inch
        OC20in = i.get('OC20in')
        FE20in = i.get('FE20in')
        Db20in = i.get('Db20in')
        Kpa20in = i.get('Kpa20in')
        
        #particle density 
        Dp20in = 100 / (((1.7 * OC20in) / Dp1) + ((1.6 * FE20in)/Dp2) + 
                     ((100 - ((1/7 * OC20in) + (1.6 * FE20in)))/ Dp3))
        
        #porosity twenty 
        P20in = 100 - (100 * Db20in/Dp20in)
        
        #theta r twenty 
        theta_r_twenty = 0.35 * Kpa20in 
        
        #new column twenty 
        SMS['20in_esm'] = (SMS['SMS-20.0in'] - theta_r_twenty)/(P20in - theta_r_twenty)
        
    for i in SMS['Soil Class Dictionary']:
        
        #forty inch
        OC40in = i.get('OC40in')
        FE40in = i.get('FE40in')
        Db40in = i.get('Db40in')
        Kpa40in = i.get('Kpa40in')
        
        #particle density 
        Dp40in = 100 / (((1.7 * OC40in) / Dp1) + ((1.6 * FE40in)/Dp2) + 
                     ((100 - ((1/7 * OC40in) + (1.6 * FE40in)))/ Dp3))
        
        #porosity forty 
        P40in = 100 - (100 * Db40in/Dp40in)
        
        #theta r forty 
        theta_r_forty = 0.35 * Kpa40in 
        
        #new column forty 
        SMS['40in_esm'] = (SMS['SMS-40.0in'] - theta_r_forty)/(P40in - theta_r_forty)
        
       
    #put the 
    SMS['station'] = station
    SMS['Soil Dictionary'] = lis_dict
    SMS['Date'] = Date
    
    #create the new df
    SMS = SMS[['Date', 'station', 'Soil Dictionary', '2in_esm', '4in_esm', '8in_esm',
        '20in_esm', '40in_esm']]
   
    
    # #append the stations back after numerical calculations as well as soil dictionary
    return SMS
        
    
def ESM_mean(SMS): 
    df_dict = {}
    for i in SMS['station'].unique():
        DF = SMS[SMS['station'] == i]
        DF.set_index('Date', inplace=True)
        NEW_DF = DF.sort_index()
        MEAN_DF = NEW_DF.rolling('7D', min_periods=3).mean()
        df_dict[i] = MEAN_DF
    return df_dict
    
    
    
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

#stations that need assumptions 
#2078 - missing bulk density measurments 
#2177 - pedon report measurements overestimate effective soil moisture by 2

