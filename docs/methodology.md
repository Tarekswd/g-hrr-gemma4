# Scientific Methodology & Experimental Protocol

## 1. Benchmark Task Formulation
Experiments are evaluated on a representative cohort of 100 diverse repository-level tasks sampled from **SWE-bench Lite / Verified** across leading open-source repositories (`astropy`, `django`, `matplotlib`, `psf/requests`, `pytest-dev/pytest`, `scikit-learn`, `sympy`).

Each task instance $T = (R, I, t_{val})$ consists of:
*   $R$: Git repository snapshot at the commit immediately prior to the issue resolution.
*   $I$: Problem statement text (GitHub issue title + body).
*   $t_{val}$: Validation test suite comprising both `FAIL_TO_PASS` (must pass after patch) and `PASS_TO_PASS` (must not regress).

## 2. Compared Systems (Controlled Configurations)
1.  **System A (Baseline)**: Conventional keyword search + standard file exploration.
2.  **System B (Semantic Retrieval)**: Hybrid BM25 + dense code embeddings ($k \in \{5, 10, 20, 40, 80\}$).
3.  **System C (Semantic + Graph)**: Semantic retrieval expanded with static code graph neighbors (Depths 0, 1, 2, 3).
4.  **System D (Hierarchical Graph)**: Multi-level hierarchical pruning (Repo $\to$ Module $\to$ Symbol $\to$ 1-hop Graph).
5.  **System E (Adaptive Repair)**: Full hierarchical graph + closed-loop test execution feedback and targeted repair.

## 3. Evaluation Metrics
*   **Resolution Rate ($R_{pass}$)**: $\frac{N_{pass}}{N_{total}} \times 100\%$.
*   **Token Consumption ($\bar{T}$)**: Mean total tokens per issue (prompt + generation).
*   **Tool Calls ($\bar{C}_{tool}$)**: Mean tool invocations per task.
*   **Runtime ($\bar{\tau}$)**: Wall-clock duration per issue in seconds.
*   **Statistical Significance**: McNemar's paired test for binary pass/fail comparisons; 95% bootstrap confidence intervals (1,000 resamples).
