from typing import Dict, List

def create_ngrams(tokens: List[str], min_size: int = 3, max_size: int = 6) -> Dict[str, List[int]]:

    terms = {}
    for position, token in enumerate(tokens):
        for ngram_window in range(min_size, max(max_size, len(token)) + 1):
            ngram = token[:ngram_window]
            if ngram not in terms:
                terms[ngram] = {}
            terms[ngram].append(position)
    
    return terms
