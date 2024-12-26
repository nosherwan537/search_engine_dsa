from dotenv import load_dotenv
from sklearn.neighbors import NearestNeighbors
import os
import google.generativeai as genai
import numpy as np
from sklearn.preprocessing import normalize
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
from sklearn.decomposition import PCA

# Load necessary data
with open('bm25_model.pkl', 'rb') as f:
    bm25 = pickle.load(f)

with open('lexicon.pkl', 'rb') as f:
    lexicon = pickle.load(f)

with open('barrels_lsi.pkl', 'rb') as f:
    barrels = pickle.load(f)

with open('svd_matrices.pkl', 'rb') as f:
    U, S, Vt = pickle.load(f)

with open('term_vectors.pkl', 'rb') as f:
    term_vectors = pickle.load(f)

# Load Medium articles CSV
documents_df = pd.read_csv("../medium_articles.csv")

# Ensure the DataFrame contains the required columns
required_columns = ['title', 'text', 'url']
if not all(col in documents_df.columns for col in required_columns):
    raise ValueError(f"The CSV file must contain the following columns: {', '.join(required_columns)}")

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Load Gemini API key
# load_dotenv()
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# # Configure Gemini model
# generation_config = {
#     "temperature": 0.7,
#     "top_p": 0.95,
#     "top_k": 40,
#     "max_output_tokens": 256,
#     "response_mime_type": "text/plain",
# }

# model = genai.GenerativeModel(
#     model_name="gemini-1.5-pro",
#     generation_config=generation_config,
# )

# Pre-fit NearestNeighbors model once
nbrs = NearestNeighbors(n_neighbors=10, metric='cosine').fit(Vt.T)

def preprocess_query(query):
    query = re.sub(r'[^\w\s]', '', query.lower())
    tokens = word_tokenize(query)
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return tokens

def retrieve_nearest_docs(query_tokens, top_n=10):
    # Retrieve term vectors for query tokens
    query_vectors = [term_vectors[token] for token in query_tokens if token in term_vectors]
    
    if not query_vectors:
        return []

    # Aggregate query vectors
    query_vector = np.sum(query_vectors, axis=0)

    # Using pre-fitted NearestNeighbors model to find the nearest documents
    distances, indices = nbrs.kneighbors(query_vector.reshape(1, -1))

    return indices[0]

#  Refine query for a specific dataset focusing on semantics and logic
# def expand_query_with_llm(query):
#     try:
#         chat_session = model.start_chat(history=[])
#         llm_response = chat_session.send_message(
#             f"Refine this search query by expanding it with more specific keywords, related terms, and concepts that enhance its meaning and relevance to the topic, without providing explanations. Focus on enhancing the searchability of the query based on its context, query is: {query}"
#         )
#         refined_query = llm_response.text.strip()
#         return refined_query
#     except Exception as e:
#         print(f"Gemini API Error: {e}")
#         return query

def search(query, top_n=10):
    # expanded_query = expand_query_with_llm(query)
    query_tokens = preprocess_query(query)

    # BM25 Scoring
    bm25_scores = bm25.get_scores(query_tokens)

    # Retrieve candidate documents using SVD-based vectors
    candidate_docs = retrieve_nearest_docs(query_tokens, top_n)

    # Combine BM25 and semantic similarity scores
    combined_scores = defaultdict(float)
    
    # BM25 contribution
    for doc_id, bm25_score in enumerate(bm25_scores):
        combined_scores[doc_id] += 0.7 * bm25_score

    # Semantic contribution using precomputed vectors and ANN results
    for doc_id in candidate_docs:
        combined_scores[doc_id] += 0.3 * 1  

    # Rank documents by combined scores
    ranked_docs = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return ranked_docs

def retrieve_document(doc_id):
    try:
        row = documents_df.iloc[doc_id]
        title = str(row["title"])
        text = str(row["text"])
        url = str(row["url"])
        snippet = " ".join(text.split()[:50])
        return {"title": title, "snippet": snippet, "url": url}
    except (IndexError, ValueError, KeyError):
        return {"title": f"Document {doc_id}", "snippet": "Snippet unavailable.", "url": ""}


