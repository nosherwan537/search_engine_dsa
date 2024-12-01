import pandas as pd
import re
import pickle
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

df=pd.read_csv(r'C:\Users\D E L L\Documents\search_engine\medium_articles.csv')
texts=df['text'].fillna("").tolist()
stop_words = set(stopwords.words('english'))

def clean_text(docID,text):
    text =re.sub(r'[^\w\s]','',text)
    tokens=word_tokenize(text.lower())
    cleaned_tokens = [i for i in tokens if i not in stop_words]
    return (docID,cleaned_tokens)

cleaned_texts=[clean_text(docID,text) for docID,text in enumerate(texts)]

with open('../cleaned_texts.pkl','wb') as f:
    pickle.dump(cleaned_texts,f)

print("Preprocessing done!")