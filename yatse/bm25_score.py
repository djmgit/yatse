import math

from .entities import k1, SearchedTerms

def get_bm25_relevance_score(document: str, terms: SearchedTerms, total_documents: int):
    
    bm25_score = 0.0
    print (f"document : {document}")
    for _, term_data in terms.terms.items():
        tf = len(term_data.matched_docs_with_pos.get(document, []))
        total_matching_documents = term_data.total_matches
        idf = math.log((total_documents - total_matching_documents + 1.0) / total_matching_documents) / math.log(1.0 + total_documents)

        bm25 = tf * idf / (tf + k1)
        bm25_score += bm25

        #print (f"term : {term}")
        #print (f"tf : {tf}")
        #print (f"total_matching documents : {total_matching_documents}")
        #print (f"total_documents : {total_documents}")
        #print (f"num_terms : {len(terms.terms)}")
        #print (f"idf : {idf}")
        #print (f"bm25 : {bm25}")
        #print ("----------- \n")
    
    bm25_score = 0.5 + bm25_score  / (2 * len(terms.terms))

    return bm25_score


