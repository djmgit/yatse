import string
from typing import List
from .entities import STOPWORDS

def parser(text: str) -> List[str]:

    # get rid of punctuations
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.lower()

    tokens = [token for token in text.split() if token not in STOPWORDS]
    return tokens
