import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from vis_config import ZONE_DICT 

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

def value_per_building(df, measurement, ward='All', building_type='All'):
    year_list = sorted(df['Assessment Year'].unique())
    stat_list = []
    if building_type != 'All':
        if building_type == 'House':
            df = df[df['Zoning'].isin(ZONE_DICT['House'])]
            stat_list, year_list = value_per_year(df, measurement, ward)
        elif building_type == 'Townhouse':
            df = df[df['Zoning'].isin(ZONE_DICT['Townhouse'])]
            stat_list, year_list = value_per_year(df, measurement, ward)
        elif building_type == 'Apartment':
            df = df[df['Zoning'].isin(ZONE_DICT['Apartment'])]
            stat_list, year_list = value_per_year(df, measurement, ward)
        elif building_type == 'Rural':
            df = df[df['Zoning'].isin(ZONE_DICT['Rural'])]
            stat_list, year_list = value_per_year(df, measurement, ward)
        else:
            raise ValueError('building_type must be House, Townhouse, Apartment or Rural.')
    else:
        stat_list, year_list = value_per_year(df, measurement, ward)
    return stat_list, year_list
             

# resi_house_data = pd.read_csv('prop_price/data/processed/Historical_clean.csv', dtype={'Suite': object})
# stat_list, year_list = value_per_building(resi_house_data, 'Average', ward='papastew Ward', building_type='Townhouse')
# stat_list, year_list = value_per_year(resi_house_data, measurement, ward='All')
# print(stat_list)