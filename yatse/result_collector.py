import os

from .bm25_score import get_bm25_relevance_score
from .db_handler import DbHandler
from .entities import Term, SearchedTerms
from .text_tokenizer import parser
from .ngram import create_ngrams

def extract_terms(text: str, db_handler: DbHandler):

    tokens = parser(text)
    terms = create_ngrams(tokens)

    terms_with_docs = SearchedTerms({})
    for term in terms:
        documents = db_handler.get_term(term)
        terms_with_docs.terms[term] = Term(matched_docs=documents.keys(),
                                           total_matches=len(documents.keys()),
                                           matched_docs_with_pos=documents)
    
    return terms_with_docs

def get_all_matched_docs(terms: SearchedTerms):

    docs = set([])
    for _, term_data in terms.terms.items():
        docs.add(term_data.matched_docs)

    return docs

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
    results["documents"] = {}
    for document in matched_docs:
        bm25_relevence_score = get_bm25_relevance_score(document, terms)
        results["documents"].append({
            "relevence_socre": bm25_relevence_score,
            "document_name": document,
            "document_full_path": os.path.join(data_path, document),
            "occurence_count": search_terms_freq_in_doc(terms, document)
        })
