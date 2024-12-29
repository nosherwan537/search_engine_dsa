import requests
import os
import pandas as pd

def articles(article_urls,self):
    if os.path.exists(self.file_path):
        df = pd.read_csv(self.file_path)
    else:
        df = pd.DataFrame(columns=['title', 'url', 'text', 'authors', 'timestamp', 'tags'])

    for article_url in article_urls:
        metadata_url = f"https://medium2.p.rapidapi.com/article/{article_url}"
        content_url = f"https://medium2.p.rapidapi.com/article/{article_url}/content"

        metadata_response = requests.get(metadata_url, headers=self.headers)
        if metadata_response.status_code == 200:
            metadata_content = metadata_response.json()
            title = metadata_content.get('title', 'No title available')
            url = metadata_content.get('url', 'No URL available')
            authors = metadata_content.get('authors', None)
            timestamp = metadata_content.get('timestamp', None)
            tags = metadata_content.get('tags', None)
        else:
            print(f"Failed to retrieve metadata for URL {article_url}. HTTP Status Code: {metadata_response.status_code}")
            continue

        content_response = requests.get(content_url, headers=self.headers)
        if content_response.status_code == 200:
            content = content_response.json()
            text = content.get('content', 'No content available')
        else:
            print(f"Failed to retrieve content for URL {article_url}. HTTP Status Code: {content_response.status_code}")
            continue

        if url in df['url'].values:
            print(f"Article with URL {url} already exists. Skipping.")
            continue

        new_row = {
            'title': title,
            'url': url,
            'text': text,
            'authors': authors,
            'timestamp': timestamp,
            'tags': tags
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        print(f"Added article: {title}")

    df.to_csv(self.file_path, index=False, encoding='utf-8')
    print("All articles processed and saved to medium_articles.csv.")