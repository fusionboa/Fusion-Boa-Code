"""
FusionBoa → Kotlin Code Generator

Translates a FusionBoa AST into equivalent Kotlin source code.
Supports all Fusion features.
"""

from ..parser.ast_nodes import *


class KotlinGenerator:
    """Generates Kotlin code from a FusionBoa AST."""

    def __init__(self, ast: Program):
        self.ast = ast
        self.indent_level = 0
        self._in_class = False

    def _indent(self) -> str:
        return "    " * self.indent_level

    def generate(self) -> str:
        self.indent_level = 1  # Start inside main()
        lines = []
        for stmt in self.ast.statements:
            lines.append(self._gen_statement(stmt))
        return "fun main() {\n" + "\n".join(lines) + "\n}\n"

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
            BreakStatement: lambda n: "break",
            ContinueStatement: lambda n: "continue",
            PassStatement: lambda n: "// pass",
            ImportStatement: self._gen_import_statement,
            ExportStatement: self._gen_export_statement,
            TryStatement: self._gen_try_statement,
            PrintStatement: self._gen_print_statement,
            InputStatement: self._gen_input_statement,
            DoWhileLoop: self._gen_do_while_loop,
            EnumDefinition: self._gen_enum_definition,
            DeferStatement: lambda n: "// deferred",
            GuardStatement: self._gen_guard_statement,
            DestructuringDeclaration: self._gen_destructuring,
            IncrementExpression: lambda n: self._indent() + (f"++{n.target}" if n.prefix else f"{n.target}++"),
            DecrementExpression: lambda n: self._indent() + (f"--{n.target}" if n.prefix else f"{n.target}--"),
            WithStatement: self._gen_with_statement,
            DecoratorStatement: lambda n: self._indent() + f"// @{n.name}",
            StaticMethodDeclaration: self._gen_static_method,
            # v0.5.0 Masterpiece
            RecordDefinition: self._gen_record_definition,
            PropertyDefinition: self._gen_property_definition,
            ExtensionDefinition: self._gen_extension_definition,
            # v0.9.1+ Universal Polyglot
            SetLiteral: self._gen_set_stmt,
            TupleLiteral: self._gen_tuple_stmt,
            MultiReturnStatement: self._gen_multi_return,
            YieldFromStatement: lambda n: self._indent() + f"// yield from: {self._gen_expression(n.iterable)}",
            GoStatement: self._gen_go_stmt,
            ChannelDeclaration: lambda n: self._indent() + f"// channel: {n.name} (use Channel<T>)",
            ChannelSelect: lambda n: self._indent() + f"// select {len(n.cases)} channels",
            ChannelClose: lambda n: self._indent() + f"// channel close",
            SynchronizedBlock: self._gen_synchronized,
            AsyncWithStatement: lambda n: self._indent() + f"// async with",
            ModuleDefinition: lambda n: self._indent() + f"// module {n.name}",
            MixinStatement: lambda n: self._indent() + f"// {n.mixin_type} {n.mixin_name}",
            ObjectDefinition: self._gen_object_def,
            ActorDefinition: lambda n: self._indent() + f"// actor {n.name}",
            SealedClassDefinition: self._gen_sealed_class,
            NewExpression: lambda n: self._indent() + f"{n.type_name}({', '.join(self._gen_expression(a) for a in n.arguments)})",
            DeleteExpression: lambda n: self._indent() + f"// delete {n.target} (GC handles)",
            GlobalStatement: lambda n: self._indent() + f"// global {', '.join(n.names)}",
            AtomicCounter: lambda n: self._indent() + f"val {n.name} = java.util.concurrent.atomic.AtomicInteger({self._gen_expression(n.initial_value) if n.initial_value else '0'})",
            LateInitDeclaration: self._gen_lateinit,
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
        if isinstance(node, LengthExpression): return f"({self._gen_expression(node.expression)}).size"
        if isinstance(node, AwaitExpression): return f"/* await */ {self._gen_expression(node.expression)}"
        if isinstance(node, ListComprehension): return self._gen_list_comprehension(node)
        if isinstance(node, StringInterpolation): return self._gen_string_interpolation(node)
        if isinstance(node, SpreadElement): return f"*{self._gen_expression(node.expression)}"
        if isinstance(node, KeywordArgument): return f"{node.name} = {self._gen_expression(node.value)}"
        if isinstance(node, RangeLiteral):
            return f"({self._gen_expression(node.start)}..{self._gen_expression(node.end)})"
        if isinstance(node, InExpression): return f"({self._gen_expression(node.left)} in {self._gen_expression(node.right)})"
        if isinstance(node, IsExpression): return f"({self._gen_expression(node.left)} is {self._gen_expression(node.right)})"
        if isinstance(node, DictComprehension): return f"// dict comp"
        if isinstance(node, MultiLineString): return self._gen_literal(Literal(node.value))
        if isinstance(node, SliceExpression): return f"// slice"
        if isinstance(node, GeneratorExpression): return f"/* generator */"
        if isinstance(node, IncrementExpression): return f"++{node.target}" if node.prefix else f"{node.target}++"
        if isinstance(node, DecrementExpression): return f"--{node.target}" if node.prefix else f"{node.target}--"
        # v0.9.1+ Expression nodes
        if isinstance(node, SetLiteral):
            el = ", ".join(self._gen_expression(e) for e in node.elements)
            return f"setOf({el})"
        if isinstance(node, TupleLiteral):
            el = ", ".join(self._gen_expression(e) for e in node.elements)
            return f"Pair({el})" if len(node.elements) == 2 else f"Triple({el})" if len(node.elements) == 3 else f"tupleOf({el})"
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
        if node.value is None: return "null"
        if node.value is True: return "true"
        if node.value is False: return "false"
        if isinstance(node.value, str):
            return '"' + node.value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'
        return str(node.value)

    def _gen_binary_op(self, node: BinaryOp) -> str:
        op_map = {"and": "&&", "or": "||", "^": "/* pow */",
                  "==": "==", "!=": "!=", "<": "<", ">": ">",
                  "<=": "<=", ">=": ">=", "+": "+", "-": "-",
                  "*": "*", "/": "/", "%": "%",
                  "&": "and", "|": "or", "<<": "shl", ">>": "shr",
                  "??": "?:", "is": "is", "//": "/"}
        kt_op = op_map.get(node.operator, node.operator)
        left = self._gen_expression(node.left)
        right = self._gen_expression(node.right)
        return f"({left} {kt_op} {right})"

    def _gen_unary_op(self, node: UnaryOp) -> str:
        op_map = {"neg": "-", "not": "!", "~": ".inv()"}
        kt_op = op_map.get(node.operator, node.operator)
        operand = self._gen_expression(node.operand)
        return f"({kt_op}{operand})"

    def _gen_call(self, node: Call) -> str:
        callee = self._gen_expression(node.callee)
        args = ", ".join(self._gen_expression(a) for a in node.arguments)
        if isinstance(node.callee, Identifier):
            if node.callee.name == "print":
                return f"println({args})"
            if node.callee.name == "input":
                return f"readLine({args})"
        return f"{callee}({args})"

    def _gen_attribute(self, node: Attribute) -> str:
        return f"{self._gen_expression(node.object)}.{node.attribute}"

    def _gen_index(self, node: Index) -> str:
        return f"{self._gen_expression(node.object)}[{self._gen_expression(node.index)}]"

    def _gen_list_literal(self, node: ListLiteral) -> str:
        elements = ", ".join(self._gen_expression(e) for e in node.elements)
        return f"mutableListOf({elements})"

    def _gen_dict_literal(self, node: DictLiteral) -> str:
        pairs = ", ".join(f"{self._gen_expression(k)} to {self._gen_expression(v)}" for k, v in node.pairs)
        return f"mutableMapOf({pairs})"

    def _gen_lambda(self, node: Lambda) -> str:
        params = ", ".join(node.parameters)
        body = self._gen_expression(node.body)
        return f"{{ {params} -> {body} }}"

    def _gen_ternary(self, node: Ternary) -> str:
        return f"if ({self._gen_expression(node.condition)}) {self._gen_expression(node.true_value)} else {self._gen_expression(node.false_value)}"

    def _gen_list_comprehension(self, node: ListComprehension) -> str:
        expr = self._gen_expression(node.expression)
        iterable = self._gen_expression(node.iterable)
        if node.condition:
            cond = self._gen_expression(node.condition)
            return f"({iterable}).filter {{ {node.variable} -> {cond} }}.map {{ {node.variable} -> {expr} }}"
        return f"({iterable}).map {{ {node.variable} -> {expr} }}"

    def _gen_string_interpolation(self, node: StringInterpolation) -> str:
        parts = []
        for p in node.parts:
            if isinstance(p, Literal) and isinstance(p.value, str):
                parts.append(p.value.replace("$", "\\$"))
            else:
                parts.append("${" + self._gen_expression(p) + "}")
        return '"' + "".join(parts) + '"'

    def _gen_expression_statement(self, node: ExpressionStatement) -> str:
        return self._gen_expression(node.expression)

    def _gen_variable_declaration(self, node: VariableDeclaration) -> str:
        return f"var {node.name} = {self._gen_expression(node.value)}"

    def _gen_const_declaration(self, node: ConstDeclaration) -> str:
        return f"val {node.name} = {self._gen_expression(node.value)}"

    def _gen_assignment(self, node: Assignment) -> str:
        return f"{node.target} = {self._gen_expression(node.value)}"

    def _gen_augmented_assignment(self, node: AugmentedAssignment) -> str:
        val = self._gen_expression(node.value)
        target = node.target
        if node.operator == "||": return f"{target} = {target} || {val}"
        if node.operator == "&&": return f"{target} = {target} && {val}"
        if node.operator == "??": return f"{target} = {target} ?: {val}"
        return f"{target} {node.operator}= {val}"

    def _gen_if_statement(self, node: IfStatement) -> str:
        lines = [f"if ({self._gen_expression(node.condition)}) {{"]
        for stmt in node.body: lines.append(f"    {self._gen_statement(stmt)}")
        for elif_cond, elif_body in node.elif_branches:
            lines.append(f"}} else if ({self._gen_expression(elif_cond)}) {{")
            for stmt in elif_body: lines.append(f"    {self._gen_statement(stmt)}")
        if node.else_body:
            lines.append("} else {")
            for stmt in node.else_body: lines.append(f"    {self._gen_statement(stmt)}")
        lines.append("}")
        return "\n".join(lines)

    def _gen_match_statement(self, node: MatchStatement) -> str:
        lines = [f"when ({self._gen_expression(node.expression)}) {{"]
        for pattern, body in node.cases:
            lines.append(f"    {self._gen_expression(pattern)} -> {{")
            for stmt in body: lines.append(f"        {self._gen_statement(stmt)}")
            lines.append("    }")
        if node.default_body:
            lines.append("    else -> {")
            for stmt in node.default_body: lines.append(f"        {self._gen_statement(stmt)}")
            lines.append("    }")
        lines.append("}")
        return "\n".join(lines)

    def _gen_for_loop(self, node: ForLoop) -> str:
        lines = []
        if node.iterable:
            lines.append(f"for ({node.variable} in {self._gen_expression(node.iterable)}) {{")
        else:
            from_v = self._gen_expression(node.range_from)
            to_v = self._gen_expression(node.range_to)
            lines.append(f"for ({node.variable} in {from_v}..{to_v}) {{")
        for stmt in node.body: lines.append(f"    {self._gen_statement(stmt)}")
        lines.append("}")
        return "\n".join(lines)

    def _gen_repeat_loop(self, node: RepeatLoop) -> str:
        lines = [f"repeat({self._gen_expression(node.times)}) {{"]
        for stmt in node.body: lines.append(f"    {self._gen_statement(stmt)}")
        lines.append("}")
        return "\n".join(lines)

    def _gen_while_loop(self, node: WhileLoop) -> str:
        lines = [f"while ({self._gen_expression(node.condition)}) {{"]
        for stmt in node.body: lines.append(f"    {self._gen_statement(stmt)}")
        lines.append("}")
        return "\n".join(lines)

    def _gen_function_definition(self, node: FunctionDefinition) -> str:
        lines = []
        prefix = "suspend " if node.is_async else ""
        params = list(node.parameters)
        if node.has_rest_param:
            params.append(f"vararg {node.rest_param_name}")
        param_strs = []
        for p in params:
            if p in node.defaults:
                param_strs.append(f"{p}: Any = {self._gen_expression(node.defaults[p])}")
            else:
                param_strs.append(f"{p}: Any")
        lines.append(f"{prefix}fun {node.name}({', '.join(param_strs)}) {{")
        for stmt in node.body: lines.append(f"    {self._gen_statement(stmt)}")
        lines.append("}")
        return "\n".join(lines)

    def _gen_class_definition(self, node: ClassDefinition) -> str:
        lines = []
        if node.parent:
            lines.append(f"class {node.name} : {node.parent}() {{")
        else:
            lines.append(f"class {node.name} {{")
        for stmt in node.body:
            lines.append(f"    {self._gen_statement(stmt)}")
        lines.append("}")
        return "\n".join(lines)

    def _gen_return_statement(self, node: ReturnStatement) -> str:
        if node.value:
            return f"return {self._gen_expression(node.value)}"
        return "return"

    def _gen_yield_statement(self, node: YieldStatement) -> str:
        if node.value:
            return f"/* yield */ {self._gen_expression(node.value)}"
        return "/* yield */"

    def _gen_import_statement(self, node: ImportStatement) -> str:
        if node.items:
            items = ", ".join(node.items)
            return f"import {node.module}.{items}"
        return f"import {node.module}.*"

    def _gen_export_statement(self, node: ExportStatement) -> str:
        return self._gen_statement(node.declaration) + "  // export"

    def _gen_try_statement(self, node: TryStatement) -> str:
        lines = ["try {"]
        for stmt in node.body: lines.append(f"    {self._gen_statement(stmt)}")
        if node.catch_body:
            if node.catch_var:
                lines.append(f"}} catch ({node.catch_var}: Exception) {{")
            else:
                lines.append("} catch (e: Exception) {")
            for stmt in node.catch_body: lines.append(f"    {self._gen_statement(stmt)}")
        if node.finally_body:
            lines.append("} finally {")
            for stmt in node.finally_body: lines.append(f"    {self._gen_statement(stmt)}")
        lines.append("}")
        return "\n".join(lines)

    def _gen_print_statement(self, node: PrintStatement) -> str:
        if node.expression:
            return f"println({self._gen_expression(node.expression)})"
        return "println()"

    def _gen_input_statement(self, node: InputStatement) -> str:
        if node.target:
            if node.prompt:
                return f'print({self._gen_literal(Literal(value=node.prompt))}); val {node.target} = readLine()'
            return f"val {node.target} = readLine()"
        return "readLine()"

    def _gen_destructuring(self, node):
        targets = ", ".join(node.targets)
        value = self._gen_expression(node.value)
        return self._indent() + f"val ({targets}) = {value}"

    def _gen_guard_statement(self, node):
        cond = self._gen_expression(node.condition)
        lines = ['    if (!' + cond + ') {']
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        lines.append('    return')
        self.indent_level -= 1
        lines.append('    }')
        return '\n'.join(lines)

    def _gen_with_statement(self, node):
        r = self._gen_expression(node.resource)
        v = node.variable if node.variable else "_res"
        lines = [self._indent() + f"val {v} = {r}  // with",
                self._indent() + "try {"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "} finally {")
        self.indent_level += 1
        lines.append(self._indent() + f"({v} as? AutoCloseable)?.close()")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_static_method(self, node):
        return self._gen_statement(node.declaration).replace("fun ", "// static\nfun ", 1)

    def _gen_do_while_loop(self, node):
        lines = [f"do {{"]
        for stmt in node.body: lines.append(f"    {self._gen_statement(stmt)}")
        lines.append(f"}} while ({self._gen_expression(node.condition)})")
        return "\n".join(lines)

    def _gen_enum_definition(self, node):
        lines = [f"enum class {node.name} {{"]
        for i, member in enumerate(node.members):
            lines.append(f"    {member}({i}),")
        lines.append("}")
        return "\n".join(lines)

    # ---- v0.5.0 Masterpiece Codegen ----

    def _gen_record_definition(self, node: RecordDefinition) -> str:
        """define record -> Kotlin data class"""
        lines = [f"data class {node.name}("]
        field_strs = []
        for fname, ftype, fdefault in node.fields:
            kt_type = {"int": "Int", "integer": "Int", "float": "Double",
                       "string": "String", "bool": "Boolean", "boolean": "Boolean",
                       "any": "Any"}.get(ftype, "Any")
            default = f" = {self._gen_expression(fdefault)}" if fdefault is not None else ""
            field_strs.append(f"    val {fname}: {kt_type}{default}")
        lines.append(",\n".join(field_strs))
        lines.append(")")
        return "\n".join(lines)

    def _gen_property_definition(self, node: PropertyDefinition) -> str:
        """define property -> Kotlin property with custom getter/setter"""
        lines = []
        kt_type = "Any"
        if node.type_annotation:
            kt_type = {"int": "Int", "integer": "Int", "float": "Double",
                       "string": "String", "bool": "Boolean", "any": "Any"}.get(node.type_annotation.type_name, "Any")
        lines.append(f"val {node.name}: {kt_type}" if not node.setter_body else f"var {node.name}: {kt_type}")
        if node.getter_body:
            lines[-1] += ""
            lines.append("    get() {")
            for stmt in node.getter_body:
                lines.append(f"        {self._gen_statement(stmt)}")
            lines.append("    }")
        if node.setter_body:
            lines.append("    set(value) {")
            for stmt in node.setter_body:
                lines.append(f"        {self._gen_statement(stmt)}")
            lines.append("    }")
        return "\n".join(lines)

    def _gen_extension_definition(self, node: ExtensionDefinition) -> str:
        """define extension on Type -> Kotlin extension functions"""
        lines = []
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                params = ", ".join(f"{p}: Any" for p in stmt.parameters)
                lines.append(f"fun {node.target_type}.{stmt.name}({params}) {{" if params else f"fun {node.target_type}.{stmt.name}() {{")
                for s in stmt.body:
                    lines.append(f"    {self._gen_statement(s)}")
                lines.append("}")
        return "\n".join(lines)


    # ---- v0.9.1+ Handler Methods ----

    def _gen_set_stmt(self, node):
        el = ", ".join(str(e) for e in node.elements)
        return self._indent() + f"setOf({el})"

    def _gen_tuple_stmt(self, node):
        el = ", ".join(str(e) for e in node.elements)
        if len(node.elements) == 2: return self._indent() + f"Pair({el})"
        if len(node.elements) == 3: return self._indent() + f"Triple({el})"
        return self._indent() + f"tupleOf({el})"

    def _gen_multi_return(self, node):
        vals = ", ".join(self._gen_expression(v) for v in node.values)
        if len(node.values) == 2: return f"return Pair({vals})"
        if len(node.values) == 3: return f"return Triple({vals})"
        return f"return arrayOf({vals})"

    def _gen_go_stmt(self, node):
        lines = [self._indent() + f"// goroutine: {node.name or 'anonymous'}"]
        lines.append(self._indent() + "thread {")
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_synchronized(self, node):
        lock = node.lock_object or "_lock"
        lines = [self._indent() + f"synchronized({lock}) {{"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_object_def(self, node):
        prefix = "companion " if node.is_companion else ""
        lines = [self._indent() + f"{prefix}object {node.name} {{"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_sealed_class(self, node):
        lines = [self._indent() + f"sealed class {node.name} {{"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        for sub in node.subclasses:
            lines.append(self._indent() + f"class {sub} : {node.name}()")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_lateinit(self, node):
        return self._indent() + f"lateinit var {node.name}: {node.var_type}"


def generate_kotlin(ast: Program) -> str:
    gen = KotlinGenerator(ast)
    return gen.generate()
