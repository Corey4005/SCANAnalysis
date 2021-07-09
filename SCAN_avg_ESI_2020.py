import pandas as pd
import numpy as np

# Read in the ESI data
esi = pd.read_csv('/Users/coreywalker/Desktop/NOAA/ESIExtractProject/ESI_1wk_tif2select_pt.csv')
esi['Date'] = pd.to_datetime(esi['Date'])
# print(esi.dtype)
#print(esi.shape) # 19080 rows x 3 columns
#print(esi.columns)



# # Read in the SCAN data
scan_path = '/Users/coreywalker/Desktop/NOAA/SCANAnalysis/SCAN_DEPTHS_ALL.csv'
scan = pd.read_csv(scan_path)
#print(scan.columns)
#print(scan.shape)
#print(scan.columns)

# # Just get the columns we are interested in
sms = scan[['Date', 'station','SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in','SMS-40.0in']]
sms_test = scan[['Date', 'station', 'SMS-2.0in']]

# # Date column to datetime format
sms['Date'] = pd.to_datetime(sms['Date'])
#print(sms.dtypes)

sms_grp = sms.groupby(['station', pd.Grouper(key='Date', freq='W-SUN')]).size()

index = np.where(sms_grp == 7)
print(index[0])
#print(sms_test.iloc[index[0]])
#sms_grp.to_csv('/Users/coreywalker/Desktop/test_group.csv')
#.mean().reset_index()
#print(sms_grp.size('Date'))

# print(sms_grp.shape)
#print(filtered.shape)
#print(sms_grp['station'].unique())

# # Get data for year 2020
# # grouping every week. Make sure you have week prior or after (depending on how get avg.)
# # MAKE SURE THIS IS CALCULATING THE AVERAGES THE WAY YOU WANT!!! IS THIS AVG. 7DAY PRIOR OR AFTER?


# sms_2020= sms[(sms['Date'] >= '2020-01-01') & (sms['Date'] <= '2021-01-05')]
# print(sms_2020.shape) # 5828 X 7
# print(sms_2020['Date'].nunique()) # 372
# print(sms_2020['Date'].dt.year.unique())


# grp_7 = sms_2020.groupby(['station', pd.Grouper(key='Date', freq='7D')]).mean().reset_index()
# print(grp_7.shape) # 834 X 7
# print(grp_7['Date'].nunique()) # 53 unique dates
# print(grp_7['station'].nunique()) # only 17 stations

# # checking out the dates to see if all looks right.
# grp_7_dates = grp_7['Date'].dt.date.unique()
# print(len(grp_7_dates))
# print(grp_7_dates.max())
# print(grp_7_dates.min())

# # merge the esi and SCAN
# sms_esi = pd.merge(left=esi, right=sms_grp, on=['Date', 'station'], how='outer', indicator='how').reset_index()



# # # This is what we are really interested in:
# both = sms_esi[sms_esi['how']=='both']
# print(both['Date'].nunique()) 
# print(both.shape) 
# print(both)

# both.to_csv('/Users/coreywalker/Desktop/NOAA/both_merged.csv')





