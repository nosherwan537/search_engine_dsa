import nltk
import re
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

def clean_text(docID, text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text.lower())
    cleaned_tokens = [
        lemmatizer.lemmatize(token) for token in tokens if token not in stop_words
    ]
    return (docID, cleaned_tokens)

def preprocess(self, docs):
    id_token_tuples = []
    try:
       with open(self.cleaned_texts_path, 'rb') as f:
            cleaned_texts = pickle.load(f)
    except FileNotFoundError:
        cleaned_texts = []

    for docID, doc in enumerate(docs):
        text = doc.get("text", "")
        id_token_tuple = clean_text(docID, text)
        cleaned_texts.append(id_token_tuple)
        id_token_tuples.append(id_token_tuple)

    with open(self.cleaned_texts_path, 'wb') as f:
        pickle.dump(cleaned_texts, f)

    print(f"Processed and added {len(docs)} documents.")
    return id_token_tuples

def update_lexicon(self, id_token_tuples):
    try:
        with open(self.lexicon_path, 'rb') as f:
            lexicon = pickle.load(f)
    except FileNotFoundError:
        lexicon = {}

    print("Before:", len(lexicon))
    wordID = len(lexicon)

    for docID, words in id_token_tuples:
        for word in words:
            if word not in lexicon:
                lexicon[word] = wordID
                wordID += 1

    with open(self.lexicon_path, 'wb') as f:
        pickle.dump(lexicon, f)
    print("After:", len(lexicon))
    print("Lexicon updated.")