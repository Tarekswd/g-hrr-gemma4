"""
Lexical BM25 retrieval for source code documents and symbol signatures.
"""
import math
import re
from typing import List, Dict, Tuple, Any

class BM25Retriever:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus: List[Dict[str, Any]] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_len: float = 0.0
        self.doc_freqs: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}

    def _tokenize(self, text: str) -> List[str]:
        # Split on non-alphanumeric and camelCase / snake_case
        tokens = re.findall(r'[A-Za-z0-9]+', text.lower())
        return tokens

    def index(self, documents: List[Dict[str, Any]]) -> None:
        """
        Index documents. Each document must have 'id' and 'text'.
        """
        self.corpus = documents
        self.doc_lengths = []
        self.doc_freqs = {}
        total_tokens = 0

        for doc in documents:
            tokens = self._tokenize(doc.get("text", ""))
            self.doc_lengths.append(len(tokens))
            total_tokens += len(tokens)
            unique_tokens = set(tokens)
            for t in unique_tokens:
                self.doc_freqs[t] = self.doc_freqs.get(t, 0) + 1

        n_docs = len(documents)
        self.avg_doc_len = total_tokens / max(n_docs, 1)

        self.idf = {}
        for term, freq in self.doc_freqs.items():
            # Standard Lucene/BM25 IDF
            self.idf[term] = math.log(1.0 + (n_docs - freq + 0.5) / (freq + 0.5))

    def retrieve(self, query: str, top_k: int = 10) -> List[Tuple[Dict[str, Any], float]]:
        query_tokens = self._tokenize(query)
        scores: List[float] = [0.0] * len(self.corpus)

        for i, doc in enumerate(self.corpus):
            tokens = self._tokenize(doc.get("text", ""))
            doc_len = self.doc_lengths[i]
            token_counts: Dict[str, int] = {}
            for t in tokens:
                token_counts[t] = token_counts.get(t, 0) + 1

            doc_score = 0.0
            for qt in query_tokens:
                if qt not in self.idf:
                    continue
                tf = token_counts.get(qt, 0)
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / max(self.avg_doc_len, 1e-6)))
                doc_score += self.idf[qt] * (numerator / max(denominator, 1e-6))

            scores[i] = doc_score

        indexed_scores = [(self.corpus[i], scores[i]) for i in range(len(self.corpus))]
        indexed_scores.sort(key=lambda x: x[1], reverse=True)
        return indexed_scores[:top_k]
