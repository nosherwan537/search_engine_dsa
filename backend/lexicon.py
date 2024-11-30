import pickle
import pandas as pd
import numpy as np

with open('cleaned_texts.pkl','rb') as f:
    cleaned_texts=pickle.load(f)

def build_lexicon(texts):
    lexicon={}
    wordID=0
    for docID,pos_word in cleaned_texts:
        for pos,word in pos_word:
            if word not in lexicon:
                lexicon[word] = wordID
                wordID+=1
    return lexicon

lexicon=build_lexicon(cleaned_texts)
print("Lexicon size:",len(lexicon))


with open('lexicon.pkl','wb') as f:
    pickle.dump(lexicon,f)

print("Lexicon built!")