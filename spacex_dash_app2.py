# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
spacex_df.astype({'Payload Mass (kg)': 'int64'}).dtypes
print(spacex_df.dtypes)


# Create a list of dictionaries for the sites
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
sites_list = []

for i in launch_sites_df['Launch Site']:
    temp_dict= dict()
    temp_dict['label'] = str(i)
    temp_dict['value'] = str(i)
    sites_list.append(temp_dict)
sites_list.insert(0,{'label': 'ALL', 'value': 'ALL'})


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site-dropdown',
                                        options=sites_list,
                                            value="ALL",
                                            placeholder="Select a Launch site here",
                                            searchable=True,
                                            ),
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                            min=0, max=10000, step=1000,
                                            marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500'},
                                            value=[min_payload, max_payload]),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
        [Output(component_id= 'success-pie-chart', component_property= 'figure'),
        Output(component_id='success-payload-scatter-chart', component_property='figure')],
        [Input(component_id= 'site-dropdown', component_property='value'),
        Input(component_id="payload-slider", component_property="value")]
        )

def get_pie_chart(entered_site, payload): #this needs to contain the scatter graph also.
    filtered_df = spacex_df
    print(payload)
    #for item in enumerate(payload):
    #    payload[item] = float(item)
    
    
    if entered_site == 'ALL':
        total_sites = filtered_df.groupby(['Launch Site'])['class'].sum().reset_index()
        fig = px.pie(total_sites, values='class', 
        names='Launch Site', 
        title='Total sucessful launches')
        
        fig1 = px.scatter(filtered_df,
                        x="Payload Mass (kg)", 
                        y= "class", 
                        color="Booster Version Category")
        return fig, fig1
    else:
        entered_site == str(entered_site)
        
        entered_df = spacex_df[spacex_df['Launch Site'] == str(entered_site)]
        fig = px.pie(entered_df, 
            values="class", 
            names="Launch Site", 
            title="Success vs failed")
        filtered_df = spacex_df[
                        spacex_df["Payload Mass (kg)"]> float(payload[0]) &
                        spacex_df["Payload Mass (kg)"] < float(payload[1])]
        print(filtered_df.head())
        fig1 = px.scatter(filtered_df,
                        x="Payload Mass (kg)", 
                        y= "class", 
                        color="Booster Version Category")
        return fig, fig1
    fig.show()    




# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
