# Declarative Agent Architecture Patterns for Kaggle Gemma 4

## 1. Principles of Declarative Agent Configuration
In `swegemma`, agents are configured via YAML without arbitrary Python runtime orchestration.
The architecture relies on:
1.  **Strict Hierarchical Decomposition**:
    *   **Root Agent (`agent.yaml`)**: Acts as the primary controller, managing the loop between analysis, navigation, code editing, and patch submission.
    *   **Sub-Agents (`sub_agents/`)**: Specialized agents with constrained toolsets (e.g. read-only `analyzer` for localization, `reviewer` for patch safety).
2.  **Modular Prompt Composition**:
    *   System prompts utilize modular references or structured sections to guarantee clear cognitive separation between reasoning steps.
3.  **Deterministic Tool Budgets**:
    *   To avoid infinite exploration loops within the 12-hour evaluation budget, the agent's instructions enforce finite tool iterations per task phase:
        *   Exploration & Retrieval: $\le 6$ calls.
        *   Patch Generation & Application: $\le 4$ calls.
        *   Verification & Repair: $\le 3$ loops.
