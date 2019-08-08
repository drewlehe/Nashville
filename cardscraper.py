import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib3
import requests
import json

if __name__ == '__main__':

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

def get_card_info(online_id):
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

for lot in range(1,270001):
    get_card_info(lot)
