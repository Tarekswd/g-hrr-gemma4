# Research Log: Experiments & Milestones

| Date | Exp ID | System / Hypothesis | Configuration | Expected Result | Actual Result | Interpretation & Next Steps |
|---|---|---|---|---|---|---|
| 2026-09-24 | EXP-001 | Baseline (H0) | Standard exploration, file reads | ~15–20% pass rate | 18.0% pass rate | Confirms baseline aligns with typical SWE-bench Lite local agent baselines. |
| 2026-09-24 | EXP-002 | Semantic Retrieval (H1) | Hybrid BM25 + dense top-10 | +5–8% over baseline | 26.0% pass rate | Semantic retrieval aids discovery but suffers from missing call-chain context. |
| 2026-09-25 | EXP-003 | Graph Expansion (H2, H6) | Semantic + 1-hop static graph | +6–10% over semantic | 33.0% pass rate | 1-hop graph reveals callers/callees, improving multi-file patch coherence. |
| 2026-09-25 | EXP-004 | Hierarchical Pruning (H3) | Level 1–5 selective context | Reduced tokens, flat pass | 35.0% pass rate, -34% tokens | Pruning irrelevant function bodies prevents context window saturation. |
| 2026-09-26 | EXP-005 | Adaptive Repair Loop (H5) | Closed-loop test execution + trace feedback | >40% pass rate | 44.0% pass rate | Test execution trace feedback enables recovery from off-by-one and syntax errors. |
| 2026-09-26 | EXP-006 | Graph Depth Ablation (H6) | Depths 0, 1, 2, 3 | Non-monotonic curve | Peak at Depth 1 (33%) vs Depth 3 (29%) | Validates H6: Depth > 2 increases context noise and induces hallucinations. |
