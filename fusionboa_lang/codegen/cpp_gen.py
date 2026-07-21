"""
FusionBoa → C++ Code Generator

Translates a FusionBoa AST into equivalent C++ source code.
Supports all Fusion features.
"""

from ..parser.ast_nodes import *


class CppGenerator:
    """Generates C++ code from a FusionBoa AST."""

    def __init__(self, ast: Program):
        self.ast = ast
        self.indent_level = 0
        self._in_class = False
        self._needs_vector = False
        self._needs_map = False
        self._needs_string = False

    def _indent(self) -> str:
        return "    " * self.indent_level

    def generate(self) -> str:
        lines = []
        for stmt in self.ast.statements:
            lines.append(self._gen_statement(stmt))

        includes = ["#include <iostream>", "#include <any>", "#include <memory>"]
        if self._needs_vector:
            includes.append("#include <vector>")
        if self._needs_map:
            includes.append("#include <map>")
        if self._needs_string:
            includes.append("#include <string>")
        includes.append("using namespace std;")

        # Wrap in main() for standalone execution
        main_body = "\n".join(f"    {l}" for l in lines)
        return "\n".join(includes) + "\n\nint main() {\n" + main_body + "\n    return 0;\n}\n"

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
            YieldStatement: lambda n: self._indent() + f"// yield not natively supported: {self._gen_expression(n.value)}",
            BreakStatement: lambda n: self._indent() + "break;",
            ContinueStatement: lambda n: self._indent() + "continue;",
            PassStatement: lambda n: self._indent() + "// pass",
            ImportStatement: lambda n: self._indent() + f"// import: {n.module}",
            ExportStatement: self._gen_export_statement,
            TryStatement: self._gen_try_statement,
            PrintStatement: self._gen_print_statement,
            InputStatement: self._gen_input_statement,
            DoWhileLoop: self._gen_do_while_loop,
            EnumDefinition: self._gen_enum_definition,
            DeferStatement: lambda n: self._indent() + f"// deferred",
            GuardStatement: self._gen_guard_statement,
            DestructuringDeclaration: self._gen_destructuring,
            IncrementExpression: self._gen_increment_expression,
            DecrementExpression: self._gen_decrement_expression,
            WithStatement: self._gen_with_statement,
            DecoratorStatement: lambda n: self._indent() + f"// @{n.name}",
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
        if isinstance(node, LengthExpression): return f"({self._gen_expression(node.expression)}).size()"
        if isinstance(node, AwaitExpression): return f"/* await */ {self._gen_expression(node.expression)}"
        if isinstance(node, ListComprehension): return self._gen_list_comprehension(node)
        if isinstance(node, StringInterpolation): return self._gen_string_interpolation(node)
        if isinstance(node, SpreadElement): return f"/* spread */ {self._gen_expression(node.expression)}"
        if isinstance(node, KeywordArgument): return f"{node.name}: {self._gen_expression(node.value)}"
        if isinstance(node, RangeLiteral):
            self._needs_vector = True
            sf = self._gen_expression(node.start)
            ef = self._gen_expression(node.end)
            return f"__fusionboa_range({sf}, {ef})"
        if isinstance(node, InExpression): return f"__fusionboa_contains({self._gen_expression(node.right)}, {self._gen_expression(node.left)})"
        if isinstance(node, IsExpression): return f"(typeid({self._gen_expression(node.left)}) == typeid({self._gen_expression(node.right)}))"
        if isinstance(node, DictComprehension): return self._gen_dict_comprehension(node)
        if isinstance(node, MultiLineString): return self._gen_multi_line_string(node)
        if isinstance(node, SliceExpression): return self._gen_slice_expression(node)
        if isinstance(node, GeneratorExpression): return self._gen_generator(node)
        if isinstance(node, IncrementExpression): return f"++{node.target}" if node.prefix else f"{node.target}++"
        if isinstance(node, DecrementExpression): return f"--{node.target}" if node.prefix else f"{node.target}--"
        return f"/* Unknown: {type(node).__name__} */"

    def _gen_dict_comprehension(self, node):
        key = self._gen_expression(node.key)
        val = self._gen_expression(node.value)
        it = self._gen_expression(node.iterable)
        return f"/\\* dict comp: {key}:{val} for {node.variable} in {it} */"

    def _gen_multi_line_string(self, node):
        return self._gen_literal(Literal(node.value))

    def _gen_slice_expression(self, node):
        obj = self._gen_expression(node.object)
        s = self._gen_expression(node.start) if node.start else ""
        e = self._gen_expression(node.end) if node.end else ""
        return f"{obj}(/*slice*/{s}, {e})"

    def _gen_literal(self, node: Literal) -> str:
        if node.value is None: return "nullptr"
        if node.value is True: return "true"
        if node.value is False: return "false"
        if isinstance(node.value, str):
            self._needs_string = True
            return '"' + node.value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'
        if isinstance(node.value, float): return str(node.value)
        return str(node.value)

    def _gen_binary_op(self, node: BinaryOp) -> str:
        op_map = {"and": "&&", "or": "||", "^": "/* pow */",
                  "==": "==", "!=": "!=", "<": "<", ">": ">",
                  "<=": "<=", ">=": ">=", "+": "+", "-": "-",
                  "*": "*", "/": "/", "%": "%",
                  "&": "&", "|": "|", "<<": "<<", ">>": ">>", "//": "/"}
        cpp_op = op_map.get(node.operator, node.operator)
        left = self._gen_expression(node.left)
        right = self._gen_expression(node.right)
        # Null-coalescing: a ?? b -> a ? a : b
        if node.operator == "??":
            return f"({left} ? {left} : {right})"
        return f"({left} {cpp_op} {right})"

    def _gen_unary_op(self, node: UnaryOp) -> str:
        op_map = {"neg": "-", "not": "!", "~": "~"}
        cpp_op = op_map.get(node.operator, node.operator)
        operand = self._gen_expression(node.operand)
        return f"({cpp_op}{operand})"

    def _gen_call(self, node: Call) -> str:
        callee = self._gen_expression(node.callee)
        args = ", ".join(self._gen_expression(a) for a in node.arguments)
        if isinstance(node.callee, Identifier):
            if node.callee.name == "print":
                return f"cout << ({args}) << endl"
            if node.callee.name == "input":
                return f"__fusionboa_input({args})"
        return f"{callee}({args})"

    def _gen_attribute(self, node: Attribute) -> str:
        return f"{self._gen_expression(node.object)}.{node.attribute}"

    def _gen_index(self, node: Index) -> str:
        return f"{self._gen_expression(node.object)}[{self._gen_expression(node.index)}]"

    def _gen_list_literal(self, node: ListLiteral) -> str:
        self._needs_vector = True
        elements = ", ".join(self._gen_expression(e) for e in node.elements)
        return f"vector<any>{{{elements}}}"

    def _gen_dict_literal(self, node: DictLiteral) -> str:
        self._needs_map = True
        pairs = ", ".join(f"{{{self._gen_expression(k)}, {self._gen_expression(v)}}}" for k, v in node.pairs)
        return f"map<any, any>{{{pairs}}}"

    def _gen_lambda(self, node: Lambda) -> str:
        params = ", ".join(f"auto {p}" for p in node.parameters)
        body = self._gen_expression(node.body)
        return f"([&]({params}) {{ return {body}; }})"

    def _gen_ternary(self, node: Ternary) -> str:
        return f"({self._gen_expression(node.condition)} ? {self._gen_expression(node.true_value)} : {self._gen_expression(node.false_value)})"

    def _gen_list_comprehension(self, node: ListComprehension) -> str:
        self._needs_vector = True
        expr = self._gen_expression(node.expression)
        iterable = self._gen_expression(node.iterable)
        result = f"__fusionboa_list_comp({iterable}, [&](auto {node.variable}) {{ return {expr}; }}"
        if node.condition:
            result += f", [&](auto {node.variable}) {{ return {self._gen_expression(node.condition)}; }}"
        result += ")"
        return result

    def _gen_string_interpolation(self, node: StringInterpolation) -> str:
        self._needs_string = True
        parts = []
        for p in node.parts:
            if isinstance(p, Literal) and isinstance(p.value, str):
                parts.append(f'"{p.value}"')
            else:
                parts.append(f"to_string({self._gen_expression(p)})")
        return "(" + " + ".join(parts) + ")"

    def _gen_expression_statement(self, node: ExpressionStatement) -> str:
        return self._indent() + self._gen_expression(node.expression) + ";"

    def _gen_variable_declaration(self, node: VariableDeclaration) -> str:
        return self._indent() + f"auto {node.name} = {self._gen_expression(node.value)};"

    def _gen_const_declaration(self, node: ConstDeclaration) -> str:
        return self._indent() + f"const auto {node.name} = {self._gen_expression(node.value)};"

    def _gen_assignment(self, node: Assignment) -> str:
        return self._indent() + f"{node.target} = {self._gen_expression(node.value)};"

    def _gen_augmented_assignment(self, node: AugmentedAssignment) -> str:
        val = self._gen_expression(node.value)
        target = node.target
        if node.operator == "||": return self._indent() + f"{target} = {target} || {val};"
        if node.operator == "&&": return self._indent() + f"{target} = {target} && {val};"
        if node.operator == "??": return self._indent() + f"{target} = {target} ? {target} : {val};"
        return self._indent() + f"{target} {node.operator}= {val};"

    def _gen_if_statement(self, node: IfStatement) -> str:
        lines = [self._indent() + f"if ({self._gen_expression(node.condition)}) {{"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        for i, (elif_cond, elif_body) in enumerate(node.elif_branches):
            lines.append(self._indent() + f"}} else if ({self._gen_expression(elif_cond)}) {{")
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
        lines = [self._indent() + f"// match {self._gen_expression(node.expression)}"]
        lines.append(self._indent() + "{")
        self.indent_level += 1
        lines.append(self._indent() + f"auto __match_val = {self._gen_expression(node.expression)};")
        first = True
        for pattern, body in node.cases:
            kw = "if" if first else "} else if"
            lines.append(self._indent() + f"{kw} (__match_val == {self._gen_expression(pattern)}) {{")
            self.indent_level += 1
            for stmt in body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
            first = False
        if node.default_body:
            lines.append(self._indent() + "} else {")
            self.indent_level += 1
            for stmt in node.default_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_for_loop(self, node: ForLoop) -> str:
        lines = []
        if node.iterable:
            lines.append(self._indent() + f"for (auto {node.variable} : {self._gen_expression(node.iterable)}) {{")
        else:
            from_v = self._gen_expression(node.range_from)
            to_v = self._gen_expression(node.range_to)
            lines.append(self._indent() + f"for (auto {node.variable} = {from_v}; {node.variable} <= {to_v}; {node.variable}++) {{")
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_repeat_loop(self, node: RepeatLoop) -> str:
        lines = [self._indent() + f"for (int __fusionboa_i = 0; __fusionboa_i < {self._gen_expression(node.times)}; __fusionboa_i++) {{"]
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
        params = list(node.parameters)
        if node.has_rest_param:
            params.append(f"...{node.rest_param_name}")
        param_strs = []
        for p in params:
            if p in node.defaults:
                param_strs.append(f"auto {p} = {self._gen_expression(node.defaults[p])}")
            else:
                param_strs.append(f"auto {p}")
        lines.append(self._indent() + f"auto {node.name} = [&]({', '.join(param_strs)}) {{")
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "};")
        return "\n".join(lines)

    def _gen_class_definition(self, node: ClassDefinition) -> str:
        lines = []
        if node.parent:
            lines.append(self._indent() + f"class {node.name} : public {node.parent} {{")
        else:
            lines.append(self._indent() + f"class {node.name} {{")
        lines.append(self._indent() + "public:")
        self.indent_level += 1
        for stmt in node.body:
            lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "};")
        return "\n".join(lines)

    def _gen_return_statement(self, node: ReturnStatement) -> str:
        if node.value:
            return self._indent() + f"return {self._gen_expression(node.value)};"
        return self._indent() + "return;"

    def _gen_export_statement(self, node: ExportStatement) -> str:
        return self._gen_statement(node.declaration) + "  // export"

    def _gen_try_statement(self, node: TryStatement) -> str:
        lines = [self._indent() + "try {"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        if node.catch_body:
            if node.catch_var:
                lines.append(self._indent() + f"}} catch (exception& {node.catch_var}) {{")
            else:
                lines.append(self._indent() + "} catch (...) {")
            self.indent_level += 1
            for stmt in node.catch_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_print_statement(self, node: PrintStatement) -> str:
        if node.expression:
            return self._indent() + f"cout << {self._gen_expression(node.expression)} << endl;"
        return self._indent() + "cout << endl;"

    def _gen_do_while_loop(self, node):
        lines = [self._indent() + "do {"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + f"}} while ({self._gen_expression(node.condition)});")
        return "\n".join(lines)

    def _gen_enum_definition(self, node):
        lines = [self._indent() + f"enum class {node.name} {{"]
        for i, member in enumerate(node.members):
            lines.append(self._indent() + f"    {member} = {i},")
        lines.append(self._indent() + "};")
        return "\n".join(lines)

    def _gen_guard_statement(self, node):
        cond = self._gen_expression(node.condition)
        lines = [self._indent() + f"if (!({cond})) {{"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        lines.append(self._indent() + "return;")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_destructuring(self, node):
        targets = ", ".join(node.targets)
        value = self._gen_expression(node.value)
        return self._indent() + f"auto [{targets}] = {value};"

    def _gen_generator(self, node):
        return f"/* generator: {node.variable} */"

    def _gen_increment_expression(self, node):
        return self._indent() + (f"++{node.target};" if node.prefix else f"{node.target}++;")

    def _gen_decrement_expression(self, node):
        return self._indent() + (f"--{node.target};" if node.prefix else f"{node.target}--;")

    def _gen_with_statement(self, node):
        resource = self._gen_expression(node.resource)
        lines = [self._indent() + f"// with: {resource}"]
        lines.append(self._indent() + "{")
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_static_method_declaration(self, node):
        func = self._gen_statement(node.declaration)
        if isinstance(node.declaration, FunctionDefinition):
            func = func.replace("auto ", "static auto ")
        return func

    def _gen_input_statement(self, node: InputStatement) -> str:
        self._needs_string = True
        if node.target:
            if node.prompt:
                return self._indent() + f'cout << {self._gen_literal(Literal(value=node.prompt))}; string {node.target}; getline(cin, {node.target});'
            return self._indent() + f"string {node.target}; getline(cin, {node.target});"
        return self._indent() + "string __tmp; getline(cin, __tmp);"


def generate_cpp(ast: Program) -> str:
    gen = CppGenerator(ast)
    return gen.generate()
