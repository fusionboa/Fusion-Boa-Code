"""
FusionBoa → Julia Code Generator

Translates a FusionBoa AST into equivalent Julia source code.
Supports all Fusion features.
"""

from ..parser.ast_nodes import *


class JuliaGenerator:
    """Generates Julia code from a FusionBoa AST."""

    def __init__(self, ast: Program):
        self.ast = ast
        self.indent_level = 0

    def _indent(self) -> str:
        return "    " * self.indent_level

    def generate(self) -> str:
        lines = []
        for stmt in self.ast.statements:
            lines.append(self._gen_statement(stmt))
        return "\n".join(lines)

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
            RepeatLoop: self._gen_repeat_loop,
            WhileLoop: self._gen_while_loop,
            FunctionDefinition: self._gen_function_definition,
            ClassDefinition: self._gen_class_definition,
            ReturnStatement: self._gen_return_statement,
            YieldStatement: self._gen_yield_statement,
            BreakStatement: lambda n: self._indent() + "break",
            ContinueStatement: lambda n: self._indent() + "continue",
            PassStatement: lambda n: self._indent() + "# pass",
            ImportStatement: self._gen_import_statement,
            ExportStatement: self._gen_export_statement,
            TryStatement: self._gen_try_statement,
            PrintStatement: self._gen_print_statement,
            InputStatement: self._gen_input_statement,
            DoWhileLoop: self._gen_do_while_loop,
            EnumDefinition: self._gen_enum_definition,
            DeferStatement: lambda n: self._indent() + "# deferred",
            GuardStatement: self._gen_guard_statement_wrapper,
            DestructuringDeclaration: self._gen_destructuring,
            IncrementExpression: lambda n: self._indent() + f"{n.target} += 1",
            DecrementExpression: lambda n: self._indent() + f"{n.target} -= 1",
            WithStatement: self._gen_with_statement,
            DecoratorStatement: lambda n: self._indent() + f"# @{n.name}",
            StaticMethodDeclaration: lambda n: self._gen_statement(n.declaration).replace("function ", "# static\nfunction ", 1),
            # v0.5.0 Masterpiece
            RecordDefinition: self._gen_record_definition,
            PropertyDefinition: self._gen_property_definition,
            ExtensionDefinition: self._gen_extension_definition,
        }
        gen_func = gen_map.get(type(node))
        if gen_func: return gen_func(node)
        return f"# Unknown: {type(node).__name__}"

    def _gen_expression(self, node: ASTNode) -> str:
        if node is None: return ""
        if isinstance(node, Literal): return self._gen_literal(node)
        if isinstance(node, Identifier): return node.name
        if isinstance(node, BinaryOp): return self._gen_binary_op(node)
        if isinstance(node, UnaryOp): return self._gen_unary_op(node)
        if isinstance(node, Call): return self._gen_call(node)
        if isinstance(node, Attribute): return self._gen_attribute(node)
        if isinstance(node, Index): return self._gen_index(node)
        if isinstance(node, ListLiteral): return self._gen_list_literal(node)
        if isinstance(node, DictLiteral): return self._gen_dict_literal(node)
        if isinstance(node, Lambda): return self._gen_lambda(node)
        if isinstance(node, Ternary): return self._gen_ternary(node)
        if isinstance(node, LengthExpression): return f"length({self._gen_expression(node.expression)})"
        if isinstance(node, AwaitExpression): return f"@async {self._gen_expression(node.expression)}"
        if isinstance(node, ListComprehension): return self._gen_list_comprehension(node)
        if isinstance(node, StringInterpolation): return self._gen_string_interpolation(node)
        if isinstance(node, SpreadElement): return f"{self._gen_expression(node.expression)}..."
        if isinstance(node, KeywordArgument): return f"{node.name}={self._gen_expression(node.value)}"
        if isinstance(node, RangeLiteral):
            return f"({self._gen_expression(node.start)}:{self._gen_expression(node.end)})"
        if isinstance(node, InExpression): return f"({self._gen_expression(node.left)} in {self._gen_expression(node.right)})"
        if isinstance(node, IsExpression): return f"({self._gen_expression(node.left)} isa {self._gen_expression(node.right)})"
        if isinstance(node, DictComprehension): return f"# dict comp: {node.variable}"
        if isinstance(node, MultiLineString): return self._gen_literal(Literal(node.value))
        if isinstance(node, SliceExpression): return f"# slice"
        if isinstance(node, GeneratorExpression): return f"# generator: {node.variable}"
        if isinstance(node, IncrementExpression): return f"{node.target} += 1"
        if isinstance(node, DecrementExpression): return f"{node.target} -= 1"
        return f"# Unknown: {type(node).__name__}"

    def _gen_literal(self, node: Literal) -> str:
        if node.value is None: return "nothing"
        if node.value is True: return "true"
        if node.value is False: return "false"
        if isinstance(node.value, str):
            return '"' + node.value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'
        return str(node.value)

    def _gen_binary_op(self, node: BinaryOp) -> str:
        op_map = {"and": "&&", "or": "||", "^": "^",
                  "==": "==", "!=": "!=", "<": "<", ">": ">",
                  "<=": "<=", ">=": ">=", "+": "+", "-": "-",
                  "*": "*", "/": "/", "%": "%",
                  "&": "&", "|": "|", "<<": "<<", ">>": ">>", "//": "div"}
        jl_op = op_map.get(node.operator, node.operator)
        left = self._gen_expression(node.left)
        right = self._gen_expression(node.right)
        # Null-coalescing: a ?? b -> coalesce(a, b) or a === nothing ? b : a
        if node.operator == "??":
            return f"(something({left}, {right}))"
        return f"({left} {jl_op} {right})"

    def _gen_unary_op(self, node: UnaryOp) -> str:
        op_map = {"neg": "-", "not": "!", "~": "~"}
        jl_op = op_map.get(node.operator, node.operator)
        operand = self._gen_expression(node.operand)
        return f"({jl_op}{operand})"

    def _gen_call(self, node: Call) -> str:
        callee = self._gen_expression(node.callee)
        args = ", ".join(self._gen_expression(a) for a in node.arguments)
        if isinstance(node.callee, Identifier):
            if node.callee.name == "print":
                return f"println({args})"
            if node.callee.name == "input":
                return f"readline({args})"
        return f"{callee}({args})"

    def _gen_attribute(self, node: Attribute) -> str:
        return f"{self._gen_expression(node.object)}.{node.attribute}"

    def _gen_index(self, node: Index) -> str:
        return f"{self._gen_expression(node.object)}[{self._gen_expression(node.index)}]"

    def _gen_list_literal(self, node: ListLiteral) -> str:
        elements = ", ".join(self._gen_expression(e) for e in node.elements)
        return f"[{elements}]"

    def _gen_dict_literal(self, node: DictLiteral) -> str:
        pairs = ", ".join(f"{self._gen_expression(k)} => {self._gen_expression(v)}" for k, v in node.pairs)
        return f"Dict({pairs})"

    def _gen_lambda(self, node: Lambda) -> str:
        params = ", ".join(node.parameters)
        body = self._gen_expression(node.body)
        return f"({params}) -> {body}"

    def _gen_ternary(self, node: Ternary) -> str:
        return f"({self._gen_expression(node.condition)} ? {self._gen_expression(node.true_value)} : {self._gen_expression(node.false_value)})"

    def _gen_list_comprehension(self, node: ListComprehension) -> str:
        expr = self._gen_expression(node.expression)
        iterable = self._gen_expression(node.iterable)
        if node.condition:
            cond = self._gen_expression(node.condition)
            return f"[{expr} for {node.variable} in {iterable} if {cond}]"
        return f"[{expr} for {node.variable} in {iterable}]"

    def _gen_string_interpolation(self, node: StringInterpolation) -> str:
        parts = []
        for p in node.parts:
            if isinstance(p, Literal) and isinstance(p.value, str):
                parts.append(p.value)
            else:
                parts.append("$(" + self._gen_expression(p) + ")")
        return '"' + "".join(parts) + '"'

    def _gen_expression_statement(self, node: ExpressionStatement) -> str:
        return self._indent() + self._gen_expression(node.expression)

    def _gen_variable_declaration(self, node: VariableDeclaration) -> str:
        return self._indent() + f"{node.name} = {self._gen_expression(node.value)}"

    def _gen_const_declaration(self, node: ConstDeclaration) -> str:
        return self._indent() + f"const {node.name} = {self._gen_expression(node.value)}"

    def _gen_assignment(self, node: Assignment) -> str:
        return self._indent() + f"{node.target} = {self._gen_expression(node.value)}"

    def _gen_augmented_assignment(self, node: AugmentedAssignment) -> str:
        val = self._gen_expression(node.value)
        target = node.target
        if node.operator == "||": return self._indent() + f"{target} = {target} || {val}"
        if node.operator == "&&": return self._indent() + f"{target} = {target} && {val}"
        if node.operator == "??": return self._indent() + f"{target} = {target} === nothing ? {val} : {target}"
        return self._indent() + f"{target} {node.operator}= {val}"

    def _gen_if_statement(self, node: IfStatement) -> str:
        lines = [self._indent() + f"if {self._gen_expression(node.condition)}"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        for elif_cond, elif_body in node.elif_branches:
            lines.append(self._indent() + f"elseif {self._gen_expression(elif_cond)}")
            self.indent_level += 1
            for stmt in elif_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        if node.else_body:
            lines.append(self._indent() + "else")
            self.indent_level += 1
            for stmt in node.else_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_match_statement(self, node: MatchStatement) -> str:
        lines = [self._indent() + f"# match {self._gen_expression(node.expression)}"]
        lines.append(self._indent() + f"__match_val = {self._gen_expression(node.expression)}")
        first = True
        for pattern, body in node.cases:
            kw = "if" if first else "elseif"
            lines.append(self._indent() + f"{kw} __match_val == {self._gen_expression(pattern)}")
            self.indent_level += 1
            for stmt in body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
            first = False
        if node.default_body:
            lines.append(self._indent() + "else")
            self.indent_level += 1
            for stmt in node.default_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_for_loop(self, node: ForLoop) -> str:
        lines = []
        if node.iterable:
            lines.append(self._indent() + f"for {node.variable} in {self._gen_expression(node.iterable)}")
        else:
            from_v = self._gen_expression(node.range_from)
            to_v = self._gen_expression(node.range_to)
            lines.append(self._indent() + f"for {node.variable} in {from_v}:{to_v}")
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_repeat_loop(self, node: RepeatLoop) -> str:
        lines = [self._indent() + f"for __fusionboa_i in 1:{self._gen_expression(node.times)}"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_while_loop(self, node: WhileLoop) -> str:
        lines = [self._indent() + f"while {self._gen_expression(node.condition)}"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_function_definition(self, node: FunctionDefinition) -> str:
        lines = []
        params = list(node.parameters)
        if node.has_rest_param:
            params.append(f"{node.rest_param_name}...")
        param_strs = []
        for p in params:
            if p in node.defaults:
                param_strs.append(f"{p}={self._gen_expression(node.defaults[p])}")
            else:
                param_strs.append(p)
        lines.append(self._indent() + f"function {node.name}({', '.join(param_strs)})")
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_class_definition(self, node: ClassDefinition) -> str:
        lines = []
        if node.parent:
            lines.append(self._indent() + f"mutable struct {node.name} <: {node.parent}")
        else:
            lines.append(self._indent() + f"mutable struct {node.name}")
        # Extract fields from init function
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition) and stmt.name == "init":
                for p in stmt.parameters:
                    if p != "this":
                        lines.append(self._indent() + f"    {p}::Any")
        lines.append(self._indent() + "end")
        lines.append("")
        # Generate methods
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                if stmt.name == "init":
                    # Constructor
                    params = [p for p in stmt.parameters if p != "this"]
                    param_strs = ", ".join(params)
                    lines.append(self._indent() + f"function {node.name}({param_strs})")
                    lines.append(self._indent() + f"    obj = new({', '.join(params)})")
                    lines.append(self._indent() + "    return obj")
                    lines.append(self._indent() + "end")
                else:
                    params = [p for p in stmt.parameters if p != "this"]
                    param_strs = ", ".join(params)
                    lines.append(self._indent() + f"function {stmt.name}(self:: {node.name}, {param_strs})")
                    self.indent_level += 1
                    for s in stmt.body: lines.append(self._gen_statement(s))
                    self.indent_level -= 1
                    lines.append(self._indent() + "end")
            else:
                lines.append(self._gen_statement(stmt))
        return "\n".join([l for l in lines if l is not None])

    def _gen_return_statement(self, node: ReturnStatement) -> str:
        if node.value:
            return self._indent() + f"return {self._gen_expression(node.value)}"
        return self._indent() + "return"

    def _gen_yield_statement(self, node: YieldStatement) -> str:
        if node.value:
            return self._indent() + f"# yield {self._gen_expression(node.value)}"
        return self._indent() + "# yield"

    def _gen_import_statement(self, node: ImportStatement) -> str:
        if node.items:
            items = ", ".join(node.items)
            return self._indent() + f"using {node.module}: {items}"
        return self._indent() + f"using {node.module}"

    def _gen_export_statement(self, node: ExportStatement) -> str:
        return self._gen_statement(node.declaration) + "  # export"

    def _gen_try_statement(self, node: TryStatement) -> str:
        lines = [self._indent() + "try"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        if node.catch_body:
            if node.catch_var:
                lines.append(self._indent() + f"catch {node.catch_var}")
            else:
                lines.append(self._indent() + "catch")
            self.indent_level += 1
            for stmt in node.catch_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        if node.finally_body:
            lines.append(self._indent() + "finally")
            self.indent_level += 1
            for stmt in node.finally_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_print_statement(self, node: PrintStatement) -> str:
        if node.expression:
            return self._indent() + f"println({self._gen_expression(node.expression)})"
        return self._indent() + "println()"

    def _gen_input_statement(self, node: InputStatement) -> str:
        if node.target:
            if node.prompt:
                return self._indent() + f'print({self._gen_literal(Literal(value=node.prompt))}); {node.target} = readline()'
            return self._indent() + f"{node.target} = readline()"
        return self._indent() + "readline()"

    def _gen_do_while_loop(self, node):
        lines = [self._indent() + "while true"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        lines.append(self._indent() + f"if !({self._gen_expression(node.condition)}) break end")
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_guard_statement_wrapper(self, node):
        cond = self._gen_expression(node.condition)
        lines = [self._indent() + f"if !({cond})"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        lines.append(self._indent() + "return")
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_enum_definition(self, node):
        lines = [self._indent() + f"@enum {node.name} begin"]
        for i, member in enumerate(node.members):
            lines.append(self._indent() + f"    {member} = {i}")
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_with_statement(self, node):
        r = self._gen_expression(node.resource)
        lines = [self._indent() + f"# with: {r}"]
        for s in node.body: lines.append(self._gen_statement(s))
        return "\n".join(lines)

    def _gen_destructuring(self, node):
        targets = ", ".join(node.targets)
        value = self._gen_expression(node.value)
        return self._indent() + f"{targets} = {value}"

    # ---- v0.5.0 Masterpiece Codegen ----

    def _gen_record_definition(self, node: RecordDefinition) -> str:
        """define record -> Julia immutable struct"""
        lines = [self._indent() + f"struct {node.name}"]
        self.indent_level += 1
        for fname, ftype, fdefault in node.fields:
            jl_type = {"int": "Int", "integer": "Int", "float": "Float64",
                       "string": "String", "bool": "Bool", "boolean": "Bool",
                       "list": "Vector{Any}", "dict": "Dict{String,Any}",
                       "any": "Any"}.get(ftype, "Any")
            default = f" = {self._gen_expression(fdefault)}" if fdefault is not None else ""
            lines.append(self._indent() + f"{fname}::{jl_type}{default}")
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_property_definition(self, node: PropertyDefinition) -> str:
        """define property -> Julia getter/setter functions"""
        lines = []
        if node.getter_body:
            lines.append(self._indent() + f"function {node.name}(self)")
            self.indent_level += 1
            for stmt in node.getter_body:
                lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
            lines.append(self._indent() + "end")
        if node.setter_body:
            lines.append(self._indent() + f"function set_{node.name}!(self, {node.setter_param})")
            self.indent_level += 1
            for stmt in node.setter_body:
                lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
            lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_extension_definition(self, node: ExtensionDefinition) -> str:
        """define extension on Type -> Julia method overloading"""
        lines = [self._indent() + f"# Extension methods for {node.target_type}"]
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                params = ", ".join(stmt.parameters) if stmt.parameters else ""
                lines.append(self._indent() + f"function {stmt.name}(self::{node.target_type}, {params})" if params else self._indent() + f"function {stmt.name}(self::{node.target_type})")
                self.indent_level += 1
                for s in stmt.body:
                    lines.append(self._gen_statement(s))
                self.indent_level -= 1
                lines.append(self._indent() + "end")
        return "\n".join(lines)


def generate_julia(ast: Program) -> str:
    gen = JuliaGenerator(ast)
    return gen.generate()
