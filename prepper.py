'''script to prep data in my SharpestMinds project'''

import numpy as np
import pandas as pd 
import sys

def correct(df_old):
    '''Correcting incorrectly-entered data'''
    df=df_old.copy()
    df.loc[176025, 'Sale Price'] = 37000
    df.loc[27056, 'Sale Price'] = 161000
    df.loc[191004, 'Sale Price'] = 810000
    df.loc[239278, 'Sale Price'] = 280395
    df.loc[138891, 'Sale Price'] = 200000
    df.loc[241961, 'Sale Date'] = '2019-03-04'
    df.loc[241961, 'Sale Date'] = pd.to_datetime(df.loc[241961, 'Sale Date'])
    df.loc[241961, 'Sale Price'] = 370000
    df.loc[230115, 'Sale Price'] = 325000
    df.loc[53151, 'Sale Price'] = 310900
    df.loc[259815, 'Sale Price'] = 1513142
    df.loc[129682, 'Sale Price'] = 1300000
    df.loc[154271, 'Square Footage Improved'] = 10094
    df.drop(190142, inplace=True) #Has a massive ADU ~4 times the size of the 'main' structure. Main struct is low-grade, ADU is luxury.
    df.drop(128094, inplace=True) #Can't find out anything about this house. Improbably large sqft and acreage, low price.
    return df

def clean(df_old):
    '''Drop redundant rows, dirty data, create some new transformed columns'''
    #Creating new dataframe without duplicate entires
    df=df_old.sort_values(by='Sale Date').drop_duplicates(subset='Map & Parcel', keep = 'last')
    #Dropping parcels that were involved in multi-parcel sales
    df=df[df['Multiple Parcels Involved in Sale'] == 'No']
    #Want to create a new column which is the mean sale price per square foot of a parcel in that neighborhood
    df['PPS']=df['Sale Price']/df['Square Footage Improved']
    df['PPS']=df['PPS'].replace(np.inf, np.nan)
    meanpps=df.groupby('Neighborhood')['PPS'].mean().to_frame().rename(columns={'PPS':'NeighborhoodPPS'})
    df=df.merge(meanpps, how='left', left_on = 'Neighborhood',right_index=True)
    #Testing the averaged assessment ratio idea.
    df['Assessment Ratio'] = df['Assessment Land Improved'] / df['Total Appraisal Value Improved']
    nbhdratio=df.groupby('Neighborhood')['Assessment Ratio'].mean().to_frame().rename(columns={'Assessment Ratio':'Nbhd Ratio'})
    df=df.merge(nbhdratio, how='left', left_on = 'Neighborhood',right_index=True)
    df['Month']= df['Sale Date'].dt.month
    df['Quarter'] = df['Sale Date'].dt.quarter
    df['Year'] = df['Sale Date'].dt.year
    df.Quarter= df.Quarter.map(lambda x: str(x) if pd.notnull(x) else '')
    df['Building Grade']= df['Building Grade'].str.replace(r'\w\w\w', '').dropna()
    return df

def transform(df_old):
    '''Log-transforming several numerical features'''
    df= df_old.copy()
    #Log-transforming features because they're heavily right-skewed
    df['Log Assessment']= df['Assessment Land Improved'].map(lambda x: np.log(x) if (pd.notnull(x) and x != 0) else None).replace(np.inf, np.nan)
    df['Log Fixtures']= df['Fixtures'].map(lambda x: np.log(x) if (pd.notnull(x) and x != 0) else None).replace(np.inf, np.nan)
    df['Log SqFt']= df['Square Footage Improved'].map(lambda x: np.log(x) if (pd.notnull(x) and x != 0) else None).replace(np.inf, np.nan)
    df['Log PPS']= df['PPS'].map(lambda x: np.log(x) if (pd.notnull(x) and x != 0) else None).replace(np.inf, np.nan)
    df['Log Land']= df['Land Area Acres'].map(lambda x: np.log(x) if (pd.notnull(x) and x != 0) else None).replace(np.inf, np.nan)
    df['Log NbhdPPS']= df['NeighborhoodPPS'].map(lambda x: np.log(x) if (pd.notnull(x) and x != 0) else None).replace(np.inf, np.nan)
    df['Log NbhdRatio']= df['Nbhd Ratio'].map(lambda x: np.log(x) if (pd.notnull(x) and x != 0) else None).replace(np.inf, np.nan)
    #Doing a log(n-x) transform, then raising to the 1.5 power because heavily left-skewed
    df['Log Built']= df['Year Built'].map(lambda x: np.log(2020-x)**1.5 if (pd.notnull(x) and x != 0) else None).replace(np.inf,np.nan)
    return df

def prep(df_old):
    '''Combine all previous functions to the DataFrame and return it cleaned-up'''
    df = pd.read_csv('{}'.format(df_old),index_col=0,low_memory=False, parse_dates = ['Most Recent Sale Date', 'Sale Date'], dtype={'Zone': str, 'Neighborhood': str})
    df = correct(df)
    df = clean(df)
    df = transform(df)
    return df

if __name__ == '__main__':
    df = prep(sys.arg[1])
    
