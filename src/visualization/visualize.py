import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def value_per_year(df, measurement, ward='All'):
    year_list = sorted(df['Assessment Year'].unique())
    stat_list = []
    if ward != 'All':
        df = df[df['Ward'] == ward]
    for year in year_list:
        year_mask = df[df['Assessment Year'] == year]
        if measurement == 'Average':
            stat_avg = year_mask['Assessed Value'].mean()
            stat_list.append(stat_avg)
        elif measurement == 'Median':
            stat_avg = year_mask['Assessed Value'].median()
            stat_list.append(stat_avg)
        else:
            raise ValueError('Not a correct measurement, use either Average or Median.')
    return stat_list, year_list

def value_per_ward(df, measurement, year='All'):
    ward_list = sorted(df['Ward'].unique())
    ward_price_list = []
    if year != 'All':
        df = df[df['Assessment Year'] == year]
    for ward in ward_list:
        if measurement == 'Average':
            mask = df[df['Ward'] == ward]
            ward_price_list.append(mask['Assessed Value'].mean())
        elif measurement == 'Median':
            mask = df[df['Ward'] == ward]
            ward_price_list.append(mask['Assessed Value'].median())
        else:
            raise ValueError('Not a correct measurement, use either Average or Median.')
    return ward_price_list, ward_list    

# resi_house_data = pd.read_csv('prop_price/data/processed/Historical_clean.csv', dtype={'Suite': object})
# ward_price_list, ward_list = value_per_ward(resi_house_data, 'Average', year='All')
# print(ward_price_list, ward_list)