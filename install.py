#!/usr/bin/env python3
"""
FusionBoa Language - Cross-Platform Installer
=============================================
Adds FusionBoa to your system PATH automatically.
Works on Windows (via registry, avoids setx truncation), macOS, and Linux.

Usage:
    python install.py
"""

import sys
import os
import platform
import subprocess
from pathlib import Path

FUSIONBOA_HOME = Path(__file__).parent.resolve()

BANNER = """
  ========================================
    FusionBoa Language - Installer
  ========================================"""


def check_python():
    """Verify Python version."""
    ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"  Python: {ver}  ({sys.executable})")
    if sys.version_info < (3, 8):
        print("  [X] FusionBoa requires Python 3.8+. Please upgrade.")
        sys.exit(1)
    print("  [+] Python OK")


def _check_path_contains(target: str) -> bool:
    """Check if target directory is already in PATH (exact match per entry)."""
    path_entries = os.environ.get("PATH", "").split(os.pathsep)
    return str(target) in path_entries


def _check_command_works() -> bool:
    """Check if 'fusionboa' command resolves from PATH."""
    try:
        result = subprocess.run(
            ["fusionboa", "version"],
            capture_output=True, text=True, timeout=5,
            shell=(platform.system() == "Windows"),
        )
        return "FusionBoa" in result.stdout
    except Exception:
        return False


def install_windows():
    """Add to user PATH on Windows via registry (safe, no truncation)."""
    print("  [*] Windows detected - writing to registry (HKCU\\Environment)...")

    try:
        import winreg

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, "Environment",
            0, winreg.KEY_READ | winreg.KEY_WRITE,
        )

        try:
            current, _ = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            current = ""

        entries = current.split(";") if current else []
        target = str(FUSIONBOA_HOME)

        if target in entries:
            print("  [~] Already in user PATH — nothing to do.")
            winreg.CloseKey(key)
            return True

        entries.append(target)
        new_path = ";".join(entries)

        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        winreg.CloseKey(key)

        # Broadcast the environment change so new terminals see it
        try:
            import ctypes
            ctypes.windll.user32.SendMessageTimeoutW(
                0xFFFF, 0x001A, 0, "Environment", 0x0002, 5000, None,
            )
        except Exception:
            pass  # broadcast is best-effort

        print("  [+] User PATH updated via registry (no truncation risk).")
        return True

    except PermissionError:
        print("  [X] Permission denied. Run as Administrator or use:")
        print(f"      setx PATH \"%PATH%;{FUSIONBOA_HOME}\"")
        return False
    except Exception as e:
        print(f"  [X] Error: {e}")
        print(f"  [!] Fallback: setx PATH \"%PATH%;{FUSIONBOA_HOME}\"")
        return False


def install_unix():
    """Add to PATH on macOS/Linux via shell profile (deduped)."""
    print("  [*] Unix detected - updating shell profile...")

    home = Path.home()
    shell = os.environ.get("SHELL", "/bin/bash")

    if "zsh" in shell:
        profile = home / ".zshrc"
    elif "bash" in shell:
        profile = home / ".bashrc"
        # macOS bash reads .bash_profile first if it exists
        bash_profile = home / ".bash_profile"
        if bash_profile.exists():
            profile = bash_profile
    else:
        profile = home / ".profile"

    export_line = f'export PATH="{FUSIONBOA_HOME}:$PATH"  # FusionBoa Language'

    # Read existing content and check for duplicates
    existing = ""
    if profile.exists():
        existing = profile.read_text()

    if str(FUSIONBOA_HOME) in existing:
        print(f"  [~] Already in {profile} — nothing to do.")
        return True

    # Append with a leading newline for separation
    with open(profile, "a") as f:
        f.write(f"\n{export_line}\n")

    print(f"  [+] Added to {profile}")
    print(f"  [+] Run: source {profile}")
    return True


def verify_installation():
    """Verify fusionboa works from this session."""
    print()
    print("  [*] Verifying...")
    try:
        result = subprocess.run(
            [sys.executable, str(FUSIONBOA_HOME / "fusionboa.py"), "version"],
            capture_output=True, text=True, timeout=10,
        )
        if "FusionBoa" in result.stdout:
            print(f"  [+] {result.stdout.strip()}")
        else:
            print(f"  [!] Unexpected: {result.stdout.strip()}")
    except Exception as e:
        print(f"  [!] {e}")


def main():
    print(BANNER)
    print(f"\n  Installing from: {FUSIONBOA_HOME}\n")

    check_python()

    if _check_command_works():
        print("  [~] 'fusionboa' command already works from PATH!")
        print()
        print("  FusionBoa is already installed and ready.")
        verify_installation()
        return

    if _check_path_contains(str(FUSIONBOA_HOME)):
        print("  [~] FusionBoa directory is in PATH but command not found.")
        print("  [~] Try restarting your terminal.")
        verify_installation()
        return

    system = platform.system()
    if system == "Windows":
        success = install_windows()
    else:
        success = install_unix()

    print()
    if success:
        print("  [+] Installation complete!")
        print("  [!] RESTART your terminal for PATH changes to take effect.")
        print()
        print("  Try it out:")
        print("      fusionboa version")
        print("      fusionboa help")
        print("      fusionboa run hello.fusboa")
    else:
        print("  [!] Manual installation required.")
        print(f"  [!] Add this directory to your PATH: {FUSIONBOA_HOME}")

    verify_installation()
    print()
    print("  ========================================")


if __name__ == "__main__":
    main()
