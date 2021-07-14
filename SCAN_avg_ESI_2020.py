import pandas as pd
import seaborn as sns
from scipy import stats


# Read in the ESI data
esi_path = 'C:/Users/cwalker/Desktop/Data/Processed_ESI/ESI_1wk_tif2select_pt.csv'
esi = pd.read_csv(esi_path)
esi['Date'] = pd.to_datetime(esi['Date'])

# # put in the scan_path!
scan_path = 'C:/Users/cwalker/Desktop/Data/SCAN_Data/SCAN_DEPTHS_ALL.csv'
scan = pd.read_csv(scan_path)


# # Just get the columns we are interested in
sms = scan[['Date', 'station','SMS-2.0in', 'SMS-4.0in', 'SMS-8.0in', 'SMS-20.0in','SMS-40.0in']]

# # Date column to datetime format
sms['Date'] = pd.to_datetime(sms['Date'])

#group the dataframe by station and date and agrigate the mean and count for each group.
sms_grp = sms.groupby(['station', pd.Grouper(key='Date', freq='W-WED')]).agg(['mean', 'count'])


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

x = corrected['ESI']
y = corrected['SMS-2.0in_mean']

#seaborn plots
#plot = sns.regplot(x = x_values, y = y_values, 
#                   scatter_kws={'s':2}, color='red', line_kws={'color': 'black'})


plot = sns.regplot(x, y, scatter_kws={'s':2}, line_kws={'color': 'black'})
stats = stats.pearsonr(x, y)
r2 = stats[0]
p_value = stats[1]
format_r2 = '{0:.3f}'.format(r2)
format_p = '{0:6f}'.format(p_value)
plot.text(-3.46, 57,
          s="R^2:{}, p_value:{}".format('' + str(format_r2), '' + str(format_p)))



#matplotlib plots
# x = corrected['ESI']
# y = corrected['SMS-2.0in_mean']

# plt.xlabel('ESI')
# plt.ylabel('SMS-Mean-2.0')

# plt.title('ESI vs SMS')

# plt.show()





