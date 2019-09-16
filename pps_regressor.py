import numpy as np
import pandas as pd 
import lightgbm as lgb
import json

def prediction(bokeh_input):
    print(open(bokeh_input, 'r').read())
    #Take in the settings from the 
    model = lgb.Booster(model_file='model.json')
    with open('selection.json', 'r') as inputfile:
        price_pred = model.predict(inputfile)
    with open('price.json', 'w') as outputfile:
        json.dump(price_pred, outputfile)
    return price_pred


# Example = {'Neighborhood': int(nbhd), 'Building Type Custom': density, 'Fixtures': fixtures, 'Exterior Wall': wall_type,
#            'Building Grade': segment, 'Year Built': int(year_built), 'SqFt Improved':  int(squarefootage)}