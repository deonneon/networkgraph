import json
import networkx as nx
from pyvis.network import Network

# Load the character interactions data from the first script
with open("character_interactions.json", "r") as f:
    character_interactions = json.load(f)

# Create a graph using NetworkX
G = nx.Graph()

# Add edges based on interactions (convert string keys back to pairs)
for pair_str, weight in character_interactions.items():
    char1, char2 = pair_str.split("-")  # Split the string back into two characters
    G.add_edge(char1, char2, weight=weight)

# Create visualization using Pyvis
net = Network(notebook=True)

# Add nodes and edges to the Pyvis graph
net.from_nx(G)

# Generate and show the network graph
net.show("jane_eyre_relationships_basic.html")
