from typing import Dict, List

def create_ngrams(tokens: List[str], min_size: int = 3, max_size: int = 6) -> Dict[str, List[int]]:
    """
    Function to create edge ngrams with positions.

    :param tokens: list of tokens
    :param min_size: min size of an ngrams
    :param max_size: max_size of an ngram
    
    :return Dict[str, List[int]]: list of ngrams containing their positions
    """

    terms = {}
    for position, token in enumerate(tokens):
        for ngram_window in range(min_size, max(max_size, len(token)) + 1):
            ngram = token[:ngram_window]
            if ngram not in terms:
                terms[ngram] = []
            terms[ngram].append(position)
    
    return terms
