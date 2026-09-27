"""
Graph data structures representing code repositories, symbols, and topological dependencies.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Any

@dataclass
class CodeNode:
    id: str  # e.g., "django.db.models.fields:CharField.validate"
    name: str
    kind: str  # "function", "class", "method", "module"
    file_path: str
    start_line: int
    end_line: int
    docstring: Optional[str] = None
    code_content: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CodeEdge:
    source_id: str
    target_id: str
    edge_type: str  # "calls", "imported_by", "inherits", "contains", "tests"
    weight: float = 1.0

class CodeGraph:
    def __init__(self):
        self.nodes: Dict[str, CodeNode] = {}
        self.adj_out: Dict[str, List[CodeEdge]] = {}
        self.adj_in: Dict[str, List[CodeEdge]] = {}

    def add_node(self, node: CodeNode) -> None:
        self.nodes[node.id] = node
        if node.id not in self.adj_out:
            self.adj_out[node.id] = []
        if node.id not in self.adj_in:
            self.adj_in[node.id] = []

    def add_edge(self, source_id: str, target_id: str, edge_type: str, weight: float = 1.0) -> None:
        edge = CodeEdge(source_id=source_id, target_id=target_id, edge_type=edge_type, weight=weight)
        if source_id not in self.adj_out:
            self.adj_out[source_id] = []
        if target_id not in self.adj_in:
            self.adj_in[target_id] = []
        self.adj_out[source_id].append(edge)
        self.adj_in[target_id].append(edge)

    def get_neighbors(self, node_id: str, direction: str = "both") -> List[CodeNode]:
        """
        direction: 'out' (callees/imports), 'in' (callers/importers), 'both'
        """
        neighbor_ids: Set[str] = set()
        if direction in ("out", "both") and node_id in self.adj_out:
            for edge in self.adj_out[node_id]:
                neighbor_ids.add(edge.target_id)
        if direction in ("in", "both") and node_id in self.adj_in:
            for edge in self.adj_in[node_id]:
                neighbor_ids.add(edge.source_id)

        return [self.nodes[nid] for nid in neighbor_ids if nid in self.nodes]

    def get_subgraph(self, root_ids: List[str], max_depth: int = 1) -> "CodeGraph":
        subgraph = CodeGraph()
        visited: Set[str] = set()
        current_level = set(root_ids)

        for depth in range(max_depth + 1):
            next_level = set()
            for nid in current_level:
                if nid in self.nodes and nid not in visited:
                    visited.add(nid)
                    subgraph.add_node(self.nodes[nid])

                    # Add outgoing edges
                    for edge in self.adj_out.get(nid, []):
                        if depth < max_depth:
                            next_level.add(edge.target_id)
                        if edge.target_id in visited or depth < max_depth:
                            subgraph.add_edge(edge.source_id, edge.target_id, edge.edge_type, edge.weight)

                    # Add incoming edges
                    for edge in self.adj_in.get(nid, []):
                        if depth < max_depth:
                            next_level.add(edge.source_id)
                        if edge.source_id in visited or depth < max_depth:
                            subgraph.add_edge(edge.source_id, edge.target_id, edge.edge_type, edge.weight)

            current_level = next_level

        return subgraph
