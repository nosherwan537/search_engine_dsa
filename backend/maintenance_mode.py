# in maintainance mode new document will be added to the dataset and barrels and search model will be updated

import pickle
import pipeline
import pipeline.articles
import add_document
import pipeline.barrels
import pipeline.bm25
import pipeline.indexing
import pipeline.preprocessing
import pipeline.remake_url
import pipeline.term_vector
def perform_maintenance():
    with open("new_docs.pkl","rb") as f:
        new_docs = pickle.load(f)
    print("New Documents Loaded")
    # using pipeline to 
    # 1. add documents to medium_articles.csv
    # 2. preprocessing new documents
    # 3. updating lexicon on basis of new document
    # 4. updating forward index to include new document
    # 5. make model, barrels, inverted index, url
    flow = add_document.Pipeline(new_docs)
    docs = pipeline.articles.articles(flow)
    if docs is not None:
        # preprocessing dataset and updating lexicon
        id_token_tuples = pipeline.preprocessing.preprocess(flow,docs)
        pipeline.preprocessing.update_lexicon(flow,id_token_tuples)
        # updating forward index
        pipeline.indexing.index(flow,id_token_tuples)
        # remaking barrels
        pipeline.barrels.remake_barrels(flow)
        # making bm25 model
        pipeline.bm25.remake_model(flow)
        # making term vectors
        pipeline.term_vector.make_vectors(flow)
        # generating the urls
        pipeline.remake_url.remake_url(flow)
    new_docs = []
    with open("new_docs.pkl",'wb') as f:
        pickle.dump(new_docs,f)

perform_maintenance()


    

