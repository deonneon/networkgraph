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

# List of main characters in Jane Eyre
characters = [
    "Jane",
    "Edward",
    "John",
    "Diana",
    "Mary",
    "Helen",
    "Bessie",
    "Blanche",
    "Bertha",
    "Fairfax",
    "Brocklehurst",
    "Georgiana",
    "Eliza",
    "Temple",
    "Rosamond",
    "Richard",
    "Grace",
    "Reed",
    "Lloyd",
]

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

# Add nodes (characters)
for character in characters:
    G.add_node(character)

# Add edges based on interactions
for (char1, char2), weight in character_interactions.items():
    G.add_edge(char1, char2, weight=weight)

# Create visualization using Pyvis
net = Network(
    notebook=True, height="750px", width="100%", bgcolor="#222222", font_color="white"
)

# Add nodes and edges to the Pyvis graph
for node in G.nodes:
    net.add_node(node, label=node)

for edge in G.edges(data=True):
    net.add_edge(edge[0], edge[1], value=edge[2]["weight"])

# Generate and show the network graph
net.show("jane_eyre_relationships.html")
