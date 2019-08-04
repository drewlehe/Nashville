import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib3
import requests
import json
page = requests.get('http://www.padctn.org/services/recent-sales/')
soup = bs(page.text, 'html.parser')
from urllib.request import urlopen, urlretrieve, quote
from openpyxl import Workbook
u = urlopen(site)
try:
    html = u.read().decode('utf-8')
finally:
    u.close()

with open('davidson.csv', 'w', newline='') as csvfile:

    propertyWriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    for link in soup.select('a[href^="http://"]'):
        href = link.get('href')

        # Make sure it has one of the correct extensions
        if not any(href.endswith(x) for x in ['.xls','.xlsx']):
            continue
        if 'comm' in href or 'rural' in href:
            continue
        filename = href.rsplit('/', 2)[-2] + '_' + href.rsplit('/', 2)[-1]
        print("Downloading %s to %s" % (href, filename) )
        urlretrieve(href, filename)
        print("Done.")
        propertyWriter.writerow(link.text)

#Creating a DataFrame and Excel file for each year's data.
import glob
df2019=pd.DataFrame()
df2018=pd.DataFrame()
df2017=pd.DataFrame()
df2016=pd.DataFrame()
df2015=pd.DataFrame()
for f in glob.glob("2019*.xls"):
    df = pd.read_excel(f)
    df2019 = df2019.append(df,ignore_index=True)
    df2019.to_csv(r'sales2019.csv', header=True)
for f in glob.glob("2018*.xls"):
    df = pd.read_excel(f)
    df2018 = df2018.append(df,ignore_index=True)
    df2018.to_csv(r'sales2018.csv', header=True)
for f in glob.glob("2017*.xls"):
    df = pd.read_excel(f)
    df2017 = df2017.append(df,ignore_index=True)
    df2017.to_csv(r'sales2017.csv', header=True)
for f in glob.glob("2016*.xls"):
    df = pd.read_excel(f)
    df2016 = df2016.append(df,ignore_index=True)
    df2016.to_csv(r'sales2016.csv', header=True)
for f in glob.glob("2015*.xls"):
    df = pd.read_excel(f)
    df2015 = df2015.append(df,ignore_index=True)
    df2015.to_csv(r'sales2015.csv', header=True)

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
