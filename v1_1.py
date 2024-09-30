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

# List of main characters in Jane Eyre with color groupings
character_groups = {
    "yellow": ["Jane", "Edward", "Blanche", "Fairfax", "Bertha", "Richard"],
    "red": ["John", "Diana", "Mary", "Rosamond"],
    "blue": ["Reed", "Eliza", "Georgiana", "Bessie"],
    "green": ["Lloyd", "Helen", "Temple", "Brocklehurst", "Grace"],
}

# Flatten the list of characters for easy checking
characters = [char for group in character_groups.values() for char in group]

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
    if (
        len(char_in_sent) > 1
    ):  # More than one character in the sentence indicates interaction
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
    G.add_edge(char1, char2, weight=weight)

# Create visualization using Pyvis
net = Network(
    notebook=True, height="750px", width="100%", bgcolor="#222222", font_color="white"
)


# Function to map character to color
def get_color(character):
    for color, chars in character_groups.items():
        if character in chars:
            return color
    return "gray"


# Add nodes with different sizes based on degree of interaction
for node in G.nodes:
    size = G.degree[node] * 2  # Node size based on the number of connections
    color = get_color(node)
    net.add_node(node, label=node, color=color, size=size)

# Add edges with variable thickness based on interaction frequency
for edge in G.edges(data=True):
    char1, char2, data = edge
    width = data["weight"] * 2  # Scale edge width by interaction weight
    net.add_edge(char1, char2, value=width)

# Generate and show the network graph
net.show("jane_eyre_relationships.html")
