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

def clean_text(text):
    text =re.sub(r'[^\w\s]','',text)
    tokens=word_tokenize(text.lower())
    stop_words=set(stopwords.words('english'))
    return [i for i in tokens if i not in stop_words]

cleaned_texts=[clean_text(text) for text in texts]

with open('cleaned_texts.pkl','wb') as f:
    pickle.dump(cleaned_texts,f)

print("Preprocessing done!")