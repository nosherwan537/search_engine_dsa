import pickle

# Load the lexicon from the pickle file
with open('lexicon.pkl', 'rb') as f:
    lexicon = pickle.load(f)

# Display the first 10 entries in the lexicon

for word, wordID in list(lexicon.items())[:10]:
    print(f"{word}: {wordID}")
