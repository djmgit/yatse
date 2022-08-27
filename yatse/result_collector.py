import logging
import os

from .bm25_score import get_bm25_relevance_score
from .db_handler import DbHandler
from .entities import Term, SearchedTerms
from .text_tokenizer import parser
from .ngram import create_ngrams

logger = logging.getLogger(__name__)

def extract_terms(text: str, db_handler: DbHandler):
    logger.info("extracting terms from query")
    tokens = parser(text)
    terms = create_ngrams(tokens)

    terms_with_docs = SearchedTerms({})
    for term in terms:
        documents = db_handler.get_term(term)
        terms_with_docs.terms[term] = Term(matched_docs=documents.keys(),
                                           total_matches=len(documents.keys()),
                                           matched_docs_with_pos=documents)
    
    logger.debug(f"Total extracted terms from query : {len(terms_with_docs.terms)}")

    return terms_with_docs

def get_all_matched_docs(terms: SearchedTerms):

    docs = set([])
    for _, term_data in terms.terms.items():
        docs.update(term_data.matched_docs)

    logger.info(f"Total matched documents found : {len(docs)}")

    return list(docs)

def search_terms_freq_in_doc(terms: SearchedTerms, document: str):

    tf = {}
    for term, term_data in terms.terms.items():
        freq = len(term_data.matched_docs_with_pos.get(document, []))
        tf[term] = freq
    return tf


def collect_results(text: str, data_path: str, db_handler: DbHandler):
    """
    Function to aggregate search result, rank them

    Example result:
    {
        "total_matched_docs": 10,
        "documents": [{
            "relevence_score": 0.005,
            "document_name": doc-1,
            "document_full_path": /tmp/doc-1,
            "occurence_count": 5
        }]
    }
    """

    terms = extract_terms(text, db_handler)
    matched_docs = get_all_matched_docs(terms)

    results = {}
    results["documents"] = []
    for document in matched_docs:
        bm25_relevance_score = get_bm25_relevance_score(document, terms, db_handler.get_total_doc_count())
        results["documents"].append({
            "relevance_score": bm25_relevance_score,
            "document_name": document,
            "document_full_path": os.path.join(data_path, document)
        })
    
    results["documents"].sort(key=lambda x: x["relevance_score"], reverse=True)
    results["total_matched_documents"] = len(matched_docs)
    return results
