#imports 
import pandas as pd
from climatology_assumption import SCAN
from climatology_assumption import SCAN_READ
from climatology_assumption import theta_table
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import seaborn as sns

#data from theta_table sorted by negative r values
path = 'C:/Users/cwalker/Desktop/SCANAnalysis/data/climatology_vs_Carsel_Parish.csv'
data = pd.read_csv(path)
negatives = data[data['theta_r_difference']<0]

#create an instance 
I = SCAN(data=SCAN_READ)

#clean the data
cleaned_df = I.standard_deviation().z_score().quality_z_score(std=3.5).clean_data().show()


#create theta table to index with
theta_tab = theta_table(cleaned_df)

#define anomaly functions
def Calculate_Climatology_ESM(df):
    '''
    

    Parameters
    ----------
    df : Pandas DataFrame
        Pass the cleaned_df from the climatology_assumption_effective_SM_conversion.py
        module

    Returns
    -------
    store : Dictionary
        Contains the Effective Saturation Values from the Cleaned Data using the climatology values
        as theta_r and theta_s.

    '''
    store = {}
    ESM = lambda x: ((x/100)-theta_r)/(theta_s-theta_r) 
    for i in cleaned_df['station'].unique():
        df = cleaned_df[cleaned_df['station'] == i]
        df = df[['SMS-2.0in_x', 'SMS-4.0in_x', 'SMS-8.0in_x', 'SMS-20.0in_x', 'SMS-40.0in_x']]
        tt = theta_tab[theta_tab['station'] == i]
        for j in df:
            theta_r = float(tt[tt['depths'] == j]['assumed_climatology_theta_r'].item())
            theta_s = float(tt[tt['depths'] == j]['assumed_climatology_theta_s'].item())
            new_col = 'ESM' + '_' + j
            df[new_col] = df[j].apply(ESM)
            
        df = df[['ESM_SMS-2.0in_x', 'ESM_SMS-4.0in_x', 
                 'ESM_SMS-8.0in_x', 'ESM_SMS-20.0in_x', 
                 'ESM_SMS-40.0in_x']]
        df.set_index('Date', inplace=True)
        store[i] = df
        
    return store

    
