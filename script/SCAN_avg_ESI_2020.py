import pandas as pd
import seaborn as sns
from matplotlib.offsetbox import AnchoredText
from scipy import stats
import warnings 

warnings.filterwarnings('ignore')


# Read in the ESI data
esi_path = 'C:/Users/Corey4005/Desktop/NOAA/ESIExtractProject/data/ESI_1wk_tif2select_pt.csv'
esi = pd.read_csv(esi_path)
esi['Date'] = pd.to_datetime(esi['Date'])

# # put in the scan_path!
scan_path = 'C:/Users/Corey4005/Desktop/NOAA/SCANAnalysis/data/SCAN_DEPTHS_ALL.csv'
scan = pd.read_csv(scan_path)


# # Just get the columns we are interested in
sms = scan[['Date', 'station','SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in','SMS-40.0in']]

# # Date column to datetime format
sms['Date'] = pd.to_datetime(sms['Date'])

#group the dataframe by station and date and agrigate the mean and count for each group.
key_codes = pd.DataFrame({'Weekday': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], 'Key': ['W-Sun', 'W-Mon', 'W-Tue', 'W-Wed', 'W-Thu', 'W-Fri', 'W-Sat',]})
print(f" \n\n Here is a key of the way you can group the data by week: \n\n {key_codes}")
freq = input("Input the desired grouping frequency: ")

#create a dataframe of the unique stations

#create an input variable for the merge

sms_grp = sms.groupby(['station', pd.Grouper(key='Date', freq=str(freq))]).agg(['mean', 'count'])


#testing...
# origin = pd.Timestamp("2000-26-01")
# sms_grp = sms.groupby('station', pd.Grouper(key='Date', freq='W', origin=origin)).agg(['mean', 'count'])

#the groupby function creates a multiindex that needs to be joined together.
sms_grp.columns = sms_grp.columns.map('_'.join)

#reset the index so that the columns are formatted correctly. 
sms_grp = sms_grp.reset_index()
two_in = sms_grp[['station', 'Date', 'SMS-2.0in_mean', 'SMS-2.0in_count']]

#now, we filter to get just the weeks that produced a mean from 7 values. 
sms_2in_index = two_in[two_in['SMS-2.0in_count'] == 7]

#merge the ESI with the sms 2-in index at Date and Station.
merge_sms_esi = pd.merge(left=esi, right=sms_2in_index, on=['Date', 'station'], how='outer', indicator='how').reset_index()
#index the dataframe and get only the values where both were merged AND ESI has a real value. 
both = merge_sms_esi[merge_sms_esi['how']=='both']
corrected = both[both['ESI'] != -9999]

#send that bad boy to a csv for analysis. 
# corrected.to_csv('')

#create x and y values for weekly plot
x = corrected['ESI']
y = corrected['SMS-2.0in_mean']

#create a regplot based on weekly values. 
plot = sns.regplot(x, y, scatter_kws={'s':2}, line_kws={'color': 'black'})
stats = stats.pearsonr(x, y)
r2 = stats[0]
p_value = stats[1]
format_r2 = '{0:.3f}'.format(r2)
format_p = '{0:6f}'.format(p_value)
shape = corrected.shape[0]

#create a legend for weekly values plot.
at = AnchoredText(s=f"R2: {format_r2} \n P: {format_p} \n Key: {freq} \n n: {shape}", loc='upper left')
plot.add_artist(at)

#create a facetplot for each station showing regression by station. 
g = sns.FacetGrid(corrected, col='station', height=6, col_wrap=3)
g.map_dataframe(sns.regplot, x="ESI", y="SMS-2.0in_mean")
g.set_axis_labels("ESI", "SMS-2.0in_mean")
g.add_legend()










