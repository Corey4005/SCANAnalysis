#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project: 
    This is a project for calculating effective saturation at
    USDA SCAN sites given soil class and assumptions about the physical 
    characteristics for each. 

Created on Wed Jan 26 11:41:36 2022

@author: coreywalker
contact: 
    cdw0063@uah.edu
    
note: 
    Please site this repository if the functions are used in another analysis. 
    
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
from scipy.stats import pearsonr
warnings.filterwarnings('ignore')

#SCAN station data 
SCAN_ALL = '../data/SCAN_DEPTHS_ALL.csv'
SCAN_READ = pd.read_csv(SCAN_ALL)
# SCAN_READ.replace(0, np.nan)
# SCAN_READ.dropna(inplace=True)

#GOES ESI data
GOES_ESI_ALL = '../data/1_wk_ESI_all.csv'
GOES_READ = pd.read_csv(GOES_ESI_ALL)
GOES_READ['Date'] = pd.to_datetime(GOES_READ['Date'])
GOES_READ.drop('Unnamed: 0', axis=1, inplace=True)
GOES_READ = GOES_READ[GOES_READ['ESI'] > -9999]
GOES_READ.dropna(inplace=True)

#treecover data 
TREE_COVER = '../data/tree_cover_by_station_pixel.csv'
TREE_READ = pd.read_csv(TREE_COVER)
TREE_READ.drop('Unnamed: 0', axis=1, inplace=True)

class SCAN:
    '''
    SCAN CLASS - used to set Alabama SCAN sites with assumed soil 
    characteristics based on soil classes. 
        
    Class properties:
            
        self.df - pandas dataframe of SCAN_READ
                
        self.stations - pandas dataframe with all stations that have soil
            texture characteristics listed in Pedon Report
    
    Example Codes: 
        
        Return clean data
        
            I = SCAN(data=SCAN_READ)
            df = I.standard_deviation().z_score().quality_z_score(std=3.5).clean_data().show()
            
            returns: Pandas DataFrame
                Contains cleaned values at each station with data
                up to +/- 3.5 standard deviations from the mean. Each station can be 
                indexed for their particular values
                
                example: 
                    #get station 2057 information
                    
                    st2057 = df[df['station']=='2057:AL:SCAN']
                    

    '''

    def __init__(self, data):
        '''
        

        Parameters
        ----------
        data : pandas df
            Data Parameter passed in the SCAN class when initialized.

        Returns
        -------
        attributes:
            
            self.df
            self.new_df
            self.stations
        '''
        self.df = data
        self.stations = self.df[['Date', 'station','SMS-2.0in', 'SMS-4.0in', 
                               'SMS-8.0in', 'SMS-20.0in','SMS-40.0in']].copy()
    
    def standard_deviation(self):
        '''
        Purpose:
            Calculates the Standard Deviation by Month for Each USDA SCAN station
            and appends it to the dataframe. 

        Returns
        -------
        self.stations property
            This is an updated dataframe with monthly standard deviations appended
            to each reading. 

        '''
        store = {}
        df = self.stations
        for i in df['station'].unique():
            new_df = df[df['station'] == i]
            new_df.set_index('Date', inplace=True)
            new_df.index = pd.to_datetime(new_df.index)
            new_df.sort_index(inplace=True)
            std = new_df.groupby(new_df.index.month).std()
            std['station'] = i
            std.reset_index(inplace=True)
            std.rename(columns={'Date':'Month'}, inplace=True)
            
            new_df['Month'] = new_df.index.month
            new_df.reset_index(inplace=True)
            merged = new_df.merge(std, on=['station', 'Month'])
            store[i] = merged
        df = pd.concat(store, axis=0)
        df.index = df.index.get_level_values(1)
        
        self.stations = df
        return self
    
    def z_score(self): 
        '''
        Purpose: 
            Calculates Z-score for each point in the raw data. 

        Returns
        -------
        store : dictionary.
            Stations with soil moisture and z-score information. 
            
        '''
        store = {}
        for i in self.stations['station'].unique():
            new_df = self.stations[self.stations['station'] == i]
            new_df.set_index('Date', inplace=True)
            new_df.index = pd.to_datetime(new_df.index)
            new_df.sort_index(inplace=True)
            
            #create z-score column. 
            new_df['z_2'] = (new_df['SMS-2.0in_x'] - new_df['SMS-2.0in_x'].mean()) / new_df['SMS-2.0in_y']
            new_df['z_4'] = (new_df['SMS-4.0in_x'] - new_df['SMS-4.0in_x'].mean()) / new_df['SMS-4.0in_y']
            new_df['z_8'] = (new_df['SMS-8.0in_x'] - new_df['SMS-8.0in_x'].mean()) / new_df['SMS-8.0in_y']
            new_df['z_20'] = (new_df['SMS-20.0in_x'] - new_df['SMS-20.0in_x'].mean()) / new_df['SMS-20.0in_y']
            new_df['z_40'] = (new_df['SMS-40.0in_x'] - new_df['SMS-40.0in_x'].mean()) / new_df['SMS-40.0in_y']
            
            new_df = new_df[['station','SMS-2.0in_x', 'SMS-4.0in_x', 'SMS-8.0in_x', 'SMS-2.0in_y',
                             'SMS-4.0in_y', 'SMS-8.0in_y', 'SMS-20.0in_y', 'SMS-40.0in_y', 
                             'SMS-20.0in_x','SMS-40.0in_x','z_2', 'z_4', 'z_8', 'z_20', 'z_40']]
            new_df.reset_index()
            
            #store new df with z score. 
            store[i] = new_df
    
        df = pd.concat(store, axis=0)
        df.index = df.index.get_level_values(1)
        df.rename(columns={'SMS-2.0in_y': '2in-stdev', 'SMS-4.0in_y': '4in-stdev',
                           'SMS-8.0in_y': '8in-stdev', 'SMS-20.0in_y': '20in-stdev',
                           'SMS-40.0in_y': '40in-stdev'}, inplace=True)
        self.stations = df
        return self
    
    def quality_z_score(self, std=None):
        '''
        Parameters
        ----------
        std : float
            pass the number of standard deviations you would like to set as 
            'good data'. 
            
        Purpose:
            creates data quality columns depending on z-score

        Returns
        -------
        pandas dataframe
            Dataframe containing raw data, z-score and data quality columns

        '''
        df = self.stations
        std = std
        def encoder(df, column=None):
            '''
            

            Parameters
            ----------
            df : self.stations
            
            column : string, optional
                pass the column string you would like to encode. The default is None.
                

            Returns
            -------
            new_col : list
                A list of data quality ('too high, too low, or good data') 
                for the column passed in the encoder in question.

            '''
            new_col = []
            for i in df[column]:
                if i > std:
                    word = 'Too High'
                    new_col.append(word)
                elif i < -std:
                    word = 'Too Low'
                    new_col.append(word)
                else:
                    word = 'Good Data'
                    new_col.append(word)
            
            return new_col
        
        df['2in_quality'] = encoder(df, column='z_2')
        df['4in_quality'] = encoder(df, column='z_4')
        df['8in_quality'] = encoder(df, column='z_8')
        df['20in_quality'] = encoder(df, column='z_20')
        df['40in_quality'] = encoder(df, column='z_40')
        
        
        self.stations = df
        return self
    
    def clean_data(self):
        df = self.stations
        #print lengths 
        two_high = len(df.loc[df['2in_quality'] == 'Too High', 'SMS-2.0in_x'])
        two_low = len(df.loc[df['2in_quality'] == 'Too Low', 'SMS-2.0in_x'])
        
        #four 
        four_high = len(df.loc[df['4in_quality'] == 'Too High', 'SMS-4.0in_x'])
        four_low = len(df.loc[df['4in_quality'] == 'Too Low', 'SMS-4.0in_x']) 
        
        #eight
        eight_high = len(df.loc[df['8in_quality'] == 'Too High', 'SMS-8.0in_x']) 
        eight_low = len(df.loc[df['8in_quality'] == 'Too Low', 'SMS-8.0in_x'])
        
        #twenty 
        twenty_high = len(df.loc[df['20in_quality'] == 'Too High', 'SMS-20.0in_x'])
        twenty_low = len(df.loc[df['20in_quality'] == 'Too Low', 'SMS-20.0in_x'])
        
        #forty
        forty_high = len(df.loc[df['40in_quality'] == 'Too High', 'SMS-40.0in_x'])
        forty_low = len(df.loc[df['40in_quality'] == 'Too Low', 'SMS-40.0in_x'])
        
        data_scrubbed = {'two-in-cleaned': [two_high, two_low], 
                         'four-in-cleaned': [four_high, four_low],
                         'eight-in-cleaned': [eight_high, eight_low], 
                         'twenty-in-cleaned': [twenty_high, twenty_low],
                         'forty-in-cleaned':[forty_high, forty_low]}
        
        data_scrubbed_df = pd.DataFrame(data_scrubbed)
        transpose = data_scrubbed_df.transpose()
        transpose.columns=['Too High', 'Too Low']
        
        print('\n')
        print('The data cleaned as outliers are in the following dataframe:')
        print('\n')
        print(transpose)
        
        #two
        df.loc[df['2in_quality'] == 'Too High', 'SMS-2.0in_x'] = np.nan
        df.loc[df['2in_quality'] == 'Too Low', 'SMS-2.0in_x'] = np.nan
        #four
        df.loc[df['4in_quality'] == 'Too High', 'SMS-4.0in_x'] = np.nan
        df.loc[df['4in_quality'] == 'Too Low', 'SMS-4.0in_x'] = np.nan
        #eight
        df.loc[df['8in_quality'] == 'Too High', 'SMS-8.0in_x'] = np.nan
        df.loc[df['8in_quality'] == 'Too Low', 'SMS-8.0in_x'] = np.nan
        #twenty
        df.loc[df['20in_quality'] == 'Too High', 'SMS-20.0in_x'] = np.nan
        df.loc[df['20in_quality'] == 'Too Low', 'SMS-20.0in_x'] = np.nan
        #forty
        df.loc[df['40in_quality'] == 'Too High', 'SMS-40.0in_x'] = np.nan
        df.loc[df['40in_quality'] == 'Too Low', 'SMS-40.0in_x'] = np.nan
        
        #replace 0 values
        df = df.replace(0.0, np.nan)
        
        print('\n')
        #get rid of all values above 100%
        two_in_one_hundred_values = len(df[df['SMS-2.0in_x']>100])
        four_in_one_hundred_values = len(df[df['SMS-4.0in_x']>100])
        eight_in_one_hundred_values = len(df[df['SMS-8.0in_x']>100])
        twenty_in_one_hundred_values = len(df[df['SMS-20.0in_x']>100])
        forty_in_one_hundred_values = len(df[df['SMS-40.0in_x']>100])
        
        print(f'Total 2in values > 100% volumetric soil moisture cleaned: {two_in_one_hundred_values}')
        print(f'Total 4in values > 100% volumetric soil moisture cleaned: {four_in_one_hundred_values}')
        print(f'Total 8in values > 100% volumetric soil moisture cleaned: {eight_in_one_hundred_values}')
        print(f'Total 20in values > 100% volumetric soil moisture cleaned: {twenty_in_one_hundred_values}')
        print(f'Total 40in values > 100% volumetric soil moisture cleaned: {forty_in_one_hundred_values}')
        
        df.loc[df['SMS-2.0in_x']>100, 'SMS-2.0in_x'] = np.nan
        df.loc[df['SMS-4.0in_x']>100, 'SMS-4.0in_x'] = np.nan
        df.loc[df['SMS-8.0in_x']>100, 'SMS-8.0in_x'] = np.nan
        df.loc[df['SMS-20.0in_x']>100, 'SMS-20.0in_x'] = np.nan
        df.loc[df['SMS-40.0in_x']>100, 'SMS-40.0in_x'] = np.nan
        
        self.stations = df
        return self
    
    
        
    def soil_class(self): 
        #stations notes
        #2177 no field measurements of soil texture, will use lab measurements 
            #in calculation. 
        #2174 station pedon report missing. Will get info from web soil survey. 
        #2173 missing field measurements of soil texture, will use lab measures
            #in calculation.
        #2178 - missing soil characterization 'field texture', will use lab 
            #measures instead. 
        #2181 - No field or lab texture measurements. 
        #2182 - No pedon report. 
        #2176 - Unable to read soil characteristics due to inadequate depth
            #measures for each type. Therefore, this station will not be
            #included. 
        #2179 - Mising forty in soil characteristics due to inadequate depth
            #measure. Will use lab reports and web soil survey
        #2175 -
        
        '''
        Purpose:
            append the soil dictionary for each station that has an
            available pedon report in Alabama.
        
        Returns: 
            self.stations property with updated dataframe. 
        '''
        dict_list = []
        
        for i in self.stations['station']:
            if i == '2057:AL:SCAN':
                soil_dict = {'two':'SICL', 'four':'SICL', 
                             'eight':'SICL', 'twenty':'SICL', 
                             'forty':'SICL'}
                dict_list.append(soil_dict)
        
            elif i == '2113:AL:SCAN':
                #two in and four in are fine sandy loam
                soil_dict = {'two':'FSL', 'four':'FSL', 
                             'eight':'FSL', 'twenty':'L', 
                             'forty':'L'}
                dict_list.append(soil_dict)
        
            elif i == '2055:AL:SCAN':
                #two and four in are gravelly
                soil_dict = {'two': 'GRSIL', 'four': 'GRSIL', 
                             'eight':'GRSIL', 'twenty': 'SICL', 
                             'forty': 'SICL'}
                dict_list.append(soil_dict)
                
            elif i == '2180:AL:SCAN':
                soil_dict = {'two': 'SL', 'four': 'SL', 
                             'eight':'SL', 'twenty': 'SL', 
                             'forty': 'SCL'}
                
                dict_list.append(soil_dict)
                
            elif i == '2114:AL:SCAN': 
                soil_dict = {'two': 'SIL', 'four': 'SIC', 
                             'eight':'C', 'twenty': 'C', 
                             'forty': 'C'}
                
                dict_list.append(soil_dict)
            
            elif i == '2056:AL:SCAN':
                soil_dict = {'two': 'L', 'four': 'L', 
                              'eight':'CL', 'twenty': 'C', 
                              'forty':'C'}
                    
                dict_list.append(soil_dict)
                
            elif i == '2115:AL:SCAN':
                
                soil_dict = {'two': 'LS', 'four': 'LS', 
                              'eight':'SL', 'twenty': 'SCL', 'forty': 'CL'}
                
                dict_list.append(soil_dict)
                
            elif i == '2053:AL:SCAN':
                
                soil_dict = {'two': 'SICL', 'four': 'SIL', 
                              'eight':'SIL', 'twenty': 'SICL', 
                              'forty': 'CL'}
            
            
                dict_list.append(soil_dict)
            
            #new stations with assumptions
            elif i == '2078:AL:SCAN':
                
                soil_dict = {'two': 'SICL', 'four': 'SIL', 
                             'eight': 'SICL', 'twenty': 'SICL', 
                             'forty': 'CL'}
                
                dict_list.append(soil_dict)
                
            elif i == '2177:AL:SCAN':
            #using lab measurements
                
                soil_dict = {'two': 'SIC', 'four': 'SIC',
                             'eight': 'SIC', 'twenty': 'SIC', 
                             'forty': 'SIC'}
                
                dict_list.append(soil_dict)
                
            elif i == '2173:AL:SCAN':
            #using lab measurements
                soil_dict = {'two': 'SIL', 'four': 'SIL',
                             'eight': 'SICL', 'twenty': 'SICL', 
                             'forty': 'C'}
                
                dict_list.append(soil_dict)
            
            elif i == '2178:AL:SCAN':
            #using lab measures
                soil_dict = {'two': 'FSL', 'four': 'FSL', 
                             'eight': 'FSL', 'twenty': 'FSL', 
                             'forty': 'L'}
                
                dict_list.append(soil_dict)
            
            elif i == '2175:AL:SCAN':
            #using lab measures
                soil_dict = {'two': 'L', 'four': 'L', 
                             'eight': 'L', 'twenty': 'L', 
                             'forty': 'C'}
                
                dict_list.append(soil_dict)
                
            elif i == '2174:AL:SCAN':
            #using web soil survey
                soil_dict = {'two': 'SIC', 'four': 'SIC', 
                             'eight': 'C', 'twenty': 'C',
                             'forty': 'C'}
            
                dict_list.append(soil_dict)
            elif i == '2182:AL:SCAN':
            #using web soil survey
                
                soil_dict = {'two': 'LS', 'four': 'LS',
                             'eight': 'LS', 'twenty': 'FS',
                             'forty': 'SL'}
            
                dict_list.append(soil_dict)
                
            elif i == '2179:AL:SCAN':
            #lab measures and websoil survey
            
                soil_dict = {'two': 'FSL', 'four': 'FSL', 
                             'eight': 'FSL', 'twenty': 'FSL',
                             'forty': 'BRCK'}
                
                dict_list.append(soil_dict)
            
            elif i == '2181:AL:SCAN':
            #using websoil survey
            
                soil_dict = {'two': 'FSL', 'four': 'FSL', 
                             'eight': 'FSL', 'twenty': 'SL',
                             'forty': 'SCL'}
                
                dict_list.append(soil_dict)
                
            elif i == '2176:AL:SCAN':
            #using websoil survey
            
                soil_dict = {'two': 'FS', 'four': 'FS', 
                             'eight': 'FS', 'twenty': 'S',
                             'forty': 'S'}
                
                dict_list.append(soil_dict)
                
        self.stations['Soil Class Dictionary'] = dict_list
        return self
    
    def unpack(self):
        '''
        Purpose: Unpack the self.stations dataframe containing the soil texture
            class dictionaries and return pandas column with the soil
            texture class for each depth. 
            
        returns: updated self.stations dataframe. 
        '''
        
    
        #lists 
        two_in = []
        four_in = []
        eight_in = []
        twenty_in = []
        forty_in = []
        
        #get two
        for i in self.stations['Soil Class Dictionary']:
            two = i.get('two')
            two_in.append(two)
        
        self.stations['two_in_soil'] = two_in
        
        #get four
        for i in self.stations['Soil Class Dictionary']:
            four = i.get('four')
            four_in.append(four)
        
        self.stations['four_in_soil'] = four_in
                
        for i in self.stations['Soil Class Dictionary']:
            eight = i.get('eight')
            eight_in.append(eight)
        
        self.stations['eight_in_soil'] = eight_in
        
        for i in self.stations['Soil Class Dictionary']:
            twenty = i.get('twenty')
            twenty_in.append(twenty)
        
        self.stations['twenty_in_soil'] = twenty_in
        
        for i in self.stations['Soil Class Dictionary']:
            forty = i.get('forty')
            forty_in.append(forty)
        
        self.stations['forty_in_soil'] = forty_in
            
        return self
        
    def show(self):
         '''
         Purpose: 
             return the self.stations property in its current form. 
             
         returns: 
             printed dataframe
         '''
         return self.stations
     
############# NON-CLASS FUNCTIONS BELOW ###################
def theta_table(df):
    '''
    

    Parameters
    ----------
    df : Pandas DataFrame
        Pass the dataframe generated by:
            df = I.standard_deviation().z_score().quality_z_score(std=3.5).clean_data().show().

    Returns
    -------
    theta_df : Pandas DataFrame
        A dataframe containing the highest theta-s, lowest theta-r and 
        soil-type for each station for the record of climatology.

    '''
    stn = []
    depth = []
    theta_rs = []
    theta_ss = []
    ns = []
    soil_data = []
    
    #researched hydraulic properties Carsel and Parish 
    #of soil textures format: 'key': theta-r, theta-s
    #notice that GRSIL and SIL, as well as SL and FSL, as well as FS and S
    #are the same.
    properties = {'S': (0.045, 0.43),
                  'FS': (0.045, 0.43),
                  'LS': (0.057, 0.41),
                  'SL': (0.065, 0.41),
                  'FSL': (0.065, 0.41),
                  'L': (0.078, 0.43),
                  'SI': (0.034, 0.46),
                  'GRSIL': (0.067, 0.45),
                  'SIL': (0.067, 0.45),
                  'SCL': (0.1, 0.39), 
                  'CL': (0.095, 0.41), 
                  'SIC': (0.070, 0.36), 
                  'SICL': (0.089, 0.43),
                  'C': (0.068, 0.38),
                  'BRCK': (np.nan, np.nan)
        }
    
    for i in df['station'].unique():
        station_df = df[df['station'] == i]
        station_df = station_df[['SMS-2.0in_x', 'SMS-4.0in_x', 'SMS-8.0in_x', 'SMS-20.0in_x', 'SMS-40.0in_x']]
        for j in station_df:
            theta_s = station_df[j].max()/100
            theta_r = station_df[j].min()/100
            theta_s_format = '{:.4f}'.format(theta_s)
            theta_r_format = '{:.4f}'.format(theta_r)
            n = len(station_df[j])
            ns.append(n)
            soils = STATION(station=i)
            soil_at_depth = soils.get(j)
            stn.append(i)
            depth.append(j)
            theta_rs.append(theta_r_format)
            theta_ss.append(theta_s_format)
            soil_data.append(soil_at_depth)
            
    all_data = {'station':stn, 
                'depths':depth, 
                'n': ns,
                'assumed_climatology_theta_r':theta_rs, 
                'assumed_climatology_theta_s':theta_ss, 
                'soiltype': soil_data}
    
    theta_df = pd.DataFrame(all_data)
    
    #soil properties functions
    get_theta_r = lambda x: properties[x][0]
    get_theta_s = lambda x: properties[x][1]
    
    theta_df['physical_theta_r'] = theta_df['soiltype'].apply(get_theta_r)
    theta_df['physical_theta_s'] = theta_df['soiltype'].apply(get_theta_s)
    
    return(theta_df)
           

def STATION(station=None):
    '''

    Parameters
    ----------
    station : type = str
        Input the desired alabama station triplet as a string. The default is None.

    Returns
    -------
    Print Statement 
        (Station, [list of soil types by depth]).

    '''
    I = SCAN(data=SCAN_READ)
    soils = I.soil_class().unpack().show()
    st = soils[soils['station'] == station]
    two = st['two_in_soil'].unique()[0]
    four = st['four_in_soil'].unique()[0]
    eight = st['eight_in_soil'].unique()[0]
    twenty = st['twenty_in_soil'].unique()[0]
    forty = st['forty_in_soil'].unique()[0]
    station_soil = {'SMS-2.0in_x' : two, 
                 'SMS-4.0in_x' : four, 
                 'SMS-8.0in_x' : eight, 
                 'SMS-20.0in_x': twenty, 
                 'SMS-40.0in_x': forty
        }
    return station_soil

