'''Contains the function to predict the price of the house, given the selected values in the widget.'''
import numpy as np
import pandas as pd 
import lightgbm as lgb
import json

DENSITIES = {0:"SINGLE FAM", 1: "PLEX"}
SEGMENTS = {0: 'D', 1: 'C', 2: 'B'}
QUARTERS = {0: '1', 1: '2', 2: '3', 3: '4'}

def prediction(input_dict):
    '''Take in the bldg_data dictionary as a json, transform the features and give a price prediction'''
    #Load trained ML model
    model = lgb.Booster(model_file='pps-model.txt')
    lst = [(input_dict)]
    tester = pd.DataFrame(lst)
    tester['Log-Built'] = np.log(tester['Year Built'])
    tester['Log-SqFt'] = np.log(int(tester['Square Footage']))
    #Grab the average price per square foot in each neighborhood, add it to DataFrame
    with open('meanpps.json', 'r') as nbhdpps:
        nbhd_dict = json.load(nbhdpps)
    meanpps = pd.DataFrame(nbhd_dict, index=None)
    meanpps.index=meanpps.index.astype(str)
    nbhds = [str(int(float(i))) for i in meanpps.index]
    tester=pd.merge(how = 'left', left = tester, right = meanpps, left_on="Neighborhood", right_index=True)
    #Transform some columns and create some new columns
    tester['Log-NbhdPPS'] = np.log(tester['NeighborhoodPPS'])
    tester['Building-Grade'] = tester['Building-Grade'].map(lambda x: SEGMENTS[x])
    tester['Building-Type-Custom'] = tester['Building-Type-Custom'].map(lambda x: DENSITIES[x])
    tester['Quarter'] = tester['Quarter'].map(lambda x: QUARTERS[x])
    tester['Year']=2019
    ML = tester[['Year', 'Log-Built', 'Neighborhood', 'Building-Type-Custom', 
                 'Quarter', 'Building-Grade', 'Log-SqFt', 'Log-NbhdPPS']]
    dummies = pd.get_dummies(ML)
    #Grab column names/order for the dummy variables
    with open(f'ml_vars.json', 'r') as file:
        ml_vars = json.load(file)
    data = pd.DataFrame(columns=ml_vars)
    data['Year']=data['Year'].astype(int)
    data[['Log-SqFt', 'Log-NbhdPPS', 'Log-Built']] = data[['Log-SqFt', 'Log-NbhdPPS', 'Log-Built']].astype(float)
    X=pd.concat([data,dummies], axis=0, sort=True)
    X.fillna(value=0, inplace=True)
    #Put columns in correct order
    X = X[ml_vars]
    price_pred = model.predict(X)
    return price_pred