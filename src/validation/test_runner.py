"""
Test execution sandbox interface for running pytest and unittests safely.
"""
import subprocess
import time
from typing import Dict, Any, List, Optional

class TestRunner:
    def __init__(self, timeout_seconds: int = 60):
        self.timeout_seconds = timeout_seconds

    def run_tests(self, cwd: str, test_command: str = "pytest") -> Dict[str, Any]:
        """
        Executes test suite in cwd and captures stdout, stderr, and exit codes.
        """
        start_time = time.time()
        try:
            res = subprocess.run(
                test_command,
                cwd=cwd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds
            )
            elapsed = time.time() - start_time
            return {
                "exit_code": res.returncode,
                "passed": res.returncode == 0,
                "stdout": res.stdout,
                "stderr": res.stderr,
                "duration": elapsed,
                "timed_out": False
            }
        except subprocess.TimeoutExpired:
            return {
                "exit_code": -1,
                "passed": False,
                "stdout": "",
                "stderr": f"Test run timed out after {self.timeout_seconds} seconds.",
                "duration": self.timeout_seconds,
                "timed_out": True
            }
        except Exception as e:
            return {
                "exit_code": -1,
                "passed": False,
                "stdout": "",
                "stderr": str(e),
                "duration": 0.0,
                "timed_out": False
            }
