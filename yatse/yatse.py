import logging
from typing import Dict, List

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED
from .indexer import index, index_file
from .db_handler import DbHandler
from .result_collector import collect_results

logger  = logging.getLogger(__name__)

class Yatse:

    def __init__(self, redis_host: str = '127.0.0.1', redis_port=6379, cluster_mode: bool = False, data_path: str = "", log_level=logging.ERROR):
        self.db_handler: DbHandler = DbHandler(cluster_mode=cluster_mode, host=redis_host, port=redis_port)
        self.data_path = data_path
        if log_level:
            logging.basicConfig(level=log_level)
    
    def index(self, document_id: str, text: str = ""):
        """
        Function used to index text.

        :param document_id: name/id of document, should be unique
        :param text: document content
        """

        if text != "":
            index(document_id, text, self.db_handler, data_path=self.data_path)
            return
        index_file(document_id, self.data_path, self.db_handler)

    def search(self, query: str, limit=10):
        """
        Function to search a query

        :param query: query string
        
        :return Dict[str, Union[str,List[Dict[str, str]]]]: collection of results
        """

        if self.db_handler.get_total_doc_count() == 0:
            return {}
        result = collect_results(query, self.data_path, self.db_handler, limit=limit)
        return result
