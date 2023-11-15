from typing import Dict
import chromadb
from pathlib import Path
import os


def add_data(
    collection: chromadb.Collection, ids, embeddings, sequences, metadata: Dict = None
):
    """
    Add data to a collection
    """
    try:
        collection.add(
            ids=ids, embeddings=embeddings, documents=sequences, metadatas=metadata
        )
    except ValueError:
        print("Error adding data to collection")


def get_client_and_collection(name: str):
    path = Path(os.path.dirname(__file__))
    client = chromadb.PersistentClient(str(path))
    collection = client.get_or_create_collection(name)
    return client, collection
