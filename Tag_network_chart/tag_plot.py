import dash
import dash.dcc as dcc
import dash.html as html
from dash.dependencies import Input, Output
import numpy as np
import os  # my python is in fucking puperty
import networkx as nx
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
from textwrap import dedent as d
import json

from Data_processing.Coocurrence.cooccurrence import CoOccurrence
from Tag_network_chart.make_network_graph import make_network_fig

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = "Tag network"

app = dash.Dash(__name__)

cooccurrence = CoOccurrence()
cooccurrence.generate_occurrences(dtype_co_occurrence=np.uint32)  # network viz master is the cwd for some reason
cooccurrence.generate_graph()
cooccurrence.generate_partition()

layout = nx.drawing.layout.spring_layout(G=cooccurrence.tag_graph)
# fig = go.Figure(data=[go.Figure])
# go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])

# layout
app.layout = html.Div([
    dcc.Graph(
        id='tag_network_graph',
        figure=make_network_fig(cooccurrence.tag_graph, cooccurrence, [], layout, None)
    ),
    dcc.Markdown(
        html.Pre(id="click_data")
    ),
    html.Label("Tag search"),
    dcc.Input(type="text", id="search-box"),
    html.Br(),
    html.Div(id="search-output"),
    html.Br(),
    html.Div(id="fuckyou"),
    html.Br(),
    html.Div(id="click-info")
])


@app.callback(
    Output(component_id="search-output", component_property="children"),
    Input(component_id="search-box", component_property="value")
)
def search_tag(tag_name):
    return 'Output: {}'.format(tag_name)


@app.callback(
    Output(component_id="fuckyou", component_property="children"),
    Input(component_id="tag_network_graph", component_property="selectedData")
)
def update_fig(selectedData):
    try:
        selectedPoints = [selectedData["points"][i]["customdata"] for i in range(len(selectedData["points"]))]
        return 'Output: {}'.format(selectedPoints)
    except:  # not to broad motherfucker
        return 'Output: {}'.format("None")


@app.callback(
    Output(component_id="tag_network_graph", component_property="figure"),
    Input(component_id="tag_network_graph", component_property="selectedData"),
    Input(component_id="search-box", component_property="value")
)
def redraw_fig(selectedData, value):  # shit name
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    selectedPoints = []
    if trigger == "search-box":  # todo bugs when not typing fast enough
        selectedPoints = [str(value)]
    elif trigger == "tag_network_graph":
        if selectedData:
            selectedPoints = [selectedData["points"][i]["customdata"] for i in range(len(selectedData["points"]))]
    return make_network_fig(cooccurrence.tag_graph, cooccurrence, selectedPoints, layout, None)


@app.callback(
    Output(component_id="click-info", component_property="children"),
    Input(component_id="tag_network_graph", component_property="clickData")
)  # todo make table
def selection_info(clickData):
    tag = clickData["points"][0]["customdata"]
    most_viewed = list(cooccurrence.df.loc[list([tag in cooccurrence.df["tags"][i].split("|") for i in range(cooccurrence.df.shape[0])]),["video_id","view_count"]].sort_values("view_count")["video_id"])
    top_5 = most_viewed if len(most_viewed) < 5 else most_viewed[:5]
    output = ["https://www.youtube.com/watch?v=" + elem for elem in top_5]
    return output


if __name__ == '__main__':
    app.run_server(debug=True, host='localhost', port=8080)
