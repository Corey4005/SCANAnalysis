#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 18:17:41 2022

@author: cwalker
"""

from class_soils import soils
from datasets import SCAN_READ

obj = soils(SCAN_READ)
obj.mean_soil_moisture_by_month()
obj.standard_deviation_by_month()
obj.get_stations_month()
obj.merge_station_stdev_mean()
obj.z_score()
obj.quality_z_score(std=3.5)
obj.clean_data()