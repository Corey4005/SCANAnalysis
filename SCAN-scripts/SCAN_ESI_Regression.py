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

#create rolling averages for each level of soil moisture
sms['2in_rolling_mean'] = sms['SMS-2.0in'].rolling(7, min_periods=3).mean()
sms['4in_rolling_mean'] = sms['SMS-4.0in'].rolling(7, min_periods=3).mean()
sms['8in_rolling_mean'] = sms['SMS-8.0in'].rolling(7, min_periods=3).mean()
sms['20in_rolling_mean'] = sms['SMS-20.0in'].rolling(7, min_periods=3).mean()
sms['40in_rolling_mean'] = sms['SMS-40.0in'].rolling(7, min_periods=3).mean()

#create rolling sums for each level of soil moisture
sms['2in_rolling_sum'] = sms['SMS-2.0in'].rolling(7, min_periods=3).sum()
sms['4in_rolling_sum'] = sms['SMS-4.0in'].rolling(7, min_periods=3).sum()
sms['8in_rolling_sum'] = sms['SMS-8.0in'].rolling(7, min_periods=3).sum()
sms['20in_rolling_sum'] = sms['SMS-20.0in'].rolling(7, min_periods=3).sum()
sms['40in_rolling_sum'] = sms['SMS-40.0in'].rolling(7, min_periods=3).sum()


#create averages for sliced mean data
sms['SMS-all-avg'] = (sms['2in_rolling_mean'] + sms['4in_rolling_mean'] + sms['8in_rolling_mean'] + sms['20in_rolling_mean'] + sms['40in_rolling_mean']) / 5
sms['SMS-2.0+4.0_avg'] = (sms['2in_rolling_mean'] + sms['4in_rolling_mean']) / 2
sms['SMS-4.0+8.0_avg'] = (sms['4in_rolling_mean'] + sms['8in_rolling_mean']) / 2
sms['SMS-8.0+20.0_avg'] = (sms['8in_rolling_mean'] + sms['20in_rolling_mean']) / 2
sms['SMS-20.0+40.0_avg'] = (sms['20in_rolling_mean'] + sms['40in_rolling_mean']) /2

#create averages for sliced sum data
sms['SMS-all-sum'] = (sms['2in_rolling_sum'] + sms['4in_rolling_sum'] + sms['8in_rolling_sum'] + sms['20in_rolling_sum'] + sms['40in_rolling_sum'])
sms['SMS-2.0+4.0-sum'] = (sms['2in_rolling_sum'] + sms['4in_rolling_sum']) 
sms['SMS-4.0+8.0-sum'] = (sms['4in_rolling_sum'] + sms['8in_rolling_sum']) 
sms['SMS-8.0+20.0-sum'] = (sms['8in_rolling_sum'] + sms['20in_rolling_sum']) 
sms['SMS-20.0+40.0-sum'] = (sms['20in_rolling_sum'] + sms['40in_rolling_sum']) 

#create three layers sliced mean data
sms['SMS-2.0+4.0+8.0_avg'] = (sms['2in_rolling_mean'] + sms['4in_rolling_mean'] + sms['8in_rolling_mean']) / 3
sms['SMS-4.0+8.0+20.0_avg'] = (sms['4in_rolling_mean'] + sms['8in_rolling_mean'] + sms['20in_rolling_mean']) / 3
sms['SMS-8.0+20.0+40.0_avg'] = (sms['8in_rolling_mean'] + sms['20in_rolling_mean'] + sms['40in_rolling_mean']) / 3

#create averages for three layers sliced sum data
sms['SMS-2.0+4.0+8.0-sum'] = (sms['2in_rolling_sum'] + sms['4in_rolling_sum'] + sms['8in_rolling_sum']) 
sms['SMS-4.0+8.0+20.0-sum'] = (sms['4in_rolling_sum'] + sms['8in_rolling_sum'] + sms['20in_rolling_sum']) 
sms['SMS-8.0+20.0+40.0-sum'] = (sms['8in_rolling_sum'] + sms['20in_rolling_sum'] + sms['40in_rolling_sum']) 

#subset sms for each single group mean by station
two_in = sms[['station', 'Date', '2in_rolling_mean']]
four_in = sms[['station', 'Date', '4in_rolling_mean']]
eight_in = sms[['station', 'Date', '8in_rolling_mean']]
twenty_in = sms[['station', 'Date', '20in_rolling_mean']]
forty_in = sms[['station', 'Date', '40in_rolling_mean']]

#subset SMS for all data averaged together.
all_avg = sms[['station', 'Date', 'SMS-all-avg']]

#subset sms for each single group sum by station
two_in_sum = sms[['station', 'Date', '2in_rolling_sum']]
four_in_sum = sms[['station', 'Date', '4in_rolling_sum']]
eight_in_sum = sms[['station', 'Date', '8in_rolling_sum']]
twenty_in_sum = sms[['station', 'Date', '20in_rolling_sum']]
forty_in_sum = sms[['station', 'Date', '40in_rolling_sum']]

#subset SMS for all data summed together. 
all_sum = sms[['station', 'Date', 'SMS-all-sum']]

#subset the sms for each two layers sliced mean groups by station
two_in_four_in_avg = sms[['station', 'Date', 'SMS-2.0+4.0_avg']]
four_in_eight_in_avg = sms[['station', 'Date', 'SMS-4.0+8.0_avg']]
eight_in_twenty_in_avg = sms[['station', 'Date','SMS-8.0+20.0_avg']]
twenty_in_forty_in_avg = sms[['station', 'Date', 'SMS-20.0+40.0_avg']]

#subset the sms for each two layers sliced sum groups by station 
two_four_sum = sms[['station', 'Date', 'SMS-2.0+4.0-sum']]
four_eight_sum = sms[['station', 'Date', 'SMS-4.0+8.0-sum',]]
eight_twenty_sum = sms[['station', 'Date', 'SMS-8.0+20.0-sum']]
twenty_forty_sum = sms[['station', 'Date', 'SMS-20.0+40.0-sum']]

#subset the sms for each three layers sliced  mean groups by station
two_four_eight_in_avg = sms[['station', 'Date', 'SMS-2.0+4.0+8.0_avg']]
four_eight_twenty_in_avg = sms[['station', 'Date', 'SMS-4.0+8.0+20.0_avg']]
eight_twenty_forty_in_avg = sms[['station', 'Date', 'SMS-8.0+20.0+40.0_avg']]

#subset the sms for each three layers sliced sum groups by station
two_four_eight_sum = sms[['station', 'Date', 'SMS-2.0+4.0+8.0-sum']]
four_eight_twenty_sum = sms[['station', 'Date', 'SMS-4.0+8.0+20.0-sum']]
eight_twenty_forty_sum = sms[['station', 'Date', 'SMS-8.0+20.0+40.0-sum']]

#merge ESI and SMS on single groups mean
two_in_merge = pd.merge(left=esi, right=two_in, on=['Date', 'station'], how='outer')
four_in_merge = pd.merge(left=esi, right=four_in, on=['Date', 'station'], how='outer')
eight_in_merge = pd.merge(left=esi, right=eight_in, on=['Date', 'station'], how='outer')
twenty_in_merge = pd.merge(left=esi, right=twenty_in, on=['Date', 'station'], how='outer')
forty_in_merge = pd.merge(left=esi, right=forty_in, on=['Date', 'station'], how='outer')

#merge ESI and SMS on all data averaged 
all_avg_merge = pd.merge(left=esi, right=all_avg, on=['Date', 'station'], how='outer')

#merge ESI and SMS on single groups sum 
two_in_sum_merge = pd.merge(left=esi, right=two_in_sum, on=['Date', 'station'], how='outer')
four_in_sum_merge = pd.merge(left=esi, right=four_in_sum, on=['Date', 'station'], how='outer')
eight_in_sum_merge = pd.merge(left=esi, right=eight_in_sum, on=['Date', 'station'], how='outer')
twenty_in_sum_merge = pd.merge(left=esi, right=twenty_in_sum, on=['Date', 'station'], how='outer')
forty_in_sum_merge = pd.merge(left=esi, right=forty_in_sum, on=['Date', 'station'], how='outer')

#merge ESI on SMS and all data summed
all_sum_merge = pd.merge(left=esi, right=all_sum, on=['Date', 'station'], how='outer')

#merge ESI and SMS on two groups mean 
two_in_four_in_merge = pd.merge(left=esi, right=two_in_four_in_avg, on=['Date', 'station'], how='outer')
four_in_eight_in_merge = pd.merge(left=esi, right=four_in_eight_in_avg, on=['Date', 'station'], how='outer')
eight_in_twenty_in_merge = pd.merge(left=esi, right=eight_in_twenty_in_avg, on=['Date', 'station'], how='outer')
twenty_in_forty_in_merge = pd.merge(left=esi, right=twenty_in_forty_in_avg, on=['Date', 'station'], how='outer')

#merge ESI and SMS on two groups summed
two_four_sum_merge = pd.merge(left=esi, right=two_four_sum, on=['Date', 'station'], how='outer')
four_eight_sum_merge = pd.merge(left=esi, right=four_eight_sum, on=['Date', 'station'], how='outer')
eight_twenty_sum_merge = pd.merge(left=esi, right=eight_twenty_sum, on=['Date', 'station'], how='outer')
twenty_forty_sum_merge = pd.merge(left=esi, right=twenty_forty_sum, on=['Date', 'station'], how='outer')

#merge ESI and SMS on three groups mean 
two_four_eight_in_merge = pd.merge(left=esi, right=two_four_eight_in_avg, on=['Date', 'station'], how='outer')
four_eight_twenty_in_merge = pd.merge(left=esi, right=four_eight_twenty_in_avg, on=['Date', 'station'], how='outer')
eight_twenty_forty_in_merge = pd.merge(left=esi, right=eight_twenty_forty_in_avg, on=['Date', 'station'], how='outer')

#merge ESI and SMS on three groups summed 
two_four_eight_sum_merge = pd.merge(left=esi, right=two_four_eight_sum, on=['Date', 'station'], how='outer')
four_eight_twenty_sum_merge = pd.merge(left=esi, right=four_eight_twenty_sum, on=['Date', 'station'], how='outer')
eight_twenty_forty_sum_merge = pd.merge(left=esi, right=eight_twenty_forty_sum, on=['Date', 'station'], how='outer')

#correct the single mean indexes to get rid of ESI values where there is a bad reading and drop all NaNs. 
two_corrected = two_in_merge[two_in_merge['ESI'] != -9999].dropna()
four_corrected = four_in_merge[four_in_merge['ESI'] != -9999].dropna()
eight_corrected = eight_in_merge[eight_in_merge['ESI']!= -9999].dropna()
twenty_corrected = twenty_in_merge[twenty_in_merge['ESI'] != -9999].dropna()
forty_corrected = forty_in_merge[forty_in_merge['ESI'] != -9999].dropna()
all_avg_corrected = all_avg_merge[all_avg_merge['ESI'] != -9999].dropna()


#correct the double mean indexes to get rid of ESI values where there is a bad reading and drop all NaNs. 
two_in_four_in_corrected = two_in_four_in_merge[two_in_four_in_merge['ESI'] != -9999].dropna()
four_in_eight_in_corrected = four_in_eight_in_merge[four_in_eight_in_merge['ESI'] != -9999].dropna()
eight_in_twenty_in_corrected = eight_in_twenty_in_merge[eight_in_twenty_in_merge['ESI'] != -9999].dropna()
twenty_in_forty_in_corrected = twenty_in_forty_in_merge[twenty_in_forty_in_merge['ESI'] != -9999].dropna()

#correct the triple mean indexes to get rid of ESI values where there is a bad reading and drop all NaNs. 
two_four_eight_in_corrected = two_four_eight_in_merge[two_four_eight_in_merge['ESI'] != -9999].dropna()
four_eight_twenty_in_corrected = four_eight_twenty_in_merge[four_eight_twenty_in_merge['ESI'] != -9999].dropna()
eight_twenty_forty_in_corrected = eight_twenty_forty_in_merge[eight_twenty_forty_in_merge['ESI'] != -9999].dropna()

#correct the rolling sum single indexes to get rid of ESI values where there is a bad reading and drop all NaNs.
two_in_sum_corrected = two_in_sum_merge[two_in_sum_merge['ESI'] != -9999].dropna()
four_in_sum_corrected = four_in_sum_merge[four_in_sum_merge['ESI'] != -9999].dropna()
eight_in_sum_corrected = eight_in_sum_merge [eight_in_sum_merge['ESI'] != -9999].dropna()
twenty_in_sum_corrected = twenty_in_sum_merge[twenty_in_sum_merge['ESI'] != -9999].dropna()
forty_in_sum_corrected = forty_in_sum_merge[forty_in_sum_merge['ESI'] != -9999].dropna()

#correct the rolling all sum single index to get rid of ESI values where there is a bad reading and drop all NaNs. 
all_sum_corrected = all_sum_merge[all_sum_merge['ESI'] != -9999].dropna()

#correct the rolling sum double indexes to get rid of ESI values where there is a bad reading and drop all NaNs. 
two_four_sum_corrected = two_four_sum_merge[two_four_sum_merge['ESI'] != -9999].dropna()
four_eight_sum_corrected = four_eight_sum_merge[four_eight_sum_merge['ESI'] != -9999].dropna()
eight_twenty_sum_corrected = eight_twenty_sum_merge[eight_twenty_sum_merge['ESI'] != -9999].dropna()
twenty_forty_sum_corrected = twenty_forty_sum_merge[twenty_forty_sum_merge['ESI'] != -9999].dropna()

#correct the rolling sum triple indexes to get rid of ESI values where there is a bad reading and drop all NaNs
two_four_eight_sum_corrected = two_four_eight_sum_merge[two_four_eight_sum_merge['ESI'] != -9999].dropna()
four_eight_twenty_sum_corrected = four_eight_twenty_sum_merge[four_eight_twenty_sum_merge['ESI'] != -9999].dropna()
eight_twenty_forty_sum_corrected = eight_twenty_forty_sum_merge[eight_twenty_forty_sum_merge['ESI'] != -9999].dropna()

# #create x and y values for each mean group plot.
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

#create the x and y values for each single sum group plot. 
two_in_sum_x = two_in_sum_corrected['ESI']
two_in_sum_y = two_in_sum_corrected['2in_rolling_sum']

four_in_sum_x = four_in_sum_corrected['ESI']
four_in_sum_y = four_in_sum_corrected['4in_rolling_sum']

eight_in_sum_x = eight_in_sum_corrected['ESI']
eight_in_sum_y = eight_in_sum_corrected['8in_rolling_sum']

twenty_in_sum_x = twenty_in_sum_corrected['ESI']
twenty_in_sum_y = twenty_in_sum_corrected['20in_rolling_sum']

forty_in_sum_x = forty_in_sum_corrected['ESI']
forty_in_sum_y = forty_in_sum_corrected['40in_rolling_sum']

all_sum_x = all_sum_corrected['ESI']
all_sum_y = all_sum_corrected['SMS-all-sum']

#create the x and y values for mean two slice group plots. 
two_in_four_in_x = two_in_four_in_corrected['ESI']
two_in_four_in_y = two_in_four_in_corrected['SMS-2.0+4.0_avg']

four_in_eight_in_x = four_in_eight_in_corrected['ESI']
four_in_eight_in_y = four_in_eight_in_corrected['SMS-4.0+8.0_avg']

eight_in_twenty_in_x = eight_in_twenty_in_corrected['ESI']
eight_in_twenty_in_y = eight_in_twenty_in_corrected['SMS-8.0+20.0_avg']

twenty_in_forty_in_x = twenty_in_forty_in_corrected['ESI']
twenty_in_forty_in_y = twenty_in_forty_in_corrected['SMS-20.0+40.0_avg']

#create the x and y values for each two slice sum group plot. 
two_four_sum_x = two_four_sum_corrected['ESI']
two_four_sum_y = two_four_sum_corrected['SMS-2.0+4.0-sum']

four_eight_sum_x = four_eight_sum_corrected['ESI']
four_eight_sum_y = four_eight_sum_corrected['SMS-4.0+8.0-sum']

eight_twenty_sum_x = eight_twenty_sum_corrected['ESI']
eight_twenty_sum_y = eight_twenty_sum_corrected['SMS-8.0+20.0-sum']

twenty_forty_sum_x = twenty_forty_sum_corrected['ESI']
twenty_forty_sum_y = twenty_forty_sum_corrected['SMS-20.0+40.0-sum']

#create the figure subplots based on each level of soil. 
fig, ax = plt.subplots(nrows=1, ncols=6, figsize=(25,10))
fig.suptitle('Alabama SCAN Soil Moisture Stations (SMS) at Different Depths vs Alexi Sattelite Environmental Stress Index (ESI)')

#here is the subplot for two in mean data.
sns.regplot(ax=ax[0], x=two_in_x, y=two_in_y, data='two_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_two = stats.pearsonr(two_in_x, two_in_y)
formated_r_two = ("{:.4f}".format(stats_two[0]))
formated_p_two = ("{:.4f}".format(stats_two[1]))
shape_two = two_corrected.shape[0]
at_two = AnchoredText(s=f"R2: {formated_r_two} \n P: {formated_p_two} \n n: {shape_two}", loc='upper left')
ax[0].add_artist(at_two)
ax[0].set_title('All 2in Mean SMS vs ESI')

#here is the subplot for four inch mean data
sns.regplot(ax=ax[1], x=four_in_x, y=four_in_y, data='four_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_four = stats.pearsonr(four_in_x, four_in_y)
formated_r_four = ("{:.4f}".format(stats_four[0]))
formated_p_four = ("{:.4f}".format(stats_four[1]))
shape_four = four_corrected.shape[0]
at_four = AnchoredText(s=f"R2: {formated_r_four} \n P: {formated_p_four} \n n: {shape_four}", loc='upper left')
ax[1].add_artist(at_four)
ax[1].set_title('All 4in Mean SMS vs ESI')

#here is the subplot for eight inch mean data
sns.regplot(ax=ax[2], x=eight_in_x, y=eight_in_y, data='eight_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_eight = stats.pearsonr(eight_in_x, eight_in_y)
formated_r_eight = ("{:.4f}".format(stats_eight[0]))
formated_p_eight = ("{:.4f}".format(stats_eight[1]))
shape_eight = eight_corrected.shape[0]
at_eight = AnchoredText(s=f"R2: {formated_r_eight} \n P: {formated_p_eight} \n n: {shape_eight}", loc='upper left')
ax[2].add_artist(at_eight)
ax[2].set_title('All 8in Mean SMS vs ESI')

#here is the subplot for twenty inch mean data
sns.regplot(ax=ax[3], x=twenty_in_x, y=twenty_in_y, data='twenty_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_twenty = stats.pearsonr(twenty_in_x, twenty_in_y)
formated_r_twenty = ("{:.4f}".format(stats_twenty[0]))
formated_p_twenty = ("{:.4f}".format(stats_twenty[1]))
shape_twenty = twenty_corrected.shape[0]
at_twenty = AnchoredText(s=f"R2: {formated_r_twenty} \n P: {formated_p_twenty} \n n: {shape_twenty}", loc='upper left')
ax[3].add_artist(at_twenty)
ax[3].set_title('All 20in Mean SMS vs ESI')

#here is the subplot for forty inch mean data
sns.regplot(ax=ax[4], x=forty_in_x, y=forty_in_y, data='forty_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_forty = stats.pearsonr(forty_in_x, forty_in_y)
formated_r_forty = ("{:.4f}".format(stats_forty[0]))
formated_p_forty = ("{:.4f}".format(stats_forty[1]))
shape_forty = forty_corrected.shape[0]
at_forty = AnchoredText(s=f"R2: {formated_r_forty} \n P: {formated_p_forty} \n n: {shape_forty}", loc='upper left')
ax[4].add_artist(at_forty)
ax[4].set_title('All 40in Mean SMS vs ESI')

#here is the subplot for the all levels mean data
sns.regplot(ax=ax[5], x=all_avg_x, y=all_avg_y, data='all_avg_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_all = stats.pearsonr(all_avg_x, all_avg_y)
formated_r_all_avg = ("{:.4f}".format(stats_all[0]))
formated_p_all_avg = ("{:.4f}".format(stats_all[1]))
shape_all_avg = all_avg_corrected.shape[0]
at_all = AnchoredText(s=f"R2: {formated_r_all_avg} \n P: {formated_p_all_avg} \n n: {shape_all_avg}", loc='upper left')
ax[5].add_artist(at_all)
ax[5].set_title('All Depths Mean SMS vs ESI')

#here is the overall plot for the two_slice mean data
fig2, ax2 = plt.subplots(nrows=1, ncols=4, figsize=(25, 10))

#here is the subplot for two_in_four_in data
sns.regplot(ax=ax2[0], x=two_in_four_in_x, y=two_in_four_in_y, data='two_in_four_in_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_slice2 = stats.pearsonr(two_in_four_in_x, two_in_four_in_y)
formated_r_slice2 = ("{:.4f}".format(stats_slice2[0]))
formated_p_slice2 = ("{:.4f}".format(stats_slice2[1]))
shape_slice2 = two_in_four_in_corrected.shape[0]
at_slice2 = AnchoredText(s=f"R2: {formated_r_slice2} \n P: {formated_p_slice2} \n n: {shape_slice2}", loc='upper left')
ax2[0].add_artist(at_slice2)
ax2[0].set_title('2in_4in_slice Mean SMS vs ESI')


#here is the subplot for four_in_eight_in data
sns.regplot(ax=ax2[1], x=four_in_eight_in_x, y=four_in_eight_in_y, data='four_in_eight_in_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_slice4 = stats.pearsonr(four_in_eight_in_x, four_in_eight_in_y)
formated_r_slice4 = ("{:.4f}".format(stats_slice4[0]))
formated_p_slice4 = ("{:.4f}".format(stats_slice4[1]))
shape_slice4 = four_in_eight_in_corrected.shape[0]
at_slice4 = AnchoredText(s=f"R2: {formated_r_slice4} \n P: {formated_p_slice4} \n n: {shape_slice4}", loc='upper left')
ax2[1].add_artist(at_slice4)
ax2[1].set_title('4in_8in_slice Mean SMS vs ESI')

#here is the subplot for forty inch data
sns.regplot(ax=ax2[2], x=eight_in_twenty_in_x, y=eight_in_twenty_in_y, data='eight_in_twenty_in_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_slice8 = stats.pearsonr(eight_in_twenty_in_x, eight_in_twenty_in_y)
formated_r_slice8 = ("{:.4f}".format(stats_slice8[0]))
formated_p_slice8 = ("{:.4f}".format(stats_slice8[1]))
shape_slice8 = eight_in_twenty_in_corrected.shape[0]
at_slice8 = AnchoredText(s=f"R2: {formated_r_slice8} \n P: {formated_p_slice8} \n n: {shape_slice8}", loc='upper left')
ax2[2].add_artist(at_slice8)
ax2[2].set_title('8in_20in_slice Mean SMS vs ESI')

#here is the subplot for forty inch data
sns.regplot(ax=ax2[3], x=twenty_in_forty_in_x, y=twenty_in_forty_in_y, data='twenty_in_forty_in_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_slice20 = stats.pearsonr(twenty_in_forty_in_x, twenty_in_forty_in_y)
formated_r_slice20 = ("{:.4f}".format(stats_slice20[0]))
formated_p_slice20 = ("{:.4f}".format(stats_slice20[1]))
shape_slice20 = twenty_in_forty_in_corrected.shape[0]
at_slice20 = AnchoredText(s=f"R2: {formated_r_slice20} \n P: {formated_p_slice20} \n n: {shape_slice20}", loc='upper left')
ax2[3].add_artist(at_slice20)
ax2[3].set_title('20in_40in_slice Mean SMS vs ESI')

#seting context for the plots.
sns.set_context("paper")
sns.set_style('whitegrid')

#create the three slice plots mean x and y values
two_four_eight_in_x = two_four_eight_in_corrected['ESI']
two_four_eight_in_y = two_four_eight_in_corrected['SMS-2.0+4.0+8.0_avg']

four_eight_twenty_in_x = four_eight_twenty_in_corrected['ESI']
four_eight_twenty_in_y = four_eight_twenty_in_corrected['SMS-4.0+8.0+20.0_avg']

eight_twenty_forty_in_x = eight_twenty_forty_in_corrected['ESI']
eight_twenty_forty_in_y = eight_twenty_forty_in_corrected['SMS-8.0+20.0+40.0_avg']

#create the three slice plots sum x and y values
two_four_eight_sum_x = two_four_eight_sum_corrected['ESI']
two_four_eight_sum_y = two_four_eight_sum_corrected['SMS-2.0+4.0+8.0-sum']

four_eight_twenty_sum_x = four_eight_twenty_sum_corrected['ESI']
four_eight_twenty_sum_y = four_eight_twenty_sum_corrected['SMS-4.0+8.0+20.0-sum']

eight_twenty_forty_sum_x = eight_twenty_forty_sum_corrected['ESI']
eight_twenty_forty_sum_y = eight_twenty_forty_sum_corrected['SMS-8.0+20.0+40.0-sum']

#here is the plot for the overall three slice values. 
fig3, ax3 = plt.subplots(nrows=1, ncols=3, figsize=(15,10))

#here is the plot for the two_four_eight slice
sns.regplot(ax=ax3[0], x=two_four_eight_in_x, y=two_four_eight_in_y, data='two_four_eight_in_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_slice_248 = stats.pearsonr(two_four_eight_in_x, two_four_eight_in_y)
formated_r_slice_248 = ("{:.4f}".format(stats_slice_248[0]))
formated_p_slice_248 = ("{:.4f}".format(stats_slice_248[1]))
shape_slice_248 = two_four_eight_in_corrected.shape[0]
at_slice_248 = AnchoredText(s=f"R2: {formated_r_slice_248} \n P: {formated_p_slice_248} \n n: {shape_slice_248}", loc='upper left')
ax3[0].add_artist(at_slice_248)
ax3[0].set_title('two_four_eight_in Mean slice vs ESI')

#here is the plot for the four_eight_twenty slice
sns.regplot(ax=ax3[1], x=four_eight_twenty_in_x, y=four_eight_twenty_in_y, data='four_eight_twenty_in_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_slice_4820 = stats.pearsonr(four_eight_twenty_in_x, four_eight_twenty_in_y)
formated_r_slice_4820 = ("{:.4f}".format(stats_slice_4820[0]))
formated_p_slice_4820 = ("{:.4f}".format(stats_slice_4820[1]))
shape_slice_4820= four_eight_twenty_in_corrected.shape[0]
at_slice_4820 = AnchoredText(s=f"R2: {formated_r_slice_4820} \n P: {formated_p_slice_4820} \n n: {shape_slice_4820}", loc='upper left')
ax3[1].add_artist(at_slice_4820)
ax3[1].set_title('four_eight_twenty_in Mean slice vs ESI')

#here is the plot for the eight_twenty_forty slice. 
sns.regplot(ax=ax3[2], x=eight_twenty_forty_in_x, y=eight_twenty_forty_in_y, data='eight_twenty_forty_in_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_slice_82040 = stats.pearsonr(eight_twenty_forty_in_x, eight_twenty_forty_in_y)
formated_r_slice_82040 = ("{:.4f}".format(stats_slice_82040[0]))
formated_p_slice_82040 = ("{:.4f}".format(stats_slice_82040[1]))
shape_slice_82040 = eight_twenty_forty_in_corrected.shape[0]
at_slice_82040 = AnchoredText(s=f"R2: {formated_r_slice_82040} \n P: {formated_p_slice_82040} \n n: {shape_slice_82040}", loc='upper left')
ax3[2].add_artist(at_slice_82040)
ax3[2].set_title('eight_twenty_forty_in Mean slice vs ESI')

#here is the overall plot for the sum single groups. 
fig4, ax4 = plt.subplots(nrows=1, ncols=6, figsize=(25, 10))

#here is the plot for the all 2in sum data
sns.regplot(ax=ax4[0], x=two_in_sum_x, y=two_in_sum_y, data='two_in_sum_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_sum2 = stats.pearsonr(two_in_sum_x, two_in_sum_y)
formated_r_sum2 = ("{:.4f}".format(stats_sum2[0]))
formated_p_sum2 = ("{:.4f}".format(stats_sum2[1]))
shape_sum2 = two_in_sum_corrected.shape[0]
at_sum2 = AnchoredText(s=f"R2: {formated_r_sum2} \n P: {formated_p_sum2} \n n: {shape_sum2}", loc='upper left')
ax4[0].add_artist(at_sum2)
ax4[0].set_title('All 2in SMS Sum vs ESI')

#here is the plot for the all 4in sum data
sns.regplot(ax=ax4[1], x=four_in_sum_x, y=four_in_sum_y, data='four_in_sum_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_sum4 = stats.pearsonr(four_in_sum_x, four_in_sum_y)
formated_r_sum4 = ("{:.4f}".format(stats_sum4[0]))
formated_p_sum4 = ("{:.4f}".format(stats_sum4[1]))
shape_sum4 = four_in_sum_corrected.shape[0]
at_sum4 = AnchoredText(s=f"R2: {formated_r_sum4} \n P: {formated_p_sum4} \n n: {shape_sum4}", loc='upper left')
ax4[1].add_artist(at_sum4)
ax4[1].set_title('All 4in SMS Sum vs ESI')

#here is the plot for the all 8in sum data
sns.regplot(ax=ax4[2], x=eight_in_sum_x, y=eight_in_sum_y, data='eight_in_sum_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_sum8 = stats.pearsonr(eight_in_sum_x, eight_in_sum_y)
formated_r_sum8 = ("{:.4f}".format(stats_sum8[0]))
formated_p_sum8 = ("{:.4f}".format(stats_sum8[1]))
shape_sum8 = eight_in_sum_corrected.shape[0]
at_sum8 = AnchoredText(s=f"R2: {formated_r_sum8} \n P: {formated_p_sum8} \n n: {shape_sum8}", loc='upper left')
ax4[2].add_artist(at_sum8)
ax4[2].set_title('All 8in SMS Sum vs ESI')

#here is the plot for all 20in sum data
sns.regplot(ax=ax4[3], x=twenty_in_sum_x, y=twenty_in_sum_y, data='twenty_in_sum_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_sum20 = stats.pearsonr(twenty_in_sum_x, twenty_in_sum_y)
formated_r_sum20 = ("{:.4f}".format(stats_sum20[0]))
formated_p_sum20 = ("{:.4f}".format(stats_sum20[1]))
shape_sum20 = twenty_in_sum_corrected.shape[0]
at_sum20 = AnchoredText(s=f"R2: {formated_r_sum20} \n P: {formated_p_sum20} \n n: {shape_sum20}", loc='upper left')
ax4[3].add_artist(at_sum20)
ax4[3].set_title('All 20in SMS Sum vs ESI')

#here is the plot for all forty in sum data
sns.regplot(ax=ax4[4], x=forty_in_sum_x, y=forty_in_sum_y, data='forty_in_sum_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_sum40 = stats.pearsonr(twenty_in_sum_x, twenty_in_sum_y)
formated_r_sum40 = ("{:.4f}".format(stats_sum40[0]))
formated_p_sum40 = ("{:.4f}".format(stats_sum40[1]))
shape_sum40 = forty_in_sum_corrected.shape[0]
at_sum40 = AnchoredText(s=f"R2: {formated_r_sum40} \n P: {formated_p_sum40} \n n: {shape_sum40}", loc='upper left')
ax4[4].add_artist(at_sum40)
ax4[4].set_title('All 40in SMS Sum vs ESI')

#here is the plot for all sum data averaged together. 
sns.regplot(ax=ax4[5], x=all_sum_x, y=all_sum_y, data='all_sum_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_all_sum = stats.pearsonr(all_sum_x, all_sum_y)
formated_r_all_sum = ("{:.4f}".format(stats_all_sum[0]))
formated_p_all_sum = ("{:.4f}".format(stats_all_sum[1]))
shape_all_sum = all_sum_corrected.shape[0]
at_all_sum = AnchoredText(s=f"R2: {formated_r_all_sum} \n P: {formated_p_all_sum} \n n: {shape_all_sum}", loc='upper left')
ax4[5].add_artist(at_all_sum)
ax4[5].set_title('All Depths SMS Sum vs ESI')

#here is the overall plot for the sum double groups
fig5, ax5 = plt.subplots(nrows=1, ncols=4, figsize=(25, 10))

#here is the double group plot for 2in_4in sum
sns.regplot(ax=ax5[0], x=two_four_sum_x, y=two_four_sum_y, data='two_four_sum_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_two_four_sum = stats.pearsonr(two_four_sum_x, two_four_sum_y)
formated_r_two_four_sum = ("{:.4f}".format(stats_two_four_sum[0]))
formated_p_two_four_sum = ("{:.4f}".format(stats_two_four_sum[1]))
shape_two_four_sum = two_four_sum_corrected.shape[0]
at_two_four_sum = AnchoredText(s=f"R2: {formated_r_two_four_sum} \n P: {formated_p_two_four_sum} \n n: {shape_two_four_sum}", loc='upper left')
ax5[0].add_artist(at_two_four_sum)
ax5[0].set_title('2in_4in slice Sum vs ESI')

#here is the double group plot for 4in_8in sum
sns.regplot(ax=ax5[1], x=four_eight_sum_x, y=four_eight_sum_y, data='four_eight_sum_corrected', scatter_kws={'s':2}, line_kws={'color': 'black'})
stats_four_eight_sum = stats.pearsonr(four_eight_sum_x, four_eight_sum_y)
formated_r_four_eight_sum = ("{:.4f}".format(stats_four_eight_sum[0]))
formated_p_four_eight_sum = ("{:.4f}".format(stats_four_eight_sum[1]))
shape_four_eight_sum = four_eight_sum_corrected.shape[0]
at_two_four_sum = AnchoredText(s=f"R2: {formated_r_four_eight_sum} \n P: {formated_p_four_eight_sum} \n n: {shape_four_eight_sum}", loc='upper left')
ax5[1].add_artist(at_two_four_sum)
ax5[1].set_title('4in_8in slice Sum vs ESI')

# #lets try a grid plot to look at individual station stats for each depth. 
variable_y = 1.0

#here are the individual stations for single group means 
stations_two = sns.lmplot(x='ESI', y='2in_rolling_mean', data=two_corrected, col='station', height=6, col_wrap=3)
stations_two.fig.suptitle('ESI (y-axis) by Individual Alabama USDA 2in SMS (x-axis)', y=variable_y)

stations_four = sns.lmplot(x='ESI', y='4in_rolling_mean', data=four_corrected, col='station', height=6, col_wrap=3)
stations_four.fig.suptitle('ESI (y-axis) by Individual Alabama USDA 4in SMS (x-axis)', y=variable_y)

stations_eight = sns.lmplot(x='ESI', y='8in_rolling_mean', data=eight_corrected, col='station', height=6, col_wrap=3)
stations_eight.fig.suptitle('ESI (y-axis) by Individual Alabama USDA 8in SMS (x-axis)', y=variable_y)

stations_twenty = sns.lmplot(x='ESI', y='20in_rolling_mean', data=twenty_corrected, col='station', height=6, col_wrap=3)
stations_twenty.fig.suptitle('ESI (y-axis) by Individual Alabama USDA 20in SMS (x-axis)', y=variable_y)

stations_forty = sns.lmplot(x='ESI', y='40in_rolling_mean', data=forty_corrected, col='station', height=6, col_wrap=3)
stations_forty.fig.suptitle('ESI (y-axis) by Individual Alabama USDA 40in SMS (x-axis)', y=variable_y)

stations_all = sns.lmplot(x='ESI', y='SMS-all-avg', data=all_avg_corrected, col='station', height=6, col_wrap=3)
stations_all.fig.suptitle('ESI (y-axis) by Individual Alabama USDA all-depths avg SMS (x-axis)', y=variable_y)

#here are the individual stations for double group means 
stations_two_four = sns.lmplot(x='ESI', y='SMS-2.0+4.0_avg', data=two_in_four_in_corrected, col='station', height=6, col_wrap=3)
stations_two_four.fig.suptitle('ESI (y-axis) by Individual Alabama USDA two_in_four_in slice avg SMS (x-axis)', y=variable_y)

stations_four_eight = sns.lmplot(x='ESI', y='SMS-4.0+8.0_avg', data=four_in_eight_in_corrected, col='station', height=6, col_wrap=3)
stations_four_eight.fig.suptitle('ESI (y-axis) by Individual Alabama USDA four_in_eight_in slice avg SMS (x-axis)', y=variable_y)

stations_eight_twenty = sns.lmplot(x='ESI', y='SMS-8.0+20.0_avg', data=eight_in_twenty_in_corrected, col='station', height=6, col_wrap=3)
stations_eight_twenty.fig.suptitle('ESI (y-axis) by Individual Alabama USDA eight_in_twenty_in slice avg SMS (x-axis)', y=variable_y)

stations_twenty_forty = sns.lmplot(x='ESI', y='SMS-20.0+40.0_avg', data=twenty_in_forty_in_corrected, col='station', height=6, col_wrap=3)
stations_twenty_forty.fig.suptitle('ESI (y-axis) by Individual Alabama USDA twenty_in_forty_in slice avg SMS (x-axis)', y=variable_y)

#here are the individual stations for triple group means
stations_two_four_eight = sns.lmplot(x='ESI', y='SMS-2.0+4.0+8.0_avg', data=two_four_eight_in_corrected, col='station', height=6, col_wrap=3)
stations_two.fig.suptitle('ESI (y-axis) by Individual Alabama USDA two_four_eight_in slice SMS (x-axis)', y=variable_y)

stations_four_eight_twenty = sns.lmplot(x='ESI', y='SMS-4.0+8.0+20.0_avg', data=four_eight_twenty_in_corrected, col='station', height=6, col_wrap=3)
stations_two.fig.suptitle('ESI (y-axis) by Individual Alabama USDA four_eight_twenty_in slice SMS (x-axis)', y=variable_y)

stations_eight_twenty_forty = sns.lmplot(x='ESI', y='SMS-8.0+20.0+40.0_avg', data=eight_twenty_forty_in_corrected, col='station', height=6, col_wrap=3)
stations_two.fig.suptitle('ESI (y-axis) by Individual Alabama USDA eight_twenty_forty_in slice SMS (x-axis)', y=variable_y)





#create the figure functons to annotate the appropriate stats for each graph. 
def annotate_two(data, **kws):
    ax = plt.gca()
    r_2, p_2 = stats.pearsonr(data['ESI'], data['2in_rolling_mean'])
    shape2 = data.shape[0]
    ax.text(-2.5, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_2, p_2, shape=shape2))


def annotate_four(data, **kws):
    r_4, p_4 = stats.pearsonr(data['ESI'], data['4in_rolling_mean'])
    shape4 = data.shape[0]
    ax = plt.gca()
    ax.text(-2.5, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_4, p_4, shape=shape4))

def annotate_eight(data, **kws):
    r_8, p_8 = stats.pearsonr(data['ESI'], data['8in_rolling_mean'])
    shape8 = data.shape[0]
    ax = plt.gca()
    ax.text(-2.5, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_8, p_8, shape=shape8))
 
def annotate_twenty(data, **kws):
    r_20, p_20 = stats.pearsonr(data['ESI'], data['20in_rolling_mean'])
    shape20 = data.shape[0]
    ax = plt.gca()
    ax.text(-2.5, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_20, p_20, shape=shape20))

def annotate_forty(data, **kws):
    r_40, p_40 = stats.pearsonr(data['ESI'], data['40in_rolling_mean'])
    shape40 = data.shape[0]
    ax = plt.gca()
    ax.text(-2.5, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_40, p_40, shape=shape40))
    
def annotate_all(data, **kws):
    r_all, p_all = stats.pearsonr(data['ESI'], data['SMS-all-avg'])
    shapeall = data.shape[0]
    ax = plt.gca()
    ax.text(-2.5, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_all, p_all, shape=shapeall))
    
def annotate_two_four(data, **kws):
    r_two_four, p_two_four = stats.pearsonr(data['ESI'], data['SMS-2.0+4.0_avg'])
    shape_two_four = data.shape[0]
    ax = plt.gca()
    ax.text(-2.5, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_two_four, p_two_four, shape=shape_two_four))
    
def annotate_four_eight(data, **kws):
    r_four_eight, p_four_eight = stats.pearsonr(data['ESI'], data['SMS-4.0+8.0_avg'])
    shape_four_eight = data.shape[0]
    ax = plt.gca()
    ax.text(-2.5, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_four_eight, p_four_eight, shape=shape_four_eight))

def annotate_eight_twenty(data, **kws):
    r_eight_twenty, p_eight_twenty = stats.pearsonr(data['ESI'], data['SMS-8.0+20.0_avg'])
    shape_eight_twenty = data.shape[0]
    ax = plt.gca()
    ax.text(-2.5, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_eight_twenty, p_eight_twenty, shape=shape_eight_twenty))
    
def annotate_twenty_forty(data, **kws):
    r_twenty_forty, p_twenty_forty = stats.pearsonr(data['ESI'], data['SMS-20.0+40.0_avg'])
    shape_twenty_forty = data.shape[0]
    ax = plt.gca()
    ax.text(-2.5, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_twenty_forty, p_twenty_forty, shape=shape_twenty_forty))

def annotate_two_four_eight(data, **kws):
    r_two_four_eight, p_two_four_eight = stats.pearsonr(data['ESI'], data['SMS-2.0+4.0+8.0_avg'])
    shape_two_four_eight = data.shape[0]
    ax = plt.gca()
    ax.text(-2.5, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_two_four_eight, p_two_four_eight, shape=shape_two_four_eight))

def annotate_four_eight_twenty(data, **kws):
    r_four_eight_twenty, p_four_eight_twenty = stats.pearsonr(data['ESI'], data['SMS-4.0+8.0+20.0_avg'])
    shape_four_eight_twenty = data.shape[0]
    ax = plt.gca()
    ax.text(-2.5, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_four_eight_twenty, p_four_eight_twenty, shape=shape_four_eight_twenty))
    
def annotate_eight_twenty_forty(data, **kws):
    r_eight_twenty_forty, p_eight_twenty_forty = stats.pearsonr(data['ESI'], data['SMS-8.0+20.0+40.0_avg'])
    shape_eight_twenty_forty = data.shape[0]
    ax = plt.gca()
    ax.text(-2.5, 50, s='r={:.4f}, \n p={:.4g},\n n={shape}'.format(r_eight_twenty_forty, p_eight_twenty_forty, shape=shape_eight_twenty_forty))
    
#show all the individual figures so that they can be saved. 
stations_two.map_dataframe(annotate_two)
stations_four.map_dataframe(annotate_four)
stations_eight.map_dataframe(annotate_eight)
stations_twenty.map_dataframe(annotate_twenty)
stations_forty.map_dataframe(annotate_forty)
stations_all.map_dataframe(annotate_all)
stations_two_four.map_dataframe(annotate_two_four)
stations_four_eight.map_dataframe(annotate_four_eight)
stations_eight_twenty.map_dataframe(annotate_eight_twenty)
stations_twenty_forty.map_dataframe(annotate_twenty_forty)
stations_two_four_eight.map_dataframe(annotate_two_four_eight)
stations_four_eight_twenty.map_dataframe(annotate_four_eight_twenty)
stations_eight_twenty_forty.map_dataframe(annotate_eight_twenty_forty)

fig.savefig('All_2slice_SMS+ESI.pdf')
fig2.savefig('All_3slice_SMS+ESI.pdf')
stations_two.savefig('stations_two.pdf')
stations_four.savefig('stations_four.pdf')
stations_eight.savefig('stations_eight.pdf')
stations_twenty.savefig('stations_twenty.pdf')
stations_forty.savefig('stations_forty.pdf')
stations_two_four.savefig('stations_two_four.pdf')
stations_four_eight.savefig('stations_four_eight.pdf')
stations_eight_twenty.savefig('stations_eight_twenty.pdf')
stations_twenty_forty.savefig('stations_twenty_forty.pdf')
stations_two_four_eight.savefig('stations_two_four_eight.pdf')
stations_four_eight_twenty.savefig('stations_four_eight_twenty.pdf')
stations_eight_twenty_forty.savefig('stations_eight_twenty_forty.pdf')

plt.show()



