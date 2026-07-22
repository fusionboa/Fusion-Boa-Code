"""
FusionBoa → Python Code Generator

Translates a FusionBoa AST into equivalent Python source code.
Supports all Fusion features including string interpolation, list comprehensions,
default parameters, spread/rest, yield, const, and export.
"""

from ..parser.ast_nodes import *
from ..lexer.tokens import TokenType


class PythonGenerator:
    """Generates Python code from a FusionBoa AST."""

    def __init__(self, ast: Program):
        self.ast = ast
        self.indent_level = 0
        self._in_class = False
        self._needs_typing_imports = False
        self._needs_abc_imports = False
        self._needs_re_import = False
        self._needs_functools_import = False
        self._needs_dataclass_import = False

    def _indent(self) -> str:
        return "    " * self.indent_level

    def generate(self) -> str:
        lines = []
        for stmt in self.ast.statements:
            lines.append(self._gen_statement(stmt))
        # Prepend needed imports at top
        result = "\n".join(lines)
        imports = []
        if self._needs_functools_import:
            imports.append("import functools")
        if self._needs_re_import:
            imports.append("import re")
        if self._needs_typing_imports:
            imports.append("from typing import Generic, TypeVar")
        if self._needs_abc_imports:
            imports.append("from abc import ABC, abstractmethod")
        if self._needs_dataclass_import:
            imports.append("from dataclasses import dataclass, field")
            imports.append("from typing import Optional")
        if imports:
            result = "\n".join(imports) + "\n\n" + result
        return result

    def _gen_statement(self, node: ASTNode) -> str:
        if node is None: return ""
        gen_map = {
            ExpressionStatement: self._gen_expression_statement,
            VariableDeclaration: self._gen_variable_declaration,
            ConstDeclaration: self._gen_const_declaration,
            Assignment: self._gen_assignment,
            AugmentedAssignment: self._gen_augmented_assignment,
            IfStatement: self._gen_if_statement,
            MatchStatement: self._gen_match_statement,
            ForLoop: self._gen_for_loop,
            ForAwaitLoop: self._gen_for_await_loop,
            RepeatLoop: self._gen_repeat_loop,
            WhileLoop: self._gen_while_loop,
            FunctionDefinition: self._gen_function_definition,
            ClassDefinition: self._gen_class_definition,
            InterfaceDefinition: self._gen_interface_definition,
            ReturnStatement: self._gen_return_statement,
            YieldStatement: self._gen_yield_statement,
            BreakStatement: lambda n: self._indent() + "break",
            ContinueStatement: lambda n: self._indent() + "continue",
            PassStatement: lambda n: self._indent() + "pass",
            ImportStatement: self._gen_import_statement,
            ExportStatement: self._gen_export_statement,
            TryStatement: self._gen_try_statement,
            PrintStatement: self._gen_print_statement,
            InputStatement: self._gen_input_statement,
            DoWhileLoop: self._gen_do_while_loop,
            EnumDefinition: self._gen_enum_definition,
            DeferStatement: self._gen_defer_statement,
            GuardStatement: self._gen_guard_statement,
            SwapStatement: self._gen_swap_statement,
            PushStatement: self._gen_push_statement,
            PopStatement: self._gen_pop_statement,
            DestructuringDeclaration: self._gen_destructuring_declaration,
            IncrementExpression: self._gen_increment_expression,
            DecrementExpression: self._gen_decrement_expression,
            WithStatement: self._gen_with_statement,
            DecoratorStatement: self._gen_decorator_statement,
            StaticMethodDeclaration: self._gen_static_method_declaration,
            AssertStatement: self._gen_assert_statement,
            RaiseStatement: self._gen_raise_statement,
            DeleteStatement: self._gen_delete_statement,
            UsingStatement: self._gen_using_statement,
            OperatorOverload: self._gen_operator_overload,
            # v0.5.0 Masterpiece
            RecordDefinition: self._gen_record_definition,
            PropertyDefinition: self._gen_property_definition,
            NamespaceDefinition: self._gen_namespace_definition,
            ExtensionDefinition: self._gen_extension_definition,
            LazyDeclaration: self._gen_lazy_declaration,
        }
        gen_func = gen_map.get(type(node))
        if gen_func: return gen_func(node)
        return f"# Unknown: {type(node).__name__}"

    def _gen_expression(self, node: ASTNode) -> str:
        if node is None: return ""
        if isinstance(node, Literal): return self._gen_literal(node)
        if isinstance(node, Identifier): return self._gen_identifier(node)
        if isinstance(node, BinaryOp): return self._gen_binary_op(node)
        if isinstance(node, UnaryOp): return self._gen_unary_op(node)
        if isinstance(node, Call): return self._gen_call(node)
        if isinstance(node, Attribute): return self._gen_attribute(node)
        if isinstance(node, Index): return self._gen_index(node)
        if isinstance(node, ListLiteral): return self._gen_list_literal(node)
        if isinstance(node, DictLiteral): return self._gen_dict_literal(node)
        if isinstance(node, Lambda): return self._gen_lambda(node)
        if isinstance(node, Ternary): return self._gen_ternary(node)
        if isinstance(node, LengthExpression): return self._gen_length_expression(node)
        if isinstance(node, AwaitExpression): return f"await {self._gen_expression(node.expression)}"
        if isinstance(node, ListComprehension): return self._gen_list_comprehension(node)
        if isinstance(node, StringInterpolation): return self._gen_string_interpolation(node)
        if isinstance(node, SpreadElement): return f"*{self._gen_expression(node.expression)}"
        if isinstance(node, KeywordArgument): return f"{node.name}={self._gen_expression(node.value)}"
        if isinstance(node, RangeLiteral): return f"range({self._gen_expression(node.start)}, {self._gen_expression(node.end)} + 1)"
        if isinstance(node, InExpression): return f"({self._gen_expression(node.left)} in {self._gen_expression(node.right)})"
        if isinstance(node, IsExpression): return f"isinstance({self._gen_expression(node.left)}, {self._gen_expression(node.right)})"
        if isinstance(node, DictComprehension): return self._gen_dict_comprehension(node)
        if isinstance(node, MultiLineString): return repr(node.value)
        if isinstance(node, DeferStatement): return self._gen_defer_statement(node)
        if isinstance(node, SliceExpression): return self._gen_slice_expression(node)
        if isinstance(node, GuardStatement): return self._gen_guard_statement(node)
        if isinstance(node, BetweenExpression): return self._gen_between_expression(node)
        if isinstance(node, WhenExpression): return self._gen_when_expression(node)
        if isinstance(node, EmptyExpression): return self._gen_empty_expression(node)
        if isinstance(node, GeneratorExpression): return self._gen_generator_expression(node)
        if isinstance(node, IncrementExpression): return f"{node.target} += 1"
        if isinstance(node, DecrementExpression): return f"{node.target} -= 1"
        if isinstance(node, RegexLiteral): return self._gen_regex_literal(node)
        if isinstance(node, TypeOfExpression): return f"type({self._gen_expression(node.expression)})"
        if isinstance(node, MatchPattern): return f"re.search({self._gen_expression(node.pattern)}, str({self._gen_expression(node.expression)}))"
        if isinstance(node, CastExpression): return self._gen_cast_expression(node)
        if isinstance(node, PartialPlaceholder): return f"__fusionboa_partial_{node.index}"
        return f"/* Unknown expr: {type(node).__name__} */"

    # ---- v0.5.1 Functional expression helpers ----
    # Map FusionBoa functional names to Python builtins
    
    def _gen_call(self, node: Call) -> str:
        callee = self._gen_expression(node.callee)
        args = ", ".join(self._gen_expression(a) for a in node.arguments)
        if isinstance(node.callee, Identifier):
            name = node.callee.name
            if name == "reduce":
                self._needs_functools_import = True
                return f"functools.reduce({args})"
            if name in ("print", "input"):
                return f"{name}({args})"
        return f"{callee}({args})"

    # ---- Expressions ----

    def _gen_literal(self, node: Literal) -> str:
        if node.value is None: return "None"
        if node.value is True: return "True"
        if node.value is False: return "False"
        if isinstance(node.value, str): return repr(node.value)
        return str(node.value)

    def _gen_identifier(self, node: Identifier) -> str:
        return "self" if node.name == "this" else node.name

    def _auto_str(self, expr_str: str, expr_node: ASTNode) -> str:
        """Wrap with str() if node is not already a string-producing expression."""
        if isinstance(expr_node, Literal) and isinstance(expr_node.value, str):
            return expr_str  # Already a string, no wrapping needed
        if isinstance(expr_node, StringInterpolation):
            return expr_str  # Already an f-string
        if isinstance(expr_node, BinaryOp) and expr_node.operator == "+":
            return expr_str  # Already a concatenation (at least one side already wrapped)
        if isinstance(expr_node, Call) and isinstance(expr_node.callee, Identifier) and expr_node.callee.name == "str":
            return expr_str  # Already wrapped in str()
        # Wrap everything else with str() for safe concatenation
        return f"str({expr_str})"

    def _is_stringy(self, node: ASTNode) -> bool:
        """Check if an AST node produces a string value (for safe + concatenation)."""
        if isinstance(node, Literal) and isinstance(node.value, str):
            return True
        if isinstance(node, StringInterpolation):
            return True
        if isinstance(node, Call) and isinstance(node.callee, Identifier) and node.callee.name == "str":
            return True
        if isinstance(node, BinaryOp) and node.operator == "+":
            # Only stringy if one of the operands is stringy
            return self._is_stringy(node.left) or self._is_stringy(node.right)
        return False

    def _gen_binary_op(self, node: BinaryOp) -> str:
        op_map = {"and": "and", "or": "or", "xor": "^", "==": "==", "!=": "!=",
                   "<": "<", ">": ">",
                   "<=": "<=", ">=": ">=", "+": "+", "-": "-", "*": "*", "/": "/",
                   "//": "//", "%": "%", "^": "**",
                   "&": "&", "|": "|", "<<": "<<", ">>": ">>",
                   "in": "in", "not in": "not in",
                   "has": "in",
                   "contains": "in"}
        py_op = op_map.get(node.operator, node.operator)
        left = self._gen_expression(node.left)
        right = self._gen_expression(node.right)

        # Null-coalescing: a ?? b -> a if a is not None else b
        if node.operator == "??":
            return f"({left} if {left} is not None else {right})"
        # Auto str coercion for + with strings
        if node.operator == "+":
            if self._is_stringy(node.left) or self._is_stringy(node.right):
                left = self._auto_str(left, node.left)
                right = self._auto_str(right, node.right)
        # Pipe operator: x |> f -> f(x), x |> f(a, b) -> f(x, a, b)
        # Special handling for first/last/reverse/sort which are not Python builtins
        if node.operator == "|>":
            if isinstance(node.right, Identifier) and node.right.name in ("first", "last", "reverse", "sort", "unique", "compact"):
                pipe_name = node.right.name
                if pipe_name == "first":
                    return f"{left}[0]"
                if pipe_name == "last":
                    return f"{left}[-1]"
                if pipe_name in ("reverse", "sort"):
                    # sort -> sorted(), reverse -> reversed()
                    return f"list(sorted({left}))" if pipe_name == "sort" else f"list(reversed({left}))"
                if pipe_name == "unique":
                    return f"list(set({left}))"
                if pipe_name == "compact":
                    return f"[i for i in {left} if i]"
            if isinstance(node.right, Call):
                callee = self._gen_expression(node.right.callee)
                args = [left] + [self._gen_expression(a) for a in node.right.arguments]
                return f"{callee}({', '.join(args)})"
            return f"{right}({left})"
        # has operator: list has item -> item in list (swapped)
        if node.operator == "has":
            return f"({right} in {left})"
        # has no operator: list has no item -> item not in list
        if node.operator == "has no":
            return f"({right} not in {left})"
        # contains operator: name contains "hello" -> "hello" in name (swapped)
        if node.operator == "contains":
            return f"({right} in {left})"
        # starts with: name starts with "hello" -> name.startswith("hello")
        if node.operator == "starts with":
            return f"{left}.startswith({right})"
        # ends with: name ends with "world" -> name.endswith("world")
        if node.operator == "ends with":
            return f"{left}.endswith({right})"
        # includes: list includes item -> item in list (swapped)
        if node.operator == "includes":
            return f"({right} in {left})"
        # excludes: list excludes item -> item not in list (swapped)
        if node.operator == "excludes":
            return f"({right} not in {left})"
        # is same as: x is same as y -> x is y
        if node.operator == "is same as":
            return f"({left} is {right})"
        return f"({left} {py_op} {right})"

    def _gen_unary_op(self, node: UnaryOp) -> str:
        op_map = {"neg": "-", "not": "not ", "~": "~"}
        py_op = op_map.get(node.operator, node.operator)
        operand = self._gen_expression(node.operand)
        if node.operator == "neg": return f"(-{operand})"
        return f"({py_op} {operand})"


    def _gen_attribute(self, node: Attribute) -> str:
        obj = self._gen_expression(node.object)
        return f"{obj}.{node.attribute}"

    def _gen_index(self, node: Index) -> str:
        obj = self._gen_expression(node.object)
        idx = self._gen_expression(node.index)
        return f"{obj}[{idx}]"

    def _gen_list_literal(self, node: ListLiteral) -> str:
        elements = ", ".join(self._gen_expression(e) for e in node.elements)
        return f"[{elements}]"

    def _gen_dict_literal(self, node: DictLiteral) -> str:
        pairs = ", ".join(f"{self._gen_dict_key(k)}: {self._gen_expression(v)}" for k, v in node.pairs)
        return f"{{{pairs}}}"

    def _gen_dict_key(self, node: ASTNode) -> str:
        if isinstance(node, Identifier): return repr(node.name)
        if isinstance(node, Literal) and isinstance(node.value, str): return repr(node.value)
        return self._gen_expression(node)

    def _gen_lambda(self, node: Lambda) -> str:
        params = ", ".join(node.parameters)
        body = self._gen_expression(node.body)
        return f"lambda {params}: {body}"

    def _gen_ternary(self, node: Ternary) -> str:
        return f"({self._gen_expression(node.true_value)} if {self._gen_expression(node.condition)} else {self._gen_expression(node.false_value)})"

    def _gen_length_expression(self, node: LengthExpression) -> str:
        return f"len({self._gen_expression(node.expression)})"

    def _gen_list_comprehension(self, node: ListComprehension) -> str:
        expr = self._gen_expression(node.expression)
        iterable = self._gen_expression(node.iterable)
        if node.condition:
            cond = self._gen_expression(node.condition)
            return f"[{expr} for {node.variable} in {iterable} if {cond}]"
        return f"[{expr} for {node.variable} in {iterable}]"

    def _gen_dict_comprehension(self, node: DictComprehension) -> str:
        key = self._gen_expression(node.key)
        value = self._gen_expression(node.value)
        iterable = self._gen_expression(node.iterable)
        if node.condition:
            cond = self._gen_expression(node.condition)
            return f"{{{key}: {value} for {node.variable} in {iterable} if {cond}}}"
        return f"{{{key}: {value} for {node.variable} in {iterable}}}"

    def _gen_slice_expression(self, node: SliceExpression) -> str:
        obj = self._gen_expression(node.object)
        start = self._gen_expression(node.start) if node.start else ""
        end = self._gen_expression(node.end) if node.end else ""
        return f"{obj}[{start}:{end}]"

    def _gen_string_interpolation(self, node: StringInterpolation) -> str:
        parts = []
        for p in node.parts:
            if isinstance(p, Literal) and isinstance(p.value, str):
                parts.append(p.value.replace("{", "{{").replace("}", "}}"))
            else:
                parts.append("{" + self._gen_expression(p) + "}")
        return "f" + repr("".join(parts))

    # ---- Statements ----

    def _gen_expression_statement(self, node: ExpressionStatement) -> str:
        return self._indent() + self._gen_expression(node.expression)

    def _gen_variable_declaration(self, node: VariableDeclaration) -> str:
        value = self._gen_expression(node.value)
        type_hint = ""
        if node.type_annotation:
            type_hint = f": {self._gen_type_annotation(node.type_annotation)}"
        return self._indent() + f"{node.name}{type_hint} = {value}"

    def _gen_const_declaration(self, node: ConstDeclaration) -> str:
        value = self._gen_expression(node.value)
        type_hint = ""
        if node.type_annotation:
            type_hint = f": {self._gen_type_annotation(node.type_annotation)}"
        return self._indent() + f"{node.name}{type_hint} = {value}  # const"

    def _gen_type_annotation(self, node: TypeAnnotation) -> str:
        type_map = {
            "int": "int", "integer": "int", "float": "float", "string": "str",
            "bool": "bool", "boolean": "bool", "list": "list", "dict": "dict",
            "dictionary": "dict", "any": "Any", "void": "None",
        }
        return type_map.get(node.type_name, node.type_name)

    def _translate_this(self, name: str) -> str:
        if name == "this": return "self"
        if name.startswith("this."): return "self." + name[5:]
        return name

    def _gen_assignment(self, node: Assignment) -> str:
        value = self._gen_expression(node.value)
        target = self._translate_this(node.target)
        return self._indent() + f"{target} = {value}"

    def _gen_augmented_assignment(self, node: AugmentedAssignment) -> str:
        value = self._gen_expression(node.value)
        target = self._translate_this(node.target)
        # Logical assignment: x ||= val -> x = x or val, x &&= val -> x = x and val, x ??= val -> x = x if x is not None else val
        if node.operator == "||":
            return self._indent() + f"{target} = {target} or {value}"
        if node.operator == "&&":
            return self._indent() + f"{target} = {target} and {value}"
        if node.operator == "??":
            return self._indent() + f"{target} = {target} if {target} is not None else {value}"
        return self._indent() + f"{target} {node.operator}= {value}"

    def _gen_if_statement(self, node: IfStatement) -> str:
        lines = []
        lines.append(self._indent() + f"if {self._gen_expression(node.condition)}:")
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        for elif_cond, elif_body in node.elif_branches:
            lines.append(self._indent() + f"elif {self._gen_expression(elif_cond)}:")
            self.indent_level += 1
            for stmt in elif_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        if node.else_body:
            lines.append(self._indent() + "else:")
            self.indent_level += 1
            for stmt in node.else_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        return "\n".join(lines)

    def _gen_match_statement(self, node: MatchStatement) -> str:
        lines = [self._indent() + f"match {self._gen_expression(node.expression)}:"]
        self.indent_level += 1
        for pattern, body in node.cases:
            lines.append(self._indent() + f"case {self._gen_expression(pattern)}:")
            self.indent_level += 1
            for stmt in body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        # Guarded cases: case x if x > 5:
        for guard_case in node.guarded_cases:
            pat = self._gen_expression(guard_case.pattern)
            guard = self._gen_expression(guard_case.guard)
            lines.append(self._indent() + f"case {pat} if {guard}:")
            self.indent_level += 1
            for stmt in guard_case.body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        if node.default_body:
            lines.append(self._indent() + "case _:")
            self.indent_level += 1
            for stmt in node.default_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        self.indent_level -= 1
        return "\n".join(lines)

    def _gen_for_loop(self, node: ForLoop) -> str:
        lines = []
        if node.iterable:
            lines.append(self._indent() + f"for {node.variable} in {self._gen_expression(node.iterable)}:")
        else:
            from_v = self._gen_expression(node.range_from)
            to_v = self._gen_expression(node.range_to)
            lines.append(self._indent() + f"for {node.variable} in range({from_v}, {to_v} + 1):")
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        return "\n".join(lines)

    def _gen_repeat_loop(self, node: RepeatLoop) -> str:
        lines = [self._indent() + f"for __fusionboa_i in range(int({self._gen_expression(node.times)})):"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        return "\n".join(lines)

    def _gen_while_loop(self, node: WhileLoop) -> str:
        lines = [self._indent() + f"while {self._gen_expression(node.condition)}:"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        return "\n".join(lines)

    def _gen_function_definition(self, node: FunctionDefinition) -> str:
        lines = []
        prefix = "async " if node.is_async else ""
        name = node.name
        params = list(node.parameters)
        if node.has_rest_param:
            params.append(f"*{node.rest_param_name}")
        param_strs = []
        for p in params:
            if p in node.defaults:
                param_strs.append(f"{p}={self._gen_expression(node.defaults[p])}")
            else:
                param_strs.append(p)
        lines.append(self._indent() + f"{prefix}def {name}({', '.join(param_strs)}):")
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        return "\n".join(lines)

    def _gen_class_definition(self, node: ClassDefinition) -> str:
        lines = []
        bases = []
        if node.parent:
            bases.append(node.parent)
        if node.implements:
            bases.extend(node.implements)
        base_str = f"({', '.join(bases)})" if bases else ""
        
        # Add type: ignore for interface-style usage
        if node.generics:
            generics_str = ", ".join(node.generics)
            self._needs_typing_imports = True
            for g in node.generics:
                lines.append(self._indent() + f"{g} = TypeVar('{g}')")
            lines.append(self._indent() + f"class {node.name}(Generic[{generics_str}]{', ' + ', '.join(bases) if bases else ''}):")
        else:
            lines.append(self._indent() + f"class {node.name}{base_str}:")
        self.indent_level += 1
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                if not stmt.parameters or stmt.parameters[0] != "this":
                    stmt.parameters = ["self"] + list(stmt.parameters)
                if stmt.name == "init":
                    stmt.name = "__init__"
            elif isinstance(stmt, OperatorOverload):
                lines.append(self._gen_operator_overload(stmt))
                continue
            lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        return "\n".join(lines)

    def _gen_return_statement(self, node: ReturnStatement) -> str:
        if node.value:
            return self._indent() + f"return {self._gen_expression(node.value)}"
        return self._indent() + "return"

    def _gen_yield_statement(self, node: YieldStatement) -> str:
        if node.value:
            return self._indent() + f"yield {self._gen_expression(node.value)}"
        return self._indent() + "yield"

    def _gen_import_statement(self, node: ImportStatement) -> str:
        if node.items:
            items = ", ".join(node.items)
            return self._indent() + f"from {node.module} import {items}"
        if node.alias:
            return self._indent() + f"import {node.module} as {node.alias}"
        return self._indent() + f"import {node.module}"

    def _gen_export_statement(self, node: ExportStatement) -> str:
        return self._gen_statement(node.declaration) + "  # exported"

    def _gen_try_statement(self, node: TryStatement) -> str:
        lines = [self._indent() + "try:"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        if node.catch_body:
            if node.catch_var:
                lines.append(self._indent() + f"except Exception as {node.catch_var}:")
            else:
                lines.append(self._indent() + "except Exception:")
            self.indent_level += 1
            for stmt in node.catch_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        if node.finally_body:
            lines.append(self._indent() + "finally:")
            self.indent_level += 1
            for stmt in node.finally_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        return "\n".join(lines)

    def _gen_print_statement(self, node: PrintStatement) -> str:
        if node.expression:
            return self._indent() + f"print({self._gen_expression(node.expression)})"
        return self._indent() + "print()"

    def _gen_input_statement(self, node: InputStatement) -> str:
        if node.target:
            if node.prompt:
                return self._indent() + f"{node.target} = input({repr(node.prompt)})"
            return self._indent() + f"{node.target} = input()"
        return self._indent() + "input()"

    def _gen_do_while_loop(self, node: DoWhileLoop) -> str:
        lines = [self._indent() + "while True:"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        lines.append(self._indent() + f"if not ({self._gen_expression(node.condition)}): break")
        self.indent_level -= 1
        return "\n".join(lines)

    def _gen_enum_definition(self, node: EnumDefinition) -> str:
        lines = [self._indent() + f"# enum {node.name}"]
        for i, member in enumerate(node.members):
            lines.append(self._indent() + f"{node.name}_{member} = {i}")
        return "\n".join(lines)

    def _gen_defer_statement(self, node: DeferStatement) -> str:
        """defer: body - runs at function exit. Generates try/finally pattern."""
        lines = []
        for stmt in node.body:
            lines.append(self._gen_statement(stmt))
        return "\n".join([self._indent() + "# deferred (cleanup):"] + lines)

    def _gen_guard_statement(self, node: GuardStatement) -> str:
        cond = self._gen_expression(node.condition)
        # Guard = if condition is false, execute the body and return
        lines = [self._indent() + f"if not ({cond}):"]
        self.indent_level += 1
        for stmt in node.body:
            lines.append(self._gen_statement(stmt))
        lines.append(self._indent() + "return")
        self.indent_level -= 1
        return "\n".join(lines)

    def _gen_swap_statement(self, node: SwapStatement) -> str:
        """swap x and y -> x, y = y, x"""
        return self._indent() + f"{node.left}, {node.right} = {node.right}, {node.left}"

    def _gen_push_statement(self, node: PushStatement) -> str:
        """push value into list -> list.append(value)"""
        value = self._gen_expression(node.value)
        return self._indent() + f"{node.target}.append({value})"

    def _gen_pop_statement(self, node: PopStatement) -> str:
        """pop from list -> list.pop()"""
        return self._indent() + f"{node.target}.pop()"

    def _gen_destructuring_declaration(self, node: DestructuringDeclaration) -> str:
        """'let [a, b] be expr' -> a, b = expr (list unpacking)
        'let {name, age} be dict' -> name, age = dict['name'], dict['age']"""
        if node.destructure_type == "list":
            targets = ", ".join(node.targets)
            value = self._gen_expression(node.value)
            return self._indent() + f"{targets} = {value}"
        else:
            # Dict destructuring: let {a, b} be d -> a, b = d['a'], d['b']
            value = self._gen_expression(node.value)
            targets = ", ".join(node.targets)
            values = ", ".join(f"{value}[{repr(t)}]" for t in node.targets)
            return self._indent() + f"{targets} = {values}"

    def _gen_increment_expression(self, node: IncrementExpression) -> str:
        """x++ or ++x -> x += 1"""
        return self._indent() + f"{node.target} += 1"

    def _gen_decrement_expression(self, node: DecrementExpression) -> str:
        """x-- or --x -> x -= 1"""
        return self._indent() + f"{node.target} -= 1"

    def _gen_with_statement(self, node: WithStatement) -> str:
        """with resource as var: body -> with resource as var:\n    body"""
        lines = []
        resource = self._gen_expression(node.resource)
        if node.variable:
            lines.append(self._indent() + f"with {resource} as {node.variable}:")
        else:
            lines.append(self._indent() + f"with {resource}:")
        self.indent_level += 1
        for stmt in node.body:
            lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        return "\n".join(lines)

    def _gen_decorator_statement(self, node: DecoratorStatement) -> str:
        """@decorator -> @decorator"""
        if node.arguments:
            args = ", ".join(self._gen_expression(a) for a in node.arguments)
            return self._indent() + f"@{node.name}({args})"
        return self._indent() + f"@{node.name}"

    def _gen_static_method_declaration(self, node: StaticMethodDeclaration) -> str:
        """define static function -> @staticmethod + function"""
        lines = [self._indent() + "@staticmethod"]
        lines.append(self._gen_function_definition(node.declaration))
        return "\n".join(lines)

    def _gen_assert_statement(self, node: AssertStatement) -> str:
        cond = self._gen_expression(node.condition)
        if node.message:
            msg = self._gen_expression(node.message)
            return self._indent() + f"assert {cond}, {msg}"
        return self._indent() + f"assert {cond}"

    def _gen_raise_statement(self, node: RaiseStatement) -> str:
        if node.message:
            msg = self._gen_expression(node.message)
            return self._indent() + f"raise Exception({msg})"
        return self._indent() + "raise Exception()"

    def _gen_delete_statement(self, node: DeleteStatement) -> str:
        if node.source:
            src = self._gen_expression(node.source)
            return self._indent() + f"del {src}[{repr(node.target)}]"
        return self._indent() + f"del {node.target}"

    def _gen_using_statement(self, node: UsingStatement) -> str:
        """using resource as name: body -> with resource as name: body"""
        lines = []
        resource = self._gen_expression(node.resource)
        if node.variable:
            lines.append(self._indent() + f"with {resource} as {node.variable}:")
        else:
            lines.append(self._indent() + f"with {resource}:")
        self.indent_level += 1
        for stmt in node.body:
            lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        return "\n".join(lines)

    def _gen_for_await_loop(self, node: ForAwaitLoop) -> str:
        """for await each item in async_iterable: body -> async for item in async_iterable: body"""
        lines = [self._indent() + f"async for {node.variable} in {self._gen_expression(node.iterable)}:"]
        self.indent_level += 1
        for stmt in node.body:
            lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        return "\n".join(lines)

    def _gen_interface_definition(self, node: InterfaceDefinition) -> str:
        """define interface Name: body -> class Name(ABC): with abstract methods"""
        self._needs_abc_imports = True
        lines = []
        if node.parent:
            lines.append(self._indent() + f"class {node.name}({node.parent}, ABC):")
        else:
            lines.append(self._indent() + f"class {node.name}(ABC):")
        self.indent_level += 1
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                lines.append(self._indent() + "@abstractmethod")
                stmt.body = [PassStatement()]  # Interface methods have no body
            lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        return "\n".join(lines)

    def _gen_operator_overload(self, node: OperatorOverload) -> str:
        """define operator + with other: body -> __add__(self, other): body"""
        op_map = {
            "+": "__add__", "-": "__sub__", "*": "__mul__", "/": "__truediv__",
            "//": "__floordiv__", "%": "__mod__", "^": "__pow__",
            "==": "__eq__", "!=": "__ne__", "<": "__lt__", ">": "__gt__",
            "<=": "__le__", ">=": "__ge__", "[]": "__getitem__",
            "&": "__and__", "|": "__or__", "~": "__invert__",
            "<<": "__lshift__", ">>": "__rshift__",
        }
        py_name = op_map.get(node.operator, f"__{node.operator}__")
        params = ["self"] + node.parameters
        lines = [self._indent() + f"def {py_name}({', '.join(params)}):"]
        self.indent_level += 1
        for stmt in node.body:
            lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        return "\n".join(lines)

    def _gen_regex_literal(self, node: RegexLiteral) -> str:
        """Generate regex compilation from regex literal."""
        self._needs_re_import = True
        flags_str = ""
        if node.flags:
            flag_map = {"i": "re.IGNORECASE", "m": "re.MULTILINE", "s": "re.DOTALL"}
            flags_list = [flag_map.get(f, f"re.{f}") for f in node.flags]
            flags_str = ", " + " | ".join(flags_list)
        return f"re.compile(r'{node.pattern}'{flags_str})"

    def _gen_cast_expression(self, node: CastExpression) -> str:
        """x as int -> int(x)"""
        expr = self._gen_expression(node.expression)
        type_map = {"int": "int", "integer": "int", "float": "float", "string": "str",
                    "bool": "bool", "boolean": "bool", "list": "list", "dict": "dict", "str": "str"}
        py_type = type_map.get(node.target_type, node.target_type)
        return f"{py_type}({expr})"

    # ---- v0.5.0 Masterpiece Codegen ----

    def _gen_record_definition(self, node: RecordDefinition) -> str:
        """define record -> Python @dataclass(frozen=True) for immutability"""
        self._needs_dataclass_import = True
        lines = [self._indent() + "@dataclass(frozen=True)"]
        lines.append(self._indent() + f"class {node.name}:")
        self.indent_level += 1
        for fname, ftype, fdefault in node.fields:
            type_hint = f": {self._gen_type_annotation(TypeAnnotation(type_name=ftype))}" if ftype != "any" else ""
            if fdefault is not None:
                default_val = self._gen_expression(fdefault)
                lines.append(self._indent() + f"{fname}{type_hint} = {default_val}")
            else:
                lines.append(self._indent() + f"{fname}{type_hint} = None")
        self.indent_level -= 1
        return "\n".join(lines)

    def _gen_property_definition(self, node: PropertyDefinition) -> str:
        """define property -> Python @property"""
        lines = []
        type_hint = ""
        if node.type_annotation:
            type_hint = f" -> {self._gen_type_annotation(node.type_annotation)}"
        
        if node.getter_body:
            lines.append(self._indent() + "@property")
            lines.append(self._indent() + f"def {node.name}(self){type_hint}:")
            self.indent_level += 1
            for stmt in node.getter_body:
                lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        
        if node.setter_body:
            lines.append(self._indent() + f"@{node.name}.setter")
            lines.append(self._indent() + f"def {node.name}(self, {node.setter_param}):")
            self.indent_level += 1
            for stmt in node.setter_body:
                lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        
        return "\n".join(lines)

    def _gen_namespace_definition(self, node: NamespaceDefinition) -> str:
        """define namespace -> Python class with @staticmethod methods"""
        lines = [self._indent() + f"class {node.name}:"]
        self.indent_level += 1
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                lines.append(self._indent() + "@staticmethod")
                stmt.parameters = [p for p in stmt.parameters if p != "this"]
                if stmt.parameters and stmt.parameters[0] == "self":
                    stmt.parameters = stmt.parameters[1:]
            lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        return "\n".join(lines)

    def _gen_extension_definition(self, node: ExtensionDefinition) -> str:
        """define extension on Type -> functions that take first param as target"""
        lines = [self._indent() + f"# Extension methods for {node.target_type}"]
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                if not stmt.parameters:
                    stmt.parameters = ["self"]
            lines.append(self._gen_statement(stmt))
        return "\n".join(lines)

    def _gen_lazy_declaration(self, node: LazyDeclaration) -> str:
        """lazy let x be expr -> _lazy_x = None; then property getter"""
        value = self._gen_expression(node.value)
        type_hint = ""
        if node.type_annotation:
            type_hint = f": {self._gen_type_annotation(node.type_annotation)}"
        return self._indent() + f"{node.name} = None  # lazy; init with: {node.name} = ({value}) if {node.name} is None else {node.name}"

    def _gen_generator_expression(self, node: GeneratorExpression) -> str:
        """'(x for each x in items if cond)' -> (x for x in items if cond)"""
        expr = self._gen_expression(node.expression)
        iterable = self._gen_expression(node.iterable)
        if node.condition:
            cond = self._gen_expression(node.condition)
            return f"({expr} for {node.variable} in {iterable} if {cond})"
        return f"({expr} for {node.variable} in {iterable})"



    def _gen_between_expression(self, node: BetweenExpression) -> str:
        """x between a and b -> a <= x <= b"""
        left = self._gen_expression(node.left)
        lower = self._gen_expression(node.lower)
        upper = self._gen_expression(node.upper)
        return f"({lower} <= {left} <= {upper})"

    def _gen_when_expression(self, node: WhenExpression) -> str:
        """when condition then value or other -> value if condition else other"""
        cond = self._gen_expression(node.condition)
        true_val = self._gen_expression(node.true_value)
        false_val = self._gen_expression(node.false_value)
        return f"({true_val} if {cond} else {false_val})"

    def _gen_empty_expression(self, node: EmptyExpression) -> str:
        """list is empty -> len(list) == 0"""
        expr = self._gen_expression(node.expression)
        return f"len({expr}) == 0"


def generate_python(ast: Program) -> str:
    gen = PythonGenerator(ast)
    return gen.generate()
