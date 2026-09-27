# Comprehensive Survey: SWE Benchmarks and Autonomous Coding Agents

## 1. The SWE-bench Paradigm
*   **Paper Reference**: Jimenez et al., *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* (ICLR 2024).
*   **Core Task**: Given a repository snapshot and a GitHub issue description (problem statement), generate a unified git diff patch that resolves the issue such that the repository's test suite passes (evaluating `FAIL_TO_PASS` and `PASS_TO_PASS` tests).
*   **Key Bottleneck for Local Models**: Real-world repositories contain tens or hundreds of thousands of lines of code. Local, quantized models (like 31B parameter models) suffer from context dilution, hallucination of non-existent APIs, and loss of attention when bombarded with tens of thousands of tokens of irrelevant code.

## 2. Agentic Architectures (SWE-agent, Aider, Devin)
*   **SWE-agent** (Yang et al., 2024): Introduced the Agent-Computer Interface (ACI). Emphasized tailored toolsets (line-numbered file viewers, directory explorers, targeted search) rather than raw bash shells to prevent models from generating runaway commands or crashing contexts.
*   **RepoCoder & GraphCodeBERT**:
    *   Zhang et al., *RepoCoder: Iterative Retrieval-Augmented Generation for Repository-Level Code Completion*. Showed that iterative retrieval using generated pseudo-code outperforms single-pass retrieval.
    *   Guo et al., *GraphCodeBERT: Pre-training Language Models with Multi-Hop Data Flow*. Demonstrated that semantic code graphs (AST data flow and control flow) anchor model reasoning better than pure token sequences.

## 3. The Retrieval-Augmented Dilemma in Local SWE Agents
*   Dense vector search alone retrieves textually or semantically similar snippets (e.g., function names matching words in the issue).
*   However, software bugs are often caused by **dependency chains**: callers passing invalid arguments, overridden virtual methods in sibling files, or configuration schemas defined in parent directories.
*   Pure vector RAG misses these structural links. Graph-guided retrieval explicitly expands candidate symbols through their call/import graph to uncover root causes without bloating the context with irrelevant files.
