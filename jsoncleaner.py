'''File for cleaning up the DataFrame comprised of the json files downloaded from the webscraper.'''

import json
import pandas as pd
import numpy as np
import googlemaps
import os
import re

API_KEY = os.getenv('PlacesAPIKey')

STORYDICT = {'TWO': 2, 'ONE': 1, 'TWO': 2, 'THREE': 3,
             'SPLIT-LEVEL': 1.5, 'BI-LEVEL': 2, 'BSMT HOUSE': 1, '': ''}

TYPEDICT = {'HIGHRISE APT': 'CONDO', 'APARTMENT': 'CONDO', 'HRISE CONDO': 'CONDO',
            'RESD CONDO': 'CONDO', 'RW SING FAM': 'SINGLE FAM', 'SINGLE FAM': 'SINGLE FAM',
            'RZ SING FAM': 'SINGLE FAM', 'RH SING FAM': 'SINGLE FAM',
            'RY SING FAM': 'SINGLE FAM', 'MODULAR HOME': 'SINGLE FAM',
            'SING FAM': 'SINGLE FAM', 'RESD TRIPLEX': 'PLEX', 'RESD QUADPLX': 'PLEX',
            'R1 DUPLEX': 'PLEX', 'RES DUPLEX': 'PLEX', 'LODGE/FRAT\'L': 'THIRD',
            'CHURCH': 'THIRD', 'HEALTH CLUB': 'COMM', 'GROCERY/SMKT': 'COMM',
            'RETAIL/SHPG': 'COMM', 'DAYCARE': 'COMM', 'MARKET': 'COMM',
            'REST/BAR': 'COMM', 'OFFICE': 'OFFICE', 'WAREHOUSE': 'INDUSTRIAL',
            'EQUIP SHED': 'INDUSTRIAL', 'SERV GARAGE': 'INDUSTRIAL', 'TRUCK TERM': 'INDUSTRIAL',
            'ZERO LOT': 'VACANT', 'CAR WASH': 'COMM', 'MED OFC': 'OFFICE',
            'LAUNDRY': 'COMM', 'AUDITORIUM': 'THIRD', 'BANK': 'COMM', 'BOWLING': 'COMM',
            'BUSINESS CTR': 'COMM', 'CINEMA': 'COMM', 'CLUB/UNION': "THIRD",
            "COMM GRNHSE": "INDUSTRIAL", 'WHSE RETAIL': 'COMM', 'ENG/RESEARCH': 'OFFICE',
            'COUNTRY CLUB': 'THIRD', 'DEPT STORE': 'RETAIL', 'TENNIS': 'THIRD',
            'WALKUP APT': 'CONDO', 'DRUG STORE': 'COMM', 'DISC STORE': 'COMM',
            'ELDERLY HSG': 'CONDO', "FUNERAL HM": "THIRD", 'SALES SHOWRM': 'COMM',
            'LUMBER': 'INDUSTRIAL', 'MANF PLANT': 'INDUSTRIAL', 'MAINT HANGER': 'INDUSTRIAL',
            'MOTEL': 'COMM', 'MINI-LUBE': 'INDUSTRIAL', 'MINI-WAREHSE': 'INDUSTRIAL',
            'FAST FOOD': 'COMM', 'HOTEL': 'COMM', 'NURSING HOME': 'CONDO', "PARK'G GAR": 'COMM',
            'SERV STATION': 'COMM', 'INDOOR WP': 'COMM', 'HOSPITAL': 'THIRD', 'T-HANGER': 'INDUSTRIAL'
            }

gmaps = googlemaps.Client(key=API_KEY)

COLS = ['Assessment Classification*', 'Assessment Improvement',
       'Assessment Land', 'Assessment Total', 'Assessment Year', 'Baths', 'Baths2'
       'Beds','Beds2', 'Building Condition','Building Condition2', 'Building Grade','Building Grade2', 'Building Type',
       'Building Type2',
       'Current Owner', 'Deed Reference', 'Exterior Wall','Exterior Wall2', 'Fixtures','Fixtures2',
       'Foundation Type','Foundation Type2', 'Frame Type', 'Half Bath', 'Half Bath2', 'Improvement Value',
       'Land Area', 'Land Value', 'Location', 'Mailing Address',
       'Map & Parcel', 'Most Recent Sale Date', 'Most Recent Sale Price',
       'Neighborhood', 'Number of Living Units', 'Roof Cover', 'Rooms','Rooms2',
       'Square Footage','Square Footage2', 'Story Height', 'Story Height2', 'Tax District',
       'Total Appraisal Value', 'Year Built','Year Built2', 'Zone', 'Parcel ID', 'Land Use',
       'Property Address', 'Suite/ Condo   #', 'Property City', 'Sale Date',
       'Sale Price', 'Legal Reference', 'Sold As Vacant',
       'Multiple Parcels Involved in Sale', 'Assessment Improvement Improved',
       'Most Recent Sale Price Improved', 'Improvement Value Improved',
       'Assessment Total Improved', 'Land Value Improved',
       'Assessment Land Improved', 'Total Appraisal Value Improved',
       'Square Footage Improved', 'Building Type Custom', 'Land Area Acres']

def dolcomma(col):
    '''Cleans up monetary column and converts to numeric'''
    return pd.to_numeric(col.map(lambda x: str(x).replace(',', '').replace('$', '').replace('USD', '') if pd.notnull(x) else None))


def monetarycol(df):
    '''Applies dolcomma to json columns and converts to integer'''
    df['Assessment Improvement Improved'] = dolcomma(df['Assessment Land'])
    df['Most Recent Sale Price Improved'] = dolcomma(df['Most Recent Sale Price'])
    df['Improvement Value Improved'] = dolcomma(df['Improvement Value'])
    df['Assessment Total Improved'] = dolcomma(df['Assessment Total'])
    df['Land Value Improved'] = dolcomma(df['Land Value'])
    df['Assessment Land Improved'] = dolcomma(df['Assessment Land'])
    df['Total Appraisal Value Improved'] = dolcomma(df['Total Appraisal Value'])
    df['Square Footage Improved'] = dolcomma(df['Square Footage'])
    return df


def heightizer(df_old):
    '''Cleaning story height columns and converting to numeric'''
    df = df_old.copy()

    df['Story Height'] = df['Story Height'].map(
        lambda x: str(x).replace(' STORY', '').replace(' STY', '') if (x != '' and not pd.isnull(x)) else x)
    print(df['Story Height'].value_counts())
    df['Story Height'] = pd.to_numeric(df['Story Height'], errors='ignore')
    df['Story Height'] = df['Story Height'].map(
        lambda x: STORYDICT[x] if x in STORYDICT else x)
    return df


def typizer(df_old):
    '''Combining similar building types'''
    df = df_old.copy()
    df['Building Type Custom'] = df['Building Type'].map(
        lambda x: TYPEDICT[x] if (x != '' and not pd.isnull(x)) else None)
    return df

def columnizer(df_old):
    '''Cleaning up date columns, converting other columns to numeric'''
    df = monetarycol(df_old)
    df = typizer(df)
    df = heightizer(df)
    df['Land Area Acres'] = pd.to_numeric(df['Land Area'].map(lambda x: str(x).replace(
        ' ', '').replace('Acres', '').replace(',', '') if pd.notnull(x) else None))
    df=df.filter(items=COLS)
    return df