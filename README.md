# Intoduction to the SCANAnalysis Repository
Welcome to the SCANAnalysis repository! Here the goal is to share scientific analysis, evidence and scripts used to compare USDA SCAN site soil moisture stations across Alabama and their respective ALEXI ESI satellite pixels. 

This repo will analyze several research questions and provide answers to those questions demonstrated below:  

# Research Questions with Answers
1. How does ALEXI ESI compare to USDA SCAN site effective saturation anomalies?
- [Linear regression analysis showing slight relationship between known soil moisture and ESI at USDA SCAN station 2053](https://github.com/Corey4005/SCANAnalysis/blob/main/notebooks/Timeseries%20Analysis%20-%20SCAN%202053.ipynb)
- [A Plot (line 8) showing time series analysis between drought year 2006 at three soil depths corresponding to USDA SCAN site 2053 and associated ESI values](https://github.com/Corey4005/SCANAnalysis/blob/main/SCAN-scripts/SCAN%20vs%20ESI%20updates.ipynb)
- [Barplot (line 11) showing pairwise correlations across 8 stations at 5 depths with ESI](https://github.com/Corey4005/SCANAnalysis/blob/main/SCAN-scripts/SCAN%20vs%20ESI%20updates.ipynb) [*assuming* 2017 USDA Soil Parameters (pg. 209)](https://www.nrcs.usda.gov/wps/portal/nrcs/detailfull/soils/ref/?cid=nrcs142p2_054262)
- [Barplot (line 3) showing pairwise correlations across 18 stations at 5 depths using soil parameter tables from](https://github.com/Corey4005/SCANAnalysis/blob/main/SCAN-scripts/Statistics.ipynb) [*Carsel et. al.*](https://hwbdocuments.env.nm.gov/Los%20Alamos%20National%20Labs/General/14689.PDF?msclkid=a36b5239b03c11ec83b65afc7552cc4a)

2. What are the spatial and temporal relationships between ALEXI ESI and USDA SCAN sites across Alabama? 
- [Timeseries plots (lines 9 / 10) showing seasonal variablity in correlations between soil moisture anomalies and ALEXI ESI](https://github.com/Corey4005/SCANAnalysis/blob/main/SCAN-scripts/SCAN%20vs%20ESI%20updates.ipynb)

3. Can the derived statistical relationships between ALEXI ESI and observed
soil moisture be used to guide agricultural activities in locations far from
soil moisture sensors?
- [Deep learning model barplot (line 13) showing accuracy of classifying soil moiture as high or low across 4 depths using ESI as input parameter](https://github.com/Corey4005/SCANAnalysis/blob/main/SCAN-scripts/SCAN%20vs%20ESI%20updates.ipynb) 

# Questions without Answers 
1. Does Leaf Area Index affect the relationship between ESI and USDA SCAN? 
2. How does land classification type relate to correlations? 
3. What are the accuracy and error characteristics of these ESI-to-observation
comparisons?

## Useful Repository Scripts 
| Type | Description |
| ---- | ---- | 
|[Data Extraction](https://github.com/Corey4005/SCANAnalysis/blob/main/ESI-scripts/ExtractESI.py)| This is the script I used to extract data from the latitude and longitude of each SCAN site across Alabama from 80 GB worth of GOES sattelite images (20 years of daily data). If using this script, you will need to create your own filepath. It needs to be the filepath to the rootfile containing the GOES (daily data for each year) subdirectories. ALEXI ESI data can be provided to you by [Dr. Christopher Hain](https://weather.msfc.nasa.gov/sport/staff/chris_hain/?msclkid=e9d7c9a3b03711ec9b556478c604d69f) to download on your local machine|
|[Data Extraction](https://github.com/Corey4005/SCANAnalysis/blob/main/Earth-Engine/SCANTreeCover.js)| This is a script used to extract tree cover percentages across twenty years for a SCAN site of interest. This script can be pasted in the [Google Earth Engine](https://earthengine.google.com/) console or can be accessed directly [here](https://code.earthengine.google.com/e69616eae671012a18a2a954da7bc233). | 
| [Functions](https://github.com/Corey4005/SCANAnalysis/blob/main/SCAN-scripts/effective_SM_conversion_all.py) | A suite of functions to calculate soil moisture anomalies at each USDA SCAN site and compare to ESI. This uses assumptions on soil moisture provided by the [2017 USDA Soil Survey Manual](https://www.nrcs.usda.gov/wps/portal/nrcs/detailfull/soils/ref/?cid=nrcs142p2_054262) (pg. 209), and parameters provided by 9 site pedon reports. With this module you can append soil types, calculate effective soil moisture, classify high and low water contents, and look at correlations with ESI by site. There are also functions that will allow you to model soil moisture classes using a deep learning model. It should be noted that this script does not clean any of the data. |
| [Functions](https://github.com/Corey4005/SCANAnalysis/blob/main/SCAN-scripts/assumptions.py) |This is a list of functions for cleaning the USDA soil moisture data and calculating effective saturation using soil texture characteristic tables from [*Carsel et. al.*](https://hwbdocuments.env.nm.gov/Los%20Alamos%20National%20Labs/General/14689.PDF?msclkid=a36b5239b03c11ec83b65afc7552cc4a) With this module you can calculate standard deviations, z-scores, clean and calculate soil moisture anomalies, and plot ESI relationships with each USDA SCAN site. |
|[Shapefiles](https://github.com/Corey4005/SCANAnalysis/tree/main/shapefiles)| These are the shapefiles representing the shape of each ALEXI pixel corresponding to a USDA SCAN site. used to extract information from various sattelite remote sensing datasets |

# Task List
- [ ] Update data section with a README.md. 
- [ ] Create a math section describing assumptions. 
- [ ] Create Jupyter notebook showing land-class and ALEXI vs SCAN pearson R.
- [ ] Update data folder with script to acquire SCAN data. 
