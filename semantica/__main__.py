# # run a client of gradio
# from gradio import Interface
# from pathlib import Path
# from multiprocessing import Pool, cpu_count
# import chromadb
# from semantica.utils.parser import parse_files
# from semantica.utils.embedding import embed
# from semantica.utils.preprocessing import preprocess
# from semantica.db.db_methods import add_data
# import os


# # def run(name: str):
# #     return "Hello" + name + "!"


# # if __name__ == "__main__":
# #     #     path = Path(os.path.abspath(os.path.dirname(__file__)))
# #     #     path = path / "data/pdf_raw"
# #     #     client, collection = start(str(path))
# #     interface = Interface(fn=run, inputs="text", outputs="text")
