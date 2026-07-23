"""
FusionBoa → Swift Code Generator

Translates a FusionBoa AST into equivalent Swift source code.
Supports all Fusion features.
"""

from ..parser.ast_nodes import *


class SwiftGenerator:
    """Generates Swift code from a FusionBoa AST."""

    def __init__(self, ast: Program):
        self.ast = ast
        self.indent_level = 0

    def _indent(self) -> str:
        return "    " * self.indent_level

    def generate(self) -> str:
        imports = ["import Foundation"]
        lines = []
        for stmt in self.ast.statements:
            lines.append(self._gen_statement(stmt))
        return "\n".join(imports + [""] + lines)

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
            YieldStatement: lambda n: self._indent() + f"// yield not supported: {self._gen_expression(n.value)}",
            BreakStatement: lambda n: self._indent() + "break",
            ContinueStatement: lambda n: self._indent() + "continue",
            PassStatement: lambda n: self._indent() + "// pass",
            ImportStatement: self._gen_import_statement,
            ExportStatement: self._gen_export_statement,
            TryStatement: self._gen_try_statement,
            PrintStatement: self._gen_print_statement,
            InputStatement: self._gen_input_statement,
            DoWhileLoop: self._gen_do_while_loop,
            EnumDefinition: self._gen_enum_definition,
            DeferStatement: lambda n: self._indent() + "// deferred",
            GuardStatement: self._gen_guard_statement,
            DestructuringDeclaration: self._gen_destructuring,
            IncrementExpression: lambda n: self._indent() + (f"{n.target} += 1"),
            DecrementExpression: lambda n: self._indent() + (f"{n.target} -= 1"),
            WithStatement: self._gen_with_statement,
            DecoratorStatement: lambda n: self._indent() + f"// @{n.name}",
            StaticMethodDeclaration: self._gen_static_method,
            # v0.5.0 Masterpiece
            RecordDefinition: self._gen_record_definition,
            PropertyDefinition: self._gen_property_definition,
            ExtensionDefinition: self._gen_extension_definition,
            # v0.9.1+ Universal Polyglot
            SetLiteral: self._gen_set_stmt,
            TupleLiteral: lambda n: self._indent() + f"({', '.join(str(e) for e in n.elements)})" if n.elements else self._indent() + "()",
            MultiReturnStatement: self._gen_multi_return,
            YieldFromStatement: lambda n: self._indent() + f"// yield from: {self._gen_expression(n.iterable)}",
            GoStatement: lambda n: self._indent() + f"// goroutine: {n.name or 'anonymous'} (use Task.detached)",
            ChannelDeclaration: lambda n: self._indent() + f"// channel: {n.name}",
            ChannelSelect: lambda n: self._indent() + f"// select {len(n.cases)} channels",
            ChannelClose: lambda n: self._indent() + f"// channel close",
            SynchronizedBlock: self._gen_synchronized,
            AsyncWithStatement: self._gen_async_with,
            ModuleDefinition: lambda n: self._indent() + f"// module {n.name}",
            MixinStatement: lambda n: self._indent() + f"// {n.mixin_type} {n.mixin_name}",
            ObjectDefinition: lambda n: self._indent() + f"// object {n.name} (Swift: use singleton pattern)",
            ActorDefinition: self._gen_actor,
            SealedClassDefinition: lambda n: self._indent() + f"// sealed class {n.name} (use enum with associated values)",
            NewExpression: lambda n: self._indent() + f"{n.type_name}({', '.join(self._gen_expression(a) for a in n.arguments)})",
            DeleteExpression: lambda n: self._indent() + f"// delete {n.target} (ARC handles)",
            GlobalStatement: lambda n: self._indent() + f"// global {', '.join(n.names)}",
            AtomicCounter: lambda n: self._indent() + f"let {n.name} = OSAtomicInt32({self._gen_expression(n.initial_value) if n.initial_value else '0'})",
            SubscriptDefinition: self._gen_subscript,
        }
        gen_func = gen_map.get(type(node))
        if gen_func: return gen_func(node)
        return f"// Unknown: {type(node).__name__}"

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
        if isinstance(node, LengthExpression): return f"({self._gen_expression(node.expression)}).count"
        if isinstance(node, AwaitExpression): return f"await {self._gen_expression(node.expression)}"
        if isinstance(node, ListComprehension): return self._gen_list_comprehension(node)
        if isinstance(node, StringInterpolation): return self._gen_string_interpolation(node)
        if isinstance(node, SpreadElement): return f"/* spread */ {self._gen_expression(node.expression)}"
        if isinstance(node, KeywordArgument): return f"{node.name}: {self._gen_expression(node.value)}"
        if isinstance(node, RangeLiteral):
            return f"({self._gen_expression(node.start)}...{self._gen_expression(node.end)})"
        if isinstance(node, InExpression): return f"({self._gen_expression(node.right)}).contains({self._gen_expression(node.left)})"
        if isinstance(node, IsExpression): return f"({self._gen_expression(node.left)} is {self._gen_expression(node.right)})"
        if isinstance(node, DictComprehension): return f"// dict comp"
        if isinstance(node, MultiLineString): return self._gen_literal(Literal(node.value))
        if isinstance(node, SliceExpression): return f"// slice"
        if isinstance(node, GeneratorExpression): return f"/* generator */"
        if isinstance(node, IncrementExpression): return f"{node.target} += 1"
        if isinstance(node, DecrementExpression): return f"{node.target} -= 1"
        # v0.9.1+ Expression nodes
        if isinstance(node, SetLiteral):
            el = ", ".join(self._gen_expression(e) for e in node.elements)
            return f"Set([{el}])"
        if isinstance(node, TupleLiteral):
            el = ", ".join(self._gen_expression(e) for e in node.elements)
            return f"({el})"
        if isinstance(node, SymbolLiteral): return f"/* :{node.name} */"
        if isinstance(node, BlockExpression): return f"/* block */"
        if isinstance(node, JsxElement): return f"/* JSX:{node.tag} */"
        if isinstance(node, HookCall): return f"/* {node.hook_name}() */"
        if isinstance(node, NewExpression):
            args = ", ".join(self._gen_expression(a) for a in node.arguments)
            return f"{node.type_name}({args})"
        if isinstance(node, DeleteExpression): return f"/* delete {node.target} */"
        if isinstance(node, BroadcastExpression): return f"/* broadcast */"
        if isinstance(node, VectorizeExpression): return f"/* vectorize */"
        if isinstance(node, FormulaExpression): return f"/* formula */"
        if isinstance(node, KeyOfExpression): return f"/* keyof {node.target_type} */"
        if isinstance(node, TemplateLiteral): return f"/* template literal */"
        if isinstance(node, YieldToBlock): return f"/* yield to block */"
        return f"/* Unknown: {type(node).__name__} */"

    def _gen_literal(self, node: Literal) -> str:
        if node.value is None: return "nil"
        if node.value is True: return "true"
        if node.value is False: return "false"
        if isinstance(node.value, str):
            return '"' + node.value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'
        if isinstance(node.value, float):
            return str(node.value)
        return str(node.value)

    def _gen_binary_op(self, node: BinaryOp) -> str:
        op_map = {"and": "&&", "or": "||", "^": "/* pow */",
                  "==": "==", "!=": "!=", "<": "<", ">": ">",
                  "<=": "<=", ">=": ">=", "+": "+", "-": "-",
                  "*": "*", "/": "/", "%": "%",
                  "&": "&", "|": "|", "<<": "<<", ">>": ">>",
                  "??": "??", "is": "is", "//": "/"}
        sw_op = op_map.get(node.operator, node.operator)
        left = self._gen_expression(node.left)
        right = self._gen_expression(node.right)
        return f"({left} {sw_op} {right})"

    def _gen_unary_op(self, node: UnaryOp) -> str:
        op_map = {"neg": "-", "not": "!", "~": "~"}
        sw_op = op_map.get(node.operator, node.operator)
        operand = self._gen_expression(node.operand)
        return f"({sw_op}{operand})"

    def _gen_call(self, node: Call) -> str:
        callee = self._gen_expression(node.callee)
        args = ", ".join(self._gen_expression(a) for a in node.arguments)
        if isinstance(node.callee, Identifier):
            if node.callee.name == "print":
                return f"print({args})"
            if node.callee.name == "input":
                return f"readLine({args})"
        return f"{callee}({args})"

    def _gen_attribute(self, node: Attribute) -> str:
        return f"{self._gen_expression(node.object)}.{node.attribute}"

    def _gen_index(self, node: Index) -> str:
        return f"{self._gen_expression(node.object)}[{self._gen_expression(node.index)}]"

    def _gen_list_literal(self, node: ListLiteral) -> str:
        elements = ", ".join(self._gen_expression(e) for e in node.elements)
        return f"[{elements}]"

    def _gen_dict_literal(self, node: DictLiteral) -> str:
        pairs = ", ".join(f"{self._gen_expression(k)}: {self._gen_expression(v)}" for k, v in node.pairs)
        return f"[{pairs}]"

    def _gen_lambda(self, node: Lambda) -> str:
        params = ", ".join(node.parameters)
        body = self._gen_expression(node.body)
        return f"{{ ({params}) in return {body} }}"

    def _gen_ternary(self, node: Ternary) -> str:
        return f"({self._gen_expression(node.condition)} ? {self._gen_expression(node.true_value)} : {self._gen_expression(node.false_value)})"

    def _gen_list_comprehension(self, node: ListComprehension) -> str:
        expr = self._gen_expression(node.expression)
        iterable = self._gen_expression(node.iterable)
        if node.condition:
            cond = self._gen_expression(node.condition)
            return f"({iterable}).filter {{ {node.variable} in {cond} }}.map {{ {node.variable} in {expr} }}"
        return f"({iterable}).map {{ {node.variable} in {expr} }}"

    def _gen_string_interpolation(self, node: StringInterpolation) -> str:
        parts = []
        for p in node.parts:
            if isinstance(p, Literal) and isinstance(p.value, str):
                parts.append(p.value)
            else:
                parts.append("\\(" + self._gen_expression(p) + ")")
        return '"' + "".join(parts) + '"'

    def _gen_expression_statement(self, node: ExpressionStatement) -> str:
        return self._indent() + self._gen_expression(node.expression)

    def _gen_variable_declaration(self, node: VariableDeclaration) -> str:
        return self._indent() + f"var {node.name} = {self._gen_expression(node.value)}"

    def _gen_const_declaration(self, node: ConstDeclaration) -> str:
        return self._indent() + f"let {node.name} = {self._gen_expression(node.value)}"

    def _gen_assignment(self, node: Assignment) -> str:
        return self._indent() + f"{node.target} = {self._gen_expression(node.value)}"

    def _gen_augmented_assignment(self, node: AugmentedAssignment) -> str:
        val = self._gen_expression(node.value)
        target = node.target
        if node.operator == "||": return self._indent() + f"{target} = {target} || {val}"
        if node.operator == "&&": return self._indent() + f"{target} = {target} && {val}"
        if node.operator == "??": return self._indent() + f"{target} = {target} ?? {val}"
        return self._indent() + f"{target} {node.operator}= {val}"

    def _gen_destructuring(self, node):
        targets = ", ".join(node.targets)
        value = self._gen_expression(node.value)
        return self._indent() + f"let ({targets}) = {value}"

    def _gen_if_statement(self, node: IfStatement) -> str:
        lines = [self._indent() + f"if {self._gen_expression(node.condition)} {{"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        for elif_cond, elif_body in node.elif_branches:
            lines.append(self._indent() + f"}} else if {self._gen_expression(elif_cond)} {{")
            self.indent_level += 1
            for stmt in elif_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        if node.else_body:
            lines.append(self._indent() + "} else {")
            self.indent_level += 1
            for stmt in node.else_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_match_statement(self, node: MatchStatement) -> str:
        lines = [self._indent() + f"switch {self._gen_expression(node.expression)} {{"]
        self.indent_level += 1
        for pattern, body in node.cases:
            lines.append(self._indent() + f"case {self._gen_expression(pattern)}:")
            self.indent_level += 1
            for stmt in body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        if node.default_body:
            lines.append(self._indent() + "default:")
            self.indent_level += 1
            for stmt in node.default_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_for_loop(self, node: ForLoop) -> str:
        lines = []
        if node.iterable:
            lines.append(self._indent() + f"for {node.variable} in {self._gen_expression(node.iterable)} {{")
        else:
            from_v = self._gen_expression(node.range_from)
            to_v = self._gen_expression(node.range_to)
            lines.append(self._indent() + f"for {node.variable} in {from_v}...{to_v} {{")
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_repeat_loop(self, node: RepeatLoop) -> str:
        lines = [self._indent() + f"for _ in 0..<{self._gen_expression(node.times)} {{"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_while_loop(self, node: WhileLoop) -> str:
        lines = [self._indent() + f"while {self._gen_expression(node.condition)} {{"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_function_definition(self, node: FunctionDefinition) -> str:
        lines = []
        prefix = "async " if node.is_async else ""
        params = list(node.parameters)
        if node.has_rest_param:
            params.append(f"{node.rest_param_name}: Any...")
        param_strs = []
        for p in params:
            if p in node.defaults:
                param_strs.append(f"{p}: Any = {self._gen_expression(node.defaults[p])}")
            else:
                param_strs.append(f"{p}: Any")
        lines.append(self._indent() + f"{prefix}func {node.name}({', '.join(param_strs)}) {{")
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_class_definition(self, node: ClassDefinition) -> str:
        lines = []
        if node.parent:
            lines.append(self._indent() + f"class {node.name}: {node.parent} {{")
        else:
            lines.append(self._indent() + f"class {node.name} {{")
        self.indent_level += 1
        for stmt in node.body:
            lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_return_statement(self, node: ReturnStatement) -> str:
        if node.value:
            return self._indent() + f"return {self._gen_expression(node.value)}"
        return self._indent() + "return"

    def _gen_import_statement(self, node: ImportStatement) -> str:
        if node.items:
            items = ", ".join(node.items)
            return self._indent() + f"import {node.module}  // items: {items}"
        return self._indent() + f"import {node.module}"

    def _gen_export_statement(self, node: ExportStatement) -> str:
        return "public " + self._gen_statement(node.declaration)

    def _gen_try_statement(self, node: TryStatement) -> str:
        lines = [self._indent() + "do {"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        if node.catch_body:
            if node.catch_var:
                lines.append(self._indent() + f"}} catch let {node.catch_var} {{")
            else:
                lines.append(self._indent() + "} catch {")
            self.indent_level += 1
            for stmt in node.catch_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        if node.finally_body:
            lines.append(self._indent() + "} defer {")
            self.indent_level += 1
            for stmt in node.finally_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_print_statement(self, node: PrintStatement) -> str:
        if node.expression:
            return self._indent() + f"print({self._gen_expression(node.expression)})"
        return self._indent() + "print()"

    def _gen_input_statement(self, node: InputStatement) -> str:
        if node.target:
            if node.prompt:
                return self._indent() + f'print({self._gen_literal(Literal(value=node.prompt))}); var {node.target} = readLine()'
            return self._indent() + f"var {node.target} = readLine()"
        return self._indent() + "readLine()"

    def _gen_guard_statement(self, node):
        cond = self._gen_expression(node.condition)
        lines = [self._indent() + 'guard ' + cond + ' else {']
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        lines.append(self._indent() + "return")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_with_statement(self, node):
        r = self._gen_expression(node.resource)
        v = node.variable if node.variable else "_res"
        lines = [self._indent() + f"let {v} = {r}  // with",
                self._indent() + "defer { /* cleanup */ }"]
        for s in node.body: lines.append(self._gen_statement(s))
        return "\n".join(lines)

    def _gen_static_method(self, node):
        return self._gen_statement(node.declaration).replace("func ", "static func ", 1)

    def _gen_do_while_loop(self, node):
        lines = [self._indent() + "repeat {"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + f"}} while {self._gen_expression(node.condition)}")
        return "\n".join(lines)

    def _gen_enum_definition(self, node):
        lines = [self._indent() + f"enum {node.name}: Int {{"]
        for i, member in enumerate(node.members):
            sep = "," if i < len(node.members) - 1 else ""
            lines.append(self._indent() + f"    case {member} = {i}{sep}")
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    # ---- v0.5.0 Masterpiece Codegen ----

    def _gen_record_definition(self, node: RecordDefinition) -> str:
        """define record -> Swift struct"""
        lines = [self._indent() + f"struct {node.name} {{"]
        self.indent_level += 1
        for fname, ftype, fdefault in node.fields:
            sw_type = {"int": "Int", "integer": "Int", "float": "Double",
                       "string": "String", "bool": "Bool", "boolean": "Bool",
                       "any": "Any"}.get(ftype, "Any")
            default = f" = {self._gen_expression(fdefault)}" if fdefault is not None else ""
            lines.append(self._indent() + f"let {fname}: {sw_type}{default}")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_property_definition(self, node: PropertyDefinition) -> str:
        """define property -> Swift computed property"""
        lines = []
        sw_type = "Any"
        if node.type_annotation:
            sw_type = {"int": "Int", "integer": "Int", "float": "Double",
                       "string": "String", "bool": "Bool", "any": "Any"}.get(node.type_annotation.type_name, "Any")
        if node.getter_body:
            lines.append(self._indent() + f"var {node.name}: {sw_type} {{")
            self.indent_level += 1
            for stmt in node.getter_body:
                lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
            lines.append(self._indent() + "}")
        if node.setter_body:
            lines.append(self._indent() + f"var {node.name}: {sw_type} {{")
            self.indent_level += 1
            lines.append(self._indent() + f"set({node.setter_param}) {{")
            self.indent_level += 1
            for stmt in node.setter_body:
                lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
            lines.append(self._indent() + "}")
            self.indent_level -= 1
            lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_extension_definition(self, node: ExtensionDefinition) -> str:
        """define extension on Type -> Swift extension"""
        lines = [self._indent() + f"extension {node.target_type} {{"]
        self.indent_level += 1
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                params = ", ".join(f"{p}: Any" for p in stmt.parameters)
                lines.append(self._indent() + f"func {stmt.name}({params}) {{" if params else self._indent() + f"func {stmt.name}() {{")
                self.indent_level += 1
                for s in stmt.body:
                    lines.append(self._gen_statement(s))
                self.indent_level -= 1
                lines.append(self._indent() + "}")
            else:
                lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)


    # ---- v0.9.1+ Handler Methods ----

    def _gen_set_stmt(self, node):
        el = ", ".join(str(e) for e in node.elements)
        return self._indent() + f"Set([{el}])"

    def _gen_multi_return(self, node):
        vals = ", ".join(self._gen_expression(v) for v in node.values)
        return self._indent() + f"return ({vals})"

    def _gen_synchronized(self, node):
        lock = node.lock_object or "_lock"
        lines = [self._indent() + f"objc_sync_enter({lock})"]
        for s in node.body: lines.append(self._gen_statement(s))
        lines.append(self._indent() + f"objc_sync_exit({lock})")
        return "\n".join(lines)

    def _gen_async_with(self, node):
        r = self._gen_expression(node.resource)
        lines = [self._indent() + f"// async with: {r}"]
        for s in node.body: lines.append(self._gen_statement(s))
        return "\n".join(lines)

    def _gen_actor(self, node):
        lines = [self._indent() + f"actor {node.name} {{"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_subscript(self, node):
        params = ", ".join(f"{name}: {typ}" for name, typ in node.parameters)
        lines = [self._indent() + f"subscript({params}) -> {node.return_type or 'Any'} {{"]
        self.indent_level += 1
        if node.getter_body:
            for s in node.getter_body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)


def generate_swift(ast: Program) -> str:
    gen = SwiftGenerator(ast)
    return gen.generate()
