from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os


def init_db():
    uri = os.environ.get("MONGO_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client.developers
