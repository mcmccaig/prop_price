import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

resi_house_data = pd.read_csv('prop_price/data/processed/Historical_clean.csv', dtype={'Suite': object})

def stat_per_year(df, stat_column_name, measurement):
    year_list = df['Assessment Year'].unique()
    year_list = np.sort(year_list)
    stat_avg_list = []
    for year in year_list:
        year_mask = df[df['Assessment Year'] == year]
        if measurement == 'Average':
            stat_avg = year_mask[stat_column_name].mean()
            stat_avg_list.append(stat_avg)
        elif measurement == 'Median':
            stat_avg = year_mask[stat_column_name].median()
            stat_avg_list.append(stat_avg)
        else:
            raise ValueError('Not a correct measurement, use either Average or Median.')
    return stat_avg_list, year_list

def prop_price_year_graph(df, stat_column_name, measurement):
    assessed_value, year_list = stat_per_year(df, stat_column_name, measurement)
    fig = px.line(df, x=year_list, y=assessed_value)
    fig.update_layout(xaxis_title = 'Year', yaxis_title = f'{measurement} Assessed Value', title={
        'text':f'{measurement} Assessed Value per Year',
    })
    fig.show()


def interactive_plot(df, stat_column_name, measurement):
    fig = go.Figure()
    for measure in measurement:
        assessed_value, year_list = stat_per_year(df, stat_column_name, measure)
        fig.add_trace(go.Scatter(x=year_list, y=assessed_value))
    fig.update_layout(xaxis_title = 'Year', yaxis_title = f'{measurement} Assessed Value', title={
        'text':f'{measurement} Assessed Value per Year',
    })

    fig.update_scenes(
        aspectratio=dict(x=1, y=1, z=0.7),
        aspectmode="manual"
    )

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=["type", "Average"],
                        label="Average",
                        method="restyle"
                    ),
                    dict(
                        args=["type", "Median"],
                        label="Median",
                        method="restyle"
                    )
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ]
    )
    fig.show()


# prop_price_year_graph(resi_house_data, 'Assessed Value', 'Average')
interactive_plot(resi_house_data, 'Assessed Value', ['Average', 'Median'])