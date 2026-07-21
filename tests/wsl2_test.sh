#!/usr/bin/env bash
# =============================================================================
# FusionBoa — WSL2 Test Setup (Linux from Windows 11)
# =============================================================================
# Run this inside WSL2 to test FusionBoa on Linux without leaving Windows.
#
# Prerequisites (one-time, in PowerShell as Admin):
#   wsl --install -d Ubuntu
#
# Usage (inside WSL2 terminal):
#   cd /mnt/c/FusionBoa
#   bash tests/wsl2_test.sh
# =============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[92m"
RED="\033[91m"
YELLOW="\033[93m"
CYAN="\033[96m"
RESET="\033[0m"

echo -e "\n${BOLD}${CYAN}==================================================${RESET}"
echo -e "${BOLD}${CYAN}  FusionBoa — WSL2 Linux Test Suite${RESET}"
echo -e "${BOLD}${CYAN}==================================================${RESET}"

# --- Detect if we're in WSL ---
if ! grep -qi microsoft /proc/version 2>/dev/null; then
    echo -e "\n${YELLOW}[!] Not running inside WSL2. This script is meant for WSL2 on Windows.${RESET}"
    echo -e "    For native Linux: just run 'python fusionboa.py version' directly.\n"
fi

# --- Check Python ---
echo -e "\n${BOLD}[1/4] Checking Python...${RESET}"
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo -e "${RED}[X] Python 3 not found! Install with: sudo apt install python3${RESET}"
    exit 1
fi

PY_VER=$($PYTHON --version 2>&1)
echo -e "${GREEN}[+] $PY_VER${RESET}"

# --- Check FusionBoa ---
echo -e "\n${BOLD}[2/4] Checking FusionBoa...${RESET}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

if [ ! -f "$PROJECT_DIR/fusionboa.py" ]; then
    echo -e "${RED}[X] fusionboa.py not found! Run this from the FusionBoa project directory.${RESET}"
    exit 1
fi

echo -e "${GREEN}[+] Project found at: $PROJECT_DIR${RESET}"

# --- Run FusionBoa Version ---
echo -e "\n${BOLD}[3/4] Running version check...${RESET}"
$PYTHON "$PROJECT_DIR/fusionboa.py" version

# --- Run Test Suite ---
echo -e "\n${BOLD}[4/4] Running test suite...${RESET}"

PASS=0
FAIL=0
TOTAL=0

# Tests that just compile (no external runtime needed)
# These use 'build' mode to verify code generation succeeds
COMPILE_TESTS=(
    "hello.fusboa:go"
    "hello.fusboa:rs"
    "hello.fusboa:cpp"
    "hello.fusboa:swift"
    "hello.fusboa:kt"
    "hello.fusboa:java"
    "hello.fusboa:jl"
    "hello.fusboa:r"
    "hello.fusboa:cs"
    "hello.fusboa:lua"
    "hello.fusboa:ts"
)

# Tests that compile AND run (runtime available on most systems)
declare -a RUN_TESTS=(
    "hello.fusboa:py"
    "hello.fusboa:js"
    "hello.fusboa:rb"
    "app.fusboa:py"
    "app.fusboa:js"
)

# --- Compile-only tests (verify code generation works) ---
echo -e "\n${BOLD}Compile-only tests (no runtime needed):${RESET}"
for test in "${COMPILE_TESTS[@]}"; do
    IFS=':' read -r file target <<< "$test"
    TOTAL=$((TOTAL + 1))
    example_path="$PROJECT_DIR/fusionboa_lang/examples/$file"

    if $PYTHON "$PROJECT_DIR/fusionboa.py" build "$example_path" -t "$target" &>/dev/null; then
        echo -e "  ${GREEN}+${RESET} $file → $target"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}-${RESET} $file → $target"
        FAIL=$((FAIL + 1))
    fi
done

# --- Run tests (compile + execute) ---
echo -e "\n${BOLD}Run tests (compile + execute):${RESET}"
for test in "${RUN_TESTS[@]}"; do
    IFS=':' read -r file target <<< "$test"
    TOTAL=$((TOTAL + 1))
    example_path="$PROJECT_DIR/fusionboa_lang/examples/$file"

    if $PYTHON "$PROJECT_DIR/fusionboa.py" run "$example_path" -t "$target" &>/dev/null; then
        echo -e "  ${GREEN}+${RESET} $file → $target"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}-${RESET} $file → $target"
        FAIL=$((FAIL + 1))
    fi
done

# --- Multi-target build test ---
echo -e "\n${BOLD}Multi-target build test:${RESET}"
TOTAL=$((TOTAL + 1))
if $PYTHON "$PROJECT_DIR/fusionboa.py" build "$PROJECT_DIR/fusionboa_lang/examples/app.fusboa" --targets py,js,html,json &>/dev/null; then
    echo -e "  ${GREEN}✓${RESET} app.fusboa → py,js,html,json"
    PASS=$((PASS + 1))
else
    echo -e "  ${RED}✗${RESET} app.fusboa multi-target build"
    FAIL=$((FAIL + 1))
fi

# --- Summary ---
echo -e "\n${BOLD}═══════════════════════════════════════${RESET}"
echo -e "${BOLD}  Results:${RESET}"
echo -e "  ${GREEN}Passed: $PASS/$TOTAL${RESET}"
if [ $FAIL -gt 0 ]; then
    echo -e "  ${RED}Failed: $FAIL/$TOTAL${RESET}"
fi
echo -e "${BOLD}═══════════════════════════════════════${RESET}\n"

exit $FAIL
