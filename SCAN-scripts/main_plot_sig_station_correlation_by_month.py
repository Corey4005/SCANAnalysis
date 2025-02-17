#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 18:17:41 2022

@author: cwalker
"""

from class_driver import Driver
from datasets import SCAN_READ


#instantiate a driver object with data
obj = Driver(SCAN_READ)

#calculate the soil moisture mean by month dataframe
obj.mean_soil_moisture_by_month()

#get the standard deviation by month dataframe
obj.standard_deviation_by_month()

#create a column for months in the stations dataframe
obj.get_month_from_dates()

#merge stdev, mean and stations dataframe together
obj.merge_station_stdev_mean()

#calculate the z_scores for each of the observations in the merged dataframe
obj.z_score()

#calculate the data quality based on z_score
obj.quality_z_score(std=3.5)

#clean the data and remove data that is outside the 3.5 standard deviation limit
obj.clean_data()

#resample the SMS data and return 1w, 2w, 3w, 4w dataframes and store in resample class
obj.soil_moisture_one_week_resample()
obj.soil_moisture_two_week_resample()
obj.soil_moisture_three_week_resample()
obj.soil_moisture_four_week_resample()

#resample the ALEXI data to 2w, 3w, and 4w and store in resample class
obj.ALEXI_two_week_resample()
obj.ALEXI_three_week_resample()
obj.ALEXI_four_week_resample()

#append the soils to SMS dataframes
obj.create_1w_soil_columns()
obj.create_2w_soil_columns()
obj.create_3w_soil_columns()
obj.create_4w_soil_columns()

#merge with ALEXI on 1w, 2w, 3w, 4w and store in driver class 
obj.merge_1w_soil_resample_with_ALEXI()
obj.merge_2w_soil_resample_with_ALEXI()
obj.merge_3w_soil_resample_with_ALEXI()
obj.merge_4w_soil_resample_with_ALEXI()

#correlate by soil type, depth and ESI.
obj.corr_1w_resample_ESI_by_soils()
obj.corr_2w_resample_ESI_by_soils()
obj.corr_3w_resample_ESI_by_soils()
obj.corr_4w_resample_ESI_by_soils()

#concatinate the correlation dataframes into one.
obj.concatinate_corr_dataframes()

#plots - uncomment each one at a time
obj.create_time_series_box_plot_df()

#plot signifigant station counts by month 
obj.plot_sig_box_plot_stations_by_month(resample_input='1w', depth_input='SMS-4.0in')

