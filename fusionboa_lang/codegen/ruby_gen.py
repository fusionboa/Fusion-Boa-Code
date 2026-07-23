"""
FusionBoa → Ruby Code Generator
Ruby is naturally English-like, making it a perfect target.
"""

from ..parser.ast_nodes import *


class RubyGenerator:
    def __init__(self, ast: Program):
        self.ast = ast
        self.indent_level = 0

    def _indent(self) -> str:
        return "  " * self.indent_level

    def generate(self) -> str:
        return "\n".join(self._gen_statement(s) for s in self.ast.statements)

    def _gen_statement(self, node: ASTNode) -> str:
        if node is None: return ""
        if isinstance(node, ExpressionStatement): return self._indent() + self._gen_expression(node.expression)
        if isinstance(node, VariableDeclaration): return self._indent() + f"{node.name} = {self._gen_expression(node.value)}"
        if isinstance(node, ConstDeclaration): return self._indent() + f"{node.name.upper()} = {self._gen_expression(node.value)}"
        if isinstance(node, Assignment): return self._indent() + f"{node.target} = {self._gen_expression(node.value)}"
        if isinstance(node, AugmentedAssignment): return self._gen_augmented_assignment(node)
        if isinstance(node, PrintStatement):
            v = self._gen_expression(node.expression) if node.expression else ""
            return self._indent() + f"puts {v}"
        if isinstance(node, IfStatement): return self._gen_if(node)
        if isinstance(node, ForLoop): return self._gen_for(node)
        if isinstance(node, WhileLoop): return self._gen_while(node)
        if isinstance(node, RepeatLoop): return self._gen_repeat(node)
        if isinstance(node, FunctionDefinition): return self._gen_function(node)
        if isinstance(node, ClassDefinition): return self._gen_class(node)
        if isinstance(node, ReturnStatement):
            return self._indent() + (f"return {self._gen_expression(node.value)}" if node.value else "return")
        if isinstance(node, TryStatement): return self._gen_try(node)
        if isinstance(node, MatchStatement): return self._gen_match(node)
        if isinstance(node, ImportStatement): return self._gen_import(node)
        if isinstance(node, InputStatement):
            t = node.target
            p = f"\"{node.prompt}\"" if node.prompt else "\"\""
            return self._indent() + (f"{t} = gets.chomp" if t else "gets.chomp")
        if isinstance(node, BreakStatement): return self._indent() + "break"
        if isinstance(node, ContinueStatement): return self._indent() + "next"
        if isinstance(node, PassStatement): return self._indent() + "# pass"
        if isinstance(node, DoWhileLoop): return self._gen_do_while(node)
        if isinstance(node, EnumDefinition): return self._gen_enum(node)
        if isinstance(node, DeferStatement): return self._indent() + "# deferred"
        if isinstance(node, GuardStatement): return self._gen_guard_statement(node)
        if isinstance(node, DestructuringDeclaration): return self._gen_destructuring(node)
        if isinstance(node, IncrementExpression):
            return self._indent() + f"{node.target} += 1"
        if isinstance(node, DecrementExpression):
            return self._indent() + f"{node.target} -= 1"
        if isinstance(node, WithStatement):
            r = self._gen_expression(node.resource)
            v = node.variable if node.variable else "_res"
            lines = [self._indent() + f"{v} = {r}  # with", self._indent() + "begin"]
            self.indent_level += 1
            for s in node.body: lines.append(self._gen_statement(s))
            self.indent_level -= 1
            lines.append(self._indent() + f"ensure; /* cleanup {v} */; end")
            return "\n".join(lines)
        if isinstance(node, DecoratorStatement): return self._indent() + f"# @{node.name}"
        if isinstance(node, StaticMethodDeclaration):
            func = self._gen_statement(node.declaration)
            return func.replace("def ", "def self.", 1)
        # v0.5.0 Masterpiece
        if isinstance(node, RecordDefinition): return self._gen_record_definition(node)
        if isinstance(node, PropertyDefinition): return self._gen_property_definition(node)
        if isinstance(node, ExtensionDefinition): return self._gen_extension_definition(node)
        # v0.9.1+ Universal Polyglot
        if isinstance(node, SetLiteral): return self._gen_set_stmt(node)
        if isinstance(node, TupleLiteral): return self._gen_tuple_stmt(node)
        if isinstance(node, MultiReturnStatement): return self._gen_multi_return(node)
        if isinstance(node, YieldFromStatement): return self._indent() + f"# yield from: {self._gen_expression(node.iterable)}"
        if isinstance(node, GoStatement): return self._indent() + f"# goroutine: {node.name or 'anonymous'} (use Thread.new)"
        if isinstance(node, ChannelDeclaration): return self._indent() + f"# channel: {node.name} (use Queue)"
        if isinstance(node, ChannelSelect): return self._indent() + f"# select {len(node.cases)} channels"
        if isinstance(node, ChannelClose): return self._indent() + f"# channel close"
        if isinstance(node, SynchronizedBlock): return self._gen_synchronized(node)
        if isinstance(node, AsyncWithStatement): return self._indent() + f"# async with"
        if isinstance(node, ModuleDefinition): return self._gen_module_def(node)
        if isinstance(node, MixinStatement): return self._gen_mixin(node)
        if isinstance(node, ObjectDefinition): return self._indent() + f"# object {node.name} (singleton)"
        if isinstance(node, ActorDefinition): return self._indent() + f"# actor {node.name}"
        if isinstance(node, SealedClassDefinition): return self._indent() + f"# sealed class {node.name}"
        if isinstance(node, NewExpression): return self._indent() + f"{node.type_name}.new({', '.join(self._gen_expression(a) for a in node.arguments)})"
        if isinstance(node, DeleteExpression): return self._indent() + f"# delete {node.target} (GC handles)"
        if isinstance(node, GlobalStatement): return self._indent() + f"# global {', '.join(node.names)}"
        if isinstance(node, AtomicCounter): return self._gen_atomic(node)
        raise NotImplementedError(f"Ruby codegen does not support AST node: {type(node).__name__}")

    def _gen_expression(self, node: ASTNode) -> str:
        if node is None: return "nil"
        if isinstance(node, Literal):
            if node.value is None: return "nil"
            if node.value is True: return "true"
            if node.value is False: return "false"
            if isinstance(node.value, str): return repr(node.value)
            return str(node.value)
        if isinstance(node, Identifier):
            return "self" if node.name == "this" else node.name
        if isinstance(node, BinaryOp):
            op_map = {"and": "&&", "or": "||", "^": "**", "==": "==", "!=": "!=",
                       "<": "<", ">": ">", "<=": "<=", ">=": ">=",
                       "&": "&", "|": "|", "<<": "<<", ">>": ">>", "//": "/",
                       "??": "||", "in": "include?", "not in": "!include?", "is": "is_a?"}
            op = op_map.get(node.operator, node.operator)
            return f"({self._gen_expression(node.left)} {op} {self._gen_expression(node.right)})"
        if isinstance(node, UnaryOp):
            m = {"neg": "-", "not": "!", "~": "~"}
            return f"({m.get(node.operator, node.operator)}{self._gen_expression(node.operand)})"
        if isinstance(node, Call):
            callee = self._gen_expression(node.callee)
            args = ", ".join(self._gen_expression(a) for a in node.arguments)
            if isinstance(node.callee, Identifier):
                if node.callee.name == "print": return f"puts({args})"
                if node.callee.name == "input": return "gets.chomp"
            return f"{callee}({args})"
        if isinstance(node, Attribute):
            return f"{self._gen_expression(node.object)}.{node.attribute}"
        if isinstance(node, Index):
            return f"{self._gen_expression(node.object)}[{self._gen_expression(node.index)}]"
        if isinstance(node, ListLiteral):
            return "[" + ", ".join(self._gen_expression(e) for e in node.elements) + "]"
        if isinstance(node, DictLiteral):
            pairs = ", ".join(f"{self._gen_expression(k)} => {self._gen_expression(v)}" for k, v in node.pairs)
            return "{" + pairs + "}"
        if isinstance(node, Ternary):
            return f"({self._gen_expression(node.condition)} ? {self._gen_expression(node.true_value)} : {self._gen_expression(node.false_value)})"
        if isinstance(node, LengthExpression):
            return f"{self._gen_expression(node.expression)}.length"
        if isinstance(node, StringInterpolation):
            parts = []
            for p in node.parts:
                if isinstance(p, Literal) and isinstance(p.value, str):
                    parts.append(p.value)
                else:
                    parts.append("#{" + self._gen_expression(p) + "}")
            return '"' + "".join(parts) + '"'
        if isinstance(node, ListComprehension):
            e = self._gen_expression(node.expression)
            it = self._gen_expression(node.iterable)
            return f"{it}.map {{ |{node.variable}| {e} }}"
        if isinstance(node, InExpression): return f"({self._gen_expression(node.right)}.include?({self._gen_expression(node.left)}))"
        if isinstance(node, IsExpression): return f"({self._gen_expression(node.left)}.is_a?({self._gen_expression(node.right)}))"
        if isinstance(node, RangeLiteral): return f"({self._gen_expression(node.start)}..{self._gen_expression(node.end)})"
        if isinstance(node, DictComprehension): return f"# dict comp"
        if isinstance(node, MultiLineString): return '"' + node.value + '"'
        if isinstance(node, SliceExpression): return "# slice"
        if isinstance(node, GeneratorExpression): return self._gen_generator(node)
        if isinstance(node, IncrementExpression): return f"{node.target} += 1"
        if isinstance(node, DecrementExpression): return f"{node.target} -= 1"
        # v0.9.1+ Expression nodes
        if isinstance(node, SetLiteral):
            return "Set[" + ", ".join(self._gen_expression(e) for e in node.elements) + "]"
        if isinstance(node, TupleLiteral):
            return "[" + ", ".join(self._gen_expression(e) for e in node.elements) + "]"
        if isinstance(node, SymbolLiteral): return f":{node.name}"
        if isinstance(node, BlockExpression): return self._gen_block_expr(node)
        if isinstance(node, JsxElement): return f"# JSX:{node.tag}"
        if isinstance(node, HookCall): return f"# {node.hook_name}()"
        if isinstance(node, NewExpression):
            args = ", ".join(self._gen_expression(a) for a in node.arguments)
            return f"{node.type_name}.new({args})"
        if isinstance(node, DeleteExpression): return f"# delete {node.target}"
        if isinstance(node, BroadcastExpression): return f"# broadcast"
        if isinstance(node, VectorizeExpression): return f"# vectorize"
        if isinstance(node, FormulaExpression): return f"# formula"
        if isinstance(node, KeyOfExpression): return f"# keyof {node.target_type}"
        if isinstance(node, TemplateLiteral): return f"# template literal"
        if isinstance(node, YieldToBlock): return f"yield({', '.join(self._gen_expression(a) for a in node.arguments)})"
        return f"/* {type(node).__name__} */"

    def _gen_if(self, node):
        lines = [self._indent() + f"if {self._gen_expression(node.condition)}"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        for cond, body in node.elif_branches:
            lines.append(self._indent() + f"elsif {self._gen_expression(cond)}")
            self.indent_level += 1
            for s in body: lines.append(self._gen_statement(s))
            self.indent_level -= 1
        if node.else_body:
            lines.append(self._indent() + "else")
            self.indent_level += 1
            for s in node.else_body: lines.append(self._gen_statement(s))
            self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_for(self, node):
        lines = []
        if node.iterable:
            lines.append(self._indent() + f"{self._gen_expression(node.iterable)}.each do |{node.variable}|")
        else:
            fv = self._gen_expression(node.range_from)
            tv = self._gen_expression(node.range_to)
            lines.append(self._indent() + f"({fv}..{tv}).each do |{node.variable}|")
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_while(self, node):
        lines = [self._indent() + f"while {self._gen_expression(node.condition)}"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_repeat(self, node):
        lines = [self._indent() + f"{self._gen_expression(node.times)}.times do"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_function(self, node):
        params = ", ".join(node.parameters)
        lines = [self._indent() + f"def {node.name}({params})"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_class(self, node):
        parent = f" < {node.parent}" if node.parent else ""
        lines = [self._indent() + f"class {node.name}{parent}"]
        self.indent_level += 1
        for s in node.body:
            if isinstance(s, FunctionDefinition) and s.name == "init":
                saved = s.name
                s.name = "initialize"
                lines.append(self._gen_statement(s))
                s.name = saved
            else:
                lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_try(self, node):
        lines = [self._indent() + "begin"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        if node.catch_body:
            v = f" => {node.catch_var}" if node.catch_var else ""
            lines.append(self._indent() + f"rescue Exception{v}")
            self.indent_level += 1
            for s in node.catch_body: lines.append(self._gen_statement(s))
            self.indent_level -= 1
        if node.finally_body:
            lines.append(self._indent() + "ensure")
            self.indent_level += 1
            for s in node.finally_body: lines.append(self._gen_statement(s))
            self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_match(self, node):
        lines = [self._indent() + f"case {self._gen_expression(node.expression)}"]
        self.indent_level += 1
        for pattern, body in node.cases:
            lines.append(self._indent() + f"when {self._gen_expression(pattern)}")
            self.indent_level += 1
            for s in body: lines.append(self._gen_statement(s))
            self.indent_level -= 1
        if node.default_body:
            lines.append(self._indent() + "else")
            self.indent_level += 1
            for s in node.default_body: lines.append(self._gen_statement(s))
            self.indent_level -= 1
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_import(self, node):
        if node.items:
            return self._indent() + f"# require '{node.module}'  # import {{ {', '.join(node.items)} }}"
        return self._indent() + f"require '{node.module}'"


    def _gen_do_while(self, node):
        lines = [self._indent() + "loop do"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        lines.append(self._indent() + f"break unless ({self._gen_expression(node.condition)})")
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_enum(self, node):
        lines = [self._indent() + f"# enum {node.name}"]
        for i, member in enumerate(node.members):
            lines.append(self._indent() + f"{node.name}_{member} = {i}")
        return "\n".join(lines)

    def _gen_destructuring(self, node):
        targets = ", ".join(node.targets)
        value = self._gen_expression(node.value)
        return self._indent() + f"{targets} = {value}"

    def _gen_generator(self, node):
        expr = self._gen_expression(node.expression)
        it = self._gen_expression(node.iterable)
        cond = f"if {self._gen_expression(node.condition)}" if node.condition else ""
        return f"{it}.lazy.select {{ |{node.variable}| {self._gen_expression(node.condition) if node.condition else 'true'} }}.map {{ |{node.variable}| {expr} }}"

    def _gen_augmented_assignment(self, node):
        val = self._gen_expression(node.value)
        target = node.target
        if node.operator == "||":
            return self._indent() + f"{target} ||= {val}"
        if node.operator == "&&":
            return self._indent() + f"{target} &&= {val}"
        if node.operator == "??":
            return self._indent() + f"{target} = {target}.nil? ? {val} : {target}"
        return self._indent() + f"{target} = {target} {node.operator} {val}"

    # ---- v0.5.0 Masterpiece Codegen ----

    def _gen_record_definition(self, node: RecordDefinition) -> str:
        """define record -> Ruby Struct (immutable with freeze)"""
        field_names = ", ".join(f"'{fname}'" for fname, _, _ in node.fields) if node.fields else ""
        lines = [self._indent() + f"{node.name} = Struct.new({field_names}) do"]
        self.indent_level += 1
        lines.append(self._indent() + "def initialize(*args)")
        self.indent_level += 1
        lines.append(self._indent() + "super")
        lines.append(self._indent() + "freeze")
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_property_definition(self, node: PropertyDefinition) -> str:
        """define property -> Ruby attr_reader/attr_writer with custom logic"""
        lines = []
        if node.getter_body:
            lines.append(self._indent() + f"def {node.name}")
            self.indent_level += 1
            for stmt in node.getter_body:
                lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
            lines.append(self._indent() + "end")
        if node.setter_body:
            lines.append(self._indent() + f"def {node.name}=(value)")
            self.indent_level += 1
            for stmt in node.setter_body:
                lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
            lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_extension_definition(self, node: ExtensionDefinition) -> str:
        """define extension on Type -> Ruby open class/monkey-patching"""
        lines = [self._indent() + f"# Extension methods for {node.target_type}"]
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                params = ", ".join(stmt.parameters)
                lines.append(self._indent() + f"def {stmt.name}({params})")
                self.indent_level += 1
                for s in stmt.body:
                    lines.append(self._gen_statement(s))
                self.indent_level -= 1
                lines.append(self._indent() + "end")
            else:
                lines.append(self._gen_statement(stmt))
        return "\n".join(lines)


    def _gen_block_expr(self, node):
        params = "|" + ", ".join(node.parameters) + "|" if node.parameters else ""
        lines = [f"do {params}"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_set_stmt(self, node):
        el = ", ".join(str(e) for e in node.elements)
        return self._indent() + f"Set[{el}]"

    def _gen_tuple_stmt(self, node):
        el = ", ".join(str(e) for e in node.elements)
        return self._indent() + f"[{el}]"

    def _gen_multi_return(self, node):
        vals = ", ".join(self._gen_expression(v) for v in node.values)
        return self._indent() + f"return [{vals}]"

    def _gen_synchronized(self, node):
        lock = node.lock_object or "Mutex.new"
        lines = [self._indent() + f"{lock}.synchronize do"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_module_def(self, node):
        lines = [self._indent() + f"module {node.name}"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "end")
        return "\n".join(lines)

    def _gen_mixin(self, node):
        return self._indent() + f"{node.mixin_type} {node.mixin_name}"

    def _gen_atomic(self, node):
        val = self._gen_expression(node.initial_value) if node.initial_value else "0"
        return self._indent() + f"{node.name} = Concurrent::AtomicFixnum.new({val})"


def generate_ruby(ast: Program) -> str:
    return RubyGenerator(ast).generate()
