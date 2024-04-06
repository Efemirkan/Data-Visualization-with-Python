import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import numpy as np


# Read the data
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str,
                                   'Year': str})

# Define replace_null(column_name) function to replace Nan values with mean of the column
def replace_null(column_name):
    
    mean_value = airline_data[column_name].mean()
    airline_data[column_name].fillna(mean_value, inplace=True)

replace_null('CarrierDelay')
replace_null('WeatherDelay')
replace_null('NASDelay')
replace_null('SecurityDelay')
replace_null('LateAircraftDelay')

# Create a dash app
app = dash.Dash(__name__)

# Adjust the dash app layouts
app.layout = html.Div(children=[
                                # Title
                                html.H1('Flight Delay Time Statistics',
                                        style= {'textAlign' : 'center',
                                            'color' : '#503D36',
                                            'font-size' : 30
                                            }
                                
                                ),

                                # Input Component
                                html.Div(['Input Year',
                                          dcc.Input(id='input-year',
                                                    value= '2010',
                                                    type= 'number',
                                                    style= {'height': '35px',
                                                            'font-size': 30
                                                        }

                                          )
                                        ],
                                        style={'font-size': 40}
                                ),

                                html.Br(),
                                html.Br(),
                                # Segment 1
                                html.Div([
                                            html.Div(dcc.Graph(
                                                id= 'carrier-plot')
                                            ),
                                            html.Div(dcc.Graph(   
                                                id= 'weather-plot')                                           
                                            )
                                        ],
                                        style={'display': 'flex'}
                                ),
                                
                                # Segment 2
                                html.Div([
                                            html.Div(dcc.Graph(
                                                id= 'nas-plot')
                                            ),
                                            html.Div(dcc.Graph(
                                                id= 'security-plot')
                                            )
                                        ],
                                        style={'display': 'flex'}
                                ),
                                # Segment 3

                                html.Div(dcc.Graph(
                                            id= 'late-plot'
                                        ),
                                        style= {'width': '65%'}
                                
                                )

                                ]
                    )


# Define compute_info(airline_data, entered_year) to group required data
def compute_info(airline_data, entered_year):

    # Select data
    df = airline_data[airline_data['Year'] == entered_year]

    # Compute delay averages
    avg_carrier = df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_system = df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_security = df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_aircraft = df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()

    return avg_aircraft, avg_carrier, avg_security, avg_system, avg_weather

# Callback decorator
@app.callback([
        Output(component_id= 'carrier-plot', component_property= 'figure'),
        Output(component_id= 'weather-plot', component_property= 'figure'),
        Output(component_id= 'nas-plot', component_property= 'figure'),
        Output(component_id= 'security-plot', component_property= 'figure'),
        Output(component_id= 'late-plot', component_property= 'figure'),
            ],
        Input(component_id= 'input-year', component_property= 'value')
)

# Define create_graph(entered_year) funtion to create figures
def create_graph(entered_year):

    # Call the grouped data
    avg_aircraft, avg_carrier, avg_security, avg_system, avg_weather = compute_info(airline_data, entered_year)

    # Line plot for carrier delay
    carrier_fig = px.line(avg_carrier, 
                        x='Month', 
                        y='CarrierDelay', 
                        color='Reporting_Airline', 
                        title='Average carrier delay time by airline'
                    )

    # Line plot for weather delay
    weather_fig = px.line(avg_weather,
                        x='Month',
                        y='WeatherDelay',
                        color='Reporting_Airline',
                        title='Average weather delay time by airline'

                    )

    # Line plot for national air system delay
    nas_fig = px.line(avg_system,
                    x='Month',
                    y='NASDelay',
                    color='Reporting_Airline',
                    title='Average national air system delay time by airline' 
                )

    # Line plot for security delay
    security_fig = px.line(avg_security,
                    x='Month',
                    y='SecurityDelay',
                    color='Reporting_Airline',
                    title='Average security delay time by airline' 
                )

    # Line plot for late aircraft delay  
    aircraft_fig = px.line(avg_aircraft,
                    x='Month',
                    y='LateAircraftDelay',
                    color='Reporting_Airline',
                    title='Average security delay time by airline' 
                )

    return [carrier_fig, weather_fig, nas_fig, security_fig, aircraft_fig]

# Run the app
if __name__ == '__main__':
    app.run_server()