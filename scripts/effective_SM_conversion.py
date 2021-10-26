#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 15:01:33 2021

@author: ellenbw
"""

import pandas as pd
import seaborn as sns
from matplotlib.offsetbox import AnchoredText
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.offsetbox import AnchoredText
import sys

st = '2053:AL:SCAN'

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

sms.set_index('Date', inplace=True)
sms_station_2053 = sms[sms['station'] == st]

sms_station_2053 = sms_station_2053.drop('station', axis = 1)

sms_station_2053.index = pd.to_datetime(sms_station_2053.index)

sms_station_2053 = (sms_station_2053-0.072)/(0.477-0.072)




sms_station_2053['root_zone'] = (((sms_station_2053['SMS-4.0in']+sms_station_2053['SMS-2.0in'])/2*2+((sms_station_2053['SMS-8.0in']+sms_station_2053['SMS-4.0in'])/2)*4
                      +((sms_station_2053['SMS-20.0in']+sms_station_2053['SMS-8.0in'])/2)*12+((sms_station_2053['SMS-20.0in']+sms_station_2053['SMS-40.0in'])/2)*20))/38

sms_station_2053['root_zone_top'] = (((sms_station_2053['SMS-4.0in']+sms_station_2053['SMS-2.0in'])/2*2+((sms_station_2053['SMS-8.0in']+sms_station_2053['SMS-4.0in'])/2)*4
                      +((sms_station_2053['SMS-20.0in']+sms_station_2053['SMS-8.0in'])/2)*12))/18

sms_station_2053['root_zone_bot'] = ((((sms_station_2053['SMS-20.0in']+sms_station_2053['SMS-8.0in'])/2)*12+((sms_station_2053['SMS-20.0in']+sms_station_2053['SMS-40.0in'])/2)*20))/32 

sms_station_2053 = sms_station_2053.sort_index()

year_i = sms_station_2053[(sms_station_2053.index.year >= 2006) & (sms_station_2053.index.year <=2006)].index



sms_station_2053 = sms_station_2053.rolling('7D', min_periods=3).mean()



sms_station_2053['jday'] = sms_station_2053.index.strftime('%j')

day_mean = sms_station_2053.groupby([sms_station_2053.jday]).mean()
day_std = sms_station_2053.groupby([sms_station_2053.jday]).std()

drought_year_sms = sms_station_2053[(sms_station_2053.index.year >= 2006) & (sms_station_2053.index.year <=2006)]

#drought_year_sms['root_zone'] = (((drought_year_sms['SMS-4.0in']+drought_year_sms['SMS-2.0in'])/2*2+((drought_year_sms['SMS-8.0in']+drought_year_sms['SMS-4.0in'])/2)*4
                      #+((drought_year_sms['SMS-20.0in']+drought_year_sms['SMS-8.0in'])/2)*12+((drought_year_sms['SMS-20.0in']+drought_year_sms['SMS-40.0in'])/2)*20))/38 




#drought_year_sms.reset_index()[day_mean.columns]

day_mean.index = range(0,len(day_mean))
day_std.index = range(0,len(day_std))
drought_year_sms_anom = (drought_year_sms.reset_index()[day_mean.columns]-day_mean)

station_2053_esi_og = esi[esi['station'] == st]

station_2053_esi = pd.read_csv('../../esi_cs.csv', index_col = [0], infer_datetime_format = True, parse_dates = True)



drought_year_esi = station_2053_esi[station_2053_esi['ESI'] > -9999.0]
#drought_year_esi = station_2053_esi_og[(station_2053_esi_og.index.year >= 2006) & (station_2053_esi_og.index.year <=2006) & (station_2053_esi_og['ESI'] > -9999.0)]
#sys.exit()
drought_year_sms_anom = drought_year_sms_anom.iloc[:-1]


drought_year_sms_anom.index = year_i
drought_year_sms.index = year_i

#drought_year_sms_anom = drought_year_sms_anom.sort_index()

#drought_year_mean_sms_anom = drought_year_sms_anom.rolling('7D', min_periods=3).mean()

#merged = pd.merge(drought_year_esi, drought_year_mean_sms_anom, left_index=True, right_index=True)


#dropped = merged.dropna()

drought_year__sms_anom = drought_year_sms_anom.dropna()
drought_year__sms = drought_year_sms.dropna()
'''
dropped['root_zone'] = (((dropped['SMS-4.0in']+dropped['SMS-2.0in'])/2*2+((dropped['SMS-8.0in']+dropped['SMS-4.0in'])/2)*4
                      +((dropped['SMS-20.0in']+dropped['SMS-8.0in'])/2)*12+((dropped['SMS-20.0in']+dropped['SMS-40.0in'])/2)*20))/38 

dropped['root_zone_top'] = (((dropped['SMS-4.0in']+dropped['SMS-2.0in'])/2*2+((dropped['SMS-8.0in']+dropped['SMS-4.0in'])/2)*4
                      +((dropped['SMS-20.0in']+dropped['SMS-8.0in'])/2)*12+((dropped['SMS-20.0in']+dropped['SMS-40.0in'])/2)*20))/38 

dropped['root_zone_bot'] = (((dropped['SMS-4.0in']+dropped['SMS-2.0in'])/2*2+((dropped['SMS-8.0in']+dropped['SMS-4.0in'])/2)*4
                      +((dropped['SMS-20.0in']+dropped['SMS-8.0in'])/2)*12+((dropped['SMS-20.0in']+dropped['SMS-40.0in'])/2)*20))/38 

'''

#create a timeseries plot
fig2, ax2= plt.subplots(figsize=(20,7))
fig2.subplots_adjust(right=0.75)

#ESI_twin = ax2.twinx()

Root_mean, = ax2.plot(drought_year_sms['root_zone'], color='black', label='Root Zone Weighted Mean SMS')
Root_mean_top, = ax2.plot(drought_year_sms['root_zone_top'], color='black', linestyle = '--', label='Top Root Zone Weighted Mean SMS')
Root_mean_bot, = ax2.plot(drought_year_sms['root_zone_bot'], color='black', linestyle = '-.', label='Bottom Root Zone Weighted Mean SMS')
ESI, = ax2.plot(drought_year_esi ['ESI'], color='red', label='ESI')

ax2.set_xlabel('Year')
ax2.set_ylabel('SMS Root Zone Weighted')
ax2.set_title('1 Year (2006) 1 Week ALEXI ESI vs 1 Week Weighted Volumetric Soil Moisture - USDA SCAN Station 2053')
#ESI_twin_ax.set_ylabel('ESI')
ax2.legend(handles=[Root_mean,Root_mean_top,Root_mean_bot, ESI])

sns.set_context('notebook')


#create a timeseries plot
fig2, ax2= plt.subplots(figsize=(20,7))
fig2.subplots_adjust(right=0.75)

ESI_twin = ax2.twinx()

SMS_4, = ax2.plot(drought_year_sms['SMS-4.0in'], color='black', label='Root Zone Weighted Mean SMS')
#Root_mean_top, = ax2.plot(drought_year_sms_anom['root_zone_top'], color='black', linestyle = '--', label='Top Root Zone Weighted Mean SMS')
#Root_mean_bot, = ax2.plot(drought_year_sms_anom['root_zone_bot'], color='black', linestyle = '-.', label='Bottom Root Zone Weighted Mean SMS')
ESI, = ESI_twin.plot(drought_year_esi ['ESI'], color='red', label='ESI')

ax2.set_xlabel('Year')
ax2.set_ylabel('4in SMS')
ax2.set_title('1 Year (2006) 1 Week ALEXI ESI vs 1 Week Weighted Volumetric Soil Moisture - USDA SCAN Station 2053')
ESI_twin.set_ylabel('ESI')
ax2.legend(handles=[SMS_4, ESI])

sns.set_context('notebook')


fig2, ax2= plt.subplots(figsize=(20,7))
fig2.subplots_adjust(right=0.75)

ESI_twin = ax2.twinx()

SM_4, = ax2.plot(drought_year_sms_anom['SMS-4.0in'], color='black', label='4in SMS')
#Root_mean_top, = ax2.plot(drought_year_sms['root_zone_top'], color='black', linestyle = '--', label='Top Root Zone Weighted Mean SMS')
#Root_mean, = ax2.plot(drought_year_sms_anom['root_zone'], color='black', linestyle = '--', label='Top Root Zone Weighted Mean SMS')
ESI, = ESI_twin.plot(drought_year_esi['ESI'], color='red', label='ESI')

ax2.set_xlabel('Year')
ax2.set_ylabel('4in SMS')
ax2.set_title('1 Year (2006) 1 Week ALEXI ESI vs 1 Week Weighted Volumetric Soil Moisture - USDA SCAN Station 2053')
ESI_twin.set_ylabel('ESI')
ax2.legend(handles=[SM_4, ESI])

sns.set_context('notebook')


merged = pd.merge(drought_year_esi, drought_year_sms_anom, left_index=True, right_index=True)
dropped = merged.dropna()
sns.heatmap(dropped.corr(), annot=True, cmap='magma')











