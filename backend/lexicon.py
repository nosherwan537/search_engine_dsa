import pickle
import pandas as pd
import numpy as np

with open('cleaned_texts.pkl','rb') as f:
    cleaned_texts=pickle.load(f)

def build_lexicon(texts):
    lexicon=set()
    word_id=0
    for text in cleaned_texts:
        for word in text:
            if word not in lexicon:
                lexicon.add(word)
                word_id+=1
    return lexicon

lexicon=build_lexicon(cleaned_texts)
print("Lexicon size:",len(lexicon))


with open('lexicon.pkl','wb') as f:
    pickle.dump(lexicon,f)

print("Lexicon built!")