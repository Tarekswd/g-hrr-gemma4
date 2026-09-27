"""
Hybrid search combining BM25 lexical search and dense semantic search via Reciprocal Rank Fusion (RRF).
"""
from typing import List, Dict, Tuple, Any
from .bm25 import BM25Retriever
from .semantic_search import DenseCodeRetriever

class HybridCodeSearcher:
    def __init__(self, rrf_k: int = 60, alpha: float = 0.5):
        self.rrf_k = rrf_k
        self.alpha = alpha
        self.bm25 = BM25Retriever()
        self.dense = DenseCodeRetriever()

    def index(self, documents: List[Dict[str, Any]]) -> None:
        self.bm25.index(documents)
        self.dense.index(documents)

    def retrieve(self, query: str, top_k: int = 10) -> List[Tuple[Dict[str, Any], float]]:
        bm25_results = self.bm25.retrieve(query, top_k=top_k * 2)
        dense_results = self.dense.retrieve(query, top_k=top_k * 2)

        rrf_scores: Dict[str, float] = {}
        doc_map: Dict[str, Dict[str, Any]] = {}

        for rank, (doc, _) in enumerate(bm25_results):
            doc_id = doc["id"]
            doc_map[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + self.alpha / (self.rrf_k + rank + 1)

        for rank, (doc, _) in enumerate(dense_results):
            doc_id = doc["id"]
            doc_map[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 - self.alpha) / (self.rrf_k + rank + 1)

        sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return [(doc_map[doc_id], score) for doc_id, score in sorted_docs[:top_k]]
