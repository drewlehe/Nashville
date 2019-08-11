'''File for cleaning up the DataFrame comprised of the json files downloaded from the webscraper.'''

import json
import pandas as pd
import numpy as np

CUSTOMDICT = {'ONE': 1, 'ONE STY': 1, '1 STY': 1, '1.25 STY': 1.5,
              '1.5 STORY': 1.5, '1.75 STY': 1.5, 'TWO': 2, 'TWO STY': 2,
              '2 STY': 2, '2.25 STY': 2.5, '2.75 STY': 2.5, '2.5 STORY': 2.5,
              'THREE': 3, '3 STY': 3, 'THREE STY': 3, '4 STY': 4, '4 STORY': 4,
              'SPLIT-LEVEL': 1.5, 'BI-LEVEL': 2}

STORYDICT = {'TWO': 2, 'ONE': 1, 'ONE STY': 1, '1 STY': 1, '1.25 STY': 1.25,
             '1.5 STORY': 1.5, '1.75 STY': 1.75, 'TWO STY': 2, '2 STY': 2,
             '2.25 STY': 2.25, '2.75 STY': 2.75, '2.5 STORY': 2.75, 'THREE': 3,
             '3 STY': 3, 'THREE STY': 3, '4 STY': 4, '4 STORY': 4,
             'SPLIT-LEVEL': 1.5, 'BI-LEVEL': 2}
TYPEDICT = {'HIGHRISE APT': 'CONDO', 'APARTMENT': 'CONDO', 'HRISE CONDO': 'CONDO', 'RESD CONDO': 'CONDO',
            'RW SING FAM': 'SINGLE FAM',
            'RZ SING FAM': 'SINGLE FAM', 'RH SING FAM': 'SINGLE FAM', 'RY SING FAM': 'SINGLE FAM', 'MODULAR HOME': 'SINGLE FAM',
            'SING FAM': 'SINGLE FAM', 'RESD TRIPLEX': 'PLEX', 'RESD QUADPLX': 'PLEX', 'R1 DUPLEX': 'PLEX', 'RES DUPLEX': 'PLEX',
            'LODGE/FRAT\'L': 'THIRD', 'CHURCH': 'THIRD', 'HEALTH CLUB': 'COMM', 'GROCERY/SMKT': 'COMM', 'RETAIL/SHPG': 'COMM',
            'DAYCARE': 'COMM', 'MARKET': 'COMM', 'REST/BAR': 'COMM', 'OFFICE': 'COMM', 'WAREHOUSE': 'COMM'}


def dolcomma(col):
    '''Cleans up monetary column and converts to numeric'''
    return pd.to_numeric(col.map(lambda x: x.replace(',', '').replace('$', '')))


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
    df['Story Height Custom'] = pd.to_numeric(df['Story Height'].map(
        lambda x: CUSTOMDICT[x] if x is not None else None))

    df['Story Height'] = pd.to_numeric(df['Story Height'].map(
        lambda x: STORYDICT[x] if x is not None else None))
    return df


def typizer(df_old):
    '''Combining similar building types'''
    df = df_old.copy()
    df['Building Type Custom'] = df['Building Type'].replace(TYPEDICT)
    return df


def columnizer(df_old):
    '''Cleaning up date columns, converting other columns to numeric'''
    df = typizer(df_old)
    df = monetarycol(df_old)
    df = heightizer(df_old)
    # Cleaning up certain date columns
    df['Most Recent Sale Date'] = pd.to_datetime(df['Most Recent Sale Date'])
    df['Sale Date'] = pd.to_datetime(df['Sale Date'])
    # Converting 'Land Area' column to clean float
    df['Land Area Acres'] = df['Land Area'].map(lambda x: x.replace(
        ' ', '').replace('Acres', '')).map(lambda x: float(x))
    # Neighborhood column is all numbers, but it's categorical.
    df['Neighborhood'] = df['Neighborhood'].map(lambda x: str(x))
    return df


if __name__ == '__main__':

    df = pd.read_csv('merged.csv', index_col=None)

    print(df.head())
