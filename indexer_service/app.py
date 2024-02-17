from flask import Flask, request, jsonify
import os

from indexer import Indexer

app = Flask(__name__)

indexer = Indexer()

@app.route('/index', methods=['POST', 'GET']) 
def index_endpoint():
    if indexer.index_documents():
        return jsonify({"status": "success", "message": "Indexing Done"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to index documents"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
