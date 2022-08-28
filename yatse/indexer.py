import datetime
import logging
import os
import time

from .db_handler import DbHandler
from .text_tokenizer import parser
from .ngram import create_ngrams
from .utils import save_raw_data

logger = logging.getLogger(__name__)

def index(document_id: str, text: str, db_handler: DbHandler, save: bool = True, data_path: str = ""):

    logger.info(f"Indexing document : {document_id}")
    indexing_start_time = time.time()
    tokens = parser(text)
    terms = create_ngrams(tokens)
    for term, positions in terms.items():
        db_handler.add_term(term, document_id, positions)
    indexing_end_time = time.time()
    time_to_index = indexing_end_time - indexing_start_time
    time_to_index_human = datetime.timedelta(seconds=time_to_index)
    logger.info(f"Document : {document_id} indexed in {time_to_index}s which is {time_to_index_human}. Terms indexed : {len(terms)}")

    if db_handler.add_document(document_id):
        db_handler.increment_total_doc_count()
    logger.debug("Increased total indexed documents count")
    
    if save:
        save_raw_data(document_id, data_path, text)
        logger.info(f"Saved {document_id} at {os.path.join(data_path, document_id)}")

def index_file(document_id: str, data_path: str, db_handler: DbHandler):

    logger.info(f"Reading document : {document_id}")
    with open(os.path.join(data_path, document_id), 'r') as f:
        text = f
    index(document_id, text, db_handler, save=False)
