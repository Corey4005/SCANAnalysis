#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 15:01:33 2021

@author: Lee Ellenburg, Corey Walker
"""

import pandas as pd
import seaborn as sns
from matplotlib.offsetbox import AnchoredText
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.offsetbox import AnchoredText
import sys

#create the function we need to apply effective sm conversion
def convert(df, column='string', OC=None, FE=None, Db=None, Kpa=None): 
    '''
    
    Parameters: 
    
    :df: (Pandas Dataframe). Pass a panadas dataframe corresponding to the 
    USDA scan site data. 
    
    :column: (string). Pass a string that corresponds to the column that you 
    wish to be converted to effective soil moisture. Ex: 'SMS-2.0in'
    
    :OC: (Int). Pass an organic content measure for the soil provided from 
    your respective USDA SCAN site soil report. Ex: 1.1 (units: mm / kg)
    
    :FE: (Int). Pass an FE content measure for the soil provided from your 
    respective USDA SCAN site soil report. Ex: 2.4 (units: mm / kg)
    
    :Kpa: (Int) Pass a pressure value provided by the soil report at 1500 Kpa. 
    Ex: 13.5 (units: Kpa)
    '''
    #set up the df with the column you want to convert

    convert_column = df[column] 
    
    
    #The knowns for the equations 
    Dp1 = 1.4
    Dp2 = 4.2 
    Dp3 = 2.65
    Db = Db
    
    #Calculate particle density 
    Dp = 100 / (((1.7 * OC) / Dp1) + ((1.6 * FE)/Dp2) + ((100 - ((1/7 * OC) + (1.6 * FE)))/ Dp3))
    
    #Calculate Porosity 
    Porosity = 100 - (100 * Db/Dp)
    
    #Theta R 
    theta_r = 0.35 * Kpa
    
    #esm
    df[column + '_'+ 'esm'] = (convert_column - theta_r)/(Porosity - theta_r)
                          
    return df


#set up the station you want to run the query for
st = '2053:AL:SCAN'

#set up and read in the ESI data
esi_path = '../data/ESI_1wk_tif2select_pt.csv'
esi = pd.read_csv(esi_path)
esi['Date'] = pd.to_datetime(esi['Date'])
esi.set_index('Date', inplace=True)

# Read in the SCAN data
scan_path = '../data/SCAN_DEPTHS_ALL.csv'
scan = pd.read_csv(scan_path)

# Just get the columns we are interested in and convert dates to datetime
sms = scan[['Date', 'station','SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in','SMS-40.0in']].copy()
sms['Date'] = pd.to_datetime(sms['Date'])

# set the index for the columns we are interested in. 
sms.set_index('Date', inplace=True)
sms_station_2053 = sms[sms['station'] == st]

#do the functions to convert to effective sm for each SM column

#2in 2053
convert(sms_station_2053, 'SMS-2.0in', OC=1.9, FE=2.3, Db=1.53, Kpa=13.5)

#4in 2053
convert(sms_station_2053, 'SMS-4.0in', OC=1.1, FE=1.5, Db=1.55, Kpa=10.4)

#8in 2053
convert(sms_station_2053, 'SMS-8.0in', OC=1.1, FE=1.5, Db=1.55, Kpa=10.4)

#20in 2053
convert(sms_station_2053, 'SMS-20.0in', OC=0.2, FE=2.2, Db=1.39, Kpa=15.2)

#40in 2053
convert(sms_station_2053, 'SMS-40.0in', OC=0.2, FE=3.8, Db=1.49, Kpa=20.7)

#sort the station info to make sure it is in correct order
sms_station_2053 = sms_station_2053.sort_index()


#get the appropriate dataframe for just esm now
esm_2053 = sms_station_2053[['SMS-2.0in_esm', 'SMS-4.0in_esm', 
                             'SMS-8.0in_esm', 'SMS-20.0in_esm', 
                             'SMS-40.0in_esm',]]

#create the root_zone calculations
esm_2053['root_zone'] = (((esm_2053['SMS-4.0in_esm']+esm_2053['SMS-2.0in_esm'])/2*2+((esm_2053['SMS-8.0in_esm']+esm_2053['SMS-4.0in_esm'])/2)*4
                      +((esm_2053['SMS-20.0in_esm']+esm_2053['SMS-8.0in_esm'])/2)*12+((esm_2053['SMS-20.0in_esm']+esm_2053['SMS-40.0in_esm'])/2)*20))/38 


#convert df to a rolling weekly mean
esm_2053 = esm_2053.rolling('7D', min_periods=3).mean()

#get the julian day for each date in index
esm_2053['jday'] = esm_2053.index.strftime('%j')

##create a mean for all weeks for the entire dataset and standard deviation. 
day_mean = esm_2053.groupby([esm_2053.jday]).mean()
day_std = esm_2053.groupby([esm_2053.jday]).std()

#index for specific years
i_years = esm_2053[(esm_2053.index.year >= 2006) & (esm_2053.index.year <=2008)]


i_years = i_years.reset_index()[day_mean.columns]

day_mean.index = range(0,len(day_mean))
day_std.index = range(0,len(day_std))
i_years_anom = (i_years.reset_index()[day_mean.columns]-day_mean)

# station_2053_esi_og = esi[esi['station'] == st]

# station_2053_esi = pd.read_csv('../../esi_cs.csv', index_col = [0], infer_datetime_format = True, parse_dates = True)



# drought_year_esi = station_2053_esi[station_2053_esi['ESI'] > -9999.0]
# #drought_year_esi = station_2053_esi_og[(station_2053_esi_og.index.year >= 2006) & (station_2053_esi_og.index.year <=2006) & (station_2053_esi_og['ESI'] > -9999.0)]
# #sys.exit()
# drought_year_sms_anom = drought_year_sms_anom.iloc[:-1]


# drought_year_sms_anom.index = year_i
# drought_year_sms.index = year_i

# #drought_year_sms_anom = drought_year_sms_anom.sort_index()

# #drought_year_mean_sms_anom = drought_year_sms_anom.rolling('7D', min_periods=3).mean()

# #merged = pd.merge(drought_year_esi, drought_year_mean_sms_anom, left_index=True, right_index=True)


# #dropped = merged.dropna()

# drought_year__sms_anom = drought_year_sms_anom.dropna()
# drought_year__sms = drought_year_sms.dropna()
# '''
# dropped['root_zone'] = (((dropped['SMS-4.0in']+dropped['SMS-2.0in'])/2*2+((dropped['SMS-8.0in']+dropped['SMS-4.0in'])/2)*4
#                       +((dropped['SMS-20.0in']+dropped['SMS-8.0in'])/2)*12+((dropped['SMS-20.0in']+dropped['SMS-40.0in'])/2)*20))/38 

# dropped['root_zone_top'] = (((dropped['SMS-4.0in']+dropped['SMS-2.0in'])/2*2+((dropped['SMS-8.0in']+dropped['SMS-4.0in'])/2)*4
#                       +((dropped['SMS-20.0in']+dropped['SMS-8.0in'])/2)*12+((dropped['SMS-20.0in']+dropped['SMS-40.0in'])/2)*20))/38 

# dropped['root_zone_bot'] = (((dropped['SMS-4.0in']+dropped['SMS-2.0in'])/2*2+((dropped['SMS-8.0in']+dropped['SMS-4.0in'])/2)*4
#                       +((dropped['SMS-20.0in']+dropped['SMS-8.0in'])/2)*12+((dropped['SMS-20.0in']+dropped['SMS-40.0in'])/2)*20))/38 

# '''

# #create a timeseries plot
# fig2, ax2= plt.subplots(figsize=(20,7))
# fig2.subplots_adjust(right=0.75)

# #ESI_twin = ax2.twinx()

# Root_mean, = ax2.plot(drought_year_sms['root_zone'], color='black', label='Root Zone Weighted Mean SMS')
# Root_mean_top, = ax2.plot(drought_year_sms['root_zone_top'], color='black', linestyle = '--', label='Top Root Zone Weighted Mean SMS')
# Root_mean_bot, = ax2.plot(drought_year_sms['root_zone_bot'], color='black', linestyle = '-.', label='Bottom Root Zone Weighted Mean SMS')
# ESI, = ax2.plot(drought_year_esi ['ESI'], color='red', label='ESI')

# ax2.set_xlabel('Year')
# ax2.set_ylabel('SMS Root Zone Weighted')
# ax2.set_title('1 Year (2006) 1 Week ALEXI ESI vs 1 Week Weighted Volumetric Soil Moisture - USDA SCAN Station 2053')
# #ESI_twin_ax.set_ylabel('ESI')
# ax2.legend(handles=[Root_mean,Root_mean_top,Root_mean_bot, ESI])

# sns.set_context('notebook')


# #create a timeseries plot
# fig2, ax2= plt.subplots(figsize=(20,7))
# fig2.subplots_adjust(right=0.75)

# ESI_twin = ax2.twinx()

# SMS_4, = ax2.plot(drought_year_sms['SMS-4.0in'], color='black', label='Root Zone Weighted Mean SMS')
# #Root_mean_top, = ax2.plot(drought_year_sms_anom['root_zone_top'], color='black', linestyle = '--', label='Top Root Zone Weighted Mean SMS')
# #Root_mean_bot, = ax2.plot(drought_year_sms_anom['root_zone_bot'], color='black', linestyle = '-.', label='Bottom Root Zone Weighted Mean SMS')
# ESI, = ESI_twin.plot(drought_year_esi ['ESI'], color='red', label='ESI')

# ax2.set_xlabel('Year')
# ax2.set_ylabel('4in SMS')
# ax2.set_title('1 Year (2006) 1 Week ALEXI ESI vs 1 Week Weighted Volumetric Soil Moisture - USDA SCAN Station 2053')
# ESI_twin.set_ylabel('ESI')
# ax2.legend(handles=[SMS_4, ESI])

# sns.set_context('notebook')


# fig2, ax2= plt.subplots(figsize=(20,7))
# fig2.subplots_adjust(right=0.75)

# ESI_twin = ax2.twinx()

# SM_4, = ax2.plot(drought_year_sms_anom['SMS-4.0in'], color='black', label='4in SMS')
# #Root_mean_top, = ax2.plot(drought_year_sms['root_zone_top'], color='black', linestyle = '--', label='Top Root Zone Weighted Mean SMS')
# #Root_mean, = ax2.plot(drought_year_sms_anom['root_zone'], color='black', linestyle = '--', label='Top Root Zone Weighted Mean SMS')
# ESI, = ESI_twin.plot(drought_year_esi['ESI'], color='red', label='ESI')

# ax2.set_xlabel('Year')
# ax2.set_ylabel('4in SMS')
# ax2.set_title('1 Year (2006) 1 Week ALEXI ESI vs 1 Week Weighted Volumetric Soil Moisture - USDA SCAN Station 2053')
# ESI_twin.set_ylabel('ESI')
# ax2.legend(handles=[SM_4, ESI])

# sns.set_context('notebook')


# merged = pd.merge(drought_year_esi, drought_year_sms_anom, left_index=True, right_index=True)
# dropped = merged.dropna()
# sns.heatmap(dropped.corr(), annot=True, cmap='magma')











