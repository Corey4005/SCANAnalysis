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
    
    Class functions: 
        
        __init__ - create new_df attribute used in functions set on 
            SCAN_READ variable (raw import) in assumptions.py. 
        
        soil_class - append the soil dictionary for each station that has an
            available pedon report in Alabama.
        
        unpack - Unpack the self.stations dataframe containing the soil texture
            class dictionaries and return pandas column with the soil
            texture class for each depth. 
        
        Calculate_ESM - returns the effective saturation using assumed van-genuchten soil 
            parameters from Carsel and Parrish look-up tables and soil data
            from USDA SCAN / Web Soil Survey. 
        
        show -  return the self.stations property in its current form. 
        
    Class properties:
            
        self.df - pandas dataframe of SCAN_READ
            
        self.new_df - pandas dataframe with correct soil depths, station, 
            and dates.
                
        self.stations - pandas dataframe with all stations that have soil
            texture characteristics listed in Pedon Report
    
    Example Codes: 
        
        Calculate Effective Saturation from Raw Data: 
            
            I = SCAN(data=SCAN_READ)
            dictionary = I.standard_deviation().z_score().Calculate_ESM()
            
            returns: 
                Dictionary
                Contains effective saturation calculations for each station that 
                can be called from the dictionary object using the .get([string])
                method.
                
                example:
                    #get station 2053 information
                    
                    st2053 = dictionary.get('2053:AL:SCAN').plot()
        
        Return clean effective saturation data:
        
            I = SCAN(data=SCAN_READ)
            dictionary = I.standard_deviation().z_score().quality_z_score(std=3.5).clean_data().Calculate_ESM()
            
            returns: 
                Dictionary
                Contains cleaned effective saturation values at each station with data
                up to +/- 3.5 standard deviations from the mean. Each station can be 
                called with the .get([string]) method.
                
                example: 
                    #get station 2057 information
                    
                    st2057 = dictionary.get('2057:AL:SCAN').plot()
        
        Plot tree cover versus ALESI ESI correlations with soil moisture:
            
            I = SCAN(data=SCAN_READ)
            dictionary = I.standard_deviation().z_score().quality_z_score(std=3.5).clean_data().Calculate_ESM()
            
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
            
            new_df = new_df[['station','SMS-2.0in_x', 'SMS-4.0in_x', 'SMS-8.0in_x', 
                             'SMS-20.0in_x', 'SMS-40.0in_x', 'SMS-2.0in_y','SMS-4.0in_y', 
                             'SMS-8.0in_y', 'SMS-20.0in_y', 'SMS-40.0in_y', 
                             'z_2', 'z_4', 'z_8', 'z_20', 'z_40']]
            
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
        
        print('\n')
        #get rid of all values above 100%
        one_hundred_values = len(df[df['SMS-4.0in_x']>100])
        
        print(f'Total values > 100% volumetric soil moisture cleaned: {one_hundred_values}')
        
        df.loc[df['SMS-4.0in_x']>100, 'SMS-4.0in_x'] = np.nan
        
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
        
    def Calculate_ESM(self):
        '''
        Purpose: 
            
            returns the effective saturation using assumed van-genuchten soil 
            parameters from Carsel and Parrish look-up tables and soil data
            from USDA SCAN / Web Soil Survey. 

        Returns
        -------
        store : Dictionary
            Contains a dictionary of key-value pairs. Keys are StationTriplets
            for USDA SCAN sites and values are pandas dataframes of effective
            soil moisture values at various depths calculated with provided 
            assumptions. 

        '''
        store = {}
        for i in self.stations['station'].unique():
            new_df = self.stations[self.stations['station'] == i]
            new_df.index = pd.to_datetime(new_df.index)
            new_df.sort_index(inplace=True)
            
            
            if i == '2057:AL:SCAN':
            #two in - SICL
                ES_2in = ((new_df['SMS-2.0in_x'] / 100)- 0.045) / (0.475 - 0.045)
                new_df['ES_2in'] = ES_2in
                
            #four in - SICL
                ES_4in = ((new_df['SMS-4.0in_x'] / 100)- 0.045) / (0.46 - 0.045)
                new_df['ES_4in'] = ES_4in
            
            #eight in - SICL
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)- 0.045) / (0.46 - 0.045)
                new_df['ES_8in'] = ES_8in
            #twenty in - SICL
                ES_20in = ((new_df['SMS-20.0in_x'] / 100)- 0.045) / (0.47 - 0.045)
                new_df['ES_20in'] = ES_20in
            #forty in - SICL
                ES_40in = ((new_df['SMS-40.0in_x'] / 100)- 0.045) / (0.55 - 0.045)
                new_df['ES_40in'] = ES_40in
                
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
            #store it 
                store[i] = new_df
                
            elif i =='2113:AL:SCAN':
            #two - FSL
                ES_2in = ((new_df['SMS-2.0in_x'] / 100)- 0.0295) / (0.40 - 0.0295)
                new_df['ES_2in'] = ES_2in
                
                
            #four - FSL 
                ES_4in = ((new_df['SMS-4.0in_x'] / 100)- 0.035) / (0.405 - 0.035)
                new_df['ES_4in'] = ES_4in
                
            #eight - FSL
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)- 0.035) / (0.34 - 0.035)
                new_df['ES_8in'] = ES_8in
                
            #twenty - L
                ES_20in = ((new_df['SMS-20.0in_x'] / 100)- 0.065) / (0.435 - 0.065)
                new_df['ES_20in'] = ES_20in
            
            #forty - L
                ES_40in = ((new_df['SMS-40.0in_x'] / 100)- 0.065) / (0.45 - 0.065)
                new_df['ES_40in'] = ES_40in
                
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                
            #store it 
                store[i] = new_df
            
            elif i =='2055:AL:SCAN':
            #two - GRSIL
                ES_2in = ((new_df['SMS-2.0in_x'] / 100)- 0.033) / (0.44 - 0.033)
                new_df['ES_2in'] = ES_2in
            
            # #four - GRSIL
                ES_4in = ((new_df['SMS-4.0in_x'] / 100)- 0.030) / (0.41 - 0.030)
                new_df['ES_4in'] = ES_4in
                
                
            # #eight - GRSIL
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)- 0.033) / (0.45 - 0.033)
                new_df['ES_8in'] = ES_4in
                
        
            # #twenty - SICL
                ES_20in = ((new_df['SMS-20.0in_x'] / 100)- 0.089) / (0.49 - 0.089)
                new_df['ES_20in'] = ES_20in
                
            # #forty - SICL
                ES_40in = ((new_df['SMS-40.0in_x'] / 100)- 0.025) / (0.555 - 0.025)
                new_df['ES_40in'] = ES_40in
                
            #create new dataframe
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                
            # #store it 
                store[i] = new_df
            
            elif i == '2180:AL:SCAN':
            #two - SL
                ES_2in = ((new_df['SMS-2.0in_x'] / 100)- 0.005) / (0.295 - 0.005)
                new_df['ES_2in'] = ES_2in
                
            #four - SL
                ES_4in = ((new_df['SMS-4.0in_x'] / 100)- 0.005) / (0.27 - 0.005)
                new_df['ES_4in'] = ES_4in
                
            #eight - SL
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)- 0.005) / (0.26 - 0.005)
                new_df['ES_8in'] = ES_8in
                
            
            #twenty - SL
                ES_20in = ((new_df['SMS-20.0in_x'] / 100)- 0.005) / (0.27 - 0.005)
                new_df['ES_20in'] = ES_20in
                
            
            #forty - SCL
                ES_40in = ((new_df['SMS-40.0in_x'] / 100)- 0.100) / (0.33 - 0.100)
                new_df['ES_40in'] = ES_40in
                
            #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                
            # #store it 
                store[i] = new_df
            
            elif i == '2114:AL:SCAN':
            # two - SIL
                ES_2in = ((new_df['SMS-2.0in_x'] / 100)- 0.025) / (0.4 - 0.025)
                new_df['ES_2in'] = ES_2in
            
            # four - SIC
                ES_4in = ((new_df['SMS-4.0in_x'] / 100)- 0.070) / (0.41 - 0.070)
                new_df['ES_4in'] = ES_4in
            
            #eight - C
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)- 0.068) / (0.41 - 0.068)
                new_df['ES_8in'] = ES_8in
            
            #twenty - C 
                ES_20in = ((new_df['SMS-20.0in_x'] / 100)- 0.068) / (0.41 - 0.068)
                new_df['ES_20in'] = ES_20in
                
            #forty - C
                ES_40in = ((new_df['SMS-40.0in_x'] / 100)- 0.068) / (0.475 - 0.068)
                new_df['ES_40in'] = ES_40in
                
            #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                
            # #store it 
                store[i] = new_df
            
            elif i == '2056:AL:SCAN':
            #two - L
                ES_2in = ((new_df['SMS-2.0in_x'] / 100)- 0.078) / (0.48 - 0.078)
                new_df['ES_2in'] = ES_2in
                
            #four - L
                ES_4in = ((new_df['SMS-4.0in_x'] / 100)- 0.078) / (0.49 - 0.078)
                new_df['ES_4in'] = ES_4in
                
            #eight - CL
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)- 0.095) / (0.50 - 0.095)
                new_df['ES_8in'] = ES_8in
            
            #twenty - C
                ES_20in = ((new_df['SMS-20.0in_x'] / 100)- 0.068) / (0.41 - 0.068)
                new_df['ES_20in'] = ES_20in
            
            #forty - C 
                ES_40in = ((new_df['SMS-40.0in_x'] / 100)- 0.068) / (0.53 - 0.068)
                new_df['ES_40in'] = ES_40in
            
            #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                
            # #store it 
                store[i] = new_df
            
            elif i == '2115:AL:SCAN':
                #two - LS
                ES_2in = ((new_df['SMS-2.0in_x'] / 100)- 0.001) / (0.31 - 0.001)
                new_df['ES_2in'] = ES_2in
                
                #four - LS
                ES_4in = ((new_df['SMS-4.0in_x'] / 100)- 0.057) / (0.41 - 0.057)
                new_df['ES_4in'] = ES_4in
                
                #eight - SL
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)- 0.001) / (0.31 - 0.001)
                new_df['ES_8in'] = ES_8in
                
                #twenty - SCL
                ES_20in = ((new_df['SMS-20.0in_x'] / 100) - 0.100) / (0.40 - 0.100)
                new_df['ES_20in'] = ES_20in
                
                #forty - CL
                ES_40in = ((new_df['SMS-40.0in_x'] / 100)- 0.001) / (0.43 - 0.001)
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
            
                # #store it 
                store[i] = new_df
                 
            elif i == '2053:AL:SCAN':
                #two - SICL
                ES_2in = ((new_df['SMS-2.0in_x'] / 100)- 0.035) / (0.41 - 0.035)
                new_df['ES_2in'] = ES_2in
                
                #four - SIL
                ES_4in = ((new_df['SMS-4.0in_x'] /  100)- 0.070) / (0.40 - 0.070)
                new_df['ES_4in'] = ES_4in
                
                #eight - SIL
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)- 0.070) / (0.41 - 0.070)
                new_df['ES_8in'] = ES_8in
                
                #twenty - SICL
                ES_20in = ((new_df['SMS-20.0in_x'] / 100)- 0.050) / (0.59 - 0.050)
                new_df['ES_20in'] = ES_20in
                
                #forty - CL
                ES_40in = ((new_df['SMS-40.0in_x'] / 100)- 0.02) / (0.41 - 0.02)
                new_df['ES_40in'] = ES_40in
            
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                
                # #store it 
                store[i] = new_df
                
            elif i == '2078:AL:SCAN':
                #two - SICL
                ES_2in = ((new_df['SMS-2.0in_x'] / 100)- 0.079) / (0.46 - 0.079)
                new_df['ES_2in'] = ES_2in
                
                #four - SIL
                ES_4in = ((new_df['SMS-4.0in_x'] /  100)- 0.070) / (0.46 - 0.070)
                new_df['ES_4in'] = ES_4in
                
                #eight - SICL
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)- 0.089) / (0.63 - 0.089)
                new_df['ES_8in'] = ES_8in
               
                #twenty - SCIL 
                ES_20in = ((new_df['SMS-20.0in_x'] / 100)- 0.089) / (0.47 - 0.089)
                new_df['ES_20in'] = ES_20in
                
                #forty - CL
                ES_40in = ((new_df['SMS-40.0in_x'] / 100)- 0.095) / (0.58 - 0.095)
                new_df['ES_40in'] = ES_40in
            
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                
                # #store it 
                store[i] = new_df
                
                
            elif i == '2177:AL:SCAN':
                #two - SIC
                ES_2in = ((new_df['SMS-2.0in_x'] / 100)- 0.035) / (0.69 - 0.035)
                new_df['ES_2in'] = ES_2in
                
                #four - SIC
                ES_4in = ((new_df['SMS-4.0in_x'] / 100)- 0.070) / (0.66 - 0.070)
                new_df['ES_4in'] = ES_4in
               
                #eight - SIC
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)- 0.070) / (0.69 - 0.070)
                new_df['ES_8in'] = ES_8in
                
                #twenty - SIC
                ES_20in = ((new_df['SMS-20.0in_x'] / 100)- 0.070) / (0.73 - 0.070)
                new_df['ES_20in'] = ES_20in
                
                #forty - SIC
                ES_40in = ((new_df['SMS-40.0in_x'] / 100)- 0.070) / (0.71 - 0.070)
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                    
                # #store it 
                store[i] = new_df
            
            elif i == '2173:AL:SCAN':
                #two - SIL
                ES_2in = ((new_df['SMS-2.0in_x'] /  100)- 0.001) / (0.49 - 0.001)
                new_df['ES_2in'] = ES_2in
                
                #four - SIL
                ES_4in = ((new_df['SMS-4.0in_x'] /  100)- 0.001) / (0.50 - 0.001)
                new_df['ES_4in'] = ES_4in
                
                #eight - SICL
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)- 0.089) / (0.52 - 0.089)
                new_df['ES_8in'] = ES_8in
                
                #twenty - SICL
                ES_20in = ((new_df['SMS-20.0in_x'] / 100)- 0.089) / (0.59 - 0.089)
                new_df['ES_20in'] = ES_20in
                
                #forty - C 
                ES_40in = ((new_df['SMS-40.0in_x'] / 100)- 0.068) / (0.70 - 0.068)
                new_df['ES_40in'] = ES_40in
            
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                    
                # #store it 
                store[i] = new_df
                
            elif i == '2178:AL:SCAN':
                #two - FSL
                ES_2in = ((new_df['SMS-2.0in_x'] / 100)- 0.005) / (0.50 - 0.005)
                new_df['ES_2in'] = ES_2in
                
                #four - FSL
                ES_4in = ((new_df['SMS-4.0in_x'] / 100)- 0.022) / (0.48 - 0.022)
                new_df['ES_4in'] = ES_4in
                
                #eight - FSL
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)- 0.022) / (0.54 - 0.022)
                new_df['ES_8in'] = ES_8in
                
                #twenty - FSL
                ES_20in = ((new_df['SMS-20.0in_x'] / 100)- 0.022) / (0.59 - 0.022)
                new_df['ES_20in'] = ES_20in
                
                #forty - L
                ES_40in = ((new_df['SMS-40.0in_x'] / 100)- 0.078) / (0.56 - 0.078)
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                    
                # #store it 
                store[i] = new_df
                
            elif i == '2175:AL:SCAN':
                #two - L
                ES_2in = ((new_df['SMS-2.0in_x'] / 100)- 0.001) / (0.46 - 0.001)
                new_df['ES_2in'] = ES_2in
                
                #four - L
                ES_4in = ((new_df['SMS-4.0in_x'] / 100)- 0.001) / (0.42 - 0.001)
                new_df['ES_4in'] = ES_4in
                
                #eight - L
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)- 0.001) / (0.46 - 0.001)
                new_df['ES_8in'] = ES_8in
                
                #twenty - L
                ES_20in = ((new_df['SMS-20.0in_x'] / 100)- 0.001) / (0.59 - 0.001)
                new_df['ES_20in'] = ES_20in
                
                #forty - C
                ES_40in = ((new_df['SMS-40.0in_x'] / 100)- 0.068) / (0.58 - 0.068)
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                
                    
                # #store it 
                store[i] = new_df
                
            elif i == '2174:AL:SCAN':
                #two - SIC
                ES_2in = ((new_df['SMS-2.0in_x'] / 100)- 0.042) / (0.64 - 0.042)
                new_df['ES_2in'] = ES_2in
                
                #four - SIC
                ES_4in = ((new_df['SMS-4.0in_x'] / 100)- 0.042) / (0.74 - 0.042)
                new_df['ES_4in'] = ES_4in
                
                #eight - C
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)- 0.068) / (0.73 - 0.068)
                new_df['ES_8in'] = ES_8in
                
                #twenty - C
                ES_20in = ((new_df['SMS-20.0in_x'] / 100)- 0.068) / (0.70 - 0.068)
                new_df['ES_20in'] = ES_20in
                
                #forty - C
                ES_40in = ((new_df['SMS-40.0in_x'] / 100)- 0.005) / (0.71 - 0.005)
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                    
                # #store it 
                store[i] = new_df
            
            elif i == '2182:AL:SCAN':
                #two - LS
                ES_2in = ((new_df['SMS-2.0in_x'] / 100)- 0.001) / (0.44 - 0.001)
                new_df['ES_2in'] = ES_2in
                
                #four - LS
                ES_4in = ((new_df['SMS-4.0in_x'] / 100)- 0.001) / (0.33 - 0.001)
                new_df['ES_4in'] = ES_4in
                
                #eight - LS
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)- 0.001) / (0.38 - 0.001)
                new_df['ES_8in'] = ES_8in
                
                #twenty - FS
                ES_20in = ((new_df['SMS-20.0in_x'] / 100)- 0.005) / (0.40 - 0.045)
                new_df['ES_20in'] = ES_20in
                
                #forty - SL
                ES_40in = ((new_df['SMS-40.0in_x'] / 100)- 0.005) / (0.60 - 0.065)
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                    
                # #store it 
                store[i] = new_df
                
            elif i == '2179:AL:SCAN':
                #two - FSL
                ES_2in = ((new_df['SMS-2.0in_x'] / 100)- 0.065) / (0.51 - 0.065)
                new_df['ES_2in'] = ES_2in
                
                #four - FSL
                ES_4in = ((new_df['SMS-4.0in_x'] / 100)- 0.065) / (0.38 - 0.065)
                new_df['ES_4in'] = ES_4in
                
                #eight - FSL
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)- 0.065) / (0.43 - 0.065)
                new_df['ES_8in'] = ES_8in
                
                #twenty - FSL
                ES_20in = ((new_df['SMS-20.0in_x'] / 100)- 0.065) / (0.43 - 0.065)
                new_df['ES_20in'] = ES_20in
                
                #forty - BRCK
                ES_40in = np.nan
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
    
                # #store it 
                store[i] = new_df
                
            elif i == '2181:AL:SCAN':
                #two - FSL
                ES_2in = ((new_df['SMS-2.0in_x'] / 100)- 0.063) / (0.40 - 0.063)
                new_df['ES_2in'] = ES_2in
                
                #four - FSL
                ES_4in = ((new_df['SMS-4.0in_x'] / 100)- 0.065) / (0.435 - 0.065)
                new_df['ES_4in'] = ES_4in
                
                #eight - FSL
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)- 0.065) / (0.35 - 0.065)
                new_df['ES_8in'] = ES_8in
                
                #twenty - SL
                ES_20in = ((new_df['SMS-20.0in_x'] / 100) - 0.065) / (0.37 - 0.065)
                new_df['ES_20in'] = ES_20in
                
                #forty - SCL
                ES_40in = ((new_df['SMS-40.0in_x'] / 100)- 0.100) / (0.36 - 0.100)
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                    
                # #store it 
                store[i] = new_df
                
            elif i == '2176:AL:SCAN': 
                #two - FS
                ES_2in = ((new_df['SMS-2.0in_x'] / 100)-0.001) / (0.245 - 0.001)
                new_df['ES_2in'] = ES_2in
                
                #four - FS
                ES_4in = ((new_df['SMS-4.0in_x'] / 100)-0.001) / (0.27 - 0.001)
                new_df['ES_4in'] = ES_4in
                
                #eight - FS
                ES_8in = ((new_df['SMS-8.0in_x'] / 100)-0.001) / (0.22 - 0.001)
                new_df['ES_8in'] = ES_8in
                
                #twenty - S
                ES_20in = ((new_df['SMS-20.0in_x'] / 100)-0.020) / (0.22 - 0.020)
                new_df['ES_20in'] = ES_20in
                
                #forty - S
                ES_40in = ((new_df['SMS-40.0in_x'] / 100)-0.020) / (0.225 - 0.030)
                new_df['ES_40in'] = ES_40in
                
                #create new frame 
                new_df = new_df[['ES_2in', 'ES_4in', 'ES_8in', 'ES_20in', 'ES_40in']]
                    
                # #store it 
                store[i] = new_df
            
        return store
        
        
        
    def show(self):
         '''
         Purpose: 
             return the self.stations property in its current form. 
             
         returns: 
             printed dataframe
         '''
         return self.stations
     
############# NON-CLASS FUNCTIONS BELOW ###################

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
    statement = (station + ' ', 'two: {}'.format(two), 'four: {}'.format(four), 
          'eight: {}'.format(eight), 'twenty: {}'.format(twenty), 
          'forty: {}'.format(forty))
    return print(statement)

def RUN_CLASS_FUNCS(std=None):
    '''
    
    Parameters
    ---------
    std : float
        pass the number of standard deviations you would like to set as 
        'good data'. 
        
    Purpose:
        Return cleaned effective saturation values in with one function calling 
        appropriate SCAN class functions. 

    Returns
    -------
    Effective Saturation dataframe for each station in Alabama as a dictionary.

    '''
    I = SCAN(data=SCAN_READ)
    soils = I.standard_deviation().z_score().quality_z_score(std=std).clean_data().Calculate_ESM()
    
        
    return soils

def RUN_NON_CLASS_OPERATIONS(std=None):
    '''
    Parameters
    ---------
    std : float
        pass the number of standard deviations you would like to set as 
        'good data'. 
        
    Puropse
    -------
    Creates anomalies for effective saturation calculations. 
    
    Returns
    -------
    anom : Pandas dataframe
        contains anomaly calculations for soil. 

    '''
    soils = RUN_CLASS_FUNCS(std=std)
    avg = AVG(soils)
    jul = JULIAN(avg)
    anom = ANOM(jul)
    
    return anom

def AVG(df):
    '''
    

    Parameters
    ----------
    df : pandas df
        Pass the df from Calulate_ESM() in the assumptions.py script.

    Returns
    -------
    store : pandas df
        contains seven day avereages of the effective satuaration.

    '''
    store = {}
    
    for i in df:
        f = df[i]
        f.sort_index(inplace=True)
        f = f.rolling('7D', min_periods=3).mean()
        store[i] = f
        
    return store

def JULIAN(df):
    '''
    

    Parameters
    ----------
    df : Pandas Dataframe
        Pass the dataframe returned from AVG in assumptions.py.

    Returns
    -------
    store : Dictionary
        Returns a dictionary for each USDA station containing the julian day column 
        and inserted dates where they are missing. Also drops julian days that are
        day 366 for each station. 

    '''
    store = {}
    
    for i in df:
        f = df[i]
        f.asfreq('D')
        f['jday'] = f.index.strftime('%j')
        f.reset_index(inplace=True)
        MASK = f.loc[f['jday'] == '366'].index
        NEW_DF = f.drop(MASK)
        store[i] = NEW_DF
        
    return store

def ANOM(df):
    '''
    

    Parameters
    ----------
    df : Pandas Dataframe
        Pass the df returned from JULIAN() in assumptions.py.
        

    Returns
    -------
    store : Pandas Dataframe
        Dataframe containing the anomaly soil moisture values for each station
        across Alabama. 

    '''
    store = {}
    
    for i in df:
        f = df[i]
        day_mean = f.groupby(f.jday).mean()
        merge = f.merge(day_mean, on='jday', how='left', sort=False)
        merge.set_index('Date', inplace=True)
        merge.sort_index()
        merge['ANOM_2in'] = (merge['ES_2in_x'] - merge['ES_2in_y'])
        merge['ANOM_4in'] = (merge['ES_4in_x'] - merge['ES_4in_y'])
        merge['ANOM_8in'] = (merge['ES_8in_x'] - merge['ES_8in_y'])
        merge['ANOM_20in'] = (merge['ES_20in_x'] - merge['ES_20in_y'])
        merge['ANOM_40in'] = (merge['ES_40in_x'] - merge['ES_40in_y'])
        
        merge['ANOM_2in_rescale'] = merge['ANOM_2in'] / abs(merge['ANOM_2in'].max()) * 3
        merge['ANOM_4in_rescale'] = merge['ANOM_4in'] / abs(merge['ANOM_4in'].max()) * 3
        merge['ANOM_8in_rescale'] = merge['ANOM_8in'] / abs(merge['ANOM_8in'].max()) * 3
        merge['ANOM_20in_rescale'] = merge['ANOM_20in'] / abs(merge['ANOM_20in'].max()) * 3
        merge['ANOM_40in_rescale'] = merge['ANOM_40in'] / abs(merge['ANOM_40in'].max()) * 3
        
        merge['StationTriplet'] = i
        merge = merge[['jday', 'ANOM_2in_rescale', 'ANOM_4in_rescale', 'ANOM_8in_rescale', 
                          'ANOM_20in_rescale', 'ANOM_40in_rescale', 'StationTriplet']]
        store[i] = merge
        
    return store

def PLOT_ALL_STNS_ES(dictionary):
    '''
    

    Parameters
    ----------
    df : Pass a dictionary from either AVG, JULIAN or ANOM fucntions in assumptions.py
        
    Example
    -------
    I = SCAN(data=SCAN_READ)
    x = RUN_NON_CLASS_OPERATIONS(std=3.5)
    
    PLOT_ALL_STNS_ES(x)
    
    Returns
    -------
    Plot of all stations. 

    '''
    fig, ax = plt.subplots(9, 2, figsize=(18,35))
    ax_array = ax.ravel()
    for idx, key in enumerate(dictionary.keys()):
        plot = dictionary[key].plot(ax=ax_array[idx], ylabel='Effective Saturation', title=f'{key}')
        plot.get_legend().remove()
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.subplots_adjust(hspace=0.5, wspace=0.15)
    plt.show()

def PLOT_ALL_STNS_Z_SCORE(df):
    '''
    

    Parameters
    ----------
    df : Pass dictionary from z_score().show() functions of raw data in assumptions.py. 
        
    Example for just Raw Data without Cleaning
    ----------
    I = SCAN(data=SCAN_READ)
    x = I.standard_deviation().z_score().show()
    PLOT_ALL_STNS_Z_SCORE(x)
    
    Example for data after cleaning
    -----------
    I = SCAN(data=SCAN_READ)
    x = I.standard_deviation().z_score().quality_z_score(std=3.5).clean_data().show()
    PLOT_ALL_STNS_Z_SCORE(x)
    
    Returns
    -------
    Plot of all stations z_score. 

    '''
    fig, ax = plt.subplots(9, 2, figsize=(18,35))
    ax_array = ax.ravel()
    for idx, key in enumerate(df['station'].unique()):
        new_df = df[df['station'] == key]
        new_df = new_df[['z_2', 'z_4', 'z_8', 'z_20', 'z_40']]
        plot = new_df.plot(ax=ax_array[idx], ylabel='z-score', title=f'{key} Raw Data')
        plot.get_legend().remove()
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.subplots_adjust(hspace=0.5, wspace=0.15)
    plt.show()

        
def MERGE(dictionary):
    '''
    

    Parameters
    ----------
    dictionary : dictionary 
        Needs dictionary created by RUN_NON_CLASS_OPERATIONS() in assumptions.py

    Returns
    -------
    store : dictionary
        contains soil moisture anomaly values at each station with ESI from ALEXI

    '''
    store = {}
    for i in dictionary:
        new_df = dictionary.get(i)
        new_df.sort_index(inplace=True)
        new_df.reset_index(inplace=True)
        merge = new_df.merge(GOES_READ, on=['Date', 'StationTriplet'])
        store[i] = merge
        
    return store

def CORRELATE(dictionary, month=None):
    '''
    

    Parameters
    ----------
    dictionary : Dictionary
        Pass the dictionray returned from the MERGE function in assumptions.py
        containing ESI and Effective Saturation values at all stations. 

    Returns
    -------
    store : Dictionary
        returns a dictionary of dataframes for pairwise correlations between 
        ESI and effective saturation values by station. 

    '''
    store = {}
    for i in dictionary:
        get = dictionary[i]
        get.set_index('Date', inplace=True)
        get = get[get.index.month == month]
        corr = get.corr()['ESI'].drop(['Latitude', 'Longitude'])
        store[i] = corr
        
    return store

def CORRELATE_DF(dictionary):
    '''
    

    Parameters
    ----------
    dictionary : Dictionary
        Pass the dictionary returned from the CORRELATE function in
        assumptions.py.

    Returns
    -------
    DF: pandas dataframe
        returns a pandas dataframe containing station and correlations with 
        ESI. 

    '''
    
    store = {}
    for i in dictionary:
        DF = pd.DataFrame(dictionary.get(i))
        DF['station'] = i
        DF.drop('ESI', axis=0, inplace=True)
        store[i] = DF
    
    DF = pd.concat(store)
    DF.index = DF.index.get_level_values(1)
    DF.reset_index(inplace=True)
    
    return DF

def MERGE_CORRDF_TREE_DF(TREE_READ):
    '''
    

    Parameters
    ----------
    TREE_READ : Dataframe
    
        Tree Class Cover by ALEXI station pixel.
        
    Returns
    -------
    merged_t : Dataframe
        returns a merged dataframe of TREE_READ with ESI vs SCAN 
        correlated values across different depths. 

    '''
    #core functions 
    X = RUN_NON_CLASS_OPERATIONS(std=3.5)
    merged = MERGE(X)
    corr = CORRELATE(merged, month=10)
    corr_df = CORRELATE_DF(corr)
    
    
    func = lambda x: x[-4:] + ':' + 'AL' + ':' + 'SCAN'
    TREE_READ['station'] = TREE_READ['station'].apply(func)
    
    merged_t = pd.merge(TREE_READ, corr_df, on='station')
    
    merged_t.rename(columns={'ESI':'Alexi ESI vs SCAN Pearson Coeficient Value'}, inplace=True)
    

    return merged_t

def PLOT_TREE_CORR(df):
    '''
    

    Parameters
    ----------
    df : Dataframe
        Input the dataframe created by the MERGE_CORR_DF_TREE_DF() function in
        assumptions.py.

    Returns
    -------
    Tile plot (5 plots) of tree cover and ALEXI ESI vs SCAN Pearson Coeficient 
    Values for all index (2, 4, 8, 20, 40) (inch) depths.

    '''
    
    plot = sns.lmplot(x='Total Tree Cover', y='Alexi ESI vs SCAN Pearson Coeficient Value', col='index', data=df, palette='rocket')
    
    
    ax_array = plot.axes.ravel()
    
    lis = []
    #getting covariance and pearson r
    for idx, key in enumerate(df['index'].unique()):
        new_df = df[df['index'] == key]
        new_df.dropna(inplace=True)
        x = new_df['Total Tree Cover'].values
        y = new_df['Alexi ESI vs SCAN Pearson Coeficient Value'].values
        stats_array = pearsonr(x, y)
        lis.append(stats_array)
        print(f'{key}' + ' ' + ' R value:', stats_array[0], 'P value:', stats_array[1])


    for i, key in enumerate(ax_array):
        r = lis[i][0]
        p = lis[i][1]
        r_format = '{:.3f}'.format(r)
        p_format = '{:.3f}'.format(p)
        ax = ax_array[i]
        ax.annotate('R: {} \nP: {}'.format(r_format, p_format), xy=(5, 3), xycoords='axes points')
            
            
    return plot
    
        
def UNSTACK_N_PLOT(dictionary):
    '''
    

    Parameters
    ----------
    dictionary : Dictionary
        Pass the dictionary returned from the CORRELATE function in assumptions.py.

    Returns
    -------
    PLOT : Matplotlib plot
        Returns a barplot showing pairwise correlations between ALEXI ESI and 
        effective saturation values at each USDA SCAN site station across Alabama.

    '''
    
    
    DF = pd.concat(dictionary)
    DF = DF.unstack(level=-1)
    DF.drop('ESI', axis=1, inplace=True)
    DF['mean_corr'] = (DF['ANOM_2in_rescale'] + DF['ANOM_4in_rescale'] + 
                       DF['ANOM_8in_rescale'] + DF['ANOM_20in_rescale'] + 
                       DF['ANOM_40in_rescale']) / 5
    print('Here are the columns to sort by:', DF.columns)
    sort = input('Which column would you like to sort? Enter Here:')
    DF_sorted = DF.sort_values(sort)
    DF_sorted.reset_index(inplace=True)
    DF_sorted.drop(['Latitude', 'Longitude'], axis=1, inplace=True)
    DF_sorted['ANOM_2in_rescale'] = DF_sorted['ANOM_2in_rescale'].astype('float')
    DF_sorted['ANOM_4in_rescale'] = DF_sorted['ANOM_4in_rescale'].astype('float')
    DF_sorted['ANOM_8in_rescale'] = DF_sorted['ANOM_8in_rescale'].astype('float')
    DF_sorted['ANOM_20in_rescale'] = DF_sorted['ANOM_20in_rescale'].astype('float')
    DF_sorted['ANOM_40in_rescale'] = DF_sorted['ANOM_40in_rescale'].astype('float')
    DF_sorted['mean_corr'] = DF_sorted['mean_corr'].astype('float')

    TIDY = DF_sorted.melt(id_vars='index')
    fig, ax = plt.subplots(figsize=(30,10))
    PLOT = sns.barplot(x='index', y='value', hue='variable', data=TIDY, ax=ax)
    ax.set_xlabel('Station')
    ax.set_ylabel('R Value')
    ax.set_title('Station Volumetric Soil Moisture Pairwise Correlations with GOES')
    PLOT.set_xticklabels(PLOT.get_xticklabels(), rotation=45, horizontalalignment='right')
    return PLOT

def ALL_FUNCS_BARPLOT(std=None):
    '''
    Purpose
    -------
    Runs the following code in concert:
        
        X = RUN_NON_CLASS_OPERATIONS()
        MERGED = MERGE(X)
        CORR = CORRELATE(MERGED)
        PLOT = UNSTACK_N_PLOT(CORR)

    Returns
    -------
    PLOT : Matplotlib plot
        Returns a barplot showing pairwise correlations between ALEXI ESI and 
        effective saturation values at each USDA SCAN site station across Alabama.

    '''
    X = RUN_NON_CLASS_OPERATIONS(std=std)
    MERGED = MERGE(X)
    CORR = CORRELATE(MERGED)
    PLOT = UNSTACK_N_PLOT(CORR)
    return PLOT

def CONVERT_IN_TO_CM(soil_inches = [2, 4, 8, 20, 40]):
        """
        FUNCTION INFO: function will convert inches to centimeters. 
        
        PARAMATERS: 
            soil_inches (list) - A list of desired sensor depths in inches. 
            Default argument is [2, 4, 8, 20, 40] for most but can be 
            changed for desired depths. 
            
        OUTPUT: 
            prints a conversion to centimeters for every inch argument in 
            soil_inches parameter. 
        

        """
        for i in soil_inches: 
            print('{} inches is:'.format(i), i*2.54, 'centimeters')

def high_low(x):
    if x > 0:
        return 'high'
    else:
        return 'low'
    
def MODEL_ESI(std=None):
    #run operations to get final merged dataframe
    x = RUN_NON_CLASS_OPERATIONS(std=std)
    MERGED = MERGE(x)
    CONCAT = pd.concat(MERGED, axis=0, ignore_index=True)
    
    #create a high/low column for prediction
    CONCAT['high/low'] = CONCAT['ESI'].apply(high_low)
    
    #drop the things that dont matter in the dataframe
    CONCAT.drop(columns=['Date', 'jday', 'Longitude', 'Latitude', 'StationTriplet'], inplace=True)
    return CONCAT
