# Kaggle Paper Track: Exact Form Submission Copy-Paste Guide

This document contains the exact text, verified character counts, and file attachments for the **Google - The Gemma 4 Developer Agent Paper Track** submission form.

---

## 1. Title
*Field constraint: Max 80 characters*

```text
G-HRR: Graph-Guided Hierarchical Reasoning for Local Gemma 4 SWE Agents
```
*(Character count: 71 / 80)*

---

## 2. Writeup URL (Slug)
*Field constraint: URL slug under `kaggle.com/competitions/gemma-4-developer-agent-paper/writeups/`*

```text
g-hrr-graph-guided-hierarchical-reasoning
```

---

## 3. Subtitle
*Field constraint: Max 140 characters*

```text
Boosting local Gemma-4-31B SWE-bench resolution from 18% to 44% via AST dependency graphs, hierarchical pruning & closed-loop test repair.
```
*(Character count: 138 / 140)*

---

## 4. Card and Thumbnail Image (560 x 280)
Upload the pre-generated image:
*   **File Path**: `01_research_paper/paper/card_thumbnail_560x280.png`
*   **Dimensions**: Exact `560 x 280` pixels.

---

## 5. Media Gallery (Upload in order)
Upload the high-resolution figures from `01_research_paper/paper/figures/`:
1.  `fig1_architecture.png` (G-HRR System Architecture)
2.  `fig5_system_comparison.png` (Resolution Rate Comparison on SWE-bench)
3.  `fig3_depth_tradeoff.png` (Resolution Rate vs. Graph Expansion Depth)
4.  `fig9_tradeoff_frontier.png` (Pareto-Optimal Token vs. Success Efficiency Frontier)
5.  `fig8_failure_distribution.png` (Failure Category Distribution Shift)

---

## 6. Project Description (Markdown for Kaggle Writeup Editor)

```markdown
# Graph-Guided Hierarchical Repository Reasoning for Local Software Engineering Agents

**Paper Track Submission** | Google DeepMind / Kaggle Gemma 4 Developer Agent Competition  
**Target Venue**: NeurIPS 2026 Expo Presentation  
**Target Model**: `gemma-4-31b-it-qat-w4a16-ct`  

---

### Executive Summary

Deploying autonomous software engineering (SWE) agents on local, 4-bit quantized foundation models—such as Google's open-weights **Gemma 4 31B** (`gemma-4-31b-it-qat-w4a16-ct`)—presents acute challenges. Unconstrained cloud agents rely on 100k+ token windows to ingest large files wholesale. When deployed locally, agents fall prey to two symmetric traps:
1. **The Context Starvation Trap**: Constraining context to single-file snippets isolates the model from caller contracts and downstream type expectations, leading to frequent interface contract violations.
2. **The Context Pollution Trap**: Ingesting extensive source files via dense vector search saturates attention, diluting critical fault signatures and inducing hallucinations in quantized weights.

To solve this, we propose **Graph-Guided Hierarchical Repository Reasoning (G-HRR)**, an agentic framework designed specifically for local software engineering models. Evaluated on a diverse 100-task benchmark cohort from **SWE-bench**, G-HRR elevates issue resolution from **18.0%** (baseline exploration) and **26.0%** (dense semantic retrieval) to **44.0%** ($p < 0.001$, McNemar's test), while cutting token consumption by **34.2%**.

---

### 1. The G-HRR Architecture

G-HRR couples three tightly integrated components:

1. **AST Dependency Graph & Bounded BFS**:
   Parses repository source files into an Abstract Syntax Tree (AST) code graph capturing multi-hop caller-callee, inheritance, containment, and import topologies.
2. **Smallest Sufficient Context Optimization**:
   Rather than dumping entire files, G-HRR filters context into a 5-tier hierarchy:
   * **Level 1**: Top-level repository layout.
   * **Level 2**: Module skeleton (class signatures with pruned bodies).
   * **Level 3**: Focal candidate symbols (full implementations).
   * **Level 4**: Dependency neighborhood (signatures & docstrings of 1-hop callers/callees).
   * **Level 5**: Validation test cases.
3. **Closed-Loop Adaptive Test Repair**:
   Parses `pytest` traceback failures, identifies faulting lines, and adaptively expands graph depth from $d=1$ to $d=2$ along failing call chains.

---

### 2. Empirical Benchmark Results (100 SWE-bench Tasks)

| System Configuration | Resolution Rate ($R_{pass}$) | 95% Bootstrap CI | Mean Tokens | Mean Tool Calls | Duration (s) |
|---|:---:|:---:|:---:|:---:|:---:|
| **System A (Baseline Exploration)** | 18.0% | [11.2, 26.1] | 24,850 | 14.2 | 194.5 |
| **System B (Dense Semantic Retrieval)** | 26.0% | [17.9, 35.2] | 31,420 | 16.8 | 231.2 |
| **System C (Semantic + Graph)** | 33.0% | [24.1, 42.8] | 29,180 | 13.5 | 188.4 |
| **System D (Hierarchical Graph)** | 35.0% | [25.9, 44.9] | **19,240** | **11.2** | **156.8** |
| **System E (Full G-HRR)** | **44.0%** | **[34.3, 54.0]** | 22,610 | 12.8 | 179.3 |

*Statistically significant improvement over baseline: $\chi^2 = 14.2, p < 0.001$ (McNemar's test).*

---

### 3. Key Scientific Discoveries

* **Graph Depth Non-Monotonicity (H6)**: Static expansion beyond depth 1 incurs negative returns ($35.0\% \to 29.0\%$) due to context bloat and distraction. However, **Adaptive Depth** (expanding to depth 2 only along failed test stack traces) achieves the peak **44.0%** resolution.
* **Token Pruning Efficacy (H3)**: Hierarchical filtering prunes 38.8% of tokens compared to dense semantic search while boosting patch resolution by +9.0%.
* **Failure Taxonomy Shift (13 Categories)**: G-HRR collapses localization errors (`wrong_localization`) from **37.8% down to 8.9%**, shifting remaining failures toward subtle edge-case omissions (`incomplete_patch`: 28.6%).

---

### 4. Qualitative Case Study: Django Field Validation

In a real-world defect in `django/models/fields.py`, passing a custom object without string representation to `CharField.validate()` triggered an unhandled `AttributeError` upstream in `clean()`.
* **Baseline Exploration**: Performed keyword search on `AttributeError`. Retrieved `clean()` in `forms/fields.py` (**F1: wrong localization**), applied a null-check, and failed validation tests.
* **Semantic RAG**: Retrieved `CharField.validate()`. Inserted a defensive `try/except` block inside the method (**F4: symptom fix**), breaking caller type expectations.
* **G-HRR Resolution**: Seed retrieval identified `CharField.validate()`. The AST graph expanded 1-hop callers to `Model.clean_fields()`. Hierarchical pruning supplied the caller contract. The Gemma 4 model recognized that `to_python()` must be invoked prior to validation. A 4-line patch was applied and verified by `pytest` within 2 tool calls.

---

### 5. Attachments & Full Paper PDF

* **Full 6-Page Camera-Ready Paper**: Download `paper.pdf` attached below.
* **Complete Reproducible Code**: AST graph builders, RRF retrieval, hierarchical pruning, and unit tests included in the project repository.
```

---

## 7. Attachments
*   **File to Upload**: `01_research_paper/paper/paper.pdf` (Camera-ready 6-page PDF).
*   **Optional Code Attachment**: `01_research_paper/` repository archive.

---

## 8. DOI Citation
*   **Action**: Check the checkbox: **[x] Opt in to DOI creation**.
