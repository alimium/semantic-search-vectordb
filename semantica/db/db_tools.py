import chromadb
from pathlib import Path
import os
from semantica.utils.embedding import embed
from semantica.utils.preprocessing import preprocess
from chromadb.utils import embedding_functions


class SemanticaDB:
    def __init__(self, name, db_path=None) -> None:
        if db_path is None:
            db_path = Path(os.path.dirname(__file__)) / "files"
        self.client = chromadb.PersistentClient(str(db_path))
        self.collection = self.client.get_or_create_collection(
            name,
            metadata={"hnsw:space": "cosine"},
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                "paraphrase-mpnet-base-v2"
            ),
        )

    def add_data(self, id_, sequences, metadata, custom_embed: bool = True):
        """
        Add data for one file to a collection. A file is a sequence of sentences.
        """
        if len(self.collection.get(id_)["ids"]) == 0:
            text = ". ".join(sequences)
            embedding = embed(sequences)
            try:
                if custom_embed:
                    self.collection.add(
                        [id_],
                        documents=[text],
                        embeddings=[embedding],
                        metadatas=[metadata],
                    )
                else:
                    self.collection.add([id_], documents=[text])
                print(f"File {id_} added to database.")
            except ValueError as e:
                print(f"File {id_} was not added successfully | {e}")
        else:
            print(f"File {id_} already exists in database.")

    def get_files(self, query, n):
        query = preprocess(sequence=query)
        embedded_query = embed(query)
        results = self.collection.query(
            query_embeddings=[embedded_query], n_results=n, include=["metadatas"]
        )
        paths = [p["file_path"] for p in results["metadatas"][0]]
        return results["ids"][0], paths

    def get_texts(self, query, n):
        query = preprocess(sequence=query)
        embedded_query = embed(query)
        results = self.collection.query(
            query_embeddings=[embedded_query], n_results=n, include=["documents"]
        )
        return results["ids"][0], results["documents"][0]
