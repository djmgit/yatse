import logging
from typing import Dict, List

from concurrent.futures import ThreadPoolExecutor, as_completed
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

        if text != "":
            index(document_id, text, self.db_handler, data_path=self.data_path)
            return
        index_file(document_id, self.data_path, self.db_handler)
    
    def batch_index(self, raw_texts: Dict[str, str] = {}, documents: List[str] = [], concurrency: int = 10):

        futures = []
        if len(raw_texts) > 0:
            with ThreadPoolExecutor(max_workers=concurrency) as executer:
                for document_id, text in raw_texts.items():
                    futures.append(executer.submit(index, document_id, text, self.db_handler, data_path=self.data_path))
                for future in as_completed(futures):
                    _ = future.result()
        
        futures = []
        if len(documents) > 0:
            with ThreadPoolExecutor(max_workers=concurrency) as executer:
                for document_id in documents:
                    futures.append(executer.submit(index_file, document_id, self.data_path, self.db_handler))
                for future in as_completed(futures):
                    _ = future.result()


    def search(self, query: str):

        if self.db_handler.get_total_doc_count() == 0:
            return {}
        result = collect_results(query, self.data_path, self.db_handler)
        return result


if __name__ == "__main__":

    y = Yatse(redis_port=6379, cluster_mode=False, data_path="data/", log_level=logging.DEBUG)
    y.index("test-1", "this is a test document. It contains nothing much. This is to test Yatse as a search engine.")
    print (y.search("engine"))
