from flask import Flask, request, jsonify
from flask_cors import CORS
from search_and_rank import search, retrieve_document

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

@app.route('/search', methods=['POST'])
def handle_search():
    try:
        # Parse the incoming JSON request
        data = request.json
        query = data.get('query', '').strip()
        print(f"Received query: {query}")  # Log incoming query

        if not query:
            return jsonify({"error": "No query provided"}), 400

        # Perform the search using the updated implementation
        results = search(query)
        print(f"Search results: {results}")  # Log search results

        if not results:
            return jsonify({"results": [], "message": "No results found for the query."}), 200

        # Format the output with document details
        output = []
        for doc_id, score in results:
            doc_details = retrieve_document(doc_id)  # Get title, snippet, and url for the document
            output.append({
                "title": doc_details["title"],
                "snippet": doc_details["snippet"],
                "score": round(score, 4),  # Round the score for better readability
                "url": doc_details.get("url", "")  # Assuming URL is stored in the document details
            })

        return jsonify({"results": output}), 200

    except Exception as e:
        # Handle any unexpected errors
        print(f"Error: {e}")  # Log error details
        return jsonify({"error": "An error occurred during the search process.", "details": str(e)}), 500

if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)
