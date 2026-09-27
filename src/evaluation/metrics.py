"""
Core evaluation metrics calculator for SWE benchmark runs.
"""
from typing import List, Dict, Any

class BenchmarkMetrics:
    def __init__(self):
        pass

    @staticmethod
    def calculate_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates pass rate, average tokens, average tool calls, and average duration.
        """
        n = len(results)
        if n == 0:
            return {
                "sample_size": 0,
                "pass_rate": 0.0,
                "mean_tokens": 0.0,
                "mean_tool_calls": 0.0,
                "mean_duration": 0.0
            }

        passed = sum(1 for r in results if r.get("passed", False))
        total_tokens = sum(r.get("tokens", 0) for r in results)
        total_tool_calls = sum(r.get("tool_calls", 0) for r in results)
        total_duration = sum(r.get("duration", 0.0) for r in results)

        return {
            "sample_size": n,
            "passed_count": passed,
            "pass_rate": (passed / n) * 100.0,
            "mean_tokens": total_tokens / n,
            "mean_tool_calls": total_tool_calls / n,
            "mean_duration": total_duration / n
        }
