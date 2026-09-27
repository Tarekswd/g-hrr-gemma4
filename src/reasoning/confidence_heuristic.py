"""
Confidence heuristic estimator for patch correctness and localization reliability.
Note: Named and treated strictly as a heuristic score, not a calibrated statistical probability.
"""
from typing import Dict, Any, List

class ConfidenceHeuristic:
    def __init__(self):
        pass

    def compute_heuristic(
        self,
        test_passed: bool,
        lines_changed: int,
        files_changed: int,
        syntax_valid: bool,
        test_coverage_matches: bool
    ) -> float:
        """
        Calculates a confidence heuristic between 0.0 and 1.0.
        """
        score = 0.0

        if not syntax_valid:
            return 0.0

        # Syntax validity baseline
        score += 0.2

        if test_passed:
            score += 0.5
        else:
            # If test failed, confidence cannot exceed 0.35
            return min(score + 0.15 if test_coverage_matches else 0.1, 0.35)

        # Penalize excessive edits (over-editing)
        if lines_changed <= 15:
            score += 0.15
        elif lines_changed <= 50:
            score += 0.10
        elif lines_changed > 150:
            score -= 0.15

        # Penalize multi-file sprawl unless required
        if files_changed == 1:
            score += 0.10
        elif files_changed > 3:
            score -= 0.10

        if test_coverage_matches:
            score += 0.05

        return max(0.0, min(1.0, score))
