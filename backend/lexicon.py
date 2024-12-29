import pickle

with open('../cleaned_texts.pkl','rb') as f: # Load cleaned texts
    cleaned_texts=pickle.load(f)

def build_lexicon(texts): # Build lexicon
    lexicon={}
    wordID=0
    for docID,words in cleaned_texts:
        for word in words:
            if word not in lexicon:
                lexicon[word] = wordID
                wordID+=1
    return lexicon

lexicon=build_lexicon(cleaned_texts) # Build lexicon
print("Lexicon size:",len(lexicon))


with open('lexicon.pkl','wb') as f: # Save lexicon
    pickle.dump(lexicon,f)

print("Lexicon built!")