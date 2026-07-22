"""
FusionBoa → TypeScript Code Generator
Extends the JavaScript generator with TypeScript types.
"""

from ..parser.ast_nodes import *


class TypeScriptGenerator:
    def __init__(self, ast: Program):
        self.ast = ast
        self.indent_level = 0

    def _indent(self) -> str:
        return "  " * self.indent_level

    def generate(self) -> str:
        return "\n".join(self._gen_statement(s) for s in self.ast.statements)

    def _gen_statement(self, node: ASTNode) -> str:
        if node is None: return ""
        if isinstance(node, ExpressionStatement): return self._indent() + self._gen_expression(node.expression) + ";"
        if isinstance(node, VariableDeclaration): return self._indent() + f"let {node.name} = {self._gen_expression(node.value)};"
        if isinstance(node, ConstDeclaration): return self._indent() + f"const {node.name}: number = {self._gen_expression(node.value)};"
        if isinstance(node, Assignment): return self._indent() + f"{node.target} = {self._gen_expression(node.value)};"
        if isinstance(node, AugmentedAssignment): return self._indent() + f"{node.target} {node.operator}= {self._gen_expression(node.value)};"
        if isinstance(node, PrintStatement):
            v = self._gen_expression(node.expression) if node.expression else ""
            return self._indent() + f"console.log({v});"
        if isinstance(node, IfStatement): return self._gen_if(node)
        if isinstance(node, ForLoop): return self._gen_for(node)
        if isinstance(node, WhileLoop): return self._gen_while(node)
        if isinstance(node, RepeatLoop): return self._gen_repeat(node)
        if isinstance(node, FunctionDefinition): return self._gen_function(node)
        if isinstance(node, ClassDefinition): return self._gen_class(node)
        if isinstance(node, ReturnStatement):
            return self._indent() + (f"return {self._gen_expression(node.value)};" if node.value else "return;")
        if isinstance(node, TryStatement): return self._gen_try(node)
        if isinstance(node, MatchStatement): return self._gen_match(node)
        if isinstance(node, ImportStatement): return self._gen_import(node)
        if isinstance(node, BreakStatement): return self._indent() + "break;"
        if isinstance(node, ContinueStatement): return self._indent() + "continue;"
        if isinstance(node, PassStatement): return self._indent() + "// pass"
        if isinstance(node, DoWhileLoop): return self._gen_do_while(node)
        if isinstance(node, EnumDefinition): return self._gen_enum(node)
        if isinstance(node, InputStatement):
            t = node.target
            p = f"\"{node.prompt}\"" if node.prompt else "\"\""
            return self._indent() + (f"let {t}: string = prompt({p}) ?? \"\";" if t else "prompt();")
        if isinstance(node, DestructuringDeclaration):
            return self._gen_destructuring(node)
        if isinstance(node, AugmentedAssignment):
            return self._gen_augmented_assignment(node)
        if isinstance(node, IncrementExpression):
            return self._indent() + (f"++{node.target};" if node.prefix else f"{node.target}++;")
        if isinstance(node, DecrementExpression):
            return self._indent() + (f"--{node.target};" if node.prefix else f"{node.target}--;")
        if isinstance(node, WithStatement):
            r = self._gen_expression(node.resource)
            v = node.variable if node.variable else "_res"
            lines = [self._indent() + f"let {v} = {r};  // with", self._indent() + "try {"]
            self.indent_level += 1
            for s in node.body: lines.append(self._gen_statement(s))
            self.indent_level -= 1
            lines.append(self._indent() + "} finally {")
            self.indent_level += 1
            lines.append(self._indent() + f"// cleanup {v}")
            self.indent_level -= 1
            lines.append(self._indent() + "}")
            return "\n".join(lines)
        if isinstance(node, DecoratorStatement):
            return self._indent() + f"// @{node.name}"
        if isinstance(node, StaticMethodDeclaration):
            func = self._gen_statement(node.declaration)
            return func.replace("function ", "static function ", 1)
        # v0.5.0 Masterpiece
        if isinstance(node, RecordDefinition): return self._gen_record_definition(node)
        if isinstance(node, PropertyDefinition): return self._gen_property_definition(node)
        if isinstance(node, ExtensionDefinition): return self._gen_extension_definition(node)
        return self._indent() + f"// {type(node).__name__}"

    def _gen_expression(self, node: ASTNode) -> str:
        if node is None: return "null"
        if isinstance(node, Literal):
            if node.value is None: return "null"
            if node.value is True: return "true"
            if node.value is False: return "false"
            if isinstance(node.value, str): return repr(node.value)
            return str(node.value)
        if isinstance(node, Identifier): return node.name
        if isinstance(node, BinaryOp):
            op_map = {"and": "&&", "or": "||", "^": "**", "==": "===", "!=": "!==",
                       "<": "<", ">": ">", "<=": "<=", ">=": ">=",
                       "&": "&", "|": "|", "<<": "<<", ">>": ">>", "//": "Math.floor",
                       "??": "??", "is": "instanceof"}
            op = op_map.get(node.operator, node.operator)
            return f"({self._gen_expression(node.left)} {op} {self._gen_expression(node.right)})"
        if isinstance(node, UnaryOp):
            m = {"neg": "-", "not": "!", "~": "~"}
            return f"({m.get(node.operator, '')}{self._gen_expression(node.operand)})"
        if isinstance(node, Call):
            callee = self._gen_expression(node.callee)
            args = ", ".join(self._gen_expression(a) for a in node.arguments)
            if isinstance(node.callee, Identifier):
                if node.callee.name == "print": return f"console.log({args})"
                if node.callee.name == "input": return f"prompt({args})"
            return f"{callee}({args})"
        if isinstance(node, Attribute): return f"{self._gen_expression(node.object)}.{node.attribute}"
        if isinstance(node, Index): return f"{self._gen_expression(node.object)}[{self._gen_expression(node.index)}]"
        if isinstance(node, ListLiteral):
            return "[" + ", ".join(self._gen_expression(e) for e in node.elements) + "]"
        if isinstance(node, DictLiteral):
            pairs = ", ".join(f"{self._gen_expression(k)}: {self._gen_expression(v)}" for k, v in node.pairs)
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
                    parts.append("${" + self._gen_expression(p) + "}")
            return "`" + "".join(parts) + "`"
        if isinstance(node, ListComprehension):
            e = self._gen_expression(node.expression)
            it = self._gen_expression(node.iterable)
            c = f".filter(({node.variable}) => {self._gen_expression(node.condition)})" if node.condition else ""
            return f"{it}.map(({node.variable}) => {e}){c}"
        if isinstance(node, InExpression): return f"({self._gen_expression(node.left)} in {self._gen_expression(node.right)})"
        if isinstance(node, IsExpression): return f"({self._gen_expression(node.left)} instanceof {self._gen_expression(node.right)})"
        if isinstance(node, RangeLiteral): return f"Array.from({{length: {self._gen_expression(node.end)} - {self._gen_expression(node.start)} + 1}}, (_, i) => i + {self._gen_expression(node.start)})"
        if isinstance(node, GeneratorExpression): return self._gen_generator(node)
        if isinstance(node, IncrementExpression): return f"++{node.target}" if node.prefix else f"{node.target}++"
        if isinstance(node, DecrementExpression): return f"--{node.target}" if node.prefix else f"{node.target}--"
        return f"null as any"

    def _gen_if(self, node):
        lines = [self._indent() + f"if ({self._gen_expression(node.condition)}) {{"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        for cond, body in node.elif_branches:
            lines.append(self._indent() + f"}} else if ({self._gen_expression(cond)}) {{")
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
            lines.append(self._indent() + f"for (let {node.variable} of {self._gen_expression(node.iterable)}) {{")
        else:
            fv = self._gen_expression(node.range_from)
            tv = self._gen_expression(node.range_to)
            lines.append(self._indent() + f"for (let {node.variable} = {fv}; {node.variable} <= {tv}; {node.variable}++) {{")
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_while(self, node):
        lines = [self._indent() + f"while ({self._gen_expression(node.condition)}) {{"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_repeat(self, node):
        lines = [self._indent() + f"for (let _i = 0; _i < {self._gen_expression(node.times)}; _i++) {{"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_function(self, node):
        params = ", ".join(f"{p}: any" for p in node.parameters)
        prefix = "async " if node.is_async else ""
        name = "constructor" if node.name == "constructor" else node.name
        if name == "constructor":
            lines = [self._indent() + f"{prefix}constructor({params}) {{"]
        else:
            lines = [self._indent() + f"{prefix}function {name}({params}): any {{"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_class(self, node):
        parent = f" extends {node.parent}" if node.parent else ""
        lines = [self._indent() + f"class {node.name}{parent} {{"]
        self.indent_level += 1
        for s in node.body:
            if isinstance(s, FunctionDefinition) and s.name == "init":
                saved = s.name
                s.name = "constructor"
                lines.append(self._gen_statement(s))
                s.name = saved
            else:
                lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_try(self, node):
        lines = [self._indent() + "try {"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        if node.catch_body:
            v = f" ({node.catch_var}: any)" if node.catch_var else " (e: any)"
            lines.append(self._indent() + f"}} catch{v} {{")
            self.indent_level += 1
            for s in node.catch_body: lines.append(self._gen_statement(s))
            self.indent_level -= 1
        if node.finally_body:
            lines.append(self._indent() + "} finally {")
            self.indent_level += 1
            for s in node.finally_body: lines.append(self._gen_statement(s))
            self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_match(self, node):
        lines = [self._indent() + f"switch ({self._gen_expression(node.expression)}) {{"]
        self.indent_level += 1
        for pattern, body in node.cases:
            lines.append(self._indent() + f"case {self._gen_expression(pattern)}:")
            self.indent_level += 1
            for s in body: lines.append(self._gen_statement(s))
            lines.append(self._indent() + "break;")
            self.indent_level -= 1
        if node.default_body:
            lines.append(self._indent() + "default:")
            self.indent_level += 1
            for s in node.default_body: lines.append(self._gen_statement(s))
            self.indent_level -= 1
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_import(self, node):
        if node.items:
            items = ", ".join(node.items)
            return self._indent() + f"import {{ {items} }} from '{node.module}';"
        return self._indent() + f"import '{node.module}';"


    def _gen_do_while(self, node):
        lines = [self._indent() + "do {"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + f"}} while ({self._gen_expression(node.condition)});")
        return "\n".join(lines)

    def _gen_enum(self, node):
        lines = [self._indent() + f"enum {node.name} {{"]
        for i, member in enumerate(node.members):
            lines.append(self._indent() + f"  {member} = {i},")
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_destructuring(self, node):
        if node.destructure_type == "list":
            targets = "[" + ", ".join(node.targets) + "]"
        else:
            targets = "{" + ", ".join(node.targets) + "}"
        value = self._gen_expression(node.value)
        return self._indent() + f"let {targets} = {value};"

    def _gen_generator(self, node):
        expr = self._gen_expression(node.expression)
        it = self._gen_expression(node.iterable)
        if node.condition:
            cond = self._gen_expression(node.condition)
            return f"(function*() {{ for (let {node.variable} of {it}) {{ if ({cond}) yield {expr}; }} }})()"
        return f"(function*() {{ for (let {node.variable} of {it}) {{ yield {expr}; }} }})()"

    def _gen_augmented_assignment(self, node):
        val = self._gen_expression(node.value)
        target = node.target
        if node.operator == "||":
            return self._indent() + f"{target} ||= {val};"
        if node.operator == "&&":
            return self._indent() + f"{target} &&= {val};"
        if node.operator == "??":
            return self._indent() + f"{target} ??= {val};"
        return self._indent() + f"{target} {node.operator}= {val};"

    # ---- v0.5.0 Masterpiece Codegen ----

    def _gen_record_definition(self, node: RecordDefinition) -> str:
        """define record -> TS readonly interface + factory"""
        lines = [self._indent() + f"interface {node.name} {{"]
        self.indent_level += 1
        for fname, ftype, _ in node.fields:
            ts_type = {"int": "number", "integer": "number", "float": "number",
                       "string": "string", "bool": "boolean", "boolean": "boolean",
                       "list": "any[]", "dict": "Record<string, any>",
                       "any": "any"}.get(ftype, "any")
            lines.append(self._indent() + f"readonly {fname}: {ts_type};")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        lines.append(self._indent() + f"function create{node.name}({', '.join(f'{fname}: {self._ts_type(ftype)}' for fname, ftype, _ in node.fields)}): {node.name} {{")
        self.indent_level += 1
        fields_obj = ", ".join(f"{fname}" for fname, _, _ in node.fields)
        lines.append(self._indent() + f"return Object.freeze({{ {fields_obj} }});")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _ts_type(self, ftype: str) -> str:
        return {"int": "number", "integer": "number", "float": "number",
                "string": "string", "bool": "boolean", "boolean": "boolean",
                "any": "any"}.get(ftype, "any")

    def _gen_property_definition(self, node: PropertyDefinition) -> str:
        """define property -> TS get/set accessors"""
        lines = []
        ts_type = self._ts_type(node.type_annotation.type_name) if node.type_annotation else "any"
        if node.getter_body:
            lines.append(self._indent() + f"get {node.name}(): {ts_type} {{")
            self.indent_level += 1
            for stmt in node.getter_body:
                lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
            lines.append(self._indent() + "}")
        if node.setter_body:
            lines.append(self._indent() + f"set {node.name}({node.setter_param}: {ts_type}) {{")
            self.indent_level += 1
            for stmt in node.setter_body:
                lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
            lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_extension_definition(self, node: ExtensionDefinition) -> str:
        """define extension on Type -> TS declaration merging + prototype"""
        lines = [self._indent() + f"// Extension methods for {node.target_type}"]
        lines.append(self._indent() + f"declare global {{ interface {node.target_type} {{ }}")
        self.indent_level += 1
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                params = ", ".join(f"{p}: any" for p in stmt.parameters)
                lines.append(self._indent() + f"{stmt.name}({params}): any;")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                params = ", ".join(f"{p}: any" for p in stmt.parameters)
                lines.append(self._indent() + f"{node.target_type}.prototype.{stmt.name} = function({params}): any {{")
                self.indent_level += 1
                for s in stmt.body:
                    lines.append(self._gen_statement(s))
                self.indent_level -= 1
                lines.append(self._indent() + "};")
        return "\n".join(lines)


def generate_typescript(ast: Program) -> str:
    return TypeScriptGenerator(ast).generate()
