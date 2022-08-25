from venv import create

from .db_handler import DbHandler
from .entities import Term
from .text_tokenizer import parser
from .ngram import create_ngrams

def extract_terms(text: str, db_handler: DbHandler):

    tokens = parser(text)
    terms = create_ngrams(tokens)

    terms_with_docs = []
    for term in terms:
        documents = db_handler.get_term(term)
        terms_with_docs.append(Term(matched_docs=documents.keys(),
                                    total_matches=len(documents.keys()),
                                    matched_docs_with_pos=documents))
    
    return terms_with_docs
