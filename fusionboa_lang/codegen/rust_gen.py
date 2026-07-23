"""
FusionBoa → Rust Code Generator
"""

from ..parser.ast_nodes import *


class RustGenerator:
    def __init__(self, ast: Program):
        self.ast = ast
        self.indent_level = 0

    def _indent(self) -> str:
        return "    " * self.indent_level

    def generate(self) -> str:
        lines = ['fn main() {']
        self.indent_level = 1
        for s in self.ast.statements:
            if isinstance(s, (FunctionDefinition, ClassDefinition)):
                continue
            lines.append(self._gen_statement(s))
        self.indent_level = 0
        lines.append("}")
        lines.append("")
        for s in self.ast.statements:
            if isinstance(s, (FunctionDefinition, ClassDefinition)):
                lines.append(self._gen_statement(s))
        return "\n".join(lines)

    def _gen_statement(self, node: ASTNode) -> str:
        if node is None: return ""
        if isinstance(node, ExpressionStatement): return self._indent() + self._gen_expression(node.expression) + ";"
        if isinstance(node, VariableDeclaration):
            return self._indent() + f"let {node.name} = {self._gen_expression(node.value)};"
        if isinstance(node, ConstDeclaration):
            return self._indent() + f"const {node.name}: &str = {self._gen_expression(node.value)};"
        if isinstance(node, Assignment):
            return self._indent() + f"{node.target} = {self._gen_expression(node.value)};"
        if isinstance(node, AugmentedAssignment):
            return self._gen_augmented_assignment(node)
        if isinstance(node, PrintStatement):
            v = self._gen_expression(node.expression) if node.expression else '""'
            return self._indent() + f'println!("{{}}", {v});'
        if isinstance(node, IfStatement): return self._gen_if(node)
        if isinstance(node, ForLoop): return self._gen_for(node)
        if isinstance(node, WhileLoop): return self._gen_while(node)
        if isinstance(node, RepeatLoop): return self._gen_repeat(node)
        if isinstance(node, FunctionDefinition): return self._gen_function(node)
        if isinstance(node, ClassDefinition): return self._gen_struct(node)
        if isinstance(node, ReturnStatement):
            return self._indent() + (f"return {self._gen_expression(node.value)};" if node.value else "return;")
        if isinstance(node, BreakStatement): return self._indent() + "break;"
        if isinstance(node, ContinueStatement): return self._indent() + "continue;"
        if isinstance(node, DoWhileLoop): return self._gen_do_while(node)
        if isinstance(node, EnumDefinition): return self._gen_enum(node)
        if isinstance(node, DeferStatement): return self._indent() + "// deferred"
        if isinstance(node, GuardStatement): return self._gen_guard_statement(node)
        if isinstance(node, DestructuringDeclaration): return self._gen_destructuring(node)
        if isinstance(node, IncrementExpression):
            return self._indent() + f"{node.target} += 1;"
        if isinstance(node, DecrementExpression):
            return self._indent() + f"{node.target} -= 1;"
        if isinstance(node, WithStatement):
            r = self._gen_expression(node.resource)
            lines = [self._indent() + f"// with: {r}", self._indent() + "{"]
            self.indent_level += 1
            for s in node.body: lines.append(self._gen_statement(s))
            self.indent_level -= 1
            lines.append(self._indent() + "}")
            return "\n".join(lines)
        if isinstance(node, DecoratorStatement): return self._indent() + f"// @{node.name}"
        if isinstance(node, StaticMethodDeclaration):
            return self._gen_statement(node.declaration).replace("fn ", "// static\nfn ", 1)
        # v0.5.0 Masterpiece
        if isinstance(node, RecordDefinition): return self._gen_record_definition(node)
        if isinstance(node, PropertyDefinition): return self._gen_property_definition(node)
        if isinstance(node, ExtensionDefinition): return self._gen_extension_definition(node)
        # v0.9.1+ Universal Polyglot
        if isinstance(node, SetLiteral): return self._gen_set_stmt(node)
        if isinstance(node, TupleLiteral): return self._gen_tuple_stmt(node)
        if isinstance(node, MultiReturnStatement): return self._gen_multi_return(node)
        if isinstance(node, YieldFromStatement): return self._indent() + f"// yield from: {self._gen_expression(node.iterable)}"
        if isinstance(node, GoStatement): return self._indent() + f"// goroutine: {node.name or 'anonymous'} (use tokio::spawn)"
        if isinstance(node, ChannelDeclaration): return self._indent() + f"// channel: {node.name} (use tokio::sync::mpsc)"
        if isinstance(node, ChannelSelect): return self._indent() + f"// select {len(node.cases)} channels (use tokio::select!)"
        if isinstance(node, ChannelClose): return self._indent() + f"// channel close"
        if isinstance(node, SynchronizedBlock): return self._gen_synchronized(node)
        if isinstance(node, AsyncWithStatement): return self._indent() + f"// async with"
        if isinstance(node, ModuleDefinition): return self._gen_module_def(node)
        if isinstance(node, MixinStatement): return self._indent() + f"// {node.mixin_type} {node.mixin_name}"
        if isinstance(node, ObjectDefinition): return self._indent() + f"// object {node.name} (singleton)"
        if isinstance(node, ActorDefinition): return self._indent() + f"// actor {node.name}"
        if isinstance(node, SealedClassDefinition): return self._gen_sealed_class(node)
        if isinstance(node, NewExpression): return self._gen_new_stmt(node)
        if isinstance(node, DeleteExpression): return self._gen_delete_stmt(node)
        if isinstance(node, GlobalStatement): return self._indent() + f"// global {', '.join(node.names)}"
        if isinstance(node, AtomicCounter): return self._gen_atomic(node)
        return self._indent() + f"// {type(node).__name__};"

    def _gen_expression(self, node: ASTNode) -> str:
        if node is None: return "None"
        if isinstance(node, Literal):
            if node.value is None: return "None"
            if node.value is True: return "true"
            if node.value is False: return "false"
            if isinstance(node.value, str): return f'String::from({repr(node.value)})'
            return str(node.value)
        if isinstance(node, Identifier): return node.name
        if isinstance(node, BinaryOp):
            op_map = {"and": "&&", "or": "||", "^": ".pow", "==": "==", "!=": "!=",
                       "<": "<", ">": ">", "<=": "<=", ">=": ">=",
                       "&": "&", "|": "|", "<<": "<<", ">>": ">>", "//": "/"}
            op = op_map.get(node.operator, node.operator)
            l = self._gen_expression(node.left)
            r = self._gen_expression(node.right)
            # Null-coalescing: a ?? b -> a.unwrap_or(b) (requires Option)
            if node.operator == "??":
                return f"{l}.unwrap_or({r})"
            if op == ".pow": return f"({l}).pow({r})"
            return f"({l} {op} {r})"
        if isinstance(node, UnaryOp):
            m = {"neg": "-", "not": "!", "~": "!"}
            return f"({m.get(node.operator, '')}{self._gen_expression(node.operand)})"
        if isinstance(node, Call):
            callee = self._gen_expression(node.callee)
            args = ", ".join(self._gen_expression(a) for a in node.arguments)
            if isinstance(node.callee, Identifier) and node.callee.name == "print":
                return f'println!("{{}}", {args})'
            return f"{callee}({args})"
        if isinstance(node, Attribute): return f"{self._gen_expression(node.object)}.{node.attribute}"
        if isinstance(node, Index): return f"{self._gen_expression(node.object)}[{self._gen_expression(node.index)}]"
        if isinstance(node, ListLiteral):
            el = ", ".join(self._gen_expression(e) for e in node.elements)
            return f"vec![{el}]"
        if isinstance(node, DictLiteral):
            pairs = ", ".join(f"({self._gen_expression(k)}, {self._gen_expression(v)})" for k, v in node.pairs)
            return f"vec![{pairs}].into_iter().collect()"
        if isinstance(node, Ternary):
            c = self._gen_expression(node.condition)
            t = self._gen_expression(node.true_value)
            f = self._gen_expression(node.false_value)
            return f"(if {c} {{ {t} }} else {{ {f} }})"
        if isinstance(node, LengthExpression):
            return f"{self._gen_expression(node.expression)}.len()"
        if isinstance(node, InExpression): return f"({self._gen_expression(node.right)}).contains(&{self._gen_expression(node.left)})"
        if isinstance(node, IsExpression): return f"({self._gen_expression(node.left)}.is::<{self._gen_expression(node.right)}>())"
        if isinstance(node, RangeLiteral): return f"({self._gen_expression(node.start)}..={self._gen_expression(node.end)})"
        if isinstance(node, DictComprehension): return f"// dict comp"
        if isinstance(node, MultiLineString): return f'String::from({repr(node.value)})'
        if isinstance(node, SliceExpression): return f"// slice"
        if isinstance(node, GeneratorExpression): return self._gen_generator(node)
        if isinstance(node, IncrementExpression): return f"{node.target} += 1"
        if isinstance(node, DecrementExpression): return f"{node.target} -= 1"
        # v0.9.1+ Expression nodes
        if isinstance(node, SetLiteral):
            el = ", ".join(self._gen_expression(e) for e in node.elements)
            return f"vec![{el}].into_iter().collect::<std::collections::HashSet<_>>()"
        if isinstance(node, TupleLiteral):
            el = ", ".join(self._gen_expression(e) for e in node.elements)
            return f"({el})"
        if isinstance(node, SymbolLiteral): return f"/* :{node.name} */"
        if isinstance(node, BlockExpression): return f"/* block */"
        if isinstance(node, JsxElement): return f"/* JSX:{node.tag} */"
        if isinstance(node, HookCall): return f"/* {node.hook_name}() */"
        if isinstance(node, NewExpression):
            args = ", ".join(self._gen_expression(a) for a in node.arguments)
            return f"Box::new({node.type_name}{{{args}}})" if args else f"Box::new({node.type_name}{{}})"
        if isinstance(node, DeleteExpression): return f"// drop({node.target})"
        if isinstance(node, BroadcastExpression): return f"/* broadcast */"
        if isinstance(node, VectorizeExpression): return f"/* vectorize */"
        if isinstance(node, FormulaExpression): return f"/* formula */"
        if isinstance(node, KeyOfExpression): return f"/* keyof {node.target_type} */"
        if isinstance(node, TemplateLiteral): return f"/* template literal */"
        if isinstance(node, YieldToBlock): return f"/* yield to block */"
        return "None"

    def _gen_if(self, node):
        lines = [self._indent() + f"if {self._gen_expression(node.condition)} {{"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        for cond, body in node.elif_branches:
            lines.append(self._indent() + f"}} else if {self._gen_expression(cond)} {{")
            self.indent_level += 1
            for s in body: lines.append(self._gen_statement(s))
            self.indent_level -= 1
        if node.else_body:
            lines.append(self._indent() + "} else {")
            self.indent_level += 1
            for s in node.else_body: lines.append(self._gen_statement(s))
            self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_for(self, node):
        lines = []
        if node.iterable:
            lines.append(self._indent() + f"for {node.variable} in &{self._gen_expression(node.iterable)} {{")
        else:
            fv = self._gen_expression(node.range_from)
            tv = self._gen_expression(node.range_to)
            lines.append(self._indent() + f"for {node.variable} in {fv}..={tv} {{")
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_while(self, node):
        lines = [self._indent() + f"while {self._gen_expression(node.condition)} {{"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_repeat(self, node):
        lines = [self._indent() + f"for _ in 0..{self._gen_expression(node.times)} {{"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_function(self, node):
        params = ", ".join(f"{p}: i32" for p in node.parameters) if node.parameters else ""
        lines = [self._indent() + f"fn {node.name}({params}) -> i32 {{"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_struct(self, node):
        lines = [self._indent() + f"struct {node.name} {{"]
        self.indent_level += 1
        for s in node.body:
            if isinstance(s, Assignment):
                lines.append(self._indent() + f"{s.target}: i32,  // field")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        lines.append("")
        lines.append(self._indent() + f"impl {node.name} {{")
        self.indent_level += 1
        for s in node.body:
            if isinstance(s, FunctionDefinition):
                if s.name == "init":
                    s.name = "new"
                lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)


    def _gen_do_while(self, node):
        lines = [self._indent() + "loop {"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        lines.append(self._indent() + f"if !({self._gen_expression(node.condition)}) {{ break; }}")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_enum(self, node):
        lines = [self._indent() + f"enum {node.name} {{"]
        for i, member in enumerate(node.members):
            lines.append(self._indent() + f"    {member} = {i},")
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_destructuring(self, node):
        targets = ", ".join(node.targets)
        value = self._gen_expression(node.value)
        return self._indent() + f"let ({targets}) = {value};"

    def _gen_generator(self, node):
        it = self._gen_expression(node.iterable)
        return f"/* generator */"

    def _gen_augmented_assignment(self, node):
        val = self._gen_expression(node.value)
        target = node.target
        if node.operator in ("||", "&&", "??"):
            return self._indent() + f"{target} = {target} {node.operator} {val};  // logical assign"
        return self._indent() + f"{target} {node.operator}= {val};"

    # ---- v0.5.0 Masterpiece Codegen ----

    def _gen_record_definition(self, node: RecordDefinition) -> str:
        """define record -> Rust struct with derive macros"""
        lines = [self._indent() + "#[derive(Debug, Clone, PartialEq)]",
                 self._indent() + f"struct {node.name} {{"]
        self.indent_level += 1
        for fname, ftype, fdefault in node.fields:
            rust_type = {"int": "i32", "integer": "i32", "float": "f64",
                         "string": "String", "bool": "bool", "boolean": "bool",
                         "any": "Box<dyn std::any::Any>"}.get(ftype, "Box<dyn std::any::Any>")
            default = f" = {self._gen_expression(fdefault)}" if fdefault is not None else ""
            lines.append(self._indent() + f"pub {fname}: {rust_type},{default}")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_property_definition(self, node: PropertyDefinition) -> str:
        """define property -> Rust impl block with getter/setter"""
        lines = [self._indent() + "impl struct {"]
        self.indent_level += 1
        cap_name = node.name[0].upper() + node.name[1:]
        if node.getter_body:
            lines.append(self._indent() + f"pub fn {node.name}(&self) -> &dyn std::any::Any {{")
            self.indent_level += 1
            for stmt in node.getter_body:
                lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
            lines.append(self._indent() + "}")
        if node.setter_body:
            lines.append(self._indent() + f"pub fn set_{node.name}(&mut self, {node.setter_param}: Box<dyn std::any::Any>) {{")
            self.indent_level += 1
            for stmt in node.setter_body:
                lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
            lines.append(self._indent() + "}")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_extension_definition(self, node: ExtensionDefinition) -> str:
        """define extension on Type -> Rust impl block"""
        lines = [self._indent() + f"// Extension methods for {node.target_type}"]
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                params = ", ".join(f"{p}: i32" for p in stmt.parameters)
                lines.append(self._indent() + f"fn {node.target_type}_{stmt.name}(self: &{node.target_type}, {params}) {{" if params else self._indent() + f"fn {node.target_type}_{stmt.name}(self: &{node.target_type}) {{")
                self.indent_level += 1
                for s in stmt.body:
                    lines.append(self._gen_statement(s))
                self.indent_level -= 1
                lines.append(self._indent() + "}")
            else:
                lines.append(self._gen_statement(stmt))
        return "\n".join(lines)


    # ---- v0.9.1+ Handler Methods ----

    def _gen_set_stmt(self, node):
        el = ", ".join(str(e) for e in node.elements)
        return self._indent() + f"let _set = vec![{el}].into_iter().collect::<std::collections::HashSet<_>>();"

    def _gen_tuple_stmt(self, node):
        el = ", ".join(str(e) for e in node.elements)
        return self._indent() + f"let _tuple = ({el});"

    def _gen_multi_return(self, node):
        vals = ", ".join(self._gen_expression(v) for v in node.values)
        return self._indent() + f"return ({vals});"

    def _gen_synchronized(self, node):
        lock = node.lock_object or "_mutex"
        lines = [self._indent() + f"let __lock = {lock}.lock().unwrap();",
                 self._indent() + "// synchronized block"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        return "\n".join(lines)

    def _gen_module_def(self, node):
        lines = [self._indent() + f"mod {node.name} {{"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_sealed_class(self, node):
        lines = [self._indent() + f"// sealed class {node.name} (Rust: use sealed trait pattern)"]
        lines.append(self._indent() + f"trait {node.name} {{}}")
        for sub in node.subclasses:
            lines.append(self._indent() + f"// impl {node.name} for {sub} {{}}")
        return "\n".join(lines)

    def _gen_new_stmt(self, node):
        args = ", ".join(self._gen_expression(a) for a in node.arguments)
        return self._indent() + f"let __ptr = Box::new({node.type_name}{{{args}}});" if args else self._indent() + f"let __ptr = Box::new({node.type_name}{{}});"

    def _gen_delete_stmt(self, node):
        return self._indent() + f"drop({node.target});  // explicit drop"

    def _gen_atomic(self, node):
        val = self._gen_expression(node.initial_value) if node.initial_value else "0"
        return self._indent() + f"let {node.name} = std::sync::atomic::AtomicI32::new({val});"


def generate_rust(ast: Program) -> str:
    return RustGenerator(ast).generate()
