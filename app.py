# -*- coding: utf-8 -*-

################################################################################################# IMPORTS
import json
import datetime
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from collections import Counter
import plotly.express as px
import pandas as pd
import numpy as np
from os.path import exists
import os
import _pickle as cPickle
from flask import send_from_directory

from Data_processing.cooccurrencefolder.cooccurrence import CoOccurrence

debugging = False

################################################################################################# DATA STRUCTURES
print("-------------------> Loading data structures")
start = datetime.datetime.now()
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

category_names_to_ids_dict = {"Film & Animation": 1,
                              "Autos & Vehicles": 2,
                              "Music": 10,
                              "Pets & Animals": 15,
                              "Sports": 17,
                              "Short Movies": 18,
                              "Travel & Events": 19,
                              "Gaming": 20,
                              "Videoblogging": 21,
                              "People & Blogs": 22,
                              "Comedy": 23,
                              "Entertainment": 24,
                              "News & Politics": 25,
                              "Howto & Style": 26,
                              "Education": 27,
                              "Science & Technology": 28,
                              "Nonprofits & Activism": 29,
                              "Movies": 30,
                              "Anime/Animation": 31,
                              "Action/Adventure": 32,
                              "Classics": 33,
                              "Comedy": 34,
                              "Documentary": 35,
                              "Drama": 36,
                              "Family": 37,
                              "Foreign": 38,
                              "Horror": 39,
                              "Sci-Fi/Fantasy": 40,
                              "Thriller": 41,
                              "Shorts": 42,
                              "Shows": 43,
                              "Trailers": 44}

end = datetime.datetime.now()
print("It took " + str((end - start).total_seconds() * 1000) + " miliseconds to load the data structures.")

################################################################################################# STYLING
print("-------------------> Loading styling")
start = datetime.datetime.now()
available_colors = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6",
                    "#6a3d9a", "#ffff99", "#b15928"]

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

end = datetime.datetime.now()
print("It took " + str((end - start).total_seconds() * 1000) + " miliseconds to load the styling.")

################################################################################################# LOAD DATASET AND SET UP NECESSARY VARIABLES
already_loaded_dataset_and_set_up_variables = False
if not already_loaded_dataset_and_set_up_variables:
    print("-------------------> Loading dataset and setting up necessary variables")
    start = datetime.datetime.now()


    def prepareData(processed_csv_path):
        print("prepareData has been called")
        if debugging:
            df = pd.read_csv(processed_csv_path, nrows=1000)
        else:
            df = pd.read_csv(processed_csv_path)
        df.publishedAt = pd.to_datetime(df.publishedAt)
        df.trending_date = pd.to_datetime(df.trending_date)

        #df['Years'] = df['trending_date'].dt.strftime('%Y')
        df['Months'] = df['trending_date'].dt.strftime('%Y-%m')
        df['Days'] = df['trending_date'].dt.date

        return df


    def extractFilterOptions(df):
        print("extractFilterOptions has been called")
        available_regions = df['region'].unique()
        available_categories = df.loc[df['category_text'] != "0"]
        available_categories = available_categories['category_text'].unique()

        return available_regions, available_categories


    df = prepareData(processed_csv_path)
    available_regions, available_categories = extractFilterOptions(df)

    print("Setting up unique dates and lists for dropdowns")
    dates_from_processed_dataset = df["trending_date"]
    unique_dates_dates = dates_from_processed_dataset.unique()
    max_date = unique_dates_dates.max()
    min_date = unique_dates_dates.min()
    max_date_string = str(max_date)
    min_date_string = str(min_date)
    unique_dates = unique_dates_dates.astype(str)
    no_of_unique_dates = len(unique_dates)

    country_list = []
    for i in country_codes:
        country_list.append({'label': i, 'value': i})

    categories_list = []
    for i in available_categories:
        categories_list.append({'label': i, 'value': i})

    if not debugging:
        print("Setting up cooccurrence")
        cooccurrence = CoOccurrence()
        cooccurrence.setup(debugging, df_from_dashboard=df)
        print("Finished setting up cooccurrence")

        print("Setting up cooccurrence dictionary from pickle")
        with open("./occurrence.pickle", 'rb') as handle:
            cooccurrence.tags_occurrence_dict = np.load(handle, allow_pickle=True)
        occurrence_df = pd.DataFrame.from_dict(cooccurrence.tags_occurrence_dict, orient='index')
        print("Finished setting up cooccurrence dictionary from pickle")

    end = datetime.datetime.now()
    print("It took " + str(
        (end - start).total_seconds() * 1000) + " miliseconds load dataset and set up necessary variables.")

################################################################################################# DASHBOARD SET UP
print("-------------------> Setting up dashboard")
start = datetime.datetime.now()
controls = dbc.FormGroup(
    [
        html.P('Regions', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id="countries-drop-down",
            options=country_list,
            value=['BR'],
            multi=True
        ),
        html.P('Categories', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(id="categories-drop-down", options=categories_list, value=["Music", "Gaming"], multi=True),
        html.P('Time scale', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.RadioItems(
            id='filter_time',
            options=[{'label': i, 'value': i} for i in ['Days', 'Months']],
            value='Days',  # default value
            style={
                'margin': 'auto'
            }
        )])
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
            dcc.Graph(id='stacked-area-chart', className="TETSTTSTSTS"), md=4
        ),
        dbc.Col(
            html.Div(children=[dcc.Graph(id='title-bar-chart'), dcc.RangeSlider(
                id="rangeslider-dates",
                min=0,
                max=no_of_unique_dates,
                updatemode='mouseup',
                step=1,
                value=[0, no_of_unique_dates],
                pushable=2), html.Div(id='div-date-strings-for-rangeslider',
                                      style={"text-align": "center", "display": "inline-block", "width": "100%"})]),
            md=4
        ),
        dbc.Col(
            dcc.Graph(id='tags-chart'), md=4
        )
    ]
)

content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_5'), md=12
        )
    ]
)

content_fourth_row = dbc.Row(
    [
        dbc.Col(
            html.Div(id='div-hidden-div-for-category-clicked'), md=12
        ),
        dbc.Col(
            html.Div(id='div-hidden-div-for-tagchart'), md=12
        ),
        dbc.Col(
            html.Div(id='div-hidden-div-for-rangeslider'), md=12
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


assets_path = os.getcwd() +'/assets'
#app = dash.Dash(__name__,assets_folder=assets_path)

app = dash.Dash(__name__, assets_folder=assets_path, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])

end = datetime.datetime.now()
print("It took " + str((end - start).total_seconds() * 1000) + " miliseconds to set up the dashboard.")


################################################################################################# Helper methods
def find_lower_and_upper_dates_from_rangeslider(date_string_from_hidden_rangeslider_div):
    if date_string_from_hidden_rangeslider_div is not None:
        datestring_array = date_string_from_hidden_rangeslider_div.split("|")
        return datestring_array[0], datestring_array[1]
    else:
        return min_date_string, max_date_string


def update_data_for_titlechart(input_countries, input_categories, slider_interval, date_lower, date_upper):
    date_lower_only_date = date_lower[0:10]
    date_upper_only_date = date_upper[0:10]
    total_titles = 0
    did_use_par_or_bracks = 0
    did_use_caps = 0
    did_use_emojis = 0
    did_not_use_par_or_bracks = 0
    did_not_use_caps = 0
    did_not_use_emojis = 0

    for input_country in input_countries:
        if len(input_categories) == 0:
            if date_lower[0:10] == min_date_string[0:10] and date_upper[0:10] == max_date_string[0:10]:
                current_data_set = "Dataset/Titledata/" + input_country + "/" + input_country + "_title_totals.csv"
                df_for_titlechart = pd.read_csv(current_data_set)

                total_titles += np.array(df_for_titlechart.total_number_of_titles)[0]
                did_use_par_or_bracks += np.array(df_for_titlechart.number_of_titles_with_parenthesis_or_squarebracket_usage)[0]
                did_use_caps += np.array(df_for_titlechart.number_of_titles_with_caps_usage)[0]
                did_use_emojis += np.array(df_for_titlechart.number_of_titles_with_emoji_usage)[0]
            else:
                current_data_set = "Dataset/Titledata/" + input_country + "/" + input_country + "_allcategories_totals_per_day.csv"
                df_for_titlechart = pd.read_csv(current_data_set)
                mask = (df_for_titlechart['date'] > date_lower) & (
                            df_for_titlechart['date'] < date_upper)
                df_for_titlechart = df_for_titlechart.loc[mask]

                for index, row in df_for_titlechart.iterrows():
                    total_titles += row['total_number_of_titles']
                    did_use_par_or_bracks += row['number_of_titles_with_parenthesis_or_squarebracket_usage']
                    did_use_caps += row['number_of_titles_with_caps_usage']
                    did_use_emojis += row['number_of_titles_with_emoji_usage']
        else:
            for input_category in input_categories:
                category_id = category_names_to_ids_dict[input_category]
                current_data_set = "Dataset/Titledata/" + input_country + "/" + input_country + "_category" + str(
                    category_id) + "_totals_per_day.csv"
                file_exists = exists(current_data_set)
                if file_exists:
                    df_for_titlechart = pd.read_csv(current_data_set)
                else:
                    continue

                mask = (df_for_titlechart['date'] > date_lower) & (
                            df_for_titlechart['date'] < date_upper)
                df_for_titlechart = df_for_titlechart.loc[mask]

                for index, row in df_for_titlechart.iterrows():
                    total_titles += row['total_number_of_titles']
                    did_use_par_or_bracks += row['number_of_titles_with_parenthesis_or_squarebracket_usage']
                    did_use_caps += row['number_of_titles_with_caps_usage']
                    did_use_emojis += row['number_of_titles_with_emoji_usage']
    did_use_par_or_bracks = (did_use_par_or_bracks / total_titles) * 100 if total_titles > 0 else 0
    did_use_caps = (did_use_caps / total_titles) * 100 if total_titles > 0 else 0
    did_use_emojis = (did_use_emojis / total_titles) * 100 if total_titles > 0 else 0

    did_not_use_par_or_bracks = 100 - did_use_par_or_bracks if total_titles > 0 else 0
    did_not_use_caps = 100 - did_use_caps if total_titles > 0 else 0
    did_not_use_emojis = 100 - did_use_emojis if total_titles > 0 else 0

    return total_titles, did_use_par_or_bracks, did_use_caps, did_use_emojis, did_not_use_par_or_bracks, did_not_use_caps, did_not_use_emojis


def top_n_tags(cooccurrence, regions, categories, startdate, enddate, title_filter_string, n=10):
    if title_filter_string != "":
        title_chart_string_to_array = title_filter_string.split("|")
        title_chart_column = title_chart_string_to_array[0]
        title_chart_boolean = bool(title_chart_string_to_array[1])
        values = cooccurrence.df.loc[(cooccurrence.df["region"].isin(regions)) & (cooccurrence.df["tagged"]) & (
            cooccurrence.df["category_text"].isin(categories)) & (
                                                 pd.to_datetime(cooccurrence.df["trending_date"]) >= startdate) & (
                                                 pd.to_datetime(cooccurrence.df["trending_date"]) <= enddate) & (
                                                 cooccurrence.df[title_chart_column] == title_chart_boolean)]["tags"]
    else:
        values = cooccurrence.df.loc[(cooccurrence.df["region"].isin(regions)) & (cooccurrence.df["tagged"]) & (
            cooccurrence.df["category_text"].isin(categories)) & (
                                                 pd.to_datetime(cooccurrence.df["trending_date"]) >= startdate) & (
                                                 pd.to_datetime(cooccurrence.df["trending_date"]) <= enddate)]["tags"]
    cooccurrence.tags_occurrence_dict.clear()
    cooccurrence.tags_occurrence_dict = {cooccurrence.unique_tags[i]: 0 for i in
                                         range(0, len(cooccurrence.unique_tags))}
    for tags in values:
        for tag in tags.split("|"):
            cooccurrence.tags_occurrence_dict[tag] += 1
    return dict(Counter(cooccurrence.tags_occurrence_dict).most_common(n))


################################################################################################# Callbacks
@app.callback(
    dash.dependencies.Output('stacked-area-chart', 'figure'),
    [dash.dependencies.Input('countries-drop-down', 'value'),
     Input('filter_time', 'value'),
     Input("rangeslider-dates", "value"),
     Input("div-hidden-div-for-rangeslider", "children"),
     dash.dependencies.Input('categories-drop-down', 'value')])
def update_graph(regionInput, timeInput, slider_interval, date_string_from_hidden_rangeslider_div, categoryInput):
    date_lower, date_upper = find_lower_and_upper_dates_from_rangeslider(date_string_from_hidden_rangeslider_div)
    if date_lower[0:10] == min_date_string[0:10] and date_upper[0:10] == max_date_string[0:10]:
        date_lower = df.trending_date.min()
        date_upper = df.trending_date.max()
    print("Callback for stacked area chart has been called")
    ctx = dash.callback_context

    selected_regions = regionInput
    selected_time_format = timeInput
    selected_categories = categoryInput

    fig = go.Figure()
    if selected_regions:
        total_videos_for_region = df.loc[(df.region.isin(selected_regions)) & (
                    df.trending_date >= pd.to_datetime(unique_dates[slider_interval[0]])) & (
                                                     df.trending_date <= pd.to_datetime(
                                                 unique_dates[slider_interval[1] - 1])), selected_time_format]
        # videos_that_match = df.loc[(df.category_text.isin(selected_categories)) & (df.region.isin(selected_regions)) & (df.trending_date >= pd.to_datetime(unique_dates[slider_interval[0]])) & (df.trending_date <= pd.to_datetime(unique_dates[slider_interval[1] - 1])), selected_time_format]
        total_videos_for_region = total_videos_for_region.value_counts()
        total_videos_for_region = total_videos_for_region.sort_index()
        color_count = 0
        for categories in selected_categories:
            region_count = 0
            for region in selected_regions:
                # total_videos_for_region = df.loc[(df.region == region) & (df.trending_date >= pd.to_datetime(unique_dates[slider_interval[0]])) & (df.trending_date <= pd.to_datetime(unique_dates[slider_interval[1] - 1])), selected_time_format]
                videos_that_match = df.loc[(df.category_text == categories) & (df.region == region) & (
                            df.trending_date >= pd.to_datetime(unique_dates[slider_interval[0]])) & (
                                                       df.trending_date <= pd.to_datetime(
                                                   unique_dates[slider_interval[1] - 1])), selected_time_format]
                if (region_count == 0):
                    videos_that_match_count = videos_that_match.value_counts()
                    region_count += 1;
                else:
                    videos_that_match_count += videos_that_match.value_counts()

                videos_that_match_count = videos_that_match_count.sort_index()

            x = videos_that_match_count.index
            y_temp = (videos_that_match_count / total_videos_for_region) * 100
            y = y_temp.values

            color_count += 1
            fig.add_trace(go.Scatter(
                x=x,
                y=y,
                customdata=videos_that_match_count,
                mode='lines',
                name=categories,
                line=dict(width=0.5, color=available_colors[color_count - 1]),
                stackgroup='one'  # define stack group
                # groupnorm='percent' # sets the normalization for the sum of the stackgroup
            ))

        fig.update_layout(
            # title = "Trending YouTube data for " + str(selected_regions) + " in " + str(selected_categories),
            title="Categories",
            title_font_size=20, legend_font_size=10,
            showlegend=True,
            hovermode="closest",
            hoverdistance=500,
            yaxis=dict(type='linear', ticksuffix='%')
        )

        fig.update_xaxes(
            title_text='Date',
            title_font=dict(size=15, family='Verdana', color='black'),
            tickfont=dict(family='Calibri', color='black', size=12),
            rangeslider_visible=True,
            range=[date_lower, date_upper],
            rangeslider=dict(
                autorange=True,
                range=[date_lower, date_upper]
            )
        )

        fig.update_yaxes(
            title_text="Number of videos(%)",
            title_font=dict(size=15, family='Verdana', color='black'),
            tickfont=dict(family='Calibri', color='black', size=12))

    return fig


@app.callback(
    Output('div-hidden-div-for-rangeslider', 'children'),
    Input('stacked-area-chart', 'relayoutData'),
    prevent_initial_call=True)
def rangeslider_on_change(relayoutdata):
    if "xaxis.range" in relayoutdata:
        xaxis_range = relayoutdata["xaxis.range"]
        return str(xaxis_range[0]) + "|" + str(xaxis_range[1])
    else:
        return min_date_string + "|" + max_date_string


@app.callback(
    Output('title-bar-chart', 'figure'),
    Input("countries-drop-down", "value"),
    Input("categories-drop-down", "value"),
    Input("rangeslider-dates", "value"),
    Input("div-hidden-div-for-rangeslider", "children"),
    Input("div-hidden-div-for-category-clicked", "children"))
def update_title_chart(input_countries, input_categories, slider_interval, date_string_from_hidden_rangeslider_div, category_selected_from_stacked_area_chart):
    print("Callback for title chart has been called")
    date_lower, date_upper = find_lower_and_upper_dates_from_rangeslider(date_string_from_hidden_rangeslider_div)
    input_categories_array = input_categories
    if category_selected_from_stacked_area_chart != "":
        input_categories_array = [category_selected_from_stacked_area_chart]
    total_titles, did_use_par_or_bracks, did_use_caps, did_use_emojis, did_not_use_par_or_bracks, did_not_use_caps, did_not_use_emojis = update_data_for_titlechart(
        input_countries, input_categories_array, slider_interval, date_lower, date_upper)

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Yes", x=['Did use () or []', 'Did use CAPS', 'Did use emojis'],
                         y=[did_use_par_or_bracks, did_use_caps, did_use_emojis], marker_color='rgb(44, 127, 184)'))
    fig.add_trace(go.Bar(name="No", x=['Did use () or []', 'Did use CAPS', 'Did use emojis'],
                         y=[did_not_use_par_or_bracks, did_not_use_caps, did_not_use_emojis],
                         marker_color='rgb(254, 178, 76)'))

    fig.update_layout(barmode='stack')
    fig.update_layout(yaxis_range=(0, 100))
    fig.update_layout(transition={
        'duration': 500,
        'easing': 'cubic-in-out'
    })
    fig.update_yaxes(
        title_text="Number of videos(%)", range=(0.0, 100), autorange=True,
        title_font=dict(size=15, family='Verdana', color='black'),
        tickfont=dict(family='Calibri', color='black', size=12))
    fig.update_layout(
        title="Titles",
        title_font_size=20, legend_font_size=10,
        showlegend=True,
        yaxis=dict(type='linear', ticksuffix='%'))

    return fig


@app.callback(
    Output('div-date-strings-for-rangeslider', 'children'),
    Input('rangeslider-dates', 'value'))
def settext(slider_interval):
    print("Callback for range slider has been called")
    return unique_dates[slider_interval[0]][0:10] + " - " + unique_dates[slider_interval[1] - 1][0:10]





@app.callback(
    Output('tags-chart', 'figure'),
    Input("countries-drop-down", "value"),
    Input("categories-drop-down", "value"),
    Input("rangeslider-dates", "value"),
    Input("div-hidden-div-for-rangeslider", "children"),
    Input("div-hidden-div-for-category-clicked", "children"),
    Input("div-hidden-div-for-tagchart", "children"))
def update_tags_chart(input_countries, input_categories, slider_interval, date_string_from_hidden_rangeslider_div, category_selected_from_stacked_area_chart, selected_from_title_chart):
    print("Callback for tag chart has been called")
    date_lower, date_upper = find_lower_and_upper_dates_from_rangeslider(date_string_from_hidden_rangeslider_div)
    date_lower_string = date_lower[0:10] + "  00:00:00+00:00"
    date_upper_string = date_upper[0:10] + "  00:00:00+00:00"
    if not debugging:
        input_categories_array = input_categories
        if category_selected_from_stacked_area_chart != "":
            input_categories_array = [category_selected_from_stacked_area_chart]
        top_n_tags_dict = top_n_tags(cooccurrence=cooccurrence, regions=input_countries,
                                     categories=input_categories_array,
                                     startdate=pd.to_datetime(date_lower_string),
                                     enddate=pd.to_datetime(date_upper_string),
                                     title_filter_string=selected_from_title_chart)

        fig = go.Figure(
            go.Bar(x=list(top_n_tags_dict.keys()), y=list(top_n_tags_dict.values()), marker_color='rgb(44, 127, 184)'))

        fig.update_layout(
            title="Tags",
            title_font_size=20, legend_font_size=10,
            showlegend=True,
            hovermode="closest",
            yaxis=dict(type='linear'))

        fig.update_xaxes(
            title_text='Tags',
            title_font=dict(size=15, family='Verdana', color='black'),
            tickfont=dict(family='Calibri', color='black', size=12))

        fig.update_yaxes(
            title_text="Number of videos",
            title_font=dict(size=15, family='Verdana', color='black'),
            tickfont=dict(family='Calibri', color='black', size=12))

        fig.update_layout(showlegend=False)

        return fig
    else:
        return go.Figure(go.Bar(x=["Debugging"], y=[20], marker_color='rgb(44, 127, 184)'))


@app.callback(
    Output('div-hidden-div-for-category-clicked', 'children'),
    Input('stacked-area-chart', 'clickData'),
    State("categories-drop-down", "value"))
def stacked_area_chart_on_click(clickdata, categories):
    if clickdata is not None:
        points = clickdata['points']
        curve_number = points[0]['curveNumber']
        category_text = categories[int(curve_number)]
        return category_text
    else:
        return ""


@app.callback(
    Output('div-hidden-div-for-tagchart', 'children'),
    Input('title-bar-chart', 'clickData'))
def title_chart_on_click(clickdata):
    if clickdata is not None:
        points = clickdata['points']
        curve_number = points[0]['curveNumber']
        point_number = points[0]['pointNumber']
        boolean_answer = not bool(curve_number)
        if point_number == 0:
            return "did_use_parens|" + str(boolean_answer)
        elif point_number == 1:
            return "did_use_caps|" + str(boolean_answer)
        else:
            return "did_use_emojis|" + str(boolean_answer)
    else:
        return ""


print("-------------------> The application is running")
already_loaded_dataset_and_set_up_variables = True
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False, use_reloader=False)
