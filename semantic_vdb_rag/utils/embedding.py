"""
This module holds embedding engines
"""
import numpy as np
from sentence_transformers import SentenceTransformer


def embed(sequnce_list: str, model, average: bool = False, char_lim: int = None):
    """
    Embed a list of sentences into possibly one vector by averaging over all the independent vectors.
    """
    model = SentenceTransformer("paraphrase-mpnet-base-v2") if model is None else model
    embeddings = []
    for s in sequnce_list:
        if char_lim is not None and len(s) > char_lim:
            new_sequence_list = []
            partitions = len(s) // char_lim
            for i in range(partitions):
                new_sequence_list.append(s[i * char_lim : (i + 1) * char_lim])
            new_sequence_list.append(s[partitions * char_lim :])
            new_emb = embed(new_sequence_list, model, average=True, char_lim=char_lim)
            embeddings.append(new_emb)
        else:
            emb = model.encode(sequnce_list)
            embeddings.extend(emb)
    return np.mean(embeddings, axis=0) if average else embeddings
