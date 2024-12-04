import json
import nltk
from nltk.corpus import wordnet as wn
import re

# Download WordNet if not already downloaded
nltk.download('wordnet')
nltk.download('omw-1.4')

# Function to extract synonyms for a given word
def get_synonyms(word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    return list(synonyms)

# Function to extract words, remove duplicates and filter only alphabetic words
def extract_unique_words(text):
    # Use regex to extract words, convert to lowercase, and remove duplicates
    words = set(re.findall(r'\b\w+\b', text.lower()))
    return sorted(words)

# Open and read the JSON file
with open('transformed_species_data.json', 'r') as file:
    data = json.load(file)

# Initialize an empty set to collect all unique words
unique_words = set()

# Iterate through each entry in the JSON file
for entry in data:
    if 'introduction' in entry:
        unique_words.update(extract_unique_words(entry['introduction']))
    if 'sections' in entry:
        unique_words.update(extract_unique_words(entry['sections']))

# Write synonyms for each unique word to the output file
with open('synonyms_output.txt', 'w') as output_file:
    for word in unique_words:
        synonyms = get_synonyms(word)
        if synonyms:  # Only write words with available synonyms
            output_file.write(f"{word}, {', '.join(synonyms)}\n")

print("Synonyms written to synonyms.txt")
