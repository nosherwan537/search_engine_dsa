import pickle
from collections import defaultdict

# Load the forward index
with open('forward_index.pkl', 'rb') as f:
    fwdIndx = pickle.load(f)

# Inverted Index Structure
# {
#     <int>(wordID): {
#         <int>(docID): {
#             "pos": <list>(positions),
#             "HL": <list>(hitlists)
#         }
#     }
# }
invIndx = defaultdict(lambda: defaultdict(lambda: {"pos": [], "HL": []}))

# Build the inverted index
for docID, words in fwdIndx.items():
    for wordID, wordData in words.items():
        # Ensure `pos` and `HL` are lists before extending
        pos = wordData["pos"] if isinstance(wordData["pos"], list) else [wordData["pos"]]
        hl = wordData["HL"] if isinstance(wordData["HL"], list) else [wordData["HL"]]
        
        invIndx[wordID][docID]["pos"].extend(pos)
        invIndx[wordID][docID]["HL"].extend(hl)

print('Inverted Index Built')

# Convert the defaultdict to a regular dictionary before saving
def convert_defaultdict_to_dict(d):
    if isinstance(d, defaultdict):
        d = {key: convert_defaultdict_to_dict(value) for key, value in d.items()}
    return d

# Convert the entire structure
invIndx_dict = convert_defaultdict_to_dict(invIndx)

# Save the inverted index to a pickle file
with open('inverted_index.pkl', 'wb') as f:
    pickle.dump(invIndx_dict, f)

print('Inverted Index Saved')
