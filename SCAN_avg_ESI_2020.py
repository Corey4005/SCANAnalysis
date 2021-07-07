import pandas as pd

# Read in the ESI data
esi = pd.read_csv('C:/Users/cwalker/Desktop/Data/Processed_ESI/ESI_1wk_tif2select_pt.csv')
esi['Date'] = pd.to_datetime(esi['Date'], format='%Y-%m-%d')
print(esi.shape) # 19080 rows x 3 columns
print(esi.columns)

# Select just data from year 2020
esi_2020 = esi[esi['Date'].dt.year == 2020]
print(esi_2020.shape) # 954 rows 3 cols
print(esi_2020['Date'].nunique()) # 53 unique dates

# # Read in the SCAN data
# scan_path = '/path/to/SCAN_data/'
# scan = pd.read_csv(scan_path + 'SCAN_DEPTHS_ALL.csv')
# print(scan.shape)
# print(scan.columns)
# # Just get the columns we are interested in
# sms = scan[['Date', 'station','SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in','SMS-40.0in']]
# # Date column to datetime format
# sms['Date'] = pd.to_datetime(sms['Date'],format='%Y-%m-%d')
# print(sms.dtypes)
# # Get data for year 2020
# # grouping every week. Make sure you have week prior or after (depending on how get avg.)
# # COREY, MAKE SURE THIS IS CALCULATING THE AVERAGES THE WAY YOU WANT!!! IS THIS AVG. 7DAY PRIOR OR AFTER?
# sms_2020= sms[(sms['Date'] >= '2020-01-01')& (sms['Date'] <= '2021-01-05')]
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
# sms_esi = pd.merge(left=esi_2020, right=grp_7, on=['Date', 'station'], how='outer', indicator='how' )
# print(sms_esi.shape) # 954 rows 9 cols

# # Let's see if things merged the way we expected:
# left = sms_esi[sms_esi['how']=='left_only']
# print(left.shape) # 120 rows of missing data from the SCAN
# print(left['Date'].nunique()) # looks like some missing data from the SCAN dataset
# print(left.head())

# # This is what we are really interested in:
# both = sms_esi[sms_esi['how']=='both']
# print(both['Date'].nunique()) # 53
# print(both.shape) # 834 rows, 9 cols

# # just chekcing what didn't merge from SCAN
# right = sms_esi[sms_esi['how']=='right_only']
# print(right.shape) # 0 rows. Great!!!! No, missing data from the SCAN data

# # example to look at missing data
# # Take a look at some of the missing scan data to be sure it really is missing
# print(grp_7[(grp_7['Date']=='2020-09-02') & (grp_7['station']=='2114:AL:SCAN')])
# # even check the data before our grouping
# print(sms_2020[(sms_2020['Date']=='2020-09-02') & (sms_2020['station']=='2114:AL:SCAN')])

# final_df = both[['Date', 'station','ESI', 'SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in','SMS-20.0in', 'SMS-40.0in']]
# final_df.sort_values('Date', inplace=True)
# final_df.to_csv('/path/to/esi_1wk_tif/SCANavg_ESI_2020.csv', index=False)

