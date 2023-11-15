from semantica.db import db_methods
import os
from pathlib import Path
from semantica.utils.parser import parse_files

if __name__ == "__main__":
    # parse pdf files into txt
    pdf_path = Path(os.path.dirname(__file__)) / "data/pdf_raw"
    txt_path = pdf_path.parent / "extracted"
    parse_files(str(pdf_path), num_workers=0)

    client, collection = db_methods.get_client_and_collection("semanticadb")
