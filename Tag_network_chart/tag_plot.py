import dash
import dash.dcc as dcc
import dash.html as html
import networkx as nx
import plotly.graph_objs as go
import pandas as pd
from colour import Color
from datetime import datetime
from textwrap import dedent as d
import json

from make_test_network_graph import make_network_fig

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Tag network"


app = dash.Dash(__name__)


# create graph
def create_tag_network():
    pass


#fig = go.Figure(data=[go.Figure])
    #go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])

# layout
app.layout = html.Div([
    dcc.Graph(
        #id='tag_network_graph'
        figure=make_network_fig()
    )
])


if __name__ == '__main__':
    app.run_server(debug=True, host='localhost', port=8080)
