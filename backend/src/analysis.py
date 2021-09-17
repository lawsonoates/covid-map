
import pandas as pd
import matplotlib.pyplot as plt
import csv

ISO2_INDEX = 1
COUNTRY_REGION_INDEX = 7

# def get_country_region(code):

#     country_region = ''

#     with open('lookup.csv') as lookup_file:
#         lookup_reader = csv.reader(lookup_file)

#         for row in lookup_reader:
#             if row[ISO2_INDEX] == code:
#                 country_region = row[COUNTRY_REGION_INDEX]
#                 break

#     return country_region

# def get_series(country_region, column):

#     df = pd.read_csv('downloaded.csv')

#     region_df = df.loc[df['Country_Region'] == country_region]

#     return region_df.loc[:, column]

# def get_sum(series):
#     sum = int(series.sum())
#     return '{:,}'.format(sum)

# def search_series(query):

#     query = query.lower()
#     df = pd.read_csv('lookup.csv')

#     regions_series = df.loc[:, 'Country_Region']

#     prev_value = ''
#     for index, value in regions_series.items():
        
#         if value == prev_value:   
#             regions_series = regions_series.drop([index], axis=0)

#         prev_value = value

#     exact = False
#     result = []
#     # print(regions_series)
#     for index, value in regions_series.items():
#         # print(f'Index: {index}, Value: {value}')
#         value = value.lower()
#         if value == query and not exact:
#             result = [value]
#         elif value == query and exact:
#             result.append(value)
#         elif value.startswith(query) and not exact:
#             result.append(value)

#     return result

