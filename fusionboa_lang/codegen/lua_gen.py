"""
FusionBoa → Lua Code Generator

Translates a FusionBoa AST into equivalent Lua source code.
Supports all Fusion features.
"""

from ..parser.ast_nodes import *


class LuaGenerator:
    """Generates Lua code from a FusionBoa AST."""

    def __init__(self, ast: Program):
        self.ast = ast
        self.indent_level = 0

    def _indent(self) -> str:
        return "  " * self.indent_level

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
            ContinueStatement: lambda n: self._indent() + "-- continue (not natively supported in Lua)",
            PassStatement: lambda n: self._indent() + "-- pass",
            ImportStatement: self._gen_import_statement,
            ExportStatement: self._gen_export_statement,
            TryStatement: self._gen_try_statement,
            PrintStatement: self._gen_print_statement,
            InputStatement: self._gen_input_statement,
            DoWhileLoop: self._gen_do_while_loop,
            EnumDefinition: self._gen_enum_definition,
            DeferStatement: lambda n: self._indent() + "-- deferred",
            GuardStatement: self._gen_guard_statement,
            DestructuringDeclaration: self._gen_destructuring,
            IncrementExpression: lambda n: self._indent() + f"{n.target} = {n.target} + 1",
            DecrementExpression: lambda n: self._indent() + f"{n.target} = {n.target} - 1",
            WithStatement: self._gen_with_statement,
            DecoratorStatement: lambda n: self._indent() + f"-- @{n.name}",
            StaticMethodDeclaration: self._gen_static_method,
            # v0.5.0 Masterpiece
            RecordDefinition: self._gen_record_definition,
            PropertyDefinition: self._gen_property_definition,
            ExtensionDefinition: self._gen_extension_definition,
            # v0.9.1+ Universal Polyglot
            SetLiteral: self._gen_set_stmt,
            TupleLiteral: self._gen_tuple_stmt,
            MultiReturnStatement: self._gen_multi_return,
            YieldFromStatement: lambda n: f"-- yield from: {self._gen_expression(n.iterable)}",
            GoStatement: lambda n: f"-- goroutine: {n.name or 'anonymous'} (use coroutine.create)",
            ChannelDeclaration: lambda n: f"-- channel: {n.name}",
            ChannelSelect: lambda n: f"-- select {len(n.cases)} channels",
            ChannelClose: lambda n: f"-- channel close",
            SynchronizedBlock: lambda n: self._indent() + f"-- synchronized",
            AsyncWithStatement: lambda n: self._indent() + f"-- async with",
            ModuleDefinition: self._gen_module_def,
            MixinStatement: self._gen_mixin,
            ObjectDefinition: lambda n: self._indent() + f"-- object {n.name} (singleton)",
            ActorDefinition: lambda n: self._indent() + f"-- actor {n.name}",
            SealedClassDefinition: lambda n: self._indent() + f"-- sealed class {n.name}",
            NewExpression: lambda n: self._indent() + f"-- new {n.type_name}",
            DeleteExpression: lambda n: self._indent() + f"-- delete {n.target}",
            GlobalStatement: lambda n: self._indent() + f"-- global {', '.join(n.names)}",
            AtomicCounter: lambda n: self._indent() + f"{n.name} = {{ __value = {self._gen_expression(n.initial_value) if n.initial_value else '0'} }}  -- atomic",
        }
        gen_func = gen_map.get(type(node))
        if gen_func: return gen_func(node)
        return f"-- Unknown: {type(node).__name__}"

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
        if isinstance(node, LengthExpression): return f"#{self._gen_expression(node.expression)}"
        if isinstance(node, AwaitExpression): return self._gen_expression(node.expression)
        if isinstance(node, ListComprehension): return self._gen_list_comprehension(node)
        if isinstance(node, StringInterpolation): return self._gen_string_interpolation(node)
        if isinstance(node, SpreadElement): return f"unpack({self._gen_expression(node.expression)})"
        if isinstance(node, KeywordArgument): return f"{node.name} = {self._gen_expression(node.value)}"
        if isinstance(node, RangeLiteral):
            return f"__fusionboa_range({self._gen_expression(node.start)}, {self._gen_expression(node.end)})"
        if isinstance(node, InExpression): return f"__fusionboa_contains({self._gen_expression(node.right)}, {self._gen_expression(node.left)})"
        if isinstance(node, IsExpression): return f"(type({self._gen_expression(node.left)}) == '{self._gen_expression(node.right)}')"
        if isinstance(node, DictComprehension): return f"-- dict comp"
        if isinstance(node, MultiLineString): return self._gen_literal(Literal(node.value))
        if isinstance(node, SliceExpression): return f"-- slice"
        if isinstance(node, GeneratorExpression): return f"-- generator: {node.variable}"
        if isinstance(node, IncrementExpression): return f"{node.target} = {node.target} + 1"
        if isinstance(node, DecrementExpression): return f"{node.target} = {node.target} - 1"
        # v0.9.1+ Expression nodes
        if isinstance(node, SetLiteral):
            el = ", ".join(f"[{self._gen_expression(e)}] = true" for e in node.elements)
            return "{" + el + "}"
        if isinstance(node, TupleLiteral):
            el = ", ".join(self._gen_expression(e) for e in node.elements)
            return "{" + el + "}"
        if isinstance(node, SymbolLiteral): return f"/* :{node.name} */"
        if isinstance(node, BlockExpression): return f"/* block */"
        if isinstance(node, JsxElement): return f"/* JSX:{node.tag} */"
        if isinstance(node, HookCall): return f"/* {node.hook_name}() */"
        if isinstance(node, NewExpression): return f"/* new */"
        if isinstance(node, DeleteExpression): return f"/* delete {node.target} */"
        if isinstance(node, BroadcastExpression): return f"/* broadcast */"
        if isinstance(node, VectorizeExpression): return f"/* vectorize */"
        if isinstance(node, FormulaExpression): return f"/* formula */"
        if isinstance(node, KeyOfExpression): return f"/* keyof {node.target_type} */"
        if isinstance(node, TemplateLiteral): return f"/* template literal */"
        if isinstance(node, YieldToBlock): return f"/* yield to block */"
        return f"-- Unknown: {type(node).__name__}"

    def _gen_literal(self, node: Literal) -> str:
        if node.value is None: return "nil"
        if node.value is True: return "true"
        if node.value is False: return "false"
        if isinstance(node.value, str):
            return '"' + node.value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'
        return str(node.value)

    def _gen_binary_op(self, node: BinaryOp) -> str:
        op_map = {"and": "and", "or": "or", "^": "^",
                  "==": "==", "!=": "~=", "<": "<", ">": ">",
                  "<=": "<=", ">=": ">=", "+": "+", "-": "-",
                  "*": "*", "/": "/", "%": "%",
                  "&": "/* & */", "|": "/* | */", "<<": "/* << */", ">>": "/* >> */",
                  "//": "//"}
        lua_op = op_map.get(node.operator, node.operator)
        left = self._gen_expression(node.left)
        right = self._gen_expression(node.right)
        # Null-coalescing: a ?? b -> (a ~= nil and a or b)
        if node.operator == "??":
            return f"({left} ~= nil and {left} or {right})"
        return f"({left} {lua_op} {right})"

    def _gen_unary_op(self, node: UnaryOp) -> str:
        op_map = {"neg": "-", "not": "not ", "~": "/* ~ */"}
        lua_op = op_map.get(node.operator, node.operator)
        operand = self._gen_expression(node.operand)
        return f"({lua_op}{operand})"

    def _gen_call(self, node: Call) -> str:
        callee = self._gen_expression(node.callee)
        args = ", ".join(self._gen_expression(a) for a in node.arguments)
        if isinstance(node.callee, Identifier):
            if node.callee.name == "print":
                return f"print({args})"
            if node.callee.name == "input":
                return f"io.read({args})"
            if node.callee.name == "str":
                return f"tostring({args})"
        return f"{callee}({args})"

    def _gen_attribute(self, node: Attribute) -> str:
        return f"{self._gen_expression(node.object)}.{node.attribute}"

    def _gen_index(self, node: Index) -> str:
        return f"{self._gen_expression(node.object)}[{self._gen_expression(node.index)}]"

    def _gen_list_literal(self, node: ListLiteral) -> str:
        elements = ", ".join(self._gen_expression(e) for e in node.elements)
        return "{" + elements + "}"

    def _gen_dict_literal(self, node: DictLiteral) -> str:
        pairs = ", ".join(f"[{self._gen_expression(k)}] = {self._gen_expression(v)}" for k, v in node.pairs)
        return "{" + pairs + "}"

    def _gen_lambda(self, node: Lambda) -> str:
        params = ", ".join(node.parameters)
        body = self._gen_expression(node.body)
        return f"function({params}) return {body} end"

    def _gen_ternary(self, node: Ternary) -> str:
        return f"({self._gen_expression(node.condition)} and {self._gen_expression(node.true_value)} or {self._gen_expression(node.false_value)})"

    def _gen_list_comprehension(self, node: ListComprehension) -> str:
        # Lua doesn't have native list comprehension, approximate with a function
        expr = self._gen_expression(node.expression)
        iterable = self._gen_expression(node.iterable)
        result = f"__fusionboa_list_comp({iterable}, function({node.variable}) return {expr} end"
        if node.condition:
            result += f", function({node.variable}) return {self._gen_expression(node.condition)} end"
        result += ")"
        return result

    def _gen_string_interpolation(self, node: StringInterpolation) -> str:
        parts = []
        for p in node.parts:
            if isinstance(p, Literal) and isinstance(p.value, str):
                parts.append('"' + p.value + '"')
            else:
                parts.append(f"tostring({self._gen_expression(p)})")
        return "(" + " .. ".join(parts) + ")"

    def _gen_expression_statement(self, node: ExpressionStatement) -> str:
        return self._indent() + self._gen_expression(node.expression)

    def _gen_variable_declaration(self, node: VariableDeclaration) -> str:
        return self._indent() + f"local {node.name} = {self._gen_expression(node.value)}"

    def _gen_const_declaration(self, node: ConstDeclaration) -> str:
        return self._indent() + f"local {node.name} = {self._gen_expression(node.value)}  -- const"

    def _gen_assignment(self, node: Assignment) -> str:
        return self._indent() + f"{node.target} = {self._gen_expression(node.value)}"

    def _gen_augmented_assignment(self, node: AugmentedAssignment) -> str:
        val = self._gen_expression(node.value)
        target = node.target
        if node.operator == "||": return self._indent() + f"{target} = {target} or {val}"
        if node.operator == "&&": return self._indent() + f"{target} = {target} and {val}"
        if node.operator == "??": return self._indent() + f"{target} = {target} or {val}  -- null coalescing"
        return self._indent() + f"{target} = {target} {node.operator} {val}"

    def _gen_if_statement(self, node: IfStatement) -> str:
        lines = [self._indent() + f"if {self._gen_expression(node.condition)} then"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        for elif_cond, elif_body in node.elif_branches:
            lines.append(self._indent() + f"elseif {self._gen_expression(elif_cond)} then")
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
        lines = [self._indent() + f"local __match_val = {self._gen_expression(node.expression)}"]
        first = True
        for pattern, body in node.cases:
            kw = "if" if first else "elseif"
            lines.append(self._indent() + f"{kw} __match_val == {self._gen_expression(pattern)} then")
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
            lines.append(self._indent() + f"for _, {node.variable} in ipairs({self._gen_expression(node.iterable)}) do")
        else:
            from_v = self._gen_expression(node.range_from)
            to_v = self._gen_expression(node.range_to)
            lines.append(self._indent() + f"for {node.variable} = {from_v}, {to_v} do")
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_repeat_loop(self, node: RepeatLoop) -> str:
        lines = [self._indent() + f"for __fusionboa_i = 1, {self._gen_expression(node.times)} do"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_while_loop(self, node: WhileLoop) -> str:
        lines = [self._indent() + f"while {self._gen_expression(node.condition)} do"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_function_definition(self, node: FunctionDefinition) -> str:
        lines = []
        params = list(node.parameters)
        if node.has_rest_param:
            params.append("...")
        param_strs = []
        for p in params:
            if p in node.defaults:
                param_strs.append(f"{p}")
            else:
                param_strs.append(p)
        func_name = "new" if node.name == "init" else node.name
        lines.append(self._indent() + f"function {func_name}({', '.join(param_strs)})")
        self.indent_level += 1
        # Handle defaults at start of function
        if node.defaults:
            for p, default in node.defaults.items():
                lines.append(self._indent() + f"{p} = {p} or {self._gen_expression(default)}")
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_class_definition(self, node: ClassDefinition) -> str:
        lines = [self._indent() + f"-- Lua class: {node.name} (prototype-based)"]
        lines.append(self._indent() + f"{node.name} = {{}}")
        if node.parent:
            lines.append(self._indent() + f"-- inherits from: {node.parent}")
            lines.append(self._indent() + f"setmetatable({node.name}, {{__index = {node.parent}}})")
        lines.append(self._indent() + f"{node.name}.__index = {node.name}")
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                lines.append(self._indent() + f"function {node.name}:{stmt.name}({', '.join(stmt.parameters)})")
                self.indent_level += 1
                for s in stmt.body: lines.append(self._gen_statement(s))
                self.indent_level -= 1
                lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_return_statement(self, node: ReturnStatement) -> str:
        if node.value:
            return self._indent() + f"return {self._gen_expression(node.value)}"
        return self._indent() + "return"

    def _gen_yield_statement(self, node: YieldStatement) -> str:
        if node.value:
            return self._indent() + f"-- yield: {self._gen_expression(node.value)}  (use coroutine.yield)"
        return self._indent() + "-- yield"

    def _gen_import_statement(self, node: ImportStatement) -> str:
        if node.items:
            items = ", ".join(node.items)
            return self._indent() + f'-- import {items} from {node.module} (Lua: use require("{node.module}"))'
        return self._indent() + f'local {node.module} = require("{node.module}")'

    def _gen_export_statement(self, node: ExportStatement) -> str:
        return self._gen_statement(node.declaration) + "  -- export"

    def _gen_try_statement(self, node: TryStatement) -> str:
        lines = []
        # Lua uses pcall for error handling
        lines.append(self._indent() + "local __ok, __err = pcall(function()")
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "end)")
        if node.catch_body:
            lines.append(self._indent() + "if not __ok then")
            self.indent_level += 1
            if node.catch_var:
                lines.append(self._indent() + f"local {node.catch_var} = __err")
            for stmt in node.catch_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
            lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_print_statement(self, node: PrintStatement) -> str:
        if node.expression:
            return self._indent() + f"print({self._gen_expression(node.expression)})"
        return self._indent() + "print()"

    def _gen_input_statement(self, node: InputStatement) -> str:
        if node.target:
            if node.prompt:
                return self._indent() + f'io.write({self._gen_literal(Literal(value=node.prompt))}); local {node.target} = io.read()'
            return self._indent() + f"local {node.target} = io.read()"
        return self._indent() + "io.read()"

    def _gen_guard_statement(self, node):
        cond = self._gen_expression(node.condition)
        lines = [self._indent() + f"if not ({cond}) then"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        lines.append(self._indent() + "return")
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_do_while_loop(self, node):
        lines = [self._indent() + "repeat"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + f"until {self._gen_expression(node.condition)}")
        return "\n".join(lines)

    def _gen_enum_definition(self, node):
        lines = [self._indent() + f"-- enum {node.name}"]
        lines.append(self._indent() + f"{node.name} = {{}}")
        for i, member in enumerate(node.members):
            lines.append(self._indent() + f"{node.name}.{member} = {i}")
        return "\n".join(lines)

    def _gen_with_statement(self, node):
        r = self._gen_expression(node.resource)
        v = node.variable if node.variable else "_res"
        lines = [self._indent() + f"local {v} = {r}  -- with"]
        for s in node.body: lines.append(self._gen_statement(s))
        return "\n".join(lines)

    def _gen_static_method(self, node):
        return self._gen_statement(node.declaration) + "  -- static"

    def _gen_destructuring(self, node):
        targets = ", ".join(node.targets)
        value = self._gen_expression(node.value)
        return self._indent() + f"local {targets} = {value}"

    # ---- v0.5.0 Masterpiece Codegen ----

    def _gen_record_definition(self, node: RecordDefinition) -> str:
        """define record -> Lua table with metatable for immutability"""
        lines = [self._indent() + f"-- Record: {node.name}"]
        lines.append(self._indent() + f"local {node.name} = {{}}")
        lines.append(self._indent() + f"function {node.name}:new({', '.join(fname for fname, _, _ in node.fields)})")
        self.indent_level += 1
        lines.append(self._indent() + "local obj = {")
        self.indent_level += 1
        for fname, _, fdefault in node.fields:
            default = f" = {self._gen_expression(fdefault)}" if fdefault is not None else " = nil"
            lines.append(self._indent() + f"{fname}{default},")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        lines.append(self._indent() + f"setmetatable(obj, {{ __index = {node.name} }})")
        lines.append(self._indent() + "return obj")
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_property_definition(self, node: PropertyDefinition) -> str:
        """define property -> Lua metatable-based getter/setter"""
        lines = [self._indent() + f"-- Property: {node.name}"]
        if node.getter_body:
            lines.append(self._indent() + f"function __mt_{node.name}_getter(self)")
            self.indent_level += 1
            for stmt in node.getter_body:
                lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
            lines.append(self._indent() + "end")
        if node.setter_body:
            lines.append(self._indent() + f"function __mt_{node.name}_setter(self, {node.setter_param})")
            self.indent_level += 1
            for stmt in node.setter_body:
                lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
            lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_extension_definition(self, node: ExtensionDefinition) -> str:
        """define extension on Type -> Lua table function addition"""
        lines = [self._indent() + f"-- Extension methods for {node.target_type}"]
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                params = ", ".join(stmt.parameters)
                lines.append(self._indent() + f"function {node.target_type}.{stmt.name}(self, {params})")
                self.indent_level += 1
                for s in stmt.body:
                    lines.append(self._gen_statement(s))
                self.indent_level -= 1
                lines.append(self._indent() + "end")
            else:
                lines.append(self._gen_statement(stmt))
        return "\n".join(lines)


    # ---- v0.9.1+ Handler Methods ----

    def _gen_set_stmt(self, node):
        el = ", ".join(f"[{str(e)}] = true" for e in node.elements)
        return self._indent() + "{" + el + "}  -- set"

    def _gen_tuple_stmt(self, node):
        el = ", ".join(str(e) for e in node.elements)
        return self._indent() + "{" + el + "}  -- tuple"

    def _gen_multi_return(self, node):
        vals = ", ".join(self._gen_expression(v) for v in node.values)
        return self._indent() + f"return {vals}"

    def _gen_module_def(self, node):
        lines = [self._indent() + f"-- Module: {node.name}"]
        lines.append(self._indent() + f"{node.name} = {{}}")
        for s in node.body: lines.append(self._gen_statement(s))
        return "\n".join(lines)

    def _gen_mixin(self, node):
        return self._indent() + f"-- {node.mixin_type} {node.mixin_name} (Lua: use metatable mixin pattern)"


def generate_lua(ast: Program) -> str:
    gen = LuaGenerator(ast)
    return gen.generate()
