"""
Full empirical benchmark execution script.
Runs 100-task cohort across all 5 systems, computes statistical intervals,
and writes experiments.csv and failure_analysis.csv.
"""
import os
import sys
import csv
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.experiments.experiment_runner import BenchmarkCohortGenerator, ExperimentRunner
from src.evaluation.metrics import BenchmarkMetrics
from src.evaluation.statistical_tests import StatisticalAnalysis

def main():
    parser = argparse.ArgumentParser(description="Run empirical SWE benchmark suite")
    parser.add_argument("--cohort-size", type=int, default=100, help="Number of benchmark tasks")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    print(f"=== Initializing Empirical Benchmark (N={args.cohort_size}, Seed={args.seed}) ===")
    tasks = BenchmarkCohortGenerator.generate_cohort(n_tasks=args.cohort_size, seed=args.seed)
    runner = ExperimentRunner(seed=args.seed)

    systems = [
        ("baseline", "System A (Baseline)"),
        ("semantic", "System B (Semantic)"),
        ("graph", "System C (Graph)"),
        ("hierarchical", "System D (Hierarchical)"),
        ("adaptive_full", "System E (G-HRR Full)")
    ]

    all_results = []
    system_summaries = {}
    system_outcomes = {}

    for sys_key, sys_label in systems:
        print(f"Evaluating {sys_label}...")
        runs = runner.run_system_evaluation(sys_key, tasks)
        all_results.extend(runs)

        outcomes = [1 if r["passed"] else 0 for r in runs]
        system_outcomes[sys_key] = outcomes
        summary = BenchmarkMetrics.calculate_summary(runs)
        mean, lower, upper = StatisticalAnalysis.bootstrap_ci(outcomes)
        summary["ci_lower"] = lower
        summary["ci_upper"] = upper
        system_summaries[sys_key] = summary

    # Export results/experiments.csv
    exp_csv_path = os.path.join(os.path.dirname(__file__), "..", "results", "experiments.csv")
    os.makedirs(os.path.dirname(exp_csv_path), exist_ok=True)
    with open(exp_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["system", "instance_id", "passed", "tokens", "tool_calls", "duration", "failure_category"])
        writer.writeheader()
        writer.writerows(all_results)
    print(f"Exported raw runs to: {exp_csv_path}")

    # Export results/failure_analysis.csv
    fail_csv_path = os.path.join(os.path.dirname(__file__), "..", "results", "failure_analysis.csv")
    failure_counts = {}
    for r in all_results:
        if not r["passed"] and r["failure_category"]:
            sys_id = r["system"]
            cat = r["failure_category"]
            if sys_id not in failure_counts:
                failure_counts[sys_id] = {}
            failure_counts[sys_id][cat] = failure_counts[sys_id].get(cat, 0) + 1

    with open(fail_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["system", "failure_category", "count"])
        for sys_id, cat_dict in failure_counts.items():
            for cat, count in cat_dict.items():
                writer.writerow([sys_id, cat, count])
    print(f"Exported failure analysis to: {fail_csv_path}")

    # Print summary table
    print("\n" + "=" * 80)
    print("BENCHMARK SUMMARY RESULTS")
    print("=" * 80)
    print(f"{'System':<25} | {'Pass Rate':<18} | {'Tokens':<10} | {'Tools':<8} | {'Duration (s)':<12}")
    print("-" * 80)
    for sys_key, sys_label in systems:
        s = system_summaries[sys_key]
        pass_str = f"{s['pass_rate']:.1f}% [{s['ci_lower']:.1f}, {s['ci_upper']:.1f}]"
        print(f"{sys_label:<25} | {pass_str:<18} | {int(s['mean_tokens']):<10} | {s['mean_tool_calls']:<8.1f} | {s['mean_duration']:<12.1f}")
    print("=" * 80)

    # McNemar test: Full G-HRR vs Baseline
    mcnemar = StatisticalAnalysis.mcnemar_test(system_outcomes["baseline"], system_outcomes["adaptive_full"])
    print(f"\nMcNemar Test (G-HRR vs Baseline): Chi2={mcnemar['chi2']:.3f}, p-value={mcnemar['p_value']:.4e}")

if __name__ == "__main__":
    main()
