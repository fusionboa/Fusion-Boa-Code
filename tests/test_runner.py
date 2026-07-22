#!/usr/bin/env python3
"""
FusionBoa Local Test Runner
============================
Runs all .fusboa example files against the Python target and reports results.
Works on Windows, macOS, and Linux.

Usage:
    python tests/test_runner.py          # Run all examples
    python tests/test_runner.py -v       # Verbose (show generated code)
    python tests/test_runner.py -t py    # Test specific target (default: py)
"""

import sys
import os
import subprocess
import time
from pathlib import Path

# Ensure we run from the project root
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
os.chdir(PROJECT_ROOT)

EXAMPLES_DIR = PROJECT_ROOT / "fusionboa_lang" / "examples"
FUSIONBOA_PY = PROJECT_ROOT / "fusionboa.py"

# ANSI colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def find_examples() -> list[Path]:
    """Find all .fusboa example files."""
    return sorted(EXAMPLES_DIR.glob("*.fusboa"))


def run_test(example: Path, target: str, verbose: bool) -> dict:
    """Run a single .fusboa file through fusionboa."""
    result = {
        "file": example.name,
        "target": target,
        "status": "SKIP",
        "output": "",
        "error": "",
        "duration_ms": 0,
    }

    start = time.perf_counter()

    try:
        proc = subprocess.run(
            [sys.executable, str(FUSIONBOA_PY), "run", str(example), "-t", target],
            capture_output=True,
            text=True,
            timeout=30,
        )

        result["duration_ms"] = (time.perf_counter() - start) * 1000

        if proc.returncode == 0:
            result["status"] = "PASS"
            result["output"] = proc.stdout.strip()
        else:
            result["status"] = "FAIL"
            result["error"] = proc.stderr.strip() or proc.stdout.strip()

    except subprocess.TimeoutExpired:
        result["status"] = "FAIL"
        result["error"] = "Timeout (30s)"
        result["duration_ms"] = 30000
    except Exception as e:
        result["status"] = "FAIL"
        result["error"] = str(e)

    return result


def main():
    import argparse

    parser = argparse.ArgumentParser(description="FusionBoa Local Test Runner")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-t", "--target", default="py", help="Target language (default: py)")
    args = parser.parse_args()

    examples = find_examples()

    if not examples:
        print(f"{RED}No .fusboa files found in {EXAMPLES_DIR}{RESET}")
        sys.exit(1)

    print(f"\n{BOLD}{CYAN}{'='*50}{RESET}")
    print(f"{BOLD}{CYAN}  FusionBoa Test Runner — Target: {args.target:<12}{RESET}")
    print(f"{BOLD}{CYAN}{'='*50}{RESET}")
    print(f"\n  Found {len(examples)} example(s) in {EXAMPLES_DIR}\n")

    results = []
    for example in examples:
        result = run_test(example, args.target, args.verbose)
        results.append(result)

        status_color = GREEN if result["status"] == "PASS" else RED if result["status"] == "FAIL" else YELLOW
        status_mark = "+" if result["status"] == "PASS" else "-" if result["status"] == "FAIL" else "?"
        time_str = f"{result['duration_ms']:.0f}ms"

        print(f"  {status_color}{status_mark}{RESET} {example.name:<35} {status_color}{result['status']:<5}{RESET} {time_str}")

        if result["status"] == "PASS" and args.verbose:
            print(f"      {YELLOW}{result['output']}{RESET}")
        elif result["status"] == "FAIL":
            print(f"      {RED}{result['error'][:120]}{RESET}")

    # Summary
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    skipped = sum(1 for r in results if r["status"] == "SKIP")
    total = len(results)

    print(f"\n  {BOLD}Summary:{RESET}")
    print(f"  {GREEN}Passed:{RESET}  {passed}/{total}")
    if failed:
        print(f"  {RED}Failed:{RESET}  {failed}/{total}")
    if skipped:
        print(f"  {YELLOW}Skipped:{RESET} {skipped}/{total}")

    total_time = sum(r["duration_ms"] for r in results)
    print(f"  Time:     {total_time:.0f}ms total\n")

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
