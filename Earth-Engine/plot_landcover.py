#import modules
import pandas as pd
import seaborn as sns
import os

#import data
trees_loc = '..\data\SCANTreeCover'

#create datapath
dp = os.path.join(os.getcwd(), trees_loc)

#create filelist to store all .csvs
filelist = []

#get all the files from the trees_loc to a list:
for root, dirs, files in os.walk(dp):
    for f in files:
        filelist.append(f)

#create a newfile list that will contain whole file paths
new_filelist = []

#create filepaths for every csv
for f in filelist:
    new_filelist.append(os.path.join(dp, f))

#set a storage dictionary
dic = {} 

#store all information in the dictionary
for f in new_filelist:
    read = pd.read_csv(f)
    df = pd.DataFrame(read)
    df['station'] = f[-12:-4]
    df.drop('system:index', axis=1, inplace=True)
    df.drop('.geo', axis=1, inplace=True)
    df.set_index('station', inplace=True)
    dic[f] = df

#concat the dictionary
df = pd.concat(dic)
df = df.droplevel(level=0)


#calculate evergreen mean for 20 years
df['Mean Evergreen Cover'] = (df['Total Evergreen 2001'] + df['Total Evergreen 2004'] 
                        + df['Total Evergreen 2006'] + df['Total Evergreen 2008']
                        + df['Total Evergreen 2011'] + df['Total Evergreen 2013']
                        + df['Total Evergreen 2016'] + df['Total Evergreen 2019']) / 8

#calculate mixed mean for 20 years
df['Mean Mixed Cover'] = (df['Total Mixed 2001'] + df['Total Mixed 2004'] 
                        + df['Total Mixed 2006'] + df['Total Mixed 2008']
                        + df['Total Mixed 2011'] + df['Total Mixed 2013']
                        + df['Total Mixed 2016'] + df['Total Mixed 2019']) / 8

#calculate deciduous cover
df['Mean Deciduous Cover'] = (df['Total Deciduous 2001'] + df['Total Deciduous 2004'] 
                        + df['Total Deciduous 2006'] + df['Total Deciduous 2008']
                        + df['Total Deciduous 2011'] + df['Total Deciduous 2013']
                        + df['Total Deciduous 2016'] + df['Total Deciduous 2019']) / 8

df = df[['Mean Evergreen Cover', 'Mean Mixed Cover', 'Mean Deciduous Cover']]

df.sort_values('Mean Deciduous Cover', inplace=True)
df.reset_index(inplace=True)

#create an order for the mean tree cover plot

melt = pd.melt(df, id_vars='station')
plot = sns.barplot(x='station', y='value', hue='variable', data=melt)
plot.set_xticklabels(labels=df.index, rotation=90)

# #plot mean treecover 
# plot = sns.barplot(x=df.index, y=df['Mean Evergreen Cover'], data=df, order=order.index)
# plot.set_xticklabels(labels=order.index, rotation=90)
# plot.set_title('ALEXI Pixel Tree Cover 2001-2019')

