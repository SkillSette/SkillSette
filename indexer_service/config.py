from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI') 
DB_NAME = os.getenv('DB_NAME','codespread')
COLLECTION_NAME = os.getenv('COLLECTION_NAME','developers')
INDEX_NAME = os.getenv('INDEX_NAME','default-index')
MODEL_NAME = os.getenv('MODEL_NAME','BAAI/bge-base-en-v1.5')
CHROMA_HOST = os.getenv('CHROMA_HOST', 'localhost')
CHROMA_PORT = os.getenv('CHROMA_PORT', '8000')