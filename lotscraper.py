'''Script for downloading the historical sales from each parcel and data from each parcel's property card on padctn.org'''

import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib3
import requests
import json
import sys
import re

HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

def get_card_info(online_id):
    #Scrape the data from each parcel's "property card," then store it in Parcels folder
    address = "http://www.padctn.org/prc/property/{}/print".format(lot)
    nulist = []
    card = requests.get(address, headers=HEADERS)
    cardsoup = bs(card.text, 'html.parser')
    results = cardsoup.find_all('ul', class_='att')
    subsoup = [lst.text for result in results for lst in result.find_all('li')]
    keys = []
    values = []
    for string in subsoup:
        if ':' not in string:
            continue
        else:
            values.append(string.split(':')[1].strip())
            keys.append(string.split(':')[0].strip())
    websters = dict(zip(keys, values))
    with open('Parcels/parcel{}'.format(lot), 'w') as file:
        json.dump(websters, file)

def get_history(online_id):
    #Scrape the historical sales data for each property, then store it in Historicals folder
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
        websters['Map & Parcel'] = mapid
    else:
        websters = {}
        websters['Map & Parcel'] = mapid
    with open('Historicals/parcel{}.json'.format(lot), 'w') as file:
            json.dump(websters, file)
        
        
if __name__ == '__main__':

    bottom = int(sys.argv[1])
    top = int(sys.argv[2])+1
    for lot in range(bottom, top):
        get_card_info(lot)
        get_history(lot)
