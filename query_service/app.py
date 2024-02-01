from flask import Flask, request, jsonify, render_template
import os
import chromadb
from llama_index import VectorStoreIndex, StorageContext, ServiceContext
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.vector_stores import ChromaVectorStore
from llama_index.agent import OpenAIAgent
import logging
import nest_asyncio
nest_asyncio.apply()

app = Flask(__name__)
logger = logging.getLogger(__name__)

INDEX_NAME = os.getenv('INDEX_NAME', 'developers')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'BAAI/bge-base-en-v1.5')

def get_document_data(node):
    # This function should extract the document data from a NodeWithScore object.
    # The implementation will depend on how your NodeWithScore objects store or reference the documents.
    # For example:
    return {
        "score": node.score,
        "node": node.node,  # Replace 'node.document' with the actual way to get the document
        # Include other relevant fields here
    }

def perform_query(query_text, similarity):
    try:
        # Setup for querying with the index
        # Assuming you have a similar setup as in the indexing service
        # ChromaDB Client Setup
        print(f"start query: {query_text}")
        embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
        chroma_client = chromadb.HttpClient(host="chroma", port="8000")

        collection_chroma = chroma_client.get_or_create_collection(INDEX_NAME)
        print(f"collection_chroma: {collection_chroma.count()}")
        # Initialize the vector store with the ChromaDB collection
        vector_store = ChromaVectorStore(chroma_collection=collection_chroma)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        service_context = ServiceContext.from_defaults(embed_model=embed_model)
        # # load your index from stored vectors
        index = VectorStoreIndex.from_vector_store(
            vector_store, storage_context=storage_context, service_context=service_context
        )

        logger.info(f"similarity: {similarity}")
        query_engine = index.as_query_engine(similarity_top_k=similarity)
        # query_engine_tool = QueryEngineTool(
        #     query_engine=query_engine,
        #     metadata=ToolMetadata(
        #         name="sub_question_query_engine",
        #         description="useful for when you want to answer queries that require analyzing multiple SEC 10-K documents for Uber",
        #     ),
        # )
        #tools = [query_engine_tool]
        #agent = OpenAIAgent.from_tools(tools, verbose=True)
        #response = agent.chat(query_text)
        response = query_engine.query(query_text)
        res_txt= str(response)
        print(f"response: {str(response)}")
        documents = [get_document_data(node)["node"].to_dict() for node in response.source_nodes]
        return res_txt, documents
    except Exception as e:
        logger.error(f"Error performing query: {e}")
        return []

@app.route('/query', methods=['POST', 'GET'])
def query_endpoint():
    try:
        query_text = request.json.get('query', '')
        similarity = request.json.get('similarity', 10)
        # Perform the query
        res_txt, documents = perform_query(query_text, similarity)
        return jsonify({"results": documents, "main_res": res_txt}), 200
    except Exception as e:
        logger.error(f"Error processing query request: {e}")
        return jsonify({"error": "An error occurred"}), 500

@app.route('/')
def home():
    return render_template('index.html')
app.run(debug=True, host='0.0.0.0', port=5001)
