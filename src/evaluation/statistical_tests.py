"""
Statistical analysis tools: bootstrap confidence intervals and McNemar's paired test for binary success.
"""
import random
import math
from typing import List, Tuple, Dict, Any

class StatisticalAnalysis:
    @staticmethod
    def bootstrap_ci(binary_outcomes: List[int], n_resamples: int = 1000, alpha: float = 0.05) -> Tuple[float, float, float]:
        """
        Calculates empirical mean and (1 - alpha) bootstrap confidence intervals.
        """
        n = len(binary_outcomes)
        if n == 0:
            return 0.0, 0.0, 0.0

        sample_mean = (sum(binary_outcomes) / n) * 100.0
        resample_means = []

        random.seed(42)
        for _ in range(n_resamples):
            resample = [random.choice(binary_outcomes) for _ in range(n)]
            resample_means.append((sum(resample) / n) * 100.0)

        resample_means.sort()
        lower_idx = int((alpha / 2.0) * n_resamples)
        upper_idx = int((1.0 - alpha / 2.0) * n_resamples)

        ci_lower = resample_means[lower_idx]
        ci_upper = resample_means[min(upper_idx, n_resamples - 1)]

        return sample_mean, ci_lower, ci_upper

    @staticmethod
    def mcnemar_test(outcomes_a: List[int], outcomes_b: List[int]) -> Dict[str, Any]:
        """
        McNemar's test for paired binary outcomes.
        Returns contingency table, chi-square statistic with continuity correction, and approximate p-value.
        """
        assert len(outcomes_a) == len(outcomes_b), "Outcomes lists must have identical lengths."

        # a: pass A, pass B
        # b: pass A, fail B
        # c: fail A, pass B
        # d: fail A, fail B
        b = 0
        c = 0

        for oa, ob in zip(outcomes_a, outcomes_b):
            if oa == 1 and ob == 0:
                b += 1
            elif oa == 0 and ob == 1:
                c += 1

        if (b + c) == 0:
            return {"chi2": 0.0, "p_value": 1.0, "b": b, "c": c}

        # Edwards continuity correction
        chi2 = (abs(b - c) - 1.0) ** 2 / (b + c)
        # Approximate p-value using chi2 with 1 degree of freedom (survival function approximation)
        p_value = math.erfc(math.sqrt(chi2 / 2.0))

        return {
            "chi2": chi2,
            "p_value": p_value,
            "b_only_a_passed": b,
            "c_only_b_passed": c
        }
