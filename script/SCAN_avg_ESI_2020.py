import pandas as pd
import seaborn as sns
from matplotlib.offsetbox import AnchoredText
import matplotlib.pyplot as plt
from scipy import stats
import scipy as sp
import warnings 


#ignore warnings that are thrown. 
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


#create an input variable for the merge
sms_grp = sms.groupby(['station', pd.Grouper(key='Date', freq=str(freq))]).agg(['mean', 'count'])


#the groupby function creates a multiindex that needs to be joined together.
sms_grp.columns = sms_grp.columns.map('_'.join)

#reset the index so that the columns are formatted correctly. 
sms_grp = sms_grp.reset_index()

#create groups by station, date, depth and count.
two_in = sms_grp[['station', 'Date', 'SMS-2.0in_mean', 'SMS-2.0in_count']]
four_in = sms_grp[['station', 'Date', 'SMS-4.0in_mean', 'SMS-4.0in_count']]
eight_in = sms_grp[['station', 'Date', 'SMS-8.0in_mean', 'SMS-8.0in_count']]
twenty_in = sms_grp[['station', 'Date', 'SMS-20.0in_mean', 'SMS-20.0in_count']]
forty_in = sms_grp[['station', 'Date', 'SMS-40.0in_mean', 'SMS-40.0in_count']]


#now, we filter to get just the weeks that produced a mean from 7 values. 
sms_2in_index = two_in[two_in['SMS-2.0in_count'] == 7]
sms_4in_index = four_in[four_in['SMS-4.0in_count']== 7]
sms_8in_index = eight_in[eight_in['SMS-8.0in_count']== 7]
sms_20in_index = twenty_in[twenty_in['SMS-20.0in_count']== 7]
sms_40in_index = forty_in[forty_in['SMS-40.0in_count']== 7]

#merge the ESI with the sms index at each group.
two_in_merge_sms_esi = pd.merge(left=esi, right=sms_2in_index, on=['Date', 'station'], how='outer', indicator='how').reset_index()
four_in_merge_sms_esi = pd.merge(left=esi, right=sms_4in_index, on=['Date', 'station'], how='outer', indicator='how').reset_index()
eight_in_merge_sms_esi = pd.merge(left=esi, right=sms_8in_index, on=['Date', 'station'], how='outer', indicator='how').reset_index()
twenty_in_merge_sms_esi = pd.merge(left=esi, right=sms_20in_index, on=['Date', 'station'], how='outer', indicator='how').reset_index()
forty_in_merge_sms_esi = pd.merge(left=esi, right=sms_40in_index, on=['Date', 'station'], how='outer', indicator='how').reset_index()


#index the dataframes and get only the values where both SMS AND ESI have a real value. 
both_two = two_in_merge_sms_esi[two_in_merge_sms_esi['how']=='both']
both_four = four_in_merge_sms_esi[four_in_merge_sms_esi['how']=='both']
both_eight = eight_in_merge_sms_esi[eight_in_merge_sms_esi['how']=='both']
both_twenty = twenty_in_merge_sms_esi[twenty_in_merge_sms_esi['how']=='both']
both_forty = forty_in_merge_sms_esi[forty_in_merge_sms_esi['how']=='both']

#correct the indexes to get rid of ESI values where there is a bad reading. 
two_corrected = both_two[both_two['ESI'] != -9999]
four_corrected = both_four[both_four['ESI'] != -9999]
eight_corrected = both_eight[both_eight['ESI']!= -9999]
twenty_corrected = both_twenty[both_twenty['ESI'] != -9999]
forty_corrected = both_forty[both_forty['ESI'] != -9999] 

# #create x and y values for eaach group plot.
two_in_x = two_corrected['ESI']
two_in_y = two_corrected['SMS-2.0in_mean']

four_in_x = four_corrected['ESI']
four_in_y = four_corrected['SMS-4.0in_mean']

print(two_in_x, two_in_y)
print(four_in_x, four_in_y)

eight_in_x = eight_corrected['ESI']
eight_in_y = eight_corrected['SMS-8.0in_mean']

twenty_in_x = twenty_corrected['ESI']
twenty_in_y = twenty_corrected['SMS-20.0in_mean']

forty_in_x = forty_corrected['ESI']
forty_in_y = forty_corrected['SMS-40.0in_mean']

#create a regplot based on two_in values. 
plot = sns.regplot(two_in_x, two_in_y, scatter_kws={'s':2}, line_kws={'color': 'black'})
stats = stats.pearsonr(two_in_x, two_in_y)
r2 = stats[0]
p_value = stats[1]
format_r2 = '{0:.3f}'.format(r2)
format_p = '{0:6f}'.format(p_value)
shape = two_corrected.shape[0]
at = AnchoredText(s=f"R2: {format_r2} \n P: {format_p} \n Key: {freq} \n n: {shape}", loc='upper left')
plot.add_artist(at)

#create a regplot based on four_in values. 
plot2 = sns.regplot(four_in_x, four_in_y, scatter_kws={'s':2}, line_kws={'color': 'black'})
# stats2 = stats.pearsonr(four_in_x, four_in_y)
# four_in_r2 = stats2[0]
# four_in_p = stats2[1]
# format_four_in_r2 = '{0:.3f}'.format(four_in_r2)
# format_four_in_p = '{0:6f}'.format(four_in_p)
# shape_four_in = four_corrected.shape[0]
# at2 = AnchoredText(s=f"R2: {format_four_in_r2} \n P: {format_four_in_p} \n Key: {freq} \n n: {shape_four_in}", loc='upper left')
# plot2.add_artist(at2)

# #create a regplot based on eight_in values. 
# plot3 = sns.regplot(eight_in_x, eight_in_y, scatter_kws={'s':2}, line_kws={'color': 'black'})
# stats3 = stats.pearsonr(eight_in_x, eight_in_y)
# r2 = stats[0]
# p_value = stats[1]
# format_r2 = '{0:.3f}'.format(r2)
# format_p = '{0:6f}'.format(p_value)
# shape = eight_corrected.shape[0]
# at = AnchoredText(s=f"R2: {format_r2} \n P: {format_p} \n Key: {freq} \n n: {shape}", loc='upper left')
# plot.add_artist(at)

# #create a regplot based on twenty_in values. 
# plot4 = sns.regplot(twenty_in_x, twenty_in_y, scatter_kws={'s':2}, line_kws={'color': 'black'})
# stats4 = stats.pearsonr(twenty_in_x, twenty_in_y)
# r2 = stats[0]
# p_value = stats[1]
# format_r2 = '{0:.3f}'.format(r2)
# format_p = '{0:6f}'.format(p_value)
# shape = twenty_corrected.shape[0]
# at = AnchoredText(s=f"R2: {format_r2} \n P: {format_p} \n Key: {freq} \n n: {shape}", loc='upper left')
# plot.add_artist(at)

# #create a regplot based on forty_in values. 
# plot5 = sns.regplot(forty_in_x, forty_in_y, scatter_kws={'s':2}, line_kws={'color': 'black'})
# stats5 = stats.pearsonr(forty_in_x, forty_in_y)
# r2 = stats[0]
# p_value = stats[1]
# format_r2 = '{0:.3f}'.format(r2)
# format_p = '{0:6f}'.format(p_value)
# shape = forty_corrected.shape[0]
# at = AnchoredText(s=f"R2: {format_r2} \n P: {format_p} \n Key: {freq} \n n: {shape}", loc='upper left')
# plot.add_artist(at)


# #lets try a grid plot to look at individual station stats. 
# g2 = sns.lmplot(x='ESI', y='SMS-2.0in_mean', data=corrected, col='station', height=6, col_wrap=3)

# def annotate(data, **kws):
#     r, p =sp.stats.pearsonr(data['ESI'], data['SMS-2.0in_mean'])
#     shape2 = data.shape[0]
#     ax = plt.gca()
#     ax.text(-2, 50, s='r={:.2f}, \n p={:.2g},\n n={shape2}'.format(r, p, shape2=shape2))

# g2.map_dataframe(annotate)
# plt.show()

