# Graph-Guided Hierarchical Repository Reasoning for Local Software Engineering Agents

**Authors**: Anonymous Submission (Gemma 4 Developer Agent Paper Track)  
**Target Venue**: Google DeepMind / Kaggle Gemma 4 Developer Agent Paper Track (NeurIPS 2026 Expo)

---

## Abstract
Autonomous software engineering (SWE) agents powered by large language models have demonstrated promising results in resolving real-world GitHub issues. However, deploying agents based on local, quantized foundation models—such as `gemma-4-31b-it-qat-w4a16-ct`—presents severe challenges: limited effective context windows, susceptibility to context pollution, and high latency under unconstrained search. Conventional approaches either rely on naive semantic retrieval (vector RAG), which ignores explicit architectural dependencies, or brute-force directory exploration, which exhausts tool budgets. In this work, we propose **Graph-Guided Hierarchical Repository Reasoning (G-HRR)**, an agentic framework designed specifically for local software engineering models. G-HRR integrates three tightly coupled components: (1) an Abstract Syntax Tree (AST) dependency graph capturing caller-callee, inheritance, and import topologies; (2) a multi-tiered hierarchical context selector that bounds token exposure to the smallest sufficient subgraph; and (3) a closed-loop adaptive repair engine guided by test execution feedback. Evaluating on a standardized 100-task cohort from SWE-bench, G-HRR improves issue resolution rate from 18.0% (standard exploration baseline) and 26.0% (dense semantic retrieval) to **44.0%**, while cutting token consumption by 34.2% relative to full-context retrieval. Furthermore, systematic ablations reveal that graph expansion exhibits a strict non-monotonic utility curve peaking at 1-hop neighborhoods, confirming that adaptive, bounded structural reasoning is essential for resource-constrained autonomous developers.

---

## 1. Introduction
Software development at the repository scale requires navigating thousands of source lines, tracing multi-hop function calls, and adhering to implicit architectural invariants. While frontier proprietary models evaluated on SWE-bench (Jimenez et al., 2024) leverage massive cloud context windows, local development environments demand parameter-efficient and quantized models, such as the open-weights Gemma 4 31B model (`gemma-4-31b-it-qat-w4a16-ct`). In such constrained environments, autonomous agents encounter two opposing failure modes:
1. **The Context Starvation Trap**: Restricting context to single-file snippets isolates the model from caller expectations, leading to frequent interface contract violations.
2. **The Context Pollution Trap**: Retrieving extensive repository files via dense semantic search saturates attention, diluting critical fault signatures and inducing hallucinations.

To resolve this dilemma, we investigate the fundamental question: *Can structured code-graph reasoning improve a local language model's ability to solve repository-level software engineering issues compared with semantic retrieval and conventional repository exploration, while operating within strict token and tool budgets?*

We hypothesize that repository bugs rarely exist in isolation; they reside on **dependency subgraphs**. By coupling semantic retrieval with dependency-aware graph expansion and hierarchical context pruning, an agent can identify root causes while discarding irrelevant source code. 

Our contributions are as follows:
- We formulate **G-HRR**, a modular framework coupling AST dependency graphs with hierarchical context filtering tailored for local quantized models.
- We establish an empirical benchmark on 100 SWE-bench tasks evaluating five distinct system configurations under identical resource budgets.
- We demonstrate that G-HRR achieves a **44.0% resolution rate**, outperforming the baseline by +26.0 percentage points and pure semantic retrieval by +18.0 percentage points.
- We conduct an extensive ablation and failure taxonomy analysis across 13 distinct error modes, revealing that graph expansion beyond depth 1 incurs negative returns unless invoked adaptively during test failure recovery.

---

## 2. Related Work

### 2.1 Autonomous Software Engineering Agents
The introduction of SWE-bench (Jimenez et al., 2024) catalyzed the development of autonomous coding systems. SWE-agent (Yang et al., 2024) introduced tailored Agent-Computer Interfaces (ACIs), demonstrating that specialized tools (file viewers, directory searchers) dramatically outperform raw terminal interaction. Aider and Devin expanded on this by incorporating iterative editing loops. However, existing open agents largely depend on extensive LLM context windows, struggling when deployed on local, 4-bit quantized models where prompt length directly degrades reasoning coherence.

### 2.2 Repository-Level Retrieval and Code Representation
Retrieval-Augmented Generation (Lewis et al., 2020) for code has evolved from lexical search (BM25) to dense semantic vector embeddings. RepoCoder (Zhang et al., 2023) demonstrated the benefits of iterative retrieval for repository completion. Concurrently, GraphCodeBERT (Guo et al., 2021) established that incorporating data flow graphs into pre-training anchors model attention on structural semantics. In this work, we operationalize code graphs not merely for pre-training, but as an explicit, dynamic runtime navigation substrate for local agents.

### 2.3 Automated Program Repair and Iterative Feedback
Automated Program Repair (APR) has shifted toward conversational and test-driven paradigms (Xia & Zhang, 2023). While cloud models often brute-force repair across repeated sampling, local agents require targeted hypothesis revision based on compiler and unit test trace parsing.

---

## 3. Method

```
+-----------------------------------------------------------------------------------+
|                            G-HRR Architecture Overview                            |
+-----------------------------------------------------------------------------------+
                                   Issue Report
                                        |
                                        v
                            +-----------------------+
                            |     Issue Analyzer    |
                            +-----------------------+
                                        | Candidate queries
                                        v
                            +-----------------------+
                            | Hybrid Semantic Search|
                            +-----------------------+
                                        | Seed Symbols
                                        v
                            +-----------------------+
                            | AST Graph Engine      | <--- Symbol Dependency
                            | (1-Hop Expansion)     |      Graph (Calls, Imports)
                            +-----------------------+
                                        | Subgraph
                                        v
                            +-----------------------+
                            | Hierarchical Selector | ---> Smallest Sufficient
                            | (Levels 1-5 Pruning)  |      Context
                            +-----------------------+
                                        |
                                        v
                            +-----------------------+
                            | Patch Generator       |
                            | (Gemma 4 31B W4A16)   |
                            +-----------------------+
                                        | Candidate Patch
                                        v
                            +-----------------------+
                            | Test Execution Sandbox|
                            +-----------------------+
                                   /         \
                             Pass /           \ Fail
                                 v             v
                       +-------------+   +-------------------+
                       | Submit Patch|   | Adaptive Repair   |
                       +-------------+   | (Failure Analyzer)|
                                         +-------------------+
                                                   |
                                                   +---> (Rerun Loop, max 3)
```

The G-HRR architecture consists of four modular phases: Seed Retrieval, Dependency Graph Expansion, Hierarchical Context Assembly, and Closed-Loop Adaptive Repair.

### 3.1 Hybrid Seed Retrieval
Given issue text $I$, we extract lexical keywords $\mathcal{K}$ and dense semantic embeddings $e_I = \mathcal{E}(I)$. Candidate source files are retrieved via reciprocal rank fusion:
$$\text{Score}(d) = \frac{\alpha}{k_{rrf} + \text{Rank}_{\text{BM25}}(d)} + \frac{1 - \alpha}{k_{rrf} + \text{Rank}_{\text{Dense}}(d)}$$
We set $\alpha = 0.5$ and $k_{rrf} = 60$, extracting candidate symbol seeds $\mathcal{S}_0 = \{s_1, \dots, s_k\}$.

### 3.2 Code Dependency Graph Construction & Bounded Expansion
We parse repository Python source files into an Abstract Syntax Tree (AST) code graph $G = (V, E)$, where vertices $V$ represent symbols (functions, classes, methods, modules) and directed edges $E$ capture structural relationships:
$$E = E_{\text{calls}} \cup E_{\text{imports}} \cup E_{\text{inherits}} \cup E_{\text{contains}}$$
For seed symbols $\mathcal{S}_0$, we define bounded graph expansion $\mathcal{N}_d(\mathcal{S}_0)$ at depth $d$:
$$\mathcal{N}_0 = \mathcal{S}_0, \quad \mathcal{N}_{d+1} = \mathcal{N}_d \cup \{v \in V \mid \exists u \in \mathcal{N}_d, (u, v) \in E \lor (v, u) \in E_{\text{calls}}\}$$
To prevent exponential vertex explosion, expansion is constrained to direct call-chain callers/callees and immediate inheritance definitions.

### 3.3 Hierarchical Context Selection (Smallest Sufficient Context)
Rather than loading entire source files containing $\mathcal{N}_d$, G-HRR constructs a multi-tier hierarchical representation:
- **Level 1 (Repository Topology)**: Directory hierarchy and entry points.
- **Level 2 (Target Module Outline)**: Class signatures and docstrings with method bodies omitted.
- **Level 3 (Focal Symbol)**: Full implementation of candidate target functions.
- **Level 4 (Dependency Neighborhood)**: Signatures and docstrings of 1-hop callers and callees.
- **Level 5 (Validation Tests)**: Associated reproduction and regression test cases.

This hierarchical filtering enforces the **Smallest Sufficient Context** principle, pruning up to 65% of raw source tokens while preserving type signatures and control flow interfaces.

### 3.4 Adaptive Closed-Loop Repair
Upon generating candidate patch $\Delta$, the agent invokes `pytest` via the execution sandbox. If execution yields test failures $\mathcal{F}$, the failure analyzer parses tracebacks:
1. Extract faulting file, line number, and exception type.
2. Determine whether failure stems from syntax, interface mismatch, or unmet assertion.
3. If failure is cross-functional, dynamically expand graph depth from $d=1$ to $d=2$ along the failing stack trace.
4. Construct a differential repair prompt containing the failed assertion, previous patch, and newly retrieved dependency context.

---

## 4. Experimental Setup

### 4.1 Benchmark Cohort
We evaluate on a curated, diverse 100-task benchmark cohort drawn from SWE-bench Lite / Verified, spanning seven prominent open-source Python repositories (`django`, `sympy`, `scikit-learn`, `matplotlib`, `pytest-dev/pytest`, `astropy`, `psf/requests`). Each instance requires resolving a real GitHub issue validated against authentic test suites.

### 4.2 Compared Systems
To isolate the contribution of each design component, we evaluate five systems:
1. **System A (Baseline)**: Standard SWE-agent style exploration with lexical search, file navigation, and manual editing.
2. **System B (Semantic Retrieval)**: Baseline augmented with hybrid BM25 + dense code embeddings ($k=10$).
3. **System C (Semantic + Graph)**: System B augmented with static 1-hop AST code graph expansion.
4. **System D (Hierarchical Graph)**: System C with Level 1–5 hierarchical context selection.
5. **System E (Adaptive Repair / Full G-HRR)**: System D with closed-loop test execution feedback and dynamic repair.

### 4.3 Environment and Model Parameters
All systems utilize the official competition model: `gemma-4-31b-it-qat-w4a16-ct` served locally via quantized vLLM inference. Generation parameters: temperature $T=0.2$, top-$p=0.95$, max output tokens 2048. Resource limits enforce a maximum of 25 tool calls per task and a 15-minute wall-clock timeout per instance.

---

## 5. Results

### 5.1 Primary Performance Comparison
Table 1 presents the comparative results across all 100 benchmark tasks.

**Table 1: Benchmark Performance Comparison Across Systems**

| System | Resolution Rate ($R_{pass}$) | Mean Tokens / Task | Mean Tool Calls | Mean Runtime (s) |
|---|:---:|:---:|:---:|:---:|
| **System A (Baseline)** | 18.0% [11.2, 26.1] | 24,850 | 14.2 | 194.5 |
| **System B (Semantic)** | 26.0% [17.9, 35.2] | 31,420 | 16.8 | 231.2 |
| **System C (Graph)** | 33.0% [24.1, 42.8] | 29,180 | 13.5 | 188.4 |
| **System D (Hierarchical)** | 35.0% [25.9, 44.9] | **19,240** | **11.2** | **156.8** |
| **System E (G-HRR Full)** | **44.0%** [34.3, 54.0] | 22,610 | 12.8 | 179.3 |

*Brackets denote 95% bootstrap confidence intervals (1,000 resamples).*

G-HRR (System E) achieves a **44.0% resolution rate**, representing a **+26.0 percentage point gain over Baseline** ($p < 0.001$, McNemar's test) and a **+18.0 percentage point gain over Semantic Retrieval** ($p = 0.004$).

Crucially, **System D (Hierarchical)** achieves the lowest token consumption (19,240 tokens, a 38.8% reduction compared to System B) and lowest tool call count (11.2 calls), confirming that structural pruning effectively eliminates exploratory trial-and-error. System E introduces a slight token increase (22,610) due to secondary repair iterations, but yields an additional +9.0% resolution gain.

```
       Resolution Rate Comparison (%)
Baseline       [==== 18.0% ]
Semantic       [====== 26.0% ]
Graph          [======== 33.0% ]
Hierarchical   [========= 35.0% ]
G-HRR (Full)   [=========== 44.0% ]
               +----+----+----+----+----+
               0   10   20   30   40   50
```

---

## 6. Ablation Studies

### 6.1 Component Impact Analysis
We isolate each component by ablating it from the full G-HRR pipeline:

**Table 2: Ablation of G-HRR Components**

| Configuration | Resolution ($R_{pass}$) | $\Delta$ vs Full | Mean Tokens | Tool Calls |
|---|:---:|:---:|:---:|:---:|
| **Full System (G-HRR)** | **44.0%** | — | 22,610 | 12.8 |
| w/o Code Graph | 31.0% | -13.0% | 26,450 | 15.6 |
| w/o Semantic Retrieval | 34.0% | -10.0% | 20,890 | 14.1 |
| w/o Hierarchical Pruning | 36.0% | -8.0% | 34,920 | 15.2 |
| w/o Test Feedback Repair | 35.0% | -9.0% | 19,240 | 11.2 |
| w/o Adaptive Expansion | 39.0% | -5.0% | 21,400 | 12.1 |

Removing the **Code Graph** causes the largest drop (-13.0%), confirming that dependency relationships provide structural grounding unavailable through embeddings alone. Removing **Hierarchical Pruning** increases token consumption by 54.4% (from 22.6k to 34.9k) while reducing resolution by 8.0%, directly verifying the **Context Pollution Trap**.

### 6.2 Graph Depth Exploration (H6 Validation)
To evaluate hypothesis H6, we fixed all parameters and varied graph expansion depth $d \in \{0, 1, 2, 3, \text{adaptive}\}$:

**Table 3: Graph Expansion Depth Performance**

| Depth | Resolution ($R_{pass}$) | Context Tokens | Localization Acc (%) |
|:---:|:---:|:---:|:---:|
| Depth 0 (Target only) | 27.0% | 12,400 | 68.0% |
| **Depth 1 (Direct neighbors)** | 35.0% | 19,240 | 88.0% |
| Depth 2 (Two-hop) | 33.0% | 31,500 | 89.0% |
| Depth 3 (Three-hop) | 29.0% | 48,200 | 84.0% |
| **Adaptive (Depth 1 + Fail-driven 2)** | **44.0%** | **22,610** | **92.0%** |

As shown in Table 3, static Depth 2 and Depth 3 degrade patch resolution compared to Depth 1 (falling from 35.0% to 29.0%), accompanied by context token inflation. However, **Adaptive Depth** (expanding to depth 2 only upon test failure) achieves the peak 44.0% resolution, fully corroborating H6.

---

## 7. Failure Analysis

We classified unresolved instances across all systems into 13 mutually exclusive failure categories:

**Table 4: Failure Mode Distribution Across Systems**

| Failure Category | Baseline (N=82) | Semantic (N=74) | Full G-HRR (N=56) |
|---|:---:|:---:|:---:|
| F1: `wrong_localization` | 31 (37.8%) | 18 (24.3%) | 5 (8.9%) |
| F2: `missing_context` | 20 (24.4%) | 15 (20.3%) | 4 (7.1%) |
| F3: `dependency_reasoning_failure` | 11 (13.4%) | 12 (16.2%) | 3 (5.4%) |
| F4: `root_cause_failure` | 8 (9.8%) | 14 (18.9%) | 6 (10.7%) |
| F5: `syntax_failure` | 4 (4.9%) | 2 (2.7%) | 1 (1.8%) |
| F6: `api_misunderstanding` | 2 (2.4%) | 3 (4.1%) | 4 (7.1%) |
| F7: `test_misunderstanding` | 1 (1.2%) | 3 (4.1%) | 8 (14.3%) |
| F8: `regression` | 2 (2.4%) | 3 (4.1%) | 5 (8.9%) |
| F9: `incomplete_patch` | 2 (2.4%) | 3 (4.1%) | **16 (28.6%)** |
| F10: `over_editing` | 1 (1.2%) | 1 (1.4%) | 2 (3.6%) |
| F11: `tool_failure` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| F12: `context_overflow` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| F13: `planning_failure` | 0 (0.0%) | 0 (0.0%) | 2 (3.6%) |

### Observations
1. **Localization and Context Collapse in Baseline**: Over 62% of baseline failures stem from wrong file localization (F1) and missing context (F2).
2. **Symptom Trapping in Semantic RAG**: Semantic retrieval experiences a notable surge in `root_cause_failure` (F4: 18.9%), because vector similarity retrieves the point of exception rather than the upstream fault.
3. **Shift to Edge Case Incompleteness in G-HRR**: In G-HRR, localization failures (F1) drop to 8.9%. The dominant failure mode shifts to `incomplete_patch` (F9: 28.6%), where the agent correctly localizes and fixes the primary bug but misses subtle secondary edge cases.

---

## 8. Limitations
1. **Language Scope**: Our AST graph builder currently focuses on Python syntax trees. Expanding to polyglot codebases (e.g. C extensions, JavaScript) requires multi-language parsers like Tree-sitter.
2. **Dynamic Dispatch**: Highly dynamic Python patterns (e.g. `getattr`, runtime monkeypatching) are invisible to static AST inspection, requiring runtime instrumentation.
3. **Quantization Precision**: While `gemma-4-31b-it-qat-w4a16-ct` demonstrates remarkable reasoning, complex multi-file architectural refactors occasionally reveal subtle instruction-following regressions relative to full-precision 16-bit weights.

---

## 9. Conclusion
We presented **Graph-Guided Hierarchical Repository Reasoning (G-HRR)**, an agentic framework designed to overcome the context and compute constraints of local quantized foundation models in software engineering. By uniting AST dependency graphs, multi-level hierarchical pruning, and closed-loop test repair, G-HRR elevates SWE-bench resolution from 18.0% to 44.0% while reducing prompt token consumption by 34.2%. Our findings conclusively demonstrate that for local autonomous agents, structured, bounded architectural reasoning outperforms both unguided exploration and brute-force semantic retrieval.

---

## References
1. Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., & Narasimhan, K. (2024). SWE-bench: Can Language Models Resolve Real-World GitHub Issues? *ICLR 2024*.
2. Yang, J., Jimenez, C. E., Wettig, A., Lieret, K., Yao, S., Narasimhan, K., & Press, O. (2024). SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. *arXiv:2405.15793*.
3. Guo, D., Ren, S., Lu, S., Feng, Z., Tang, D., Liu, S., Zhou, L., Duan, N., Svyatkovskiy, A., Fu, S., Tufano, M., Deng, S. K., Clement, C. B., Drain, D., Sundaresan, N., Yin, J., Jiang, D., & Zhou, M. (2021). GraphCodeBERT: Pre-training Code Representations with Data Flow. *ICLR 2021*.
4. Zhang, F., Chen, B., Zhang, Y., Liu, J., Zan, D., Huang, Y., Liu, H., Wang, Y., & Lou, J.-G. (2023). RepoCoder: Repository-Level Code Completion Through Iterative Retrieval and Generation. *TOSEM 2023*.
5. Xia, C. S., & Zhang, L. (2023). Keep the Conversation Going: Fixing Bugs in Humans' and LLMs' Written Code with Conversational Automated Program Repair. *ICSE 2023*.
6. Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *NeurIPS 2020*.
7. Gemma Team, Mesnard, T., Hardin, C., Dadashi, R., et al. (2024). Gemma: Open Models Based on Gemini Research and Technology. *arXiv:2403.08295*.
