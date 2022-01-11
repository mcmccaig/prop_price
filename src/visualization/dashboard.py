# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from visualize import value_per_year, value_per_ward
import json

app = dash.Dash(__name__)

resi_house_data = pd.read_csv('prop_price/data/processed/Historical_clean.csv', dtype={'Suite': object})
with open('prop_price/data/raw/edm_ward.geojson', encoding='utf-8') as f:
    gj = json.load(f)

#get wards into list for graph options
ward_list = ['All']
for i in sorted(resi_house_data['Ward'].unique()):
    ward_list.append(i)

#list of years 
year_list = ['All']
for i in sorted(resi_house_data['Assessment Year'].unique()):
    year_list.append(i)


app.layout = html.Div(children=[
    html.Div([
        dcc.Graph(id='Assessed Value per Year'),
        #avg/med dropdown menu
        dcc.RadioItems(
            id='stat_dropdown',
            options=[
                {'label': 'Average', 'value': 'Average'},
                {'label': 'Median', 'value': 'Median'},
            ],
            value='Average',
            labelStyle={'display': 'inline-block'}
        ),
        #ward dropdown
        dcc.Dropdown(
            id='location_dropdown',
            options=[{'label': i, 'value': i} for i in ward_list],
            value='All'
        )
    ]),

    html.Div([
        dcc.Graph(id='Ward Map'),
        #avg/med dropdown menu
        dcc.RadioItems(
            id='stat_dropdown2',
            options=[
                {'label': 'Average', 'value': 'Average'},
                {'label': 'Median', 'value': 'Median'},
            ],
            value='Average',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='year_dropdown',
            options=[{'label': i, 'value': i} for i in year_list],
            value='All'
        )


    ])
])

@app.callback(
    Output('Assessed Value per Year', 'figure'),
    Input('stat_dropdown', 'value'),
    Input('location_dropdown', 'value')
    )

def update_figure(stat_select, location_select):
    stat_val_list, year_list = value_per_year(resi_house_data, stat_select, location_select)
    fig = px.line(resi_house_data, x=year_list, y=stat_val_list, title='Assessed Value per Year')
    fig.update_layout(transition_duration=500, yaxis_tickformat = "$.2f")
    fig.update_xaxes(title='Year')
    fig.update_yaxes(title='Assessed Value ($)')
    return fig

@app.callback(
    Output('Ward Map', 'figure'),
    Input('stat_dropdown2', 'value'),
    Input('year_dropdown', 'value')
)

def update_map(stat_select, year_select):
    ward_price_list, ward_list = value_per_ward(resi_house_data, stat_select, year_select)
    fig = px.choropleth_mapbox(resi_house_data, geojson=gj, featureidkey="properties.name_2",
                           locations=ward_list, color=ward_price_list,
                           mapbox_style="carto-positron",
                           center={"lat": 53.5461, "lon": -113.4938},
                           zoom=8.5
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)