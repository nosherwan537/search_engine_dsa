import pickle
import os

n = 150

def new_doc(id):
    if os.path.exists("new_docs.pkl") and os.path.getsize("new_docs.pkl") > 0:
        with open("new_docs.pkl", "rb") as f:
            new_docs = pickle.load(f)
    else:
        new_docs = []
    if id in new_docs:
        print("ID already added")
    else:
        new_docs.append(id)
    with open("new_docs.pkl", "wb") as f:
        pickle.dump(new_docs, f)
    
    print(new_docs)

def is_trigger_maintenance():
    with open("new_docs.pkl","rb") as f:
        new_docs = pickle.load(f)
    if len(new_docs) > n:
        return True
    return False



