"""
Graph expansion logic supporting depth 0, 1, 2, 3, and adaptive expansion.
"""
from typing import List, Set, Dict, Any
from .code_graph import CodeGraph, CodeNode

class GraphExpander:
    def __init__(self, code_graph: CodeGraph):
        self.code_graph = code_graph

    def expand(self, seed_node_ids: List[str], depth: int = 1) -> List[CodeNode]:
        """
        Bounded BFS expansion from seed nodes up to max depth.
        """
        if depth == 0:
            return [self.code_graph.nodes[nid] for nid in seed_node_ids if nid in self.code_graph.nodes]

        visited: Set[str] = set()
        current_layer: Set[str] = set(seed_node_ids)
        result_nodes: List[CodeNode] = []

        for d in range(depth + 1):
            next_layer: Set[str] = set()
            for nid in current_layer:
                if nid not in visited and nid in self.code_graph.nodes:
                    visited.add(nid)
                    result_nodes.append(self.code_graph.nodes[nid])

                    if d < depth:
                        neighbors = self.code_graph.get_neighbors(nid, direction="both")
                        for neighbor in neighbors:
                            if neighbor.id not in visited:
                                next_layer.add(neighbor.id)
            current_layer = next_layer

        return result_nodes

    def adaptive_expand(self, seed_node_ids: List[str], test_failed: bool = False, missing_symbols: List[str] = None) -> List[CodeNode]:
        """
        Adaptive strategy: Default to depth 1; if test fails or missing symbols exist, selectively expand depth 2 along failure path.
        """
        base_nodes = self.expand(seed_node_ids, depth=1)
        if not test_failed and not missing_symbols:
            return base_nodes

        # Expand along failing or missing symbol nodes
        additional_seeds = []
        if missing_symbols:
            for s in missing_symbols:
                for nid in self.code_graph.nodes:
                    if s.lower() in nid.lower():
                        additional_seeds.append(nid)

        extra_nodes = self.expand(additional_seeds or seed_node_ids, depth=2)
        node_dict = {n.id: n for n in base_nodes + extra_nodes}
        return list(node_dict.values())
