import math

from .entities import k1, SearchedTerms

def get_bm25_relevance_score(document: str, terms: SearchedTerms, total_documents: int):
    
    bm25_score = 0.0
    for term, term_data in terms.terms.items():
        tf = len(term_data.matched_docs_with_pos.get(document, []))
        total_matching_documents = term_data.total_matches
        idf = math.log((total_documents - total_matching_documents + 1) / total_matching_documents) / math.log(1 + total_documents)

        bm25 = tf * idf / (tf + k1)
        bm25_score += bm25
    
    bm25_score = 0.5 + bm25_score  / (2 * len(terms.terms))

    return bm25_score


