import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def value_per_year(df, measurement, ward='All'):
    year_list = df['Assessment Year'].unique()
    year_list = np.sort(year_list)
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

# resi_house_data = pd.read_csv('prop_price/data/processed/Historical_clean.csv', dtype={'Suite': object})
# ward_list = sorted(resi_house_data['Ward'].unique())
# print(ward_list)
# print(resi_house_data.head())
# stat_list, year_list = value_per_year(resi_house_data, 'Average', ward=ward_list[1])
# print(dict(zip(year_list, stat_list)))