# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 10:42:54 2021

@author: cwalker
"""



import pandas as pd 
import numpy as np

file = 'C:/Users/cwalker/Desktop/Data/SCAN_Data/SCAN_2020.csv'
savepath = 'C:/Users/cwalker/Desktop/Data/SCAN_Data'

def scan_extract(file):
    READ_SCAN = pd.read_csv(file)
    DF = pd.DataFrame(READ_SCAN)
    DF['Date'] = pd.to_datetime(DF['Date'])
    file_name = savepath + '/SCAN' + '_' + 'Processed' + '.csv'
    group = DF.groupby(pd.Grouper(key='Date', freq='7D')).mean()
    new_df = pd.DataFrame(group)
    new_df = new_df.fillna(np.nan)
    new_df.to_csv(file_name)
    return 
    
if __name__ == '__main__':
    scan_extract(file)
    
    
