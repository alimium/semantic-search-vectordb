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
    txt = re.sub(r"(?<!\d)[“’-](?!\d)", "", txt)

    return txt


def _stp_removal(txt):
    stop_words = set(stopwords.words("english"))
    txt = [tkn for tkn in txt if tkn not in stop_words]
    return txt


def _lemmatize(txt):
    lemmatizer = WordNetLemmatizer()
    txt = [lemmatizer.lemmatize(tkn) for tkn in txt]
    return txt


def preprocess(
    file_path=None,
    sequence=None,
    cleanup: bool = True,
    stop_word_removal: bool = True,
    lemmatize: bool = True,
):
    cnt = True
    if file_path is None and sequence is None:
        print("Error: Provide at least one parameter.")
        cnt = False
    elif file_path is None:
        txt = sequence
    elif sequence is None:
        with open(file_path, "r", encoding="utf-8") as f:
            txt = f.read()
    else:
        print("Error: Provide just one of the parameters.")
        cnt = False
    if cnt:
        tokens = sent_tokenize(txt)
        sentences = []
        for t in tokens:
            if cleanup:
                t = _cleanup(t)
            t = word_tokenize(t)
            if stop_word_removal:
                t = _stp_removal(t)
            if lemmatize:
                t = _lemmatize(t)
            t = " ".join(t)
            if len(t) > 0:
                sentences.append(t)
        return sentences
