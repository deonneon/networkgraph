import json
import networkx as nx
from pyvis.network import Network

# List of main characters in Jane Eyre with color groups
characters = {
    "Jane": "#FFFF00",  # Yellow
    "Edward": "#FF0000",  # Red
    "John": "#FF0000",  # Red
    "Diana": "#FF0000",  # Red
    "Mary": "#FF0000",  # Red
    "Helen": "#00FF00",  # Green
    "Bessie": "#0000FF",  # Blue
    "Blanche": "#FFA500",  # Orange
    "Bertha": "#FFA500",  # Orange
    "Fairfax": "#FFFF00",  # Yellow
    "Brocklehurst": "#FFA500",  # Orange
    "Georgiana": "#0000FF",  # Blue
    "Eliza": "#0000FF",  # Blue
    "Temple": "#FFA500",  # Orange
    "Rosamond": "#FF0000",  # Red
    "Richard": "#FFA500",  # Orange
    "Grace": "#FFA500",  # Orange
    "Reed": "#0000FF",  # Blue
    "Lloyd": "#0000FF",  # Blue
}

# Load the character interactions data from the first script
with open("character_interactions.json", "r") as f:
    character_interactions = json.load(f)

# Create a graph using NetworkX
G = nx.Graph()

# Add nodes (characters) with color attributes
for character, color in characters.items():
    G.add_node(character, color=color)

# Add edges based on interactions (convert string keys back to pairs)
for pair_str, weight in character_interactions.items():
    char1, char2 = pair_str.split("-")  # Split the string back into two characters
    G.add_edge(char1, char2, weight=weight)

# Calculate node sizes based on degree centrality
centrality = nx.degree_centrality(G)
node_sizes = {node: 10 + (centrality[node] * 50) for node in G.nodes()}

# Create visualization using Pyvis
net = Network(
    notebook=True, height="750px", width="100%", bgcolor="#222222", font_color="white"
)

# Add nodes and edges to the Pyvis graph
for node in G.nodes(data=True):
    net.add_node(
        node[0],
        label=node[0],
        color=node[1]["color"],
        size=node_sizes[node[0]],
        shadow=False,
        linewidths=0,
    )

# Normalize edge weights
max_weight = max(edge[2]["weight"] for edge in G.edges(data=True))
for edge in G.edges(data=True):
    normalized_weight = 1 + (edge[2]["weight"] / max_weight) * 10
    net.add_edge(edge[0], edge[1], value=normalized_weight)

# Disable node hover highlighting and focus effect
net.set_options(
    """
var options = {
  "nodes": {
    "borderWidth": 0
  }
}
"""
)

# Generate and show the network graph
net.show("jane_eyre_relationships.html")
