"""
This module hosts a helper function to extract text from pdf files.
"""

import os
from pathlib import Path
from multiprocessing import Pool, cpu_count
import fitz


def _extract_text(v):
    file = v[0]
    base = v[1]
    dst = v[2]
    skp = v[3]

    try:
        with fitz.open(base / file) as doc:
            text = "".join([page.get_text(sort=True) for page in doc])
            if len(text) == 0:
                return
        with open(dst / f"{file[:-4]}.txt", "w", encoding="utf8") as f:
            f.write(text)
        print(f"extracted {file}")
    except (ValueError, RuntimeError) as e:
        if skp:
            if isinstance(e, fitz.fitz.FileDataError):
                print(f"Error: Document {file} has broken file data.")
            elif isinstance(e, fitz.fitz.EmptyFileError):
                print(f"Error: Document {file} is empty.")
            elif isinstance(e, fitz.fitz.FileNotFoundError):
                print(f"Error: Document {file} not found.")
            elif isinstance(e, ValueError):
                print(f"Error: Document {file} might be encrypted")
            else:
                print("Error: An unexpected error has occured")
        else:
            raise e


def _mp_handler(cpus, iterable):
    with Pool(cpus) as p:
        p.map(_extract_text, iterable, len(iterable) // cpus)


def parse_files(
    base_folder: str,
    dst_folder: str = None,
    num_workers: int = None,
    skip_on_err: bool = True,
) -> None:
    """
    Parses PDF documents into TXT files in parallel.

    Parameters
    ----------
        `base_folder:str`
            path to the folder where the PDF files are at
        `dst_folder:str` (optional)
            path to a destination folder. extracted *.txt files will be written here.
            If `None`, base folder will be used.
        `num_workers:int` (optional)
            number of workers for multiprocessing pool. If `None`, number of cpu cores will be used.
        `skip_on_err: bool` (optional)
            whether to skip the file that caused an error.

    Returns
    -------
        None
    """
    base_folder = Path(os.path.abspath(base_folder))
    print(dst_folder)
    dst_folder = (
        base_folder if dst_folder is None else Path(os.path.abspath(dst_folder))
    )
    if dst_folder != base_folder:
        dst_folder.mkdir(parents=True, exist_ok=True)

    files = [file for file in os.listdir(base_folder) if file.endswith(".pdf")]
    vectors = [(file, base_folder, dst_folder, skip_on_err) for file in files]
    _mp_handler(cpu_count() if num_workers is None else num_workers, vectors)
