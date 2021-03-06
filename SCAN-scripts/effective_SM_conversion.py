#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 15:01:33 2021

@author: Lee Ellenburg, Corey Walker
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

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

#set up date range you are interested in
print('Enter a year you want the plots to begin with:')
start_year = int(input())


print('Enter a year you want the plots to end with:')
end_year = int(input())

#set up the station you want to run the query for
st = '2053:AL:SCAN'

#set up and read in the ESI data
esi_path = '../data/ESI_1wk_from_tif.csv'
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

#Set a dataframe just for the raw data
sms_station_2053_raw = sms_station_2053[['SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in',
       'SMS-40.0in']]

#Subset the raw data for comparison later
sms_station_2053_raw = sms_station_2053[(sms_station_2053_raw.index.year >= start_year) & (sms_station_2053_raw.index.year <=end_year)]

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
day_mean = day_mean[day_mean.index != '366']

day_std = esm_2053.groupby([esm_2053.jday]).std()

#index for specific years and insert values when the dates are off. 
i_years = esm_2053[(esm_2053.index.year >= start_year) & 
                   (esm_2053.index.year <= end_year)].asfreq('D')

#drop the 366 days because we dont want leap years.
i_years = i_years[i_years['jday'] != '366']

#get rid of jday so that we can subtract correct shapes
i_years.drop(columns='jday', inplace=True)

#create a length based on years that will be used for the subtraction for anomaly. 
years = len(i_years.index.year.unique())
day_mean_final = pd.concat([day_mean]*years)

#create the df that will subtract from i_years to create anomaly. 
i_years_anom = (i_years.values-day_mean_final.values)        

#create a new df for anom
anom = pd.DataFrame(i_years_anom)

#name the columns and the index. 
anom.columns = i_years.columns
anom.index = i_years.index

#lets get all the data for the esi station in question for the tif files 
station_2053_esi_1wk_tif = esi[esi['station'] == st]

#we need to subset the tif data by the start and end year
station_2053_esi_1wk_tif = station_2053_esi_1wk_tif[(station_2053_esi_1wk_tif.index.year >= start_year) & (station_2053_esi_1wk_tif.index.year <=end_year) & (station_2053_esi_1wk_tif['ESI'] > -9999.0)]

#create the 4wk Climate Serve Data Frame
station_2053_esi_4wk_CS = pd.read_csv('../data/ESI_4wk_CS.csv', index_col = [0], infer_datetime_format = True, parse_dates = True)

#subset the Climate Serve Data with the start and end year
station_2053_esi_4wk_CS = station_2053_esi_4wk_CS[(station_2053_esi_4wk_CS.index.year >= start_year) & (station_2053_esi_4wk_CS.index.year <=end_year) & (station_2053_esi_4wk_CS['Timeseries'] > -9999.0)]

#make the sm plot comparing raw data to esm
fig, ax = plt.subplots(ncols=2, figsize=(20,10))
ax[0].xaxis_date()
ax[1].xaxis_date()

ax[0].plot(anom['SMS-2.0in_esm'], label='2in ESM')
ax[0].plot(anom['SMS-4.0in_esm'], label='4in ESM')
ax[0].plot(anom['SMS-8.0in_esm'], label='8in ESM')
ax[0].legend()
ax[0].set_title(f'2,4,8 in Effective Soil Moisture Station 2053 \n Years: {start_year} - {end_year}'.format(start_year, end_year))

ax[1].plot(sms_station_2053_raw['SMS-2.0in'], label='2in Raw')
ax[1].plot(sms_station_2053_raw['SMS-4.0in'], label='4in Raw')
ax[1].plot(sms_station_2053_raw['SMS-8.0in'], label='8in Raw')
ax[1].set_title(f'2,4,8 in Raw Soil Moisture Station 2053 \n Years: {start_year} - {end_year}'.format(start_year, end_year))
ax[1].legend()

fig.autofmt_xdate()

#create the plot comparing ESI Modis and ESM
fig1, ax1 = plt.subplots(figsize=(20,10))
ax1.plot(station_2053_esi_4wk_CS['Timeseries'], label='4wk Climate Serve ESI MODIS', color='blue')
ax1.set_xlabel('Date')
ax1.set_ylabel('ESI Anomaly % 20 Year Mean')
ax1.legend(loc=4)

#create a twinx for the 4in sm anomaly. 
ax_twin = ax1.twinx()
ax_twin.set_ylabel('4in Effective Soil Moisture Anomaly % of 20 Year Mean', color='red')

#plot the second 4in plot so that it is on the same anomaly scale. 
ax_twin.plot(anom['SMS-4.0in_esm']*10, label='4in ESM Station 2053', color='red', linestyle='--')
ax_twin.tick_params(axis='y', labelcolor='red')
ax_twin.legend(loc=3)
ax1.set_title('4 Week MODIS ESI vs 4in Effective SM')

#create the plot comparing ESI GOES and ESM
figg, axg = plt.subplots(figsize=(20,10))
axg.plot(station_2053_esi_1wk_tif['ESI'], label='1wk .tif ESI GOES', color='blue')
axg.set_xlabel('Date')
axg.set_ylabel('ESI Anomaly % 20 Year Mean')
axg.legend(loc=4)

#create a twinx for the 4in sm anomaly. 
ax_twin2 = axg.twinx()
ax_twin2.set_ylabel('4in Effective Soil Moisture Anomaly % of 20 Year Mean', color='red')

#create a twinx for the 4in sm anomaly
ax_twin2.plot(anom['SMS-4.0in_esm']*10, label='4in ESM Station 2053', color='red', linestyle='--')
ax_twin2.tick_params(axis='y', labelcolor='red')
ax_twin2.legend(loc=3)
axg.set_title('1 Week GOES ESI vs 4in Effective SM')

#create a correlation matrix for 4in vs GOES ESI
fig2, ax2 = plt.subplots(figsize=(15,10))
merged = pd.merge(anom['SMS-4.0in_esm'], station_2053_esi_1wk_tif['ESI'],left_index=True, right_index=True)
merged = merged.rename(columns={'ESI':'GOES ESI .tif'})
dropped = merged.dropna()
ax2 = sns.heatmap(dropped.corr(), annot=True, cmap='magma')
ax2.set_title(f".tif ESI vs 4in SCAN 2053 \n Years: {start_year} - {end_year}".format(start_year, end_year))

#create a correlation matrix for 4 in vs MODIS ESI
fig3, ax3 = plt.subplots(figsize=(15,10))
merged2 = pd.merge(anom['SMS-4.0in_esm'], station_2053_esi_4wk_CS['Timeseries'],left_index=True, right_index=True)
merged2 = merged2.rename(columns={'Timeseries':'MODIS ESI Climate Serve'})
dropped2 = merged2.dropna()
ax3 = sns.heatmap(dropped2.corr(), annot=True, cmap='magma')
ax3.set_title(f"Climate Serve ESI vs 4in SCAN 2053 \n Years: {start_year} - {end_year}".format(start_year, end_year))


#create an empty list 
li = [] 

for i in merged['SMS-4.0in_esm']:
    if i > 0.0:
        x = 'high'
    else:
        x = 'low'
        
    li.append(x)
    
li2 = []

for i in merged2['SMS-4.0in_esm']:
    if i > 0.0:
        x = 'high'
    else:
        x = 'low'
        
    li2.append(x)
#add the high or low values to the station dataframes
merged['Moisture Class'] = li
merged2['Moisture Class'] = li2

#create scatter plots
fig4, ax4 = plt.subplots()
ax4 = sns.scatterplot(data=merged, x='GOES ESI .tif', y=merged['SMS-4.0in_esm']*10, hue='Moisture Class')
ax4.set_title(f"GOES ESI .tif vs 4in ESM SCAN 2053 \n Years: {start_year} - {end_year}".format(start_year, end_year))
ax4.axhline(0.0, color='red', linestyle='--')
ax4.axvline(0.0, color='red', linestyle='--')

fig5, ax5 = plt.subplots()
ax5 = sns.scatterplot(data=merged2, x='MODIS ESI Climate Serve', y=merged2['SMS-4.0in_esm']*10, hue='Moisture Class')
ax5.set_title(f"MODIS ESI Climate Serve vs 4in SCAN 2053 \n Years: {start_year} - {end_year}".format(start_year, end_year))
ax5.axhline(0.0, color='red', linestyle='--')
ax5.axvline(0.0, color='red', linestyle='--')

pp = PdfPages(st[0:4]+'_'+f'{start_year}_{end_year}.pdf'.format(start_year, end_year))
pp.savefig(fig)
pp.savefig(figg)
pp.savefig(fig1)
pp.savefig(fig2)
pp.savefig(fig3)
pp.savefig(fig4)
pp.savefig(fig5)
pp.close()

