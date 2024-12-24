import numpy as np
import pickle
import re
from sklearn.preprocessing import normalize
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
from collections import defaultdict

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
    return tokens, word_ids

def search(query, top_n=10):
    query_tokens, query_ids = preprocess_query(query)
    if not query_ids:
        return []

    candidate_docs = defaultdict(float)
    for word_id in query_ids:
        if word_id is not None:
            concept = np.argmax(U[word_id])
            for doc_id in barrels[concept]:
                candidate_docs[doc_id] += 1  

    query_vector = sum(U[query_id] for query_id in query_ids if query_id is not None)
    query_vector = normalize(query_vector.reshape(1, -1))

    # Calculate semantic relevance and boost title matches
    scores = {}
    for doc_id in candidate_docs.keys():
        try:
            doc_id = int(doc_id)  
            doc_vector = normalize(Vt.T[doc_id].reshape(1, -1))
            semantic_score = np.dot(query_vector, doc_vector.T)[0][0]

            title = str(documents_df.iloc[doc_id]["title"]).lower()
            title_score = sum(1 for token in query_tokens if token in title)

            text = str(documents_df.iloc[doc_id]["text"]).lower()  
            text_score = sum(1 for token in query_tokens if token in text)

            # Combine scores with weights
            scores[doc_id] = (
                2 * title_score  
                + text_score
                + 0.5 * semantic_score  
            )
        except (IndexError, ValueError, KeyError, AttributeError):
            continue

    # Rank documents by final scores
    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return ranked_docs  

def retrieve_document(doc_id):
    try:
        doc_id = int(doc_id)  # Ensure doc_id is an integer
        title = str(documents_df.iloc[doc_id]["title"])
        text = str(documents_df.iloc[doc_id]["text"])
        snippet = " ".join(text.split()[:50])
        return {"title": title, "snippet": snippet}
    except (IndexError, ValueError, KeyError):
        return {"title": f"Document {doc_id}", "snippet": "Snippet unavailable."}