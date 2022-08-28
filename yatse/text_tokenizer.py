import string
from typing import List
from .entities import STOPWORDS

def parser(text: str) -> List[str]:
    """
    Function to parse text and convert it into tokens

    Stop words and punctuations are removed from text

    :param text: the text to tokenize

    :retrun List[str]: list of tokens
    """

    # get rid of punctuations
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.lower()

    tokens = [token for token in text.split() if token not in STOPWORDS]
    return tokens
