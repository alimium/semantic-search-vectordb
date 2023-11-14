"""
This module holds implementation of a pipeline for automated preprocessing, given a .txt file.
"""
import string, re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def _cleanup(txt: str):
    # make all characters lower case
    txt = txt.lower()
    # remove white spaces
    txt = txt.strip()
    # remove numbers
    txt = re.sub(r"\d+", "", txt)
    # remove punctuations
    txt = txt.translate(str.maketrans("", "", string.punctuation))
    txt = re.sub(r"(?<!\d)[“’](?!\d)", "", txt)

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
    tokens = sent_tokenize(txt)
    sentences = []
    for t in tokens:
        t = _cleanup(t)
        t = word_tokenize(t)
        t = _stp_removal(t)
        t = _lemmatize(t)
        t = " ".join(t)
        if len(t) > 0:
            sentences.append(t)
    return sentences
