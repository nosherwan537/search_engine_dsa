from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from search_and_rank import search, retrieve_document



# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

@app.route('/search', methods=['POST'])
def handle_search():
    try:
        data = request.json
        query = data.get('query', '')
        if not query:
            return jsonify({"error": "No query provided"}), 400
        
        print(f"Received query: {query}")  # Debug: Check the received query

        results = search(query)
        print(f"Search results: {results}")  # Debug: Check the results

        output = []
        for doc_id, score in results:
            doc_info = retrieve_document(doc_id)
            print(f"Document info: {doc_info}")  # Debug: Check the document info
            doc_info["score"] = float(score)
            output.append(doc_info)

        return jsonify({"results": output})

    except Exception as e:
        print(f"Error: {e}")  # Debug: Log the exception
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
