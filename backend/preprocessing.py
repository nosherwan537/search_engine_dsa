import pandas as pd
import re
import pickle
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

df=pd.read_csv("../medium_articles.csv")
texts=df['text'].fillna("").tolist()
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(docID,text):
    text =re.sub(r'[^\w\s]','',text)
    tokens=word_tokenize(text.lower())
    cleaned_tokens = [
        lemmatizer.lemmatize(token) for token in tokens if token not in stop_words
    ] 
    return (docID,cleaned_tokens)

cleaned_texts=[clean_text(docID,text) for docID,text in enumerate(texts)]

with open('../cleaned_texts.pkl','wb') as f:
    pickle.dump(cleaned_texts,f)

print("Preprocessing done!")