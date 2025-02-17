#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 15:28:57 2022

@author: cwalker
"""
from class_merge import Merge
import pandas as pd

class Correlate(Merge):

 def __init__(self, data):
     
     Merge.__init__(self, data)
     self.one_w_corr = pd.DataFrame()
     self.two_w_corr = pd.DataFrame()
     self.three_w_corr = pd.DataFrame()
     self.four_w_corr = pd.DataFrame()
     self.concatinated_corr_df = pd.DataFrame()
    
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