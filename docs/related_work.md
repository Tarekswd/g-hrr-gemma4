# Comprehensive Related Work & Literature Review

In accordance with Section 6 of the Research Specification, every foundational paper is analyzed across ten formal dimensions.

---

### 1. SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
*   **Authors**: Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, Karthik Narasimhan
*   **Year**: 2024
*   **Venue**: International Conference on Learning Representations (ICLR 2024)
*   **URL / DOI**: [https://arxiv.org/abs/2310.06770](https://arxiv.org/abs/2310.06770)
*   **Research Problem**: Prior code benchmarks evaluated isolated single-function synthesis (e.g. HumanEval), which failed to test real-world software engineering across multi-file repositories.
*   **Method**: Constructed a benchmark of 2,294 task instances from real pull requests across 12 prominent open-source Python repositories, evaluated on `FAIL_TO_PASS` and `PASS_TO_PASS` test suites.
*   **Important Finding**: State-of-the-art LLMs (GPT-4) initially solved under 4% of real-world issues, demonstrating that repository navigation and localization are the true bottlenecks.
*   **Limitation**: Evaluates end-to-end patch diffs but does not standardize the tool interfaces or retrieval mechanisms used by agents.
*   **Relevance to G-HRR**: SWE-bench serves as our primary evaluation benchmark and defining ground-truth testbed.

---

### 2. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
*   **Authors**: John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, Ofir Press
*   **Year**: 2024
*   **Venue**: arXiv preprint (arXiv:2405.15793)
*   **URL / DOI**: [https://arxiv.org/abs/2405.15793](https://arxiv.org/abs/2405.15793)
*   **Research Problem**: Raw bash terminals overwhelm LLMs with excessive command errors, syntax mismatches, and runaway outputs.
*   **Method**: Introduced the Agent-Computer Interface (ACI), featuring tailored tools for directory exploration, line-numbered file viewing, and precision editing.
*   **Important Finding**: Designing specialized tools improved SWE-bench resolution from under 4% to 12.5% using the same underlying foundation model.
*   **Limitation**: Relies on unguided lexical searching and large cloud context windows, which degrade rapidly on local quantized models.
*   **Relevance to G-HRR**: Informs our baseline architecture and reinforces the need for structured tool guardrails.

---

### 3. GraphCodeBERT: Pre-training Code Representations with Data Flow
*   **Authors**: Daya Guo, Shuo Ren, Shuai Lu, Zhangyin Feng, Duyu Tang, Shujie Liu, Long Zhou, Nan Duan, et al.
*   **Year**: 2021
*   **Venue**: International Conference on Learning Representations (ICLR 2021)
*   **URL / DOI**: [https://openreview.net/forum?id=jLoC4qKcTUQ](https://openreview.net/forum?id=jLoC4qKcTUQ)
*   **Research Problem**: Sequence-based models overlook the semantic structure of source code (variable dependency and data flow).
*   **Method**: Pre-trained transformer models using both AST-derived data-flow graphs and token sequences.
*   **Important Finding**: Integrating data-flow edges drastically improved code search, clone detection, and code translation.
*   **Limitation**: Limited to small encoder models (125M parameters) and single-file snippets rather than full repository multi-hop reasoning.
*   **Relevance to G-HRR**: Provides theoretical foundation proving that explicit graph relationships outperform pure token sequence modeling.

---

### 4. RepoCoder: Repository-Level Code Completion Through Iterative Retrieval and Generation
*   **Authors**: Fengji Zhang, Bei Chen, Yue Zhang, Jinman Liu, Daoguang Zan, Yi Huang, Huanyu Liu, Yongji Wang, Jian-Guang Lou
*   **Year**: 2023
*   **Venue**: ACM Transactions on Software Engineering and Methodology (TOSEM 2023)
*   **URL / DOI**: [https://arxiv.org/abs/2303.12570](https://arxiv.org/abs/2303.12570)
*   **Research Problem**: Repository completion requires cross-file context, but single-pass retrieval retrieves irrelevant snippets.
*   **Method**: Iterative retrieval-augmented generation that uses LLM-generated draft completions as queries for subsequent retrieval rounds.
*   **Important Finding**: Iterative retrieval consistently outperforms single-shot vector RAG on repository completion benchmarks.
*   **Limitation**: Designed for line/token code completion rather than end-to-end bug fixing, test execution, or patch diff generation.
*   **Relevance to G-HRR**: Inspires our closed-loop adaptive retrieval engine, extended from text prompts to code graphs and unit test traces.

---

### 5. Keep the Conversation Going: Fixing Bugs in Humans' and LLMs' Written Code
*   **Authors**: Chunqiu Steven Xia, Lingming Zhang
*   **Year**: 2023
*   **Venue**: ACM/IEEE International Conference on Software Engineering (ICSE 2023)
*   **URL / DOI**: [https://arxiv.org/abs/2304.00385](https://arxiv.org/abs/2304.00385)
*   **Research Problem**: Traditional Automated Program Repair (APR) relies on sampling thousands of candidates without learning from failures.
*   **Method**: Conversational APR prompting LLMs with test execution error traces and compiler feedback over multiple conversational turns.
*   **Important Finding**: Conversational feedback resolved 50+ bugs that single-pass prompting failed to repair.
*   **Limitation**: Focused on single-file functions (Defects4J / QuixBugs) rather than repository-level multi-hop dependencies.
*   **Relevance to G-HRR**: Directly informs G-HRR's test-driven repair loop and stack trace parsing engine.
