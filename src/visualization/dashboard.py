# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from visualize import value_per_year, value_per_ward, value_per_building, value_per_neigh
from vis_config import ZONE_DICT
import json

app = dash.Dash(__name__)

resi_house_data = pd.read_csv('prop_price/data/processed/Historical_clean.csv', dtype={'Suite': object})

with open('prop_price/data/raw/edm_ward.geojson', encoding='utf-8') as f:
    ward_gj = json.load(f)
with open('prop_price/data/processed/edm_neigh_clean.geojson', encoding='utf-8') as f:
    neigh_gj = json.load(f)

#get wards into list for graph options
ward_list = ['All']
for i in sorted(resi_house_data['Ward'].unique()):
    ward_list.append(i)

#list of years 
year_list = ['All']
for i in sorted(resi_house_data['Assessment Year'].unique()):
    year_list.append(i)

#zone list
zone_list = ['All']
for i in ZONE_DICT:
    zone_list.append(i)

#neighbourhood list
neigh_list = []
for i in sorted(resi_house_data['Neighbourhood'].unique()):
    neigh_list.append(i)


app.layout = html.Div(children=[

      html.Div([
        dcc.Graph(id='Assessed Value per Year'),    
        dcc.RadioItems(
            id='stat_dropdown',
            options=[
                {'label': 'Average', 'value': 'Average'},
                {'label': 'Median', 'value': 'Median'},
            ],
            value='Average',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='building_type',
            options=[{'label': i, 'value': i} for i in zone_list],
            value='All'
        ),            
        dcc.Dropdown(
            id='location_dropdown',
            options=[{'label': i, 'value': i} for i in ward_list],
            value='All'
        )
    ]),

    html.Div([
        dcc.Graph(id='Assessed Value Map'),
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
        ),
        dcc.Dropdown(
            id='location_dropdown2',
            options=[{'label': i, 'value': i} for i in ward_list],
            value="All"
        )
    ]) 
])

@app.callback(
    Output('Assessed Value per Year', 'figure'),
    Input('building_type', 'value'),
    Input('stat_dropdown', 'value'),
    Input('location_dropdown', 'value')
    )

def update_figure(building_select, stat_select, location_select):
    stat_val_list, year_list = value_per_building(resi_house_data, stat_select, location_select, building_select)
    fig = px.line(resi_house_data, x=year_list, y=stat_val_list, title='Assessed Values Per Year')
    fig.update_layout(title_font_family='Arial', title_font_size=24, title_x=0.5, title_xanchor='center', title_y = 0.85, title_yanchor='top',
                      plot_bgcolor='#f3f6f4',
                      font_family='sans-serif', font_color='#005087', 
                      transition_duration=500,
                      yaxis_tickformat = "$.2f")
    fig.update_xaxes(title='Year')
    fig.update_yaxes(title='Assessed Value ($)')
    return fig

@app.callback(
    Output('Assessed Value Map', 'figure'),
    Input('stat_dropdown2', 'value'),
    Input('year_dropdown', 'value'),
    Input('location_dropdown2', 'value')
)

def update_ward_map(stat_select, year_select, location_select):
    if location_select == 'All':
        ward_price_list, ward_list = value_per_ward(resi_house_data, stat_select, year_select)
        fig = px.choropleth_mapbox(resi_house_data, geojson=ward_gj, featureidkey="properties.name_2",
                            locations=ward_list, color=ward_price_list, color_continuous_scale='blues',
                            mapbox_style="carto-positron",
                            center={"lat": 53.5461, "lon": -113.4938},
                            zoom=8.5
                            )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_traces(colorbar_bgcolor='#005087', selector=dict(type='choroplethmapbox'))
        return fig
    else:
        neigh_price_list, neigh_list = value_per_neigh(resi_house_data, stat_select, year_select, location_select)
        fig = px.choropleth_mapbox(resi_house_data, geojson=neigh_gj, featureidkey="properties.name",
                            locations=neigh_list, color=neigh_price_list, color_continuous_scale='blues',
                            mapbox_style="carto-positron",
                            center={"lat": 53.5461, "lon": -113.4938},
                            zoom=9
                            )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig
    
if __name__ == '__main__':
    app.run_server(debug=True)
