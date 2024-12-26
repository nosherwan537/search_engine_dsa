from flask import Flask, request, jsonify
from flask_cors import CORS
from search_and_rank import search, retrieve_document
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Predefined list of search terms or can be fetched from your database
search_terms = [
    # AI/ML
    "machine learning",  
    "deep learning",     
    "artificial intelligence",  
    "natural language processing",  
    "reinforcement learning",  
    "neural networks",   

    # Data Science
    "data science",      
    "data visualization",  
    "data analytics",    
    "big data",          
    "data mining",       

    # Technology
    "blockchain",        
    "quantum computing", 
    "cloud computing",   
    "5G technology",     
    "edge computing",    
    "cybersecurity",     
    "internet of things", 

    # Engineering/Tech
    "robotics",          
    "autonomous vehicles", 
    "smart cities",      
    "augmented reality", 
    "virtual reality",   

    # Science/Tech
    "biotechnology",     
    "genomics",          
    "energy storage",    
    "green technology",  
    "nanotechnology",    

    # Entertainment
    "anime",             
    "horror",            
    "romance",           
    "sci-fi",            
    "thriller",          
    "action",            
    "comedy",            
    "fantasy",           
    "drama",             
    "adventure",         

    # Music
    "music",             
    "pop music",         
    "classical music",   
    "hip-hop music",     
    "rock music",        
    "indie music",       
    "EDM music",         
    "jazz music",        
    "love songs",        
    "romantic music",    

    # Movies
    "action movies",     
    "romantic movies",   
    "horror movies",     
    "sci-fi movies",     
    "comedy movies",     
    "drama movies",      
    "thriller movies",   
    "documentary",       
    "animated movies",   
    "family movies",     

    # Sports
    "soccer",            
    "basketball",        
    "baseball",          
    "cricket",           
    "tennis",            
    "rugby",             
    "hockey",            
    "swimming",          
    "boxing",            
    "esports",           

    # Lifestyle
    "fitness",           
    "healthy living",    
    "travel",            
    "home decor",        
    "cooking",           
    "parenting",         
    "pets",              
    "fashion",           
    "beauty",            
    "gardening",         
]

@app.route('/search_suggestions', methods=['GET'])
def search_suggestions():
    try:
        # Get the prefix query from request args
        query_prefix = request.args.get('query', '').lower().strip()
        logging.debug(f"Received prefix for suggestions: {query_prefix}")

        if not query_prefix:
            return jsonify({"suggestions": []}), 200

        # Find suggestions based on the query prefix
        suggestions = [term for term in search_terms if term.startswith(query_prefix)]

        # Limit the number of suggestions to 5
        suggestions = suggestions[:5]

        return jsonify({"suggestions": suggestions}), 200

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An error occurred while fetching suggestions.", "details": str(e)}), 500


@app.route('/search', methods=['POST'])
def handle_search():
    try:
        # Parse the incoming JSON request
        data = request.json
        query = data.get('query', '').strip()
        logging.debug(f"Received query: {query}")  # Log incoming query

        if not query:
            return jsonify({"error": "No query provided"}), 400

        # Perform the search using the updated implementation
        results = search(query)
        logging.debug(f"Search results: {results}")  # Log search results

        if not results:
            return jsonify({"results": [], "message": "No results found for the query."}), 200

        # Format the output with document details
        output = []
        for doc_id, score in results:
            doc_details = retrieve_document(doc_id)  # Get title, snippet, and url for the document
            if doc_details:
                output.append({
                    "title": doc_details["title"],
                    "snippet": doc_details["snippet"],
                    "score": round(score, 4),  # Round the score for better readability
                    "url": doc_details.get("url", "")  # Assuming URL is stored in the document details
                })

        return jsonify({"results": output, "message": "Search completed successfully."}), 200

    except KeyError as e:
        logging.error(f"Missing expected key: {e}")
        return jsonify({"error": f"Missing expected key: {e}"}), 400
    except ValueError as e:
        logging.error(f"Value error: {e}")
        return jsonify({"error": f"Invalid data: {e}"}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An error occurred during the search process.", "details": str(e)}), 500

if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)
