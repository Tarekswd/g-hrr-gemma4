# SWE-Gemma Competition Runtime, Environment, and Rules

## 1. Official Constraints & Environment
*   **Target Model**: `gemma-4-31b-it-qat-w4a16-ct`.
    *   31-Billion parameter Instruction-Tuned Gemma 4.
    *   Quantization-Aware Training (QAT), 4-bit weights, 16-bit activations (W4A16).
    *   Optimized for high-throughput, low-VRAM inference on local/competition hardware.
*   **Submission Format**: `submission.zip` uploaded directly to Kaggle.
    *   `agent.yaml` MUST reside at the root of `submission.zip`.
    *   Sandboxed YAML compilation (`compile_submission`). Dynamic python entry points (e.g. `main.py` executing external network calls) are strictly prohibited.
*   **Runtime Budget**:
    *   Total 12-hour evaluation window across all test instances.
    *   Air-gapped, offline evaluation environment. No internet access allowed during grading.
*   **Evaluation Metric**:
    *   Percentage of repository issues whose generated patch passes test suite validation:
        $$\text{Score} = \frac{\sum_{i=1}^N \mathbf{1}(\text{Task}_i \text{ passes})}{\text{Total Tasks } N}$$

## 2. Standard Built-In Tool Capabilities (`swegemma`)
The competition framework exposes 9 primary tools:
1.  `run_command`: Executes sandboxed bash shell commands (e.g., `pytest`, `git diff`).
2.  `read_file`: Views file contents with optional line boundaries.
3.  `edit_file`: Performs precision edits or string replacements.
4.  `write_file`: Writes/overwrites files.
5.  `get_status`: Inspects git status and uncommitted changes.
6.  `submit_patch`: Finalizes the solution diff and concludes the agent turn.
7.  `get_code_neighbors`: Queries symbol relationships (callers, callees, definitions, imports).
8.  `search_similar_code`: Dense embedding search over repository code chunks.
9.  `get_code_subgraph`: Extracts subgraphs of interconnected symbols.
