import pickle

# Path to your .pkl file
file_path = 'inverted_index.pkl'

# Load the inverted index from the .pkl file
with open(file_path, 'rb') as file:
    inverted_index = pickle.load(file)

# Access the first 20 elements
# Assuming the inverted index is a dictionary
first_20_elements = list(inverted_index.items())[:20]

# Print the first 20 elements
for key, value in first_20_elements:
    print(f"Key: {key}, Value: {value}")
