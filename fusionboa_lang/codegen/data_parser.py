"""
Fusion Data Value Parser

A dedicated mini-parser for FusionBoa-style dict/list literals.
Unlike the main Fusion parser, this treats all unquoted words as
strings (not keywords), handles multi-line indented blocks, and
nested structures.

This is used by the JSON, YAML, and TOML code generators.

Grammar:
    value     := dict | list | string | number | boolean | null
    dict      := '{' (pair (',' pair)*)? '}'
    pair      := value ':' value
    list      := '[' (value (',' value)*)? ']'
    string    := '"' ... '"' | "'" ... "'" | identifier
    number    := integer | float
    boolean   := 'true' | 'false'
    null      := 'null' | 'none' | 'nothing'
"""

import re
from typing import List, Tuple, Optional, Any


class DataParseError(Exception):
    pass


class DataTokenizer:
    """Tokenizes FusionBoa-style data (dicts, lists, literals)."""

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1

    def _current(self) -> str:
        if self.pos < len(self.source):
            return self.source[self.pos]
        return ''

    def _peek(self, n: int = 1) -> str:
        idx = self.pos + n
        if idx < len(self.source):
            return self.source[idx]
        return ''

    def _advance(self) -> str:
        ch = self._current()
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        self.pos += 1
        return ch

    def _skip_whitespace(self):
        while self._current() in (' ', '\t', '\n', '\r'):
            self._advance()

    def _skip_comment(self):
        while self._current() and self._current() != '\n':
            self._advance()

    def tokenize(self) -> List[Tuple[str, Any, int, int]]:
        """Return list of (type, value, line, col) tokens."""
        tokens = []
        while self.pos < len(self.source):
            ch = self._current()

            # Skip whitespace
            if ch in (' ', '\t', '\n', '\r'):
                self._skip_whitespace()
                continue

            # Skip # comments
            if ch == '#':
                self._skip_comment()
                continue

            # Single-char tokens
            if ch == '{':
                tokens.append(('LBRACE', ch, self.line, self.col))
                self._advance()
                continue
            if ch == '}':
                tokens.append(('RBRACE', ch, self.line, self.col))
                self._advance()
                continue
            if ch == '[':
                tokens.append(('LBRACKET', ch, self.line, self.col))
                self._advance()
                continue
            if ch == ']':
                tokens.append(('RBRACKET', ch, self.line, self.col))
                self._advance()
                continue
            if ch == ':':
                tokens.append(('COLON', ch, self.line, self.col))
                self._advance()
                continue
            if ch == ',':
                tokens.append(('COMMA', ch, self.line, self.col))
                self._advance()
                continue

            # Strings
            if ch in ('"', "'"):
                quote = ch
                start_line, start_col = self.line, self.col
                self._advance()  # skip opening quote
                chars = []
                while self._current() and self._current() != quote:
                    if self._current() == '\\':
                        self._advance()
                        esc = self._advance()
                        escape_map = {'n': '\n', 't': '\t', '\\': '\\', '"': '"', "'": "'", 'r': '\r'}
                        chars.append(escape_map.get(esc, esc))
                    else:
                        chars.append(self._advance())
                if self._current() == quote:
                    self._advance()  # skip closing quote
                tokens.append(('STRING', ''.join(chars), start_line, start_col))
                continue

            # Numbers
            if ch.isdigit() or (ch == '-' and self._peek().isdigit()):
                start_line, start_col = self.line, self.col
                chars = []
                is_float = False
                if ch == '-':
                    chars.append(self._advance())
                while self._current() and (self._current().isdigit() or self._current() == '.'):
                    if self._current() == '.':
                        if is_float:
                            break
                        is_float = True
                    chars.append(self._advance())
                val = ''.join(chars)
                tokens.append(('NUMBER', float(val) if is_float else int(val), start_line, start_col))
                continue

            # Identifiers, booleans, null
            if ch.isalpha() or ch == '_':
                start_line, start_col = self.line, self.col
                chars = []
                while self._current() and (self._current().isalnum() or self._current() == '_'):
                    chars.append(self._advance())
                word = ''.join(chars)
                if word.lower() in ('true', 'yes'):
                    tokens.append(('BOOLEAN', True, start_line, start_col))
                elif word.lower() in ('false', 'no'):
                    tokens.append(('BOOLEAN', False, start_line, start_col))
                elif word.lower() in ('null', 'none', 'nothing'):
                    tokens.append(('NULL', None, start_line, start_col))
                else:
                    tokens.append(('IDENTIFIER', word, start_line, start_col))
                continue

            raise DataParseError(f"Unexpected character '{ch}' at line {self.line}, col {self.col}")

        tokens.append(('EOF', None, self.line, self.col))
        return tokens


class DataParser:
    """Parses FusionBoa-style data values into Python objects."""

    def __init__(self, tokens: List[Tuple[str, Any, int, int]]):
        self.tokens = tokens
        self.pos = 0

    def _current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', None, 0, 0)

    def _advance(self):
        tok = self._current()
        self.pos += 1
        return tok

    def _check(self, token_type: str) -> bool:
        return self._current()[0] == token_type

    def _consume(self, token_type: str, error_msg: str = None):
        tok = self._current()
        if tok[0] != token_type:
            if error_msg is None:
                error_msg = f"Expected {token_type}, got {tok[0]} ('{tok[1]}') at line {tok[2]}:{tok[3]}"
            raise DataParseError(error_msg)
        return self._advance()

    def parse(self) -> Any:
        """Parse the full source into a Python value."""
        val = self._parse_value()
        # Skip trailing junk (comments were already stripped, so this is fine)
        return val

    def _parse_value(self) -> Any:
        """Parse a single value."""
        tok = self._current()
        
        if tok[0] == 'LBRACE':
            return self._parse_dict()
        if tok[0] == 'LBRACKET':
            return self._parse_list()
        if tok[0] == 'STRING':
            self._advance()
            return tok[1]
        if tok[0] == 'NUMBER':
            self._advance()
            return tok[1]
        if tok[0] == 'BOOLEAN':
            self._advance()
            return tok[1]
        if tok[0] == 'NULL':
            self._advance()
            return None
        if tok[0] == 'IDENTIFIER':
            self._advance()
            return tok[1]  # Returns the string value
        if tok[0] == 'EOF':
            return None
        
        raise DataParseError(f"Unexpected token {tok[0]} ('{tok[1]}') at line {tok[2]}:{tok[3]}")

    def _parse_dict(self) -> dict:
        """Parse a dict literal: {key: value, ...}"""
        self._consume('LBRACE')
        result = {}
        
        if self._check('RBRACE'):
            self._advance()
            return result
        
        while True:
            key = self._parse_value()
            self._consume('COLON', f"Expected ':' after dict key, got {self._current()[0]}")
            val = self._parse_value()
            result[str(key)] = val
            
            if self._check('COMMA'):
                self._advance()
                continue
            if self._check('RBRACE'):
                self._advance()
                return result
            
            # If we hit EOF without closing brace, that's an error
            if self._check('EOF'):
                raise DataParseError("Unclosed dict: expected '}'")
        
        # Fallback for safety (shouldn't reach here)
        return result

    def _parse_list(self) -> list:
        """Parse a list literal: [value, ...]"""
        self._consume('LBRACKET')
        result = []
        
        if self._check('RBRACKET'):
            self._advance()
            return result
        
        while True:
            result.append(self._parse_value())
            
            if self._check('COMMA'):
                self._advance()
                continue
            if self._check('RBRACKET'):
                self._advance()
                return result
            
            # Allow missing comma before closing bracket
            if self._check('RBRACKET'):
                self._advance()
                return result
            
            # Allow newline-separated values without commas
            if self._current()[0] in ('STRING', 'NUMBER', 'BOOLEAN', 'NULL', 'IDENTIFIER', 'LBRACE', 'LBRACKET'):
                continue
            
            if self._check('EOF'):
                raise DataParseError("Unclosed list: expected ']'")
            
            raise DataParseError(f"Unexpected token in list: {self._current()[0]} at line {self._current()[2]}:{self._current()[3]}")
        
        # Fallback
        return result


def parse_data(source: str) -> Any:
    """Parse a FusionBoa-style data value from source.
    
    Handles dicts, lists, strings, numbers, booleans, and null.
    All unquoted identifiers become strings.
    Supports multi-line with FusionBoa-style # comments.
    """
    tokenizer = DataTokenizer(source)
    tokens = tokenizer.tokenize()
    parser = DataParser(tokens)
    return parser.parse()
