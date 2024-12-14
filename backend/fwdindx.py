import pandas as pd
import pickle
allDocs = pd.read_pickle("../cleaned_texts.pkl")             # list of tuples [<tuple(docID,<list>words)>]
lexicon = pd.read_pickle("lexicon.pkl")                   # dictionary {word:wordID}
def encode_hitlist(isAnchor, pos):
    encoded = (isAnchor << 12) | (pos & 0xFFF)
    return bin(encoded)[2:].zfill(13)  # 13 bits (12 for pos, 1 for isAnchor)
# docID and wordID
fwdIndx = {}                                                
# {
#   <int>(docID) : {
#       <int>(wordID): {
#           <string>(HLL) : <int>(frequency),
#           <string>(HL) :  <bitarray>(hitlist)
#                       }
#                  }
# }
for docID, words in allDocs:
    fwdIndx[docID] = {}
    for pos,word in enumerate(words):
        if word[:8] == "httpswww":
            isAnchor = 1
        else:
            isAnchor = 0
        wordID = lexicon.get(word) 
        fwdIndx[docID][wordID] = {"pos":pos,"HL":encode_hitlist(isAnchor,pos)}
print('Forward Index Done')
with open('forward_index.pkl','wb') as f:
    pickle.dump(fwdIndx,f)
print('Forward Index Saved')