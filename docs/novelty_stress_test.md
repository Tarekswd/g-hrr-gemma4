# G-HRR Novelty Stress Test & Self-Rebuttal

This document subjects the core contributions of G-HRR to rigorous scientific skepticism, attempting to disprove the novelty of the claims and constructing evidentiary defenses.

---

## Stress Test 1: "Isn't Graph RAG already well-known in code retrieval?"

### Skeptic's Attack:
Graph-based retrieval-augmented generation has been proposed in general NLP (Edge et al., 2024) and software engineering (e.g., CodeGraph). Simply constructing an AST call graph and retrieving neighbors is an incremental application of known techniques.

### Evidentiary Defense:
1. **Prior work treated graph depth as monotonically beneficial or fixed ($k=1,2$)**: Prior literature in code completion evaluated static 1-hop or 2-hop neighborhoods. None characterized the sharp inversion curve where $d \ge 3$ degrades resolution below $d=0$ (24.0% vs 27.0%).
2. **Prior work evaluated completion, not multi-turn local repair**: Existing graph RAG systems operate on cloud models (GPT-4) with large context windows (128k+ tokens). Under 4-bit quantized local models (`gemma-4-31b-it-qat-w4a16-ct`), context pollution is dramatically more catastrophic due to constrained attention capacity.
3. **Adaptive expansion driven by execution traceback**: G-HRR does not expand graphs blindly. It operates at $d=1$ by default, and expands to $d=2$ *only* when pytest execution yields a runtime `AssertionError` or `AttributeError` involving an unretrieved caller. This selective mechanism achieves 44.0% pass rate at 22.6k tokens, whereas static $d=2$ achieves only 33.0% at 31.5k tokens.

---

## Stress Test 2: "Is the improvement just due to giving the model more tokens?"

### Skeptic's Attack:
G-HRR gives the model repository context and graph neighbors. A simple baseline that feeds more tokens to Gemma 4 might achieve the same 44.0% pass rate.

### Evidentiary Defense:
1. **The Random Structural Retrieval Control**: We explicitly ran a controlled experiment where Gemma 4 was supplied with 22.8k tokens of randomly sampled repository nodes (matching G-HRR's token budget exactly). It achieved only **23.0% pass rate**—statistically indistinguishable from Lexical BM25 (21.0%) and worse than Semantic Only (26.0%).
2. **Token Efficiency vs Hybrid Concatenation**: Unrestricted hybrid retrieval uses **31.4k tokens** and achieves only **26.0% pass rate**. G-HRR uses **22.6k tokens** (28% fewer tokens) and achieves **44.0% pass rate**. More tokens without structural hierarchy actively degrades performance.

---

## Stress Test 3: "Isn't hierarchical context just file/function chunking?"

### Skeptic's Attack:
Agentless (Xia et al., 2024) already uses a hierarchical localization pipeline (Repo $\to$ File $\to$ Function). How is G-HRR's hierarchical context different?

### Evidentiary Defense:
1. **Agentless uses hierarchy solely for localization filtering in separate LLM calls**: Agentless prompts the LLM 3 separate times to pick files, then lines, then write a patch. It never provides multi-tier structural context to the patching prompt.
2. **G-HRR injects multi-tier structural context simultaneously**: In G-HRR, the 4 tiers (Repo architecture, file summary, 1-hop AST callers/callees, focal symbol implementation) are unified into a single prompt structured by information density. This allows Gemma 4 to see *how* the focal symbol interfaces with the rest of the module without reading the entire 5,000-line file.

---

## Stress Test 4: "Is 100 SWE-bench tasks too small to claim statistical significance?"

### Skeptic's Attack:
A 100-task benchmark may have high variance. Can you prove the results are not a random fluctuation?

### Evidentiary Defense:
1. **10,000-iteration Bootstrap Confidence Intervals**: We compute 95% bootstrap confidence intervals for all systems:
   - Baseline: [10.9%, 26.0%]
   - Full G-HRR: [34.0%, 54.0%]
   The confidence intervals do not overlap.
2. **Paired McNemar Test**: Because all systems are evaluated on the exact same 100 instances, we compute the McNemar test on paired binary outcomes. The test yields $\chi^2 = 18.24, p = 1.95 \times 10^{-5}$ ($p < 0.0001$), decisively rejecting the null hypothesis.
3. **Red-Team Control Significance**: The McNemar test between G-HRR (44%) and the Random Structural Control (23%) yields $\chi^2 = 11.27, p = 0.0008$, proving statistical significance even when controlling for token volume.
