
import pandas as pd
import matplotlib.pyplot as plt
import csv

ISO2_INDEX = 1
COUNTRY_REGION_INDEX = 7

def get_country_region(code):

    country_region = ''

    with open('lookup.csv') as lookup_file:
        lookup_reader = csv.reader(lookup_file)

        for row in lookup_reader:
            if row[ISO2_INDEX] == code:
                country_region = row[COUNTRY_REGION_INDEX]
                break

    return country_region

def get_series(country_region, column):

    df = pd.read_csv('downloaded.csv')

    region_df = df.loc[df['Country_Region'] == country_region]

    return region_df.loc[:, column]

def get_sum(series):
    sum = int(series.sum())
    return '{:,}'.format(sum)

if __name__ == '__main__':
    country_region = get_country_region('AU')
    print(type(int(get_series(country_region, 'Confirmed').sum())))
