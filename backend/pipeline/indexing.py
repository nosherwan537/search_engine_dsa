from collections import defaultdict
import pickle

def encode_hitlist(isAnchor, pos):
    encoded = (isAnchor << 12) | (pos & 0xFFF)
    return bin(encoded)[2:].zfill(13)

def convert_defaultdict_to_dict(d):
    if isinstance(d, defaultdict):
        return {key: convert_defaultdict_to_dict(value) for key, value in d.items()}
    return d

def index(self,id_token_tuples):
    # Load existing indices
    with open(self.forward_index_path, "rb") as f:
        fwdIndxMain = pickle.load(f)
    print("opened forward index")
    with open(self.inverted_index_path, "rb") as f:
        invrtdIndx = pickle.load(f)
    print("opened inverted index")
    with open(self.lexicon_path, "rb") as f:
        lexicon = pickle.load(f)

    for docID, tokens in id_token_tuples:
        # Forward index for the current document
        fwdIndx = {docID: {}}
        for pos, word in enumerate(tokens):
            isAnchor = 1 if word[:8] == "httpswww" else 0
            wordID = lexicon.get(word)
            if wordID is not None: 
                fwdIndx[docID][wordID] = {"pos": pos, "HL": encode_hitlist(isAnchor, pos)}
        
        # Update the main forward index
        fwdIndxMain.update(fwdIndx)

        # Update the inverted index
        for wordID, wordData in fwdIndx[docID].items():
            if wordID not in invrtdIndx:
                invrtdIndx[wordID] = defaultdict(lambda: {"pos": [], "HL": []})
            if docID not in invrtdIndx[wordID]:
                invrtdIndx[wordID][docID] = {"pos": [], "HL": []}
            invrtdIndx[wordID][docID]["pos"].append(wordData["pos"])
            invrtdIndx[wordID][docID]["HL"].append(wordData["HL"])

    # Convert defaultdict to a regular dict for saving
    invrtdIndx_dict = convert_defaultdict_to_dict(invrtdIndx)

    # Save updated indices back to files
    with open(self.forward_index_path, "wb") as f:
        pickle.dump(fwdIndxMain, f)
    with open(self.inverted_index_path, "wb") as f:
        pickle.dump(invrtdIndx_dict, f)

    print(f"Forward and Inverted Index Updated for {len(id_token_tuples)} documents.")
