from rank_bm25 import BM25Okapi
import pickle


def remake_model(self):
    # Load cleaned texts
    with open(self.cleaned_texts_path, 'rb') as f:
        cleaned_texts = pickle.load(f)

    # Prepare corpus for BM25
    corpus = [" ".join(tokens) for _, tokens in cleaned_texts]
    tokenized_corpus = [doc.split() for doc in corpus]

    # Initialize BM25
    bm25 = BM25Okapi(tokenized_corpus)

    # Save BM25 model
    with open(self.bm25_path, 'wb') as f:
        pickle.dump(bm25, f)

    print("BM25 model built and saved!")
