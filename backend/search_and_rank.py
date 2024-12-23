import numpy as np
import pickle
import re
from sklearn.preprocessing import normalize
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load necessary data
with open('lexicon.pkl', 'rb') as f:
    lexicon = pickle.load(f)

with open('barrels_lsi.pkl', 'rb') as f:
    barrels = pickle.load(f)

with open('svd_matrices.pkl', 'rb') as f:
    U, S, Vt = pickle.load(f)

documents_df = pd.read_csv("../medium_articles.csv")

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_query(query):
    query = re.sub(r'[^\w\s]', '', query.lower())
    tokens = word_tokenize(query)
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    word_ids = [lexicon.get(token) for token in tokens if token in lexicon]
    return word_ids

def search(query, top_n=10):
    query_ids = preprocess_query(query)
    if not query_ids:
        return []

    candidate_docs = set()
    for word_id in query_ids:
        if word_id is not None:
            concept = np.argmax(U[word_id])
            candidate_docs.update(barrels[concept])

    scores = {}
    for doc_id in candidate_docs:
        doc_vector = Vt.T[doc_id]
        query_vector = sum(U[query_id] for query_id in query_ids if query_id is not None)
        score = np.dot(doc_vector, query_vector) / (np.linalg.norm(doc_vector) * np.linalg.norm(query_vector))
        scores[doc_id] = score

    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return ranked_docs

def retrieve_document(doc_id):
    try:
        title = documents_df.iloc[doc_id]["title"]
        text = documents_df.iloc[doc_id]["text"]
        snippet = " ".join(text.split()[:50])
        return {"title": title, "snippet": snippet}
    except IndexError:
        return {"title": f"Document {doc_id}", "snippet": "Snippet unavailable."}
