import pandas as pd
import seaborn as sns
from matplotlib.offsetbox import AnchoredText
import matplotlib.pyplot as plt
from scipy import stats
import warnings 

#ignore warnings that are thrown. 
warnings.filterwarnings('ignore')


# Read in the ESI data
esi_path = '/Users/coreywalker/Desktop/NOAA/ESIExtractProject/ESI_1wk_tif2select_pt.csv'
esi = pd.read_csv(esi_path)
esi['Date'] = pd.to_datetime(esi['Date'])

# # put in the scan_path!
scan_path = '/Users/coreywalker/Desktop/NOAA/SCANAnalysis/data/SCAN_DEPTHS_ALL.csv'
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

#create averages for sliced data. 
sms_grp['SMS-all-avg'] = (sms_grp['SMS-2.0in_mean'] + sms_grp['SMS-4.0in_mean'] + sms_grp['SMS-8.0in_mean'] + sms_grp['SMS-20.0in_mean'] + sms_grp['SMS-40.0in_mean']) / 5
sms_grp['SMS-2.0+4.0_avg'] = (sms_grp['SMS-2.0in_mean'] + sms_grp['SMS-4.0in_mean']) / 2
sms_grp['SMS-4.0+8.0_avg'] = (sms_grp['SMS-4.0in_mean'] + sms_grp['SMS-8.0in_mean']) / 2
sms_grp['SMS-8.0+20.0_avg'] = (sms_grp['SMS-8.0in_mean'] + sms_grp['SMS-20.0in_mean']) / 2
sms_grp['SMS-20.0+40.0_avg'] = (sms_grp['SMS-20.0in_mean'] + sms_grp['SMS-40.0in_mean']) / 2

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

eight_in_x = eight_corrected['ESI']
eight_in_y = eight_corrected['SMS-8.0in_mean']

twenty_in_x = twenty_corrected['ESI']
twenty_in_y = twenty_corrected['SMS-20.0in_mean']

forty_in_x = forty_corrected['ESI']
forty_in_y = forty_corrected['SMS-40.0in_mean']

#create the figure subplots based on each level of soil. 
fig, ax = plt.subplots(nrows=1, ncols=5, figsize=(25,10))
fig.suptitle('Alabama SCAN Soil Moisture Stations (SMS) at Different Depths vs Alexi Sattelite Environmental Stress Index (ESI)')

#here is the subplot for two in data.
sns.regplot(ax=ax[0], x=two_in_x, y=two_in_y, data='two_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_two = stats.pearsonr(two_in_x, two_in_y)
formated_r_two = ("{:.4f}".format(stats_two[0]))
formated_p_two = ("{:.4f}".format(stats_two[1]))
shape_two = two_corrected.shape[0]
at_two = AnchoredText(s=f"R2: {formated_r_two} \n P: {formated_p_two} \n Key: {freq} \n n: {shape_two}", loc='upper left')
ax[0].add_artist(at_two)
ax[0].set_title('All 2in SMS vs ESI')

#here is the subplot for four inch data
sns.regplot(ax=ax[1], x=four_in_x, y=four_in_y, data='four_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_four = stats.pearsonr(four_in_x, four_in_y)
formated_r_four = ("{:.4f}".format(stats_four[0]))
formated_p_four = ("{:.4f}".format(stats_four[1]))
shape_four = four_corrected.shape[0]
at_four = AnchoredText(s=f"R2: {formated_r_four} \n P: {formated_p_four} \n Key: {freq} \n n: {shape_four}", loc='upper left')
ax[1].add_artist(at_four)
ax[1].set_title('All 4in SMS vs ESI')

#here is the subplot for eight inch data
sns.regplot(ax=ax[2], x=eight_in_x, y=eight_in_y, data='two_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_eight = stats.pearsonr(eight_in_x, eight_in_y)
formated_r_eight = ("{:.4f}".format(stats_eight[0]))
formated_p_eight = ("{:.4f}".format(stats_eight[1]))
shape_eight = eight_corrected.shape[0]
at_eight = AnchoredText(s=f"R2: {formated_r_eight} \n P: {formated_p_eight} \n Key: {freq} \n n: {shape_eight}", loc='upper left')
ax[2].add_artist(at_eight)
ax[2].set_title('All 8in SMS vs ESI')

#here is the subplot for twenty inch data
sns.regplot(ax=ax[3], x=twenty_in_x, y=twenty_in_y, data='four_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_twenty = stats.pearsonr(twenty_in_x, twenty_in_y)
formated_r_twenty = ("{:.4f}".format(stats_twenty[0]))
formated_p_twenty = ("{:.4f}".format(stats_twenty[1]))
shape_twenty = twenty_corrected.shape[0]
at_twenty = AnchoredText(s=f"R2: {formated_r_twenty} \n P: {formated_p_twenty} \n Key: {freq} \n n: {shape_twenty}", loc='upper left')
ax[3].add_artist(at_twenty)
ax[3].set_title('All 20in SMS vs ESI')


# #here is the subplot for forty inch data
sns.regplot(ax=ax[4], x=forty_in_x, y=forty_in_y, data='four_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_forty = stats.pearsonr(forty_in_x, forty_in_y)
formated_r_forty = ("{:.4f}".format(stats_forty[0]))
formated_p_forty = ("{:.4f}".format(stats_forty[1]))
shape_forty = forty_corrected.shape[0]
at_forty = AnchoredText(s=f"R2: {formated_r_forty} \n P: {formated_p_forty} \n Key: {freq} \n n: {shape_twenty}", loc='upper left')
ax[4].add_artist(at_forty)
ax[4].set_title('All 40in SMS vs ESI')

plt.tight_layout()

# #lets try a grid plot to look at individual station stats for each depth. 

stations_two = sns.lmplot(x='ESI', y='SMS-2.0in_mean', data=two_corrected, col='station', height=6, col_wrap=3)
stations_two.fig.suptitle('ESI (y-axis) by Individual Alabama USDA 2in SMS (x-axis)')

stations_four = sns.lmplot(x='ESI', y='SMS-4.0in_mean', data=four_corrected, col='station', height=6, col_wrap=3)
stations_four.fig.suptitle('ESI (y-axis) by Individual Alabama USDA 4in SMS (x-axis)')

stations_eight = sns.lmplot(x='ESI', y='SMS-8.0in_mean', data=eight_corrected, col='station', height=6, col_wrap=3)
stations_eight.fig.suptitle('ESI (y-axis) by Individual Alabama USDA 8in SMS (x-axis)')

stations_twenty = sns.lmplot(x='ESI', y='SMS-20.0in_mean', data=twenty_corrected, col='station', height=6, col_wrap=3)
stations_twenty.fig.suptitle('ESI (y-axis) by Individual Alabama USDA 20in SMS (x-axis)')

stations_forty = sns.lmplot(x='ESI', y='SMS-40.0in_mean', data=forty_corrected, col='station', height=6, col_wrap=3)
stations_forty.fig.suptitle('ESI (y-axis) by Individual Alabama USDA 40in SMS (x-axis)')

#create the figure functons to annotate the appropriate stats for each graph. 
def annotate_two(data, **kws):
    r_2, p_2 = stats.pearsonr(data['ESI'], data['SMS-2.0in_mean'])
    shape2 = data.shape[0]
    ax = plt.gca()
    ax.text(-2, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_2, p_2, shape=shape2))

def annotate_four(data, **kws):
    r_4, p_4 = stats.pearsonr(data['ESI'], data['SMS-4.0in_mean'])
    shape4 = data.shape[0]
    ax = plt.gca()
    ax.text(-2, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_4, p_4, shape=shape4))

def annotate_eight(data, **kws):
    r_8, p_8 = stats.pearsonr(data['ESI'], data['SMS-8.0in_mean'])
    shape8 = data.shape[0]
    ax = plt.gca()
    ax.text(-2, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_8, p_8, shape=shape8))
 
def annotate_twenty(data, **kws):
    r_20, p_20 = stats.pearsonr(data['ESI'], data['SMS-20.0in_mean'])
    shape20 = data.shape[0]
    ax = plt.gca()
    ax.text(-2, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_20, p_20, shape=shape20))

def annotate_forty(data, **kws):
    r_40, p_40 = stats.pearsonr(data['ESI'], data['SMS-40.0in_mean'])
    shape40 = data.shape[0]
    ax = plt.gca()
    ax.text(-2, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_40, p_40, shape=shape40))
    
#show all the individual figures so that they can be saved. 
stations_two.map_dataframe(annotate_two)
stations_four.map_dataframe(annotate_four)
stations_eight.map_dataframe(annotate_eight)
stations_twenty.map_dataframe(annotate_twenty)
stations_forty.map_dataframe(annotate_forty)

plt.show()
plt.tight_layout()



