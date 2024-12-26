import numpy as np
import pickle
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix

# Load inverted index
with open('inverted_index.pkl', 'rb') as f:
    invIndx = pickle.load(f)

# Build Term-Document Matrix
terms = list(invIndx.keys())  # wordIDs
docs = set(docID for term in invIndx.values() for docID in term.keys())
term_to_idx = {term: idx for idx, term in enumerate(terms)}
doc_to_idx = {doc: idx for idx, doc in enumerate(docs)}

rows, cols, values = [], [], []
for term, doc_data in invIndx.items():
    for doc, data in doc_data.items():
        rows.append(term_to_idx[term])
        cols.append(doc_to_idx[doc])
        values.append(len(data["pos"]))  # Frequency as weight

A = csr_matrix((np.array(values, dtype=np.float32), (rows, cols)), shape=(len(terms), len(docs)))

svd_file = 'svd_matrices.pkl'
try:
    with open(svd_file, 'rb') as f:
        U, S, Vt = pickle.load(f)
    print("Loaded existing SVD matrices.")
except FileNotFoundError:
    print("SVD matrices not found. Computing now...")
    # Compute SVD
    k = 150  # Number of concepts
    U, S, Vt = svds(A, k=k)
    with open(svd_file, 'wb') as f:
        pickle.dump((U, S, Vt), f)
    print("SVD matrices computed and saved.")

# Organize barrels by concepts
barrels = {i: [] for i in range(k)}
concepts = Vt.T  # Rows are documents, columns are concepts
for doc_idx, concept_vector in enumerate(concepts):
    top_concepts = np.argsort(concept_vector)[-3:]  # Top 3 concepts
    for concept in top_concepts:
        barrels[concept].append(doc_idx)

# Precompute top concepts for each term
top_concepts_per_term = {term: np.argsort(U[term_idx])[-3:] for term, term_idx in term_to_idx.items()}
# Save top concepts for quick access
with open('top_concepts.pkl', 'wb') as f:
    pickle.dump(top_concepts_per_term, f)

# Save barrels
with open('barrels_lsi.pkl', 'wb') as f:
    pickle.dump(barrels, f)

print("Barrels Created with LSI")
