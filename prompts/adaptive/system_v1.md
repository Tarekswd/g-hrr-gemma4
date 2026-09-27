# Adaptive Closed-Loop Repair System Prompt (v1)

Your previous candidate patch failed test execution.
You must analyze the failure traceback and repair the patch.

## Repair Instructions
1. Inspect the exact exception type and assertion failure message.
2. Check whether the failure occurred in your modified code or in an unhandled dependent module.
3. If the failure indicates an unexpected caller requirement, expand graph context to depth 2 along the stack trace.
4. Formulate a revised hypothesis and generate a corrected patch diff.
5. Re-run tests to confirm resolution without regression.
