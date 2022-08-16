#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 13:33:51 2022

@author: cwalker
"""
from class_soils import soils
from datasets import GOES_READ
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
        self.stations_corr_by_month = pd.DataFrame()
        
    def merge_1w_soil_resample_with_ALEXI(self):
        df = self.one_w_soil_df 
        df.reset_index(inplace=True)
        ALEXI_1w = self.ALEXI
        ALEXI_1w.reset_index(inplace=True)
        merge = pd.merge(df, ALEXI_1w)
        self.merge1wALEXI = merge
        
    def merge_2w_soil_resample_with_ALEXI(self):
        df = self.two_w_soil_df 
        df.reset_index(inplace=True)
        ALEXI_2w = self.ALEXI_two_week_resampled
        ALEXI_2w.reset_index(inplace=True)
        merge = pd.merge(df, ALEXI_2w)
        self.merge2wALEXI = merge
        
    def merge_3w_soil_resample_with_ALEXI(self):
        df = self.three_w_soil_df 
        df.reset_index(inplace=True)
        ALEXI_3w = self.ALEXI_three_week_resampled
        ALEXI_3w.reset_index(inplace=True)
        merge = pd.merge(df, ALEXI_3w)
        self.merge3wALEXI = merge
        
    def merge_4w_soil_resample_with_ALEXI(self):
        df = self.four_w_soil_df
        df.reset_index(inplace=True)
        ALEXI_4w = self.ALEXI_four_week_resampled
        ALEXI_4w.reset_index(inplace=True)
        merge = pd.merge(df, ALEXI_4w)
        self.merge4wALEXI = merge
    
    def corr_1w_resample_ESI_by_soils(self):
        df = self.merge1wALEXI
        corr_list = []
        soil_type = []
        depth = []
        station = []
        resample_type = []
        num_observations = []
        
        for i in df['Two Soil Reclassified'].unique():
            new_df = df[df['Two Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                number_observations = station_df['SMS-2.0in'].count()
                num_observations.append(number_observations)
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
                number_observations = station_df['SMS-4.0in'].count()
                num_observations.append(number_observations)
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
                number_observations = station_df['SMS-8.0in'].count()
                num_observations.append(number_observations)
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
                number_observations = station_df['SMS-20.0in'].count()
                num_observations.append(number_observations)
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
                number_observations = station_df['SMS-40.0in'].count()
                num_observations.append(number_observations)
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
        self.one_w_corr['number observations'] = num_observations

    def corr_2w_resample_ESI_by_soils(self):
        df = self.merge2wALEXI
        corr_list = []
        soil_type = []
        depth = []
        station = []
        resample_type = []
        num_observations = []
        
        for i in df['Two Soil Reclassified'].unique():
            new_df = df[df['Two Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                number_observations = station_df['SMS-2.0in'].count()
                num_observations.append(number_observations)
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
                number_observations = station_df['SMS-4.0in'].count()
                num_observations.append(number_observations)
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
                number_observations = station_df['SMS-8.0in'].count()
                num_observations.append(number_observations)
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
                number_observations = station_df['SMS-20.0in'].count()
                num_observations.append(number_observations)
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
                number_observations = station_df['SMS-40.0in'].count()
                num_observations.append(number_observations)
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
        self.two_w_corr['number observations'] = num_observations
        
    def corr_3w_resample_ESI_by_soils(self):
        df = self.merge3wALEXI
        corr_list = []
        soil_type = []
        depth = []
        station = []
        resample_type = []
        num_observations = []
        
        for i in df['Two Soil Reclassified'].unique():
            new_df = df[df['Two Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                number_observations = station_df['SMS-2.0in'].count()
                num_observations.append(number_observations)
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
                number_observations = station_df['SMS-4.0in'].count()
                num_observations.append(number_observations)
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
                number_observations = station_df['SMS-8.0in'].count()
                num_observations.append(number_observations)
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
                number_observations = station_df['SMS-20.0in'].count()
                num_observations.append(number_observations)
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
                number_observations = station_df['SMS-40.0in'].count()
                num_observations.append(number_observations)
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
        self.three_w_corr['number observations'] = num_observations
        
    def corr_4w_resample_ESI_by_soils(self):
        df = self.merge4wALEXI
        corr_list = []
        soil_type = []
        depth = []
        station = []
        resample_type = []
        num_observations = []
        
        for i in df['Two Soil Reclassified'].unique():
            new_df = df[df['Two Soil Reclassified'] == i]
            for j in new_df['station'].unique():
                station_df = new_df[new_df['station'] == j]
                number_observations = station_df['SMS-2.0in'].count()
                num_observations.append(number_observations)
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
                number_observations = station_df['SMS-4.0in'].count()
                num_observations.append(number_observations)
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
                number_observations = station_df['SMS-8.0in'].count()
                num_observations.append(number_observations)
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
                number_observations = station_df['SMS-20.0in'].count()
                num_observations.append(number_observations)
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
                number_observations = station_df['SMS-40.0in'].count()
                num_observations.append(number_observations)
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
        self.four_w_corr['number observations'] = num_observations
    
    def concatinate_corr_dataframes(self):
        df = self.one_w_corr
        df2 = self.two_w_corr
        df3 = self.three_w_corr
        df4 = self.four_w_corr
        df2 = pd.concat([df, df2, df3, df4], join='inner')
        self.concatinated_corr_df = df2
        
    def plot_stations_corr_by_depth(self, depth=None, resample_type='1w', hue=False):
        while depth==None:
            print('Pass the depth you would like to get. For example: \n')
            print('SMS-2.0in, SMS-4.0in, SMS-8.0in, SMS-20.0in, SMS-40.0in')
            break
            
        if resample_type == '1w':
            df = self.merge1wALEXI
        
        elif resample_type == '2w':
            df = self.merge2wALEXI
        elif resample_type == '3w':
            df = self.merge3wALEXI
        elif resample_type == '4w':
            df = self.merge4wALEXI

        correlation = []
        month = []
        station = []
        num_observations = []
        soil_types = []
        soil_key = {'SMS-2.0in':'Two Soil Reclassified', 'SMS-4.0in':'Four Soil Reclassified', 'SMS-8.0in':'Eight Soil Reclassified', 
                    'SMS-20.0in':'Twenty Soil Reclassified', 'SMS-40.0in':'Forty Soil Reclassified'}
        for s in df['station'].unique():
            new_df = df[df['station'] ==s]
            for m in new_df['Date'].dt.month.unique():
                month_frame = new_df[new_df['Date'].dt.month == m]
                count = month_frame[depth].count()
                corr = month_frame.corr()['ESI'][depth]
                soil = month_frame[soil_key.get(depth)].unique().item()
                soil_types.append(soil)
                num_observations.append(count)
                correlation.append(corr)
                month.append(m)
                station.append(s)
                
        self.stations_corr_by_month['Correlation'] = correlation
        self.stations_corr_by_month['Month'] = month
        self.stations_corr_by_month['Station'] = station
        self.stations_corr_by_month['Observations'] = num_observations
        self.stations_corr_by_month['Soil'] = soil_types
            
        #plot
        self.__plot_corr_by_month(depth_input=depth, resample_input=resample_type, hue=hue)
    
     
    #helper function
    def __plot_corr_by_month(self, depth_input, resample_input, hue):
        
        df = self.stations_corr_by_month
        
        
        if hue==False:
            
            fig, ax = plt.subplots()
            
            for i in df['Station'].unique():
            
                new_df = df[df['Station'] == i]
                plot = sns.scatterplot(x='Month', y='Correlation', data=new_df, label=new_df['Station'].unique().item(), palette='coolwarm', ax=ax)
                plot.set_title(str(resample_input) + ' ' + 'SCAN Data vs' + ' ' + str(resample_input) + ' '+ 'ALEXI by Month and Station at' + ' ' + str(depth_input))
            
            plt.legend(bbox_to_anchor=(1.02, 1), borderaxespad=0)
        else: 
            
            my_colors = {'A': 'red', 'B': 'green', 'C': 'blue', 'D': 'yellow'}
            
            fig, ax = plt.subplots()
            
            for i in df['Station'].unique():
                new_df = df[df['Station'] == i]
                for j in new_df.iterrows():
                    soil_type = my_colors.get(j[1][4])
                    print(soil_type)
                    if soil_type =='yellow':
                        plot = ax.scatter(j[1][1], j[1][0], color=my_colors.get(j[1][4]), label='D')
                    elif soil_type =='red':
                        plot = ax.scatter(j[1][1], j[1][0], color=my_colors.get(j[1][4]), label='A')
                    elif soil_type=='blue':
                        plot = ax.scatter(j[1][1], j[1][0], color=my_colors.get(j[1][4]), label='C')
                    elif soil_type=='green':
                        plot = ax.scatter(j[1][1], j[1][0], color=my_colors.get(j[1][4]), label='B')
                
                handles, labels = plt.gca().get_legend_handles_labels()
                by_label = dict(zip(labels, handles))
                plt.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.15, 1), borderaxespad=0)
            
            ax.set_title(str(resample_input) + ' ' + 'Alabama SCAN Data vs' + ' ' + str(resample_input) + ' '+ 'ALEXI, hued by Soil Type at' + ' ' + str(depth_input))
            plt.xlabel('Month')
            plt.ylabel('Correlation')
            
        
            