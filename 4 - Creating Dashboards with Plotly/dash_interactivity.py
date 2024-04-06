import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Read data
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Year': str }
                            )

# Create a dash app
app = dash.Dash(__name__)

# Get the layout and adjust it

app.layout = html.Div(children=[html.H1('Airplane Performance Dashboard',
                                        style={'textAlign' : 'center',
                                                'color' : '#00000',
                                                'font-size' : 40
                                              }
                                        
                                        ),

                                html.Div(['Input Year',
                                           dcc.Input(id='input-year', 
                                                    value='2010',
                                                    type='number',
                                                    style={'height' : '50px',
                                                            'font-size' : 35
                                                            }
                                                    )
                                          ],
                                          style={'font-size' : 40}                    
                                        ),
                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id='line-plot'))
                                ]
                      )

# Add callback decorator
@app.callback(Output(component_id='line-plot', component_property='figure'),
                Input(component_id='input-year', component_property='value'))

def get_graph(entered_year):

    # Select data based on the entered year
    df = airline_data[airline_data['Year']== entered_year]

    # Group the data by Month and compute the average arrival delay time
    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()

    # Create the Graph
    fig = go.Figure(data=go.Scatter(x=line_data['Month'],
                                    y=line_data['ArrDelay'],
                                    mode='lines',
                                    marker=dict(color='blue')
                    ))

    fig.update_layout(title='Month vs Average Flight Delay Time',
                    xaxis_title='Month',
                    yaxis_title='ArrDelay'
                    )
    return fig

if __name__ == '__main__':
    app.run_server()