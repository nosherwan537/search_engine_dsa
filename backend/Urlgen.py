import pandas as pd
import pickle

documents_csv_path = r"D:\search_engine_dsa\search_engine_dsa\medium_articles.csv"
cleaned_texts_pkl_path = r"D:\search_engine_dsa\search_engine_dsa\cleaned_texts.pkl"
urls_pkl_path = r"D:\search_engine_dsa\search_engine_dsa\urls.pkl"


documents_df = pd.read_csv(documents_csv_path)

with open(cleaned_texts_pkl_path, 'rb') as f:
    cleaned_texts = pickle.load(f)

ids = [doc['id'] for doc in cleaned_texts]

documents_df['id'] = ids

if 'url' not in documents_df.columns:
    raise ValueError("The CSV file must contain a 'url' column.")

url_mapping = documents_df[['id', 'url']].dropna().to_dict(orient='records')

with open(urls_pkl_path, 'wb') as f:
    pickle.dump(url_mapping, f)

print(f"URLs and document IDs have been successfully saved to {urls_pkl_path}")
