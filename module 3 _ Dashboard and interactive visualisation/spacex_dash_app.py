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
launch_sites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options = [{'label': 'All Sites', 'value': 'ALL'}] +
                                                    [{'label': site, 'value': site} for site in launch_sites],
                                            value='ALL',
                                            placeholder="Select a Launch Site",
                                            searchable=True
                                             ),
                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
           # Filter only successful launches (class = 1)
        filtered_df = spacex_df[spacex_df['class'] == 1]
        # Group by Launch Site to get the total number of successful launches per site
        success_counts = filtered_df.groupby('Launch Site').size().reset_index(name='counts')
        
        # Create a pie chart showing success counts for each launch site
        fig = px.pie(success_counts, values='counts', 
                     names='Launch Site', 
                     title='Total Successful Launches for All Sites')
        return fig
    else:
        # Filter the DataFrame for the selected launch site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        
        # Count success/failure for the selected site
        filtered_df = filtered_df.groupby('class').size().reset_index(name='counts')
        
        # Create a pie chart for the selected site
        fig = px.pie(filtered_df, values='counts', 
                     names='class', 
                     title=f'Total Success and Failure Launches for {entered_site}')
        return fig
        # return the outcomes piechart for a selected site


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='payload-slider', component_property='value'),
              Input(component_id='site-dropdown', component_property='value'))

def get_scatter(slider_range,entered_site):
    Rangemin, RangeMax = slider_range
    # Filter DataFrame based on payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= Rangemin) & 
                            (spacex_df['Payload Mass (kg)'] <= RangeMax)]

    if entered_site == 'ALL':
        # Create a scatter plot for all sites
        fig2 = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Payload Mass vs. Success/Failure for All Sites',
                         labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Success (1) / Failure (0)'})
        return fig2
    else:
        # Filter DataFrame for the selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        # Create a scatter plot for the selected site
        fig2 = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Payload Mass vs. Success/Failure for {entered_site}',
                         labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Success (1) / Failure (0)'})
        return fig2
# Run the app
if __name__ == '__main__':
    app.run_server()
