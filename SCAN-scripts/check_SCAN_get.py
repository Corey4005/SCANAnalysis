#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 15:35:38 2022

@author: ellenbw
@author: cwalker

Important website:
    
    The website with documentation on how to call the web-data from the API is 
    below:
    
    
        https://www.nrcs.usda.gov/wps/portal/wcc/home/dataAccessHelp/webService/webServiceReference/
    
    
    
"""


import pandas as pd
from zeep import Client
from zeep.transports import Transport
from requests import Session
import urllib3
from datetime import date, timedelta, datetime
import numpy as np
import sys
import matplotlib.pyplot as plt
import pytz

# filepath to current soil moisture df
# if you dont have the data, get it here: https://github.com/Corey4005/SCANAnalysis/blob/main/data/SCAN_DEPTHS_ALL.csv
all_sm_df = '../data/SCAN_DEPTHS_ALL.csv'
smdf = pd.read_csv(all_sm_df)

#create a depth variable to check both datasets with
input_depth = float(input('input a depth [-2.0, -4.0, -8.0, -20.0, -40.0] :' ))

# get correct column name from the input variable
column_dict = {-2.0:'SMS-2.0in', 
               -4.0:'SMS-4.0in', 
               -8.0:'SMS-8.0in',
               -20.0:'SMS-20.0in',
               -40.0: 'SMS-40.0in'
    }
soil_depth = column_dict[input_depth]

#get volumntric soil moisture values for smdf
smdf = smdf[[soil_depth, 'Date', 'station']]
smdf['Date'] = pd.to_datetime(smdf['Date'])

#get timezone
cen = pytz.timezone('US/Central')
utc = pytz.utc
#fmt = '%Y-%m-%d %H:%M:%S %Z%z'

#start session
urllib3.disable_warnings()
session = Session()
session.verify = False
wsdl = 'https://wcc.sc.egov.usda.gov/awdbWebService/services?WSDL'

# Intialize the client
client = Client(wsdl, transport=Transport(session=session))


#start date / end date
start_date = date(2006,5,20).strftime('%Y-%m-%d')
end_date = date(2021,3,31).strftime('%Y-%m-%d')

#station params
param = 'SMS'
stn = '2115:AL:SCAN'
depth = input_depth

#call the client and get data
retval = client.service.getData(stationTriplets=stn, elementCd=param, ordinal=1,
                                                duration='DAILY', getFlags=False, beginDate=start_date,
                                                alwaysReturnDailyFeb29=False, endDate=end_date,
                                                heightDepth={'unitCd': 'in', 'value': depth})


#make the dataframe of data from client
temp_df = pd.DataFrame()
temp_df['Date'] = pd.date_range(start=retval[0].beginDate, end=retval[0].endDate, freq='D')
result = [val for val in retval[0].values]

# here, I make the list items a float value, or NaN (for easier downstream data analyses)
result2 = []

for x in result:
    try:
        result2.append(float(x))
    except:
        result2.append(np.nan)
        
# creating column name with depth and "in" for inches
col_name = str(str(param) + str(depth) + 'in')

# append the data to the new column
temp_df[col_name] = result2

# create a column for station info
temp_df['station'] = stn

# merge for comparison
merged = pd.merge(temp_df, smdf, on=['Date', 'station'], how='inner')
merged.set_index('Date', inplace=True)
merged.plot()