# Reproduction Guide

## Environment Setup
Ensure Python 3.10+ is installed.
```bash
cd 01_research_paper
# Optional virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

## Running the Verification Suite
Execute component tests to ensure all AST parsers, graph engines, and retrieval metrics operate deterministically:
```bash
python -m unittest discover tests
```

## Running the Empirical Benchmark Suite
To execute the five comparative configurations and the complete ablation matrix:
```bash
python scripts/run_experiments.py --cohort-size 100 --seed 42
```
This produces:
*   `results/experiments.csv`: Detailed task-by-task results across all systems.
*   `results/failure_analysis.csv`: Categorization of all 13 error modes across failed runs.
*   `results/tables/summary_table.md`: Formatted LaTeX and Markdown tables.

## Generating Publication Visuals
To render all paper figures:
```bash
python scripts/generate_plots.py
```
Outputs are written directly to `paper/figures/`.
