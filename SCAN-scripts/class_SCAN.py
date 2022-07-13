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
    
TASK LIST
fix get_soils() to be based on resample class
    
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
            soil_class(...) - a method to return the soil classes dictionaries for station column
            unpack(...) - a method to unpack the soil class column dictionaries into single columns for each depth
        
        Dataframe getters: 
            
            show(...) - a method to print the data assigned to the constructor when called. 
        
    Non-class functions:
        
            theta_df(...) - function to return a comparison table of climatology theta values compared to Parish et al. 
            get_station_soil - function to return soil properties for each depth at a station triplet of interest. 
            
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
        for i in df['station'].unique():
            #get the station dataframe for the unique item
            new_df = df[df['station'] == i]
            
            #set the index to Date so that it can be sorted
            new_df.set_index('Date', inplace=True)
            new_df.index = pd.to_datetime(new_df.index)
            new_df.sort_index(inplace=True)
            
            #create a month column
            new_df['Month'] = new_df.index.month
            
            #create a seperate soil moisture frame to calculate means on
            soil_moisture_frame = new_df[['station','SMS-2.0in_x', 'SMS-4.0in_x', 
                              'SMS-8.0in_x', 'SMS-20.0in_x','SMS-40.0in_x']]
            
            #mean frame
            mean_frame = soil_moisture_frame.groupby(soil_moisture_frame.index.month).mean()
            
            #reset the index
            mean_frame.reset_index(inplace=True)
            
            #merge the mean frame back into the new_df
            mean_frame.rename(columns={'Date':'Month'}, inplace=True)
            merged = new_df.merge(mean_frame, on='Month')
            
            #set the index to new_df
            merged.index = new_df.index
            
            
            merged.rename(columns={'SMS-2.0in_x_x':'SMS-2.0in', 'SMS-4.0in_x_x':'SMS-4.0in',
                                    'SMS-8.0in_x_x':'SMS-8.0in', 'SMS-20.0in_x_x':'SMS-20.0in',
                                    'SMS-40.0in_x_x':'SMS-40.0in', 'SMS-2.0in_y':'SMS-2.0in_std', 
                                    'SMS-4.0in_y':'SMS-4.0in_std', 'SMS-8.0in_y':'SMS-8.0in_std',
                                    'SMS-20.0in_y':'SMS-20.0in_std', 'SMS-40.0in_y':'SMS-40.0in_std', 
                                    'SMS-2.0in_x_y':'SMS-2.0in_month','SMS-4.0in_x_y':'SMS-4.0in_month', 
                                    'SMS-8.0in_x_y':'SMS-8.0in_month', 'SMS-20.0in_x_y':'SMS-20.0in_month', 
                                    'SMS-40.0in_x_y':'SMS-40.0in_month'}, 
                          inplace=True)
            
            #store the dataframe
            store[i] = merged
        
        #concat all the stored frames
        df = pd.concat(store, axis=0)
        df.index = df.index.get_level_values(1)
        df.reset_index(inplace=True)
        
        self.stations = df
        
        
        
    
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
        store = {}
        for i in self.stations['station'].unique():
            new_df = self.stations[self.stations['station'] == i]
            new_df.set_index('Date', inplace=True)
            new_df.index = pd.to_datetime(new_df.index)
            new_df.sort_index(inplace=True)
           
            #create z-score column. 
            new_df['z_2'] = (new_df['SMS-2.0in'] - new_df['SMS-2.0in_month']) / new_df['SMS-2.0in_std']
            new_df['z_4'] = (new_df['SMS-4.0in'] - new_df['SMS-4.0in_month']) / new_df['SMS-4.0in_std']
            new_df['z_8'] = (new_df['SMS-8.0in'] - new_df['SMS-8.0in_month']) / new_df['SMS-8.0in_std']
            new_df['z_20'] = (new_df['SMS-20.0in'] - new_df['SMS-20.0in_month']) / new_df['SMS-20.0in_std']
            new_df['z_40'] = (new_df['SMS-40.0in'] - new_df['SMS-40.0in_month']) / new_df['SMS-40.0in_std']
            
            new_df = new_df[['station','SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in', 'SMS-40.0in', 'SMS-2.0in_month',
                              'SMS-4.0in_month', 'SMS-8.0in_month', 'SMS-20.0in_month', 'SMS-40.0in_month', 
                              'SMS-2.0in_std', 'SMS-4.0in_std', 'SMS-8.0in_std', 'SMS-20.0in_std',
                              'SMS-40.0in_std', 'z_2', 'z_4', 'z_8', 'z_20', 'z_40']]
            
            new_df.reset_index()
            
            #store new df with z score. 
            store[i] = new_df
    
        df = pd.concat(store, axis=0)
        df.index = df.index.get_level_values(1)
        
        self.stations = df
        
    
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
        
    def clean_data(self):
        df = self.stations
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
        print('The data cleaned as outliers are in the following dataframe:')
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
        
        self.stations = df
        
    
        
    def show(self):
         '''
         Purpose: 
             return the self.stations property in its current form. 
             
         returns: 
             printed dataframe
         '''
         return self.stations
     
