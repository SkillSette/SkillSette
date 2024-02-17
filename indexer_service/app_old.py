from flask import Flask, request, jsonify
import os
import chromadb
from pymongo import MongoClient
import certifi
from llama_index import Document, VectorStoreIndex, StorageContext, ServiceContext
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.vector_stores import ChromaVectorStore
from chromadb.config import Settings
# Other necessary imports...

app = Flask(__name__)

# Environment variables
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME', 'codespread')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'developers')
INDEX_NAME = os.getenv('INDEX_NAME', 'default-index')
MODEL_NAME = os.getenv('MODEL_NAME', 'BAAI/bge-base-en-v1.5')


def index_documents():
    try:
        # MongoDB Client Setup
        print("start indexing")
        client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
        collection = client[DB_NAME][COLLECTION_NAME]

        # ChromaDB Client Setup
        chroma_client = chromadb.HttpClient(host="localhost", port="8000",
                                            settings=Settings(allow_reset=True, anonymized_telemetry=False))
        collection_chroma = chroma_client.get_or_create_collection(INDEX_NAME)
        print(f"collection_chroma: {collection_chroma.count()}")
        # Embedding and Indexing Setup
        embed_model = HuggingFaceEmbedding(model_name=MODEL_NAME)
        vector_store = ChromaVectorStore(chroma_collection=collection_chroma)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        service_context = ServiceContext.from_defaults(embed_model=embed_model)

        # Fetch and process documents from MongoDB...
        # Fetch all documents from the collection
        documents = fetch_documents(collection)

        # Indexing documents in ChromaDB
        VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, service_context=service_context,upsert=True
        )

        return True
    except Exception as e:
        print(f"Error indexing documents: {str(e)}")
        return False


def fetch_documents(col):
    try:
        filtered_developers = list(col.find({},
                                            {"_id": 1,
                                             "email": 1,
                                             "first_name": 1,
                                             "last_name": 1,
                                             "topics": 1,
                                             "country": 1,
                                             "github_rate": 1,
                                             "rate_per_hour": 1,
                                             "english_level": 1,
                                             "avatar": 1,
                                             "github_code_level": 1}))
        modified_documents = []

        def extract_topics(document):
            topics = document.get('topics', [])
            return ", ".join([list(topic.keys())[0] for topic in topics if list(topic.values())[0] != 0])

        # Function to extract code languages as a comma-separated string
        def extract_code_languages(document):
            github_code_level = document.get('github_code_level', {})
            return ", ".join(github_code_level.keys())

        for developer in filtered_developers:
            email = developer.get('email', '')
            # Check if required fields exist and are not empty
            required_fields = ['email', 'first_name', 'last_name', 'country', 'english_level', 'github_code_level',
                               'topics']
            if not all(developer.get(field, '') for field in required_fields):
                continue

            first_name = developer.get('first_name', '')
            last_name = developer.get('last_name', '')
            country = developer.get('country', '')
            english_level = developer.get('english_level', '')
            github_rate = round(developer.get('github_rate', ''), 2)
            # Extract topics and code languages
            topics = extract_topics(developer)
            code_languages = extract_code_languages(developer)
            avatar = developer.get('avatar', '')
            if not avatar.startswith('http'):
                avatar = 'https://www.gravatar.com/avatar/05b6d7cc7c662bf81e01b39254f88a49?d=identicon'
            metadata = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "country": country,
                "english_level": english_level,
                "avatar": avatar

                # "rate_per_hour": developer.get('rate_per_hour', ''),
            }
            # Join topics and code languages
            combined_skills = f"{topics}, {code_languages}" if topics and code_languages else topics or code_languages
            # Format text data
            text_data = f"developer {first_name} {last_name} from: {country} with skills: {combined_skills} with english level: {english_level} and rate: {github_rate}"
            document = Document(id=developer['_id'], text=text_data, metadata=metadata)
            modified_documents.append(document)
        return modified_documents
    except Exception as e:
        print(f"Error fetching documents: {str(e)}")
        return []


@app.route('/index', methods=['POST', 'GET'])
def index_endpoint():
    if index_documents():
        return jsonify({"status": "success", "message": "Indexing Done"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to index documents"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
