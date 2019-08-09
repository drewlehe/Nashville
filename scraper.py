import glob
import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib3
import requests
import json
from urllib.request import urlopen, urlretrieve, quote
from openpyxl import Workbook

if __name__ == '__main__':

    page = requests.get('http://www.padctn.org/services/recent-sales/')
    soup = bs(page.text, 'html.parser')
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
            if not any(href.endswith(x) for x in ['.xls', '.xlsx']):
                continue
            if 'comm' in href or 'rural' in href:
                continue
            filename = href.rsplit('/', 2)[-2] + '_' + href.rsplit('/', 2)[-1]
            print("Downloading %s to %s" % (href, filename))
            urlretrieve(href, filename)
            print("Done.")
            propertyWriter.writerow(link.text)

    # Creating a DataFrame and .csv file from the scraped data.
    dfsales = pd.DataFrame()
    for f in glob.glob("201*.xls"):
        df = pd.read_excel(f)
        dfsales = dfsales.append(df, ignore_index=True)
        dfsales.to_csv(r'sales.csv', header=True)
