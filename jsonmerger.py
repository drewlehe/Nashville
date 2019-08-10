"""Script for joining scraped web data with sales data into a dataframe"""
import json
import pandas as pd
import numpy as np

if __name__ == '__main__':

    result = []
    for lot in range(180000, 270000):
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

    jdf.to_csv('mergednew.csv')
