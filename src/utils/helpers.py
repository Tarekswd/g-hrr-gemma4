"""
Common helper functions for file I/O, diff handling, and JSON serialization.
"""
import os
import json
from typing import Dict, Any

def save_json(data: Any, path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def format_unified_diff(original_file: str, original_lines: list, modified_lines: list) -> str:
    import difflib
    diff = difflib.unified_diff(
        original_lines,
        modified_lines,
        fromfile=f"a/{original_file}",
        tofile=f"b/{original_file}",
        lineterm=""
    )
    return "\n".join(diff)
