'''File for cleaning up the DataFrame comprised of the json files downloaded from the webscraper.'''

import json
import pandas as pd
import numpy as np
import math

CUSTOMDICT = {'ONE': 1, 'ONE STY': 1, '1 STY': 1, '1.25 STY': 1.5,
              '1.5 STORY': 1.5, '1.75 STY': 1.5, 'TWO': 2, 'TWO STY': 2,
              '2 STY': 2, '2.25 STY': 2.5, '2.75 STY': 2.5, '2.5 STORY': 2.5,
              'THREE': 3, '3 STY': 3, 'THREE STY': 3, '4 STY': 4, '4 STORY': 4,
              'SPLIT-LEVEL': 1.5, 'BI-LEVEL': 2, 'BSMT HOUSE': 1, '5 STY': 5, '6 STY': 6, '7 STY': 7, '8 STY': 8, '9 STY': 9, '11 STY': 11}

STORYDICT = {'TWO': 2, 'ONE': 1, 'ONE STY': 1, '1 STY': 1, '1.25 STY': 1.25,
             '1.5 STORY': 1.5, '1.75 STY': 1.75, 'TWO STY': 2, '2 STY': 2,
             '2.25 STY': 2.25, '2.75 STY': 2.75, '2.5 STORY': 2.75, 'THREE': 3,
             '3 STY': 3, 'THREE STY': 3, '4 STY': 4, '4 STORY': 4,
             'SPLIT-LEVEL': 1.5, 'BI-LEVEL': 2, 'BSMT HOUSE': 1, '5 STY': 5, '6 STY': 6, '7 STY': 7, '8 STY': 8, '9 STY': 9, '11 STY': 11}

TYPEDICT = {'HIGHRISE APT': 'CONDO', 'APARTMENT': 'CONDO', 'HRISE CONDO': 'CONDO', 'RESD CONDO': 'CONDO',
            'RW SING FAM': 'SINGLE FAM', 'SINGLE FAM': 'SINGLE FAM',
            'RZ SING FAM': 'SINGLE FAM', 'RH SING FAM': 'SINGLE FAM', 'RY SING FAM': 'SINGLE FAM', 'MODULAR HOME': 'SINGLE FAM',
            'SING FAM': 'SINGLE FAM', 'RESD TRIPLEX': 'PLEX', 'RESD QUADPLX': 'PLEX', 'R1 DUPLEX': 'PLEX', 'RES DUPLEX': 'PLEX',
            'LODGE/FRAT\'L': 'THIRD', 'CHURCH': 'THIRD', 'HEALTH CLUB': 'COMM', 'GROCERY/SMKT': 'COMM', 'RETAIL/SHPG': 'COMM',
            'DAYCARE': 'COMM', 'MARKET': 'COMM', 'REST/BAR': 'COMM', 'OFFICE': 'OFFICE', 'WAREHOUSE': 'INDUSTRIAL', 'EQUIP SHED': 'INDUSTRIAL', 'SERV GARAGE': 'INDUSTRIAL', 'TRUCK TERM': 'INDUSTRIAL', 'ZERO LOT': 'VACANT', 'CAR WASH': 'COMM', 'MED OFC': 'OFFICE', 'LAUNDRY': 'COMM', 'AUDITORIUM': 'THIRD', 'BANK': 'COMM', 'BOWLING': 'COMM', 'BUSINESS CTR': 'COMM', 'CINEMA': 'COMM', 'CLUB/UNION': "THIRD", "COMM GRNHSE": "INDUSTRIAL", 'WHSE RETAIL': 'COMM', 'ENG/RESEARCH': 'OFFICE', 'COUNTRY CLUB': 'THIRD', 'DEPT STORE': 'RETAIL', 'TENNIS': 'THIRD', 'WALKUP APT': 'CONDO', 'DRUG STORE': 'COMM', 'DISC STORE': 'COMM', 'ELDERLY HSG': 'CONDO', "FUNERAL HM": "THIRD", 'SALES SHOWRM': 'COMM',
            'LUMBER': 'INDUSTRIAL', 'MANF PLANT': 'INDUSTRIAL', 'MAINT HANGER': 'INDUSTRIAL', 'MOTEL': 'COMM', 'MINI-LUBE': 'INDUSTRIAL', 'MINI-WAREHSE': 'INDUSTRIAL', 'FAST FOOD': 'COMM', 'HOTEL': 'COMM', 'NURSING HOME': 'CONDO', "PARK'G GAR": 'COMM',
            'SERV STATION': 'COMM', 'INDOOR WP': 'COMM', 'HOSPITAL': 'THIRD'
            }


def dolcomma(col):
    '''Cleans up monetary column and converts to numeric'''
    return pd.to_numeric(col.map(lambda x: str(x).replace(',', '').replace('$', '').replace('USD', '')), errors='coerce')


def monetarycol(df):
    '''Applies dolcomma to json columns and converts to integer'''
    df['Assessment Improvement Improved'] = dolcomma(df['Assessment Land'])
    df['Most Recent Sale Price Improved'] = dolcomma(df['Most Recent Sale Price'])
    df['Square Footage Improved'] = dolcomma(df['Square Footage'])
    df['Improvement Value Improved'] = dolcomma(df['Improvement Value'])
    df['Assessment Total Improved'] = dolcomma(df['Assessment Total'])
    df['Land Value Improved'] = dolcomma(df['Land Value'])
    df['Assessment Land Improved'] = dolcomma(df['Assessment Land'])
    df['Total Appraisal Value Improved'] = dolcomma(df['Total Appraisal Value'])
    return df


def heightizer(df_old):
    '''Cleaning story height columns and converting to numeric'''
    df = df_old.copy()

    df['Story Height'] = df['Story Height'].map(
        lambda x: str(x).replace(' STORY', '').replace(' STY', ''))

    df['Story Height Custom'] = pd.to_numeric(df['Story Height'].map(
        lambda x: CUSTOMDICT[x] if not pd.isnull(x) and x in CUSTOMDICT else float(x)))

    df['Story Height'] = pd.to_numeric(df['Story Height'].map(
        lambda x: STORYDICT[x] if not pd.isnull(x) and x in STORYDICT else float(x)))
    return df


def typizer(df_old):
    '''Combining similar building types'''
    df = df_old.copy()
    df['Building Type Custom'] = df['Building Type'].map(
        lambda x: TYPEDICT[x] if not pd.isnull(x) else None)
    return df


def columnizer(df_old):
    '''Cleaning up date columns, converting other columns to numeric'''
    df = monetarycol(df_old)
    df = typizer(df)
    df = heightizer(df)
    # Cleaning up certain date columns
    df['Most Recent Sale Date'] = pd.to_datetime(df['Most Recent Sale Date'], errors='ignore')
    df['Sale Date'] = pd.to_datetime(df['Sale Date'], errors='ignore')
    # Converting 'Land Area' column to clean float
    df['Land Area Acres'] = pd.to_numeric(df['Land Area'].map(lambda x: str(x).replace(
        ' ', '').replace('Acres', '').replace(',', '') if not pd.isnull(x) else None))
    # Neighborhood and Zone are all numbers, but they're categorical.
    df['Neighborhood'] = df['Neighborhood'].map(lambda x: str(x) if not pd.isnull(x) else None)
    df['Zone'] = df['Zone'].map(lambda x: str(x) if not pd.isnull(x) else None)

    return df


if __name__ == '__main__':

    df = pd.read_csv('mergednew.csv', index_col=None)

    print(df.head())
