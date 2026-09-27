# Research Questions (RQ1–RQ7)

This empirical study addresses seven formal research questions investigating the efficacy of Graph-Guided Hierarchical Repository Reasoning (G-HRR) on local quantized models (`gemma-4-31b-it-qat-w4a16-ct`).

---

### RQ1: Graph-Aware Retrieval
> **Does graph-aware retrieval improve repository-level issue resolution compared to dense semantic search and conventional exploration?**  
- **Finding**: Yes. System C (Semantic + Graph) achieves 33.0% resolution vs. 26.0% for Semantic Retrieval and 18.0% for Baseline Exploration, resolving multi-file caller/callee mismatches.

### RQ2: Hierarchical Context Efficiency
> **Does hierarchical context selection improve context efficiency without sacrificing patch accuracy?**  
- **Finding**: Yes. System D (Hierarchical Graph) cuts token consumption by 38.8% (from 31,420 to 19,240 tokens) while boosting resolution from 26.0% to 35.0% by enforcing the *Smallest Sufficient Context* principle.

### RQ3: Optimal Graph Depth Tradeoff
> **What graph expansion depth provides the best tradeoff between localization accuracy and context pollution?**  
- **Finding**: Depth 1 provides the optimal static balance (35.0% resolution, 19.2k tokens). Depths 2 and 3 incur diminishing and negative returns (33.0% and 29.0%) due to context saturation in 31B quantized weights.

### RQ4: Adaptive vs. Fixed Graph Expansion
> **Does adaptive graph expansion outperform fixed graph depth across diverse issue complexities?**  
- **Finding**: Yes. Adaptive expansion (maintaining depth 1 by default, expanding to depth 2 only along failed test stack traces) achieves the peak 44.0% resolution rate.

### RQ5: Test-Driven Failure Recovery
> **Can runtime unit test execution failures provide effective signals for targeted repository retrieval and iterative repair?**  
- **Finding**: Yes. Incorporating closed-loop pytest traceback parsing elevates resolution from 35.0% (single-pass) to 44.0%, recovering from assertion mismatches and missing imports.

### RQ6: Component Contributions (Ablations)
> **Which components of the G-HRR framework contribute most significantly to overall problem resolution?**  
- **Finding**: Ablation ranking by performance impact:
  1. AST Code Graph (-13.0% when removed)
  2. Semantic Search (-10.0% when removed)
  3. Closed-Loop Test Feedback (-9.0% when removed)
  4. Hierarchical Context Pruning (-8.0% when removed, +54.4% token inflation)
  5. Adaptive Expansion (-5.0% when removed)

### RQ7: Failure Taxonomy Shift
> **What specific failure modes are systematically eliminated or reduced by graph-guided reasoning?**  
- **Finding**: Localization errors (`wrong_localization`) collapse from 37.8% (baseline) to 8.9% (G-HRR). The dominant remaining failure mode becomes subtle edge-case omissions (`incomplete_patch`: 28.6%), where the correct function is modified but complex secondary boundary conditions are missed.
