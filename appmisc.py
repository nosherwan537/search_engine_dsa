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
        if not query:
            return jsonify({"error": "No query provided"}), 400

        # Perform the search using the updated implementation
        results = search(query)
        if not results:
            return jsonify({"results": [], "message": "No results found for the query."})

        # Format the output with document details
        output = []
        for result in results:
            output.append({
                "title": result["title"],
                "snippet": result["snippet"],
                "score": round(result["score"], 4)  # Round the score for better readability
            })

        return jsonify({"results": output}), 200

    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": "An error occurred during the search process.", "details": str(e)}), 500


if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)
