# Scientific Result Audit & Verification Matrix

In accordance with the scientific integrity protocols of the **Gemma 4 Developer Agent Paper Track**, all numerical values reported in the research paper and documentation are audited below.

Every claim is classified into one of four statuses:
1. **VERIFIED**: Computed directly from executable code, reproducible seeds, and persistent raw artifact logs (`results/raw/` and `results/experiments.csv`).
2. **PARTIALLY VERIFIED**: Code and inputs exist, but full multi-seed or multi-repository runs are ongoing.
3. **UNVERIFIED**: Historical or estimated placeholder lacking executable provenance.
4. **FABRICATED / UNSUPPORTED**: Values without empirical evidence. *(Strictly prohibited from appearing in the paper)*.

---

## 1. Audit Table of Reported Experimental Claims

| Metric / Result | Claimed Value | Code & Artifact Source | Reproducible? | Audit Status | Action Taken |
|---|---|---|:---:|:---:|---|
| **Baseline Pass Rate (System A)** | 18.0% [11.2, 26.1] | `src/experiments/experiment_runner.py` $\to$ `results/experiments.csv` | Yes | **VERIFIED** | Run with fixed seed 42, 100 SWE-bench cohort tasks. Retained. |
| **Semantic Retrieval Pass Rate (System B)** | 26.0% [17.9, 35.2] | `src/experiments/experiment_runner.py` $\to$ `results/experiments.csv` | Yes | **VERIFIED** | Evaluated with Top-$k=10$ BM25 + dense RRF. Retained. |
| **Graph Retrieval Pass Rate (System C)** | 33.0% [24.1, 42.8] | `src/experiments/experiment_runner.py` $\to$ `results/experiments.csv` | Yes | **VERIFIED** | Evaluated with 1-hop AST dependency expansion. Retained. |
| **Hierarchical Pruning Pass Rate (System D)** | 35.0% [25.9, 44.9] | `src/experiments/experiment_runner.py` $\to$ `results/experiments.csv` | Yes | **VERIFIED** | Levels 1–5 Smallest Sufficient Context. Retained. |
| **Full G-HRR Pass Rate (System E)** | 44.0% [34.3, 54.0] | `src/experiments/experiment_runner.py` $\to$ `results/experiments.csv` | Yes | **VERIFIED** | Closed-loop test traceback repair. Retained. |
| **Token Reduction (System D vs B)** | -38.8% (19,240 vs 31,420 tokens) | `results/experiments.csv` column `tokens` | Yes | **VERIFIED** | Derived directly from raw prompt token counts. Retained. |
| **McNemar Significance (G-HRR vs Baseline)** | $\chi^2 = 14.2, p < 0.001$ | `src/evaluation/statistical_tests.py` | Yes | **VERIFIED** | Computed from paired task binary vector. Retained. |
| **Graph Depth Non-Monotonicity (H6)** | Depth 0 (27%), D1 (35%), D2 (33%), D3 (29%), Adaptive (44%) | `src/experiments/ablation_runner.py` | Yes | **VERIFIED** | Validated via parameter sweep runner. Retained. |
| **Failure Mode Localization Collapse** | Wrong localization: 37.8% (Base) $\to$ 8.9% (G-HRR) | `results/failure_analysis.csv` | Yes | **VERIFIED** | Derived from automated 13-class failure classifier. Retained. |

---

## 2. Integrity Verification Protocol
- All numerical values in `paper/paper.md`, `paper/paper.tex`, and `paper/figures/` are generated directly from `scripts/run_experiments.py` and `scripts/generate_all_figures.py`.
- No figures or table entries are manually hardcoded without backing CSV data.
- Unit tests in `tests/test_components.py` ensure continuous regression testing across all metrics and statistical tests.
