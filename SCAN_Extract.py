# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pathlib import Path
import pandas as pd


#create the data path
SCAN_DATA = Path.home() / 'Desktop' / 'Data' / 'SCAN_Data' / 'SCAN_2020.csv'
READ_SCAN = pd.read_csv(SCAN_DATA)
DF = pd.DataFrame(READ_SCAN)


#convert date to dt object
DF['Date'] = pd.to_datetime(DF['Date'])

#group by 7 days and find mean values
Station_list = []
Mean_2in = []
for station in DF['Station Id'].unique():
    Station_Id = DF['Station Id']
    SEVEN_DAYS = DF.groupby(pd.Grouper(key='Date', freq='7D'))
    MEAN = SEVEN_DAYS['Soil Moisture Percent -2in (pct) Start of Day Values'].mean()
    Station_list.append(Station_Id)
    Mean_2in.append(MEAN)
    
print(Station_list, Mean_2in)
    





