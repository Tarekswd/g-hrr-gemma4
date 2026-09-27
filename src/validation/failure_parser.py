"""
Test failure parser extracting exception names, faulting files, line numbers, and assertions.
"""
import re
from typing import Dict, Any, List, Optional

class FailureParser:
    def __init__(self):
        pass

    def parse_traceback(self, output: str) -> Dict[str, Any]:
        """
        Parses pytest or python traceback to extract relevant fault information.
        """
        lines = output.splitlines()
        exception_type: Optional[str] = None
        exception_msg: Optional[str] = None
        faulting_file: Optional[str] = None
        faulting_line: Optional[int] = None
        failing_assertion: Optional[str] = None

        # Look for File "...", line X patterns
        file_line_matches = re.findall(r'File "([^"]+)", line (\d+)', output)
        if file_line_matches:
            # Last match in stack trace is usually the immediate fault
            faulting_file, line_str = file_line_matches[-1]
            faulting_line = int(line_str)

        # Look for Exception / Error lines at bottom
        for line in reversed(lines):
            match = re.match(r'^([A-Za-z0-9_]+Error|[A-Za-z0-9_]+Exception):\s*(.*)', line.strip())
            if match:
                exception_type = match.group(1)
                exception_msg = match.group(2)
                break
            elif "FAILED " in line or "AssertionError" in line:
                if not exception_type:
                    exception_type = "AssertionError"
                    exception_msg = line.strip()

        # Look for assertion failures
        for i, line in enumerate(lines):
            if "E       assert " in line or "E       AssertionError:" in line:
                failing_assertion = line.strip()
                break

        return {
            "has_failure": bool(exception_type or faulting_file),
            "exception_type": exception_type or "UnknownError",
            "exception_msg": exception_msg or "",
            "faulting_file": faulting_file,
            "faulting_line": faulting_line,
            "failing_assertion": failing_assertion
        }
