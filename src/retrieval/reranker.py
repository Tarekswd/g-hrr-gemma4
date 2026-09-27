"""
Symbol and snippet reranking logic optimizing for repository relevance and issue keyword density.
"""
from typing import List, Dict, Tuple, Any

class ContextReranker:
    def __init__(self):
        pass

    def rerank(self, query: str, candidates: List[Tuple[Dict[str, Any], float]], top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """
        Rerank candidates based on keyword presence, path depth, and lexical exact match.
        """
        query_words = set(query.lower().split())
        reranked = []

        for doc, score in candidates:
            text = doc.get("text", "").lower()
            name = doc.get("name", "").lower()
            path = doc.get("file_path", "").lower()

            exact_match_bonus = 0.0
            for word in query_words:
                if len(word) > 3 and word in name:
                    exact_match_bonus += 0.5
                if len(word) > 3 and word in path:
                    exact_match_bonus += 0.2

            # Penalize excessively deep paths unless matching query
            depth = path.count("/") + path.count("\\")
            depth_penalty = 0.01 * min(depth, 10)

            adjusted_score = score + exact_match_bonus - depth_penalty
            reranked.append((doc, adjusted_score))

        reranked.sort(key=lambda x: x[1], reverse=True)
        return reranked[:top_k]
