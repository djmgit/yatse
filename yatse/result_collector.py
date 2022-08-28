import datetime
import logging
import os
import time

from .bm25_score import get_bm25_relevance_score
from .db_handler import DbHandler
from .entities import Term, SearchedTerms
from .text_tokenizer import parser
from .ngram import create_ngrams

logger = logging.getLogger(__name__)

def extract_terms(text: str, db_handler: DbHandler):
    """
    Function to extract all terms from a query.

    It works in pretty similar was as that of processing a text
    while indexing.

    Returns a structured collection of terms and corresponding data
    For example

    SearchedTerms(
        terms = {
            "term-1": Term(
                matched_docs=["doc-1", "doc-2"]
                total_matches=2
                matched_docs_with_positions={
                    "doc-1": [1,2],
                    "doc-2": [5,7]
                }
            )
        }
    )

    :param text: qeury
    :param DBHandler: dbhandler for handling db interactions

    :return SearchedTerms: terms with data.
    """
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
    """
    Function to get all the matched documents from query

    :param terms: collection of terms along with data

    :return List[str]: List of matched documents
    """

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

    search_start_time = time.time()
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
    search_end_time = time.time()
    time_to_search = search_end_time - search_start_time
    time_to_search_human = datetime.timedelta(seconds=time_to_search)
    results["total_matched_documents"] = len(matched_docs)
    results["time_taken_seconds"] = time_to_search
    results["time_taken_human_readable"] = str(time_to_search_human)
    return results
