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
import warnings
warnings.filterwarnings('ignore')


class SCAN:
    '''
    SCAN CLASS - used to set Alabama SCAN sites with assumed soil 
    characteristics based on soil classes. 
        
    Class properties:
            
        self.df - pandas dataframe of SCAN_READ
        self.stations - pandas dataframe with all stations that have soil texture characteristics listed in Pedon Report
            
    Class methods:
        
        Contructor:
            __init__(...) - a default constructor
        
        Dataframe mutators: 
            standard_deviation_by_month(...) - a method to calculate standard deviations for each month
            mean_soil_moisutre_by_month(...) - a method to calculate the mean soil moisture by month
            z_score(...) - a method to calculate distance from mean for each data point
            quality_z_score(...) - a method to get the quality of each data point based on z_score stat
            clean_data(...) - a method to clean bad data based on the quality of the z_score
            
        Dataframe getters: 
            
            show(...) - a method to print the data assigned to the constructor when called. 
        
            
    Example Codes: 
        
        Return clean data:
        
            I = SCAN(data=SCAN_READ)
            
            df = I.standard_deviation_by_month().mean_soil_moisture_by_month.z_score()
            .quality_z_score(std=3.5).clean_data().show()
            
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
        self.stdev = pd.DataFrame()
        self.mean = pd.DataFrame()
        self.merged = pd.DataFrame()
        self.z_score_df = pd.DataFrame()
        self.quality = pd.DataFrame() 
        self.clean = pd.DataFrame()
    
    def get_month_from_dates(self):
        df = self.stations
        df['Date'] = pd.to_datetime(df['Date'])
        
        month_list = []
        for i in df['Date']:
            month = i.month
            month_list.append(month)
            
        df['Month'] = month_list
        
        self.stations = df
    
    def standard_deviation_by_month(self):
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
        print('\n')
        for i in df['station'].unique():
            print('Calculating Monthly Standard Deviation for', i)
            new_df = df[df['station'] == i]
            new_df.set_index('Date', inplace=True)
            new_df.index = pd.to_datetime(new_df.index)
            new_df.sort_index(inplace=True)
            std = new_df.groupby(new_df.index.month).std()
            std['station'] = i
            std.reset_index(inplace=True)
            std.rename(columns={'Date':'Month'}, inplace=True)
            std.rename(columns={'SMS-2.0in':'SMS-2.0in_stdev', 'SMS-4.0in':'SMS-4.0in_stdev', 'SMS-8.0in':'SMS-8.0in_stdev', 
                                'SMS-20.0in':'SMS-20.0in_stdev','SMS-40.0in':'SMS-40.0in_stdev'}, inplace=True)
            store[i] = std
        print('\n')
        print('Done!')
        df = pd.concat(store, axis=0)
        df.index = df.index.get_level_values(1)
        
        self.stdev = df
        
    
    def mean_soil_moisture_by_month(self):
       
        '''
        Purpose:
            Calculates the mean soil moisture by Month for Each USDA SCAN station
            and appends it to the primary dataframe stored in self. 

        Returns
        -------
        self.stations property
            This is an updated dataframe with monthly soil moisture values appended
            to each reading. 

        '''
        
        
        store = {}
        df = self.stations
        print('\n')
        for i in df['station'].unique():
            print('Calculating Monthly Mean for', i)
            #get the station dataframe for the unique item
            new_df = df[df['station'] == i]
            
            #set the index to Date so that it can be sorted
            new_df.set_index('Date', inplace=True)
            new_df.index = pd.to_datetime(new_df.index)
            new_df.sort_index(inplace=True)
            
            #create a month column
            new_df['Month'] = new_df.index.month
            
            #create a seperate soil moisture frame to calculate means on
            soil_moisture_frame = new_df[['station','SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in',
                   'SMS-40.0in']]
            
            #mean frame
            mean_frame = soil_moisture_frame.groupby(soil_moisture_frame.index.month).mean()
            
            #set the station column
            mean_frame['station'] = i
            
            #reset the index
            mean_frame.reset_index(inplace=True)
            
            #merge the mean frame back into the new_df
            mean_frame.rename(columns={'Date':'Month'}, inplace=True)
            mean_frame.rename(columns={'SMS-2.0in':'SMS-2.0in_month_mean', 
                                    'SMS-4.0in':'SMS-4.0in_month_mean', 'SMS-8.0in':'SMS-8.0in_month_mean',
                                    'SMS-20.0in':'SMS-20.0in_month_mean', 'SMS-40.0in':'SMS-40.0in_month_mean'}, inplace=True)
          
            #store the dataframe
            store[i] = mean_frame
        
        #concat all the stored frames
        print('\n')
        print('Done!')
        df = pd.concat(store, axis=0)
        df.index = df.index.get_level_values(1)
        df.reset_index(inplace=True)
        df.drop('index', axis=1, inplace=True)
        self.mean = df
        
        
    def merge_station_stdev_mean(self):
        std = self.stdev
        mean = self.mean
        df = self.stations
        
        stats_merge = pd.merge(std, mean, how='left')
        df_merge = pd.merge(df, stats_merge, how='left')
        self.merged = df_merge
        
    def z_score(self): 
        '''
        Purpose: 
            Calculates Z-score for each point in the raw data. 
        
        equation:
            (SMS daily data point - SMS Mean for Month) / SMS Standard Deviation for Month

        Returns
        -------
        store : dictionary.
            Stations with soil moisture and z-score information. 
            
        '''
        merged = self.merged
        store = {}
        print('\n')
        for i in merged['station'].unique():
            print('Calculating z-scores for', i)    
            new_df = merged[merged['station'] == i]
            new_df.set_index('Date', inplace=True)
            new_df.index = pd.to_datetime(new_df.index)
            new_df.sort_index(inplace=True)
           
            #create z-score column. 
            new_df['z_2'] = (new_df['SMS-2.0in'] - new_df['SMS-2.0in_month_mean']) / new_df['SMS-2.0in_stdev']
            new_df['z_4'] = (new_df['SMS-4.0in'] - new_df['SMS-4.0in_month_mean']) / new_df['SMS-4.0in_stdev']
            new_df['z_8'] = (new_df['SMS-8.0in'] - new_df['SMS-8.0in_month_mean']) / new_df['SMS-8.0in_stdev']
            new_df['z_20'] = (new_df['SMS-20.0in'] - new_df['SMS-20.0in_month_mean']) / new_df['SMS-20.0in_stdev']
            new_df['z_40'] = (new_df['SMS-40.0in'] - new_df['SMS-40.0in_month_mean']) / new_df['SMS-40.0in_stdev']
            
            new_df = new_df[['station','SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in', 'SMS-40.0in', 'SMS-2.0in_month_mean',
                              'SMS-4.0in_month_mean', 'SMS-8.0in_month_mean', 'SMS-20.0in_month_mean', 'SMS-40.0in_month_mean', 
                              'SMS-2.0in_stdev', 'SMS-4.0in_stdev', 'SMS-8.0in_stdev', 'SMS-20.0in_stdev',
                              'SMS-40.0in_stdev', 'z_2', 'z_4', 'z_8', 'z_20', 'z_40']]
            
            new_df.reset_index()
            
            #store new df with z score. 
            store[i] = new_df
        print('\n')
        print('Done!')
        df = pd.concat(store, axis=0)
        df.index = df.index.get_level_values(1)
        
        self.z_score_df = df
        
    
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
        print('\n')
        print('Creating quality columns for', std, 'standard deviations now!')
        df = self.z_score_df
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
        
        
        self.quality = df
        print('\n')
        print('Done!')
        
    def clean_data(self):
        print('\n')
        print('Cleaning data now!')
        print('\n')
        
        df = self.quality
        #print lengths 
        two_high = len(df.loc[df['2in_quality'] == 'Too High', 'SMS-2.0in'])
        two_low = len(df.loc[df['2in_quality'] == 'Too Low', 'SMS-2.0in'])
        
        #four 
        four_high = len(df.loc[df['4in_quality'] == 'Too High', 'SMS-4.0in'])
        four_low = len(df.loc[df['4in_quality'] == 'Too Low', 'SMS-4.0in']) 
        
        #eight
        eight_high = len(df.loc[df['8in_quality'] == 'Too High', 'SMS-8.0in']) 
        eight_low = len(df.loc[df['8in_quality'] == 'Too Low', 'SMS-8.0in'])
        
        #twenty 
        twenty_high = len(df.loc[df['20in_quality'] == 'Too High', 'SMS-20.0in'])
        twenty_low = len(df.loc[df['20in_quality'] == 'Too Low', 'SMS-20.0in'])
        
        #forty
        forty_high = len(df.loc[df['40in_quality'] == 'Too High', 'SMS-40.0in'])
        forty_low = len(df.loc[df['40in_quality'] == 'Too Low', 'SMS-40.0in'])
        
        data_scrubbed = {'two-in-cleaned': [two_high, two_low], 
                         'four-in-cleaned': [four_high, four_low],
                         'eight-in-cleaned': [eight_high, eight_low], 
                         'twenty-in-cleaned': [twenty_high, twenty_low],
                         'forty-in-cleaned':[forty_high, forty_low]}
        
        data_scrubbed_df = pd.DataFrame(data_scrubbed)
        transpose = data_scrubbed_df.transpose()
        transpose.columns=['Too High', 'Too Low']
        
        print('\n')
        print('The data cleaned as outliers are the following:')
        print('\n')
        print(transpose)
        
        #two
        df.loc[df['2in_quality'] == 'Too High', 'SMS-2.0in'] = np.nan
        df.loc[df['2in_quality'] == 'Too Low', 'SMS-2.0in'] = np.nan
        #four
        df.loc[df['4in_quality'] == 'Too High', 'SMS-4.0in'] = np.nan
        df.loc[df['4in_quality'] == 'Too Low', 'SMS-4.0in'] = np.nan
        #eight
        df.loc[df['8in_quality'] == 'Too High', 'SMS-8.0in'] = np.nan
        df.loc[df['8in_quality'] == 'Too Low', 'SMS-8.0in'] = np.nan
        #twenty
        df.loc[df['20in_quality'] == 'Too High', 'SMS-20.0in'] = np.nan
        df.loc[df['20in_quality'] == 'Too Low', 'SMS-20.0in'] = np.nan
        #forty
        df.loc[df['40in_quality'] == 'Too High', 'SMS-40.0in'] = np.nan
        df.loc[df['40in_quality'] == 'Too Low', 'SMS-40.0in'] = np.nan
        
        #replace 0 values
        df = df.replace(0.0, np.nan)
        
        print('\n')
        #get rid of all values above 100%
        two_in_one_hundred_values = len(df[df['SMS-2.0in']>100])
        four_in_one_hundred_values = len(df[df['SMS-4.0in']>100])
        eight_in_one_hundred_values = len(df[df['SMS-8.0in']>100])
        twenty_in_one_hundred_values = len(df[df['SMS-20.0in']>100])
        forty_in_one_hundred_values = len(df[df['SMS-40.0in']>100])
        
        print(f'Total 2in values > 100% volumetric soil moisture cleaned: {two_in_one_hundred_values}')
        print(f'Total 4in values > 100% volumetric soil moisture cleaned: {four_in_one_hundred_values}')
        print(f'Total 8in values > 100% volumetric soil moisture cleaned: {eight_in_one_hundred_values}')
        print(f'Total 20in values > 100% volumetric soil moisture cleaned: {twenty_in_one_hundred_values}')
        print(f'Total 40in values > 100% volumetric soil moisture cleaned: {forty_in_one_hundred_values}')
        
        df.loc[df['SMS-2.0in']>100, 'SMS-2.0in'] = np.nan
        df.loc[df['SMS-4.0in']>100, 'SMS-4.0in'] = np.nan
        df.loc[df['SMS-8.0in']>100, 'SMS-8.0in'] = np.nan
        df.loc[df['SMS-20.0in']>100, 'SMS-20.0in'] = np.nan
        df.loc[df['SMS-40.0in']>100, 'SMS-40.0in'] = np.nan
        
        self.clean = df
        
    ## class getters 
    def get_stdev_df(self):
        return self.stdev
    
    def get_mean_df(self):
        return self.mean
    
    def get_z_score_df(self):
        return self.z_score
    
    def get_quality_df(self):
        return self.quality
    
    def get_clean_data(self):
        return self.clean
        
     
