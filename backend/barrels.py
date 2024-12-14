import numpy as np
import pickle
from scipy.sparse.linalg import svds

# Load inverted index
with open('inverted_index.pkl', 'rb') as f:
    invIndx = pickle.load(f)

# Step 1: Build Term-Document Matrix
# Use a sparse matrix for efficiency
from scipy.sparse import csr_matrix

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

# Convert the sparse matrix to a floating-point data type
A = csr_matrix((np.array(values, dtype=np.float32), (rows, cols)), shape=(len(terms), len(docs)))


# Step 2: Perform SVD
k = 100  # Number of concepts
U, S, Vt = svds(A, k=k)

# Step 3: Organize barrels by concepts
barrels = {i: [] for i in range(k)}
concepts = Vt.T  # Rows are documents, columns are concepts
for doc_idx, concept_vector in enumerate(concepts):
    top_concept = np.argmax(concept_vector)  # Assign document to its strongest concept
    barrels[top_concept].append(doc_idx)

# Save barrels
with open('barrels_lsi.pkl', 'wb') as f:
    pickle.dump(barrels, f)

print("Barrels Created with LSI")
