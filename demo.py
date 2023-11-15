from semantica.db.db_tools import SemanticaDB
import os
from pathlib import Path
from semantica.utils.parser import parse_files
from semantica.utils.preprocessing import preprocess
from semantica.utils.summarize import SemanticaSummarizer
import gradio as gr


summarizer = SemanticaSummarizer()
db = SemanticaDB("semanticadb")


def search_interface(query):
    ids, paths = db.get_files(query, 2)
    summaries = summarizer.summarize_files(paths)
    texts = ""
    for id, path, summary in zip(ids, paths, summaries):
        texts = texts + f"File: {id}.txt\nPath: {path}\n{summary}\n\n"
    return texts


if __name__ == "__main__":
    # parse pdf files into txt
    try:
        pdf_path = Path(os.path.dirname(__file__)) / "data/pdf_raw"
        txt_path = pdf_path.parent / "extracted"
    except FileNotFoundError:
        print("Base folder not found")
    if not txt_path.exists():
        parse_files(base_folder=str(pdf_path), dst_folder=str(txt_path), num_workers=0)
        print("parsing done.")

    # add data to the collection
    names = os.listdir(txt_path)
    files = [txt_path / name for name in names]
    metadata = [{"file_path": str(file)} for file in files]
    sequences = []
    for file in files:
        sequences.append(preprocess(file_path=file))
    print(f"number of files: {len(sequences)}")
    for id, seq, met in zip(names, sequences, metadata):
        db.add_data(id[:-4], seq, met)
    print("number of files in db:", db.collection.count())

    # get the 5 most similar vectors from db
    QUERY = "what is the wage for broadcast technicians?"
    ids, docs = db.get_texts(QUERY, 2)
    ids, paths = db.get_files(QUERY, 2)

    interface = gr.Interface(fn=search_interface, inputs="text", outputs="text")
    interface.launch()
