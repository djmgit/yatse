import json
from typing import List
from redis import Redis, RedisCluster

class DbHandler:

    def __init__(self, cluster_mode: bool = False, host: str = '127.0.0.1', port: int = 6379) :
        self.redis_conn = Redis(host=host, port=port, decode_responses=True, db=0) if not cluster_mode else \
                            RedisCluster(host=host,
                                         port=port,
                                         read_from_replicas=True,
                                         ssl=False, decode_responses=True)
        self.term_prefix = "term_"
        self.total_docs_key = "total_doc"
        self.documents_key = "documents"
        
    def add_term(self, term: str, document_id: str, positions: List[int]):

        term_key = f'{self.term_prefix}{term}'
        self.redis_conn.hset(term_key, document_id, json.dumps(positions))
    
    def get_term(self, term: str):

        term_key = f'{self.term_prefix}{term}'
        term_data = self.redis_conn.hgetall(term_key)
        for document_id in term_data.keys():
            term_data[document_id] = json.loads(term_data[document_id])
        return term_data
    
    def get_all_terms(self):

        return self.redis_conn.scan("term_*")

    def increment_total_doc_count(self, delta: int = -1):

        if delta > 1:
            self.redis_conn.incr(self.total_docs_key, delta)
            return
        self.redis_conn.incr(self.total_docs_key)

    def get_total_doc_count(self):

        doc_count = self.redis_conn.get(self.total_docs_key)
        if not doc_count:
            return 0
        return float(doc_count)

    def add_document(self, document):
        if not self.redis_conn.sismember(self.documents_key, document):
            self.redis_conn.sadd(self.documents_key, document)
            return True
        
        return False
