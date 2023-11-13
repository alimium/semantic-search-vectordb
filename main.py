import os
from sentence_transformers import SentenceTransformer
import semantic_vdb_rag
from semantic_vdb_rag.utils.preprocessing import preprocess
from semantic_vdb_rag.utils.embedding import embed
from semantic_vdb_rag.utils.parser import parse_files
from multiprocessing import Pool, cpu_count
from pathlib import Path


if __name__ == "__main__":
    base_folder = Path("semantic_vdb_rag/data/pdf_raw")
    dst_folder = base_folder.parent / "extracted"
    num_workers = cpu_count()
    parse_files(base_folder, dst_folder, num_workers)

    model = SentenceTransformer("paraphrase-mpnet-base-v2")
    path = Path(os.path.abspath("./semantic_vdb_rag/data/extracted"))
    names = os.listdir(path)
    files = [path / name for name in names]

    with Pool(cpu_count()) as pool:
        prep = pool.map_async(preprocess, files, len(files) // cpu_count()).get()

    embeddings = []
    for p in prep:
        embeddings.append(embed(p, model, True, 100))

    # TOOD: Add embeddings to db
