"""
FusionBoa Language Lexer (Tokenizer)

Converts FusionBoa source code into a stream of tokens.
Handles English-like keywords, indentation-based blocks, multi-word operators,
string interpolation, spread operator, and all FusionBoa syntax.
"""

import re
from typing import List
from .tokens import Token, TokenType, KEYWORDS


class LexerError(Exception):
    """Error raised when the lexer encounters invalid input."""

    def __init__(self, message: str, line: int, col: int):
        super().__init__(f"Lexer error at line {line}, col {col}: {message}")
        self.line = line
        self.col = col


class Lexer:
    """Tokenizes FusionBoa source code."""

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: List[Token] = []
        self.indent_stack = [0]

    def _current(self) -> str:
        if self.pos < len(self.source):
            return self.source[self.pos]
        return ""

    def _peek(self, n: int = 1) -> str:
        if self.pos + n < len(self.source):
            return self.source[self.pos + n]
        return ""

    def _advance(self) -> str:
        ch = self._current()
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        self.pos += 1
        return ch

    def _skip_whitespace_on_line(self):
        while self._current() in (" ", "\t"):
            self._advance()

    def _skip_comment(self):
        while self._current() and self._current() != "\n":
            self._advance()

    def _read_identifier_or_keyword(self) -> Token:
        start_line = self.line
        start_col = self.col
        chars = []

        while self._current() and (self._current().isalnum() or self._current() == "_"):
            chars.append(self._advance())

        first_word = "".join(chars)

        if first_word not in KEYWORDS:
            has_multi = any(k.startswith(first_word + " ") for k in KEYWORDS if " " in k)
            if not has_multi:
                return Token(TokenType.IDENTIFIER, first_word, start_line, start_col)

        saved_pos = self.pos
        saved_line = self.line
        saved_col = self.col
        words = [first_word]
        current_phrase = first_word

        while True:
            if self._current() != " ":
                break
            pre_space_pos = self.pos
            pre_space_line = self.line
            pre_space_col = self.col
            while self._current() == " ":
                self._advance()
            next_chars = []
            while self._current() and (self._current().isalnum() or self._current() == "_"):
                next_chars.append(self._advance())
            if not next_chars:
                self.pos = pre_space_pos
                self.line = pre_space_line
                self.col = pre_space_col
                break
            next_word = "".join(next_chars)
            candidate = current_phrase + " " + next_word
            if candidate in KEYWORDS:
                words.append(next_word)
                current_phrase = candidate
                continue
            is_prefix = any(k.startswith(candidate + " ") for k in KEYWORDS if " " in k)
            if is_prefix:
                words.append(next_word)
                current_phrase = candidate
                continue
            self.pos = pre_space_pos
            self.line = pre_space_line
            self.col = pre_space_col
            break

        if current_phrase in KEYWORDS:
            token_type = KEYWORDS[current_phrase]
            value_map = {"true": True, "false": False, "yes": True, "no": False,
                         "null": None, "none": None, "nothing": None}
            if current_phrase in value_map:
                return Token(token_type, value_map[current_phrase], start_line, start_col)
            return Token(token_type, current_phrase, start_line, start_col)

        for i in range(len(words) - 1, 0, -1):
            shorter = " ".join(words[:i])
            if shorter in KEYWORDS:
                full_text = " ".join(words)
                shorter_text = shorter
                chars_to_unread = len(full_text) - len(shorter_text)
                self.pos -= chars_to_unread
                token_type = KEYWORDS[shorter]
                return Token(token_type, shorter, start_line, start_col)

        self.pos = saved_pos
        self.line = saved_line
        self.col = saved_col

        if first_word in KEYWORDS:
            token_type = KEYWORDS[first_word]
            value_map = {"true": True, "false": False, "yes": True, "no": False,
                         "null": None, "none": None, "nothing": None}
            if first_word in value_map:
                return Token(token_type, value_map[first_word], start_line, start_col)
            return Token(token_type, first_word, start_line, start_col)

        return Token(TokenType.IDENTIFIER, first_word, start_line, start_col)

    def _read_number(self) -> Token:
        start_line = self.line
        start_col = self.col
        chars = []
        is_float = False
        while self._current() and (self._current().isdigit() or self._current() == "."):
            if self._current() == ".":
                if is_float:
                    break
                is_float = True
            chars.append(self._advance())
        value = "".join(chars)
        if is_float:
            return Token(TokenType.FLOAT, float(value), start_line, start_col)
        return Token(TokenType.INTEGER, int(value), start_line, start_col)

    def _read_string(self, quote: str) -> Token:
        """Read a string literal. Detects {expr} interpolation and triple-quote multi-line strings."""
        start_line = self.line
        start_col = self.col

        # Check for triple-quote multi-line string
        if self._peek() == quote and self._peek(2) == quote:
            return self._read_triple_quoted_string(quote)

        self._advance()  # skip opening quote

        # First pass: check if string has interpolation
        saved_pos = self.pos
        saved_line = self.line
        saved_col = self.col
        has_interp = False
        while self._current() and self._current() != quote:
            if self._current() == "\\":
                self._advance()
                if self._current():
                    self._advance()
            elif self._current() == "{":
                nxt = self._peek()
                if nxt.isalnum() or nxt in ('_', '(', '"', "'", '!', '-', '+'):
                    has_interp = True
                    break
                else:
                    self._advance()
            else:
                self._advance()

        # Reset and read properly
        self.pos = saved_pos
        self.line = saved_line
        self.col = saved_col

        if has_interp:
            # Read raw string content with {expr} markers intact
            raw_parts = []
            brace_depth = 0
            while self._current() and not (self._current() == quote and brace_depth == 0):
                if self._current() == "{":
                    brace_depth += 1
                elif self._current() == "}":
                    brace_depth -= 1
                elif self._current() == "\\":
                    self._advance()
                    if self._current():
                        raw_parts.append(self._advance())
                    continue
                raw_parts.append(self._advance())
            if self._current() == quote:
                self._advance()
            return Token(TokenType.INTERP_STRING, "".join(raw_parts), start_line, start_col)
        else:
            # Plain string
            chars = []
            while self._current() and self._current() != quote:
                if self._current() == "\\":
                    self._advance()
                    escaped = self._advance()
                    escape_map = {"n": "\n", "t": "\t", "\\": "\\", '"': '"', "'": "'"}
                    chars.append(escape_map.get(escaped, escaped))
                else:
                    chars.append(self._advance())
            if self._current() == quote:
                self._advance()
            else:
                raise LexerError("Unterminated string", start_line, start_col)
            return Token(TokenType.STRING, "".join(chars), start_line, start_col)

    def _read_triple_quoted_string(self, quote: str) -> Token:
        """Read a triple-quoted multi-line string (three double/single quotes)."""
        start_line = self.line
        start_col = self.col
        # Skip all three opening quotes
        self._advance()  # skip first
        self._advance()  # skip second
        self._advance()  # skip third

        chars = []
        # Skip leading newline if present
        if self._current() == "\n":
            self._advance()

        while True:
            ch = self._current()
            if not ch:
                raise LexerError("Unterminated triple-quoted string", start_line, start_col)
            if ch == quote and self._peek() == quote and self._peek(2) == quote:
                self._advance()  # skip first
                self._advance()  # skip second
                self._advance()  # skip third
                break
            if ch == "\\":
                self._advance()
                next_ch = self._current()
                if next_ch == "n":
                    chars.append("\n")
                elif next_ch == "t":
                    chars.append("\t")
                elif next_ch == "\\":
                    chars.append("\\")
                elif next_ch == quote:
                    chars.append(quote)
                else:
                    chars.append("\\" + next_ch if next_ch else "\\")
                if next_ch:
                    self._advance()
            else:
                chars.append(self._advance())

        return Token(TokenType.STRING, "".join(chars), start_line, start_col)

    def _handle_indentation(self, indent_level: int):
        current_indent = self.indent_stack[-1]
        if indent_level > current_indent:
            self.tokens.append(Token(TokenType.INDENT, "", self.line, self.col))
            self.indent_stack.append(indent_level)
        elif indent_level < current_indent:
            while indent_level < self.indent_stack[-1]:
                self.tokens.append(Token(TokenType.DEDENT, "", self.line, self.col))
                self.indent_stack.pop()

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            ch = self._current()

            if ch in (" ", "\t"):
                self._advance()
                continue

            if ch == "\n":
                line = self.line
                self._advance()
                self.tokens.append(Token(TokenType.NEWLINE, "\n", line, self.col))
                # Peek past whitespace to check if next line has content
                saved_pos, saved_line, saved_col = self.pos, self.line, self.col
                indent = 0
                while self._current() in (" ", "\t"):
                    indent += 1 if self._current() == " " else 4
                    self._advance()
                if self._current() in ("\n", "#", ""):
                    # Blank line, comment-only line, or EOF - skip silently
                    self.pos, self.line, self.col = saved_pos, saved_line, saved_col
                    continue
                # Restore and use measured indentation (single pass)
                self.pos, self.line, self.col = saved_pos, saved_line, saved_col
                while self._current() in (" ", "\t"):
                    self._advance()  # advance past already-measured whitespace
                self._handle_indentation(indent)
                continue

            if ch == "#":
                self._skip_comment()
                continue

            if ch in ('"', "'"):
                if self._peek() == ch and self._peek(2) == ch:
                    self.tokens.append(self._read_string(ch))
                else:
                    self.tokens.append(self._read_string(ch))
                continue

            if ch.isdigit():
                self.tokens.append(self._read_number())
                continue

            if ch.isalpha() or ch == "_":
                self.tokens.append(self._read_identifier_or_keyword())
                continue

            # Multi-char operators
            if ch == "=":
                start_line, start_col = self.line, self.col
                self._advance()
                if self._current() == "=":
                    self._advance()
                    self.tokens.append(Token(TokenType.EQUAL_EQUAL, "==", start_line, start_col))
                elif self._current() == ">":
                    self._advance()
                    self.tokens.append(Token(TokenType.FAT_ARROW, "=>", start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.EQUAL, "=", start_line, start_col))
                continue

            if ch == "!":
                start_line, start_col = self.line, self.col
                self._advance()
                if self._current() == "=":
                    self._advance()
                    self.tokens.append(Token(TokenType.BANG_EQUAL, "!=", start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.NOT, "!", start_line, start_col))
                continue

            if ch == "<":
                start_line, start_col = self.line, self.col
                self._advance()
                if self._current() == "=":
                    self._advance()
                    self.tokens.append(Token(TokenType.LESS_EQUAL, "<=", start_line, start_col))
                elif self._current() == "<":
                    self._advance()
                    self.tokens.append(Token(TokenType.LESS_LESS, "<<", start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.LESS, "<", start_line, start_col))
                continue

            if ch == ">":
                start_line, start_col = self.line, self.col
                self._advance()
                if self._current() == "=":
                    self._advance()
                    self.tokens.append(Token(TokenType.GREATER_EQUAL, ">=", start_line, start_col))
                elif self._current() == ">":
                    self._advance()
                    self.tokens.append(Token(TokenType.GREATER_GREATER, ">>", start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.GREATER, ">", start_line, start_col))
                continue

            if ch == "+":
                start_line, start_col = self.line, self.col
                self._advance()
                if self._current() == "+":
                    self._advance()
                    self.tokens.append(Token(TokenType.PLUS_PLUS, "++", start_line, start_col))
                elif self._current() == "=":
                    self._advance()
                    self.tokens.append(Token(TokenType.PLUS_EQUAL, "+=", start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.PLUS, "+", start_line, start_col))
                continue

            if ch == "-":
                start_line, start_col = self.line, self.col
                self._advance()
                if self._current() == "-":
                    self._advance()
                    self.tokens.append(Token(TokenType.MINUS_MINUS, "--", start_line, start_col))
                elif self._current() == ">":
                    self._advance()
                    self.tokens.append(Token(TokenType.ARROW, "->", start_line, start_col))
                elif self._current() == "=":
                    self._advance()
                    self.tokens.append(Token(TokenType.MINUS_EQUAL, "-=", start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.MINUS, "-", start_line, start_col))
                continue

            if ch == "*":
                start_line, start_col = self.line, self.col
                self._advance()
                if self._current() == "=":
                    self._advance()
                    self.tokens.append(Token(TokenType.STAR_EQUAL, "*=", start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.STAR, "*", start_line, start_col))
                continue

            if ch == "/":
                start_line, start_col = self.line, self.col
                self._advance()
                if self._current() == "/":
                    # // is always a comment (use 'div' for floor division)
                    while self._current() and self._current() != "\n":
                        self._advance()
                    # Comment ends before newline; the main loop handles the newline
                    continue
                elif self._current() == "=":
                    self._advance()
                    self.tokens.append(Token(TokenType.SLASH_EQUAL, "/=", start_line, start_col))
                    continue
                # Regex literal detection: / is only division if preceded by an operand
                if self._is_division_context():
                    self.tokens.append(Token(TokenType.SLASH, "/", start_line, start_col))
                    continue
                else:
                    # Try to parse as regex literal /pattern/flags
                    regex_token = self._read_regex_literal(start_line, start_col)
                    if regex_token:
                        self.tokens.append(regex_token)
                        continue
                    else:
                        self.tokens.append(Token(TokenType.SLASH, "/", start_line, start_col))
                        continue

            if ch == "?":
                start_line, start_col = self.line, self.col
                self._advance()
                if self._current() == "?":
                    self._advance()
                    if self._current() == "=":
                        self._advance()
                        self.tokens.append(Token(TokenType.QUESTION_QUESTION_EQUAL, "??=", start_line, start_col))
                    else:
                        self.tokens.append(Token(TokenType.QUESTION_QUESTION, "??", start_line, start_col))
                elif self._current() == ".":
                    self._advance()
                    self.tokens.append(Token(TokenType.QUESTION_DOT, "?.", start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.QUESTION, "?", start_line, start_col))
                continue

            if ch == "&":
                start_line, start_col = self.line, self.col
                self._advance()
                if self._current() == "&":
                    self._advance()
                    if self._current() == "=":
                        self._advance()
                        self.tokens.append(Token(TokenType.AMPERSAND_AMPERSAND_EQUAL, "&&=", start_line, start_col))
                    else:
                        self.tokens.append(Token(TokenType.AMPERSAND_AMPERSAND, "&&", start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.AMPERSAND, "&", start_line, start_col))
                continue

            if ch == "@":
                start_line, start_col = self.line, self.col
                self._advance()
                self.tokens.append(Token(TokenType.AT_SIGN, "@", start_line, start_col))
                continue

            if ch == "~":
                start_line, start_col = self.line, self.col
                self._advance()
                self.tokens.append(Token(TokenType.TILDE, "~", start_line, start_col))
                continue

            if ch == "|":
                start_line, start_col = self.line, self.col
                self._advance()
                if self._current() == ">":
                    self._advance()
                    self.tokens.append(Token(TokenType.PIPE_OP, "|>", start_line, start_col))
                elif self._current() == "|":
                    self._advance()
                    if self._current() == "=":
                        self._advance()
                        self.tokens.append(Token(TokenType.PIPE_PIPE_EQUAL, "||=", start_line, start_col))
                    else:
                        self.tokens.append(Token(TokenType.PIPE_PIPE, "||", start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.PIPE, "|", start_line, start_col))
                continue

            # ... spread operator
            if ch == ".":
                start_line, start_col = self.line, self.col
                if self._peek() == "." and self._peek(2) == ".":
                    self._advance()
                    self._advance()
                    self._advance()
                    self.tokens.append(Token(TokenType.DOT_DOT_DOT, "...", start_line, start_col))
                else:
                    self._advance()
                    self.tokens.append(Token(TokenType.DOT, ".", start_line, start_col))
                continue

            if ch == "`":
                # Backtick - used in markdown/template literals, treat as identifier char
                self._advance()
                continue

            # Single-char operators
            single_char_map = {
                "%": TokenType.PERCENT, "^": TokenType.CARET,
                ",": TokenType.COMMA, ":": TokenType.COLON,
                ";": TokenType.SEMICOLON, "(": TokenType.LPAREN,
                ")": TokenType.RPAREN, "[": TokenType.LBRACKET,
                "]": TokenType.RBRACKET, "{": TokenType.LBRACE,
                "}": TokenType.RBRACE,
            }
            if ch in single_char_map:
                self.tokens.append(Token(single_char_map[ch], ch, self.line, self.col))
                self._advance()
                continue

            raise LexerError(f"Unexpected character: '{ch}'", self.line, self.col)

        while len(self.indent_stack) > 1:
            self.tokens.append(Token(TokenType.DEDENT, "", self.line, self.col))
            self.indent_stack.pop()

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.col))
        return self.tokens

    def _is_division_context(self) -> bool:
        """Check if / should be division rather than regex literal.
        Checks the last token in self.tokens to determine context."""
        if not self.tokens:
            return False  # At start of file, / starts a regex
        # Get the last meaningful token (skip NEWLINE, INDENT, DEDENT)
        for tok in reversed(self.tokens):
            if tok.type in (TokenType.NEWLINE, TokenType.INDENT, TokenType.DEDENT, TokenType.COMMENT):
                continue
            last_type = tok.type
            division_preceding = {
                TokenType.IDENTIFIER, TokenType.INTEGER, TokenType.FLOAT,
                TokenType.RPAREN, TokenType.RBRACKET, TokenType.RBRACE,
                TokenType.THIS, TokenType.STRING, TokenType.BOOLEAN,
                TokenType.NULL
            }
            return last_type in division_preceding
        return False  # Only whitespace/comments before, treat as regex

    def _read_regex_literal(self, start_line: int, start_col: int):
        """Read a regex literal: /pattern/flags."""
        # We've already consumed the opening /
        pattern_chars = []
        escaped = False
        while self._current():
            ch = self._current()
            if escaped:
                pattern_chars.append(ch)
                escaped = False
                self._advance()
                continue
            if ch == "\\":
                escaped = True
                pattern_chars.append(ch)
                self._advance()
                continue
            if ch == "/":
                break
            if ch == "\n":
                return None  # Unterminated regex, not a valid literal
            pattern_chars.append(ch)
            self._advance()
        else:
            return None  # EOF without closing /

        # Consume closing /
        self._advance()

        # Read flags (optional)
        flags = []
        while self._current() and self._current().isalpha():
            flags.append(self._advance())

        return Token(TokenType.REGEX_LITERAL, {"pattern": "".join(pattern_chars), "flags": "".join(flags)}, start_line, start_col)


def tokenize(source: str) -> List[Token]:
    lexer = Lexer(source)
    return lexer.tokenize()
