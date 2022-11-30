#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 20:15:28 2022

@author: cwalker
"""

from plot_functions import plot_SM_ANOM_for_ESI_date
from plot_functions import make_filepaths_frame

df = make_filepaths_frame()

  
df = plot_SM_ANOM_for_ESI_date(df, 2018, 9, 17, volumetric=True, SM_ANOM='4inANOM')
