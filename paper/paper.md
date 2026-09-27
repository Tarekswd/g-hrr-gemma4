# Beyond Similarity: Structural Context Retrieval and Minimum Sufficient Context for Local Software Engineering Agents

**Author**: Tarek Ahmadieh  
**Track**: Google DeepMind / Kaggle Gemma 4 Developer Agent Paper Track  
**Target Model**: `gemma-4-31b-it-qat-w4a16-ct`  
**Artifact Repository**: [https://github.com/Tarekswd/g-hrr-gemma4](https://github.com/Tarekswd/g-hrr-gemma4)  
**Submission Writeup**: [Kaggle Paper Track Writeup](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/writeups/g-hrr-graph-guided-hierarchical-reasoning-for-loc)  

---

## Abstract

Autonomous software engineering (SWE) agents powered by local, quantized foundation models—specifically `gemma-4-31b-it-qat-w4a16-ct`—face an acute dilemma: repository context is too vast to ingest wholesale, yet isolated code snippets fail to expose multi-hop causal dependencies. Prevailing methods rely on dense semantic retrieval, which treats code as unstructured natural language and misses structural control-flow relationships. In this work, we investigate what graph-guided repository reasoning actually teaches us about context retrieval, organization, and efficiency. 

We introduce **Graph-Guided Hierarchical Repository Reasoning (G-HRR)**, an agentic framework coupling hybrid lexical-dense retrieval, AST dependency graph expansion, and multi-tier hierarchical pruning to achieve the *Minimum Sufficient Context* (MSC). Evaluated across a 100-task benchmark cohort drawn from SWE-bench, G-HRR advances issue resolution from 18.0% (direct exploration) and 26.0% (hybrid semantic search) to **44.0%** ($p < 0.0001$, McNemar test), while consuming 28.0% fewer tokens than unpruned search.

Crucially, our experiments reveal three fundamental empirical discoveries:
1. **Structural Complementarity**: Semantic retrieval and AST graphs exhibit orthogonal failure modes. Semantic search anchors focal definitions (68.0% hit rate) but misses 26.0% of non-lexical causal dependencies, which AST graph retrieval captures to reach a **94.0% union hit rate**.
2. **Topological Relevance vs. Token Volume**: In a controlled red-team experiment, supplying an identical token budget (~22.8k tokens) of randomly sampled repository nodes yields only **23.0% resolution** ($p = 0.0008$), proving that topological syntactic structure, rather than token volume, drives the performance gain.
3. **Context Dilution Non-Monotonicity**: Static graph depth exhibits a sharp inverted-U curve ($d=1$: 35%, $d=2$: 33%, $d=3$: 29%, $d=4$: 24%) driven by exponential noise accumulation (17.5% to 90.2%), proving that deeper graph ingestion actively degrades local quantized attention.

---

## 1. Introduction

Resolving real-world software defects across repository-scale codebases requires localizing subtle faults, tracing multi-hop function calls, and preserving interface contracts across distributed modules. While proprietary cloud models evaluated on SWE-bench rely on hundreds of thousands of context tokens to ingest large files wholesale, privacy-sensitive and on-device developer workflows demand quantized open-weights models such as Google's Gemma 4 31B (`gemma-4-31b-it-qat-w4a16-ct`).

When deployed on local hardware, autonomous coding agents fall prey to two symmetric traps:
1. **The Context Starvation Trap**: Restricting prompt exposure to isolated focal functions deprives the model of upstream caller contracts and downstream type invariants, causing frequent interface contract violations.
2. **The Context Pollution Trap**: Ingesting extensive source files or unpruned directory subgraphs saturates the model's effective attention, introducing distractor tokens that induce hallucination and syntax degradation in 4-bit quantized weights.

This tension raises a fundamental research question:
> *What does graph-guided repository reasoning actually teach us about how local software-engineering agents should retrieve, organize, and use repository context?*

Rather than merely describing an engineering artifact, this paper conducts a controlled empirical study to discover the mechanisms underlying structural code reasoning. We hypothesize that repository bugs reside on **topological dependency subgraphs**. By combining semantic retrieval with bounded AST expansion and multi-tier hierarchical pruning, an agent can isolate the *Minimum Sufficient Context* required for provable repair without triggering context dilution.

### Primary Scientific Contributions
- **Structural vs. Semantic Complementarity**: We measure set-theoretic context overlap across 100 benchmark instances, proving that semantic search and AST graphs address orthogonal needs: semantic search anchors the focal implementation (68% hit rate), while AST graphs capture causal dependencies (80% hit rate), yielding a 94.0% union hit rate.
- **Red-Team Control for Topological Relevance**: We implement a Random Structural Retrieval control matching G-HRR's token budget (~22.8k tokens) using randomized repository nodes. It achieves only 23.0% resolution ($p = 0.0008$), proving that topological syntactic structure, rather than token volume, drives the gain.
- **Discovery of Graph-Depth Non-Monotonicity**: We demonstrate that static graph expansion beyond 1 hop degrades issue resolution ($d=1$: 35%, $d=4$: 24%) as irrelevant context noise increases from 17.5% to 90.2%. Adaptive, failure-driven depth-2 expansion resolves this trade-off (44.0% pass rate).
- **Formalization of Minimum Sufficient Context**: We introduce a 4-tier hierarchical pruning schema that reduces token consumption by 38.8% relative to naive concatenation while lifting issue resolution from 26.0% to 44.0%.

---

## 2. Related Work

### 2.1 Autonomous Coding Agents
SWE-bench (Jimenez et al., 2024) established the benchmark standard for evaluating LLMs on GitHub issues. SWE-agent (Yang et al., 2024) introduced specialized Agent-Computer Interfaces (ACIs), demonstrating that precision file viewer and editor tools reduce tool syntax errors. Agentless (Xia et al., 2024) showed that hierarchical localization (file then function) achieves competitive results without expensive multi-agent loops. However, existing open agents assume cloud-scale models; their performance degrades steeply on quantized local weights.

### 2.2 Code Retrieval and Representation
Retrieval-Augmented Generation (RAG) for software engineering has progressed from BM25 to dense embeddings (Lewis et al., 2020). RepoCoder (Zhang et al., 2023) demonstrated iterative similarity retrieval for code completion. GraphCodeBERT (Guo et al., 2021) demonstrated that incorporating data-flow edges during pre-training improves code representation. Graph RAG frameworks (Edge et al., 2024) construct knowledge graphs from text. In this paper, we extend code graphs from pre-training representations into explicit, dynamic runtime navigation substrates for autonomous repair.

---

## 3. Methodology

### 3.1 Code Graph Formulation
We represent repository structure as a directed multigraph $G = (V, E)$, where vertices $V = V_{\text{func}} \cup V_{\text{class}} \cup V_{\text{mod}}$ represent code entities. The directed edge set $E = E_{\text{calls}} \cup E_{\text{imports}} \cup E_{\text{inherits}} \cup E_{\text{contains}}$ captures syntactic dependencies, where $(u, v) \in E_{\text{calls}}$ denotes that entity $u$ calls entity $v$.

### 3.2 Hybrid Seed Retrieval via Reciprocal Rank Fusion
Given an issue report $I$, candidate seed symbols $\mathcal{S}_0 \subset V$ are identified using hybrid Reciprocal Rank Fusion (RRF) combining BM25 lexical ranking and dense cosine embedding similarity:
$$\text{RRF}(d) = \frac{\alpha}{k_{rrf} + \text{Rank}_{\text{BM25}}(d)} + \frac{1 - \alpha}{k_{rrf} + \text{Rank}_{\text{Dense}}(d)}$$
where $\alpha = 0.5$ and $k_{rrf} = 60$. The top-$k$ ranked symbols form initial candidate set $\mathcal{S}_0 = \{s_1, \dots, s_k\}$.

### 3.3 Bounded Graph Expansion
From seeds $\mathcal{S}_0$, we compute $d$-hop neighborhood $\mathcal{N}_d(\mathcal{S}_0)$ via bounded breadth-first search:
$$\mathcal{N}_0 = \mathcal{S}_0, \quad \mathcal{N}_{d+1} = \mathcal{N}_d \cup \{v \in V \mid \exists u \in \mathcal{N}_d, (u, v) \in E \lor (v, u) \in E_{\text{calls}}\}$$
Expansion is bidirectional: incoming caller edges reveal who depends on the candidate symbol, while outgoing callee edges reveal downstream dependencies.

### 3.4 Minimum Sufficient Context Optimization
Rather than providing full file contents for all nodes in $\mathcal{N}_d$, we formalize context selection as finding the Minimum Sufficient Context:
$$\mathcal{C}^* = \arg\min_{\mathcal{C} \subseteq \mathcal{N}_d} |\mathcal{C}| \quad \text{s.t.} \quad P(\text{Pass} \mid \mathcal{C}, I) \ge 1 - \epsilon$$
We construct $\mathcal{C}^*$ hierarchically across four structural tiers:
- **Tier 1 (Architecture)**: High-level directory schema ($\sim 500$ tokens).
- **Tier 2 (Module Skeleton)**: Class signatures and docstrings of focal files ($\sim 1,200$ tokens).
- **Tier 3 (Dependency Subgraph)**: Signatures and docstrings of 1-hop callers and callees ($\sim 3,500$ tokens).
- **Tier 4 (Focal Implementation)**: Full implementation body of the primary target function ($\sim 2,000$ tokens).

### 3.5 Adaptive Closed-Loop Repair
When a patch fails test execution in the sandbox, the failure analyzer extracts execution traceback $\mathcal{T} = \{(f_1, l_1, e_1), \dots, (f_m, l_m, e_m)\}$. If faulting symbol $v_{\text{fault}} \notin \mathcal{N}_1$, the agent adaptively triggers a Depth-2 expansion restricted to the failing stack trace edge:
$$\mathcal{N}_{\text{adapt}} = \mathcal{N}_1 \cup \text{BFS}(v_{\text{fault}}, d=1)$$
This targeted expansion avoids global depth-2 noise while providing the exact caller context needed to rectify interface contract violations.

---

## 4. Experimental Setup

### 4.1 Benchmark Cohort
We evaluate on a standardized 100-task cohort drawn from SWE-bench Lite and Verified across 7 major Python repositories: `django` (28), `sympy` (24), `scikit-learn` (18), `matplotlib` (14), `pytest` (8), `astropy` (5), and `requests` (3). Tasks are stratified by complexity: 30 Easy (single-file, depth 1), 45 Medium (multi-function, depth 2), and 25 Hard (multi-module, depth 3).

### 4.2 Evaluated Baseline Systems
We benchmark 7 controlled systems and 1 red-team control:
- **B0 (Direct Exploration)**: Standard agent bash/directory tool exploration without retrieval preprocessing.
- **B1 (Lexical BM25)**: BM25 keyword retrieval over repository code chunks.
- **B2 (Dense Retrieval)**: Cosine similarity over dense code embeddings.
- **B3 (Hybrid Search)**: Reciprocal Rank Fusion of BM25 and dense retrieval ($k=10$).
- **B4 (Fixed Graph)**: Hybrid search seeds expanded via static 1-hop AST edges without hierarchical filtering.
- **B5 (Hierarchical Only)**: 4-tier hierarchical pruning applied to hybrid search seeds without graph expansion.
- **B6 (Full G-HRR)**: Complete system coupling hybrid search, AST graph expansion, 4-tier hierarchical context, and adaptive traceback repair.
- **Control (Random Structural)**: Context budget matched token-for-token with G-HRR (~22.8k tokens), but graph neighbor nodes are randomly sampled from the repository.

### 4.3 Model Configuration
All evaluations use the official competition model `gemma-4-31b-it-qat-w4a16-ct` served via vLLM with 4-bit weights and 16-bit activations ($T=0.2$, top-$p=0.95$). Resource limits enforce 25 tool calls and 15 minutes per task.

---

## 5. Results and Empirical Discoveries

### 5.1 Primary Resolution Performance
Table 1 presents comparative benchmark results. Full G-HRR (B6) achieves a **44.0% resolution rate** (95% bootstrap CI: [34.0%, 54.0%]), outperforming baseline B0 (18.0%) by +26.0% and hybrid search B3 (26.0%) by +18.0%. McNemar's paired test confirms statistical significance over baseline ($\chi^2 = 18.24, p < 0.0001$).

| System Configuration | Pass Rate (%) | 95% Bootstrap CI | Easy | Med | Hard | kTokens | $p$-value (vs B6) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **B0: Direct Exploration** | 18.0% | [10.9, 26.0] | 35.0% | 15.0% | 4.0% | 24.8 | $p < 0.0001$ |
| **B1: Lexical (BM25)** | 21.0% | [13.0, 29.0] | 40.0% | 18.0% | 4.0% | 26.5 | $p = 0.0003$ |
| **B2: Dense Retrieval** | 24.0% | [16.0, 33.0] | 43.0% | 22.0% | 4.0% | 28.5 | $p = 0.0018$ |
| **B3: Hybrid Search** | 26.0% | [18.0, 35.0] | 47.0% | 24.0% | 4.0% | 31.4 | $p = 0.0042$ |
| **B4: Fixed Graph (1-Hop)** | 33.0% | [24.0, 42.0] | 53.0% | 33.0% | 8.0% | 29.2 | $p = 0.0410$ |
| **B5: Hierarchical Only** | 35.0% | [26.0, 45.0] | 57.0% | 33.0% | 12.0% | 19.2 | $p = 0.0820$ |
| **B6: G-HRR (Full)** | **44.0%** | **[34.0, 54.0]** | **70.0%** | **42.0%** | **16.0%** | **22.6** | **--** |
| Control: Random Structural | 23.0% | [15.0, 32.0] | 40.0% | 20.0% | 4.0% | 22.8 | $p = 0.0008$ |

### 5.2 Retrieval Localization as a Causal Bridge
Table 2 reports retrieval metrics. G-HRR achieves **89.0% Recall@5** and **0.697 MRR**, compared to 54.0% Recall@5 and 0.382 MRR for BM25. This establishes a causal bridge: superior topological localization yields high-fidelity structural context, which directly elevates issue resolution.

| System | R@1 | R@5 | R@10 | MRR | File Acc | Sym Acc |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Lexical (BM25) | 28.0% | 54.0% | 66.0% | 0.382 | 62.0% | 44.0% |
| Dense Retrieval | 34.0% | 61.0% | 71.0% | 0.448 | 69.0% | 51.0% |
| Hybrid (BM25+Dense) | 41.0% | 72.0% | 81.0% | 0.531 | 78.0% | 63.0% |
| Graph Only | 22.0% | 48.0% | 63.0% | 0.334 | 59.0% | 41.0% |
| Hybrid + Fixed Graph | 46.0% | 79.0% | 87.0% | 0.589 | 84.0% | 72.0% |
| **G-HRR (Adaptive)** | **58.0%** | **89.0%** | **95.0%** | **0.697** | **93.0%** | **84.0%** |

### 5.3 Structural vs. Semantic Complementarity
Table 3 reports set-theoretic hit rates across the benchmark cohort. While semantic search alone achieves 68.0% hit rate and graph retrieval achieves 80.0%, their union reaches **94.0%**. Crucially, **26.0% of necessary causal context was retrieved exclusively by the AST graph** and missed entirely by semantic top-5. This explains why pure semantic agents fail on complex issues: upstream callers and interface implementations frequently share zero textual similarity with the issue report.

| Context Retrieval Category | Observed Frequency (%) |
|---|:---:|
| Semantic Hit Rate (Top-5) | 68.0% |
| Graph Hit Rate (1-Hop AST) | 80.0% |
| **Union Hit Rate (Semantic $\cup$ Graph)** | **94.0%** |
| Overlap: Semantic $\cap$ Graph | 54.0% |
| Semantic-Only (Focal Symbol Anchors) | 14.0% |
| Graph-Only (Indirect Callers / Dependencies) | 26.0% |
| Neither (Unresolved Dynamic Dispatch) | 6.0% |

---

## 6. Analysis and Controlled Ablations

### 6.1 Red-Team Control: Random Structural Retrieval
To test whether G-HRR simply benefits from more context tokens, our Random Structural Retrieval control matched G-HRR's token budget (~22.8k tokens) and node count using randomly sampled repository nodes. Random Structural Retrieval achieved only **23.0% pass rate**—worse than Semantic Search (26.0%) and 21.0% below G-HRR ($p = 0.0008$, McNemar test). This confirms that *topological syntactic relevance*, rather than raw token volume, drives performance.

### 6.2 Graph Depth Non-Monotonicity and Context Pollution
Expanding static graph depth $d \in \{0, 1, 2, 3, 4, \text{adaptive}\}$ reveals an inverted-U curve: $d=0$ (27.0%), $d=1$ (35.0%), $d=2$ (33.0%), $d=3$ (29.0%), and $d=4$ (24.0%). This degradation is driven by **exponential context pollution**: irrelevant distractor nodes surge from 17.5% at $d=1$ to 90.2% at $d=4$. In contrast, G-HRR's **Adaptive Depth** achieves the peak **44.0% pass rate** while maintaining a low 13.2% noise ratio.

| Graph Depth | Pass Rate (%) | Recall@5 (%) | Mean Nodes | Noise Ratio (%) | Pass / kTokens |
|---|:---:|:---:|:---:|:---:|:---:|
| $d = 0$ (Target Only) | 27.0% | 68.0% | 1.0 | 6.0% | 2.18 |
| $d = 1$ (1-Hop AST) | 35.0% | 88.0% | 5.4 | 17.5% | 1.82 |
| $d = 2$ (2-Hop AST) | 33.0% | 89.0% | 18.2 | 52.0% | 1.05 |
| $d = 3$ (3-Hop AST) | 29.0% | 84.0% | 52.8 | 77.6% | 0.60 |
| $d = 4$ (4-Hop AST) | 24.0% | 78.0% | 128.0 | 90.2% | 0.37 |
| **Adaptive (G-HRR)** | **44.0%** | **92.0%** | **6.8** | **13.2%** | **1.95** |

### 6.3 Component Ablation Matrix
Decomposing G-HRR demonstrates that removing the **Code Graph** causes the largest drop (-18.0%), confirming that graph topology provides structural grounding unavailable through vector similarity. Removing **Hierarchical Pruning** causes an 11.0% drop while inflating tokens to 29.2k, demonstrating the severity of the Context Pollution Trap. Removing **Test Feedback Repair** reduces resolution by 9.0%, confirming the value of execution-grounded hypothesis revision.

| Configuration | Pass Rate (%) | Mean Tokens | Tool Calls | $\Delta$ Pass Rate |
|---|:---:|:---:|:---:|:---:|
| **Full G-HRR** | **44.0%** | **22,610** | **12.8** | **--** |
| w/o Code Graph | 26.0% | 31,400 | 16.8 | -18.0% |
| w/o Semantic Retrieval | 28.0% | 24,200 | 14.5 | -16.0% |
| w/o Hierarchical Pruning | 33.0% | 29,200 | 13.5 | -11.0% |
| w/o Test Feedback Repair | 35.0% | 19,200 | 11.2 | -9.0% |
| w/o Adaptive Expansion | 35.0% | 19,240 | 11.8 | -9.0% |

---

## 7. Failure Analysis and Trajectories

### 7.1 Failure Taxonomy Distribution
Comparing failure modes between Baseline (82 failures) and G-HRR (56 failures) shows that in the Baseline, failures are dominated by `wrong_localization` (37.8%) and `missing_context` (24.4%). In G-HRR, wrong localization collapses to 8.9% and missing context drops to 7.1%. The primary remaining failure mode in G-HRR becomes `incomplete_patch` (28.6%), where the model correctly localizes the bug and fixes the primary control flow, but overlooks secondary edge cases.

### 7.2 Trajectory Analysis
Analysis of the 100-task Trajectory Dataset reveals that in 65.0% of resolved tasks, G-HRR succeeds on the initial patch. In the remaining 35.0% of resolved tasks, the initial patch fails unit test assertions, but the agent recovers on Step 2 by incorporating the pytest traceback and triggering targeted caller expansion. Primary recovery triggers were caller stack trace identification (46.7%) and missing dependency signatures (33.3%).

---

## 8. Limitations

1. **Dynamic Metaprogramming**: Static AST parsing cannot resolve dynamic reflection (e.g. `getattr`, dynamic dispatch, runtime monkeypatching).
2. **Single Model Architecture**: Experiments focused on `gemma-4-31b-it-qat-w4a16-ct`; behavior may vary on smaller models (e.g. 9B) or unquantized checkpoints.
3. **Language Scope**: Current graph builder targets Python syntax; polyglot codebases require Tree-sitter AST extensions.

---

## 9. Conclusion

This work examined how local software engineering agents should retrieve, structure, and use repository context under strict resource limits. Through controlled experimentation on Gemma 4 31B W4A16, we demonstrated that semantic similarity alone is insufficient, missing 26% of causal repository dependencies. Conversely, exhaustive graph retrieval induces severe context pollution. By coupling hybrid search, AST dependency graphs, and 4-tier hierarchical pruning, G-HRR identifies the **Minimum Sufficient Context**, elevating issue resolution from 18.0% to **44.0%** ($p < 0.0001$) while consuming 28.0% fewer tokens.

---

## References

- Edge, D., et al. (2024). From Local to Global: A Graph RAG Approach to Query-Focused Summarization. *arXiv:2404.16130*.
- Gemma Team. (2024). Gemma: Open Models Based on Gemini Research and Technology. *arXiv:2403.08295*.
- Guo, D., et al. (2021). GraphCodeBERT: Pre-training Code Representations with Data Flow. In *ICLR*.
- Jimenez, C. E., et al. (2024). SWE-bench: Can Language Models Resolve Real-World GitHub Issues? In *ICLR*.
- Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. In *NeurIPS*.
- Xia, C. S., Guan, Y., & Zhang, L. (2024). Agentless: Demystifying LLM-based Software Engineering Agents. *arXiv:2407.01489*.
- Xia, C. S., & Zhang, L. (2023). Keep the Conversation Going: Fixing Bugs with Conversational APR. In *ICSE*.
- Yang, J., et al. (2024). SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. *arXiv:2405.15793*.
- Zhang, F., et al. (2023). RepoCoder: Repository-Level Code Completion Through Iterative Retrieval. *ACM TOSEM*.
