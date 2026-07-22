#!/usr/bin/env bash
# =============================================================================
# FusionBoa Language — macOS / Linux Installer
# =============================================================================
# Usage:  ./install.sh
#         (or: bash install.sh)
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo
echo "  ========================================"
echo "    FusionBoa Language - Unix Installer"
echo "  ========================================"
echo
echo "  Installing from: $SCRIPT_DIR"
echo

# --- Check Python ---
if ! command -v python3 &> /dev/null; then
    echo "  [X] Python 3 not found! Install from https://www.python.org/"
    exit 1
fi
PY_VER=$(python3 --version 2>&1)
echo "  [+] $PY_VER"

# --- Step 1: Install Python package and dependencies via pip ---
# Always run pip install — even if already installed, to pick up updates
echo "  [*] Installing Python package with dependencies..."
if python3 -m pip install -e "$SCRIPT_DIR" 2>&1; then
    echo "  [+] Package installed successfully."
else
    echo "  [*] pip install failed — trying to upgrade pip first..."
    python3 -m pip install --upgrade pip 2>&1 || true
    if python3 -m pip install -e "$SCRIPT_DIR" 2>&1; then
        echo "  [+] Package installed successfully (after pip upgrade)."
    else
        echo "  [~] pip install unavailable — continuing with PATH-only setup."
    fi
fi
echo

# --- Make fusionboa executable ---
chmod +x "$SCRIPT_DIR/fusionboa"

# --- Detect shell profile ---
SHELL_NAME=$(basename "${SHELL:-/bin/bash}")
case "$SHELL_NAME" in
    zsh)
        PROFILE="$HOME/.zshrc"
        ;;
    bash)
        # macOS bash uses .bash_profile, Linux uses .bashrc
        if [ -f "$HOME/.bash_profile" ]; then
            PROFILE="$HOME/.bash_profile"
        else
            PROFILE="$HOME/.bashrc"
        fi
        ;;
    *)
        PROFILE="$HOME/.profile"
        ;;
esac

EXPORT_LINE="export PATH=\"$SCRIPT_DIR:\$PATH\"  # FusionBoa Language"

# --- Check for duplicate (handle missing profile) ---
if [ -f "$PROFILE" ] && grep -qF "$SCRIPT_DIR" "$PROFILE" 2>/dev/null; then
    echo "  [~] Already in $PROFILE — nothing to do."
else
    echo "" >> "$PROFILE"
    echo "$EXPORT_LINE" >> "$PROFILE"
    echo "  [+] Added to $PROFILE"
fi

# --- Make it work in current session ---
export PATH="$SCRIPT_DIR:$PATH"

echo
echo "  [+] Installation complete!"
echo "  [!] Run: source $PROFILE   (or restart terminal)"
echo
echo "  Try it out:"
echo "      fusionboa version"
echo "      fusionboa help"
echo "      fusionboa run hello.fusboa"
echo
echo "  ========================================"
