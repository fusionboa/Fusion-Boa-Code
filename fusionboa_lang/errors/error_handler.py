"""
FusionBoa Professional Error Handler

Provides clean, helpful error messages with source context, fix hints,
and error recovery — never a cryptic traceback.

Usage:
    from fusionboa_lang.errors.error_handler import (
        FusionBoaError, FusionBoaSyntaxError, format_error
    )
"""

import sys
from typing import List, Optional


# ---- Base Error Classes ----

class FusionBoaError(Exception):
    """Base class for all FusionBoa errors. Always includes line/col info."""

    def __init__(self, message: str, line: int = 0, col: int = 0,
                 severity: str = "error", hint: str = ""):
        self.message = message
        self.line = line
        self.col = col
        self.severity = severity
        self.hint = hint
        super().__init__(message)

    def __str__(self):
        return self.message


class FusionBoaSyntaxError(FusionBoaError):
    """Unified syntax error for lexer and parser issues."""
    pass


class FusionBoaCodegenError(FusionBoaError):
    """Error during code generation for a specific target."""
    pass


class FusionBoaRuntimeError(FusionBoaError):
    """Error during execution of generated code."""
    pass


# ---- Pretty-Printing (checks isatty() every time) ----

def _red(s: str) -> str:
    return f"\033[1;31m{s}\033[0m" if sys.stderr.isatty() else s

def _yellow(s: str) -> str:
    return f"\033[1;33m{s}\033[0m" if sys.stderr.isatty() else s

def _cyan(s: str) -> str:
    return f"\033[1;36m{s}\033[0m" if sys.stderr.isatty() else s

def _gray(s: str) -> str:
    return f"\033[2;37m{s}\033[0m" if sys.stderr.isatty() else s

def _bold(s: str) -> str:
    return f"\033[1m{s}\033[0m" if sys.stderr.isatty() else s


def format_error(error: FusionBoaError, source_lines: List[str] = None,
                 filename: str = "") -> str:
    """Format a single error with source context, pointer, and fix hint.

    Produces output like:

        error: Unexpected token 'whlie' at line 5, col 9
          --> demo.fusboa:5:9
            |
          5 |  whlie true:
            |         ^
            |
          = Did you mean 'while'?
    """
    lines = []
    severity = error.severity

    # Header
    prefix = _red("error") if severity == "error" else _yellow(severity)
    lines.append(f"{prefix}: {error.message}")

    # Location (file:line:col)
    loc = f"{filename}:" if filename else ""
    if error.line > 0:
        loc += f"{error.line}:{error.col}"
    else:
        loc += "?"
    lines.append(f"  {_cyan('-->')} {_gray(loc)}")

    # Source context
    if source_lines and 0 < error.line <= len(source_lines):
        lines.append(f"    {_gray('|')}")

        # Show the offending line
        source_line = source_lines[error.line - 1]
        line_num_str = str(error.line)
        padding = " " * (len(line_num_str) + 1)

        lines.append(f" {_bold(line_num_str)} {_gray('|')} {source_line}")

        # Pointer
        if error.col > 0:
            pointer = " " * error.col + _red("^")
            lines.append(f" {padding}{_gray('|')} {pointer}")

        lines.append(f"    {_gray('|')}")

    # Hint
    if error.hint:
        lines.append(f"  {_cyan('=')} {error.hint}")

    return "\n".join(lines)


# ---- Hint Generation ----

# Common misspellings of FusionBoa keywords with suggestions
_KEYWORD_HINTS = {
    "whlie": "while",
    "functoin": "function",
    "funtion": "function",
    "defiine": "define",
    "prnit": "print",
    "retrun": "return",
    "retturn": "return",
    "improt": "import",
    "exprot": "export",
    "clss": "class",
    "els": "else",
    "ele": "else",
    "excepot": "except",
    "catc": "catch",
    "finnaly": "finally",
    "flaot": "float",
    "interger": "integer",
    "boolen": "boolean",
    "stirng": "string",
    "lsit": "list",
}


def suggest_keyword(word: str) -> Optional[str]:
    """Suggest the correct keyword for a likely misspelling."""
    word_lower = word.lower().strip()
    if word_lower in _KEYWORD_HINTS:
        return f"Did you mean '{_KEYWORD_HINTS[word_lower]}'?"
    return None
