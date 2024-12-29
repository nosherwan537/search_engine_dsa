import requests
import os
import pandas as pd

def articles(self):
    if os.path.exists(self.file_path):
        df = pd.read_csv(self.file_path)
        print("opened medium_articles.csv")
    else:
        df = pd.DataFrame(columns=['title', 'url', 'text', 'authors', 'timestamp', 'tags'])
    
    docs = []
    all_articles_exist = True  # Flag to check if all articles already exist in the dataset
    
    for article_url in self.ids:
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
            continue  # Skip this article and move on to the next

        content_response = requests.get(content_url, headers=self.headers)
        if content_response.status_code == 200:
            content = content_response.json()
            text = content.get('content', 'No content available')
        else:
            print(f"Failed to retrieve content for URL {article_url}. HTTP Status Code: {content_response.status_code}")
            continue  # Skip this article and move on to the next

        # Check if the article already exists in the dataset
        if url in df['url'].values:
            print(f"Article with URL {url} already exists. Skipping.")
            continue  # Skip this article, but keep processing the rest
        
        # If we find an article that is not in the dataset, we set the flag to False
        all_articles_exist = False
        
        # Add the new article to the docs list
        new_row = {
            'title': title,
            'url': url,
            'text': text,
            'authors': authors,
            'timestamp': timestamp,
            'tags': tags
        }
        docs.append(new_row)

        # Add the new article to the DataFrame
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        print(f"Added article: {title}")

    # If no new articles were added, return None
    if all_articles_exist:
        print("All articles already exist in the dataset. Returning None.")
        return None

    # Save the updated DataFrame to the CSV file
    df.to_csv(self.file_path, index=False, encoding='utf-8')
    print("medium_articles.csv saved")

    # Return the docs with new articles
    return docs
