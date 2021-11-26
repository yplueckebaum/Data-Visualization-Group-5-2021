import plotly.graph_objects as go

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from Data_processing.Coocurrence.cooccurrence import CoOccurrence


# todo: This should support figure import/export using something!
def make_network_fig(graph,cooccurrence : CoOccurrence,edge_weight_min = 5):
    # import graph
    test = cooccurrence.normalize_by_occurrence()
    G = graph#nx.random_geometric_graph(200, 0.125)
    # decide whether or not to plot data points or clusters
    layout = nx.drawing.nx_agraph.pygraphviz_layout(G,prog="sfdp")
    print("test")
    # in case of edges generate x and y of edges
    # None acts as seperator
    edge_x = []
    edge_y = []

    for edge in G.edges.data("weight"):
        if cooccurrence.tag_graph.get_edge_data(*edge)["weight"] >= edge_weight_min:
            x0, y0 = layout[edge[0]]
            x1, y1 = layout[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='text',
        mode='lines')

    # safe x and y of nodes
    node_x = []
    node_y = []
    sizes = []
    size_dict = cooccurrence.normalize_by_occurrence()
    for node in G.nodes():
        x, y = layout[node]
        node_x.append(x)
        node_y.append(y)
        sizes.append(size_dict[cooccurrence.tags_dict_inverse[node]] * 10)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,#sizes
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(cooccurrence.tags_dict_inverse[node])

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    return fig
