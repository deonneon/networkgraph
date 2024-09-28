import spacy
import networkx as nx
from pyvis.network import Network
from collections import defaultdict

# Load SpaCy's English NLP model
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 1100000

# Load the ebook (replace with your Jane Eyre text)
with open("jane_eyre.txt", "r", encoding="utf-8") as file:
    text = file.read()

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

# ... (keep the existing code for processing text and finding interactions)

# Create a graph using NetworkX
G = nx.Graph()

# Add nodes (characters) with color attributes
for character, color in characters.items():
    G.add_node(character, color=color)

# Add edges based on interactions
for (char1, char2), weight in character_interactions.items():
    G.add_edge(char1, char2, weight=weight)

# Calculate node sizes based on degree centrality
centrality = nx.degree_centrality(G)
node_sizes = {node: 10 + (centrality[node] * 50) for node in G.nodes()}

# Create visualization using Pyvis
net = Network(notebook=True, height="750px", width="100%", bgcolor="#222222", font_color="white")

# Customize physics options
net.force_atlas_2based(gravity=-50, central_gravity=0.01, spring_length=100, spring_strength=0.08, damping=0.4, overlap=0)

# Add nodes and edges to the Pyvis graph
for node in G.nodes(data=True):
    net.add_node(node[0], label=node[0], color=node[1]['color'], size=node_sizes[node[0]])

# Normalize edge weights
max_weight = max(edge[2]['weight'] for edge in G.edges(data=True))
for edge in G.edges(data=True):
    normalized_weight = 1 + (edge[2]['weight'] / max_weight) * 10
    net.add_edge(edge[0], edge[1], value=normalized_weight, color="#FFFFFF")

# Additional customization options
net.set_options("""
var options = {
  "nodes": {
    "font": {
      "size": 20
    }
  },
  "edges": {
    "color": {
      "inherit": true
    },
    "smooth": false
  },
  "physics": {
    "forceAtlas2Based": {
      "gravitationalConstant": -50,
      "centralGravity": 0.01,
      "springLength": 100,
      "springConstant": 0.08,
      "damping": 0.4,
      "avoidOverlap": 0
    },
    "minVelocity": 0.75,
    "solver": "forceAtlas2Based"
  }
}
""")

# Generate and show the network graph
net.show("jane_eyre_relationships.html")