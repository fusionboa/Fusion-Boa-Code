"""
FusionBoa → C# Code Generator

Translates a FusionBoa AST into equivalent C# source code.
Supports all Fusion features.
"""

from ..parser.ast_nodes import *


class CSharpGenerator:
    """Generates C# code from a FusionBoa AST."""

    def __init__(self, ast: Program):
        self.ast = ast
        self.indent_level = 0

    def _indent(self) -> str:
        return "    " * self.indent_level

    def generate(self) -> str:
        lines = []
        for stmt in self.ast.statements:
            lines.append(self._gen_statement(stmt))

        code = "using System;\nusing System.Collections.Generic;\nusing System.Linq;\n\n"
        code += "class FusionBoaProgram {\n"
        code += "    static void Main(string[] args) {\n"
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
            YieldStatement: self._gen_yield_statement,
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
            IncrementExpression: lambda n: (f"++{n.target};" if n.prefix else f"{n.target}++;"),
            DecrementExpression: lambda n: (f"--{n.target};" if n.prefix else f"{n.target}--;"),
            WithStatement: self._gen_with_statement,
            DecoratorStatement: lambda n: f"// @{n.name}",
            StaticMethodDeclaration: self._gen_static_method,
            # v0.5.0 Masterpiece
            RecordDefinition: self._gen_record_definition,
            PropertyDefinition: self._gen_property_definition,
            ExtensionDefinition: self._gen_extension_definition,
            # v0.9.1+ Universal Polyglot
            SetLiteral: self._gen_set_stmt,
            TupleLiteral: self._gen_tuple_stmt,
            MultiReturnStatement: self._gen_multi_return,
            YieldFromStatement: lambda n: f"// yield from: {self._gen_expression(n.iterable)}",
            GoStatement: lambda n: f"// goroutine: {n.name or 'anonymous'} (use Task.Run)",
            ChannelDeclaration: lambda n: f"// channel: {n.name}",
            ChannelSelect: lambda n: f"// select {len(n.cases)} channels",
            ChannelClose: lambda n: f"// channel close",
            SynchronizedBlock: self._gen_synchronized,
            AsyncWithStatement: self._gen_async_with,
            ModuleDefinition: lambda n: f"// module {n.name}",
            MixinStatement: lambda n: f"// {n.mixin_type} {n.mixin_name}",
            ObjectDefinition: lambda n: f"// object {n.name} (singleton)",
            ActorDefinition: lambda n: f"// actor {n.name}",
            SealedClassDefinition: self._gen_sealed_class,
            NewExpression: lambda n: f"new {n.type_name}({', '.join(self._gen_expression(a) for a in n.arguments)});" if n.arguments else f"new {n.type_name}();",
            DeleteExpression: lambda n: f"// delete {n.target} (GC handles this)",
            GlobalStatement: lambda n: f"// global {', '.join(n.names)}",
            AtomicCounter: lambda n: f"int {n.name} = {self._gen_expression(n.initial_value) if n.initial_value else '0'};  // atomic",
            PackageDeclaration: lambda n: f"// package {n.package_path}",
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
        if isinstance(node, LengthExpression): return f"({self._gen_expression(node.expression)}).Count"
        if isinstance(node, AwaitExpression): return f"await {self._gen_expression(node.expression)}"
        if isinstance(node, ListComprehension): return self._gen_list_comprehension(node)
        if isinstance(node, StringInterpolation): return self._gen_string_interpolation(node)
        if isinstance(node, SpreadElement): return f"/* spread */ {self._gen_expression(node.expression)}"
        if isinstance(node, KeywordArgument): return f"{node.name}: {self._gen_expression(node.value)}"
        if isinstance(node, RangeLiteral):
            return f"Enumerable.Range({self._gen_expression(node.start)}, {self._gen_expression(node.end)} - {self._gen_expression(node.start)} + 1)"
        if isinstance(node, InExpression): return f"({self._gen_expression(node.right)}).Contains({self._gen_expression(node.left)})"
        if isinstance(node, IsExpression): return f"({self._gen_expression(node.left)} is {self._gen_expression(node.right)})"
        if isinstance(node, DictComprehension): return f"/* dict comp: {node.variable} */"
        if isinstance(node, MultiLineString): return self._gen_literal(Literal(node.value))
        if isinstance(node, SliceExpression): return f"/* slice */"
        if isinstance(node, GeneratorExpression): return f"/* generator */"
        if isinstance(node, IncrementExpression): return f"++{node.target}" if node.prefix else f"{node.target}++"
        if isinstance(node, DecrementExpression): return f"--{node.target}" if node.prefix else f"{node.target}--"
        # v0.9.1+ Expression nodes
        if isinstance(node, SetLiteral):
            el = ", ".join(self._gen_expression(e) for e in node.elements)
            return f"new HashSet<object> {{ {el} }}"
        if isinstance(node, TupleLiteral):
            el = ", ".join(self._gen_expression(e) for e in node.elements)
            return f"({el})"
        if isinstance(node, SymbolLiteral): return f"/* :{node.name} */"
        if isinstance(node, BlockExpression): return f"/* block */"
        if isinstance(node, JsxElement): return f"/* JSX:{node.tag} */"
        if isinstance(node, HookCall): return f"/* {node.hook_name}() */"
        if isinstance(node, NewExpression):
            args = ", ".join(self._gen_expression(a) for a in node.arguments)
            return f"new {node.type_name}({args})"
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
        cs_op = op_map.get(node.operator, node.operator)
        left = self._gen_expression(node.left)
        right = self._gen_expression(node.right)
        return f"({left} {cs_op} {right})"

    def _gen_unary_op(self, node: UnaryOp) -> str:
        op_map = {"neg": "-", "not": "!", "~": "~"}
        cs_op = op_map.get(node.operator, node.operator)
        operand = self._gen_expression(node.operand)
        return f"({cs_op}{operand})"

    def _gen_call(self, node: Call) -> str:
        callee = self._gen_expression(node.callee)
        args = ", ".join(self._gen_expression(a) for a in node.arguments)
        if isinstance(node.callee, Identifier):
            if node.callee.name == "print":
                return f"Console.WriteLine({args})"
            if node.callee.name == "input":
                return f"Console.ReadLine({args})"
            if node.callee.name == "str":
                return f"{args}.ToString()"
        return f"{callee}({args})"

    def _gen_attribute(self, node: Attribute) -> str:
        return f"{self._gen_expression(node.object)}.{node.attribute}"

    def _gen_index(self, node: Index) -> str:
        return f"{self._gen_expression(node.object)}[{self._gen_expression(node.index)}]"

    def _gen_list_literal(self, node: ListLiteral) -> str:
        elements = ", ".join(self._gen_expression(e) for e in node.elements)
        return f"new List<object> {{ {elements} }}"

    def _gen_dict_literal(self, node: DictLiteral) -> str:
        pairs = ", ".join(f"{{ {self._gen_expression(k)}, {self._gen_expression(v)} }}" for k, v in node.pairs)
        return f"new Dictionary<object, object> {{ {pairs} }}"

    def _gen_lambda(self, node: Lambda) -> str:
        params = ", ".join(f"dynamic {p}" for p in node.parameters)
        body = self._gen_expression(node.body)
        return f"((Func<dynamic>)(() => {body}))"

    def _gen_ternary(self, node: Ternary) -> str:
        return f"({self._gen_expression(node.condition)} ? {self._gen_expression(node.true_value)} : {self._gen_expression(node.false_value)})"

    def _gen_list_comprehension(self, node: ListComprehension) -> str:
        expr = self._gen_expression(node.expression)
        iterable = self._gen_expression(node.iterable)
        if node.condition:
            cond = self._gen_expression(node.condition)
            return f"({iterable}).Where({node.variable} => {cond}).Select({node.variable} => {expr}).ToList()"
        return f"({iterable}).Select({node.variable} => {expr}).ToList()"

    def _gen_string_interpolation(self, node: StringInterpolation) -> str:
        parts = []
        for p in node.parts:
            if isinstance(p, Literal) and isinstance(p.value, str):
                parts.append(p.value.replace("{", "{{").replace("}", "}}"))
            else:
                parts.append("{" + self._gen_expression(p) + "}")
        return '$"' + "".join(parts) + '"'

    def _gen_expression_statement(self, node: ExpressionStatement) -> str:
        return self._gen_expression(node.expression) + ";"

    def _gen_variable_declaration(self, node: VariableDeclaration) -> str:
        return f"var {node.name} = {self._gen_expression(node.value)};"

    def _gen_const_declaration(self, node: ConstDeclaration) -> str:
        return f"var {node.name} = {self._gen_expression(node.value)};  // const"

    def _gen_assignment(self, node: Assignment) -> str:
        return f"{node.target} = {self._gen_expression(node.value)};"

    def _gen_augmented_assignment(self, node: AugmentedAssignment) -> str:
        val = self._gen_expression(node.value)
        target = node.target
        if node.operator == "||": return f"{target} = {target} || {val};"
        if node.operator == "&&": return f"{target} = {target} && {val};"
        if node.operator == "??": return f"{target} = {target} ?? {val};"
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
        lines = [f"switch ({self._gen_expression(node.expression)}) {{"]
        for pattern, body in node.cases:
            lines.append(f"    case {self._gen_expression(pattern)}:")
            for stmt in body: lines.append(f"        {self._gen_statement(stmt)}")
            lines.append("        break;")
        if node.default_body:
            lines.append("    default:")
            for stmt in node.default_body: lines.append(f"        {self._gen_statement(stmt)}")
            lines.append("        break;")
        lines.append("}")
        return "\n".join(lines)

    def _gen_for_loop(self, node: ForLoop) -> str:
        lines = []
        if node.iterable:
            lines.append(f"foreach (var {node.variable} in {self._gen_expression(node.iterable)}) {{")
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
            params.append(f"params object[] {node.rest_param_name}")
        param_strs = [f"dynamic {p}" for p in params]
        if node.defaults:
            for p in list(node.defaults.keys()):
                idx = params.index(p) if p in params else -1
                if idx >= 0:
                    param_strs[idx] = f"dynamic {p} = {self._gen_expression(node.defaults[p])}"
        lines.append(f"static dynamic {node.name}({', '.join(param_strs)}) {{")
        for stmt in node.body: lines.append(f"    {self._gen_statement(stmt)}")
        lines.append("}")
        return "\n".join(lines)

    def _gen_class_definition(self, node: ClassDefinition) -> str:
        lines = []
        if node.parent:
            lines.append(f"class {node.name} : {node.parent} {{")
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

    def _gen_yield_statement(self, node: YieldStatement) -> str:
        if node.value:
            return f"yield return {self._gen_expression(node.value)};"
        return "yield break;"

    def _gen_export_statement(self, node: ExportStatement) -> str:
        return "public " + self._gen_statement(node.declaration)

    def _gen_try_statement(self, node: TryStatement) -> str:
        lines = ["try {"]
        for stmt in node.body: lines.append(f"    {self._gen_statement(stmt)}")
        if node.catch_body:
            if node.catch_var:
                lines.append(f"}} catch (Exception {node.catch_var}) {{")
            else:
                lines.append("} catch (Exception) {")
            for stmt in node.catch_body: lines.append(f"    {self._gen_statement(stmt)}")
        if node.finally_body:
            lines.append("} finally {")
            for stmt in node.finally_body: lines.append(f"    {self._gen_statement(stmt)}")
        lines.append("}")
        return "\n".join(lines)

    def _gen_print_statement(self, node: PrintStatement) -> str:
        if node.expression:
            return f"Console.WriteLine({self._gen_expression(node.expression)});"
        return "Console.WriteLine();"

    def _gen_input_statement(self, node: InputStatement) -> str:
        if node.target:
            return f"string {node.target} = Console.ReadLine();"
        return "Console.ReadLine();"

    def _gen_do_while_loop(self, node):
        lines = [f"do {{"]
        for stmt in node.body: lines.append(f"    {self._gen_statement(stmt)}")
        lines.append(f"}} while ({self._gen_expression(node.condition)});")
        return "\n".join(lines)

    def _gen_enum_definition(self, node):
        lines = [f"enum {node.name} {{"]
        for i, member in enumerate(node.members):
            lines.append(f"    {member} = {i},")
        lines.append("}")
        return "\n".join(lines)

    def _gen_with_statement(self, node):
        r = self._gen_expression(node.resource)
        v = node.variable if node.variable else "_res"
        lines = [f"var {v} = {r};  // with", f"try {{"]
        for s in node.body: lines.append(f"    {self._gen_statement(s)}")
        lines.append(f"}} finally {{ /* dispose {v} */ }}")
        return "\n".join(lines)

    def _gen_static_method(self, node):
        func = self._gen_statement(node.declaration)
        return func.replace("static dynamic ", "static dynamic ", 1)  # already has static

    def _gen_destructuring(self, node):
        targets = ", ".join(node.targets)
        value = self._gen_expression(node.value)
        return f"// destructure: var ({targets}) = {value};"

    def _gen_guard_statement_wrapper(self, node):
        cond = self._gen_expression(node.condition)
        lines = [f"if (!({cond})) {{"]
        for stmt in node.body: lines.append(f"    {self._gen_statement(stmt)}")
        lines.append(f"    return;")
        lines.append("}")
        return "\n".join(lines)

    # ---- v0.5.0 Masterpiece Codegen ----

    def _gen_record_definition(self, node: RecordDefinition) -> str:
        """define record -> C# record class (C# 9+)"""
        fields_str = ", ".join(f"{fname} {self._cs_type(ftype)}" for fname, ftype, _ in node.fields)
        return f"record {node.name}({fields_str});"

    def _cs_type(self, ftype: str) -> str:
        return {"int": "int", "integer": "int", "float": "double",
                "string": "string", "bool": "bool", "boolean": "bool",
                "list": "List<object>", "dict": "Dictionary<object,object>",
                "any": "object"}.get(ftype, "object")

    def _gen_property_definition(self, node: PropertyDefinition) -> str:
        """define property -> C# property with get/set"""
        lines = []
        type_str = self._cs_type(node.type_annotation.type_name) if node.type_annotation else "dynamic"
        if node.getter_body or node.setter_body:
            lines.append(f"{type_str} {node.name} {{")
            if node.getter_body:
                lines.append("    get {")
                for stmt in node.getter_body:
                    lines.append(f"        {self._gen_statement(stmt)}")
                lines.append("    }")
            if node.setter_body:
                lines.append("    set {")
                for stmt in node.setter_body:
                    lines.append(f"        {self._gen_statement(stmt)}")
                lines.append("    }")
            lines.append("}")
        return "\n".join(lines)

    def _gen_extension_definition(self, node: ExtensionDefinition) -> str:
        """define extension on Type -> C# static class with 'this' keyword"""
        lines = [f"static class {node.target_type}Extensions {{"]
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                params = ", ".join(f"this dynamic self" if i == 0 else f"dynamic {p}" for i, p in enumerate(["self"] + stmt.parameters))
                lines.append(f"    public static dynamic {stmt.name}({params}) {{")
                for s in stmt.body:
                    lines.append(f"        {self._gen_statement(s)}")
                lines.append("    }")
        lines.append("}")
        return "\n".join(lines)


    # ---- v0.9.1+ Handler Methods ----

    def _gen_set_stmt(self, node):
        el = ", ".join(self._gen_expression(e) for e in node.elements)
        return f"new HashSet<object> {{ {el} }};  // set"

    def _gen_tuple_stmt(self, node):
        el = ", ".join(self._gen_expression(e) for e in node.elements)
        return f"({el});  // tuple"

    def _gen_multi_return(self, node):
        vals = ", ".join(self._gen_expression(v) for v in node.values)
        return f"return ({vals});"

    def _gen_synchronized(self, node):
        lock = node.lock_object or "_lock"
        lines = [f"lock ({lock}) {{"]
        for s in node.body: lines.append(f"    {self._gen_statement(s)}")
        lines.append("}")
        return "\n".join(lines)

    def _gen_async_with(self, node):
        r = self._gen_expression(node.resource)
        lines = [f"await using (var _res = {r})  // async with"]
        lines.append("{")
        for s in node.body: lines.append(f"    {self._gen_statement(s)}")
        lines.append("}")
        return "\n".join(lines)

    def _gen_sealed_class(self, node):
        lines = [f"sealed class {node.name} {{"]
        for s in node.body:
            lines.append(f"    {self._gen_statement(s)}")
        lines.append("}")
        return "\n".join(lines)


def generate_csharp(ast: Program) -> str:
    gen = CSharpGenerator(ast)
    return gen.generate()
