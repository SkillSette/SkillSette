import os

import chromadb
from chromadb.config import Settings

if __name__ == '__main__':
    # os.environ["ALLOW_RESET"] = "TRUE"  # ALLOW_RESET=TRUE
    # client = chromadb.HttpClient(host='localhost', port="8000",
    #                              settings=Settings(allow_reset=True, anonymized_telemetry=False))
    client = chromadb.HttpClient(host='localhost', port="8000",
                                 settings=Settings(allow_reset=True, anonymized_telemetry=False))

    # client.reset()
    collection = client.get_collection(
        name="developers")  # Get a collection object from an existing collection, by name. Will raise an exception if it's not found.

    collection_dict = collection.get()
    print(collection_dict)
    # for collection in collection_dict['ids']:
    #     print(collection)
    print("done")