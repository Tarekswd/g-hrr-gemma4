"""
Code and context compression removing superfluous comments, whitespace, and irrelevant function bodies.
"""
import re

class ContextCompressor:
    def __init__(self):
        pass

    def compress_code(self, code: str, preserve_signatures: bool = True) -> str:
        """
        Compress code by removing inline comments and consecutive empty lines.
        """
        # Remove single-line comments
        lines = []
        for line in code.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") and not stripped.startswith("#!"):
                continue
            lines.append(line)

        cleaned = "\n".join(lines)
        # Collapse multiple empty lines to one
        cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
        return cleaned

    def prune_method_bodies(self, class_code: str) -> str:
        """
        Prunes internal method bodies while keeping signatures and docstrings.
        """
        lines = class_code.splitlines()
        pruned_lines = []
        in_method = False

        for line in lines:
            if re.match(r'^\s+def\s+[A-Za-z0-9_]+\s*\(', line):
                in_method = True
                pruned_lines.append(line)
                pruned_lines.append("        pass  # body pruned")
            elif in_method and re.match(r'^\s+[A-Za-z0-9_]', line):
                in_method = False
                pruned_lines.append(line)
            elif not in_method:
                pruned_lines.append(line)

        return "\n".join(pruned_lines)
