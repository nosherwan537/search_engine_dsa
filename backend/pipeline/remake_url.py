import pandas as pd
import pickle

def remake_url(self):
    documents_df = pd.read_csv(self.file_path)

    with open(self.cleaned_texts_path, 'rb') as f:
        cleaned_texts = pickle.load(f)

    ids = [doc['id'] for doc in cleaned_texts]

    documents_df['id'] = ids

    if 'url' not in documents_df.columns:
        raise ValueError("The CSV file must contain a 'url' column.")

    url_mapping = documents_df[['id', 'url']].dropna().to_dict(orient='records')

    with open(self.urls_path, 'wb') as f:
        pickle.dump(url_mapping, f)

    print(f"URLs and document IDs have been successfully saved to {urls_pkl_path}")
