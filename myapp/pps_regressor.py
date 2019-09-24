'''Contains the function to predict the price of the house, given the selected values in the widget.'''
import numpy as np
import pandas as pd 
import lightgbm as lgb
import json

DENSITIES = {0:"SINGLE FAM", 1: "PLEX"}
SEGMENTS = {0: 'D', 1: 'C', 2: 'B'}

def prediction(input_dict):
    '''Take in the bldg_data dictionary as a json, transform the features and give a price prediction'''
    model = lgb.Booster(model_file='noyear.txt')
    lst = [(input_dict)]
    tester = pd.DataFrame(lst)
    tester['Log-Built'] = np.log(tester['Year Built'])
    tester['Log-SqFt'] = np.log(int(tester['Square Footage']))
    tester['Neighborhood'] = tester['Neighborhood'].astype(float)
    with open('meanpps.json', 'r') as nbhdpps:
        nbhd_dict = json.load(nbhdpps)
    meanpps = pd.DataFrame(nbhd_dict, index=None)
    meanpps.index=meanpps.index.astype(float)
    nbhds = list(meanpps.index)
    tester=pd.merge(how = 'left', left = tester, right = meanpps,left_on="Neighborhood", right_index=True)
    tester['Log-NbhdPPS'] = np.log(tester['NeighborhoodPPS'])
    tester['Neighborhood'] = str(tester['Neighborhood'])
    tester['Building-Grade'] = tester['Building-Grade'].map(lambda x: SEGMENTS[x])
    tester['Building-Type-Custom'] = tester['Building-Type-Custom'].map(lambda x: DENSITIES[x])
    ML = tester[['Year', 'Log-Built', 'Neighborhood',  'Building-Type-Custom', 
                               'Quarter', 'Building-Grade', 'Log-SqFt',
                               'Log-NbhdPPS']]
    with open(f'ml_vars.json', 'r') as file:
        ml_vars = json.load(file)
    data = pd.DataFrame(columns=ml_vars)
    data= pd.concat([ML, data])
    print(data.columns)
    X = pd.get_dummies(data, columns=data.columns, dtype=bool)
#     X.columns = data.columns
#     print(X[:20])
    price_pred = model.predict(data)
    return price_pred