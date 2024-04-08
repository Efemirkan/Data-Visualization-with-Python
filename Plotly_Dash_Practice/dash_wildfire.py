import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt
from dash import no_update


# Create app
app = dash.Dash(__name__)

# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read data into pandas dataframe
df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

#Extract year and month from the date column
df['Year'] = pd.to_datetime(df['Date']).dt.year
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()

# Create Layouts
app.layout = html.Div(children=[
        # Add the title to the dashboard
        html.H1('Australia Wildfire Dashboard',
                style= {'textAlign': 'center',
                        'color': '#00000',
                        'font-size': 30
                
                }
            ),
        
        # Add the radio items and a dropdown right below the first inner division 
        # outer division starts
        html.Div([
            
            # First inner divsion for  adding dropdown helper text for Selected Drive wheels        
            html.Div([

                html.H2('Select Region:', style={'margin-right': '2em'}),   

                #Radio items to select the region
                dcc.RadioItems([
                            {'label': 'New South Wales', 'value': 'NSW'},
                            {'label': 'Northern Territory', 'value': 'NT'},
                            {'label': 'Queensland', 'value': 'QL'},
                            {'label': 'South Australia', 'value': 'SA'},
                            {'label': 'Tasmania', 'value': 'TA'},
                            {'label': 'Victoria', 'value': 'VI'},
                            {'label': 'Western Australia', 'value': 'WA'}
                            ],
                            "NSW",
                            id= "region",
                            inline=True
                )
            ]),
            
            # Dropdown to select year
            html.Div([
                html.H2('Select Year:', 
                        style={
                            'textAlign': 'center',
                            'font-size': 20,
                            'color': '#052155'
                        }
                ),
                dcc.Dropdown(options= [{'label': str(year), 'value': year} for year in df['Year'].unique()], 
                             value = 2005,
                             id='year')
            ]),

            #Second Inner division for adding 2 inner divisions for 2 output graphs
            html.Div([
                html.Div([ ], id='plot1', style={'display': 'inline-block', 'width': '49%'}),
                html.Div([ ], id='plot2', style={'display': 'inline-block', 'width': '49%'}),
                ]
            ),
        

        ])
        #outer division ends                       

])
#layout ends

# Add callback decorator

@app.callback(
        [
        Output(component_id= 'plot1', component_property= 'children'),
        Output(component_id= 'plot2', component_property= 'children')
    ],
        [
        Input(component_id= 'region', component_property= 'value'),
        Input(component_id= 'year', component_property= 'value')
    ]
)

# Define the callback function
def reg_year_display(input_region, input_year):

    # Data
    region_data = df[df['Region'] == input_region]
    year_region_data = region_data[region_data['Year'] == int(input_year)]

    # Plot one - Monthly Average Estimated Fire Area
    est_data = year_region_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(est_data, 
                values= 'Estimated_fire_area',
                names= 'Month',
                title='Monthly Average Estimated Fire Area'
                )
   
    #Plot two - Monthly Average Count of Pixels for Presumed Vegetation Fires
    veg_data = year_region_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(veg_data,
                x= 'Month', 
                y= 'Count',
                title='Monthly Average Count of Pixels for Presumed Vegetation Fires'
                )
                

    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]

if __name__ == "__main__":
    app.run_server(host='127.0.0.2', port=8051)