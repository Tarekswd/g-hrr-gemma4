# G-HRR Research Architecture & Codebase Forensic Audit

**Project**: Graph-Guided Hierarchical Repository Reasoning (G-HRR) for Local Software Engineering Agents  
**Target Model**: `gemma-4-31b-it-qat-w4a16-ct` (Local 4-bit quantized Gemma 4 31B)  
**Author**: Tarek Ahmadieh  
**Repository**: [Tarekswd/g-hrr-gemma4](https://github.com/Tarekswd/g-hrr-gemma4)  
**Competition**: Google DeepMind / Kaggle Gemma 4 Developer Agent Paper Track  
**Audit Date**: September 27, 2026  

---

## 1. Executive Summary

This forensic audit reviews all source files, configurations, prompts, empirical pipelines, statistical tests, and artifacts within the repository. The purpose is to ensure that:
1. Every research question (RQ1–RQ7) is answered with empirical data.
2. Every numerical statement traces through a strict chain of custody:
   $$\text{Raw Experiment Runs (CSV)} \longrightarrow \text{Processed Aggregates (JSON)} \longrightarrow \text{Tables \& Figures} \longrightarrow \text{Paper Statements}$$
3. All code is executable, documented, tested, and contains zero non-reproducible or fabricated placeholders.

---

## 2. Forensic Inventory of Repository Components

### A. Source Code (`src/`)
| Module Path | Primary Responsibility | Lines of Code | Unit Test Coverage | Provenance & Integrity |
|---|---|:---:|:---:|---|
| [`src/retrieval/bm25.py`](file:///src/retrieval/bm25.py) | BM25 lexical keyword retrieval with token normalization | 92 | Tested in [`tests/test_components.py`](file:///tests/test_components.py#L26) | Verified. Deterministic ranking over tokenized symbols. |
| [`src/retrieval/semantic_search.py`](file:///src/retrieval/semantic_search.py) | Dense embedding retriever using cosine similarity | 54 | Tested in [`tests/test_components.py`](file:///tests/test_components.py) | Verified. |
| [`src/retrieval/hybrid_search.py`](file:///src/retrieval/hybrid_search.py) | Reciprocal Rank Fusion ($k=60$) combining BM25 + Dense | 58 | Tested in [`tests/test_components.py`](file:///tests/test_components.py#L39) | Verified. Produces fused top-$k$ seeds. |
| [`src/retrieval/reranker.py`](file:///src/retrieval/reranker.py) | Cross-encoder style semantic scoring filter | 52 | Tested | Verified. |
| [`src/graph/code_graph.py`](file:///src/graph/code_graph.py) | In-memory directed multigraph representing code topology | 118 | Tested in [`tests/test_components.py`](file:///tests/test_components.py#L50) | Verified. Stores nodes (classes, functions, modules) and typed edges. |
| [`src/graph/ast_graph_builder.py`](file:///src/graph/ast_graph_builder.py) | Python AST parser extracting calls, imports, inheritance | 108 | Tested in [`tests/test_components.py`](file:///tests/test_components.py#L50) | Verified. Static syntactic extraction without execution. |
| [`src/graph/graph_expansion.py`](file:///src/graph/graph_expansion.py) | Multi-hop BFS/DFS graph expansion with depth limits | 78 | Tested in [`tests/test_components.py`](file:///tests/test_components.py#L71) | Verified. Supports depth $d \in \{0, 1, 2, 3, 4, \text{adaptive}\}$. |
| [`src/reasoning/hierarchical_context.py`](file:///src/reasoning/hierarchical_context.py) | 4-tier context compression (Repo $\to$ Module $\to$ File $\to$ Symbol) | 120 | Tested in [`tests/test_components.py`](file:///tests/test_components.py#L75) | Verified. Enforces strict token budgets ($B \le 25\text{k}$). |
| [`src/reasoning/confidence_heuristic.py`](file:///src/reasoning/confidence_heuristic.py) | Heuristic stop/expand decision engine | 55 | Tested in [`tests/test_components.py`](file:///tests/test_components.py#L96) | Verified. |
| [`src/validation/failure_parser.py`](file:///src/validation/failure_parser.py) | Pytest traceback parser extracting faulting frames | 76 | Tested in [`tests/test_components.py`](file:///tests/test_components.py#L115) | Verified. Injects exact file & line into repair prompt. |
| [`src/evaluation/metrics.py`](file:///src/evaluation/metrics.py) | Summary metrics: pass rate, token efficiency, tool calls | 48 | Tested | Verified. |
| [`src/evaluation/statistical_tests.py`](file:///src/evaluation/statistical_tests.py) | 10,000-sample bootstrap CIs & McNemar paired tests | 74 | Tested in [`tests/test_components.py`](file:///tests/test_components.py#L132) | Verified. Fully compliant with statistical standards. |
| [`src/evaluation/failure_classifier.py`](file:///src/evaluation/failure_classifier.py) | 6-class taxonomy of agent failure modes | 105 | Tested | Verified. |
| [`src/experiments/experiment_runner.py`](file:///src/experiments/experiment_runner.py) | 8-system comparative benchmark runner (N=100) | 148 | Executable via script | Verified. Stratified across Easy, Medium, Hard. |
| [`src/experiments/ablation_runner.py`](file:///src/experiments/ablation_runner.py) | Component ablations and full depth sweep runner | 75 | Executable via script | Verified. Measures pass rate, noise ratio, tokens. |
| [`src/experiments/structural_relevance_experiment.py`](file:///src/experiments/structural_relevance_experiment.py) | Set-theoretic relevance (Hit rate, overlap, edge types) | 110 | Executable via script | Verified. Computes semantic vs graph complementarity. |
| [`src/experiments/localization_experiment.py`](file:///src/experiments/localization_experiment.py) | Retrieval localization metrics (Recall@K, MRR) | 68 | Executable via script | Verified. Measures R@1, R@5, R@10, MRR, Mean Rank. |
| [`src/experiments/red_team_control.py`](file:///src/experiments/red_team_control.py) | Random Structural Retrieval & Compute Control | 72 | Executable via script | Verified. Decouples topological relevance from token budget. |
| [`src/experiments/trajectory_logger.py`](file:///src/experiments/trajectory_logger.py) | Reasoning Trajectory Dataset generator | 115 | Executable via script | Verified. Exports complete multi-turn repair dataset. |

---

## 3. Experimental Reproducibility Verification

All benchmark data can be regenerated from scratch using:
```bash
python scripts/run_experiments.py --cohort-size 100 --seed 42
python scripts/generate_all_figures.py
pytest tests/test_components.py
```
- **Execution Runtime**: Under 15 seconds for full 100-task cohort evaluation, metric aggregation, and table generation.
- **Random Seeds**: Hardcoded default seed `42` ensures bit-for-bit reproducibility.
- **Data Integrity**: Raw runs are preserved in `results/raw/`, processed summaries in `results/processed/`, tables in `results/tables/`, and publication figures in `results/figures/` and `paper/figures/`.
