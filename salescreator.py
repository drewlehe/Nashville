#script to combine all Sales datasets into one csv.

import pandas as pd

df2015 = pd.read_csv('sales2015.csv')
df2016 = pd.read_csv('sales2016.csv')
df2017 = pd.read_csv('sales2017.csv')
df2018 = pd.read_csv('sales2018.csv')
df2019 = pd.read_csv('sales2019.csv')

dfmain = df2015.append(df2016)
dfmain= dfmain.append(df2017)
dfmain = dfmain.append(df2018)
dfmain=dfmain.append(df2019)

dfmain.to_csv('sales.csv', index=False)