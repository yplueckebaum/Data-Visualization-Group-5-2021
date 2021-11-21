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

import plotly.express as px
import pandas as pd
import numpy as np
from os.path import exists

## Align what colours to use and correct scale
available_colors = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6",
                    "#6a3d9a", "#ffff99", "#b15928"]

processed_csv_path = "processed_dataset.csv"


def prepareData(processed_csv_path):
    df = pd.read_csv(processed_csv_path)
    df.publishedAt = pd.to_datetime(df.publishedAt)
    df.trending_date = pd.to_datetime(df.trending_date)

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

processed_csv_path = "processed_dataset.csv"

country_codes = ['BR', 'CA', 'DE', 'FR', 'GB', 'IN', 'JP', 'KR', 'MX', 'RU', 'US']

category_ids_to_names_dict = {1: "Film & Animation",
2: "Autos & Vehicles",
10: "Music",
15: "Pets & Animals",
17: "Sports",
18: "Short Movies",
19: "Travel & Events",
20: "Gaming",
21: "Videoblogging",
22: "People & Blogs",
23: "Comedy",
24: "Entertainment",
25: "News & Politics",
26: "Howto & Style",
27: "Education",
28: "Science & Technology",
29: "Nonprofits & Activism",
30: "Movies",
31: "Anime/Animation",
32: "Action/Adventure",
33: "Classics",
34: "Comedy",
35: "Documentary",
36: "Drama",
37: "Family",
38: "Foreign",
39: "Horror",
40: "Sci-Fi/Fantasy",
41: "Thriller",
42: "Shorts",
43: "Shows",
44: "Trailers"}

category_names_to_ids_dict = {"Film & Animation":1,
"Autos & Vehicles":2,
"Music":10,
"Pets & Animals":15,
"Sports":17,
"Short Movies":18,
"Travel & Events":19,
"Gaming":20,
"Videoblogging":21,
"People & Blogs":22,
"Comedy":23,
"Entertainment":24,
"News & Politics":25,
"Howto & Style":26,
"Education":27,
"Science & Technology":28,
"Nonprofits & Activism":29,
"Movies":30,
"Anime/Animation":31,
"Action/Adventure":32,
"Classics":33,
"Comedy":34,
"Documentary":35,
"Drama":36,
"Family":37,
"Foreign":38,
"Horror":39,
"Sci-Fi/Fantasy":40,
"Thriller":41,
"Shorts":42,
"Shows":43,
"Trailers":44}

dates_from_processed_dataset = pd.read_csv("processed_dataset.csv", usecols=[7])
dates_from_processed_dataset.sort_values('trending_date')
unique_dates = dates_from_processed_dataset.trending_date.unique()
unique_dates = np.array(unique_dates)
no_of_unique_dates = len(unique_dates)

country_list = []
for i in country_codes:
    country_list.append({'label': i, 'value': i})

categories_list = []
for (key, value) in category_ids_to_names_dict.items():
    categories_list.append({'label': value, 'value': value})

current_data_set = "Dataset/Titledata/BR/BR_title_totals.csv"
df_for_title_chart  = pd.read_csv(current_data_set)

x = ['Did use () or []', 'Did use CAPS', 'Did use emojis']

controls = dbc.FormGroup(
    [
        html.P('Regions', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown',
            options=[{
                'label': 'Value One',
                'value': 'value1'
            }, {
                'label': 'Value Two',
                'value': 'value2'
            },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value=['value1'],  # default value
            multi=True
        ),
        html.P('Categories', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.Checklist(
            id='check_list',
            options=[{
                'label': 'Value One',
                'value': 'value1'
            },
                {
                    'label': 'Value Two',
                    'value': 'value2'
                },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value=['value1', 'value2'],
            inline=True
        )]),
        html.Br(),
        html.P('Radio Items', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.RadioItems(
            id='filter_time',
            options=[{'label': i, 'value': i} for i in ['Days', 'Months', 'Years']],
            value='Months',  # default value
            style={
                'margin': 'auto'
            }
        )]),
        html.Br(),
        dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Submit',
            color='primary',
            block=True
        ),
        dcc.Dropdown(
            id="title_drop_down",
            options=country_list,
            value=['BR'],
            multi=True
        ),
        dcc.Dropdown(id="categories_drop_down", options=categories_list, value=["Music","Gaming"], multi=True),
    ]
)

sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

content_first_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='stacked-area-chart'), md=4
        ),
        dbc.Col(
            html.Div(children=[dcc.Graph(id='title_bar_chart'), dcc.RangeSlider(
                id="dataslider",
                min=0,
                max=no_of_unique_dates,
                updatemode='mouseup',
                step=1,
                value=[0, no_of_unique_dates],
                pushable=1), html.Div(id='my-output', style={"text-align": "center", "display": "inline-block", "width":"100%"})]), md=4
        ),
        dbc.Col(
            html.Div(), md=4
        )
    ]
)

content_third_row = dbc.Row(
    [
        dbc.Col(
            html.Div(), md=12,
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


""""
@app.callback(
    Output('graph_1', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)
    fig = {
        'data': [{
            'x': [1, 2, 3],
            'y': [3, 4, 5]
        }]
    }
    return fig


@app.callback(
    Output('graph_2', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_2(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)
    fig = {
        'data': [{
            'x': [1, 2, 3],
            'y': [3, 4, 5],
            'type': 'bar'
        }]
    }
    return fig


@app.callback(
    Output('graph_3', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_3(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)
    df = px.data.iris()
    fig = px.density_contour(df, x='sepal_width', y='sepal_length')
    return fig


@app.callback(
    Output('graph_4', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_4(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure
    df = px.data.gapminder().query('year==2007')
    fig = px.scatter_geo(df, locations='iso_alpha', color='continent',
                         hover_name='country', size='pop', projection='natural earth')
    fig.update_layout({
        'height': 600
    })
    return fig


@app.callback(
    Output('graph_5', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_5(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure
    df = px.data.iris()
    fig = px.scatter(df, x='sepal_width', y='sepal_length')
    return fig


@app.callback(
    Output('graph_6', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_6(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure
    df = px.data.tips()
    fig = px.bar(df, x='total_bill', y='day', orientation='h')
    return fig


@app.callback(
    Output('card_title_1', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_card_title_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure
    return 'Card Tile 1 change by call back'


@app.callback(
    Output('card_text_1', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_card_text_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure
    return 'Card text change by call back'
"""


################## Stuff for title-chart
def update_data(input_countries, input_categories, slider_interval):
    #Should not use global, ideally - But only if multi-user session according to the tutorials (we just making a prototype, so I think it's okay?)
    global current_data_set, df_test, total_titles, did_use_par_or_bracks, did_use_caps, did_use_emojis, did_not_use_par_or_bracks, did_not_use_caps, did_not_use_emojis

    total_titles = 0
    did_use_par_or_bracks = 0
    did_use_caps = 0
    did_use_emojis = 0
    did_not_use_par_or_bracks = 0
    did_not_use_caps = 0
    did_not_use_emojis = 0

    for input_country in input_countries:
        if len(input_categories) == 0:
            if slider_interval[0] == 0 and slider_interval[1] == no_of_unique_dates:
                current_data_set = "Dataset/Titledata/" + input_country + "/" + input_country + "_title_totals.csv"
                df_test  = pd.read_csv(current_data_set)

                total_titles += np.array(df_test.total_number_of_titles)[0]
                did_use_par_or_bracks += np.array(df_test.number_of_titles_with_parenthesis_or_squarebracket_usage)[0]
                did_use_caps += np.array(df_test.number_of_titles_with_caps_usage)[0]
                did_use_emojis += np.array(df_test.number_of_titles_with_emoji_usage)[0]
            else:
                current_data_set = "Dataset/Titledata/" + input_country + "/" + input_country + "_allcategories_totals_per_day.csv"
                df_test  = pd.read_csv(current_data_set)
                mask = (df_test['date'] >= unique_dates[slider_interval[0]]) & (df_test['date'] <= unique_dates[slider_interval[1]-1])
                df_test = df_test.loc[mask]

                for index, row in df_test.iterrows():
                    total_titles += row['total_number_of_titles']
                    did_use_par_or_bracks += row['number_of_titles_with_parenthesis_or_squarebracket_usage']
                    did_use_caps += row['number_of_titles_with_caps_usage']
                    did_use_emojis += row['number_of_titles_with_emoji_usage']
        else:
            for input_category in input_categories:
                category_id = category_names_to_ids_dict[input_category]
                current_data_set = "Dataset/Titledata/" + input_country + "/" + input_country + "_category" + str(category_id) + "_totals_per_day.csv"
                file_exists = exists(current_data_set)
                if file_exists:
                    df_test  = pd.read_csv(current_data_set)
                else:
                    continue

                mask = (df_test['date'] >= unique_dates[slider_interval[0]]) & (df_test['date'] <= unique_dates[slider_interval[1]-1])
                df_test = df_test.loc[mask]

                for index, row in df_test.iterrows():
                    total_titles += row['total_number_of_titles']
                    did_use_par_or_bracks += row['number_of_titles_with_parenthesis_or_squarebracket_usage']
                    did_use_caps += row['number_of_titles_with_caps_usage']
                    did_use_emojis += row['number_of_titles_with_emoji_usage']
    did_use_par_or_bracks = (did_use_par_or_bracks/total_titles)*100 if total_titles > 0 else 0
    did_use_caps = (did_use_caps/total_titles)*100 if total_titles > 0 else 0
    did_use_emojis = (did_use_emojis/total_titles)*100 if total_titles > 0 else 0

    did_not_use_par_or_bracks = 100 - did_use_par_or_bracks if total_titles > 0 else 0
    did_not_use_caps = 100 - did_use_caps if total_titles > 0 else 0
    did_not_use_emojis = 100 - did_use_emojis if total_titles > 0 else 0

@app.callback(
    Output(component_id='title_bar_chart', component_property='figure'),
    Input("title_drop_down", "value"),
    Input("categories_drop_down", "value"),
    Input("dataslider", "value"))
def update_output_div(input_countries, input_categories, slider_interval):
    update_data(input_countries, input_categories, slider_interval)

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Yes", x=x, y=[did_use_par_or_bracks, did_use_caps, did_use_emojis], marker_color='rgb(44, 127, 184)'))
    fig.add_trace(go.Bar(name="No", x=x, y=[did_not_use_par_or_bracks, did_not_use_caps, did_not_use_emojis], marker_color='rgb(254, 178, 76)'))

    fig.update_layout(title_text='Titles')
    fig.update_layout(barmode='stack')
    fig.update_layout(yaxis_range=(0, 100))
    fig.update_layout(transition={
                'duration': 500,
                'easing': 'cubic-in-out'
        })

    return fig

@app.callback(
    Output('my-output', component_property='children'),
    Input('dataslider', 'value'))
def settext(slider_interval):
    return unique_dates[slider_interval[0]] + " - " + unique_dates[slider_interval[1]-1]


@app.callback(
    dash.dependencies.Output('stacked-area-chart', 'figure'),
    [dash.dependencies.Input('title_drop_down', 'value'),
    Input('filter_time', 'value'),
     dash.dependencies.Input('categories_drop_down', 'value')])
def update_graph(regionInput, timeInput, categoryInput):
    ctx = dash.callback_context

    selected_region = regionInput
    selected_time_format = timeInput
    selected_categories = categoryInput

    fig = go.Figure()
    color_count = 0
    for categories in selected_categories:

        videos_that_match = df.loc[(df.category_text==categories) & (df.region == selected_region[0]), selected_time_format]
        videos_that_match_count = videos_that_match.value_counts()
        videos_that_match_count = videos_that_match_count.sort_index()

        x = videos_that_match_count.index
        y = videos_that_match_count.values

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
     title = " trending YouTube data",
     title_font_size = 20, legend_font_size = 10,
     showlegend=True,
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