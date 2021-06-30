# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pathlib import Path
import pandas as pd
import glob2

# create the data path
filepath = r'C:\\Users\cwalker\Desktop\Data\SCAN_Data'
files = glob2.glob(filepath + '/*.csv')

savepath = Path.home() / 'Desktop' / 'Data' / 'Processed_SCAN'


#convert date to dt object


#create the output filename for each file. 
#group by 7 days and find mean values
for file in files: 
    READ_SCAN = pd.read_csv(file)
    DF = pd.DataFrame(READ_SCAN)
    DF['Date'] = pd.to_datetime(DF['Date'])
    Station = str(DF.loc[1, 'Station Id'])
    file_name = 'SCAN' + '_' + Station + '.csv'
    group = DF.groupby(pd.Grouper(key='Date', freq='7D')).mean()
    new_df = pd.DataFrame(group)
    filename = savepath / file_name
    new_df.to_csv(filename)

    
    









    





