#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 13:33:51 2022

@author: cwalker
"""
from class_soils import soils
from datasets import GOES_READ
import pandas as pd

class Merge(soils):
    
    GOES_READ.rename(columns={'StationTriplet':'station'}, inplace=True)
    
    def __init__(self, data):
        
        soils.__init__(self, data)
        self.merge1wALEXI = pd.DataFrame()
        self.merge2wALEXI = pd.DataFrame()
        self.merge3wALEXI = pd.DataFrame()
        self.merge4wALEXI = pd.DataFrame()
        
        
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
    
   
        

    
            