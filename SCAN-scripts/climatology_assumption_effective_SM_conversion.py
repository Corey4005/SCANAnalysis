#imports 
import pandas as pd
from climatology_assumption import SCAN
from climatology_assumption import SCAN_READ
from climatology_assumption import theta_table
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText

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

def plot(df, station=None, depth=None):
    '''
    

    Parameters
    ----------
    df : Pandas Dataframe
        Pass the cleaned_df variable from the climatology_assumption_effective_SM_conversion.py script. 
    station : str, not optional
        Set the station to the SCAN site you would like to plot.
        ex:
            station='2173:AL:SCAN'
    depth : str, not optional
        Set the depth by calling the column. You may call 2, 4, 8, 20 and 40 inches below the surface. 
        ex:
            depth='SMS-2.0in_x'

    Returns
    -------
    Plot of climatology with labeled theta_r, theta_s as well as a comparison to Parish et. al. lookup
    table and save to relevant filepath
    

    '''
    station_df = df[df['station'] == station][depth]
    tt = theta_tab[theta_tab['station'] == station]
    climate_theta_r = float(tt[tt['depths'] == depth]['assumed_climatology_theta_r'].item())
    climate_theta_s = float(tt[tt['depths'] == depth]['assumed_climatology_theta_s'].item())
    physical_theta_r = float(tt[tt['depths'] == depth]['physical_theta_r'].item())
    physcial_theta_s = float(tt[tt['depths'] == depth]['physical_theta_s'].item())
    fig, ax = plt.subplots(nrows=1,ncols=1)
    station_df.plot(ax=ax)
    ax.annotate('climate_r: {} \nphysical_r: {} \nclimate_s: {} \nphysical_s {}'
                .format(climate_theta_r, physical_theta_r, climate_theta_s, physcial_theta_s), 
                xy=(1.05,0), xycoords="axes fraction", bbox=dict(boxstyle="round", fc="w"))
    ax.set_title(station + ' ' + depth)
    figname = station[0:4] + '_' + depth[4:6]
    plt.savefig('C:/Users/cwalker/Desktop/SCAN_CHECKS/' + figname, bbox_inches='tight')
    
