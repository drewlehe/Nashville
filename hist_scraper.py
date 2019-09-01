'''Scraping historical sales data for each lot'''

import re
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import json
import sys

def get_history(page):
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    address = "http://www.padctn.org/prc/property/{}/card/1/historical".format(lot)
    card = requests.get(address, headers=HEADERS)
    cardsoup = bs(card.text, 'html.parser')
    tds = cardsoup.findAll('table')[0].findAll('td')
    detail = cardsoup.find('h2').text
    pmatch = re.search(r'\d', detail)
    loc = pmatch.start()
    mapid = detail[loc:]
    dates=[]
    amounts = []
    for item in tds:
        match = re.match(r'(\d+/\d+/\d+)',str(item.text))
        if match is not None:
            dates.append(match.group())
        if '$' not in str(item):
            continue
        else:
            amounts.append(str(item.text))
    if dates:
        websters = dict(zip(dates, amounts))
    else:
        websters = {}
        websters['Map & Parcel'] = mapid
    with open('Historicals/parcel{}.json'.format(lot), 'w') as file:
            json.dump(websters, file)

if __name__ == '__main__':

    bottom = int(sys.argv[1])
    top = int(sys.argv[2])+1
    for lot in range(bottom, top):
        get_history(lot)    
