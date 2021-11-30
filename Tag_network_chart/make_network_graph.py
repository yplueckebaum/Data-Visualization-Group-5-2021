import plotly.graph_objects as go

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from Data_processing.Coocurrence.cooccurrence import CoOccurrence


# todo: This should support figure import/export using something!
def make_network_fig(graph, cooccurrence: CoOccurrence, node_selection, layout, edge_degree_min=5):
    # import graph
    G = graph  # nx.random_geometric_graph(200, 0.125)
    # decide whether or not to plot data points or clusters
    # in case of edges generate x and y of edges
    # None acts as seperator

    # safe x and y of nodes
    node_x = []
    node_y = []
    sizes = []
    node_text = []
    size_dict = cooccurrence.normalize_by_occurrence()
    edge_nodes = {i: False for i in G.nodes}
    node_degree = []

    if node_selection:
        nodes = [cooccurrence.tags_dict[node_selection[i]] for i in range(len(node_selection))]
        for node in nodes:
            if G.degree(node) >= edge_degree_min:
                edge_nodes[node] = True
            else:
                edge_nodes[node] = False
    for node in G.nodes:
        x, y = layout[node]
        node_x.append(x)
        node_y.append(y)
        sizes.append(size_dict[cooccurrence.tags_dict_inverse[node]] * 10)
        node_text.append(cooccurrence.tags_dict_inverse[node])

        node_degree.append(G.degree(node))  # todo ?
    if node_selection:
        displayed_tags = list({i: (node_text[i] if node_text[i] in node_selection else "") for i in
                               range(len(node_text))}.values())  # todo terrible terrible coding #todo THIS IS IT
    else:
        displayed_tags = []
    edge_x = []
    edge_y = []

    for edge in G.edges.data("weight"):
        if node_selection:  # todo refractor
            if edge_nodes[edge[0]] and edge_nodes[edge[1]]:
                x0, y0 = layout[edge[0]]
                x1, y1 = layout[edge[1]]
                edge_x.append(x0)
                edge_x.append(x1)
                edge_x.append(None)
                edge_y.append(y0)
                edge_y.append(y1)
                edge_y.append(None)
        else:
            x0, y0 = layout[edge[0]]
            x1, y1 = layout[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='text+markers',
        text=displayed_tags,
        textposition="top center",
        hoverinfo='text',
        hovertext=node_text,
        customdata=node_text,
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,  # sizes
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='text',
        mode='lines')



    node_adjacencies = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))

    node_trace.marker.color = node_adjacencies
    # node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        clickmode='event+select')
                    )
    return fig
