"""
This module holds embedding engines
"""
import os
from sentence_transformers import SentenceTransformer
from semantic_vdb_rag.utils.preprocessing import preprocess
from multiprocessing import Pool, cpu_count
from pathlib import Path
import numpy as np


def embed(sequnce_list: str, model, average: bool = False, char_lim: int = None):
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
