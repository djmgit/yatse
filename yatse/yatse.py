from .indexer import index, index_file
from .db_handler import DbHandler

class Yatse:

    def __init__(self, redis_host: str = '127.0.0.1', redis_port=6379, cluster_mode: bool = False, data_path: str = ""):
        self.db_handler: DbHandler = DbHandler(cluster_mode=cluster_mode, host=redis_host, port=redis_port)
        self.data_path = data_path
    
    def index(self, document_id: str, text: str = ""):

        if text != "":
            index(document_id, text, self.db_handler)
            return
        index_file(document_id, self.data_path, self.db_handler)


if __name__ == "__main__":

    y = Yatse(redis_port=7001, cluster_mode=True, data_path="./")
    y.index("test-1", "this is a test document. It contains nothing much. This is to test Yatse as a search engine.")
