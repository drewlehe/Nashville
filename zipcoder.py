'''Adding zip codes from Google Maps to the dataframe'''
import googlemaps
import pandas as pd

# with open(r'C:\Users\alehe\OneDrive\Documents\google api key.txt',encoding='utf-8') as file:
#     API_KEY = file.read()


def zipper(old_df):
    df = old_df.copy()
    df.insert(1, 'Zipcode', '')
    API_KEY='AIzaSyCZLx_SpRYpdwTFCMFcq8GSOXfOVrEpwuI' 
    gmaps = googlemaps.Client(key=API_KEY)
    zips = []
    ADDS = df['Location']
    for parcel in ADDS:
        placeresult = gmaps.find_place(input='{} Nashville, TN'.format(
            parcel), input_type='textquery', fields=['formatted_address'],location_bias = 'circle:1000@36.16589, -86.78444')
        zipcode = str(placeresult['candidates'])[-13:-8]
        zips.append(zipcode)
    i = 0
    for parcel in df['Location']:
        df['Zipcode'].loc[i] = zips[i]
        i += 1
    return df



    
