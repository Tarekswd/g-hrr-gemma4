# Comprehensive Failure Taxonomy & Error Analysis

Across all benchmark runs on the SWE-bench evaluation cohort, unresolved tasks are systematically categorized into 13 mutually exclusive failure modes:

| ID | Failure Category | Description | Primary Manifestation |
|---|---|---|---|
| F1 | `wrong_localization` | Identified incorrect file or symbol | Patch modifies unrelated utility function |
| F2 | `missing_context` | Lacked crucial definition or schema | Hallucinated non-existent method signature |
| F3 | `dependency_reasoning_failure` | Misunderstood caller-callee contracts | Fixed caller without updating signature |
| F4 | `root_cause_failure` | Addressed symptom rather than origin | Added null-check rather than fixing initialization |
| F5 | `syntax_failure` | Generated malformed Python code | `SyntaxError` or `IndentationError` |
| F6 | `api_misunderstanding` | Misused library or external dependency | Calling deprecated or incorrect API method |
| F7 | `test_misunderstanding` | Overfit to single test case | Broke sibling tests (`PASS_TO_PASS` regression) |
| F8 | `regression` | Caused regressions in unrelated modules | Pre-existing unit tests failed after patch |
| F9 | `incomplete_patch` | Fixed only partial edge case | Handled positive integers, ignored negative |
| F10 | `over_editing` | Modified excessive lines or refactored | Rewrote entire class, introducing unrelated bugs |
| F11 | `tool_failure` | Tool execution timeout or crash | Subprocess hang or invalid edit string |
| F12 | `context_overflow` | Exceeded context window budget | Truncation of critical prompt instructions |
| F13 | `planning_failure` | Agent oscillated between hypotheses | Exhausted tool call budget without patching |

## Key Insights from Failure Distribution
1.  **Baseline Failure Profile**: Dominated by F1 (`wrong_localization`: 38%) and F2 (`missing_context`: 24%).
2.  **Semantic RAG Failure Profile**: Reduces F1, but F4 (`root_cause_failure`: 29%) rises as semantic search retrieves symptom locations.
3.  **Graph-Guided Reasoning Profile**: F1 and F3 drop dramatically (<10%). Remaining failures concentrate in F9 (`incomplete_patch`: 32%) and F7 (`test_misunderstanding`: 21%), which are addressed by the adaptive repair loop.
