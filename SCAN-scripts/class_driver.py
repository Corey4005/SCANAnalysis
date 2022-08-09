#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 13:33:51 2022

@author: cwalker
"""
from class_soils import soils
from datasets import GOES_READ
import pandas as pd
class Driver(soils):
    
    GOES_READ.rename(columns={'StationTriplet':'station'}, inplace=True)
    
    def __init__(self, data):
        
        soils.__init__(self, data)
        self.merge1wALEXI = pd.DataFrame()
        self.merge2wALEXI = pd.DataFrame()
        self.merge3wALEXI = pd.DataFrame()
        self.merge4wALEXI = pd.DataFrame()
        self.one_w_corr = pd.DataFrame()
        self.two_w_corr = pd.DataFrame()
        self.three_w_corr = pd.DataFrame()
        self.four_w_corr = pd.DataFrame()
        self.concatinated_corr_df = pd.DataFrame()
        
    def merge_1w_soil_resample_with_ALEXI(self):
        df = self.one_w_soil_df 
        df.reset_index(inplace=True)
        merge = pd.merge(df, GOES_READ)
        self.merge1wALEXI = merge
        
    def merge_2w_soil_resample_with_ALEXI(self):
        df = self.two_w_soil_df 
        df.reset_index(inplace=True)
        merge = pd.merge(df, GOES_READ)
        self.merge2wALEXI = merge
        
    def merge_3w_soil_resample_with_ALEXI(self):
        df = self.three_w_soil_df 
        df.reset_index(inplace=True)
        merge = pd.merge(df, GOES_READ)
        self.merge3wALEXI = merge
        
    def merge_4w_soil_resample_with_ALEXI(self):
        df = self.four_w_soil_df
        df.reset_index(inplace=True)
        merge = pd.merge(df, GOES_READ)
        self.merge4wALEXI = merge
    
    def corr_1w_resample_ESI_by_soils(self):
        df = self.merge1wALEXI
        corr_list = []
        soil_type = []
        depth = []
        station = []
        resample_type = []
        
        for i in df['Two Soil Reclassified'].unique():
            new_df = df[df['Two Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-2.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('2.0in')
                resample_type.append('1w')
            
        for i in df['Four Soil Reclassified'].unique():
            new_df = df[df['Four Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-4.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('4.0in')
                resample_type.append('1w')
                
        for i in df['Eight Soil Reclassified'].unique():
            new_df = df[df['Eight Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-8.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('8.0in')
                resample_type.append('1w')
        
        for i in df['Twenty Soil Reclassified'].unique():
            new_df = df[df['Twenty Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-20.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('20.0in')
                resample_type.append('1w')
                
        for i in df['Forty Soil Reclassified'].unique():
            new_df = df[df['Forty Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-40.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('40.0in')
                resample_type.append('1w')
                
        self.one_w_corr['station'] = station
        self.one_w_corr['correlation'] = corr_list
        self.one_w_corr['soil type'] = soil_type
        self.one_w_corr['depth'] = depth
        self.one_w_corr['resample type'] = resample_type

    def corr_2w_resample_ESI_by_soils(self):
        df = self.merge2wALEXI
        corr_list = []
        soil_type = []
        depth = []
        station = []
        resample_type = []
        
        for i in df['Two Soil Reclassified'].unique():
            new_df = df[df['Two Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-2.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('2.0in')
                resample_type.append('2w')
            
        for i in df['Four Soil Reclassified'].unique():
            new_df = df[df['Four Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-4.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('4.0in')
                resample_type.append('2w')
                
        for i in df['Eight Soil Reclassified'].unique():
            new_df = df[df['Eight Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-8.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('8.0in')
                resample_type.append('2w')
        
        for i in df['Twenty Soil Reclassified'].unique():
            new_df = df[df['Twenty Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-20.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('20.0in')
                resample_type.append('2w')
        
        for i in df['Forty Soil Reclassified'].unique():
            new_df = df[df['Forty Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-40.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('40.0in')
                resample_type.append('2w')
                
        self.two_w_corr['station'] = station
        self.two_w_corr['correlation'] = corr_list
        self.two_w_corr['soil type'] = soil_type
        self.two_w_corr['depth'] = depth
        self.two_w_corr['resample type'] = resample_type
        
    def corr_3w_resample_ESI_by_soils(self):
        df = self.merge3wALEXI
        corr_list = []
        soil_type = []
        depth = []
        station = []
        resample_type = []
        
        for i in df['Two Soil Reclassified'].unique():
            new_df = df[df['Two Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-2.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('2.0in')
                resample_type.append('3w')
                
        for i in df['Four Soil Reclassified'].unique():
            new_df = df[df['Four Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-4.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('4.0in')
                resample_type.append('3w')
                
        for i in df['Eight Soil Reclassified'].unique():
            new_df = df[df['Eight Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-8.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('8.0in')
                resample_type.append('3w')
                
        for i in df['Twenty Soil Reclassified'].unique():
            new_df = df[df['Twenty Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-20.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('20.0in')
                resample_type.append('3w')
                
        for i in df['Forty Soil Reclassified'].unique():
            new_df = df[df['Forty Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-40.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('40.0in')
                resample_type.append('3w')
                
        self.three_w_corr['station'] = station
        self.three_w_corr['correlation'] = corr_list
        self.three_w_corr['soil type'] = soil_type
        self.three_w_corr['depth'] = depth
        self.three_w_corr['resample type'] = resample_type
        
    def corr_4w_resample_ESI_by_soils(self):
        df = self.merge4wALEXI
        corr_list = []
        soil_type = []
        depth = []
        station = []
        resample_type = []
        
        for i in df['Two Soil Reclassified'].unique():
            new_df = df[df['Two Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-2.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('2.0in')
                resample_type.append('4w')
                
        for i in df['Four Soil Reclassified'].unique():
            new_df = df[df['Four Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-4.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('4.0in')
                resample_type.append('4w')
                
        for i in df['Eight Soil Reclassified'].unique():
            new_df = df[df['Eight Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-8.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('8.0in')
                resample_type.append('4w')
                
        for i in df['Twenty Soil Reclassified'].unique():
            new_df = df[df['Twenty Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-20.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('20.0in')
                resample_type.append('4w')
                
        for i in df['Forty Soil Reclassified'].unique():
            new_df = df[df['Forty Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                corr = station_df.corr()['ESI']['SMS-40.0in']
                corr_list.append(corr)
                station.append(j)
                soil_type.append(i)
                depth.append('40.0in')
                resample_type.append('4w')
                
        self.four_w_corr['station'] = station
        self.four_w_corr['correlation'] = corr_list
        self.four_w_corr['soil type'] = soil_type
        self.four_w_corr['depth'] = depth
        self.four_w_corr['resample type'] = resample_type
    
    def concatinate_corr_dataframes(self):
        df = self.one_w_corr
        df2 = self.two_w_corr
        df3 = self.three_w_corr
        df4 = self.four_w_corr
        df2 = pd.concat([df, df2, df3, df4], join='inner')
        self.concatinated_corr_df = df2