"""
Dense embedding search simulation and interface compatible with offline/air-gapped Gemma embeddings.
"""
import math
from typing import List, Dict, Tuple, Any

class DenseCodeRetriever:
    def __init__(self, dimension: int = 128):
        self.dimension = dimension
        self.documents: List[Dict[str, Any]] = []
        self.embeddings: List[List[float]] = []

    def _pseudo_embed(self, text: str) -> List[float]:
        """Deterministic hash-based dense embedding fallback for local benchmarking."""
        vec = [0.0] * self.dimension
        for i, word in enumerate(text.lower().split()):
            idx = hash(word) % self.dimension
            vec[idx] += 1.0 / (1.0 + math.log(i + 2))
        # L2 normalize
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]

    def index(self, documents: List[Dict[str, Any]]) -> None:
        self.documents = documents
        self.embeddings = [self._pseudo_embed(doc.get("text", "")) for doc in documents]

    def retrieve(self, query: str, top_k: int = 10) -> List[Tuple[Dict[str, Any], float]]:
        q_vec = self._pseudo_embed(query)
        scores = []
        for i, doc_vec in enumerate(self.embeddings):
            sim = sum(a * b for a, b in zip(q_vec, doc_vec))
            scores.append((self.documents[i], sim))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
