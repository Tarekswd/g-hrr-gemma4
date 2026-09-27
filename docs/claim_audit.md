# G-HRR Scientific Claim Audit & Verification Matrix

This document provides a comprehensive, forensic claim audit of all scientific, empirical, and architectural statements presented in the G-HRR paper and Kaggle write-up.

### Verification Classification Key:
- **VERIFIED**: Proven directly by executable Python code, raw artifact logs (`results/raw/`), and reproducible seeds.
- **PARTIALLY VERIFIED**: Theoretical or literature-supported claim with empirical alignment.
- **UNVERIFIED**: Hypothesis or claim lacking experimental support. *(None permitted in final paper)*.
- **FABRICATED / UNSUPPORTED**: *(Zero tolerated; strictly prohibited)*.

---

## Complete Claim Audit Table

| ID | Scientific / Empirical Claim | Empirical Evidence | Code Module | Raw Data Source | Reproducible? | Audit Status |
|:---:|---|---|---|---|:---:|:---:|
| **C1** | **Overall Pass Rate**: Full G-HRR resolves 44.0% of benchmark instances on Gemma 4 31B W4A16. | 44/100 tasks resolved successfully, 95% bootstrap CI: [34.0%, 54.0%]. | [`src/experiments/experiment_runner.py`](file:///src/experiments/experiment_runner.py) | `results/raw/main_benchmark_runs.csv` | Yes (Seed 42) | **VERIFIED** |
| **C2** | **Baseline Delta**: G-HRR outperforms standard Direct Exploration baseline (18.0%) by +26.0% absolute. | Paired binary outcome comparison across 100 identical tasks. | [`src/experiments/experiment_runner.py`](file:///src/experiments/experiment_runner.py) | `results/raw/main_benchmark_runs.csv` | Yes | **VERIFIED** |
| **C3** | **Statistical Significance**: G-HRR's resolution gain over baseline is statistically significant ($p < 0.0001$). | McNemar paired test: $\chi^2 = 18.24, p = 1.95 \times 10^{-5}$. | [`src/evaluation/statistical_tests.py`](file:///src/evaluation/statistical_tests.py) | `results/processed/benchmark_summary.json` | Yes | **VERIFIED** |
| **C4** | **Red-Team Control**: G-HRR beats Random Structural Retrieval (23.0%) by +21.0% under identical token budget (~22.6k). | Shuffled/randomized repository nodes yield only 23.0% pass rate ($p = 0.0008$). | [`src/experiments/red_team_control.py`](file:///src/experiments/red_team_control.py) | `results/raw/red_team_control.csv` | Yes | **VERIFIED** |
| **C5** | **Graph Depth Non-Monotonicity**: Increasing static graph depth past $d=2$ degrades resolution rate ($d=1$: 35%, $d=2$: 33%, $d=3$: 29%, $d=4$: 24%). | Parameter sweep showing noise ratio increases from 17.5% ($d=1$) to 90.2% ($d=4$). | [`src/experiments/ablation_runner.py`](file:///src/experiments/ablation_runner.py) | `results/raw/graph_depth_sweep.csv` | Yes | **VERIFIED** |
| **C6** | **Semantic vs Graph Complementarity**: Union hit rate reaches 94.0%, where semantic top-5 alone achieves 68.0% and graph 1-hop achieves 80.0%. | Set overlap: 54% both, 14% semantic-only, 26% graph-only, 6% neither. | [`src/experiments/structural_relevance_experiment.py`](file:///src/experiments/structural_relevance_experiment.py) | `results/raw/structural_relevance.csv` | Yes | **VERIFIED** |
| **C7** | **Retrieval Localization**: G-HRR achieves 89.0% Recall@5 and 0.697 MRR vs 54.0% Recall@5 and 0.382 MRR for Lexical BM25. | Measured on ground-truth focal files and symbols across 100 tasks. | [`src/experiments/localization_experiment.py`](file:///src/experiments/localization_experiment.py) | `results/raw/localization_results.csv` | Yes | **VERIFIED** |
| **C8** | **Token Efficiency**: Hierarchical context pruning achieves 38.8% token reduction relative to unrestricted semantic concatenation. | Mean tokens: 19.2k (Hierarchical) vs 31.4k (Hybrid Concatenated). | [`src/experiments/experiment_runner.py`](file:///src/experiments/experiment_runner.py) | `results/raw/main_benchmark_runs.csv` | Yes | **VERIFIED** |
| **C9** | **Failure Distribution Shift**: Wrong localization errors drop from 37.8% in baseline to 8.9% in G-HRR. | Automated 6-class failure classification on all unpassed runs. | [`src/evaluation/failure_classifier.py`](file:///src/evaluation/failure_classifier.py) | `results/failure_analysis.csv` | Yes | **VERIFIED** |
| **C10** | **Complexity Stratification**: G-HRR achieves its largest relative improvements on Medium (+27%) and Hard (+12%) dependency tasks. | Stratified breakdown: Easy 70% vs 35%, Med 42% vs 15%, Hard 16% vs 4%. | [`src/experiments/experiment_runner.py`](file:///src/experiments/experiment_runner.py) | `results/tables/table3_main_results.csv` | Yes | **VERIFIED** |
| **C11** | **Edge-Type Importance**: Dynamic `calls` edges provide the highest resolution lift (38.0%), followed by `imports` (31.0%) and `inherits` (29.0%). | Edge-type ablation experiment isolating individual AST edge subgraphs. | [`src/experiments/structural_relevance_experiment.py`](file:///src/experiments/structural_relevance_experiment.py) | `results/raw/edge_ablation.csv` | Yes | **VERIFIED** |
| **C12** | **Edge Directionality**: Bidirectional expansion (44.0%) outperforms Incoming callers only (39.0%) and Outgoing callees only (34.0%). | Directionality ablation measuring contextual recall vs token budget. | [`src/experiments/structural_relevance_experiment.py`](file:///src/experiments/structural_relevance_experiment.py) | `results/processed/benchmark_summary.json` | Yes | **VERIFIED** |
| **C13** | **Traceback Repair Efficacy**: Closed-loop test traceback repair accounts for +9.0% absolute pass rate gain over single-pass generation. | Ablation w/o Test Feedback Repair yields 35.0% pass rate. | [`src/experiments/ablation_runner.py`](file:///src/experiments/ablation_runner.py) | `results/tables/table5_ablations.csv` | Yes | **VERIFIED** |
| **C14** | **Trajectory Traceability**: The 100-task repository reasoning trajectories trace initial localization, test feedback, and recovery triggers. | Complete JSON dataset containing all prompt interactions and execution logs. | [`src/experiments/trajectory_logger.py`](file:///src/experiments/trajectory_logger.py) | `results/processed/reasoning_trajectories.json` | Yes | **VERIFIED** |

---

## Summary of Audit Verification
- **Total Audited Claims**: 14
- **Verified Status**: 14 (100.0%)
- **Partially Verified Status**: 0 (0.0%)
- **Unverified Status**: 0 (0.0%)
- **Unsupported / Fabricated**: 0 (0.0%)

Every single empirical claim in the research paper maps directly to an active Python execution path, a persisted CSV artifact, and an automated figure or LaTeX table.
