# Intoduction to the SCANAnalysis Repository
The point of this repository is to report and share scientific analysis between USDA SCAN site soil moisture stations across Alabama and their respective ALEXI ESI satellite pixels. This repo will analyze several research questions and provide answers. 

# Research Questions with Answers
1. How does the ALEXI ESI compare to USDA SCAN site effective saturation anomalies?
- [Linear regression analysis showing slight relationship between known soil moisture and ESI at station 2053](https://github.com/Corey4005/SCANAnalysis/blob/main/notebooks/Timeseries%20Analysis%20-%20SCAN%202053.ipynb)

2. What are the spatial and temporal relationships between ALEXI ESI and USDA SCAN sites across Alabama? 
- [Some stations correlate better with ESI, but most have seasonal variability](https://github.com/Corey4005/SCANAnalysis/blob/main/SCAN-scripts/SCAN%20vs%20ESI%20updates.ipynb)

# Current Questions without Answers
1. Does Leaf Area Index affect the relationship between ESI and USDA SCAN? 
2. How does land classification type relate to correlations? 

# Helpful Sripts
If you are wanting to do some similar analysis of ALEXI vs USDA SCAN, I reccomend the following scripts: 

1. [A suite of functions that can be used to make analysis easier, given a similar dataframe](https://github.com/Corey4005/SCANAnalysis/blob/main/SCAN-scripts/effective_SM_conversion_all.py)
    - Data used in the above script found [here](https://github.com/Corey4005/SCANAnalysis/tree/main/data)

2. [A script to decode ALEXI raster images at specific latitudes and longitudes](https://github.com/Corey4005/SCANAnalysis/blob/main/ESI-scripts/ExtractESI.py)
    - Metadata used in the above script that can be edited found [here](https://github.com/Corey4005/SCANAnalysis/tree/main/data)

