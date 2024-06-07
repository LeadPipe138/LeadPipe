#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [str(i) for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            placeholder='Select a report type',
            value='Yearly Statistics',
            style={
                'width': '80%',
                'padding': '3px',
                'fontSize': 20,
                'textAlignLast': 'center'
            }
        )
    ]),
    dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        placeholder='Select Year',
        value=year_list[0],  # Set default value to the first year
        style={
            'width': '80%',
            'padding': '3px',
            'fontSize': 20,
            'textAlignLast': 'center'
        }
    ),
    html.Div(id='output-container', className='chart-grid')
])

# Callbacks
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), Input(component_id='dropdown-statistics', component_property='value')]
)
def update_output_container(selected_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"
            )
        )

        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales, 
                x='Vehicle_Type', 
                y='Automobile_Sales',  
                title="Average Number of Automobile Sales by Vehicle Type"
            )
        )

        exp_rec = recession_data.groupby('Vehicle_Type')['Total_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec, 
                names='Vehicle_Type', 
                values='Total_Expenditure',  
                title="Total Expenditure Share by Vehicle Type During Recessions"
            )
        )

        grouped_data = recession_data.groupby('Vehicle_Type').agg({
            'Number_of_Vehicles_Sold': 'mean',
            'Unemployment_Rate': 'mean'
        }).reset_index()

        sales_bar_chart = dcc.Graph(
            figure=px.bar(
                grouped_data, 
                x='Vehicle_Type', 
                y='Number_of_Vehicles_Sold', 
                title="Effect of Unemployment Rate on Vehicle Sales by Vehicle Type"
            )
        )

        unemployment_bar_chart = dcc.Graph(
            figure=px.bar(
                grouped_data, 
                x='Vehicle_Type', 
                y='Unemployment_Rate', 
                title="Effect of Unemployment Rate on Vehicle Type by Vehicle Type"
            )
        )

        return [
            html.Div(className='chart-item', children=[
                html.Div(children=R_chart1),
                html.Div(children=R_chart2)
            ]),
            html.Div(className='chart-item', children=[
                html.Div(children=R_chart3),
                html.Div(children=[sales_bar_chart, unemployment_bar_chart])
            ])
        ]

    elif selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == int(selected_year)]

        Y_chart1 = dcc.Graph(
            figure=px.line(
                yearly_data, 
                x='Month', 
                y='Automobile_Sales', 
                title='Total Monthly Automobile Sales'
            )
        )

        Y_chart2 = dcc.Graph(
            figure=px.bar(
                yearly_data, 
                x='Vehicle_Type', 
                y='Number_of_Vehicles_Sold', 
                title='Average Vehicles Sold by Vehicle Type in the year {}'.format(selected_year)
            )
        )

        Y_chart3 = dcc.Graph(
            figure=px.pie(
                yearly_data.groupby('Vehicle_Type')['Advertisement_Expenditure'].sum().reset_index(), 
                names='Vehicle_Type', 
                values='Advertisement_Expenditure', 
                title='Total Advertisement Expenditure for Each Vehicle'
            )
        )

        return [
            html.Div(className='chart-item', children=[
                html.Div(children=Y_chart1),
                html.Div(children=Y_chart2)
            ]),
            html.Div(className='chart-item', children=[
                html.Div(children=Y_chart3)
            ])
        ]

    else:
        return None


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

