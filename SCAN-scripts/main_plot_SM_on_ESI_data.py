#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 17:01:32 2022

@author: cwalker
"""
from plot_functions import plot_SM_ANOM_for_ESI_date
from plot_functions import make_filepaths_frame

df = make_filepaths_frame()
#

depths = ['2inANOM', '4inANOM', '8inANOM', '20inANOM', '40inANOM']
arrays = []
for i in depths:    
    array = plot_SM_ANOM_for_ESI_date(df, 2015, 9, 17, percentiles=True, droughtmonitor=True, SM_ANOM=i)
    arrays.append(array)
