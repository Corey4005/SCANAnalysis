# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pathlib import Path
import pandas as pd

# create the data path
SCAN_DATA = Path.home() / 'Desktop' / 'Data' / 'SCAN_Data' / 'SCAN_2057.csv'
READ_SCAN = pd.read_csv(SCAN_DATA)
DF = pd.DataFrame(READ_SCAN)

#convert date to dt object
DF['Date'] = pd.to_datetime(DF['Date'])


#group by 7 days and find mean values

group = DF.groupby(pd.Grouper(key='Date', freq='7D')).mean()
new_df = pd.DataFrame(group).to_excel('2057.xlsx')







    





