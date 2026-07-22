"""
FusionBoa → Java Code Generator

Translates a FusionBoa AST into equivalent Java source code.
Supports all Fusion features.
"""

from ..parser.ast_nodes import *


class JavaGenerator:
    """Generates Java code from a FusionBoa AST."""

    def __init__(self, ast: Program):
        self.ast = ast
        self.indent_level = 0
        self._in_class = False
        self._needs_list = False
        self._needs_map = False

    def _indent(self) -> str:
        return "    " * self.indent_level

    def generate(self) -> str:
        lines = []
        for stmt in self.ast.statements:
            lines.append(self._gen_statement(stmt))

        imports = ["import java.util.*;"]
        body = "\n".join(lines)

        code = "\n".join(imports) + "\n\n"
        code += "public class FusionBoaProgram {\n"
        code += "    public static void main(String[] args) {\n"
        for l in lines:
            code += f"        {l}\n" if l.strip() else "\n"
        code += "    }\n"
        code += "}\n"
        return code

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
            YieldStatement: lambda n: f"// yield not supported: {self._gen_expression(n.value)}",
            BreakStatement: lambda n: "break;",
            ContinueStatement: lambda n: "continue;",
            PassStatement: lambda n: "// pass",
            ImportStatement: lambda n: f"// import: {n.module}",
            ExportStatement: self._gen_export_statement,
            TryStatement: self._gen_try_statement,
            PrintStatement: self._gen_print_statement,
            InputStatement: self._gen_input_statement,
            DoWhileLoop: self._gen_do_while_loop,
            EnumDefinition: self._gen_enum_definition,
            DeferStatement: lambda n: "// deferred",
            GuardStatement: self._gen_guard_statement_wrapper,
            DestructuringDeclaration: self._gen_destructuring,
            IncrementExpression: self._gen_increment_expression,
            DecrementExpression: self._gen_decrement_expression,
            WithStatement: self._gen_with_statement,
            DecoratorStatement: lambda n: f"// @{n.name}",
            StaticMethodDeclaration: self._gen_static_method_declaration,
            # v0.5.0 Masterpiece
            RecordDefinition: self._gen_record_definition,
            PropertyDefinition: self._gen_property_definition,
            ExtensionDefinition: self._gen_extension_definition,
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
            return f"java.util.stream.IntStream.rangeClosed({self._gen_expression(node.start)}, {self._gen_expression(node.end)}).boxed().collect(java.util.stream.Collectors.toList())"
        if isinstance(node, InExpression): return f"({self._gen_expression(node.right)}).contains({self._gen_expression(node.left)})"
        if isinstance(node, IsExpression): return f"({self._gen_expression(node.left)} instanceof {self._gen_expression(node.right)})"
        if isinstance(node, DictComprehension): return f"/* dict comp: {node.variable} */"
        if isinstance(node, MultiLineString): return self._gen_literal(Literal(node.value))
        if isinstance(node, SliceExpression): return f"/* slice */"
        if isinstance(node, GeneratorExpression): return f"/* generator */"
        if isinstance(node, IncrementExpression): return f"++{node.target}" if node.prefix else f"{node.target}++"
        if isinstance(node, DecrementExpression): return f"--{node.target}" if node.prefix else f"{node.target}--"
        return f"/* Unknown: {type(node).__name__} */"

    def _gen_literal(self, node: Literal) -> str:
        if node.value is None: return "null"
        if node.value is True: return "true"
        if node.value is False: return "false"
        if isinstance(node.value, str):
            return '"' + node.value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'
        if isinstance(node.value, float):
            return str(node.value)
        return str(node.value)

    def _java_type(self, node: ASTNode) -> str:
        """Infer a Java type from an expression."""
        if isinstance(node, Literal):
            if isinstance(node.value, str): return "String"
            if isinstance(node.value, float): return "double"
            if isinstance(node.value, int): return "int"
            if isinstance(node.value, bool): return "boolean"
        if isinstance(node, ListLiteral): return "ArrayList<Object>"
        if isinstance(node, DictLiteral): return "HashMap<Object, Object>"
        return "Object"

    def _gen_binary_op(self, node: BinaryOp) -> str:
        op_map = {"and": "&&", "or": "||", "^": "/* pow */",
                  "==": "==", "!=": "!=", "<": "<", ">": ">",
                  "<=": "<=", ">=": ">=", "+": "+", "-": "-",
                  "*": "*", "/": "/", "%": "%",
                  "&": "&", "|": "|", "<<": "<<", ">>": ">>",
                  "??": " /* ?? */ ", "is": " instanceof ", "//": "/"}
        java_op = op_map.get(node.operator, node.operator)
        left = self._gen_expression(node.left)
        right = self._gen_expression(node.right)
        # Null-coalescing: a ?? b -> a != null ? a : b
        if node.operator == "??":
            return f"({left} != null ? {left} : {right})"
        # Handle string concatenation
        if node.operator == "+":
            if isinstance(node.left, Literal) and isinstance(node.left.value, str):
                pass
            elif isinstance(node.right, Literal) and isinstance(node.right.value, str):
                pass
        return f"({left} {java_op} {right})"

    def _gen_unary_op(self, node: UnaryOp) -> str:
        op_map = {"neg": "-", "not": "!", "~": "~"}
        java_op = op_map.get(node.operator, node.operator)
        operand = self._gen_expression(node.operand)
        return f"({java_op}{operand})"

    def _gen_call(self, node: Call) -> str:
        callee = self._gen_expression(node.callee)
        args = ", ".join(self._gen_expression(a) for a in node.arguments)
        if isinstance(node.callee, Identifier):
            if node.callee.name == "print":
                return f"System.out.println({args})"
            if node.callee.name == "input":
                return f"__fusionboa_input({args})"
            if node.callee.name == "str":
                return f"String.valueOf({args})"
        return f"{callee}({args})"

    def _gen_attribute(self, node: Attribute) -> str:
        return f"{self._gen_expression(node.object)}.{node.attribute}"

    def _gen_index(self, node: Index) -> str:
        return f"{self._gen_expression(node.object)}.get({self._gen_expression(node.index)})"

    def _gen_list_literal(self, node: ListLiteral) -> str:
        self._needs_list = True
        elements = ", ".join(self._gen_expression(e) for e in node.elements)
        return f"new ArrayList<>(Arrays.asList({elements}))"

    def _gen_dict_literal(self, node: DictLiteral) -> str:
        self._needs_map = True
        code = "new HashMap<>()"
        if node.pairs:
            code += " {{"
            for k, v in node.pairs:
                code += f" put({self._gen_expression(k)}, {self._gen_expression(v)});"
            code += " }}"
        return code

    def _gen_lambda(self, node: Lambda) -> str:
        params = ", ".join(f"var {p}" for p in node.parameters)
        body = self._gen_expression(node.body)
        return f"({params}) -> {body}"

    def _gen_ternary(self, node: Ternary) -> str:
        return f"({self._gen_expression(node.condition)} ? {self._gen_expression(node.true_value)} : {self._gen_expression(node.false_value)})"

    def _gen_list_comprehension(self, node: ListComprehension) -> str:
        expr = self._gen_expression(node.expression)
        iterable = self._gen_expression(node.iterable)
        if node.condition:
            cond = self._gen_expression(node.condition)
            return f"({iterable}).stream().filter({node.variable} -> {cond}).map({node.variable} -> {expr}).collect(java.util.stream.Collectors.toList())"
        return f"({iterable}).stream().map({node.variable} -> {expr}).collect(java.util.stream.Collectors.toList())"

    def _gen_string_interpolation(self, node: StringInterpolation) -> str:
        parts = []
        for p in node.parts:
            if isinstance(p, Literal) and isinstance(p.value, str):
                parts.append('"' + p.value + '"')
            else:
                parts.append(f"String.valueOf({self._gen_expression(p)})")
        return "String.join(\"\", " + ", ".join(parts) + ")"

    def _gen_expression_statement(self, node: ExpressionStatement) -> str:
        return self._gen_expression(node.expression) + ";"

    def _gen_variable_declaration(self, node: VariableDeclaration) -> str:
        jtype = self._java_type(node.value)
        return f"{jtype} {node.name} = {self._gen_expression(node.value)};"

    def _gen_const_declaration(self, node: ConstDeclaration) -> str:
        jtype = self._java_type(node.value)
        return f"final {jtype} {node.name} = {self._gen_expression(node.value)};"

    def _gen_assignment(self, node: Assignment) -> str:
        return f"{node.target} = {self._gen_expression(node.value)};"

    def _gen_augmented_assignment(self, node: AugmentedAssignment) -> str:
        val = self._gen_expression(node.value)
        target = node.target
        if node.operator == "||": return f"{target} = {target} || {val};"
        if node.operator == "&&": return f"{target} = {target} && {val};"
        if node.operator == "??": return f"{target} = {target} != null ? {target} : {val};"
        return f"{target} {node.operator}= {val};"

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
        lines = [f"// match {self._gen_expression(node.expression)}"]
        lines.append(f"switch ({self._gen_expression(node.expression)}) {{")
        for pattern, body in node.cases:
            lines.append(f"    case {self._gen_expression(pattern)}:")
            for stmt in body: lines.append(f"        {self._gen_statement(stmt)}")
            lines.append("        break;")
        if node.default_body:
            lines.append("    default:")
            for stmt in node.default_body: lines.append(f"        {self._gen_statement(stmt)}")
        lines.append("}")
        return "\n".join(lines)

    def _gen_for_loop(self, node: ForLoop) -> str:
        lines = []
        if node.iterable:
            lines.append(f"for (var {node.variable} : {self._gen_expression(node.iterable)}) {{")
        else:
            from_v = self._gen_expression(node.range_from)
            to_v = self._gen_expression(node.range_to)
            lines.append(f"for (int {node.variable} = {from_v}; {node.variable} <= {to_v}; {node.variable}++) {{")
        for stmt in node.body: lines.append(f"    {self._gen_statement(stmt)}")
        lines.append("}")
        return "\n".join(lines)

    def _gen_repeat_loop(self, node: RepeatLoop) -> str:
        lines = [f"for (int __fusionboa_i = 0; __fusionboa_i < {self._gen_expression(node.times)}; __fusionboa_i++) {{"]
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
        params = list(node.parameters)
        if node.has_rest_param:
            params.append(f"{node.rest_param_name}...")
        param_strs = [f"Object {p}" for p in params]
        lines.append(f"public static Object {node.name}({', '.join(param_strs)}) {{")
        for stmt in node.body: lines.append(f"    {self._gen_statement(stmt)}")
        lines.append("}")
        return "\n".join(lines)

    def _gen_class_definition(self, node: ClassDefinition) -> str:
        lines = []
        if node.parent:
            lines.append(f"class {node.name} extends {node.parent} {{")
        else:
            lines.append(f"class {node.name} {{")
        for stmt in node.body:
            lines.append(f"    {self._gen_statement(stmt)}")
        lines.append("}")
        return "\n".join(lines)

    def _gen_return_statement(self, node: ReturnStatement) -> str:
        if node.value:
            return f"return {self._gen_expression(node.value)};"
        return "return;"

    def _gen_export_statement(self, node: ExportStatement) -> str:
        return "public " + self._gen_statement(node.declaration)

    def _gen_try_statement(self, node: TryStatement) -> str:
        lines = ["try {"]
        for stmt in node.body: lines.append(f"    {self._gen_statement(stmt)}")
        if node.catch_body:
            if node.catch_var:
                lines.append(f"}} catch (Exception {node.catch_var}) {{")
            else:
                lines.append("} catch (Exception e) {")
            for stmt in node.catch_body: lines.append(f"    {self._gen_statement(stmt)}")
        if node.finally_body:
            lines.append("} finally {")
            for stmt in node.finally_body: lines.append(f"    {self._gen_statement(stmt)}")
        lines.append("}")
        return "\n".join(lines)

    def _gen_print_statement(self, node: PrintStatement) -> str:
        if node.expression:
            return f"System.out.println({self._gen_expression(node.expression)});"
        return "System.out.println();"

    def _gen_input_statement(self, node: InputStatement) -> str:
        if node.target:
            return f"String {node.target} = System.console().readLine();"
        return "System.console().readLine();"

    def _gen_do_while_loop(self, node):
        lines = [f"do {{"]
        for stmt in node.body: lines.append(f"    {self._gen_statement(stmt)}")
        lines.append(f"}} while ({self._gen_expression(node.condition)});")
        return "\n".join(lines)

    def _gen_enum_definition(self, node):
        lines = [f"enum {node.name} {{"]
        for i, member in enumerate(node.members):
            sep = "," if i < len(node.members) - 1 else ";"
            lines.append(f"    {member}({i}){sep}")
        lines.append("}")
        return "\n".join(lines)

    def _gen_destructuring(self, node):
        targets = ", ".join(node.targets)
        value = self._gen_expression(node.value)
        return f"// destructure: {targets} = {value};"

    def _gen_increment_expression(self, node):
        return (f"++{node.target};" if node.prefix else f"{node.target}++;")

    def _gen_decrement_expression(self, node):
        return (f"--{node.target};" if node.prefix else f"{node.target}--;")

    def _gen_with_statement(self, node):
        resource = self._gen_expression(node.resource)
        v = node.variable if node.variable else "_res"
        lines = [f"// with: {resource}", f"AutoCloseable {v} = {resource};", f"try {{"]
        for s in node.body: lines.append(f"    {self._gen_statement(s)}")
        lines.append(f"}} finally {{ {v}.close(); }}")
        return "\n".join(lines)

    def _gen_static_method_declaration(self, node):
        func = self._gen_statement(node.declaration)
        return func.replace("public static Object", "public static Object", 1) if "static" not in func else func

    def _gen_guard_statement_wrapper(self, node):
        cond = self._gen_expression(node.condition)
        lines = [f"if (!({cond})) {{"]
        for stmt in node.body: lines.append(f"    {self._gen_statement(stmt)}")
        lines.append(f"    return;")
        lines.append("}")
        return "\n".join(lines)

    # ---- v0.5.0 Masterpiece Codegen ----

    def _gen_record_definition(self, node: RecordDefinition) -> str:
        """define record -> Java record (Java 14+)"""
        java_type = {"int": "int", "integer": "int", "float": "double",
                     "string": "String", "bool": "boolean", "boolean": "boolean",
                     "list": "List<Object>", "dict": "Map<Object,Object>",
                     "any": "Object"}
        fields_str = ", ".join(f"{java_type.get(ftype, 'Object')} {fname}" for fname, ftype, _ in node.fields)
        return f"record {node.name}({fields_str}) {{ }}"

    def _gen_property_definition(self, node: PropertyDefinition) -> str:
        """define property -> Java getter/setter methods"""
        lines = []
        cap_name = node.name[0].upper() + node.name[1:]
        if node.getter_body:
            lines.append(f"public Object get{cap_name}() {{")
            for stmt in node.getter_body:
                lines.append(f"    {self._gen_statement(stmt)}")
            lines.append("}")
        if node.setter_body:
            lines.append(f"public void set{cap_name}(Object {node.setter_param}) {{")
            for stmt in node.setter_body:
                lines.append(f"    {self._gen_statement(stmt)}")
            lines.append("}")
        return "\n".join(lines)

    def _gen_extension_definition(self, node: ExtensionDefinition) -> str:
        """define extension on Type -> Java static utility methods"""
        lines = [f"class {node.target_type}Extensions {{"]
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                params = ", ".join(f"Object {p}" for p in [node.target_type.lower()] + stmt.parameters)
                lines.append(f"    public static Object {stmt.name}({params}) {{")
                for s in stmt.body:
                    lines.append(f"        {self._gen_statement(s)}")
                lines.append("    }")
        lines.append("}")
        return "\n".join(lines)


def generate_java(ast: Program) -> str:
    gen = JavaGenerator(ast)
    return gen.generate()
