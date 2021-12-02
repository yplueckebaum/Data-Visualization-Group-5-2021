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
from make_network_graph import make_network_fig

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Tag network"

app = dash.Dash(__name__)

cooccurrence = CoOccurrence()
cooccurrence.generate_occurrences(dtype_co_occurrence=np.uint32)  # network viz master is the cwd for some reason
cooccurrence.generate_graph()

layout = nx.drawing.layout.kamada_kawai_layout(G=cooccurrence.tag_graph)

# fig = go.Figure(data=[go.Figure])
# go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])

# layout
app.layout = html.Div([
    dcc.Graph(
        id='tag_network_graph',
        figure=make_network_fig(cooccurrence.tag_graph, cooccurrence, [], layout, None, 0)
    ),
    dcc.Markdown(
        html.Pre(id="click_data")
    ),
    html.Label("Tag search"),
    dcc.Input(type="text", id="search-box"),
    html.Br(),
    html.Div(id="search-output"),
    html.Br(),
    html.Div(id="fuckyou")
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
    Input(component_id="search-box", component_property="value"),
    Input(component_id="tag_network_graph", component_property="clickData")
)
def redraw_fig(selectedData, value, clickData):  # shit name
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    if trigger == "search-box":
        return make_network_fig(cooccurrence.tag_graph, cooccurrence, [str(value)], layout, None, 0)
    elif trigger:
        if selectedData:
            selectedPoints = [selectedData["points"][i]["customdata"] for i in range(len(selectedData["points"]))]
        else:
            selectedPoints = []
        return make_network_fig(cooccurrence.tag_graph, cooccurrence, selectedPoints, layout, None, 0)


if __name__ == '__main__':
    app.run_server(debug=True, host='localhost', port=8080)
