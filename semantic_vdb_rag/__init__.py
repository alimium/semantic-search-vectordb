import os
from pathlib import Path
from multiprocessing import cpu_count
from semantic_vdb_rag.utils.parser import parse_files
import chromadb

client = chromadb.Client()
# collection = client.get_or_create_collection()
