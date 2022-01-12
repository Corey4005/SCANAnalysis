# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 12:30:50 2021

@author: cwalker
"""
# import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import keras 
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import linear_model
from textwrap import wrap

import warnings
warnings.filterwarnings("ignore")


#read in the ESI data
GOES_ESI_ALL = '../data/1_wk_ESI_all.csv'
GOES_READ = pd.read_csv(GOES_ESI_ALL)

#read in the SCAN data
SCAN_ALL = '../data/SCAN_DEPTHS_ALL.csv'
SCAN_READ = pd.read_csv(SCAN_ALL)

CLIMATE_SERVE_ALL = '../data/ESI_1wk_tif2select_pt.csv'
CLIMATE_SERVE_READ = pd.read_csv(CLIMATE_SERVE_ALL)

#create the mean anomaly for 

# Just get the columns we are interested in and convert dates to datetime
SMS = SCAN_READ[['Date', 'station','SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in','SMS-40.0in']].copy()
SMS['Date'] = pd.to_datetime(SMS['Date'], format='%m/%d/%y')
GOES_READ['Date'] = pd.to_datetime(GOES_READ['Date'])

#create a test variable to run the code on to see if it works 
TEST = SMS[(SMS['station'] == '2057:AL:SCAN') | 
           (SMS['station'] == '2113:AL:SCAN') 
           | (SMS['station'] == '2055:AL:SCAN') | 
            (SMS['station'] == '2180:AL:SCAN') | 
            (SMS['station'] == '2114:AL:SCAN') |
            (SMS['station'] == '2056:AL:SCAN') |
            (SMS['station'] == '2115:AL:SCAN') |
            (SMS['station'] == '2053:AL:SCAN')]

def SOIL_TYPE(SMS):
    
    '''
    Purpose: 
        Takes in a test dataframe containing volumetric soil moisture information 
        by station and date and outputs soil parameters column. 
        
    Parameters: 
        df containing the following station information (note - other stations will not work). 
        - '2057:AL:SCAN'
        - '2113:AL:SCAN'
        - '2055:AL:SCAN'
        - '2180:AL:SCAN'
        - '2114:AL:SCAN'
        - '2056:AL:SCAN'
        - '2115:AL:SCAN'
        - '2053:AL:SCAN'
        
    Example Usage: 
        new_df = SOIL_TYPE(TEST)
        
    Returns: 
        SMS - Pandas DataFrame containing the soil characteristics in the form 
        of a dictonary for each of the six stations listed in parameters tag 
        above. 
    '''
    dict_list = []
    
#stations to work on still

# 2053:AL:SCAN

#stations that need assumptions 
#2078 - missing bulk density measurments 
#2177 - lab, pedon report measurements overestimate effective soil moisture by 2
#2174 - pedon report missing
#2173 - lab
#2178 - missing soil characterization 'field texture'
#2181 - no field texture characterization
#2182 - no pedon report 
#2176 - no field texture characterization. 
#2179 - missibg field texture characterization 
#2175 - missing field texture characterization
#

    print('Appending Soil Types by Station Now!')
    
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
    
        elif i == '2055:AL:SCAN':
            #two and four in are gravelly
            soil_dict = {'two': 'GRSIL', 'four': 'GRSIL', 
                         'eight':'GRSIL', 'twenty': 'SICL', 
                         'forty': 'SICL', 'OC2in': 3.0, 'OC4in': 3.0, 
                         'OC8in': 0.4, 'OC20in': 0.2, 'OC40in': 0.2, 'FE2in': 0.7,
                         'FE4in': 0.7, 'FE8in': 1.5, 'FE20in': 3.6, 'FE40in': 3.8, 
                         'Db2in': 1.20, 'Db4in': 1.20, 'Db8in': 1.34, 'Db20in': 1.29,
                         'Db40in': 1.15, 'Kpa2in': 9.8, 'Kpa4in': 9.8, 
                         'Kpa8in': 8.9, 'Kpa20in': 22.4, 'Kpa40in': 23.1}
            dict_list.append(soil_dict)
            
        elif i == '2180:AL:SCAN':
            soil_dict = {'two': 'SL', 'four': 'SL', 
                         'eight':'SL', 'twenty': 'SL', 
                         'forty': 'SCL','OC2in': 0.9, 'OC4in': 0.9, 
                         'OC8in': 0.9, 'OC20in': 0.2, 'OC40in': 0.1,'FE2in': 0.7,
                         'FE4in': 0.7, 'FE8in': 0.7, 'FE20in': 1.6, 'FE40in': 2.5, 
                         'Db2in': 1.67, 'Db4in': 1.67, 'Db8in': 1.67, 'Db20in': 1.61,
                         'Db40in': 1.70,'Kpa2in': 4.6, 'Kpa4in': 4.6, 
                         'Kpa8in': 4.6, 'Kpa20in': 7.1, 'Kpa40in': 10.6}
            
            dict_list.append(soil_dict)
            
        elif i == '2114:AL:SCAN': 
            soil_dict = {'two': 'SIL', 'four': 'SIC', 
                         'eight':'C', 'twenty': 'C', 
                         'forty': 'C','OC2in': 2.9, 'OC4in': 1.3, 
                         'OC8in': 0.8, 'OC20in': 0.4, 'OC40in': 0.2,'FE2in': 1.4,
                         'FE4in': 2.0, 'FE8in': 2.2, 'FE20in': 2.2, 'FE40in': 2.1, 
                         'Db2in': 1.03, 'Db4in': 1.39, 'Db8in': 1.36, 'Db20in': 1.53,
                         'Db40in': 1.61,'Kpa2in': 17.8, 'Kpa4in': 15.0, 
                         'Kpa8in': 16.8, 'Kpa20in': 16.1, 'Kpa40in': 12.1}
            
            dict_list.append(soil_dict)
        
        elif i == '2056:AL:SCAN':
            soil_dict = {'two': 'L', 'four': 'L', 
                          'eight':'CL', 'twenty': 'C', 
                          'forty': 'C','OC2in': 2.3, 'OC4in': 2.3, 
                          'OC8in': 0.7, 'OC20in': 0.3, 'OC40in': 0.3,'FE2in': 1.2,
                          'FE4in': 1.2, 'FE8in': 1.2, 'FE20in': 1.4, 'FE40in': 1.4, 
                          'Db2in': 1.36, 'Db4in': 1.36, 'Db8in': 1.66, 'Db20in': 1.59,
                          'Db40in': 1.59,'Kpa2in': 9.6, 'Kpa4in': 9.6, 
                          'Kpa8in': 9.1, 'Kpa20in': 10.0, 'Kpa40in': 10.0}
                
            dict_list.append(soil_dict)
            
        elif i == '2115:AL:SCAN':
            
            #I would not trust the 2in soil moisture caluculations here for now because 
            #np.nans in iron measurement. I am not sure how it still calculates, even when 2in FE is nan. 
            
            soil_dict = {'two': 'LS', 'four': 'LS', 
                          'eight':'SL', 'twenty': 'SCLGR', 
                          'forty': 'GRCL','OC2in': 0.4, 'OC4in': 0.4, 
                          'OC8in': 0.2, 'OC20in': 0.1, 'OC40in': 0.1,'FE2in': np.nan,
                          'FE4in': np.nan, 'FE8in': 0.4, 'FE20in': 1.0, 'FE40in': 2.6, 
                          'Db2in': 1.48, 'Db4in': 1.48, 'Db8in': 1.62, 'Db20in': 1.56,
                          'Db40in': 1.62,'Kpa2in': 1.6, 'Kpa4in': 1.6, 
                          'Kpa8in': 4.2, 'Kpa20in': 7.3, 'Kpa40in': 13.8}
            
            dict_list.append(soil_dict)
            
        elif i == '2053:AL:SCAN':
            
            soil_dict = {'two': 'SICL', 'four': 'SIL', 
                          'eight':'SIL', 'twenty': 'SICL', 
                          'forty': 'CL','OC2in': 1.9, 'OC4in': 1.1, 
                          'OC8in': 1.1, 'OC20in': 0.2, 'OC40in': 0.2,'FE2in': 2.3,
                          'FE4in': 1.5, 'FE8in': 1.5, 'FE20in': 2.2, 'FE40in': 3.8, 
                          'Db2in': 1.53, 'Db4in': 1.55, 'Db8in': 1.55, 'Db20in': 1.39,
                          'Db40in': 1.49,'Kpa2in': 13.5, 'Kpa4in': 10.4, 
                          'Kpa8in': 10.4, 'Kpa20in': 15.2, 'Kpa40in': 20.7}
        
        
            dict_list.append(soil_dict)
            
    SMS['Soil Class Dictionary'] = dict_list
    
    print('Soil Type by Station Appended!')
    return SMS

def CALCULATE_ESM(SMS):
    '''
    Purpose: 
        converts volumetric soil moisture columns to van ganuchin effective soil 
        moisture into effective soil moisture for each level (2in, 4in, 8in, 20in, 40in)
        
    Parameters: 
        Must input dataframe created by SOIL_TYPE() function in 
        effective_SM_conversion_all.py module. 
        
    Example Usage: 
        new_df = SOIL_TYPE(TEST)
        ESM = CALCULATE_ESM(new_df)
        
    returns: 
        SMS - Pandas Dataframe containing effective soil moisture calculations 
        by column. 
    '''
    

    print('Calculating Effective Soil Moisture by Station Now!')
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
    print('.')
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
    print('..')
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
    print('...')
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
    print('....')
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
    print('.....')
       
    #put the 
    SMS['station'] = station
    SMS['Soil Dictionary'] = lis_dict
    SMS['Date'] = Date
    
    #create the new df
    SMS = SMS[['Date', 'station', 'Soil Dictionary', '2in_esm', '4in_esm', '8in_esm',
        '20in_esm', '40in_esm']]
   
    
    # #append the stations back after numerical calculations as well as soil dictionary
    print('Effective Soil Moisture Calculation Finished!')
    return SMS

def RETURN_HIGH_LOW(value): 
    '''
    Purpose: 
        applied in the ESM_ANOM() function to convert effective soil moisture
        calculations as an internal function to appropriate 'high' / 'low' tags
        for logistic regression modeling later. 
        
    Parameters: 
        None 
    
    Returns: 
        Pandas Series containing 'high' / 'low' values for each effective 
        soil moisture column. 
    
    '''
    
    if value > 0:
        return 'high'
    else:
        return 'low'
    
def ESM_ANOM(SMS): 
    '''
    Purpose: 
        Converts daily soil moisture means to rolling seven day means. Then
        subtracts this mean from the rolling mean from the all years average to get an 
        anomaly. 
    Parameters: Requires either the test 
    Returnns: 
        Dictionary containing the anomaly dataframe for each soil moisture station
        
    '''
    print('Calculating the Effective Soil Moisture Anomaly Now!')
    #come back to here and fix the string issues where soil class is dropped. 
    df_dict = {}
    for i in SMS['station'].unique():
        DF = SMS[SMS['station'] == i]
        DF.set_index('Date', inplace=True)
        NEW_DF = DF.sort_index()
       
        #create a 7 day rolling mean for the dataset 
        NEW_DF['2in_mean'] = NEW_DF['2in_esm'].rolling('7D', min_periods=3).mean()
        NEW_DF['4in_mean'] = NEW_DF['4in_esm'].rolling('7D', min_periods=3).mean()
        NEW_DF['8in_mean'] = NEW_DF['8in_esm'].rolling('7D', min_periods=3).mean()
        NEW_DF['20in_mean'] = NEW_DF['20in_esm'].rolling('7D', min_periods=3).mean()
        NEW_DF['40in_mean'] = NEW_DF['40in_esm'].rolling('7D', min_periods=3).mean()
        NEW_DF = NEW_DF.asfreq('D')
        
        NEW_DF = NEW_DF[['2in_mean','4in_mean', '8in_mean', 
                         '20in_mean', '40in_mean', 'Soil Dictionary']]
        
        # #create a julian day column for the dataset 
        NEW_DF['jday'] = NEW_DF.index.strftime('%j')
        NEW_DF.reset_index(inplace=True)
    
        
        #drop jday 366
        MASK = NEW_DF.loc[NEW_DF['jday'] == '366'].index
        NEW_DF = NEW_DF.drop(MASK)
        
        
        #create a mean for all weeks in the dataset by julian day
        DAY_MEAN = NEW_DF.groupby([NEW_DF.jday]).mean()
        
        #create the anomaly dataframe
        ANOM = NEW_DF.merge(DAY_MEAN, on='jday', how='left', sort=False)
        ANOM.set_index('Date', inplace=True)
        ANOM.sort_index()
        
        #create the anomaly calculations
        ANOM['ANOM_2in'] = (ANOM['2in_mean_x'] - ANOM['2in_mean_y'])
        ANOM['ANOM_4in'] = (ANOM['4in_mean_x'] - ANOM['4in_mean_y'])
        ANOM['ANOM_8in'] = (ANOM['8in_mean_x'] - ANOM['8in_mean_y'])
        ANOM['ANOM_20in'] = (ANOM['20in_mean_x'] - ANOM['20in_mean_y'])
        ANOM['ANOM_40in'] = (ANOM['40in_mean_x'] - ANOM['40in_mean_y'])
        
        
        FUNC = lambda x: RETURN_HIGH_LOW(x)
        ANOM['2_highlow'] = ANOM['ANOM_2in'].apply(FUNC)
        ANOM['4_highlow'] = ANOM['ANOM_4in'].apply(FUNC)
        ANOM['8_highlow'] = ANOM['ANOM_8in'].apply(FUNC)
        ANOM['20_highlow'] = ANOM['ANOM_20in'].apply(FUNC)
        ANOM['40_highlow'] = ANOM['ANOM_40in'].apply(FUNC)
        #create the new dataframe
        ANOM = ANOM[['jday', '2_highlow', '4_highlow', '8_highlow', '20_highlow', 
                     '40_highlow', 'ANOM_2in', 'ANOM_4in', 'ANOM_8in', 'ANOM_20in',
        'ANOM_40in', 'Soil Dictionary']]
        
        
        #create a dictionary to store all ANOM dataframes
        df_dict[i] = ANOM
    print('Soil Moisture Anomaly Calculation and High-Low Classes Created')
    return df_dict
        
def MERGE(ANOM_dict):
    
    '''
    Purpose: 
        Merges ESI 1-week values with anomaly dataframe created by ESM_ANOM()
        function in the effective_SM_conversion_all.py module. 
        
    
    '''
    print('Merging the Dataframe with ESI values now!')
    df_dic = {}
    for i in ANOM_dict:
        SMS = ANOM_dict.get(i)
        SMS.reset_index(inplace=True)
        GOES = GOES_READ[GOES_READ['StationTriplet'] == i]
        MERGE = GOES.merge(SMS, on='Date', how='left')
        MERGE = MERGE[['Date', 'StationTriplet', 'ESI','ANOM_2in', 'ANOM_4in',
                       '2_highlow', '4_highlow', '8_highlow', '20_highlow', 
                       '40_highlow', 'ANOM_8in', 'ANOM_20in', 'ANOM_40in', 
                       'Soil Dictionary']]
        MERGE.set_index('Date', inplace=True)
        MASK_ESI = MERGE.loc[MERGE['ESI'] == -9999].index
        MERGE = MERGE.drop(MASK_ESI)
        MERGE = MERGE.dropna()
        

        df_dic[i] = MERGE
    print('Merging Done!')
    return df_dic


def UNPACK(df_dic): 
    print('Unpacking Soil Classes!')
    df_list = [v for k,v in df_dic.items()] 
    df = pd.concat(df_list, axis=0)
    two = lambda x: x.get('two')
    four = lambda x: x.get('four')
    eight = lambda x: x.get('eight')
    twenty = lambda x: x.get('twenty')
    forty = lambda x: x.get('forty')
    df['SoilType_Two'] = df['Soil Dictionary'].apply(two)
    df['SoilType_Four'] = df['Soil Dictionary'].apply(four)
    df['SoilType_Eight'] = df['Soil Dictionary'].apply(eight)
    df['SoilType_Twenty'] = df['Soil Dictionary'].apply(twenty)
    df['SoilType_Forty'] = df['Soil Dictionary'].apply(forty)
    df = df.drop('Soil Dictionary', axis=1)
    print('Soil Classes Unpacked!')
    return df

def MAKE_DF(SMS): 
    SOILS = SOIL_TYPE(SMS)
    ESM = CALCULATE_ESM(SOILS)
    ANOM = ESM_ANOM(ESM)
    MERGED = MERGE(ANOM)
    UNPACKED = UNPACK(MERGED)
    return UNPACKED

def CORRELATE(MERGE_dic):
    COR_DIC = {}
    for i in MERGE_dic: 
        STN = MERGE_dic.get(i)
        DF = STN[STN['StationTriplet'] == i]
        CORR = DF.corr()
        CORR = pd.DataFrame(CORR['ESI'])
        CORR['station'] = i
        COR_DIC[i] = CORR
    return COR_DIC

def CORRELATE_BY_MONTH_STN(df, station): 
    
    '''
    Parameters: 
        Requires dataframe created by the MAKE_DF() function in the 
        effective_SM_conversion_all.py

        
    Returns: 
        Matplotlib plot of correlation of ESI vs Effective Soil Moisture for 
        station of interest. 
    
    Usage: 
        corr = CORRELATE_BY_MONTH_ALL(df, station)
        
        stations you can input as string: 
            
            - '2057:AL:SCAN'
            - '2113:AL:SCAN'
            - '2055:AL:SCAN'
            - '2180:AL:SCAN'
            - '2114:AL:SCAN'
            - '2056:AL:SCAN'
            - '2115:AL:SCAN'
            - '2053:AL:SCAN'
    '''
    month_list = []
    two_in_cor = []
    four_in_cor = []
    eight_in_cor = []
    twenty_in_cor = []
    forty_in_cor = []
    station_trip = []
    max_year_v = []
    min_year_v = []

    for i in df['StationTriplet'].unique(): 
       new = df[df['StationTriplet'] == i]
       
       max_year = new.index.year.max()
       min_year = new.index.year.min()
    
       
       for j in new.index.month.unique():
           station_trip.append(i)
           max_year_v.append(max_year)
           min_year_v.append(min_year)
           
           month_list.append(j)
           month_df = new.loc[new.index.month == j]
           corr = month_df.corr()['ESI']
           #get two in 
           two_in = corr.get('ANOM_2in')
           two_in_cor.append(two_in)
           
           #get four in 
           four_in = corr.get('ANOM_4in')
           four_in_cor.append(four_in)
           
           #get eight in
           eight_in = corr.get('ANOM_8in')
           eight_in_cor.append(eight_in)
           
           #get twenty in
           twenty_in = corr.get('ANOM_20in')
           twenty_in_cor.append(twenty_in)
           
           #get forty in
           forty_in = corr.get('ANOM_40in')
           forty_in_cor.append(forty_in)
           
           
           
    corr_df = pd.DataFrame()
    corr_df['max_year'] = max_year_v
    corr_df['min_year'] = min_year_v
    corr_df['station'] = station_trip
    corr_df['month'] = month_list
    corr_df['2in'] = two_in_cor
    corr_df['4in'] = four_in_cor
    corr_df['8in'] = eight_in_cor
    corr_df['20in'] = twenty_in_cor
    corr_df['40in'] = forty_in_cor
    
    #get station dataframe
    station_info = corr_df[corr_df['station'] == station]
    station_info.set_index('month', inplace=True)
    station_info.sort_index(inplace=True)
    
    #get max year and min year for plot
    max_year = station_info.iloc[0]['max_year']
    min_year = station_info.iloc[0]['min_year']
    
    station_info.drop(['max_year', 'min_year'], inplace=True, axis=1)
    
    plt.figure(figsize=(10,15))
    plot = station_info.plot()
    plot.set_title('{}-{} USDA SCAN Site {} ES vs ESI by month'
                   .format(min_year, max_year, station))
    plot.set_ylabel('R Value')
  

def CORRELATE_BY_DAY_STN(df, station): 
    
    '''
    Parameters: 
        Requires dataframe created by the MAKE_DF() function in the 
        effective_SM_conversion_all.py

        
    Returns: 
        Matplotlib plot of correlation of ESI vs Effective Soil Moisture for 
        station of interest by day. 
    
    Usage: 
        corr = CORRELATE_BY_DAY(df, station)
        
        stations you can input as string: 
            
            - '2057:AL:SCAN'
            - '2113:AL:SCAN'
            - '2055:AL:SCAN'
            - '2180:AL:SCAN'
            - '2114:AL:SCAN'
            - '2056:AL:SCAN'
            - '2115:AL:SCAN'
            - '2053:AL:SCAN'
    '''
    day_list = []
    two_in_cor = []
    four_in_cor = []
    eight_in_cor = []
    twenty_in_cor = []
    forty_in_cor = []
    station_trip = []
    max_year_v = []
    min_year_v = []
    
    for i in df['StationTriplet'].unique(): 
       new = df[df['StationTriplet'] == i]
       max_year = new.index.year.max()
       min_year = new.index.year.min()
       new['jday'] = new.index.strftime('%j')
       new.reset_index(inplace=True)
       for j in new['jday'].unique():
           station_trip.append(i)
           max_year_v.append(max_year)
           min_year_v.append(min_year)
           day_list.append(j)
           day_df = new.loc[new['jday'] == j]
           corr = day_df.corr()['ESI']
           #get two in 
           two_in = corr.get('ANOM_2in')
           two_in_cor.append(two_in)
           
           #get four in 
           four_in = corr.get('ANOM_4in')
           four_in_cor.append(four_in)
           
           #get eight in
           eight_in = corr.get('ANOM_8in')
           eight_in_cor.append(eight_in)
           
           #get twenty in
           twenty_in = corr.get('ANOM_20in')
           twenty_in_cor.append(twenty_in)
           
           #get forty in
           forty_in = corr.get('ANOM_40in')
           forty_in_cor.append(forty_in)
           
    corr_df = pd.DataFrame()
    corr_df['max_year'] = max_year_v
    corr_df['min_year'] = min_year_v
    corr_df['station'] = station_trip
    corr_df['day'] = day_list
    corr_df['2in'] = two_in_cor
    corr_df['4in'] = four_in_cor
    corr_df['8in'] = eight_in_cor
    corr_df['20in'] = twenty_in_cor
    corr_df['40in'] = forty_in_cor
    
    station_info = corr_df[corr_df['station'] == station]
    station_info.set_index('day', inplace=True)
    station_info.sort_index(inplace=True)
    
    #get max year and min year for plot
    max_year = station_info.iloc[0]['max_year']
    min_year = station_info.iloc[0]['min_year']
    
    station_info.drop(['max_year', 'min_year'], inplace=True, axis=1)
    
    plt.figure(figsize=(10,15))
    plot = station_info.plot()
    plot.set_title('{}-{} USDA SCAN Site {} ES vs ESI by jday'
                   .format(min_year, max_year, station))

    plot.set_ylabel('R Value')
    

def CORRELATE_BY_DAY_ALL(df): 
    df_dict = {}
    sites_list = list(df['StationTriplet'].unique())
    for i in df['StationTriplet'].unique(): 
       new = df[df['StationTriplet'] == i]
       new.sort_index(inplace=True)
       max_year = new.index.year.max()
       min_year = new.index.year.min()
       new['jday'] = new.index.strftime('%j')
       new['max_year'] = max_year
       new['min_year'] = min_year
       new.reset_index(inplace=True)
       df_dict[i] = new
    
    df_list = [v for k,v in df_dict.items()] 
    df = pd.concat(df_list, axis=0)
    
    #set max and min year for plots 
    max_year = df['max_year'].max()
    min_year = df['min_year'].min()
    
    #set up the lists for the new df
    two_in_cor = []
    four_in_cor = []
    eight_in_cor = []
    twenty_in_cor = []
    forty_in_cor = []
    day_list = []
    
    for i in df['jday'].unique():
        day_list.append(i)
        day_df = df.loc[df['jday'] == i]
        corr = day_df.corr()['ESI']
        
        two_in = corr.get('ANOM_2in')
        two_in_cor.append(two_in)
        
        #get four in 
        four_in = corr.get('ANOM_4in')
        four_in_cor.append(four_in)
        
        #get eight in
        eight_in = corr.get('ANOM_8in')
        eight_in_cor.append(eight_in)
        
        #get twenty in
        twenty_in = corr.get('ANOM_20in')
        twenty_in_cor.append(twenty_in)
        
        #get forty in
        forty_in = corr.get('ANOM_40in')
        forty_in_cor.append(forty_in)
        
    corr_df = pd.DataFrame()
    corr_df['jday'] = day_list
    corr_df['2in'] = two_in_cor
    corr_df['4in'] = four_in_cor
    corr_df['8in'] = eight_in_cor
    corr_df['20in'] = twenty_in_cor
    corr_df['40in'] = forty_in_cor
    
    corr_df.set_index('jday', inplace=True)
    corr_df.sort_index(inplace=True)
    
    
    plot = corr_df.plot()
    
    stations = ', '.join(sites_list)
    title = '{}-{} USDA SCAN Effective Saturation vs ALEXI ESI. Sites Included: {}'.format(min_year, max_year, stations)
    
    plot.set_title("\n".join(wrap(title)))
    plot.set_ylabel('R Value')
                   
def UNSTACK_PLOT(COR_DIC):
    DF = pd.concat(COR_DIC)
    DF = DF.unstack(level=-1)['ESI']
    DF = DF.drop(['ESI'], axis=1)
    DF.reset_index(inplace=True)
    TIDY = DF.melt(id_vars='index')
    fig, ax = plt.subplots(figsize=(12,10))
    PLOT = sns.barplot(x='index', y='value', hue='variable', data=TIDY, ax=ax)
    ax.set_xlabel('Station')
    ax.set_ylabel('R Value')
    ax.set_title('Station Volumetric Soil Moisture Pairwise Correlations with GOES')
    return PLOT
    

def PLOT_ALL_CORR(SMS):
    SOILS = SOIL_TYPE(SMS)
    ESM = CALCULATE_ESM(SOILS)
    ANOM = ESM_ANOM(ESM)
    MERGED = MERGE(ANOM)
    CORR = CORRELATE(MERGED)
    PLOT = UNSTACK_PLOT(CORR)
    return PLOT


def CONVERT_PREDICTIONS(pred): 
    #for low
    if pred > 0.5: 
        return 1
    
    #for high
    else: 
        return 0
    
def MODEL_ESI_FROM_DF(df):
    
    #get the dummies for the model
    dummies = pd.get_dummies(df[[ 'SoilType_Two', 'SoilType_Four', 
                                'SoilType_Eight', 'SoilType_Twenty']], 
                             drop_first=True)
    
    df = df.drop(['StationTriplet', 'SoilType_Two', 
                 'SoilType_Four', 'SoilType_Eight', 
                 'SoilType_Twenty', 'SoilType_Forty'], axis=1)
    
    df = pd.concat([df, dummies], axis=1)
    
    #set the values for the train test split 
    SMS = df.drop('ESI', axis=1).values
    SAT = df['ESI'].values
    
    
    #train test split
    SMS_train, SMS_test, SAT_train, SAT_test = train_test_split(SMS, SAT, test_size=0.3, 
                                                        random_state=101)
  
    
    
    #scale the data from 0-1 before testing. 
    scaler = MinMaxScaler()
    SMS_train = scaler.fit_transform(SMS_train)
    SMS_test = scaler.transform(SMS_test)
    
    
    #create keras model
    
    mae = tf.keras.losses.MeanAbsoluteError()
    model = Sequential()
    
    model.add(Dense(28, activation='relu'))
    model.add(Dropout(0.5))
              
    model.add(Dense(14, activation='relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(1))
    
    model.compile(optimizer='adam', loss=mae)
    

    early_stop = EarlyStopping(monitor='val_loss', mode='min',verbose=1, patience=25)


    model.fit(x=SMS_train, y=SAT_train, validation_data=(SMS_test, SAT_test), 
              epochs=500, verbose=True, callbacks=[early_stop])
    
    
    loss = pd.DataFrame(model.history.history)
    
    predict_ESI = model.predict(SMS_test)
    
    plt.scatter(SAT_test, predict_ESI)
    plt.plot(SAT_test, SAT_test, 'r')
    
    
    #metrics analysis
    
    # loss = pd.DataFrame(model.history.history)

    
def MODEL_2IN_HL_FROM_ESI(df): 
    #get the dummies for the model
    
    dummies = pd.get_dummies(df[['SoilType_Two', 'SoilType_Four', 
                                'SoilType_Eight', 'SoilType_Twenty', 
                                'SoilType_Forty']], drop_first=True)
    
    
    df = df.drop(['StationTriplet', 'SoilType_Two', 'SoilType_Four', 'SoilType_Eight', 
                  'SoilType_Twenty', 'SoilType_Forty', 
                  'ANOM_2in', 'ANOM_4in', 'ANOM_8in', 
                  'ANOM_20in', 'ANOM_40in', '4_highlow', 
                  '8_highlow', '20_highlow', '40_highlow'], axis=1)

    df = pd.concat([df, dummies], axis=1)
    
    df = df.drop(['SoilType_Four_GRSIL', 'SoilType_Four_L',
    'SoilType_Four_LS', 'SoilType_Four_SIC', 'SoilType_Four_SICL',
    'SoilType_Four_SIL', 'SoilType_Four_SL', 'SoilType_Eight_CL',
    'SoilType_Eight_FSL', 'SoilType_Eight_GRSIL', 'SoilType_Eight_SICL',
    'SoilType_Eight_SIL', 'SoilType_Eight_SL', 'SoilType_Twenty_L',
    'SoilType_Twenty_SCLGR', 'SoilType_Twenty_SICL', 'SoilType_Twenty_SL',
    'SoilType_Forty_CL', 'SoilType_Forty_GRCL', 'SoilType_Forty_L',
    'SoilType_Forty_SCL', 'SoilType_Forty_SICL'], axis=1)
    
    
    #set the values for the train test split 
    X = df.drop(['2_highlow'], axis=1).values
    y = df['2_highlow'].values
    
    
    encoder = LabelEncoder()
    encoded_y = encoder.fit_transform(y)

    
    #train test split
    X_train, X_test, y_train, y_test = train_test_split(X, encoded_y, test_size=0.3, 
                                                        random_state=101)
    
    
    #scale the data from 0-1 before testing. 
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    #create keras model
    model = Sequential()
    
    model.add(Dense(7, activation='relu', input_shape=(7, )))
    model.add(Dropout(0.2))
              
    model.add(Dense(4, activation='relu'))
    model.add(Dropout(0.2))
    
    model.add(Dense(1, activation='sigmoid'))
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    

    early_stop = EarlyStopping(monitor='accuracy', mode='max',verbose=1, patience=25)


    model.fit(x=X_train, y=y_train, validation_data=(X_test, y_test), 
                epochs=500, verbose=True, callbacks=[early_stop])
    
    predictions = model.predict(X_test)
    
    out = list(map(CONVERT_PREDICTIONS, predictions))
    
    cm = confusion_matrix(y_test, out)
    print(cm)
    
    cr = classification_report(y_test, out, output_dict=True)
    print(cr)
   
    return cr
    
    
def MODEL_4IN_HL_FROM_ESI(df): 
    #get the dummies for the model
    
    dummies = pd.get_dummies(df[['SoilType_Two', 'SoilType_Four', 
                                'SoilType_Eight', 'SoilType_Twenty', 
                                'SoilType_Forty']], drop_first=True)
    
    
    df = df.drop(['StationTriplet', 'SoilType_Two', 'SoilType_Four', 'SoilType_Eight', 
                  'SoilType_Twenty', 'SoilType_Forty', 
                  'ANOM_2in', 'ANOM_4in', 'ANOM_8in', 
                  'ANOM_20in', 'ANOM_40in', '2_highlow', 
                  '8_highlow', '20_highlow', '40_highlow'], axis=1)

    df = pd.concat([df, dummies], axis=1)
    
    
    df = df.drop(['SoilType_Two_LS', 'SoilType_Two_SICL', 'SoilType_Two_SIL',
    'SoilType_Two_SL', 'SoilType_Eight_CL', 'SoilType_Two_GRSIL', 'SoilType_Two_L',
    'SoilType_Eight_FSL', 'SoilType_Eight_GRSIL', 'SoilType_Eight_SICL',
    'SoilType_Eight_SIL', 'SoilType_Eight_SL', 'SoilType_Twenty_L',
    'SoilType_Twenty_SCLGR', 'SoilType_Twenty_SICL', 'SoilType_Twenty_SL',
    'SoilType_Forty_CL', 'SoilType_Forty_GRCL', 'SoilType_Forty_L',
    'SoilType_Forty_SCL', 'SoilType_Forty_SICL'], axis=1)
   
    
    #set the values for the train test split 
    X = df.drop(['4_highlow'], axis=1).values
    y = df['4_highlow'].values
    
    
    encoder = LabelEncoder()
    encoded_y = encoder.fit_transform(y)

    
    #train test split
    X_train, X_test, y_train, y_test = train_test_split(X, encoded_y, test_size=0.3, 
                                                        random_state=101)
    
    
    #scale the data from 0-1 before testing. 
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    #create keras model
    model = Sequential()
    
    model.add(Dense(8, activation='relu', input_shape=(8, )))
    model.add(Dropout(0.2))
              
    model.add(Dense(4, activation='relu'))
    model.add(Dropout(0.2))
    
    model.add(Dense(1, activation='sigmoid'))
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    

    early_stop = EarlyStopping(monitor='accuracy', mode='max',verbose=1, patience=25)


    model.fit(x=X_train, y=y_train, validation_data=(X_test, y_test), 
                epochs=500, verbose=True, callbacks=[early_stop])
    
    predictions = model.predict(X_test)
    
    out = list(map(CONVERT_PREDICTIONS, predictions))
    
    cm = confusion_matrix(y_test, out)
    print(cm)
    
   
    cr = classification_report(y_test, out, output_dict=True)
    print(cr)
   
    return cr
    
def MODEL_8IN_HL_FROM_ESI(df): 
    #get the dummies for the model
    
    dummies = pd.get_dummies(df[['SoilType_Two', 'SoilType_Four', 
                                'SoilType_Eight', 'SoilType_Twenty', 
                                'SoilType_Forty']], drop_first=True)
    
    
    df = df.drop(['StationTriplet', 'SoilType_Two', 'SoilType_Four', 'SoilType_Eight', 
                  'SoilType_Twenty', 'SoilType_Forty', 
                  'ANOM_2in', 'ANOM_4in', 'ANOM_8in', 
                  'ANOM_20in', 'ANOM_40in', '2_highlow', '4_highlow', 
                  '20_highlow', '40_highlow'], axis=1)

    df = pd.concat([df, dummies], axis=1)
    

    df = df.drop(['SoilType_Two_GRSIL', 'SoilType_Two_L',
           'SoilType_Two_LS', 'SoilType_Two_SICL', 'SoilType_Two_SIL',
           'SoilType_Two_SL', 'SoilType_Four_GRSIL', 'SoilType_Four_L',
           'SoilType_Four_LS', 'SoilType_Four_SIC', 'SoilType_Four_SICL',
           'SoilType_Four_SIL', 'SoilType_Four_SL', 'SoilType_Twenty_L',
           'SoilType_Twenty_SCLGR', 'SoilType_Twenty_SICL', 'SoilType_Twenty_SL',
           'SoilType_Forty_CL', 'SoilType_Forty_GRCL', 'SoilType_Forty_L',
           'SoilType_Forty_SCL', 'SoilType_Forty_SICL'], axis=1)
    
    #set the values for the train test split 
    X = df.drop(['8_highlow'], axis=1).values
    y = df['8_highlow'].values
    
    encoder = LabelEncoder()
    encoded_y = encoder.fit_transform(y)

    
    #train test split
    X_train, X_test, y_train, y_test = train_test_split(X, encoded_y, test_size=0.3, 
                                                        random_state=101)
    
    
    #scale the data from 0-1 before testing. 
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    #create keras model
    model = Sequential()
    
    model.add(Dense(7, activation='relu', input_shape=(7, )))
    model.add(Dropout(0.2))
              
    model.add(Dense(4, activation='relu'))
    model.add(Dropout(0.2))
    
    model.add(Dense(1, activation='sigmoid'))
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    

    early_stop = EarlyStopping(monitor='accuracy', mode='max',verbose=1, patience=25)


    model.fit(x=X_train, y=y_train, validation_data=(X_test, y_test), 
                epochs=500, verbose=True, callbacks=[early_stop])
    
    predictions = model.predict(X_test)
    
    out = list(map(CONVERT_PREDICTIONS, predictions))
    
    cm = confusion_matrix(y_test, out)
    print(cm)
    
    cr = classification_report(y_test, out, output_dict=True)
    print(cr)
    
    return cr
    
def MODEL_20IN_HL_FROM_ESI(df): 
    #get the dummies for the model
    
    dummies = pd.get_dummies(df[['SoilType_Two', 'SoilType_Four', 
                                'SoilType_Eight', 'SoilType_Twenty', 
                                'SoilType_Forty']], drop_first=True)
    
    
    df = df.drop(['StationTriplet', 'SoilType_Two', 'SoilType_Four', 'SoilType_Eight', 
                  'SoilType_Twenty', 'SoilType_Forty', 
                  'ANOM_2in', 'ANOM_4in', 'ANOM_8in', 
                  'ANOM_20in', 'ANOM_40in', '2_highlow', '4_highlow', 
                  '8_highlow', '40_highlow'], axis=1)
    
    
    df = pd.concat([df, dummies], axis=1)
    
    df = df.drop(['SoilType_Two_GRSIL', 'SoilType_Two_L',
           'SoilType_Two_LS', 'SoilType_Two_SICL', 'SoilType_Two_SIL',
           'SoilType_Two_SL', 'SoilType_Four_GRSIL', 'SoilType_Four_L',
           'SoilType_Four_LS', 'SoilType_Four_SIC', 'SoilType_Four_SICL',
           'SoilType_Four_SIL', 'SoilType_Four_SL', 'SoilType_Eight_CL',
           'SoilType_Eight_FSL', 'SoilType_Eight_GRSIL', 'SoilType_Eight_SICL',
           'SoilType_Eight_SIL', 'SoilType_Eight_SL','SoilType_Forty_CL', 'SoilType_Forty_GRCL', 'SoilType_Forty_L',
           'SoilType_Forty_SCL', 'SoilType_Forty_SICL'], axis=1)
    
    
    
    #set the values for the train test split 
    X = df.drop(['20_highlow'], axis=1).values
    y = df['20_highlow'].values
    
    encoder = LabelEncoder()
    encoded_y = encoder.fit_transform(y)

    
    #train test split
    X_train, X_test, y_train, y_test = train_test_split(X, encoded_y, test_size=0.3, 
                                                        random_state=101)
    
    
    #scale the data from 0-1 before testing. 
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    #create keras model
    model = Sequential()
    
    model.add(Dense(5, activation='relu', input_shape=(5, )))
    model.add(Dropout(0.2))
              
    model.add(Dense(3, activation='relu'))
    model.add(Dropout(0.2))
    
    model.add(Dense(1, activation='sigmoid'))
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    

    early_stop = EarlyStopping(monitor='accuracy', mode='max',verbose=1, patience=25)


    model.fit(x=X_train, y=y_train, validation_data=(X_test, y_test), 
                epochs=500, verbose=True, callbacks=[early_stop])
    
    predictions = model.predict(X_test)
    
    out = list(map(CONVERT_PREDICTIONS, predictions))
    
    cm = confusion_matrix(y_test, out)
    print(cm)
    
    cr = classification_report(y_test, out, output_dict=True)
    print(cr)
    
    return cr
    
def MODEL_40IN_HL_FROM_ESI(df): 
    
    #get the dummies for the model
    dummies = pd.get_dummies(df[['SoilType_Two', 'SoilType_Four', 
                                'SoilType_Eight', 'SoilType_Twenty', 
                                'SoilType_Forty']], drop_first=True)
    
    
    df = df.drop(['StationTriplet', 'SoilType_Two', 'SoilType_Four', 'SoilType_Eight', 
                  'SoilType_Twenty', 'SoilType_Forty', 
                  'ANOM_2in', 'ANOM_4in', 'ANOM_8in', 
                  'ANOM_20in', 'ANOM_40in', '2_highlow', '4_highlow', 
                  '8_highlow', '20_highlow'], axis=1)
    
    
    df = pd.concat([df, dummies], axis=1)
    
    df = df.drop(['SoilType_Two_GRSIL', 'SoilType_Two_L',
           'SoilType_Two_LS', 'SoilType_Two_SICL', 'SoilType_Two_SIL',
           'SoilType_Two_SL', 'SoilType_Four_GRSIL', 'SoilType_Four_L',
           'SoilType_Four_LS', 'SoilType_Four_SIC', 'SoilType_Four_SICL',
           'SoilType_Four_SIL', 'SoilType_Four_SL', 'SoilType_Eight_CL',
           'SoilType_Eight_FSL', 'SoilType_Eight_GRSIL', 'SoilType_Eight_SICL',
           'SoilType_Eight_SIL', 'SoilType_Eight_SL', 'SoilType_Twenty_L',
           'SoilType_Twenty_SCLGR', 'SoilType_Twenty_SICL', 'SoilType_Twenty_SL'], axis=1)
    
    print(df.columns)
    
    #set the values for the train test split 
    X = df.drop(['40_highlow'], axis=1).values
    y = df['40_highlow'].values
    
    encoder = LabelEncoder()
    encoded_y = encoder.fit_transform(y)

    
    #train test split
    X_train, X_test, y_train, y_test = train_test_split(X, encoded_y, test_size=0.3, 
                                                        random_state=101)
    
    
    #scale the data from 0-1 before testing. 
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    #create keras model
    model = Sequential()
    
    model.add(Dense(6, activation='relu', input_shape=(6, )))
    model.add(Dropout(0.2))
              
    model.add(Dense(3, activation='relu'))
    model.add(Dropout(0.2))
    
    model.add(Dense(1, activation='sigmoid'))
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    

    early_stop = EarlyStopping(monitor='accuracy', mode='max',verbose=1, patience=25)


    model.fit(x=X_train, y=y_train, validation_data=(X_test, y_test), 
                epochs=500, verbose=True, callbacks=[early_stop])
    
    predictions = model.predict(X_test)
    
    out = list(map(CONVERT_PREDICTIONS, predictions))
    
    cm = confusion_matrix(y_test, out)
    print(cm)
    
    cr = classification_report(y_test, out, output_dict=True)
    print(cr)
    
    return cr
def ALL_MODELS(df): 
    two_in = MODEL_2IN_HL_FROM_ESI(df)
    four_in = MODEL_4IN_HL_FROM_ESI(df)
    eight_in = MODEL_8IN_HL_FROM_ESI(df)
    twenty_in = MODEL_20IN_HL_FROM_ESI(df)
    forty_in = MODEL_40IN_HL_FROM_ESI(df)
    
    two_acc = two_in.get('accuracy')
    four_acc = four_in.get('accuracy')
    eight_acc = eight_in.get('accuracy')
    twenty_acc = twenty_in.get('accuracy')
    forty_acc = forty_in.get('accuracy')
    
    models_list = ['two_in', 'four_in', 'eight_in', 'twenty_in', 'forty_in']
    acc_list = [two_acc, four_acc, eight_acc, twenty_acc, forty_acc]
    new_df = pd.DataFrame(models_list, columns=['models'])
    new_df['accuracy'] = acc_list
    
    return new_df
def CONVERT_IN_TO_CM(soil_inches = [2, 4, 8, 20, 40]):
        """
        FUNCTION INFO: function will convert inches to centimeters. 
        
        PARAMATERS: 
            soil_inches (list) - A list of desired sensor depths in inches. 
            Default argument is [2, 4, 8, 20, 40] for most but can be 
            changed for desired depths. 
            
        OUTPUT: 
            prints a conversion to centimeters for every inch argument in 
            soil_inches parameter. 
        

        """
        for i in soil_inches: 
            print('{} inches is:'.format(i), i*2.54, 'centimeters')



