"""
FusionBoa Language Parser

Converts a stream of tokens into an Abstract Syntax Tree (AST).
Uses recursive descent parsing with Pratt parsing for expressions.
Supports: const, yield, list comprehensions, default parameters,
keyword arguments, string interpolation, spread, export, and all base features.
"""

from typing import List, Optional
from ..lexer.tokens import Token, TokenType
from ..errors.error_handler import suggest_keyword
from .ast_nodes import *


class ParseError(Exception):
    def __init__(self, message: str, token: Token = None):
        if token:
            msg = f"Parse error at line {token.line}, col {token.col}: {message}"
        else:
            msg = f"Parse error: {message}"
        super().__init__(msg)
        self.token = token


class Parser:
    """Recursive descent parser for the Fusion language."""

    # Soft keywords: print aliases that the parser recognizes as print statements
    # These are NOT in the lexer's KEYWORDS to avoid word-boundary collisions
    # with variable names like 'cool_factor' or string values like "excellent".
    _SOFT_PRINT_ALIASES = {
        "nice", "excellent", "awesome", "superb", "cool", "sweet",
        "neat", "brilliant", "fantastic", "wonderful", "terrific",
    }

    # Token types that indicate assignment context (for soft keyword disambiguation)
    _ASSIGNMENT_LOOKAHEAD = {
        TokenType.EQUAL, TokenType.PLUS_EQUAL, TokenType.MINUS_EQUAL,
        TokenType.STAR_EQUAL, TokenType.SLASH_EQUAL, TokenType.BE,
        TokenType.TO, TokenType.LPAREN, TokenType.DOT,
        TokenType.PLUS_PLUS, TokenType.MINUS_MINUS,
        TokenType.PIPE_PIPE_EQUAL, TokenType.AMPERSAND_AMPERSAND_EQUAL,
        TokenType.QUESTION_QUESTION_EQUAL,
    }

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self._allow_ternary = True  # Flag to disable ternary in comprehension contexts

    def _current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token(TokenType.EOF, "", 0, 0)

    def _peek(self, offset: int = 1) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return Token(TokenType.EOF, "", 0, 0)

    def _advance(self) -> Token:
        token = self._current()
        self.pos += 1
        return token

    def _check(self, token_type: TokenType) -> bool:
        return self._current().type == token_type

    def _check_any(self, *token_types: TokenType) -> bool:
        return self._current().type in token_types

    def _match(self, token_type: TokenType, value=None) -> bool:
        if self._check(token_type):
            if value is None or self._current().value == value:
                return True
        return False

    def _consume(self, token_type: TokenType, error_msg: str = None, value=None) -> Token:
        token = self._current()
        if token.type != token_type:
            if error_msg is None:
                error_msg = f"Expected {token_type.name}, got {token.type.name}"
            raise ParseError(error_msg, token)
        if value is not None and token.value != value:
            raise ParseError(f"Expected '{value}', got '{token.value}'", token)
        return self._advance()

    def _skip_newlines(self):
        while self._check_any(TokenType.NEWLINE, TokenType.ARTICLE):
            self._advance()

    def _skip_articles(self):
        """Skip filler words like 'the', 'a', 'an' for natural English flow."""
        while self._match(TokenType.ARTICLE):
            self._advance()

    def _is_at_statement_end(self) -> bool:
        return self._check_any(TokenType.NEWLINE, TokenType.DEDENT, TokenType.EOF)

    def _is_expr_end(self) -> bool:
        """Check if we're at the end of an expression context."""
        return self._check_any(TokenType.NEWLINE, TokenType.DEDENT, TokenType.EOF,
                              TokenType.RPAREN, TokenType.RBRACKET, TokenType.RBRACE,
                              TokenType.COMMA, TokenType.COLON)

    # ---- Entry Point ----

    def parse(self) -> Program:
        statements = []
        self._skip_newlines()
        while not self._check(TokenType.EOF):
            stmt = self._parse_statement()
            if stmt is not None:
                statements.append(stmt)
            self._skip_newlines()
        return Program(statements=statements)

    # ---- Statement Parsing ----

    def _parse_statement(self) -> Optional[ASTNode]:
        self._skip_articles()
        token = self._current()

        if self._match(TokenType.LET):
            return self._parse_variable_declaration()
        if self._match(TokenType.LAZY):
            return self._parse_lazy_declaration()
        if self._match(TokenType.CONST):
            return self._parse_const_declaration()
        if self._match(TokenType.SET):
            return self._parse_assignment()
        if self._check_any(TokenType.INCREASE, TokenType.DECREASE):
            return self._parse_augmented_assignment()
        if self._match(TokenType.DEFINE):
            # define static function
            if self._peek().type == TokenType.IDENTIFIER and self._peek().value == "static":
                tok = self._advance()  # consume 'define'
                self._advance()  # consume 'static'
                if self._check(TokenType.FUNCTION):
                    func_def = self._parse_function_definition(is_static=True, from_tok=tok)
                    return StaticMethodDeclaration(declaration=func_def, line=tok.line, col=tok.col)
            if self._peek().type == TokenType.FUNCTION:
                return self._parse_function_definition()
            elif self._peek().type == TokenType.CLASS:
                return self._parse_class_definition()
            elif self._peek().type == TokenType.INTERFACE:
                return self._parse_interface_definition()
            elif self._peek().type == TokenType.ENUM:
                return self._parse_enum_definition(is_from_define=True)
            elif self._peek().type == TokenType.RECORD:
                return self._parse_record_definition()
            elif self._peek().type == TokenType.PROPERTY:
                return self._parse_property_definition()
            elif self._peek().type == TokenType.NAMESPACE:
                return self._parse_namespace_definition()
            elif self._peek().type == TokenType.EXTENSION:
                return self._parse_extension_definition()
            else:
                raise ParseError("Expected 'function', 'class', 'interface', 'enum', 'record', 'property', 'namespace', or 'extension' after 'define'", self._current())
        if self._match(TokenType.CREATE):
            return self._parse_create_statement()
        if self._match(TokenType.IF):
            return self._parse_if_statement()
        # Soft keyword: 'before' acts as 'if' when followed by a condition and colon
        if self._check(TokenType.IDENTIFIER) and self._current().value == "before":
            # Disambiguate: peek ahead. If next token looks like an assignment
            # or a call, treat 'before' as a variable name (fall through to expression).
            nxt = self._peek()
            if nxt.type not in self._ASSIGNMENT_LOOKAHEAD:
                return self._parse_before_if_statement()
        if self._match(TokenType.MATCH):
            return self._parse_match_statement()
        if self._match(TokenType.FOR):
            if self._peek().type == TokenType.AWAIT:
                return self._parse_for_await_loop()
            return self._parse_for_loop()
        if self._match(TokenType.REPEAT):
            # repeat forever
            if self._peek().type == TokenType.FOREVER:
                return self._parse_repeat_forever()
            return self._parse_repeat_loop()
        if self._match(TokenType.WHILE):
            return self._parse_while_loop()
        if self._match(TokenType.RETURN):
            return self._parse_return_statement()
        if self._match(TokenType.YIELD):
            return self._parse_yield_statement()
        if self._match(TokenType.BREAK):
            tok = self._advance()
            return BreakStatement(line=tok.line, col=tok.col)
        if self._match(TokenType.CONTINUE):
            tok = self._advance()
            return ContinueStatement(line=tok.line, col=tok.col)
        if self._match(TokenType.PASS):
            tok = self._advance()
            return PassStatement(line=tok.line, col=tok.col)
        if self._match(TokenType.TRY):
            return self._parse_try_statement()
        if self._match(TokenType.EXPORT):
            return self._parse_export_statement()
        if self._match(TokenType.USE):
            return self._parse_import_statement()
        if self._match(TokenType.FROM):
            return self._parse_from_import_statement()
        if self._check_any(TokenType.PRINT, TokenType.DISPLAY, TokenType.SHOW):
            return self._parse_print_statement()
        if self._match(TokenType.INPUT):
            return self._parse_input_statement()
        if self._match(TokenType.AWAIT):
            return self._parse_await_statement()
        if self._match(TokenType.ASSERT):
            return self._parse_assert_statement()
        if self._match(TokenType.RAISE):
            return self._parse_raise_statement()
        if self._match(TokenType.DELETE):
            return self._parse_delete_statement()
        if self._match(TokenType.SWITCH):
            return self._parse_match_statement()  # switch is alias for match
        if self._match(TokenType.UNTIL):
            return self._parse_until_loop()
        if self._match(TokenType.UNLESS):
            return self._parse_unless_statement()
        if self._match(TokenType.USING):
            return self._parse_using_statement()
        if self._match(TokenType.DEFER):
            return self._parse_defer_statement()
        if self._match(TokenType.GUARD):
            return self._parse_guard_statement()
        if self._match(TokenType.DO):
            return self._parse_do_while_loop()
        if self._match(TokenType.ENUM):
            return self._parse_enum_definition(is_from_define=False)
        if self._match(TokenType.SWAP):
            return self._parse_swap_statement()
        if self._match(TokenType.PUSH):
            return self._parse_push_statement()
        if self._match(TokenType.POP):
            return self._parse_pop_statement()
        if self._check_any(TokenType.ADD, TokenType.SUBTRACT):
            return self._parse_add_subtract_statement()
        if self._check_any(TokenType.MULTIPLY, TokenType.DIVIDE):
            return self._parse_multiply_divide_statement()
        if self._match(TokenType.REVERSE):
            tok = self._advance()
            name = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'reverse'").value
            return ExpressionStatement(expression=Call(callee=Attribute(object=Identifier(name=name), attribute="reverse")), line=tok.line, col=tok.col)
        if self._match(TokenType.SORT):
            tok = self._advance()
            name = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'sort'").value
            return ExpressionStatement(expression=Call(callee=Attribute(object=Identifier(name=name), attribute="sort")), line=tok.line, col=tok.col)
        if self._match(TokenType.CLEAR):
            tok = self._advance()
            name = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'clear'").value
            return ExpressionStatement(expression=Call(callee=Attribute(object=Identifier(name=name), attribute="clear")), line=tok.line, col=tok.col)
        if self._match(TokenType.APPEND):
            return self._parse_append_statement()
        if self._match(TokenType.REMOVE):
            return self._parse_remove_statement()
        if self._match(TokenType.WITH):
            return self._parse_with_statement()
        if self._match(TokenType.AT_SIGN):
            return self._parse_decorator_statement()
        if self._match(TokenType.MAP):
            return self._parse_map_statement()
        if self._match(TokenType.FILTER) or self._match(TokenType.KEEP):
            return self._parse_filter_statement()
        if self._match(TokenType.REDUCE) or self._match(TokenType.COMBINE):
            return self._parse_reduce_statement()
        if self._match(TokenType.SEARCH) or self._match(TokenType.FIND):
            return self._parse_search_statement()
        if self._match(TokenType.REPLACE_WITH):
            return self._parse_replace_statement()
        if self._match(TokenType.TRANSFORM):
            return self._parse_transform_statement()
        if self._match(TokenType.COUNT):
            return self._parse_count_statement()

        # ---- v0.9.1 Universal Polyglot Parsers ----
        if self._match(TokenType.GOROUTINE):
            return self._parse_go_statement()
        if self._match(TokenType.CHANNEL) or (self._check(TokenType.IDENTIFIER) and self._current().value == "channel"):
            return self._parse_channel_declaration()
        if self._match(TokenType.SEND):
            return self._parse_channel_send()
        if self._match(TokenType.RECEIVE):
            return self._parse_channel_receive()
        if self._match(TokenType.CLOSE_CHANNEL):
            return self._parse_channel_close()
        if self._match(TokenType.SELECT_CHANNEL):
            return self._parse_channel_select()
        if self._match(TokenType.MULTI_RETURN):
            return self._parse_multi_return()
        if self._match(TokenType.YIELD_FROM):
            return self._parse_yield_from()
        if self._match(TokenType.GLOBAL):
            return self._parse_global_statement()
        if self._match(TokenType.NONLOCAL):
            return self._parse_nonlocal_statement()
        if self._match(TokenType.ASYNC_WITH):
            return self._parse_async_with()
        if self._match(TokenType.MODULE):
            return self._parse_module_definition()
        if self._match(TokenType.MIXIN):
            return self._parse_mixin_statement()
        if self._match(TokenType.OBJECT):
            return self._parse_object_definition()
        if self._match(TokenType.ACTOR):
            return self._parse_actor_definition()
        if self._match(TokenType.SEALED):
            return self._parse_sealed_class_definition()
        if self._match(TokenType.SUSPEND):
            return self._parse_suspend_function()
        if self._match(TokenType.PACKAGE):
            return self._parse_package_declaration()
        if self._match(TokenType.NATIVE):
            return self._parse_native_declaration()
        if self._match(TokenType.SYNCHRONIZED):
            return self._parse_synchronized_block()
        if self._match(TokenType.DATA_CLASS):
            return self._parse_data_class_definition()
        if self._match(TokenType.DELEGATE):
            return self._parse_delegate_definition()
        if self._match(TokenType.EVENT):
            return self._parse_event_declaration()
        if self._match(TokenType.PARTIAL_CLASS):
            return self._parse_partial_class_definition()
        if self._match(TokenType.MACRO):
            return self._parse_macro_definition()
        if self._match(TokenType.FFI):
            return self._parse_native_declaration()

        # Soft keyword print aliases: nice, excellent, cool, sweet, etc.
        # These are lexed as IDENTIFIER tokens (not PRINT) to avoid collisions
        # with variable names. The parser promotes them to print statements here.
        if self._check(TokenType.IDENTIFIER) and self._current().value in self._SOFT_PRINT_ALIASES:
            # Disambiguate: if next token is assignment-like, treat as variable
            nxt = self._peek()
            if nxt.type not in self._ASSIGNMENT_LOOKAHEAD:
                tok = self._advance()
                expr = None if self._is_at_statement_end() else self._parse_expression()
                return PrintStatement(expression=expr)

        # x++ or x-- (increment/decrement expressions as statements)
        if self._is_name_token(self._current().type):
            saved_pos = self.pos
            name_tok = self._current()
            name = name_tok.value
            if self._peek().type == TokenType.PLUS_PLUS:
                self._advance()  # consume name
                self._advance()  # consume ++
                return ExpressionStatement(expression=IncrementExpression(target=name, prefix=False, line=name_tok.line, col=name_tok.col))
            if self._peek().type == TokenType.MINUS_MINUS:
                self._advance()  # consume name
                self._advance()  # consume --
                return ExpressionStatement(expression=DecrementExpression(target=name, prefix=False, line=name_tok.line, col=name_tok.col))

        # ++x or --x (prefix increment/decrement)
        if self._check(TokenType.PLUS_PLUS):
            tok = self._advance()
            name = self._parse_name_token()
            return ExpressionStatement(expression=IncrementExpression(target=name, prefix=True, line=tok.line, col=tok.col))
        if self._check(TokenType.MINUS_MINUS):
            tok = self._advance()
            name = self._parse_name_token()
            return ExpressionStatement(expression=DecrementExpression(target=name, prefix=True, line=tok.line, col=tok.col))

        # Logical assignment: x ||= value, x &&= value, x ??= value
        # Check for any identifier-like token (including keywords used as variables)
        if self._is_name_token(self._current().type):
            saved_pos = self.pos
            name_tok = self._current()
            name = name_tok.value
            if self._peek().type in (TokenType.PIPE_PIPE_EQUAL, TokenType.AMPERSAND_AMPERSAND_EQUAL, TokenType.QUESTION_QUESTION_EQUAL):
                self._advance()  # consume identifier-like token
                op_token = self._advance()  # consume ||=/&&=/??=
                value = self._parse_expression()
                op_map = {
                    TokenType.PIPE_PIPE_EQUAL: "||",
                    TokenType.AMPERSAND_AMPERSAND_EQUAL: "&&",
                    TokenType.QUESTION_QUESTION_EQUAL: "??",
                }
                op = op_map.get(op_token.type, "||")
                return AugmentedAssignment(target=name, operator=op, value=value, line=name_tok.line, col=name_tok.col)

        # Keyword misspelling check: before falling through to expression parsing,
        # check if the current identifier looks like a misspelled keyword
        if self._check(TokenType.IDENTIFIER):
            suggestion = suggest_keyword(self._current().value)
            if suggestion:
                tok = self._current()
                raise ParseError(f"Unknown word '{tok.value}'. {suggestion}?", tok)

        expr = self._parse_expression()
        tok = self._current()
        return ExpressionStatement(expression=expr, line=tok.line, col=tok.col)

    def _parse_block(self) -> List[ASTNode]:
        self._skip_newlines()
        self._consume(TokenType.COLON, "Expected ':' at start of block")
        self._skip_newlines()
        self._consume(TokenType.INDENT, "Expected indented block after ':'")
        statements = []
        while not self._check_any(TokenType.DEDENT, TokenType.EOF):
            stmt = self._parse_statement()
            if stmt is not None:
                statements.append(stmt)
            self._skip_newlines()
        if self._check(TokenType.DEDENT):
            self._advance()
        return statements

    def _parse_block_contents(self) -> List[ASTNode]:
        self._skip_newlines()
        if self._check(TokenType.INDENT):
            self._advance()
        stmts = []
        while not self._check_any(TokenType.DEDENT, TokenType.EOF):
            if self._check_any(TokenType.CASE, TokenType.DEFAULT):
                break
            stmt = self._parse_statement()
            if stmt is not None:
                stmts.append(stmt)
            self._skip_newlines()
        if self._check(TokenType.DEDENT):
            self._advance()
        return stmts

    # ---- Specific Statement Parsers ----

    # Set of token types that can NEVER be variable names (operators, punctuation, literals)
    _STRUCTURAL_TOKENS = {
        TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH,
        TokenType.SLASH_SLASH, TokenType.PERCENT, TokenType.CARET,
        TokenType.EQUAL, TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL,
        TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL,
        TokenType.PLUS_EQUAL, TokenType.MINUS_EQUAL, TokenType.STAR_EQUAL, TokenType.SLASH_EQUAL,
        TokenType.DOT, TokenType.COMMA, TokenType.COLON, TokenType.SEMICOLON,
        TokenType.LPAREN, TokenType.RPAREN, TokenType.LBRACKET, TokenType.RBRACKET,
        TokenType.LBRACE, TokenType.RBRACE, TokenType.ARROW, TokenType.FAT_ARROW,
        TokenType.PIPE, TokenType.PIPE_OP, TokenType.PIPE_PIPE, TokenType.PIPE_PIPE_EQUAL,
        TokenType.AMPERSAND, TokenType.AMPERSAND_AMPERSAND, TokenType.AMPERSAND_AMPERSAND_EQUAL,
        TokenType.TILDE, TokenType.LESS_LESS, TokenType.GREATER_GREATER,
        TokenType.QUESTION, TokenType.QUESTION_DOT, TokenType.QUESTION_QUESTION,
        TokenType.QUESTION_QUESTION_EQUAL, TokenType.DOT_DOT, TokenType.DOT_DOT_DOT,
        TokenType.PLUS_PLUS, TokenType.MINUS_MINUS, TokenType.AT_SIGN,
        TokenType.INTEGER, TokenType.FLOAT, TokenType.STRING, TokenType.BOOLEAN,
        TokenType.NULL, TokenType.INTERP_STRING,
        TokenType.NEWLINE, TokenType.INDENT, TokenType.DEDENT, TokenType.EOF, TokenType.COMMENT,
    }

    def _is_name_token(self, token_type: TokenType) -> bool:
        """Check if a token type can be used as a variable name."""
        if token_type == TokenType.IDENTIFIER:
            return True
        return token_type not in self._STRUCTURAL_TOKENS

    def _parse_name_token(self) -> str:
        """Consume a token that can be used as a variable name (identifier or keyword)."""
        self._skip_articles()
        token = self._current()
        if token.type == TokenType.IDENTIFIER:
            self._advance()
            return token.value
        # Type keywords that can serve as variable names
        type_keywords = {
            TokenType.LIST_TYPE: "list", TokenType.STRING_TYPE: "string",
            TokenType.INTEGER_TYPE: "integer", TokenType.FLOAT_TYPE: "float",
            TokenType.BOOLEAN_TYPE: "boolean", TokenType.DICT_TYPE: "dictionary",
            TokenType.ANY_TYPE: "any",
        }
        if token.type in type_keywords:
            tok = self._advance()
            return tok.value
        if self._is_name_token(token.type):
            self._advance()
            return token.value
        raise ParseError(f"Expected variable name, got {token.type.name} ({repr(token.value)})", token)

    def _parse_variable_declaration(self) -> ASTNode:
        tok = self._advance()
        type_annotation = None
        
        # Destructuring: let [a, b] be [1, 2] or let {name, age} be user
        if self._check(TokenType.LBRACKET):
            self._advance()  # consume '['
            targets = []
            while not self._check(TokenType.RBRACKET):
                name = self._parse_name_token()
                targets.append(name)
                if self._match(TokenType.COMMA):
                    self._advance()
            self._consume(TokenType.RBRACKET, "Expected ']'")
            self._consume(TokenType.BE, "Expected 'be' after destructuring pattern")
            value = self._parse_expression()
            return DestructuringDeclaration(targets=targets, value=value, destructure_type="list", var_type="variable", line=tok.line, col=tok.col)
        
        if self._check(TokenType.LBRACE):
            self._advance()  # consume '{'
            targets = []
            while not self._check(TokenType.RBRACE):
                name = self._parse_name_token()
                targets.append(name)
                if self._match(TokenType.COMMA):
                    self._advance()
            self._consume(TokenType.RBRACE, "Expected '}'")
            self._consume(TokenType.BE, "Expected 'be' after destructuring pattern")
            value = self._parse_expression()
            return DestructuringDeclaration(targets=targets, value=value, destructure_type="dict", var_type="variable", line=tok.line, col=tok.col)
        
        name = self._parse_name_token()
        
        # Type annotation: let x: int be 5
        if self._match(TokenType.COLON):
            self._advance()
            type_name = self._parse_type_name()
            type_annotation = TypeAnnotation(type_name=type_name, line=tok.line, col=tok.col)
        
        self._consume(TokenType.BE, "Expected 'be' after variable name in 'let'")
        value = self._parse_expression()
        return VariableDeclaration(name=name, value=value, var_type="variable", type_annotation=type_annotation, line=tok.line, col=tok.col)

    def _parse_const_declaration(self) -> ASTNode:
        tok = self._advance()
        type_annotation = None
        
        # Destructuring: const [a, b] be [1, 2]
        if self._check(TokenType.LBRACKET):
            self._advance()  # consume '['
            targets = []
            while not self._check(TokenType.RBRACKET):
                name = self._parse_name_token()
                targets.append(name)
                if self._match(TokenType.COMMA):
                    self._advance()
            self._consume(TokenType.RBRACKET, "Expected ']'")
            self._consume(TokenType.BE, "Expected 'be' after destructuring pattern")
            value = self._parse_expression()
            return DestructuringDeclaration(targets=targets, value=value, destructure_type="list", var_type="constant", line=tok.line, col=tok.col)
        
        name = self._parse_name_token()
        
        # Type annotation: const PI: float be 3.14
        if self._match(TokenType.COLON):
            self._advance()
            type_name = self._parse_type_name()
            type_annotation = TypeAnnotation(type_name=type_name, line=tok.line, col=tok.col)
        
        self._consume(TokenType.BE, "Expected 'be' after name in 'const'")
        value = self._parse_expression()
        return ConstDeclaration(name=name, value=value, type_annotation=type_annotation, line=tok.line, col=tok.col)

    def _parse_assignment(self) -> Assignment:
        tok = self._advance()
        name = self._parse_dotted_name()
        self._consume(TokenType.TO, "Expected 'to' after target in 'set'")
        value = self._parse_expression()
        return Assignment(target=name, value=value, line=tok.line, col=tok.col)

    def _parse_augmented_assignment(self) -> AugmentedAssignment:
        is_increase = self._check(TokenType.INCREASE)
        tok = self._advance()
        op = "+" if is_increase else "-"
        name = self._parse_dotted_name()
        self._consume(TokenType.BY, "Expected 'by'")
        value = self._parse_expression()
        return AugmentedAssignment(target=name, operator=op, value=value, line=tok.line, col=tok.col)



    def _parse_function_definition(self, is_static: bool = False, from_tok: Token = None) -> FunctionDefinition:
        tok = from_tok if from_tok else self._advance()
        is_async = False
        if self._match(TokenType.ASYNC):
            is_async = True
            self._advance()
        self._consume(TokenType.FUNCTION, "Expected 'function'")
        name = self._parse_name_token()

        params = []
        defaults = {}
        has_rest = False
        rest_name = ""

        if self._match(TokenType.WITH):
            self._advance()
            if self._check(TokenType.IDENTIFIER) or self._check(TokenType.DOT_DOT_DOT) or self._is_name_token(self._current().type):
                params, defaults, has_rest, rest_name = self._parse_parameter_list_with_defaults()

        body = self._parse_block()
        return FunctionDefinition(name=name, parameters=params, defaults=defaults,
                                  body=body, is_async=is_async,
                                  has_rest_param=has_rest, rest_param_name=rest_name,
                                  is_static=is_static,
                                  line=tok.line, col=tok.col)

    def _parse_parameter_list_with_defaults(self):
        params = []
        defaults = {}
        has_rest = False
        rest_name = ""

        while True:
            if self._check(TokenType.DOT_DOT_DOT):
                self._advance()
                has_rest = True
                rest_name = self._consume(TokenType.IDENTIFIER, "Expected parameter name after '...'").value
                break

            if not (self._check(TokenType.IDENTIFIER) or self._is_name_token(self._current().type)):
                break
            name = self._parse_name_token()
            params.append(name)

            if self._match(TokenType.EQUAL):
                self._advance()
                default_val = self._parse_expression()
                defaults[name] = default_val

            if not self._match(TokenType.COMMA):
                break
            self._advance()

        return params, defaults, has_rest, rest_name

    def _parse_export_statement(self) -> ExportStatement:
        tok = self._advance()
        decl = self._parse_statement()
        return ExportStatement(declaration=decl, line=tok.line, col=tok.col)

    def _parse_create_statement(self) -> VariableDeclaration:
        tok = self._advance()
        # Accept ARTICLE 'the' or IDENTIFIER 'a'/'an' for natural English
        if self._match(TokenType.ARTICLE):
            self._advance()  # skip 'the'
        elif self._check(TokenType.IDENTIFIER) and self._current().value in ("a", "an"):
            self._advance()  # skip 'a'/'an'
        var_type = "list"
        if (self._check(TokenType.IDENTIFIER) and self._current().value == "list") or \
           self._check(TokenType.LIST_TYPE):
            var_type = "list"
        elif (self._check(TokenType.IDENTIFIER) and self._current().value in ("dict", "dictionary", "map", "table", "hash")) or \
             self._check(TokenType.DICT_TYPE):
            var_type = "dict"
        else:
            raise ParseError("Expected 'list', 'dict', 'dictionary', or 'map'", self._current())
        self._advance()  # consume the type keyword/identifier
        self._consume(TokenType.CALLED, "Expected 'called'")
        name = self._consume(TokenType.IDENTIFIER, "Expected variable name").value
        self._consume(TokenType.WITH, "Expected 'with'")
        value = self._parse_expression()
        return VariableDeclaration(name=name, value=value, var_type=var_type, line=tok.line, col=tok.col)

    def _parse_if_rest(self) -> tuple:
        """Parse elif/else branches shared by if and before-if statements."""
        elif_branches = []
        else_body = []
        while self._check_any(TokenType.OR, TokenType.OTHERWISE):
            self._advance()
            if self._check(TokenType.IF):
                self._advance()
                elif_cond = self._parse_expression()
                elif_body = self._parse_block()
                elif_branches.append((elif_cond, elif_body))
            else:
                else_body = self._parse_block()
                break
        return elif_branches, else_body

    def _parse_if_statement(self) -> IfStatement:
        tok = self._advance()
        condition = self._parse_expression()
        body = self._parse_block()
        elif_branches, else_body = self._parse_if_rest()
        return IfStatement(condition=condition, body=body, elif_branches=elif_branches,
                           else_body=else_body, line=tok.line, col=tok.col)

    def _parse_before_if_statement(self) -> IfStatement:
        """'before condition:' as if statement (soft keyword handled by parser)."""
        tok = self._advance()  # consume 'before' identifier
        condition = self._parse_expression()
        body = self._parse_block()
        elif_branches, else_body = self._parse_if_rest()
        return IfStatement(condition=condition, body=body, elif_branches=elif_branches,
                           else_body=else_body, line=tok.line, col=tok.col)

    def _parse_match_statement(self) -> MatchStatement:
        tok = self._advance()
        expr = self._parse_expression()
        self._skip_newlines()
        self._consume(TokenType.COLON, "Expected ':' after match expression")
        self._skip_newlines()
        self._consume(TokenType.INDENT, "Expected indented block after ':'")
        cases = []
        guarded_cases = []
        default_body = []
        while not self._check_any(TokenType.DEDENT, TokenType.EOF):
            self._skip_newlines()
            if self._check(TokenType.DEFAULT):
                self._advance()
                self._consume(TokenType.COLON, "Expected ':' after 'default'")
                default_body = self._parse_block_contents()
                break
            if self._check(TokenType.CASE):
                self._advance()
                pattern = self._parse_expression()
                # Check for match guard: case x if x > 5:
                guard = None
                if self._match(TokenType.IF):
                    self._advance()
                    guard = self._parse_expression()
                self._consume(TokenType.COLON, "Expected ':' after case pattern")
                case_body = self._parse_block_contents()
                if guard:
                    guarded_cases.append(MatchGuard(pattern=pattern, guard=guard, body=case_body))
                else:
                    cases.append((pattern, case_body))
            else:
                raise ParseError("Expected 'case' or 'default' in match block", self._current())
        if self._check(TokenType.DEDENT):
            self._advance()
        return MatchStatement(expression=expr, cases=cases, guarded_cases=guarded_cases, default_body=default_body, line=tok.line, col=tok.col)

    def _parse_for_loop(self) -> ForLoop:
        tok = self._advance()
        if self._match(TokenType.EACH):
            self._advance()
            var_name = self._consume(TokenType.IDENTIFIER, "Expected variable name").value
            self._consume(TokenType.IN, "Expected 'in'")
            iterable = self._parse_expression()
            body = self._parse_block()
            return ForLoop(variable=var_name, iterable=iterable, body=body, line=tok.line, col=tok.col)
        if self._check(TokenType.IDENTIFIER) and self._peek().type == TokenType.IN:
            # for key in obj (dict iteration without 'each')
            var_name = self._consume(TokenType.IDENTIFIER, "Expected variable name").value
            self._consume(TokenType.IN, "Expected 'in'")
            iterable = self._parse_expression()
            body = self._parse_block()
            return ForLoop(variable=var_name, iterable=iterable, body=body, is_dict_iteration=True, line=tok.line, col=tok.col)
        var_name = self._consume(TokenType.IDENTIFIER, "Expected variable name").value
        self._consume(TokenType.FROM, "Expected 'from'")
        range_from = self._parse_expression()
        self._consume(TokenType.TO, "Expected 'to'")
        range_to = self._parse_expression()
        body = self._parse_block()
        return ForLoop(variable=var_name, range_from=range_from, range_to=range_to, body=body, line=tok.line, col=tok.col)

    def _parse_repeat_forever(self) -> WhileLoop:
        """repeat forever: body -> while True: body"""
        tok = self._advance()  # consume 'repeat'
        self._advance()  # consume 'forever'
        body = self._parse_block()
        return WhileLoop(condition=Literal(value=True, line=tok.line, col=tok.col),
                         body=body, line=tok.line, col=tok.col)

    def _parse_repeat_loop(self) -> RepeatLoop:
        tok = self._advance()
        # Use PREC_PRODUCT to stop before '*' since 'times' lexes as STAR
        times = self._parse_expression(self.PREC_PRODUCT)
        # Accept both TIMES token and STAR token with value 'times'
        if self._match(TokenType.TIMES):
            self._advance()
        elif self._match(TokenType.STAR) and self._current().value == 'times':
            self._advance()
        else:
            self._consume(TokenType.TIMES, "Expected 'times'")
        body = self._parse_block()
        return RepeatLoop(times=times, body=body, line=tok.line, col=tok.col)

    def _parse_while_loop(self) -> WhileLoop:
        tok = self._advance()
        condition = self._parse_expression()
        body = self._parse_block()
        return WhileLoop(condition=condition, body=body, line=tok.line, col=tok.col)

    def _parse_return_statement(self) -> ReturnStatement:
        tok = self._advance()
        value = None if self._is_at_statement_end() else self._parse_expression()
        return ReturnStatement(value=value, line=tok.line, col=tok.col)

    def _parse_yield_statement(self) -> YieldStatement:
        tok = self._advance()
        value = None if self._is_at_statement_end() else self._parse_expression()
        return YieldStatement(value=value, line=tok.line, col=tok.col)

    def _parse_try_statement(self) -> TryStatement:
        tok = self._advance()
        body = self._parse_block()
        catch_var = None
        catch_body = []
        finally_body = []
        if self._check(TokenType.CATCH):
            self._advance()
            if self._match(TokenType.ERROR):
                self._advance()
            if self._match(TokenType.AS):
                self._advance()
                catch_var = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'as'").value
            catch_body = self._parse_block()
        if self._check(TokenType.FINALLY):
            self._advance()
            finally_body = self._parse_block()
        return TryStatement(body=body, catch_var=catch_var, catch_body=catch_body,
                            finally_body=finally_body, line=tok.line, col=tok.col)

    def _parse_dotted_name(self) -> str:
        if self._check(TokenType.THIS):
            parts = [self._advance().value]
        else:
            if self._check(TokenType.IDENTIFIER):
                parts = [self._advance().value]
            elif self._is_name_token(self._current().type):
                parts = [self._parse_name_token()]
            else:
                self._consume(TokenType.IDENTIFIER, "Expected identifier")
                parts = [""]
        while self._match(TokenType.DOT):
            self._advance()
            if self._check(TokenType.IDENTIFIER):
                parts.append(self._advance().value)
            elif self._is_name_token(self._current().type):
                parts.append(self._parse_name_token())
            else:
                self._consume(TokenType.IDENTIFIER, "Expected identifier after '.'")
        return ".".join(parts)

    def _parse_import_statement(self) -> ImportStatement:
        tok = self._advance()
        module = self._parse_dotted_name()
        alias = None
        if self._match(TokenType.AS):
            self._advance()
            alias = self._consume(TokenType.IDENTIFIER).value
        return ImportStatement(module=module, alias=alias, line=tok.line, col=tok.col)

    def _parse_do_while_loop(self) -> DoWhileLoop:
        """do: body; while condition"""
        tok = self._advance()  # consume 'do'
        body = self._parse_block()
        self._consume(TokenType.WHILE, "Expected 'while' after do block")
        condition = self._parse_expression()
        return DoWhileLoop(condition=condition, body=body, line=tok.line, col=tok.col)

    def _parse_enum_definition(self, is_from_define: bool = False) -> EnumDefinition:
        """define enum Name: A, B, C"""
        tok = self._advance()  # consume 'define' or 'enum'
        if is_from_define:
            self._consume(TokenType.ENUM, "Expected 'enum'")
        name = self._consume(TokenType.IDENTIFIER, "Expected enum name").value
        self._skip_newlines()
        self._consume(TokenType.COLON, "Expected ':' after enum name")
        self._skip_newlines()
        self._consume(TokenType.INDENT, "Expected indented block")
        members = []
        while not self._check_any(TokenType.DEDENT, TokenType.EOF):
            self._skip_newlines()
            if self._check(TokenType.IDENTIFIER):
                members.append(self._advance().value)
                if self._match(TokenType.COMMA):
                    self._advance()
            else:
                break
        if self._check(TokenType.DEDENT):
            self._advance()
        return EnumDefinition(name=name, members=members, line=tok.line, col=tok.col)

    def _parse_from_import_statement(self) -> ImportStatement:
        tok = self._advance()
        module = self._parse_dotted_name()
        self._consume(TokenType.IMPORT, "Expected 'import'")
        items = self._parse_comma_separated_idents()
        return ImportStatement(module=module, items=items, line=tok.line, col=tok.col)

    def _parse_print_statement(self) -> PrintStatement:
        self._advance()
        expr = None if self._is_at_statement_end() else self._parse_expression()
        return PrintStatement(expression=expr)

    def _parse_input_statement(self) -> InputStatement:
        tok = self._advance()
        target = None
        prompt = None
        if not self._is_at_statement_end():
            if self._check(TokenType.IDENTIFIER) and self._peek().type == TokenType.AS:
                target = self._consume(TokenType.IDENTIFIER).value
                self._advance()
                if self._match(TokenType.WITH):
                    self._advance()
                    self._consume(TokenType.IDENTIFIER, "Expected 'prompt'", value="prompt")
                    prompt = self._consume(TokenType.STRING).value
        return InputStatement(target=target, prompt=prompt, line=tok.line, col=tok.col)

    def _parse_assert_statement(self) -> AssertStatement:
        tok = self._advance()
        condition = self._parse_expression()
        message = None
        if not self._is_at_statement_end():
            message = self._parse_expression()
        return AssertStatement(condition=condition, message=message, line=tok.line, col=tok.col)

    def _parse_raise_statement(self) -> RaiseStatement:
        tok = self._advance()
        if self._check(TokenType.ERROR):
            self._advance()  # consume optional 'error'
        message = None if self._is_at_statement_end() else self._parse_expression()
        return RaiseStatement(message=message, line=tok.line, col=tok.col)

    def _parse_delete_statement(self) -> DeleteStatement:
        tok = self._advance()
        target = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'delete'").value
        source = None
        if self._match(TokenType.FROM):
            self._advance()
            source = self._parse_expression()
        return DeleteStatement(target=target, source=source, line=tok.line, col=tok.col)

    def _parse_until_loop(self) -> WhileLoop:
        """repeat until condition: body"""
        tok = self._advance()
        condition = self._parse_expression()
        body = self._parse_block()
        # until is while not
        not_cond = UnaryOp(operator="not", operand=condition, line=condition.line, col=condition.col)
        return WhileLoop(condition=not_cond, body=body, line=tok.line, col=tok.col)

    def _parse_unless_statement(self) -> IfStatement:
        """unless condition: body"""
        tok = self._advance()
        condition = self._parse_expression()
        body = self._parse_block()
        # unless is if not
        not_cond = UnaryOp(operator="not", operand=condition, line=condition.line, col=condition.col)
        return IfStatement(condition=not_cond, body=body, elif_branches=[], else_body=[], line=tok.line, col=tok.col)

    def _parse_using_statement(self) -> UsingStatement:
        """using resource as name: body -> context manager"""
        tok = self._advance()
        resource = self._parse_expression()
        var_name = None
        if self._match(TokenType.AS):
            self._advance()
            var_name = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'as'").value
        body = self._parse_block()
        return UsingStatement(resource=resource, variable=var_name, body=body, line=tok.line, col=tok.col)

    def _parse_defer_statement(self) -> DeferStatement:
        """defer: body - runs at function exit."""
        tok = self._advance()
        if self._check(TokenType.COLON):
            # Block-style defer - _parse_block will consume the colon
            body = self._parse_block()
        else:
            # Single-line defer: defer expression
            expr = self._parse_expression()
            body = [ExpressionStatement(expression=expr)]
        return DeferStatement(body=body, line=tok.line, col=tok.col)

    def _parse_guard_statement(self) -> GuardStatement:
        """guard condition else: body - exit if condition fails."""
        tok = self._advance()
        condition = self._parse_expression()
        self._consume(TokenType.ELSE, "Expected 'else' after guard condition")
        body = self._parse_block()
        return GuardStatement(condition=condition, body=body, line=tok.line, col=tok.col)

    def _parse_add_subtract_statement(self) -> AugmentedAssignment:
        """add x to y -> y += x, subtract x from y -> y -= x"""
        is_add = self._check(TokenType.ADD)
        tok = self._advance()  # consume 'add'/'subtract'
        value = self._parse_expression()
        if is_add:
            self._consume(TokenType.TO, "Expected 'to' after add value")
        else:
            self._consume(TokenType.FROM, "Expected 'from' after subtract value")
        name = self._parse_dotted_name()
        op = "+" if is_add else "-"
        return AugmentedAssignment(target=name, operator=op, value=value, line=tok.line, col=tok.col)

    def _parse_multiply_divide_statement(self) -> AugmentedAssignment:
        """multiply x by 2 -> x *= 2, divide x by 2 -> x /= 2"""
        is_mul = self._check(TokenType.MULTIPLY)
        tok = self._advance()  # consume 'multiply'/'divide'
        name = self._parse_dotted_name()
        self._consume(TokenType.BY, "Expected 'by'")
        value = self._parse_expression()
        op = "*" if is_mul else "/"
        return AugmentedAssignment(target=name, operator=op, value=value, line=tok.line, col=tok.col)

    def _parse_append_statement(self) -> ExpressionStatement:
        """append value to list -> list.append(value)"""
        tok = self._current()
        self._advance()  # consume 'append'
        value = self._parse_expression()
        self._consume(TokenType.TO, "Expected 'to' after append value")
        target = self._consume(TokenType.IDENTIFIER, "Expected list name after 'to'").value
        return ExpressionStatement(expression=Call(
            callee=Attribute(object=Identifier(name=target), attribute="append"),
            arguments=[value]
        ), line=tok.line, col=tok.col)

    def _parse_remove_statement(self) -> ExpressionStatement:
        """remove value from list -> list.remove(value)"""
        tok = self._current()
        self._advance()  # consume 'remove'
        value = self._parse_expression()
        self._consume(TokenType.FROM, "Expected 'from' after remove value")
        target = self._consume(TokenType.IDENTIFIER, "Expected list name after 'from'").value
        return ExpressionStatement(expression=Call(
            callee=Attribute(object=Identifier(name=target), attribute="remove"),
            arguments=[value]
        ), line=tok.line, col=tok.col)

    def _parse_with_statement(self) -> WithStatement:
        """with resource [as name]: body - context manager"""
        tok = self._current()
        self._advance()  # consume 'with'
        resource = self._parse_expression()
        variable = None
        if self._match(TokenType.AS):
            self._advance()  # consume 'as'
            variable = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'as'").value
        body = self._parse_block()
        return WithStatement(resource=resource, variable=variable, body=body, line=tok.line, col=tok.col)

    def _parse_decorator_statement(self) -> DecoratorStatement:
        """@decorator - decorator annotation"""
        tok = self._current()
        self._advance()  # consume @
        name = self._consume(TokenType.IDENTIFIER, "Expected decorator name after '@'").value
        args = []
        if self._match(TokenType.LPAREN):
            # @decorator(args)
            self._advance()  # consume '('
            if not self._check(TokenType.RPAREN):
                args = self._parse_argument_list()
            self._consume(TokenType.RPAREN, "Expected ')'")
        return DecoratorStatement(name=name, arguments=args, line=tok.line, col=tok.col)

    def _parse_swap_statement(self) -> SwapStatement:
        """swap x and y"""
        tok = self._current()
        self._advance()  # consume 'swap'
        left = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'swap'").value
        self._consume(TokenType.AND, "Expected 'and' between swapped variables")
        right = self._consume(TokenType.IDENTIFIER, "Expected second variable name").value
        return SwapStatement(left=left, right=right, line=tok.line, col=tok.col)

    def _parse_push_statement(self) -> PushStatement:
        """push value into list"""
        tok = self._current()
        self._advance()  # consume 'push'
        value = self._parse_expression()
        self._consume(TokenType.INTO, "Expected 'into' after push value")
        target = self._consume(TokenType.IDENTIFIER, "Expected list name after 'into'").value
        return PushStatement(value=value, target=target, line=tok.line, col=tok.col)

    def _parse_pop_statement(self) -> PopStatement:
        """pop from list"""
        tok = self._current()
        self._advance()  # consume 'pop'
        self._consume(TokenType.FROM, "Expected 'from' after 'pop'")
        target = self._consume(TokenType.IDENTIFIER, "Expected list name after 'from'").value
        return PopStatement(target=target, line=tok.line, col=tok.col)

    def _parse_await_statement(self) -> ExpressionStatement:
        tok = self._advance()
        expr = self._parse_expression()
        await_expr = AwaitExpression(expression=expr, line=tok.line, col=tok.col)
        return ExpressionStatement(expression=await_expr)

    def _parse_for_await_loop(self) -> ForAwaitLoop:
        """for await each item in async_iterable: body"""
        tok = self._advance()  # consume 'for'
        self._advance()  # consume 'await'
        if self._match(TokenType.EACH):
            self._advance()
        var_name = self._consume(TokenType.IDENTIFIER, "Expected variable name").value
        self._consume(TokenType.IN, "Expected 'in'")
        iterable = self._parse_expression()
        body = self._parse_block()
        return ForAwaitLoop(variable=var_name, iterable=iterable, body=body, line=tok.line, col=tok.col)

    def _parse_interface_definition(self) -> InterfaceDefinition:
        """define interface Name [inherits from Parent]: body"""
        tok = self._advance()  # consume 'define'
        self._consume(TokenType.INTERFACE, "Expected 'interface'")
        name = self._consume(TokenType.IDENTIFIER, "Expected interface name").value
        parent = None
        if self._match(TokenType.INHERITS):
            self._advance()
            self._consume(TokenType.FROM, "Expected 'from' after 'inherits'")
            parent = self._parse_name_token()
        body = self._parse_block()
        return InterfaceDefinition(name=name, parent=parent, body=body, line=tok.line, col=tok.col)

    def _parse_type_name(self) -> str:
        """Parse a type name like int, string, float, List<int>, string|int, int?, etc."""
        type_name = self._parse_name_token()
        
        # Handle optional types: int?
        if self._check(TokenType.QUESTION):
            self._advance()
            return f"Optional[{type_name}]"
        
        # Handle generic types like List<int>
        if self._check(TokenType.LESS):
            self._advance()
            inner = self._parse_type_name()
            self._consume(TokenType.GREATER, "Expected '>'")
            type_name = f"{type_name}[{inner}]"
        
        # Handle union types: string | int
        if self._check(TokenType.PIPE) and self._current().value != "|>":
            self._advance()
            right = self._parse_type_name()
            return f"Union[{type_name}, {right}]"
        
        return type_name

    def _parse_generic_params(self) -> List[str]:
        """Parse generic type parameters like <T, U, V>."""
        self._consume(TokenType.LESS, "Expected '<'")
        params = []
        while True:
            name = self._consume(TokenType.IDENTIFIER, "Expected type parameter name").value
            params.append(name)
            if not self._match(TokenType.COMMA):
                break
            self._advance()
        self._consume(TokenType.GREATER, "Expected '>'")
        return params

    # ---- v0.5.0 Masterpiece Edition Parsers ----

    def _parse_lazy_declaration(self) -> LazyDeclaration:
        """lazy let x be expensive_computation()"""
        tok = self._advance()  # consume 'lazy'
        self._consume(TokenType.LET, "Expected 'let' after 'lazy'")
        type_annotation = None
        name = self._parse_name_token()
        if self._match(TokenType.COLON):
            self._advance()
            type_name = self._parse_type_name()
            type_annotation = TypeAnnotation(type_name=type_name, line=tok.line, col=tok.col)
        self._consume(TokenType.BE, "Expected 'be'")
        value = self._parse_expression()
        return LazyDeclaration(name=name, value=value, type_annotation=type_annotation, line=tok.line, col=tok.col)

    def _parse_record_definition(self) -> RecordDefinition:
        """define record Name with field: type, field2: type"""
        tok = self._advance()  # consume 'define'
        self._consume(TokenType.RECORD, "Expected 'record'")
        name = self._consume(TokenType.IDENTIFIER, "Expected record name").value
        
        generics = []
        if self._check(TokenType.LESS):
            generics = self._parse_generic_params()
        
        fields = []
        if self._match(TokenType.WITH):
            self._advance()
            while True:
                fname = self._consume(TokenType.IDENTIFIER, "Expected field name").value
                ftype = "any"
                fdefault = None
                if self._match(TokenType.COLON):
                    self._advance()
                    ftype = self._parse_type_name()
                if self._match(TokenType.EQUAL):
                    self._advance()
                    fdefault = self._parse_expression()
                fields.append((fname, ftype, fdefault))
                if not self._match(TokenType.COMMA):
                    break
                self._advance()
        
        return RecordDefinition(name=name, fields=fields, generics=generics, line=tok.line, col=tok.col)

    def _parse_property_definition(self) -> PropertyDefinition:
        """define property name [with get: body; set with param: body]"""
        tok = self._advance()  # consume 'define'
        self._consume(TokenType.PROPERTY, "Expected 'property'")
        name = self._consume(TokenType.IDENTIFIER, "Expected property name").value
        
        type_annotation = None
        if self._match(TokenType.COLON):
            self._advance()
            type_name = self._parse_type_name()
            type_annotation = TypeAnnotation(type_name=type_name, line=tok.line, col=tok.col)
        
        getter_body = []
        setter_body = []
        setter_param = "value"
        
        if self._match(TokenType.WITH):
            self._advance()
            if self._match(TokenType.GET):
                self._advance()
                getter_body = self._parse_block()
            
            if self._check(TokenType.SET) or (self._check(TokenType.IDENTIFIER) and self._current().value == "setter"):
                if self._check(TokenType.IDENTIFIER):
                    self._advance()  # consume 'setter'
                else:
                    self._advance()  # consume 'set'
                if self._match(TokenType.WITH):
                    self._advance()
                    setter_param = self._consume(TokenType.IDENTIFIER, "Expected parameter name").value
                    self._consume(TokenType.COLON, "Expected ':' after set param")
                    setter_body = self._parse_block_contents()
        
        return PropertyDefinition(name=name, type_annotation=type_annotation,
                                  getter_body=getter_body, setter_body=setter_body,
                                  setter_param=setter_param, line=tok.line, col=tok.col)

    def _parse_namespace_definition(self) -> NamespaceDefinition:
        """define namespace Name: body"""
        tok = self._advance()  # consume 'define'
        self._consume(TokenType.NAMESPACE, "Expected 'namespace'")
        name = self._consume(TokenType.IDENTIFIER, "Expected namespace name").value
        body = self._parse_block()
        return NamespaceDefinition(name=name, body=body, line=tok.line, col=tok.col)

    def _parse_extension_definition(self) -> ExtensionDefinition:
        """define extension on TypeName: body"""
        tok = self._advance()  # consume 'define'
        self._consume(TokenType.EXTENSION, "Expected 'extension'")
        self._consume(TokenType.IDENTIFIER, "Expected 'on'", value="on")
        target = self._parse_name_token()
        body = self._parse_block()
        return ExtensionDefinition(target_type=target, body=body, line=tok.line, col=tok.col)

    # ---- v0.5.1 Functional Statement Parsers ----

    def _parse_map_statement(self) -> ExpressionStatement:
        """map items using func"""
        tok = self._advance()  # consume 'map'
        items = self._parse_expression()
        # Skip optional filler: 'to', variable names, 'using'
        while not self._is_at_statement_end() and self._check_any(TokenType.TO, TokenType.IDENTIFIER, TokenType.USING):
            if self._match(TokenType.USING):
                self._advance()
                break
            self._advance()  # skip 'to', variable names, etc.
        func = self._parse_expression()
        return ExpressionStatement(expression=Call(callee=Identifier(name="map"), arguments=[func, items]), line=tok.line, col=tok.col)

    def _parse_filter_statement(self) -> ExpressionStatement:
        """filter items where condition / keep items where condition"""
        tok = self._advance()  # consume 'filter'/'keep'
        items = self._parse_expression()
        # Skip optional filler words until 'where', newline, or dedent
        while not self._is_at_statement_end() and not self._check(TokenType.WHERE):
            if self._check_any(TokenType.IDENTIFIER, TokenType.FROM):
                self._advance()  # skip 'keeping', variable names, 'from'
            else:
                break
        if self._match(TokenType.WHERE):
            self._advance()
        condition = self._parse_expression()
        return ExpressionStatement(expression=Call(callee=Identifier(name="filter"), arguments=[condition, items]), line=tok.line, col=tok.col)

    def _parse_reduce_statement(self) -> ExpressionStatement:
        """fold/combine items using func starting with initial"""
        tok = self._advance()  # consume 'fold'/'combine'
        items = self._parse_expression()
        func = None
        initial = Literal(value=0, line=tok.line, col=tok.col)
        if self._match(TokenType.USING):
            self._advance()
            # Parse func with high precedence to stop BEFORE comparison operators
            # (avoids 'add starting with' being parsed as add.startswith())
            func = self._parse_expression(self.PREC_COMPARISON + 1)
        # Skip filler words until we find the initial value expression
        while not self._is_at_statement_end():
            marker = self._current()
            if marker.type in (TokenType.IDENTIFIER, TokenType.WITH, TokenType.FROM, TokenType.STARTS_WITH, TokenType.BEGINS_WITH):
                self._advance()
            else:
                break
        if not self._is_at_statement_end():
            initial = self._parse_expression()
        if func is None:
            func = items
        return ExpressionStatement(expression=Call(callee=Identifier(name="reduce"), arguments=[func, items, initial]), line=tok.line, col=tok.col)

    def _parse_search_statement(self) -> ExpressionStatement:
        """search for pattern in text (multi-word 'search for' already consumed by lexer)"""
        tok = self._advance()  # consume 'search' or 'find'/'search for'/'look for'
        # Parse pattern with high precedence so IN is NOT consumed as infix operator
        pattern = self._parse_expression(self.PREC_COMPARISON)
        if self._match(TokenType.IN):
            self._advance()
        text = self._parse_expression()
        return ExpressionStatement(expression=Call(callee=Attribute(object=text, attribute="find"), arguments=[pattern]), line=tok.line, col=tok.col)

    def _parse_replace_statement(self) -> ExpressionStatement:
        """replace old in text with new"""
        tok = self._advance()  # consume 'replace'/'substitute'
        # Parse pattern with high precedence so IN is NOT consumed as infix operator
        pattern = self._parse_expression(self.PREC_COMPARISON)
        if self._match(TokenType.IN):
            self._advance()
        text = self._parse_expression()
        # Skip any identifiers before 'with' (like 'world' in 'hello world')
        while not self._is_at_statement_end() and not self._check(TokenType.WITH):
            if self._check(TokenType.IDENTIFIER):
                self._advance()
            else:
                break
        self._consume(TokenType.WITH, "Expected 'with'")
        replacement = self._parse_expression()
        return ExpressionStatement(expression=Call(callee=Attribute(object=text, attribute="replace"), arguments=[pattern, replacement]), line=tok.line, col=tok.col)

    def _parse_transform_statement(self) -> ExpressionStatement:
        """transform each x in items using func"""
        tok = self._advance()  # consume 'transform'
        # Skip optional 'each var in'
        if self._match(TokenType.EACH):
            self._advance()
            if self._check(TokenType.IDENTIFIER):
                self._advance()  # skip variable name
            if self._match(TokenType.IN):
                self._advance()
        items = self._parse_expression()
        if self._match(TokenType.USING):
            self._advance()
        func = self._parse_expression()
        return ExpressionStatement(expression=Call(callee=Identifier(name="map"), arguments=[func, items]), line=tok.line, col=tok.col)

    def _parse_count_statement(self) -> ExpressionStatement:
        """count occurrences of item in collection (multi-word keyword already consumed)"""
        tok = self._advance()  # consume 'count occurrences' or 'total occurrences'
        # Skip 'of' if present
        if self._check(TokenType.IDENTIFIER) and self._current().value == "of":
            self._advance()
        # Parse item with high precedence so IN is NOT consumed as infix operator
        item = self._parse_expression(self.PREC_COMPARISON)
        if self._match(TokenType.IN):
            self._advance()
        collection = self._parse_expression()
        return ExpressionStatement(
            expression=Call(callee=Attribute(object=collection, attribute="count"), arguments=[item]),
            line=tok.line, col=tok.col)

    def _parse_class_definition(self) -> ClassDefinition:
        tok = self._advance()
        self._consume(TokenType.CLASS, "Expected 'class'")
        name = self._parse_name_token()
        
        generics = []
        if self._check(TokenType.LESS):
            generics = self._parse_generic_params()
        
        parent = None
        if self._match(TokenType.INHERITS):
            self._advance()
            if not self._match(TokenType.FROM):
                parent = self.tokens[self.pos - 1].value if self.tokens[self.pos - 1].type == TokenType.IDENTIFIER else None
                if parent is None:
                    parent = self._parse_name_token()
            else:
                self._advance()  # consume 'from'
                parent = self._parse_name_token()
        
        implements = []
        if self._match(TokenType.IMPLEMENTS):
            self._advance()
            while True:
                iface = self._consume(TokenType.IDENTIFIER, "Expected interface name").value
                implements.append(iface)
                if not self._match(TokenType.COMMA):
                    break
                self._advance()
        
        body = self._parse_block()
        return ClassDefinition(name=name, parent=parent, body=body, generics=generics, implements=implements, line=tok.line, col=tok.col)

    # ========== v0.9.1 Universal Polyglot Parser Methods ==========

    def _parse_go_statement(self) -> GoStatement:
        """goroutine name: body / spin up worker: body"""
        tok = self._advance()
        name = None
        if self._check(TokenType.IDENTIFIER):
            name = self._advance().value
        arguments = []
        if self._match(TokenType.WITH):
            self._advance()
            while not self._check_any(TokenType.COLON, TokenType.NEWLINE, TokenType.EOF):
                arguments.append(self._parse_expression())
                if not self._match(TokenType.COMMA):
                    break
                self._advance()
        body = self._parse_block()
        return GoStatement(name=name, body=body, arguments=arguments, line=tok.line, col=tok.col)

    def _parse_channel_declaration(self) -> ChannelDeclaration:
        """create channel of Type [with capacity N] [called name]"""
        tok = self._advance()
        # The lexer may have consumed "create channel" as a single CHANNEL token.
        # Check if "of" follows; if not, consume it.
        if self._check(TokenType.IDENTIFIER) and self._current().value == "of":
            self._advance()
        ch_type = self._parse_name_token()  # Use _parse_name_token since type names may be keyword tokens
        capacity = None
        if self._match(TokenType.WITH):
            self._advance()
            if self._check(TokenType.IDENTIFIER) and self._current().value == "capacity":
                self._advance()
            capacity_tok = self._consume(TokenType.INTEGER, "Expected capacity number")
            capacity = int(capacity_tok.value)
        name = "ch"
        if self._match(TokenType.CALLED):
            self._advance()
            name = self._consume(TokenType.IDENTIFIER, "Expected channel name").value
        return ChannelDeclaration(name=name, channel_type=ch_type, capacity=capacity, line=tok.line, col=tok.col)

    def _parse_channel_send(self) -> ChannelSend:
        """send value through channel"""
        tok = self._advance()  # consume SEND token (lexer may have consumed "through" already as part of multi-word token)
        value = self._parse_expression()
        # The word "through"/"to" may or may not have been consumed by the lexer as part of a multi-word SEND token.
        # Check if the next token is the channel name or a connector word.
        if not self._is_at_statement_end() and self._check_any(TokenType.IDENTIFIER, TokenType.CHANNEL):
            connector = self._current()
            if connector.value in ("through", "to", "onto"):
                self._advance()  # skip connector
        channel = self._consume(TokenType.IDENTIFIER, "Expected channel name").value
        return ChannelSend(value=value, channel=channel, line=tok.line, col=tok.col)

    def _parse_channel_receive(self) -> ChannelReceive:
        """listen to channel with var: body / receive from channel"""
        tok = self._advance()  # consume RECEIVE token (may be multi-word like "listen to")
        # The connector word may already be in the consumed token.
        # Skip optional connector like "from", "to", "on" if present.
        if not self._is_at_statement_end() and self._check_any(TokenType.IDENTIFIER, TokenType.FROM):
            connector = self._current()
            if connector.value in ("to", "from", "on"):
                self._advance()
        channel = self._consume(TokenType.IDENTIFIER, "Expected channel name").value
        variable = None
        body = []
        if self._match(TokenType.WITH):
            self._advance()
            variable = self._consume(TokenType.IDENTIFIER, "Expected variable name").value
            body = self._parse_block()
            return ChannelReceive(channel=channel, variable=variable, body=body, is_range=True, line=tok.line, col=tok.col)
        return ChannelReceive(channel=channel, variable=variable, line=tok.line, col=tok.col)

    def _parse_channel_close(self) -> ChannelClose:
        """close channel / shut channel"""
        tok = self._advance()
        channel = self._consume(TokenType.IDENTIFIER, "Expected channel name").value
        return ChannelClose(channel=channel, line=tok.line, col=tok.col)

    def _parse_channel_select(self) -> ChannelSelect:
        """select: case msg from ch: body [timeout: body] [default: body]"""
        tok = self._advance()
        self._skip_newlines()
        self._consume(TokenType.COLON, "Expected ':' after 'select'")
        self._skip_newlines()
        self._consume(TokenType.INDENT, "Expected indented block after select")
        cases = []
        default_body = []
        timeout = None
        while not self._check_any(TokenType.DEDENT, TokenType.EOF):
            self._skip_newlines()
            if self._check(TokenType.DEFAULT):
                self._advance()
                self._consume(TokenType.COLON, "Expected ':' after 'default'")
                default_body = self._parse_block_contents()
                break
            if self._check(TokenType.CASE):
                self._advance()
                var_name = None
                if self._check(TokenType.IDENTIFIER):
                    var_name = self._advance().value
                if self._match(TokenType.FROM):
                    self._advance()
                channel = self._consume(TokenType.IDENTIFIER, "Expected channel name").value
                self._consume(TokenType.COLON, "Expected ':'")
                case_body = self._parse_block_contents()
                cases.append((channel, var_name, case_body))
            elif self._check(TokenType.IDENTIFIER) and self._current().value in ("after", "timeout"):
                self._advance()
                timeout = self._parse_expression()
                self._consume(TokenType.COLON, "Expected ':'")
                # Parse timeout body (optional)
                if not self._check_any(TokenType.DEDENT, TokenType.EOF):
                    self._parse_block_contents()
                break
            else:
                # Unknown select clause, skip
                self._advance()
        if self._check(TokenType.DEDENT):
            self._advance()
        return ChannelSelect(cases=cases, default_body=default_body, timeout=timeout, line=tok.line, col=tok.col)

    def _parse_multi_return(self) -> MultiReturnStatement:
        """return multiple values: a, b, c"""
        tok = self._advance()
        values = []
        while not self._is_at_statement_end():
            values.append(self._parse_expression())
            if not self._match(TokenType.COMMA):
                break
            self._advance()
        return MultiReturnStatement(values=values, line=tok.line, col=tok.col)

    def _parse_yield_from(self) -> YieldFromStatement:
        """yield from iterable / yield all from iterable"""
        tok = self._advance()
        if self._check(TokenType.IDENTIFIER) and self._current().value in ("all", "each"):
            self._advance()
        iterable = self._parse_expression()
        return YieldFromStatement(iterable=iterable, line=tok.line, col=tok.col)

    def _parse_global_statement(self) -> GlobalStatement:
        """global x, y, z"""
        tok = self._advance()
        names = self._parse_comma_separated_idents()
        return GlobalStatement(names=names, line=tok.line, col=tok.col)

    def _parse_nonlocal_statement(self) -> NonlocalStatement:
        """nonlocal x / outer variable x"""
        tok = self._advance()
        names = self._parse_comma_separated_idents()
        return NonlocalStatement(names=names, line=tok.line, col=tok.col)

    def _parse_async_with(self) -> AsyncWithStatement:
        """async with resource as var: body"""
        tok = self._advance()
        resource = self._parse_expression()
        variable = None
        if self._match(TokenType.AS):
            self._advance()
            variable = self._consume(TokenType.IDENTIFIER).value
        body = self._parse_block()
        return AsyncWithStatement(resource=resource, variable=variable, body=body, line=tok.line, col=tok.col)

    def _parse_module_definition(self) -> ModuleDefinition:
        """define module Name: body"""
        tok = self._advance()
        name = self._consume(TokenType.IDENTIFIER, "Expected module name").value
        body = self._parse_block()
        return ModuleDefinition(name=name, body=body, line=tok.line, col=tok.col)

    def _parse_mixin_statement(self) -> MixinStatement:
        """include Module / extend Module / mix in Module"""
        tok = self._advance()
        mixin_type = tok.value  # "include", "extend", "prepend", "mix"
        if mixin_type == "mix":
            self._consume(TokenType.IDENTIFIER, "Expected 'in'", value="in")
            mixin_type = "include"
        name = self._consume(TokenType.IDENTIFIER, "Expected module name").value
        return MixinStatement(mixin_name=name, mixin_type=mixin_type, line=tok.line, col=tok.col)

    def _parse_object_definition(self) -> ObjectDefinition:
        """define object Name [companion]: body"""
        tok = self._advance()
        is_companion = False
        if self._match(TokenType.COMPANION):
            is_companion = True
            self._advance()
        name = self._consume(TokenType.IDENTIFIER, "Expected object name").value
        body = self._parse_block()
        return ObjectDefinition(name=name, body=body, is_companion=is_companion, line=tok.line, col=tok.col)

    def _parse_actor_definition(self) -> ActorDefinition:
        """define actor Name: body"""
        tok = self._advance()
        name = self._consume(TokenType.IDENTIFIER, "Expected actor name").value
        body = self._parse_block()
        return ActorDefinition(name=name, body=body, line=tok.line, col=tok.col)

    def _parse_sealed_class_definition(self) -> SealedClassDefinition:
        """define sealed class Name: body"""
        tok = self._advance()
        if self._match(TokenType.CLASS):
            self._advance()
        name = self._consume(TokenType.IDENTIFIER, "Expected class name").value
        body = self._parse_block()
        return SealedClassDefinition(name=name, body=body, line=tok.line, col=tok.col)

    def _parse_suspend_function(self) -> SuspendFunction:
        """suspend function name with params: body"""
        tok = self._advance()
        self._consume(TokenType.FUNCTION, "Expected 'function'")
        func_def = self._parse_function_definition(from_tok=tok)
        return SuspendFunction(declaration=func_def, line=tok.line, col=tok.col)

    def _parse_package_declaration(self) -> PackageDeclaration:
        """package com.example.app"""
        tok = self._advance()
        parts = []
        while not self._is_at_statement_end():
            p = self._consume(TokenType.IDENTIFIER, "Expected package path component").value
            parts.append(p)
            if not self._match(TokenType.DOT):
                break
            self._advance()
        return PackageDeclaration(package_path=".".join(parts), line=tok.line, col=tok.col)

    def _parse_native_declaration(self) -> NativeDeclaration:
        """native function name with params -> Type / extern function name"""
        tok = self._advance()
        self._consume(TokenType.FUNCTION, "Expected 'function'")
        name = self._consume(TokenType.IDENTIFIER, "Expected function name").value
        params = []
        if self._match(TokenType.WITH):
            self._advance()
            while not self._check_any(TokenType.COLON, TokenType.NEWLINE, TokenType.ARROW, TokenType.EOF):
                pname = self._consume(TokenType.IDENTIFIER, "Expected parameter name").value
                ptype = "any"
                if self._match(TokenType.COLON):
                    self._advance()
                    ptype = self._parse_type_name()
                params.append((pname, ptype))
                if not self._match(TokenType.COMMA):
                    break
                self._advance()
        return_type = None
        if self._match(TokenType.ARROW):
            self._advance()
            return_type = self._parse_type_name()
        return NativeDeclaration(name=name, parameters=params, return_type=return_type, line=tok.line, col=tok.col)

    def _parse_synchronized_block(self) -> SynchronizedBlock:
        """synchronized [on lock]: body"""
        tok = self._advance()
        lock = None
        if self._match(TokenType.IDENTIFIER) and self._current().value == "on":
            self._advance()
            lock = self._consume(TokenType.IDENTIFIER, "Expected lock object").value
        body = self._parse_block()
        return SynchronizedBlock(lock_object=lock, body=body, line=tok.line, col=tok.col)

    def _parse_data_class_definition(self) -> ClassDefinition:
        """data class Name: body -> define class with data semantics"""
        tok = self._advance()
        self._consume(TokenType.CLASS, "Expected 'class'")
        name = self._consume(TokenType.IDENTIFIER, "Expected class name").value
        body = self._parse_block()
        return ClassDefinition(name=name, body=body, line=tok.line, col=tok.col)

    def _parse_delegate_definition(self) -> DelegateDefinition:
        """delegate Name with params -> ReturnType"""
        tok = self._advance()
        name = self._consume(TokenType.IDENTIFIER, "Expected delegate name").value
        params = []
        if self._match(TokenType.WITH):
            self._advance()
            while not self._check_any(TokenType.ARROW, TokenType.NEWLINE, TokenType.EOF):
                pname = self._consume(TokenType.IDENTIFIER, "Expected param name").value
                ptype = "any"
                if self._match(TokenType.COLON):
                    self._advance()
                    ptype = self._parse_type_name()
                params.append((pname, ptype))
                if not self._match(TokenType.COMMA):
                    break
                self._advance()
        return_type = None
        if self._match(TokenType.ARROW):
            self._advance()
            return_type = self._parse_type_name()
        return DelegateDefinition(name=name, parameters=params, return_type=return_type, line=tok.line, col=tok.col)

    def _parse_event_declaration(self) -> EventDeclaration:
        """event Name with DelegateType"""
        tok = self._advance()
        name = self._consume(TokenType.IDENTIFIER, "Expected event name").value
        delegate_type = None
        if self._match(TokenType.WITH):
            self._advance()
            delegate_type = self._consume(TokenType.IDENTIFIER, "Expected delegate type").value
        return EventDeclaration(name=name, delegate_type=delegate_type, line=tok.line, col=tok.col)

    def _parse_partial_class_definition(self) -> PartialClassDefinition:
        """partial class Name: body"""
        tok = self._advance()
        self._consume(TokenType.CLASS, "Expected 'class'")
        name = self._consume(TokenType.IDENTIFIER, "Expected class name").value
        body = self._parse_block()
        return PartialClassDefinition(name=name, body=body, line=tok.line, col=tok.col)

    def _parse_macro_definition(self) -> MacroDefinition:
        """macro name with args: body"""
        tok = self._advance()
        name = self._consume(TokenType.IDENTIFIER, "Expected macro name").value
        params = []
        if self._match(TokenType.WITH):
            self._advance()
            while not self._check_any(TokenType.COLON, TokenType.NEWLINE, TokenType.EOF):
                p = self._consume(TokenType.IDENTIFIER, "Expected param name").value
                params.append(p)
                if not self._match(TokenType.COMMA):
                    break
                self._advance()
        body = self._parse_block()
        return MacroDefinition(name=name, parameters=params, body=body, line=tok.line, col=tok.col)

    def _parse_comma_separated_idents(self) -> List[str]:
        """Parse comma-separated identifier list like 'x, y, z'."""
        items = []
        while not self._is_at_statement_end():
            items.append(self._parse_name_token())
            if not self._match(TokenType.COMMA):
                break
            self._advance()
        return items

    # ---- Expression Parsing (Pratt) ----

    PREC_ASSIGNMENT = 1
    PREC_TERNARY = 2
    PREC_OR = 3
    PREC_AND = 4
    PREC_BITWISE = 5
    PREC_EQUALITY = 6
    PREC_COMPARISON = 7
    PREC_SUM = 8
    PREC_PRODUCT = 9
    PREC_POWER = 10
    PREC_UNARY = 11
    PREC_CALL = 12
    PREC_PRIMARY = 13

    def _get_prefix_precedence(self, token_type: TokenType) -> int:
        if token_type in (TokenType.MINUS, TokenType.NOT, TokenType.DOT_DOT_DOT):
            return self.PREC_UNARY
        return 0

    def _get_infix_precedence(self, token_type: TokenType) -> int:
        pre_map = {
            TokenType.QUESTION_QUESTION: self.PREC_OR,
            TokenType.PLUS: self.PREC_SUM, TokenType.MINUS: self.PREC_SUM,
            TokenType.STAR: self.PREC_PRODUCT, TokenType.SLASH: self.PREC_PRODUCT,
            TokenType.SLASH_SLASH: self.PREC_PRODUCT, TokenType.PERCENT: self.PREC_PRODUCT,
            TokenType.CARET: self.PREC_POWER,
            TokenType.AMPERSAND: self.PREC_BITWISE, TokenType.PIPE: self.PREC_BITWISE,
            TokenType.PIPE_OP: self.PREC_BITWISE,
            TokenType.LESS_LESS: self.PREC_BITWISE, TokenType.GREATER_GREATER: self.PREC_BITWISE,
            TokenType.EQUAL_EQUAL: self.PREC_EQUALITY, TokenType.BANG_EQUAL: self.PREC_EQUALITY,
            TokenType.LESS: self.PREC_COMPARISON, TokenType.GREATER: self.PREC_COMPARISON,
            TokenType.LESS_EQUAL: self.PREC_COMPARISON, TokenType.GREATER_EQUAL: self.PREC_COMPARISON,
            TokenType.IN: self.PREC_COMPARISON, TokenType.NOT_IN: self.PREC_COMPARISON,
            TokenType.IS: self.PREC_COMPARISON,
            TokenType.XOR: self.PREC_AND,
            TokenType.AND: self.PREC_AND, TokenType.OR: self.PREC_OR,
            TokenType.HAS: self.PREC_COMPARISON,
            TokenType.HAS_NO: self.PREC_COMPARISON,
            TokenType.INCLUDES: self.PREC_COMPARISON,
            TokenType.EXCLUDES: self.PREC_COMPARISON,
            TokenType.SAME: self.PREC_COMPARISON,
            TokenType.IS_SAME_AS: self.PREC_COMPARISON,
            TokenType.CONTAINS: self.PREC_COMPARISON,
            TokenType.STARTS_WITH: self.PREC_COMPARISON,
            TokenType.ENDS_WITH: self.PREC_COMPARISON,
            TokenType.BETWEEN: self.PREC_COMPARISON,
            TokenType.DOT: self.PREC_CALL, TokenType.LPAREN: self.PREC_CALL,
            TokenType.LBRACKET: self.PREC_CALL,
        }
        return pre_map.get(token_type, 0)

    def _parse_expression(self, precedence: int = 0) -> ASTNode:
        self._skip_articles()
        token = self._current()
        prefix_prec = self._get_prefix_precedence(token.type)

        if prefix_prec == 0:
            left = self._parse_primary()
        else:
            op_token = self._advance()
            if op_token.type == TokenType.DOT_DOT_DOT:
                # Spread element
                operand = self._parse_expression(prefix_prec)
                left = SpreadElement(expression=operand, line=op_token.line, col=op_token.col)
            else:
                right = self._parse_expression(prefix_prec)
                op = "neg" if op_token.type == TokenType.MINUS else op_token.value
                left = UnaryOp(operator=op, operand=right, line=op_token.line, col=op_token.col)

        while True:
            token = self._current()
            infix_prec = self._get_infix_precedence(token.type)
            if infix_prec <= precedence:
                break

            if token.type == TokenType.DOT:
                self._advance()
                if not self._is_name_token(self._current().type):
                    raise ParseError("Expected attribute name after '.'", self._current())
                attr_name = self._parse_name_token()
                left = Attribute(object=left, attribute=attr_name, line=token.line, col=token.col)
                continue

            if token.type == TokenType.LPAREN:
                left = self._parse_call_suffix(left)
                continue

            if token.type == TokenType.LBRACKET:
                self._advance()
                index_expr = self._parse_expression()
                # Check for slice: obj[start:end] or obj[:end] or obj[start:]
                if self._check(TokenType.COLON):
                    self._advance()  # consume ':'
                    end_expr = self._parse_expression() if not self._check(TokenType.RBRACKET) else None
                    self._consume(TokenType.RBRACKET, "Expected ']'")
                    left = SliceExpression(
                        object=left,
                        start=index_expr,
                        end=end_expr,
                        line=token.line, col=token.col
                    )
                    continue
                self._consume(TokenType.RBRACKET, "Expected ']'")
                left = Index(object=left, index=index_expr, line=token.line, col=token.col)
                continue

            op_token = self._advance()
            op_symbols = {
                TokenType.EQUAL_EQUAL: "==", TokenType.BANG_EQUAL: "!=",
                TokenType.LESS: "<", TokenType.GREATER: ">",
                TokenType.LESS_EQUAL: "<=", TokenType.GREATER_EQUAL: ">=",
                TokenType.XOR: "xor",
                TokenType.AND: "and", TokenType.OR: "or",
                TokenType.HAS: "has",
                TokenType.HAS_NO: "has no",
                TokenType.INCLUDES: "includes",
                TokenType.EXCLUDES: "excludes",
                TokenType.SAME: "is same as",
                TokenType.IS_SAME_AS: "is same as",
                TokenType.CONTAINS: "contains",
                TokenType.STARTS_WITH: "starts with",
                TokenType.ENDS_WITH: "ends with",
                TokenType.PLUS: "+", TokenType.MINUS: "-",
                TokenType.STAR: "*", TokenType.SLASH: "/",
                TokenType.SLASH_SLASH: "//", TokenType.PERCENT: "%",
                TokenType.CARET: "^",
                TokenType.AMPERSAND: "&", TokenType.PIPE: "|",
                TokenType.PIPE_OP: "|>",
                TokenType.LESS_LESS: "<<", TokenType.GREATER_GREATER: ">>",
                TokenType.QUESTION_QUESTION: "??",
                TokenType.IN: "in", TokenType.NOT_IN: "not in",
                TokenType.IS: "is",
            }
            op_value = op_symbols.get(op_token.type, op_token.value)

            # Type casting: x as int
            if op_token.type == TokenType.AS:
                type_expr = self._parse_expression(infix_prec)
                if isinstance(type_expr, Identifier):
                    left = CastExpression(expression=left, target_type=type_expr.name, line=op_token.line, col=op_token.col)
                    continue

            # Special handling for 'is empty': list is empty -> len(list) == 0
            if op_token.type == TokenType.IS and self._check(TokenType.EMPTY):
                self._advance()  # consume EMPTY
                left = EmptyExpression(expression=left, line=op_token.line, col=op_token.col)
                continue

            # Special handling for 'is not empty' via BANG_EQUAL (lexer combines 'is not')
            if op_token.type == TokenType.BANG_EQUAL and self._check(TokenType.EMPTY):
                self._advance()  # consume EMPTY
                empty_node = EmptyExpression(expression=left, line=op_token.line, col=op_token.col)
                left = UnaryOp(operator="not", operand=empty_node, line=op_token.line, col=op_token.col)
                continue

            # Special handling for 'is not empty' (if 'is' and 'not' are separate tokens)
            if op_token.type == TokenType.IS and self._check(TokenType.NOT):
                self._advance()  # consume NOT
                if self._check(TokenType.EMPTY):
                    self._advance()  # consume EMPTY
                    not_node = EmptyExpression(expression=left, line=op_token.line, col=op_token.col)
                    left = UnaryOp(operator="not", operand=not_node, line=op_token.line, col=op_token.col)
                    continue

            # Special handling for 'between': x between a and b
            if op_token.type == TokenType.BETWEEN:
                lower = self._parse_expression(infix_prec)
                self._consume(TokenType.AND, "Expected 'and' after between lower bound")
                upper = self._parse_expression(infix_prec)
                left = BetweenExpression(left=left, lower=lower, upper=upper, line=op_token.line, col=op_token.col)
                continue

            # Special handling for 'is a <type>' type checks: x is a string -> isinstance(x, str)
            if op_token.type == TokenType.IS:
                # Check if next token(s) form a type reference
                nxt = self._current()
                if nxt.type in (TokenType.INTEGER_TYPE, TokenType.FLOAT_TYPE, TokenType.STRING_TYPE,
                                TokenType.BOOLEAN_TYPE, TokenType.LIST_TYPE, TokenType.DICT_TYPE,
                                TokenType.ANY_TYPE):
                    type_node = self._parse_primary()  # consumes the type keyword
                    left = IsExpression(left=left, right=type_node, line=op_token.line, col=op_token.col)
                    continue

            right = self._parse_expression(infix_prec)
            left = BinaryOp(left=left, operator=op_value, right=right, line=op_token.line, col=op_token.col)

        # Ternary: value if condition else/otherwise/or other
        if self._allow_ternary and self._match(TokenType.IF):
            self._advance()  # consume 'if'
            condition = self._parse_expression(self.PREC_TERNARY)
            # Consume the else keyword: 'else', 'otherwise', or 'or'
            if self._check_any(TokenType.ELSE, TokenType.OR, TokenType.OTHERWISE):
                self._advance()
            else:
                raise ParseError("Expected 'else', 'or', or 'otherwise' in ternary", self._current())
            false_value = self._parse_expression(self.PREC_TERNARY)
            left = Ternary(condition=condition, true_value=left,
                           false_value=false_value,
                           line=left.line, col=left.col)

        return left

    def _parse_call_suffix(self, callee: ASTNode) -> Call:
        self._advance()  # consume '('
        args = []
        if not self._check(TokenType.RPAREN):
            args = self._parse_argument_list()
        tok = self._consume(TokenType.RPAREN, "Expected ')'")
        return Call(callee=callee, arguments=args, line=tok.line, col=tok.col)

    def _parse_argument_list(self) -> List[ASTNode]:
        args = []
        while True:
            # Check for keyword argument: name = value
            if self._check(TokenType.IDENTIFIER) and self._peek().type == TokenType.EQUAL:
                name = self._advance().value
                self._advance()  # consume '='
                value = self._parse_expression()
                args.append(KeywordArgument(name=name, value=value))
            elif self._check(TokenType.DOT_DOT_DOT):
                self._advance()
                expr = self._parse_expression()
                args.append(SpreadElement(expression=expr))
            else:
                # Check if this is a generator expression: for each x in items
                # We parse an expression first, then check if 'for' follows
                arg = self._parse_expression()
                if self._check(TokenType.FOR):
                    self._advance()
                    if self._match(TokenType.EACH):
                        self._advance()
                    variable = self._consume(TokenType.IDENTIFIER, "Expected variable in generator").value
                    self._consume(TokenType.IN, "Expected 'in' in generator")
                    old_ternary = self._allow_ternary
                    self._allow_ternary = False
                    iterable = self._parse_expression()
                    self._allow_ternary = old_ternary
                    condition = None
                    if self._match(TokenType.IF):
                        self._advance()
                        condition = self._parse_expression()
                    elif self._match(TokenType.WHERE):
                        self._advance()
                        condition = self._parse_expression()
                    arg = GeneratorExpression(
                        expression=arg, variable=variable,
                        iterable=iterable, condition=condition,
                        line=arg.line, col=arg.col
                    )
                args.append(arg)

            if not self._match(TokenType.COMMA):
                break
            self._advance()
        return args

    def _parse_primary(self) -> ASTNode:
        token = self._current()

        if token.type == TokenType.INTEGER:
            self._advance(); return Literal(value=token.value, line=token.line, col=token.col)
        if token.type == TokenType.FLOAT:
            self._advance(); return Literal(value=token.value, line=token.line, col=token.col)
        if token.type == TokenType.STRING:
            self._advance(); return Literal(value=token.value, line=token.line, col=token.col)
        if token.type == TokenType.BOOLEAN:
            self._advance()
            # Map English boolean words to actual True/False
            truthy = {"true", "yes", "yup", "definitely", "absolutely", "certainly", "surely",
                      "indeed", "positively", "affirmative", "yeah", "yep", "on", "enabled",
                      "ok", "okay", "alright", "fine", "good"}
            falsey = {"false", "no", "nope", "negative", "never", "nada", "nah", "off", "disabled",
                      "bad", "not ok", "not okay", "not good", "not fine"}
            if token.value in truthy:
                return Literal(value=True, line=token.line, col=token.col)
            elif token.value in falsey:
                return Literal(value=False, line=token.line, col=token.col)
            else:
                return Literal(value=token.value, line=token.line, col=token.col)
        if token.type == TokenType.NULL:
            self._advance(); return Literal(value=None, line=token.line, col=token.col)

        # String interpolation: "Hello, {name}!"
        if token.type == TokenType.INTERP_STRING:
            return self._parse_string_interpolation()

        # range from start to end -> RangeLiteral (only if followed by 'from')
        if token.type == TokenType.RANGE_KEYWORD:
            if self._peek().type == TokenType.FROM:
                tok = self._advance()
                self._advance()  # consume 'from'
                start = self._parse_expression()
                self._consume(TokenType.TO, "Expected 'to' after range start")
                end = self._parse_expression()
                return RangeLiteral(start=start, end=end, line=tok.line, col=tok.col)
            # If not followed by 'from', treat as identifier
            self._advance()
            return Identifier(name="range", line=token.line, col=token.col)

        if token.type == TokenType.IDENTIFIER:
            self._advance(); return Identifier(name=token.value, line=token.line, col=token.col)
        if token.type == TokenType.THIS:
            self._advance(); return Identifier(name=token.value, line=token.line, col=token.col)

        if token.type == TokenType.LPAREN:
            self._advance()
            expr = self._parse_expression()
            # Check for generator expression: (x for each x in items if cond)
            if self._check(TokenType.FOR):
                self._advance()
                if self._match(TokenType.EACH):
                    self._advance()
                variable = self._consume(TokenType.IDENTIFIER, "Expected variable in generator").value
                self._consume(TokenType.IN, "Expected 'in' in generator")
                old_ternary = self._allow_ternary
                self._allow_ternary = False
                iterable = self._parse_expression()
                self._allow_ternary = old_ternary
                condition = None
                if self._match(TokenType.IF):
                    self._advance()
                    condition = self._parse_expression()
                elif self._match(TokenType.WHERE):
                    self._advance()
                    condition = self._parse_expression()
                self._consume(TokenType.RPAREN, "Expected ')' in generator")
                return GeneratorExpression(
                    expression=expr, variable=variable,
                    iterable=iterable, condition=condition,
                    line=token.line, col=token.col
                )
            self._consume(TokenType.RPAREN, "Expected ')'")
            return expr

        if token.type == TokenType.LBRACKET:
            return self._parse_bracket_expression()

        if token.type == TokenType.LBRACE:
            return self._parse_dict_literal()

        if token.type == TokenType.FUNCTION:
            return self._parse_lambda()

        if token.type == TokenType.WHEN:
            self._advance()
            condition = self._parse_expression()
            self._consume(TokenType.THEN, "Expected 'then' after when condition")
            # Parse true_value with higher precedence than OR so 'or' isn't consumed
            true_val = self._parse_expression(self.PREC_AND + 1)
            # Consume 'or', 'otherwise', or 'else' before false value
            if self._check_any(TokenType.OR, TokenType.OTHERWISE, TokenType.ELSE):
                self._advance()
            false_val = self._parse_expression()
            return WhenExpression(condition=condition, true_value=true_val, false_value=false_val,
                                  line=token.line, col=token.col)

        if token.type == TokenType.REGEX_LITERAL:
            tok = self._advance()
            val = tok.value
            return RegexLiteral(pattern=val.get("pattern", ""), flags=val.get("flags", ""), line=tok.line, col=tok.col)

        if token.type == TokenType.EMPTY:
            self._advance()
            # empty is typically used as 'list is empty' - consume 'is' if present
            if self._check(TokenType.IS):
                self._advance()
            expr = self._parse_expression()
            return EmptyExpression(expression=expr, line=token.line, col=token.col)

        # Handle type keywords as identifiers in expressions (for 'is a type' checks)
        if token.type in (TokenType.INTEGER_TYPE, TokenType.FLOAT_TYPE, TokenType.STRING_TYPE,
                          TokenType.BOOLEAN_TYPE, TokenType.LIST_TYPE, TokenType.DICT_TYPE,
                          TokenType.ANY_TYPE):
            self._advance()
            # Return as Identifier so 'is a string' checks work
            return Identifier(name=token.value, line=token.line, col=token.col)

        # first of x -> x[0], last of x -> x[-1], rest of x -> x[1:]
        # Only trigger special behavior when followed by 'of'
        if token.type in (TokenType.FIRST, TokenType.LAST, TokenType.REST):
            if self._peek().type == TokenType.IDENTIFIER and self._peek().value == "of":
                token_type = token.type
                self._advance()  # consume first/last/rest
                self._advance()  # consume 'of'
                expr = self._parse_expression()
                if token_type == TokenType.FIRST:
                    return Index(object=expr, index=Literal(value=0), line=token.line, col=token.col)
                elif token_type == TokenType.LAST:
                    return Index(object=expr, index=Literal(value=-1), line=token.line, col=token.col)
                else:
                    return SliceExpression(object=expr, start=Literal(value=1), end=None, line=token.line, col=token.col)

        # join items with separator -> separator.join(items)
        if token.type == TokenType.JOIN:
            tok = self._advance()
            items = self._parse_expression()
            if self._match(TokenType.WITH):
                self._advance()
            separator = self._parse_expression()
            return Call(callee=Attribute(object=separator, attribute="join"), arguments=[items], line=tok.line, col=tok.col)

        # split text by separator -> text.split(separator)
        if token.type == TokenType.SPLIT:
            tok = self._advance()
            text = self._parse_expression()
            if self._match(TokenType.BY):
                self._advance()
            separator = self._parse_expression()
            return Call(callee=Attribute(object=text, attribute="split"), arguments=[separator], line=tok.line, col=tok.col)

        # min/max/sum/abs/count of x -> min(x)/max(x)/sum(x)/abs(x)/len(x)
        # Only trigger special behavior when followed by 'of'
        if token.type in (TokenType.MIN, TokenType.MAX, TokenType.SUM, TokenType.ABS, TokenType.LENGTH):
            if self._peek().type == TokenType.IDENTIFIER and self._peek().value == "of":
                tok = self._advance()
                self._advance()  # consume 'of'
                expr = self._parse_expression()
                if token.type == TokenType.MIN:
                    return Call(callee=Identifier(name="min"), arguments=[expr], line=tok.line, col=tok.col)
                elif token.type == TokenType.MAX:
                    return Call(callee=Identifier(name="max"), arguments=[expr], line=tok.line, col=tok.col)
                elif token.type == TokenType.SUM:
                    return Call(callee=Identifier(name="sum"), arguments=[expr], line=tok.line, col=tok.col)
                elif token.type == TokenType.ABS:
                    return Call(callee=Identifier(name="abs"), arguments=[expr], line=tok.line, col=tok.col)
                else:
                    return LengthExpression(expression=expr, line=tok.line, col=tok.col)

        # round x -> round(x), upper x -> x.upper(), lower x -> x.lower(), strip x -> x.strip()
        if token.type in (TokenType.ROUND, TokenType.UPPER, TokenType.LOWER, TokenType.STRIP,
                          TokenType.CAPITALIZE, TokenType.TITLE, TokenType.SWAPCASE):
            tok = self._advance()
            # If followed by an expression-ender or binary operator, this is a variable reference
            # (the Pratt loop will handle any infix operator after the identifier)
            nxt = self._current()
            if self._is_expr_end() or self._get_infix_precedence(nxt.type) > 0:
                return Identifier(name=tok.value, line=tok.line, col=tok.col)
            expr = self._parse_expression()
            if token.type == TokenType.ROUND:
                return Call(callee=Identifier(name="round"), arguments=[expr], line=tok.line, col=tok.col)
            else:
                attr = token.type.name.lower()
                return Call(callee=Attribute(object=expr, attribute=attr), arguments=[], line=tok.line, col=tok.col)

        # unique x -> list(set(x))
        if token.type == TokenType.UNIQUE:
            tok = self._advance()
            if self._is_expr_end():
                return Identifier(name="unique", line=tok.line, col=tok.col)
            expr = self._parse_expression()
            return Call(callee=Identifier(name="list"), arguments=[
                Call(callee=Identifier(name="set"), arguments=[expr])
            ], line=tok.line, col=tok.col)

        # compact x -> [i for i in x if i]
        if token.type == TokenType.COMPACT:
            tok = self._advance()
            # If there's nothing to consume (end of expression), treat as identifier
            if self._is_expr_end():
                return Identifier(name="compact", line=tok.line, col=tok.col)
            expr = self._parse_expression()
            return ListComprehension(
                expression=Identifier(name="i"),
                variable="i",
                iterable=expr,
                condition=Identifier(name="i"),
                line=tok.line, col=tok.col
            )

        # take n from x -> x[:n], drop n from x -> x[n:]
        if token.type in (TokenType.TAKE, TokenType.DROP):
            is_take = token.type == TokenType.TAKE
            tok = self._advance()
            count = self._parse_expression()
            self._consume(TokenType.FROM, "Expected 'from' after count")
            iterable = self._parse_expression()
            if is_take:
                return SliceExpression(object=iterable, start=None, end=count, line=tok.line, col=tok.col)
            else:
                return SliceExpression(object=iterable, start=count, end=None, line=tok.line, col=tok.col)

        # Any non-structural keyword token can be used as an identifier in expressions
        if self._is_name_token(token.type) and token.type != TokenType.IDENTIFIER:
            self._advance()
            return Identifier(name=token.value, line=token.line, col=token.col)

        if token.type == TokenType.INPUT:
            self._advance()
            return Call(callee=Identifier(name="input"), arguments=[])

        hint = ""
        if token.type == TokenType.IDENTIFIER:
            suggestion = suggest_keyword(token.value)
            if suggestion:
                hint = f" {suggestion}"
        raise ParseError(f"Unexpected token: {token}.{hint}", token)

    def _parse_bracket_expression(self) -> ASTNode:
        """Parse [ ... ] - could be list literal, list comprehension, or slice."""
        tok = self._advance()  # consume '['
        if self._check(TokenType.RBRACKET):
            self._advance()
            return ListLiteral(elements=[], line=tok.line, col=tok.col)

        # Check for slice: [start:end] — starts with expression followed by colon
        slice_start = self._parse_expression()
        if self._check(TokenType.COLON):
            self._advance()  # consume ':'
            slice_end = self._parse_expression() if not self._check(TokenType.RBRACKET) else None
            self._consume(TokenType.RBRACKET, "Expected ']'")
            # Return a slice as a special form: will be handled in infix [ ] parsing
            # We return the start and end as a tuple to be picked up by the infix handler
            # Actually, slice is parsed in the infix LBRACKET handler. This path is only
            # reached when [ comes as a standalone expression (not as index).
            # For slice literals like [1:10], return a ListLiteral with a special marker
            return ListLiteral(elements=[slice_start, slice_end] if slice_end else [slice_start],
                              line=tok.line, col=tok.col)

        expr = slice_start  # first expression becomes the first element

        # Check for list comprehension: [expr for each var in iterable if condition]
        if self._check(TokenType.FOR):
            self._advance()
            if self._match(TokenType.EACH):
                self._advance()
            variable = self._consume(TokenType.IDENTIFIER, "Expected variable name in comprehension").value
            self._consume(TokenType.IN, "Expected 'in' in comprehension")
            # Disable ternary in iterable parsing (comprehension's 'if' would be confused)
            old_ternary = self._allow_ternary
            self._allow_ternary = False
            iterable = self._parse_expression()
            self._allow_ternary = old_ternary
            condition = None
            if self._match(TokenType.IF):
                self._advance()
                condition = self._parse_expression()
            elif self._match(TokenType.WHERE):
                self._advance()
                condition = self._parse_expression()
            self._consume(TokenType.RBRACKET, "Expected ']'")
            return ListComprehension(expression=expr, variable=variable,
                                     iterable=iterable, condition=condition,
                                     line=tok.line, col=tok.col)

        # Plain list literal: [expr, expr, ...]
        elements = [expr]
        while self._match(TokenType.COMMA):
            self._advance()
            elements.append(self._parse_expression())
        self._consume(TokenType.RBRACKET, "Expected ']'")
        return ListLiteral(elements=elements, line=tok.line, col=tok.col)

    def _parse_string_interpolation(self) -> StringInterpolation:
        """Parse an interpolated string like "Hello, {name}! You are {age} years old"."""
        token = self._advance()  # consume INTERP_STRING
        raw = token.value
        parts = []
        i = 0
        current_text = []

        while i < len(raw):
            if raw[i] == "{" and i + 1 < len(raw):
                if current_text:
                    parts.append(Literal(value="".join(current_text), line=token.line, col=token.col))
                    current_text = []
                i += 1
                # Read expression inside braces
                expr_chars = []
                brace_depth = 0
                while i < len(raw):
                    if raw[i] == "{" and brace_depth == 0:
                        brace_depth += 1
                        expr_chars.append(raw[i])
                    elif raw[i] == "}" and brace_depth == 0:
                        break
                    elif raw[i] == "{":
                        brace_depth += 1
                        expr_chars.append(raw[i])
                    elif raw[i] == "}":
                        brace_depth -= 1
                        expr_chars.append(raw[i])
                    else:
                        expr_chars.append(raw[i])
                    i += 1
                # Parse the expression text using a sub-lexer+parser
                expr_text = "".join(expr_chars)
                if expr_text.strip():
                    sub_tokens = tokenize(expr_text)
                    sub_parser = Parser(sub_tokens)
                    expr_node = sub_parser._parse_expression()
                    parts.append(expr_node)
                i += 1  # skip closing }
            elif raw[i] == "}" and i + 1 < len(raw) and raw[i+1] == "}":
                # Escaped brace }}
                current_text.append("}")
                i += 2
            else:
                current_text.append(raw[i])
                i += 1

        if current_text:
            parts.append(Literal(value="".join(current_text), line=token.line, col=token.col))

        return StringInterpolation(parts=parts, line=token.line, col=token.col)

    def _parse_dict_literal(self) -> ASTNode:
        """Parse { ... } - could be dict literal or dict comprehension."""
        tok = self._advance()
        if self._check(TokenType.RBRACE):
            self._advance()
            return DictLiteral(pairs=[], line=tok.line, col=tok.col)

        key = self._parse_expression()
        self._consume(TokenType.COLON, "Expected ':' in dictionary")
        value = self._parse_expression()

        # Check for dict comprehension: {k: v for each k,v in iterable if condition}
        if self._check(TokenType.FOR):
            self._advance()
            if self._match(TokenType.EACH):
                self._advance()
            variable = self._consume(TokenType.IDENTIFIER, "Expected variable in dict comprehension").value
            self._consume(TokenType.IN, "Expected 'in' in dict comprehension")
            old_ternary = self._allow_ternary
            self._allow_ternary = False
            iterable = self._parse_expression()
            self._allow_ternary = old_ternary
            condition = None
            if self._match(TokenType.IF):
                self._advance()
                condition = self._parse_expression()
            elif self._match(TokenType.WHERE):
                self._advance()
                condition = self._parse_expression()
            self._consume(TokenType.RBRACE, "Expected '}'")
            return DictComprehension(
                key=key, value=value, variable=variable,
                iterable=iterable, condition=condition,
                line=tok.line, col=tok.col
            )

        pairs = [(key, value)]
        while self._match(TokenType.COMMA):
            self._advance()
            k = self._parse_expression()
            self._consume(TokenType.COLON, "Expected ':' in dictionary")
            v = self._parse_expression()
            pairs.append((k, v))
        self._consume(TokenType.RBRACE, "Expected '}'")
        return DictLiteral(pairs=pairs, line=tok.line, col=tok.col)

    def _parse_lambda(self) -> Lambda:
        tok = self._advance()
        params = []
        if self._match(TokenType.WITH):
            self._advance()
            params = self._parse_parameter_list()
        self._consume(TokenType.COLON, "Expected ':' in lambda")
        body = self._parse_expression()
        return Lambda(parameters=params, body=body, line=tok.line, col=tok.col)

    # ---- Helpers ----

    def _parse_parameter_list(self) -> List[str]:
        params = []
        if self._check(TokenType.IDENTIFIER) or self._is_name_token(self._current().type):
            params.append(self._parse_name_token())
            while self._match(TokenType.COMMA):
                self._advance()
                params.append(self._parse_name_token())
        return params

    def _parse_comma_separated_expressions(self) -> List[ASTNode]:
        exprs = [self._parse_expression()]
        while self._match(TokenType.COMMA):
            self._advance()
            exprs.append(self._parse_expression())
        return exprs

    def _parse_comma_separated_idents(self) -> List[str]:
        idents = [self._consume(TokenType.IDENTIFIER, "Expected identifier").value]
        while self._match(TokenType.COMMA):
            self._advance()
            idents.append(self._consume(TokenType.IDENTIFIER, "Expected identifier").value)
        return idents


def parse(tokens: List[Token]) -> Program:
    parser = Parser(tokens)
    return parser.parse()


# Import for string interpolation sub-parsing (at end to avoid circular issues)
from ..lexer.lexer import tokenize

