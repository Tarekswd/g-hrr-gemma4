# Core Research Questions & Hypotheses

## Primary Research Question
> **Can structured code-graph reasoning improve a local, quantized language model's (`gemma-4-31b-it-qat-w4a16-ct`) ability to solve repository-level software-engineering issues compared with semantic retrieval and conventional repository exploration, while operating under constrained token and tool-call budgets?**

## Formal Hypotheses
*   **H1 (Localization Accuracy)**: Dependency-aware code graph retrieval identifies true fault locations with higher precision than dense vector retrieval alone.
*   **H2 (Patch Resolution Rate)**: Augmenting candidate symbols with 1-hop graph neighbors yields higher test pass rates than unaugmented or full-file context.
*   **H3 (Context Efficiency)**: Hierarchical context pruning (filtering non-essential AST nodes) reduces prompt token consumption without sacrificing patch success.
*   **H4 (Tool Budget Conservation)**: Graph-guided navigation minimizes redundant repository traversals and file reads, reducing tool calls.
*   **H5 (Test-Driven Recovery)**: Closed-loop failure trace parsing combined with targeted 1-hop dependency expansion improves recovery from failed initial patches.
*   **H6 (Non-Monotonicity of Graph Depth)**: Graph expansion exhibits diminishing or negative returns beyond Depth 1; Depth 2 is beneficial only adaptively.
*   **H7 (Local Model Compensatory Effect)**: Explicit structural representations partially bridge the reasoning gap between 31B quantized local models and frontier cloud models.
