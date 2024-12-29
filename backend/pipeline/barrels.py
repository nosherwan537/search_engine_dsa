import pickle
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix
import numpy as np

def remake_barrels(self):
        """Creates barrels using LSI."""
        try:
            with open(self.inverted_index_path, 'rb') as f:
                invIndx = pickle.load(f)
        except FileNotFoundError:
            print("Error: Inverted index not found. Cannot create barrels.")
            return

        terms = list(invIndx.keys())
        docs = set(docID for term in invIndx.values() for docID in term.keys())
        term_to_idx = {term: idx for idx, term in enumerate(terms)}
        doc_to_idx = {doc: idx for idx, doc in enumerate(docs)}

        rows, cols, values = [], [], []
        for term, doc_data in invIndx.items():
            for doc, data in doc_data.items():
                rows.append(term_to_idx[term])
                cols.append(doc_to_idx[doc])
                values.append(len(data["pos"]))

        A = csr_matrix((np.array(values, dtype=np.float32), (rows, cols)), shape=(len(terms), len(docs)))

        try:
            with open(self.svd_path, 'rb') as f:
                U, S, Vt = pickle.load(f)
            print("Loaded existing SVD matrices.")
        except FileNotFoundError:
            print("SVD matrices not found. Computing now...")
            k = 150
            U, S, Vt = svds(A, k=k)
            with open(self.svd_path, 'wb') as f:
                pickle.dump((U, S, Vt), f)
            print("SVD matrices computed and saved.")

        barrels = {i: [] for i in range(k)}
        concepts = Vt.T
        for doc_idx, concept_vector in enumerate(concepts):
            top_concepts = np.argsort(concept_vector)[-3:]
            for concept in top_concepts:
                barrels[concept].append(doc_idx)

        top_concepts_per_term = {term: np.argsort(U[term_idx])[-3:] for term, term_idx in term_to_idx.items()}
        with open(self.top_concepts_path, 'wb') as f:
            pickle.dump(top_concepts_per_term, f)

        with open(self.barrels_path, 'wb') as f:
            pickle.dump(barrels, f)

        print("Barrels Created with LSI.")