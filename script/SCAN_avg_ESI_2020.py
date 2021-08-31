import pandas as pd
import seaborn as sns
from matplotlib.offsetbox import AnchoredText
import matplotlib.pyplot as plt
from scipy import stats
import warnings 

#ignore warnings that are thrown. 
warnings.filterwarnings('ignore')


# Read in the ESI data
esi_path = 'C:/Users/cwalker/Desktop/SCANAnalysis/data/ESI_1wk_tif2select_pt.csv'
esi = pd.read_csv(esi_path)
esi['Date'] = pd.to_datetime(esi['Date'])

# # put in the scan_path!
scan_path = 'C:/Users/cwalker/Desktop/SCANAnalysis/data/SCAN_DEPTHS_ALL.csv'
scan = pd.read_csv(scan_path)


# # Just get the columns we are interested in
sms = scan[['Date', 'station','SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in','SMS-40.0in']]

# Date column to datetime format
sms['Date'] = pd.to_datetime(sms['Date'])

#create rolling averages for 
sms['2in_rolling_mean'] = sms['SMS-2.0in'].rolling(7, min_periods=3).mean()
sms['4in_rolling_mean'] = sms['SMS-4.0in'].rolling(7, min_periods=3).mean()
sms['8in_rolling_mean'] = sms['SMS-8.0in'].rolling(7, min_periods=3).mean()
sms['20in_rolling_mean'] = sms['SMS-20.0in'].rolling(7, min_periods=3).mean()
sms['40in_rolling_mean'] = sms['SMS-40.0in'].rolling(7, min_periods=3).mean()

#create averages for sliced data
sms['SMS-all-avg'] = (sms['2in_rolling_mean'] + sms['4in_rolling_mean'] + sms['8in_rolling_mean'] + sms['20in_rolling_mean'] + sms['40in_rolling_mean']) / 5
sms['SMS-2.0+4.0_avg'] = (sms['2in_rolling_mean'] + sms['4in_rolling_mean']) / 2
sms['SMS-4.0+8.0_avg'] = (sms['4in_rolling_mean'] + sms['8in_rolling_mean']) / 2
sms['SMS-8.0+20.0_avg'] = (sms['8in_rolling_mean'] + sms['20in_rolling_mean']) / 2
sms['SMS-20.0+40.0_avg'] = (sms['20in_rolling_mean'] + sms['40in_rolling_mean']) /2

#subset sms for each group
two_in = sms[['station', 'Date', '2in_rolling_mean']]
four_in = sms[['station', 'Date', '4in_rolling_mean']]
eight_in = sms[['station', 'Date', '8in_rolling_mean']]
twenty_in = sms[['station', 'Date', '20in_rolling_mean']]
forty_in = sms[['station', 'Date', '40in_rolling_mean']]
all_avg = sms[['station', 'Date', 'SMS-all-avg']]
two_in_four_in_avg = sms[['station', 'Date', 'SMS-2.0+4.0_avg']]
four_in_eight_in_avg = sms[['station', 'Date', 'SMS-4.0+8.0_avg']]
eight_in_twenty_in_avg = sms[['station', 'Date','SMS-8.0+20.0_avg']]
twenty_in_forty_in_avg = sms[['station', 'Date', 'SMS-20.0+40.0_avg']]

#merge ESI and SMS
two_in_merge = pd.merge(left=esi, right=two_in, on=['Date', 'station'], how='outer')
four_in_merge = pd.merge(left=esi, right=four_in, on=['Date', 'station'], how='outer')
eight_in_merge = pd.merge(left=esi, right=eight_in, on=['Date', 'station'], how='outer')
twenty_in_merge = pd.merge(left=esi, right=twenty_in, on=['Date', 'station'], how='outer')
forty_in_merge = pd.merge(left=esi, right=forty_in, on=['Date', 'station'], how='outer')
all_avg_merge = pd.merge(left=esi, right=all_avg, on=['Date', 'station'], how='outer')
two_in_four_in_merge = pd.merge(left=esi, right=two_in_four_in_avg, on=['Date', 'station'], how='outer')
four_in_eight_in_merge = pd.merge(left=esi, right=four_in_eight_in_avg, on=['Date', 'station'], how='outer')
eight_in_twenty_in_merge = pd.merge(left=esi, right=eight_in_twenty_in_avg, on=['Date', 'station'], how='outer')
twenty_in_forty_in_merge = pd.merge(left=esi, right=twenty_in_forty_in_avg, on=['Date', 'station'], how='outer')

#correct the indexes to get rid of ESI values where there is a bad reading and drop all NaNs. 
two_corrected = two_in_merge[two_in_merge['ESI'] != -9999].dropna()
four_corrected = four_in_merge[four_in_merge['ESI'] != -9999].dropna()
eight_corrected = eight_in_merge[eight_in_merge['ESI']!= -9999].dropna()
twenty_corrected = twenty_in_merge[twenty_in_merge['ESI'] != -9999].dropna()
forty_corrected = forty_in_merge[forty_in_merge['ESI'] != -9999].dropna()
all_avg_corrected = all_avg_merge[all_avg_merge['ESI'] != -9999].dropna()
two_in_four_in_corrected = two_in_four_in_merge[two_in_four_in_merge['ESI'] != -9999].dropna()
four_in_eight_in_corrected = four_in_eight_in_merge[four_in_eight_in_merge['ESI'] != -9999].dropna()
eight_in_twenty_in_corrected = eight_in_twenty_in_merge[eight_in_twenty_in_merge['ESI'] != -9999].dropna()
twenty_in_forty_in_corrected = twenty_in_forty_in_merge[twenty_in_forty_in_merge['ESI'] != -9999].dropna()

# #create x and y values for eaach group plot.
two_in_x = two_corrected['ESI']
two_in_y = two_corrected['2in_rolling_mean']

four_in_x = four_corrected['ESI']
four_in_y = four_corrected['4in_rolling_mean']

eight_in_x = eight_corrected['ESI']
eight_in_y = eight_corrected['8in_rolling_mean']

twenty_in_x = twenty_corrected['ESI']
twenty_in_y = twenty_corrected['20in_rolling_mean']

forty_in_x = forty_corrected['ESI']
forty_in_y = forty_corrected['40in_rolling_mean']

all_avg_x = all_avg_corrected['ESI']
all_avg_y = all_avg_corrected['SMS-all-avg']

two_in_four_in_x = two_in_four_in_corrected['ESI']
two_in_four_in_y = two_in_four_in_corrected['SMS-2.0+4.0_avg']

four_in_eight_in_x = four_in_eight_in_corrected['ESI']
four_in_eight_in_y = four_in_eight_in_corrected['SMS-4.0+8.0_avg']

eight_in_twenty_in_x = eight_in_twenty_in_corrected['ESI']
eight_in_twenty_in_y = eight_in_twenty_in_corrected['SMS-8.0+20.0_avg']

twenty_in_forty_in_x = twenty_in_forty_in_corrected['ESI']
twenty_in_forty_in_y = twenty_in_forty_in_corrected['SMS-20.0+40.0_avg']

#create the figure subplots based on each level of soil. 
fig, ax = plt.subplots(nrows=2, ncols=5, figsize=(25,10))
fig.suptitle('Alabama SCAN Soil Moisture Stations (SMS) at Different Depths vs Alexi Sattelite Environmental Stress Index (ESI)')

#here is the subplot for two in data.
sns.regplot(ax=ax[0, 0], x=two_in_x, y=two_in_y, data='two_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_two = stats.pearsonr(two_in_x, two_in_y)
formated_r_two = ("{:.4f}".format(stats_two[0]))
formated_p_two = ("{:.4f}".format(stats_two[1]))
shape_two = two_corrected.shape[0]
at_two = AnchoredText(s=f"R2: {formated_r_two} \n P: {formated_p_two} \n n: {shape_two}", loc='upper left')
ax[0, 0].add_artist(at_two)
ax[0, 0].set_title('All 2in SMS vs ESI')

# #here is the subplot for four inch data
# sns.regplot(ax=ax[1], x=four_in_x, y=four_in_y, data='four_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
# stats_four = stats.pearsonr(four_in_x, four_in_y)
# formated_r_four = ("{:.4f}".format(stats_four[0]))
# formated_p_four = ("{:.4f}".format(stats_four[1]))
# shape_four = four_corrected.shape[0]
# at_four = AnchoredText(s=f"R2: {formated_r_four} \n P: {formated_p_four} \n n: {shape_four}", loc='upper left')
# ax[1].add_artist(at_four)
# ax[1].set_title('All 4in SMS vs ESI')

# #here is the subplot for eight inch data
# sns.regplot(ax=ax[2], x=eight_in_x, y=eight_in_y, data='two_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
# stats_eight = stats.pearsonr(eight_in_x, eight_in_y)
# formated_r_eight = ("{:.4f}".format(stats_eight[0]))
# formated_p_eight = ("{:.4f}".format(stats_eight[1]))
# shape_eight = eight_corrected.shape[0]
# at_eight = AnchoredText(s=f"R2: {formated_r_eight} \n P: {formated_p_eight} \n n: {shape_eight}", loc='upper left')
# ax[2].add_artist(at_eight)
# ax[2].set_title('All 8in SMS vs ESI')

# #here is the subplot for twenty inch data
# sns.regplot(ax=ax[3], x=twenty_in_x, y=twenty_in_y, data='four_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
# stats_twenty = stats.pearsonr(twenty_in_x, twenty_in_y)
# formated_r_twenty = ("{:.4f}".format(stats_twenty[0]))
# formated_p_twenty = ("{:.4f}".format(stats_twenty[1]))
# shape_twenty = twenty_corrected.shape[0]
# at_twenty = AnchoredText(s=f"R2: {formated_r_twenty} \n P: {formated_p_twenty} \n n: {shape_twenty}", loc='upper left')
# ax[3].add_artist(at_twenty)
# ax[3].set_title('All 20in SMS vs ESI')

#   #here is the subplot for forty inch data
# sns.regplot(ax=ax[4], x=forty_in_x, y=forty_in_y, data='four_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
# stats_forty = stats.pearsonr(forty_in_x, forty_in_y)
# formated_r_forty = ("{:.4f}".format(stats_forty[0]))
# formated_p_forty = ("{:.4f}".format(stats_forty[1]))
# shape_forty = forty_corrected.shape[0]
# at_forty = AnchoredText(s=f"R2: {formated_r_forty} \n P: {formated_p_forty} \n n: {shape_twenty}", loc='upper left')
# ax[4].add_artist(at_forty)
# ax[4].set_title('All 40in SMS vs ESI')

# #here is the subplot for the all average data
# sns.regplot(ax=ax[5], x=all_avg_x, y=all_avg_y, data='all_avg_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
# stats_all = stats.pearsonr(all_avg_x, all_avg_y)
# formated_r_all_avg = ("{:.4f}".format(stats_all[0]))
# formated_p_all_avg = ("{:.4f}".format(stats_all[1]))
# shape_all_avg = all_avg_corrected.shape[0]
# at_all = AnchoredText(s=f"R2: {formated_r_all_avg} \n P: {formated_p_all_avg} \n n: {shape_all_avg}", loc='upper left')
# ax[5].add_artist(at_forty)
# ax[5].set_title('All Depths SMS Avg vs ESI')

# #  #here is the subplot for forty inch data
# # sns.regplot(ax=ax[4], x=forty_in_x, y=forty_in_y, data='four_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
# # stats_forty = stats.pearsonr(forty_in_x, forty_in_y)
# # formated_r_forty = ("{:.4f}".format(stats_forty[0]))
# # formated_p_forty = ("{:.4f}".format(stats_forty[1]))
# # shape_forty = forty_corrected.shape[0]
# # at_forty = AnchoredText(s=f"R2: {formated_r_forty} \n P: {formated_p_forty} \n n: {shape_twenty}", loc='upper left')
# # ax[4].add_artist(at_forty)
# # ax[4].set_title('All 40in SMS vs ESI')

# #  #here is the subplot for forty inch data
# # sns.regplot(ax=ax[4], x=forty_in_x, y=forty_in_y, data='four_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
# # stats_forty = stats.pearsonr(forty_in_x, forty_in_y)
# # formated_r_forty = ("{:.4f}".format(stats_forty[0]))
# # formated_p_forty = ("{:.4f}".format(stats_forty[1]))
# # shape_forty = forty_corrected.shape[0]
# # at_forty = AnchoredText(s=f"R2: {formated_r_forty} \n P: {formated_p_forty} \n n: {shape_twenty}", loc='upper left')
# # ax[4].add_artist(at_forty)
# # ax[4].set_title('All 40in SMS vs ESI')

# #  #here is the subplot for forty inch data
# # sns.regplot(ax=ax[4], x=forty_in_x, y=forty_in_y, data='four_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
# # stats_forty = stats.pearsonr(forty_in_x, forty_in_y)
# # formated_r_forty = ("{:.4f}".format(stats_forty[0]))
# # formated_p_forty = ("{:.4f}".format(stats_forty[1]))
# # shape_forty = forty_corrected.shape[0]
# # at_forty = AnchoredText(s=f"R2: {formated_r_forty} \n P: {formated_p_forty} \n n: {shape_twenty}", loc='upper left')
# # ax[4].add_artist(at_forty)
# # ax[4].set_title('All 40in SMS vs ESI')

# #  #here is the subplot for forty inch data
# # sns.regplot(ax=ax[4], x=forty_in_x, y=forty_in_y, data='four_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
# # stats_forty = stats.pearsonr(forty_in_x, forty_in_y)
# # formated_r_forty = ("{:.4f}".format(stats_forty[0]))
# # formated_p_forty = ("{:.4f}".format(stats_forty[1]))
# # shape_forty = forty_corrected.shape[0]
# # at_forty = AnchoredText(s=f"R2: {formated_r_forty} \n P: {formated_p_forty} \n n: {shape_twenty}", loc='upper left')
# # ax[4].add_artist(at_forty)
# # ax[4].set_title('All 40in SMS vs ESI')

# plt.tight_layout()

# # #lets try a grid plot to look at individual station stats for each depth. 

# stations_two = sns.lmplot(x='ESI', y='2in_rolling_mean', data=two_corrected, col='station', height=6, col_wrap=3)
# stations_two.fig.suptitle('ESI (y-axis) by Individual Alabama USDA 2in SMS (x-axis)')

# stations_four = sns.lmplot(x='ESI', y='4in_rolling_mean', data=four_corrected, col='station', height=6, col_wrap=3)
# stations_four.fig.suptitle('ESI (y-axis) by Individual Alabama USDA 4in SMS (x-axis)')

# stations_eight = sns.lmplot(x='ESI', y='8in_rolling_mean', data=eight_corrected, col='station', height=6, col_wrap=3)
# stations_eight.fig.suptitle('ESI (y-axis) by Individual Alabama USDA 8in SMS (x-axis)')

# stations_twenty = sns.lmplot(x='ESI', y='20in_rolling_mean', data=twenty_corrected, col='station', height=6, col_wrap=3)
# stations_twenty.fig.suptitle('ESI (y-axis) by Individual Alabama USDA 20in SMS (x-axis)')

# stations_forty = sns.lmplot(x='ESI', y='40in_rolling_mean', data=forty_corrected, col='station', height=6, col_wrap=3)
# stations_forty.fig.suptitle('ESI (y-axis) by Individual Alabama USDA 40in SMS (x-axis)')

# #create the figure functons to annotate the appropriate stats for each graph. 
# def annotate_two(data, **kws):
#     r_2, p_2 = stats.pearsonr(data['ESI'], data['2in_rolling_mean'])
#     shape2 = data.shape[0]
#     ax = plt.gca()
#     ax.text(-2, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_2, p_2, shape=shape2))

# def annotate_four(data, **kws):
#     r_4, p_4 = stats.pearsonr(data['ESI'], data['4in_rolling_mean'])
#     shape4 = data.shape[0]
#     ax = plt.gca()
#     ax.text(-2, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_4, p_4, shape=shape4))

# def annotate_eight(data, **kws):
#     r_8, p_8 = stats.pearsonr(data['ESI'], data['8in_rolling_mean'])
#     shape8 = data.shape[0]
#     ax = plt.gca()
#     ax.text(-2, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_8, p_8, shape=shape8))
 
# def annotate_twenty(data, **kws):
#     r_20, p_20 = stats.pearsonr(data['ESI'], data['20in_rolling_mean'])
#     shape20 = data.shape[0]
#     ax = plt.gca()
#     ax.text(-2, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_20, p_20, shape=shape20))

# def annotate_forty(data, **kws):
#     r_40, p_40 = stats.pearsonr(data['ESI'], data['40in_rolling_mean'])
#     shape40 = data.shape[0]
#     ax = plt.gca()
#     ax.text(-2, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_40, p_40, shape=shape40))
    
# #show all the individual figures so that they can be saved. 
# stations_two.map_dataframe(annotate_two)
# stations_four.map_dataframe(annotate_four)
# stations_eight.map_dataframe(annotate_eight)
# stations_twenty.map_dataframe(annotate_twenty)
# stations_forty.map_dataframe(annotate_forty)

# plt.show()
# plt.tight_layout()



