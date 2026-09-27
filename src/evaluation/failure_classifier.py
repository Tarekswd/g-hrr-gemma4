"""
Standardized failure taxonomy classifier mapping execution artifacts to the 13 failure categories.
"""
from typing import Dict, Any, List

class FailureClassifier:
    CATEGORIES = [
        "wrong_localization",
        "missing_context",
        "dependency_reasoning_failure",
        "root_cause_failure",
        "syntax_failure",
        "api_misunderstanding",
        "test_misunderstanding",
        "regression",
        "incomplete_patch",
        "over_editing",
        "tool_failure",
        "context_overflow",
        "planning_failure"
    ]

    def classify_failure(
        self,
        task_info: Dict[str, Any],
        patch_diff: str,
        test_output: str,
        tool_call_count: int,
        context_tokens: int,
        true_modified_files: List[str]
    ) -> str:
        """
        Deterministic classification into one of the 13 categories.
        """
        # F11: tool failure
        if "Tool execution timeout" in test_output or "Command failed to launch" in test_output:
            return "tool_failure"

        # F12: context overflow
        if context_tokens > 32000 or "ContextWindowExceeded" in test_output:
            return "context_overflow"

        # F13: planning failure (exhausted budget without generating patch)
        if not patch_diff.strip() or tool_call_count >= 25 and not patch_diff:
            return "planning_failure"

        # F5: syntax failure
        if "SyntaxError" in test_output or "IndentationError" in test_output:
            return "syntax_failure"

        # F1: wrong localization
        patched_files = [line[4:].strip() for line in patch_diff.splitlines() if line.startswith("+++ ")]
        if true_modified_files and patched_files:
            overlap = set(patched_files).intersection(set(true_modified_files))
            if not overlap:
                return "wrong_localization"

        # F10: over-editing (>150 lines changed)
        diff_lines = len(patch_diff.splitlines())
        if diff_lines > 150:
            return "over_editing"

        # F8: regression (tests that previously passed failed)
        if "FAILED (pass_to_pass)" in test_output or "Regression detected" in test_output:
            return "regression"

        # F3: dependency reasoning failure (AttributeError or TypeError on imported caller)
        if "AttributeError" in test_output or "TypeError" in test_output:
            if "has no attribute" in test_output or "takes" in test_output and "positional argument" in test_output:
                return "dependency_reasoning_failure"

        # F6: api misunderstanding
        if "NotImplementedError" in test_output or "DeprecationWarning" in test_output or "ImportError" in test_output:
            return "api_misunderstanding"

        # F4: root cause failure (handled symptom with null check, still failed)
        if "NoneType" in test_output:
            return "root_cause_failure"

        # F7: test misunderstanding
        if "AssertionError" in test_output and "expected" in test_output.lower():
            return "test_misunderstanding"

        # F2: missing context
        if "NameError" in test_output or "UnboundLocalError" in test_output:
            return "missing_context"

        # F9: incomplete patch (default for failed assertions where localization was correct)
        return "incomplete_patch"
