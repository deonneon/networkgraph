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

# Extend the list of main and minor characters in Jane Eyre
character_groups = {
    "yellow": ["Jane", "Edward", "Blanche", "Fairfax", "Bertha", "Richard"],
    "red": ["John", "Diana", "Mary", "Rosamond"],
    "blue": ["Reed", "Eliza", "Georgiana", "Bessie"],
    "green": ["Lloyd", "Helen", "Temple", "Brocklehurst", "Grace"],
}

# Extend the full list of characters
characters = [char for group in character_groups.values() for char in group]

# Manually define relationships between character pairs
relationship_types = {
    # Family
    ("John", "Diana"): "family",
    ("Diana", "Mary"): "family",
    ("John", "Mary"): "family",
    ("Reed", "Georgiana"): "family",
    ("Reed", "Eliza"): "family",
    ("Georgiana", "Eliza"): "family",
    ("Jane", "Reed"): "family",
    ("Edward", "Bertha"): "romantic",  # Past romantic relationship
    ("Jane", "Edward"): "romantic",  # Main romantic relationship
    ("Jane", "John"): "family",
    ("Jane", "Mary"): "family",
    ("Jane", "Diana"): "family",

    # Romantic
    ("Blanche", "Edward"): "romantic",  # One-sided romantic interest
    ("Rosamond", "John"): "romantic",  # John's romantic interest in Rosamond

    # Friendship
    ("Jane", "Helen"): "friendship",
    ("Jane", "Bessie"): "friendship",
    ("Jane", "Diana"): "friendship",
    ("Jane", "Mary"): "friendship",

    # Professional
    ("Jane", "Brocklehurst"): "professional",
    ("Jane", "Fairfax"): "professional",
    ("Brocklehurst", "Helen"): "professional",
    ("Fairfax", "Edward"): "professional",
    ("Jane", "Grace"): "professional",
}

# Define the color of each type of relationship
relationship_colors = {
    "family": "red",
    "romantic": "orange",
    "friendship": "blue",
    "professional": "green",
}

# Using SpaCy to extract sentences and recognize named entities (NER)
doc = nlp(text)

# Dictionary to hold character pair interactions
character_interactions = defaultdict(int)

# Helper function to check if a character is in a sentence
def find_characters_in_sentence(sentence):
    found_characters = []
    for ent in sentence.ents:
        if ent.text in characters:
            found_characters.append(ent.text)
    return found_characters

# Loop through sentences and find interactions between characters
for sent in doc.sents:
    char_in_sent = find_characters_in_sentence(sent)
    if len(char_in_sent) > 1:  # More than one character in the sentence indicates interaction
        for i in range(len(char_in_sent)):
            for j in range(i + 1, len(char_in_sent)):
                pair = tuple(sorted([char_in_sent[i], char_in_sent[j]]))
                character_interactions[pair] += 1

# Create a graph using NetworkX
G = nx.Graph()

# Add nodes (characters) and assign colors based on their groups
for color, char_list in character_groups.items():
    for character in char_list:
        G.add_node(character, color=color)

# Add edges based on interactions and calculate edge weights
for (char1, char2), weight in character_interactions.items():
    if (char1, char2) in relationship_types:
        edge_color = relationship_colors[relationship_types[(char1, char2)]]
    else:
        edge_color = "gray"  # Default color if no relationship type is defined
    G.add_edge(char1, char2, weight=weight, color=edge_color)

# Create visualization using Pyvis
net = Network(notebook=True, height="750px", width="100%", bgcolor="#222222", font_color="white")

# Function to map character to color
def get_color(character):
    for color, chars in character_groups.items():
        if character in chars:
            return color
    return "gray"

# Add nodes with borders and size based on degree of interaction
for node in G.nodes:
    size = G.degree[node] * 2 # Node size based on the number of connections
    color = get_color(node)
    net.add_node(node, label=node, color=color, size=size, borderWidth=2, borderWidthSelected=4)

# Add edges with variable thickness based on interaction frequency
for edge in G.edges(data=True):
    char1, char2, data = edge
    width = data["weight"] * 2  # Scale edge width by interaction weight
    color = data["color"]  # Use the assigned color for relationships
    net.add_edge(char1, char2, value=width, color=color)

# Generate and show the network graph
net.show("jane_eyre_relationships.html")
