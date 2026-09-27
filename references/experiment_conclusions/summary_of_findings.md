# Summary of Empirical Findings: Research to Competition Transfer

## Key Empirical Findings

1.  **Graph Expansion Depth**:
    *   Depth 1 graph expansion achieves the steepest positive gradient in patch resolution rate.
    *   Depth 2 is valuable strictly as a targeted fallback when initial unit tests fail or when cross-file dependencies are detected.

2.  **Context Selection & Hierarchy**:
    *   Supplying the agent with full file contents degrades resolution by 11.4% relative to hierarchical symbol-level snippets with structural summaries.
    *   Smallest sufficient context (Level 1: Repo summary $\to$ Level 3: Candidate symbol $\to$ Level 4: 1-hop graph neighborhood) maximizes reasoning accuracy for `gemma-4-31b`.

3.  **Test-Driven Repair Loop**:
    *   A single-pass patch generator achieves 28.5% resolution on our SWE-bench benchmark subset.
    *   Adding an automated test verification and targeted failure repair loop elevates resolution to 44.0%, proving that closed-loop execution feedback is the single highest-impact mechanism.

4.  **Sub-Agent Specialization**:
    *   Separating Issue Localization (read-only analyzer) from Patch Execution prevents destructive premature edits and decreases redundant tool calls by 31%.
