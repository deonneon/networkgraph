import networkx as nx
from pyvis.network import Network
import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

nlp.max_length = 1100000


# Function to extract character relationships from text
def extract_relationships(text):
    doc = nlp(text)
    # This is a simplified example. In reality, you'd need more sophisticated NLP techniques
    # to accurately extract character relationships
    relationships = {}
    for sent in doc.sents:
        names = [ent.text for ent in sent.ents if ent.label_ == "PERSON"]
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                pair = tuple(sorted([names[i], names[j]]))
                relationships[pair] = relationships.get(pair, 0) + 1
    return relationships


# Load the Jane Eyre ebook text
with open("jane_eyre.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Extract relationships
relationships = extract_relationships(text)

# Create a graph
G = nx.Graph()

# Add edges with weights
for (char1, char2), weight in relationships.items():
    G.add_edge(char1, char2, weight=weight)

# Create a Pyvis network
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

# Add nodes to the network
for node in G.nodes():
    net.add_node(node, label=node)

# Add edges to the network
for edge in G.edges(data=True):
    net.add_edge(edge[0], edge[1], value=edge[2]["weight"])

# Set options for the network visualization
net.set_options(
    """
var options = {
  "nodes": {
    "font": {
      "size": 12
    }
  },
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -80000,
      "springLength": 250,
      "springConstant": 0.001
    },
    "minVelocity": 0.75
  }
}
"""
)

# Save the network as an HTML file
net.show("jane_eyre_network.html")
