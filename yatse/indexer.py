import os

from .db_handler import DbHandler
from .text_tokenizer import parser
from .ngram import create_ngrams
from .utils import save_raw_data

def index(document_id: str, text: str, db_handler: DbHandler, save: bool = True, data_path: str = ""):

    tokens = parser(text)
    terms = create_ngrams(tokens)
    for term, positions in terms.items():
        db_handler.add_term(term, document_id, positions)

    if db_handler.add_document(document_id):
        db_handler.increment_total_doc_count()
    
    if save:
        save_raw_data(document_id, data_path, text)

def index_file(document_id: str, data_path: str, db_handler: DbHandler):

    with open(os.path.join(data_path, document_id), 'r') as f:
        text = f
    index(document_id, text, db_handler, save=False)
