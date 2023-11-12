"""
This module holds embedding engines
"""
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-mpnet-base-v2")
