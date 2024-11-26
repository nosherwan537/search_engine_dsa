import pandas as pd
from concurrent.futures import ProcessPoolExecutor

# Load data and lexicon
data = pd.read_pickle(r"C:\Users\D E L L\Documents\search_engine\cleaned_texts.pkl")
lexicon = list(pd.read_pickle(r"C:\Users\D E L L\Documents\search_engine\lexicon.pkl"))
lexicon = {word: index for index, word in enumerate(lexicon)}

# Function to process a single document
def process_document(documentID, document):
    fwdIndx_data = []
    hitlists_document = {}

    for position, word in enumerate(document):
        word_id = lexicon.get(word)
        if word_id is not None:
            hitlists_document.setdefault(word_id, []).append(position)

    # Prepare data for DataFrame
    for word_id, positions in hitlists_document.items():
        fwdIndx_data.append((documentID, word_id, len(positions), positions))

    return fwdIndx_data

def process_documents(data):
    with ProcessPoolExecutor() as executor:
        results = executor.map(process_document, range(len(data)), data)

    fwdIndx_data = [item for sublist in results for item in sublist]
    return fwdIndx_data

# Process the documents and gather the data
fwdIndx_data = process_documents(data)

# Create a DataFrame from the processed data
fwdIndx = pd.DataFrame(fwdIndx_data, columns=['docID', 'wordID', 'hitlist_length', 'hitlist'])


fwdIndx.set_index(['docID', 'wordID'], inplace=True)
fwdIndx.to_parquet(r"C:\Users\D E L L\Documents\search_engine\forward_index.parquet", index=True)
sampleFwdIndx = fwdIndx.head(10)
sampleFwdIndx.to_parquet(r"C:\Users\D E L L\Documents\search_engine\sample\forward_index_parquet.csv", index=True)
