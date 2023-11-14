from typing import Dict
import chromadb


def add_data(collection: chromadb.Collection, embeddings, metadata: Dict = None):
    """
    Add data to a collection
    """
    try:
        collection.add(embeddings=embeddings, metadata=metadata)
    except ValueError:
        print("Error adding data to collection")
