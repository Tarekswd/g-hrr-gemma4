"""
Multi-tiered hierarchical context constructor enforcing the Smallest Sufficient Context principle.
"""
from typing import List, Dict, Any, Optional
from ..graph.code_graph import CodeNode

class HierarchicalContextBuilder:
    def __init__(self, token_budget: int = 16000):
        self.token_budget = token_budget

    def _estimate_tokens(self, text: str) -> int:
        return max(1, len(text) // 4)

    def build_context(
        self,
        repo_summary: str,
        focal_nodes: List[CodeNode],
        neighbor_nodes: List[CodeNode],
        test_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Assemble Level 1 through Level 5 context while honoring token_budget.
        """
        sections: List[str] = []
        total_tokens = 0

        # Level 1: Repository Overview
        l1 = f"### LEVEL 1: REPOSITORY ARCHITECTURE\n{repo_summary.strip()}\n"
        sections.append(l1)
        total_tokens += self._estimate_tokens(l1)

        # Level 2 & 3: Focal Candidate Nodes (Full Implementation)
        sections.append("### LEVEL 2 & 3: FOCAL CANDIDATE SYMBOLS (TARGET CODE)")
        for node in focal_nodes:
            node_text = (
                f"// File: {node.file_path} (Lines {node.start_line}-{node.end_line})\n"
                f"// Symbol: {node.name} [{node.kind}]\n"
                f"{node.code_content}\n"
            )
            sections.append(node_text)
            total_tokens += self._estimate_tokens(node_text)

        # Level 4: Dependency Neighborhood (Signatures & Docstrings only to save tokens)
        sections.append("### LEVEL 4: DEPENDENCY NEIGHBORHOOD (CALLERS & CALLEES)")
        for node in neighbor_nodes:
            if node.id in [fn.id for fn in focal_nodes]:
                continue
            doc = f"\n  \"\"\"{node.docstring}\"\"\"" if node.docstring else ""
            summary_text = (
                f"// Neighbor: {node.name} [{node.kind}] in {node.file_path}\n"
                f"def {node.name}(...):{doc}\n  # Implementation pruned\n"
            )
            if total_tokens + self._estimate_tokens(summary_text) < self.token_budget:
                sections.append(summary_text)
                total_tokens += self._estimate_tokens(summary_text)

        # Level 5: Test Verification Context
        if test_context:
            t_section = f"### LEVEL 5: VALIDATION TEST CASE\n{test_context.strip()}\n"
            if total_tokens + self._estimate_tokens(t_section) < self.token_budget:
                sections.append(t_section)
                total_tokens += self._estimate_tokens(t_section)

        full_prompt_context = "\n".join(sections)
        return {
            "prompt_text": full_prompt_context,
            "estimated_tokens": total_tokens,
            "focal_count": len(focal_nodes),
            "neighbor_count": len(neighbor_nodes)
        }
