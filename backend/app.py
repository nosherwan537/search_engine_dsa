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

        results = search(query)
        output = []
        for doc_id, score in results:
            doc_info = retrieve_document(doc_id)
            doc_info["score"] = float(score)  # Ensure score is converted to Python float
            output.append(doc_info)

        return jsonify({"results": output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
