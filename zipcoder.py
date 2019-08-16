import googlemaps
import pandas as pd

API_KEY= 'AIzaSyCZLx_SpRYpdwTFCMFcq8GSOXfOVrEpwuI'
ADDS= df['Location']

if __name__ == '__main__':
    gmaps=googlemaps.Client(key=API_KEY)
    zips = []
    for parcel in ADDS:
        placeresult= gmaps.find_place(input= '{} Nashville, TN'.format(parcel), input_type='textquery',fields=['formatted_address'])
        zipcode=str(placeresult['candidates'])[-13:-8]
        zips.append(zipcode)
    
    def zipper(old_df):
        df=old_df.copy()
        df.insert(1,'Zipcode', '')
        i=0
        for parcel in df['Location']:
            df['Zipcode'].loc[i] = zips[i]
            i+=1
        return df
    