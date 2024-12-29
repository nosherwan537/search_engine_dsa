import pipeline
import os
import dotenv

import pipeline.bm25
import pipeline.remake_url
import pipeline.term_vector
dotenv.load_dotenv()

class Pipeline:
    def __init__(self):
        self.file_path = r"D:\search_engine_dsa\search_engine_dsa\medium_articles.csv"
        self.lexicon_path = 'lexicon.pkl'
        self.forward_index_path = 'forward_index.pkl'
        self.inverted_index_path = 'inverted_index.pkl'
        self.cleaned_texts_path = 'cleaned_texts.pkl'
        self.svd_path = 'svd_matrices.pkl'
        self.barrels_path = 'barrels_lsi.pkl'
        self.bm25_path = 'mb25_model.pkl'
        self.urls_path = 'urls.pkl'
        self.term_vector_path = 'term_vector.pkl'
        self.top_concepts_path = 'top_concepts.pkl'
        self.headers = {
            "x-rapidapi-host": "medium2.p.rapidapi.com",
            "x-rapidapi-key": os.getenv('MEDIUM_API_KEY')
        }
    def run(self,docs):
        try:
            print("Preprocessing Documents....")
            id_token_tuples = pipeline.preprocessing.preprocess(self,docs)
            print("Updating Lexicon....")
            pipeline.preprocessing.update_lexicon(self,id_token_tuples)
            print("Updating Indexes....")
            pipeline.indexing.index(self,id_token_tuples)
            print("Remaking Barrels")
            pipeline.barrels.remake_barrels(self)
            print("Remaking Term Vectors and Bm25 model")
            pipeline.term_vector.make_vectors(self)
            pipeline.bm25.remake_model(self)
            pipeline.remake_url.remake_url(self)
        except Exception as e:
            print("Error while adding a document: {e}")
    

