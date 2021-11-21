# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 12:09:25 2021

@author: Tobias
"""

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go
import pandas as pd


## Align what colours to use and correct scale
available_colors = ["#a6cee3","#1f78b4","#b2df8a", "#33a02c","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","#cab2d6","#6a3d9a","#ffff99","#b15928"]

processed_csv_path = r"C:\Users\Tobias\Desktop\Data visualization\Project\Data-Visualization-Group-5-2021/processed_dataset.csv"

def prepareData(processed_csv_path):
    
    df = pd.read_csv(processed_csv_path)
    df.publishedAt= pd.to_datetime(df.publishedAt)
    df.trending_date= pd.to_datetime(df.trending_date)
    
    df['Years'] = df['trending_date'].dt.strftime('%Y')
    df['Months'] = df['trending_date'].dt.strftime('%Y-%m')
    df['Days'] = df['trending_date'].dt.date

    return df

def extractFilterOptions(df):
    available_regions = df['region'].unique()
    available_categories = df['category_text'].unique()
    
    return available_regions, available_categories

df = prepareData(processed_csv_path)
available_regions, available_categories = extractFilterOptions(df)


### DASHBOARD UI

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

controls = dbc.FormGroup(
    [
        html.P('Countries', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='display_regions',
            options=[{'label': i, 'value': i} for i in available_regions],
            value='GB',  # default value
        ),
        html.P('Categories', style={
            'textAlign': 'center'
        }),
        dbc.Card([dcc.Dropdown(
            id='display_categories',
            options=[{'label': i, 'value': i} for i in available_categories],
            value=["Music","Gaming"], # default value
            multi=True,
        )]),
        html.Br(),
        html.P('Time scale', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.RadioItems(
            id='filter_time',
            options=[{'label': i, 'value': i} for i in ['Days', 'Months', 'Years']],
            value='Months', # default value
            style={
                'margin': 'auto'
            }
        )]),
    ]
)

sidebar = html.Div(
    [
        html.H2('Options', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

content_first_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_1'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_2'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_3'), md=4
        )
    ]
)

content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='stacked-area-chart'), md=4,
        )
    ]
)

content_fourth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_5'), md=6
        ),
        dbc.Col(
            dcc.Graph(id='graph_6'), md=6
        )
    ]
)

content = html.Div(
    [
        html.H2('Trending YouTube Dashboard', style=TEXT_STYLE),
        html.Hr(),
        content_first_row,
        content_third_row,
        content_fourth_row
    ],
    style=CONTENT_STYLE
)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])

"""
@app.callback(
    Output('graph_1', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_1(n_clicks, dropdown_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(check_list_value)
    print(radio_items_value)
    fig = {
        'data': [{
            'x': [1, 2, 3],
            'y': [3, 4, 5]
        }]
    }
    return fig
"""


@app.callback(
    Output('stacked-area-chart', 'figure'),
    [Input('display_regions', 'value'),
     Input('filter_time', 'value'),
     Input('display_categories', 'value')])
def update_stacked_area_chart(regionInput, timeInput, categoryInput):

    selected_region = regionInput
    selected_time_format = timeInput
    selected_categories = categoryInput
    
    fig = go.Figure()
    color_count = 0
    for categories in selected_categories:
        
        videos_that_match = df.loc[(df.category_text==categories) & (df.region == selected_region),selected_time_format]
        videos_that_match_count = videos_that_match.value_counts()
        videos_that_match_count = videos_that_match_count.sort_index()
        
        x = videos_that_match_count.index
        y = videos_that_match_count.values
        
        ## example on filter on time
        ##x=df.loc[(df.category_text==categories) & (df.region == selected_region),selected_time_format],
        ##y=df.loc[(df.category_text==categories) & (df.region == selected_region),selected_metric],
            
        
        color_count += 1
        fig.add_trace(go.Scatter(
            x = x,
            y = y,
            mode='lines',
            name=categories,
            line=dict(width=0.5, color=available_colors[color_count-1]),
            stackgroup='one', # define stack group
            groupnorm='percent' # sets the normalization for the sum of the stackgroup
        ))        


    fig.update_layout(
     title = selected_region + ": trending YouTube data",
     title_font_size = 20, legend_font_size = 10,
     showlegend=True,
     width = 800, height = 700,
     yaxis=dict(type='linear',ticksuffix='%'))

    fig.update_xaxes(
         title_text = 'Date',
         title_font=dict(size=15, family='Verdana', color='black'),
         tickfont=dict(family='Calibri', color='black', size=12))

    fig.update_yaxes(
         title_text = "Number of videos(%)", range = (0,100),
         title_font=dict(size=15, family='Verdana', color='black'),
         tickfont=dict(family='Calibri', color='black', size=12))

    return fig






if __name__ == '__main__':
    app.run_server(debug=True)