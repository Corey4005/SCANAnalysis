#import modules
import pandas as pd
import seaborn as sns
import os

#import data
trees_loc = '../data/SCANTreeCover'

#create datapath
dp = os.path.join(os.getcwd(), trees_loc)
#create filelist to store all .csvs
filelist = []

#get all the files from the trees_loc to a list:
for root, dirs, files in os.walk(trees_loc):
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
print(df.columns)


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

#get a tree cover dataset for each station
df = df[['Mean Evergreen Cover', 'Mean Mixed Cover', 'Mean Deciduous Cover', 'Mean Tree Cover']]

#rename the 'Mean Tree Cover" coloumn to something more appropriate
df.rename(columns={'Mean Tree Cover':'Total Tree Cover'}, inplace=True)
df.reset_index(inplace=True)

#save the data to the correct filepath
dataloc = '../data'
dataloc = os.path.join(os.getcwd(), dataloc)
df.to_csv(dataloc + '/'+ 'tree_cover_by_station_pixel.csv')
