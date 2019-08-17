"""Script for joining scraped web data with sales data into a dataframe"""

import json
import pandas as pd
import numpy as np
import jsoncleaner
import datetime as dt

if __name__ == '__main__':

    today = str(dt.datetime.today().strftime('%Y%m%d%H%M%S'))

    result = []
    for lot in range(1, 270001):
        infile = "/Users/alehe/Desktop/Nashville/Parcels/parcel{}".format(
            lot)
        with open(infile, 'r') as infile:
            try:
                result.append(json.load(infile))
            except ValueError:
                continue

    df = pd.DataFrame(result)

    sales = pd.read_csv('/Users/alehe/OneDrive/Documents/Jupyter/SharpestMinds/sales.csv')

    jdf = df.merge(sales, right_on='Parcel ID', left_on='Map & Parcel', how='left')
    jdf = jsoncleaner.columnizer(jdf)

    jdf.to_csv('nashville_{}.csv'.format(today), index=False)
