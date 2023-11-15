# import os
# from pathlib import Path
# from multiprocessing import Pool, cpu_count
# from semantica.utils.parser import parse_files
# from semantica.utils.preprocessing import preprocess
# from semantica.utils.embedding import embed
# from semantica.db.db_methods import add_data
# from sentence_transformers import SentenceTransformer
# import chromadb


# # def start(base_folder_path: str):
# #     try:
# #         base_folder = Path(base_folder_path)
# #         dst_folder = base_folder.parent / "extracted"
# #     except FileNotFoundError:
# #         print("Base folder not found")
# #         return None
# #     if not dst_folder.exists():
# #         num_workers = cpu_count()
# #         parse_files(base_folder, dst_folder, num_workers)
# #         print("parsing done.")

# #     # create a session and get the collection
# #     client = chromadb.Client()
# #     # if client.heartbeat() <= 1000000:
# #     print(client.heartbeat())
# #     collection = client.get_or_create_collection(name="semanticadb")
# #     print("total number of db elements:", collection.count())
# #     # else:
# #     #     print("Connection error")

# #     # add data to the collection
# #     # if collection.count() == 0:
# #     names = os.listdir(dst_folder)
# #     files = [dst_folder / name for name in names]
# #     metadata = [{"file_name": name[1:-4]} for name in names]
# #     ids = [name[1:-4] for name in names]
# #     sequences, embeddings = [], []
# #     n = 1
# #     for file in files[:n]:
# #         sequences.append(preprocess(file))
# #     for seq in sequences:
# #         embeddings.append(list(embed(seq)))
# #     print(f"number of files: {len(sequences)} - number of embeddings: {len(embeddings)}")
# #     add_data(collection, ids[:n], embeddings, sequences, metadata[:n])

# #     return client, collection


# # path = Path(os.path.abspath(os.path.dirname(__file__)))
# # path = path / "data/pdf_raw"
# # client, collection = start(str(path))
# # print("initialization done.")
# # print("total number of db elements:", collection.count())
