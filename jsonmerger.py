import json
import pandas as pd
import numpy as np

if __name__ == '__main__':

    result = []
    for lot in range(1, 270000):
        infile = "/Users/alehe/OneDrive/Documents/Jupyter/SharpestMinds/Parcels/parcel{}".format(lot)
        with open(infile, 'r') as infile:
            try:
                result.append(json.load(infile))
            except ValueError:
                continue

    df = pd.DataFrame(result)

    sales = pd.read_csv('/Users/alehe/OneDrive/Documents/Jupyter/SharpestMinds/sales.csv')

    xdf = pd.read_csv('/Users/alehe/OneDrive/Documents/Jupyter/SharpestMinds/sales.csv')

    jdf = df.merge(xdf, right_on='Parcel ID', left_on='Map & Parcel')

    jdf.to_csv('merged.csv')
