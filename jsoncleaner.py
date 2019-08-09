import json
import pandas as pd
import numpy as np
if __name__ == '__main__':

    df = pd.read_csv('merged.csv', index_col=None)

    def dolcomma(col):
        return pd.to_numeric(col.map(lambda x: x.replace(',', '').replace('$', '')))

    # Cleaning up monetary columns and converting to integer
    df['Assessment Improvement Improved'] = dolcomma(df['Assessment Land'])
    df['Most Recent Sale Price Improved'] = dolcomma(df['Most Recent Sale Price'])
    df['Square Footage Improved'] = dolcomma(df['Square Footage'])
    df['Improvement Value Improved'] = dolcomma(df['Improvement Value'])
    df['Assessment Total Improved'] = dolcomma(df['Assessment Total'])
    df['Land Value Improved'] = dolcomma(df['Land Value'])
    df['Assessment Land Improved'] = dolcomma(df['Assessment Land'])
    df['Total Appraisal Value Improved'] = dolcomma(df['Total Appraisal Value'])

    # Cleaning up certain date columns
    df['Most Recent Sale Date'] = pd.to_datetime(df['Most Recent Sale Date'])
    df['Sale Date'] = pd.to_datetime(df['Sale Date'])

    # Converting 'Land Area' column to clean float
    df['Land Area Acres'] = df['Land Area'].map(lambda x: x.replace(
        ' ', '').replace('Acres', '')).map(lambda x: float(x))

    # Neighborhood column is all numbers, but it's categorical.
    df.Neighborhood = df.Neighborhood.map(lambda x: str(x))

    # Need to convert this to numeric. Split-level = 1.5, 1.75 story= 1.5
    df['Story Height Custom'] = df['Story Height'].astype(str).map(lambda x: x.replace(
        'STY', '').replace('STORY', '').replace(' ', '').replace('TWO', '2').replace('ONE', '1'))
    df['Story Height Custom'] = df['Story Height Improved'].map(lambda x: x.replace(
        'THREE', '3').replace('SPLIT-LEVEL', '1.5').replace('BI-LEVEL', '2')).replace('1.75', '1.5')
    df['Story Height Custom'] = df['Story Height Improved'].map(lambda x: float(x))

    # All apartments and multifamily I am listing as "condo"
    df['Building Type Custom'] = df['Building Type'].replace('HIGHRISE APT', 'CONDO').replace(
        'APARTMENT', 'CONDO').replace('HRISE CONDO', 'CONDO').replace('RESD CONDO', 'CONDO')
    # Combining single-family residential
    df['Building Type Custom'] = df['Building Type'].replace('RW SING FAM', 'SINGLE FAM').replace('RZ SING FAM', 'SINGLE FAM').replace(
        'RH SING FAM', 'SINGLE FAM').replace('RY SING FAM', 'SINGLE FAM').replace('MODULAR HOME', 'SINGLE FAM').replace('SING FAM', 'SINGLE FAM')
    # Combining all townhomes up to quadplexes
    df['Building Type Custom'] = df['Building Type'].replace('RESD TRIPLEX', 'PLEX').replace(
        'RESD QUADPLX', 'PLEX').replace('R1 DUPLEX', 'PLEX').replace('RES DUPLEX', 'PLEX')
    # Combining "third places"
    df['Building Type Custom'] = df['Building Type'].replace(
        'LODGE/FRAT\'L', 'THIRD').replace('CHURCH', 'THIRD')
    # Combining commercial
    df['Building Type Custom'] = df['Building Type'].replace('HEALTH CLUB', 'COMM').replace('GROCERY/SMKT', 'COMM').replace(
        'RETAIL/SHPG', 'COMM').replace('DAYCARE', 'COMM').replace('MARKET', 'COMM').replace('REST/BAR', 'COMM')
    df['Building Type Custom'] = df['Building Type'].replace(
        'OFFICE', 'COMM').replace('WAREHOUSE', 'COMM')
