import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Year': str }

                            )

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('Total number of flights to destination state split by reporting airline'),
                                html.Div(['Input Year', dcc.Input(id='input-year',
                                                                value='2010',
                                                                type='number',
                                                                style={'height' : '50px',
                                                                        'font-size' : 35
                                                                        }
                                                                )],

                                        style={'font-size': 40}
                                                                    ),

                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id='bar-graph'))


                                ])

@app.callback(Output(component_id = 'bar-graph', component_property= 'figure'),
            Input(component_id= 'input-year', component_property= 'value')    
            )

def total_flights(entered_year):

    df = airline_data[airline_data['Year'] == entered_year]

    bar_data = df.groupby('Reporting_Airline')['Flights'].sum().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(x=bar_data['Reporting_Airline'],
                        y=bar_data['Flights'],
                        marker_color = 'blue',
                        name= 'Flights',
                        opacity= 0.8,
                        text = [f"{total}" for total in bar_data['Flights']]

                    ))

    fig.update_layout(title='Flights to Destination State',
                    xaxis_title= 'Reporting Airlines',
                    yaxis_title= 'Number of Flights'
                    )

    return fig

if __name__ == '__main__':
    app.run_server()