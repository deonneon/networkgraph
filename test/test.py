import networkx as nx
from pyvis.network import Network
import random

# Create a NetworkX graph
G = nx.Graph()

# Add nodes with different sizes
G.add_node(1, label="Node 1", size=30)
G.add_node(2, label="Node 2", size=40)
G.add_node(3, label="Node 3", size=50)
G.add_node(4, label="Node 4", size=60)

# Add edges
G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(2, 4)
G.add_edge(3, 4)

# Create a PyVis network
net = Network(notebook=True)

# Add the NetworkX graph to the PyVis network
net.from_nx(G)

# Customize the graph appearance
net.toggle_physics(True)
net.show_buttons(filter_=["physics"])

# Generate the HTML file
net.show("example_graph.html")
