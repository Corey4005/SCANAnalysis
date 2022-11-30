#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 18:49:26 2022

@author: cwalker

Purpose: a script to unzip ".tif.gz" ALEXI folders from a directory containing yearly 
data

"""

path = '/rhome/cwalker/Downloads/ALEXI/' #put in wherever your filepath is containing the directories for 
#each of the years of ALEXI you have. 

import os, gzip, shutil


def gz_extract(directory):
    extension = ".tif.gz"
    os.chdir(directory)
    for year in os.listdir(directory): # loop through items in dir
        print(year)
        yearDir = os.path.join(directory, year)
        for item in os.listdir(yearDir):
            if item.endswith(extension): # check for ".gz" extension
                gz_name = os.path.join(yearDir, item) # get full path of files
                file_name = (os.path.basename(gz_name)).rsplit('.',1)[0] #get file name for file within
                file_path = os.path.join(yearDir, file_name)
                print(gz_name, file_name)
                with gzip.open(gz_name,"rb") as f_in, open(file_path,"wb") as f_out:
                     shutil.copyfileobj(f_in, f_out)
                     os.remove(gz_name) # delete zipped file
        
gz_extract(path)
        