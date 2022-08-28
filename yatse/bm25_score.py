import logging
import math

from .entities import k1, SearchedTerms

logger = logging.getLogger(__name__)

def get_bm25_relevance_score(document: str, terms: SearchedTerms, total_documents: int):
    """
    Function to caluculate bm25 score of a document with respect to given terms

    Based on this: http://sphinxsearch.com/blog/2010/08/17/how-sphinx-relevance-ranking-works/
    However I have changed the idf formula because it was throwing div by zero exception for not
    found term, that is term thats not present in any document this is because total_matching document
    for such terms is 0. Although the bm25 component for the term will be calculated as 0 since tf will
    be 0 for such terms but still if we think of idf separately it will give error which doesnt feel right.
    Hence I have based it on the formula as given in wikipedia: https://en.wikipedia.org/wiki/Okapi_BM25.
    I have added 0.5 both to numerator and denominator so that denominator never becomes 0.
    """
    
    bm25_score = 0.0
    logger.info(f"Calculating bm25 relevance core for document : {document}")
    for term, term_data in terms.terms.items():
        tf = len(term_data.matched_docs_with_pos.get(document, []))
        total_matching_documents = term_data.total_matches
        idf = math.log((total_documents - total_matching_documents + 0.5) / (total_matching_documents + 0.5)) / math.log(1.0 + total_documents)

        bm25 = tf * idf / (tf + k1)
        bm25_score += bm25

        logger.debug(f"bm25 components for term : {term} : tf : {tf}, total matching documents : {total_matching_documents}, idf: {idf}, bm25 : {bm25}")
    
    bm25_score = 0.5 + bm25_score  / (2 * len(terms.terms))
    logger.debug(f"Final bm25 score for document : {document} is {bm25_score}")

    return bm25_score
