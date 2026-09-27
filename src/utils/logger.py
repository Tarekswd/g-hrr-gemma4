"""
Logging and console reporting utilities.
"""
import sys
import time

class ExperimentLogger:
    @staticmethod
    def log(msg: str) -> None:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {msg}", flush=True)

    @staticmethod
    def error(msg: str) -> None:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [ERROR] {msg}", file=sys.stderr, flush=True)
