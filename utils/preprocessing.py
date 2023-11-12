"""
This module holds implementation of a pipeline for automated preprocessing, given a .txt file.
"""
import os, string, re
from pathlib import Path
from multiprocessing import Pool, cpu_count
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def _tokenize(text: str):
    return word_tokenize(text)


def _cleanup(txt: str):
    # make all characters lower case
    txt = txt.lower()
    # remove numbers
    txt = re.sub(r"\d+", "", txt)
    # remove punctuations
    txt = txt.translate(str.maketrans("", "", string.punctuation))
    # remove white spaces
    txt = txt.strip()

    return txt


def _stp_removal(txt):
    stop_words = set(stopwords.words("english"))
    txt = [tkn for tkn in txt if tkn not in stop_words]
    return txt


def _lemmatize(txt):
    lemmatizer = WordNetLemmatizer()
    txt = [lemmatizer.lemmatize(tkn) for tkn in txt]
    return txt


def preprocess(file_path):
    with open(file_path, "r", encoding="utf8") as f:
        txt = f.read()
    txt = _cleanup(txt)
    txt = _tokenize(txt)
    txt = _stp_removal(txt)
    txt = _lemmatize(txt)

    return txt


# if __name__ == "__main__":
#     pool = Pool(cpu_count())
#     path = Path(os.path.abspath("./data/extracted"))
#     names = os.listdir(path)
#     files = [path / name for name in names]
#     result = pool.map_async(preprocess, files, len(files) // cpu_count()).get()
#     print(len(max(result, key=lambda x: len(x))))
