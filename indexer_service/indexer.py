import os
import certifi
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME, INDEX_NAME, MODEL_NAME

from llama_index import Document, VectorStoreIndex, StorageContext, ServiceContext
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.vector_stores import MongoDBVectorStore

class Indexer:

    def __init__(self):
       
        # Initialize MongoDB client
        self.mongo_client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())


    def index_documents(self):
        try:
            # MongoDB collection
            collection = self.mongo_client[DB_NAME][COLLECTION_NAME]
            
            # MongoDB vector index
            vector_index = self.mongo_client[DB_NAME][INDEX_NAME]

            # Setup indexing 
            embed_model = HuggingFaceEmbedding(model_name=MODEL_NAME)
            vector_store = MongoDBVectorStore(vector_index)
            storage_context = StorageContext(vector_store=vector_store)
            service_context = ServiceContext(embed_model=embed_model)

            # Fetch and process documents
            documents = self.fetch_documents(collection)

            # Index documents
            VectorStoreIndex.from_documents(
                documents, storage_context=storage_context,
                service_context=service_context, upsert=True
            )

            return True
        
        except Exception as e:
            print(f"Error indexing documents: {str(e)}")
            return False



    def fetch_documents(self, col):
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

            for developer in filtered_developers:
                # Process each document
                email = developer.get('email', '')
                required_fields = ['email', 'first_name', 'last_name', 'country', 'english_level', 'github_code_level', 'topics']
                if not all(developer.get(field, '') for field in required_fields):
                    continue
                
                # Extract fields
                first_name = developer.get('first_name', '') 
                last_name = developer.get('last_name', '')
                country = developer.get('country', '')
                english_level = developer.get('english_level', '')
                github_rate = round(developer.get('github_rate', ''), 2)

                # Extract topics and languages
                topics = self.extract_topics(developer)
                languages = self.extract_code_languages(developer)
                
                # Construct metadata
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
                }

                # Construct text
                skills = f"{topics}, {languages}" if topics and languages else topics or languages 
                text_data = f"developer {first_name} {last_name} from: {country} with skills: {skills} with english level: {english_level} and rate: {github_rate}"
                
                # Create Document object

                document = Document(id=developer['_id'], text=text_data, metadata=metadata)

                modified_documents.append(document)
                return modified_documents

        except Exception as e:
               print(f"Error fetching documents: {str(e)}")
               return []
    def extract_topics(self, document):
        topics = document.get('topics', [])
        return ", ".join([list(topic.keys())[0] for topic in topics if list(topic.values())[0] != 0])

    def extract_code_languages(self, document):
        github_code_level = document.get('github_code_level', {})
        return ", ".join(github_code_level.keys())          