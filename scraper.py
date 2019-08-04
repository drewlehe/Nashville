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

nupage = requests.get('http://www.padctn.org/prc/property/170000/print')
nusoup = bs(nupage.text, 'html.parser')
print(nusoup.prettify())

results = nusoup.find_all('ul', class_='att')
subsoup = [lst.text for result in results for lst in result.find_all('li')]
souplst=[]
for result in results:
    for lst in result.find_all('li'):
        souplst.append(lst.text)
#print(souplst)
#subsoup=results.find_all('li')
nuresults = list(results[4:])
nucols= []
for result in nuresults:
    nucols.append(result.text)

cardframe = pd.DataFrame()
for col in nucols:
    cardframe[col]= col
#If I do this as a list comprehension, cardframe[col] = [col for col in nucols], I get a transposed list for some reason.
print(type(subsoup))
maindf=pd.DataFrame()
mainlst= []
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
for lot in range(152802,155001):
    address = "http://www.padctn.org/prc/property/{}/print".format(lot)
    nulist=[]
    card = requests.get(address, headers=headers)
    cardsoup = bs(card.text, 'html.parser')
    results = cardsoup.find_all('ul', class_='att')
    subsoup = [lst.text for result in results for lst in result.find_all('li')]
    keys=[]
    values=[]
    for string in subsoup:
        if ':' not in string:
            continue
        else:
            values.append(string.split(':')[1].strip())
            keys.append(string.split(':')[0].strip())
    websters= dict(zip(keys,values))
    with open('Parcels/parcel{}'.format(lot), 'w') as file:
        json.dump(websters, file)
    mainlst.append(websters)
