import pickle
from sklearn.preprocessing import normalize

# Load required files
with open('svd_matrices.pkl', 'rb') as f:
    U, S, Vt = pickle.load(f)

with open('lexicon.pkl', 'rb') as f:
    lexicon = pickle.load(f)

# Create term_to_idx from the lexicon
term_to_idx = {term: idx for idx, term in enumerate(lexicon.keys())}

# Precompute term vectors (in LSI space)
term_vectors = {}
for term, term_idx in term_to_idx.items():
    term_vector = U[term_idx]  # Get the term vector from U matrix
    term_vectors[term] = normalize(term_vector.reshape(1, -1))

# Save term_vectors to a file
with open('term_vectors.pkl', 'wb') as f:
    pickle.dump(term_vectors, f)

print("term_vectors.pkl has been created and saved.")
