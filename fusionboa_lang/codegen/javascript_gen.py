"""
FusionBoa → JavaScript Code Generator

Translates a FusionBoa AST into equivalent JavaScript (ES6+) source code.
Supports all Fusion features.
"""

from ..parser.ast_nodes import *


class JavaScriptGenerator:
    """Generates JavaScript code from a FusionBoa AST."""

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
            BreakStatement: lambda n: self._indent() + "break;",
            ContinueStatement: lambda n: self._indent() + "continue;",
            PassStatement: lambda n: self._indent() + "// pass",
            ImportStatement: self._gen_import_statement,
            ExportStatement: self._gen_export_statement,
            TryStatement: self._gen_try_statement,
            PrintStatement: self._gen_print_statement,
            InputStatement: self._gen_input_statement,
            DoWhileLoop: self._gen_do_while_loop,
            EnumDefinition: self._gen_enum_definition,
            DestructuringDeclaration: self._gen_destructuring_declaration,
            IncrementExpression: self._gen_increment_expression,
            DecrementExpression: self._gen_decrement_expression,
            WithStatement: self._gen_with_statement,
            DecoratorStatement: self._gen_decorator_statement,
            StaticMethodDeclaration: self._gen_static_method_declaration,
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
        if isinstance(node, LengthExpression): return f"{self._gen_expression(node.expression)}.length"
        if isinstance(node, AwaitExpression): return f"await {self._gen_expression(node.expression)}"
        if isinstance(node, ListComprehension): return self._gen_list_comprehension(node)
        if isinstance(node, StringInterpolation): return self._gen_string_interpolation(node)
        if isinstance(node, SpreadElement): return f"...{self._gen_expression(node.expression)}"
        if isinstance(node, KeywordArgument): return f"{node.name}: {self._gen_expression(node.value)}"
        if isinstance(node, RangeLiteral): return f"Array.from({{length: {self._gen_expression(node.end)} - {self._gen_expression(node.start)} + 1}}, (_, i) => i + {self._gen_expression(node.start)})"
        if isinstance(node, InExpression): return f"({self._gen_expression(node.left)} in {self._gen_expression(node.right)})"
        if isinstance(node, IsExpression): return f"(typeof {self._gen_expression(node.left)} === 'object')"
        if isinstance(node, GeneratorExpression): return self._gen_generator_expression(node)
        if isinstance(node, IncrementExpression): return f"++{node.target}" if node.prefix else f"{node.target}++"
        if isinstance(node, DecrementExpression): return f"--{node.target}" if node.prefix else f"{node.target}--"
        return f"/* Unknown: {type(node).__name__} */"

    def _gen_literal(self, node: Literal) -> str:
        if node.value is None: return "null"
        if node.value is True: return "true"
        if node.value is False: return "false"
        if isinstance(node.value, str): return repr(node.value)
        return str(node.value)

    def _auto_str(self, expr_str: str, expr_node: ASTNode) -> str:
        return expr_str  # JS auto-coerces with + already

    def _gen_binary_op(self, node: BinaryOp) -> str:
        op_map = {"and": "&&", "or": "||", "^": "**"}
        op_map.update({"==": "==", "!=": "!=", "<": "<", ">": ">",
                       "<=": "<=", ">=": ">=", "+": "+", "-": "-",
                       "*": "*", "/": "/", "//": "/**/", "%": "%",
                       "&": "&", "|": "|", "<<": "<<", ">>": ">>",
                       "??": "??", "in": "in", "not in": "!in", "is": "instanceof"})
        js_op = op_map.get(node.operator, node.operator)
        left = self._gen_expression(node.left)
        right = self._gen_expression(node.right)
        return f"({left} {js_op} {right})"

    def _gen_unary_op(self, node: UnaryOp) -> str:
        op_map = {"neg": "-", "not": "!", "~": "~"}
        js_op = op_map.get(node.operator, node.operator)
        operand = self._gen_expression(node.operand)
        return f"({js_op}{operand})"

    def _gen_call(self, node: Call) -> str:
        callee = self._gen_expression(node.callee)
        args = ", ".join(self._gen_expression(a) for a in node.arguments)
        if isinstance(node.callee, Identifier):
            if node.callee.name == "print":
                return f"console.log({args})"
            if node.callee.name == "input":
                return f"prompt({args})"
        return f"{callee}({args})"

    def _gen_attribute(self, node: Attribute) -> str:
        return f"{self._gen_expression(node.object)}.{node.attribute}"

    def _gen_index(self, node: Index) -> str:
        return f"{self._gen_expression(node.object)}[{self._gen_expression(node.index)}]"

    def _gen_list_literal(self, node: ListLiteral) -> str:
        return "[" + ", ".join(self._gen_expression(e) for e in node.elements) + "]"

    def _gen_dict_literal(self, node: DictLiteral) -> str:
        pairs = ", ".join(f"{self._gen_expression(k)}: {self._gen_expression(v)}" for k, v in node.pairs)
        return "{" + pairs + "}"

    def _gen_lambda(self, node: Lambda) -> str:
        params = ", ".join(node.parameters)
        body = self._gen_expression(node.body)
        return f"({params}) => {body}"

    def _gen_ternary(self, node: Ternary) -> str:
        return f"({self._gen_expression(node.condition)} ? {self._gen_expression(node.true_value)} : {self._gen_expression(node.false_value)})"

    def _gen_list_comprehension(self, node: ListComprehension) -> str:
        expr = self._gen_expression(node.expression)
        iterable = self._gen_expression(node.iterable)
        cond = f".filter({node.variable} => {self._gen_expression(node.condition)})" if node.condition else ""
        return f"{iterable}.map({node.variable} => {expr}){cond}"

    def _gen_string_interpolation(self, node: StringInterpolation) -> str:
        parts = []
        for p in node.parts:
            if isinstance(p, Literal) and isinstance(p.value, str):
                parts.append(p.value)
            else:
                parts.append("${" + self._gen_expression(p) + "}")
        return "`" + "".join(parts) + "`"

    def _gen_expression_statement(self, node: ExpressionStatement) -> str:
        return self._indent() + self._gen_expression(node.expression) + ";"

    def _gen_variable_declaration(self, node: VariableDeclaration) -> str:
        return self._indent() + f"let {node.name} = {self._gen_expression(node.value)};"

    def _gen_const_declaration(self, node: ConstDeclaration) -> str:
        return self._indent() + f"const {node.name} = {self._gen_expression(node.value)};"

    def _gen_assignment(self, node: Assignment) -> str:
        return self._indent() + f"{node.target} = {self._gen_expression(node.value)};"

    def _gen_augmented_assignment(self, node: AugmentedAssignment) -> str:
        return self._indent() + f"{node.target} {node.operator}= {self._gen_expression(node.value)};"

    def _gen_if_statement(self, node: IfStatement) -> str:
        lines = [self._indent() + f"if ({self._gen_expression(node.condition)}) {{"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        for i, (elif_cond, elif_body) in enumerate(node.elif_branches):
            lines.append(self._indent() + ("} else if (" if i == 0 else "else if (") + f"{self._gen_expression(elif_cond)}) {{")
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
        lines = [self._indent() + f"switch ({self._gen_expression(node.expression)}) {{"]
        self.indent_level += 1
        for pattern, body in node.cases:
            lines.append(self._indent() + f"case {self._gen_expression(pattern)}:")
            self.indent_level += 1
            for stmt in body: lines.append(self._gen_statement(stmt))
            lines.append(self._indent() + "break;")
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
            lines.append(self._indent() + f"for (let {node.variable} of {self._gen_expression(node.iterable)}) {{")
        else:
            from_v = self._gen_expression(node.range_from)
            to_v = self._gen_expression(node.range_to)
            lines.append(self._indent() + f"for (let {node.variable} = {from_v}; {node.variable} <= {to_v}; {node.variable}++) {{")
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_repeat_loop(self, node: RepeatLoop) -> str:
        lines = [self._indent() + f"for (let __fusionboa_i = 0; __fusionboa_i < {self._gen_expression(node.times)}; __fusionboa_i++) {{"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_while_loop(self, node: WhileLoop) -> str:
        lines = [self._indent() + f"while ({self._gen_expression(node.condition)}) {{"]
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
            params.append(f"...{node.rest_param_name}")
        param_strs = []
        for p in params:
            if p in node.defaults:
                param_strs.append(f"{p} = {self._gen_expression(node.defaults[p])}")
            else:
                param_strs.append(p)
        if node.name == "constructor":
            lines.append(self._indent() + f"{prefix}constructor({', '.join(param_strs)}) {{")
        else:
            lines.append(self._indent() + f"{prefix}function {node.name}({', '.join(param_strs)}) {{")
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_class_definition(self, node: ClassDefinition) -> str:
        lines = []
        if node.parent:
            lines.append(self._indent() + f"class {node.name} extends {node.parent} {{")
        else:
            lines.append(self._indent() + f"class {node.name} {{")
        self.indent_level += 1
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition) and stmt.name == "init":
                stmt.name = "constructor"
            lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_return_statement(self, node: ReturnStatement) -> str:
        if node.value:
            return self._indent() + f"return {self._gen_expression(node.value)};"
        return self._indent() + "return;"

    def _gen_yield_statement(self, node: YieldStatement) -> str:
        if node.value:
            return self._indent() + f"yield {self._gen_expression(node.value)};"
        return self._indent() + "yield;"

    def _gen_import_statement(self, node: ImportStatement) -> str:
        if node.items:
            items = ", ".join(node.items)
            return self._indent() + f"import {{ {items} }} from '{node.module}';"
        if node.alias:
            return self._indent() + f"import * as {node.alias} from '{node.module}';"
        return self._indent() + f"import '{node.module}';"

    def _gen_export_statement(self, node: ExportStatement) -> str:
        return "export " + self._gen_statement(node.declaration)

    def _gen_try_statement(self, node: TryStatement) -> str:
        lines = [self._indent() + "try {"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        if node.catch_body:
            if node.catch_var:
                lines.append(self._indent() + f"}} catch ({node.catch_var}) {{")
            else:
                lines.append(self._indent() + "} catch (_) {")
            self.indent_level += 1
            for stmt in node.catch_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        if node.finally_body:
            lines.append(self._indent() + "} finally {")
            self.indent_level += 1
            for stmt in node.finally_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_print_statement(self, node: PrintStatement) -> str:
        if node.expression:
            return self._indent() + f"console.log({self._gen_expression(node.expression)});"
        return self._indent() + "console.log();"

    def _gen_input_statement(self, node: InputStatement) -> str:
        if node.target:
            if node.prompt:
                return self._indent() + f"let {node.target} = prompt({repr(node.prompt)});"
            return self._indent() + f"let {node.target} = prompt();"
        return self._indent() + "prompt();"

    def _gen_do_while_loop(self, node: DoWhileLoop) -> str:
        lines = [self._indent() + "do {"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + f"}} while ({self._gen_expression(node.condition)});")
        return "\n".join(lines)

    def _gen_enum_definition(self, node: EnumDefinition) -> str:
        lines = [self._indent() + f"// enum {node.name}"]
        for i, member in enumerate(node.members):
            lines.append(self._indent() + f"const {node.name}_{member} = {i};")
        return "\n".join(lines)

    def _gen_destructuring_declaration(self, node: DestructuringDeclaration) -> str:
        """'let [a, b] be expr' -> let [a, b] = expr
        'let {name, age} be dict' -> let {name, age} = dict"""
        if node.destructure_type == "list":
            targets = "[" + ", ".join(node.targets) + "]"
        else:
            targets = "{" + ", ".join(node.targets) + "}"
        value = self._gen_expression(node.value)
        return self._indent() + f"let {targets} = {value};"

    def _gen_increment_expression(self, node: IncrementExpression) -> str:
        """x++ or ++x"""
        if node.prefix:
            return self._indent() + f"++{node.target};"
        return self._indent() + f"{node.target}++;"

    def _gen_decrement_expression(self, node: DecrementExpression) -> str:
        """x-- or --x"""
        if node.prefix:
            return self._indent() + f"--{node.target};"
        return self._indent() + f"{node.target}--;"

    def _gen_with_statement(self, node: WithStatement) -> str:
        """with resource as var: body -> try/finally cleanup"""
        lines = []
        resource = self._gen_expression(node.resource)
        var_name = node.variable if node.variable else "__fusionboa_resource"
        lines.append(self._indent() + f"let {var_name} = {resource};  // with statement")
        lines.append(self._indent() + "try {")
        self.indent_level += 1
        for stmt in node.body:
            lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "} finally {")
        self.indent_level += 1
        lines.append(self._indent() + f"// cleanup {var_name}")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_decorator_statement(self, node: DecoratorStatement) -> str:
        """@decorator -> // @decorator"""
        return self._indent() + f"// @{node.name}"

    def _gen_static_method_declaration(self, node: StaticMethodDeclaration) -> str:
        """define static function -> static function"""
        lines = [self._indent() + "static "]
        # Generate the function without the 'static ' prefix - append to first line
        func_lines = self._gen_function_definition(node.declaration).split('\n')
        if func_lines:
            func_lines[0] = self._indent() + "static " + func_lines[0].lstrip()
        return "\n".join(func_lines)

    def _gen_generator_expression(self, node: GeneratorExpression) -> str:
        """'(x for each x in items if cond)' -> function*() { for (x of items) if (cond) yield x }"""
        expr = self._gen_expression(node.expression)
        iterable = self._gen_expression(node.iterable)
        if node.condition:
            cond = self._gen_expression(node.condition)
            return f"(function*() {{ for (let {node.variable} of {iterable}) {{ if ({cond}) yield {expr}; }} }})()"
        return f"(function*() {{ for (let {node.variable} of {iterable}) {{ yield {expr}; }} }})()"




def generate_javascript(ast: Program) -> str:
    gen = JavaScriptGenerator(ast)
    return gen.generate()
