import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Test tokenization
text = "This is a test to verify the NLTK installation."
tokens = word_tokenize(text)
print("Tokens:", tokens)

# Test stopwords
stop_words = set(stopwords.words('english'))
print("Stopwords Example:", [word for word in tokens if word not in stop_words])
