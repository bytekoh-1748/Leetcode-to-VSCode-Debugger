#!/usr/bin/env python3

import sys

MIN_PYTHON = (3, 9)


# @DontTrace
def ensure_supported_python() -> None:
    if sys.version_info < MIN_PYTHON:
        required = ".".join(str(part) for part in MIN_PYTHON)
        current = sys.version.split()[0]
        raise SystemExit(
            "LeetCode Debugger requires Python "
            f"{required} or newer. Current interpreter: {current}. "
            "Select a newer Python interpreter in VS Code and try again."
        )


# @DontTrace
def run() -> int:
    ensure_supported_python()
    from leetcode_debug_runtime import main

    return main()


if __name__ == "__main__":
    raise SystemExit(run())
