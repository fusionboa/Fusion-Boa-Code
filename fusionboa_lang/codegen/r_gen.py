"""
FusionBoa → R Code Generator

Translates a FusionBoa AST into equivalent R source code.
Supports all Fusion features.
"""

from ..parser.ast_nodes import *


class RGenerator:
    """Generates R code from a FusionBoa AST."""

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
            YieldStatement: lambda n: self._indent() + f"# yield not supported: {self._gen_expression(n.value)}",
            BreakStatement: lambda n: self._indent() + "break",
            ContinueStatement: lambda n: self._indent() + "next",
            PassStatement: lambda n: self._indent() + "# pass",
            ImportStatement: self._gen_import_statement,
            ExportStatement: self._gen_export_statement,
            TryStatement: self._gen_try_statement,
            PrintStatement: self._gen_print_statement,
            InputStatement: self._gen_input_statement,
            DoWhileLoop: self._gen_do_while_loop,
            EnumDefinition: self._gen_enum_definition,
            DeferStatement: lambda n: self._indent() + "# deferred",
            GuardStatement: self._gen_guard_statement,
            DestructuringDeclaration: self._gen_destructuring,
            IncrementExpression: lambda n: self._indent() + f"{n.target} <- {n.target} + 1",
            DecrementExpression: lambda n: self._indent() + f"{n.target} <- {n.target} - 1",
            WithStatement: self._gen_with_statement,
            DecoratorStatement: lambda n: self._indent() + f"# @{n.name}",
            StaticMethodDeclaration: lambda n: self._gen_statement(n.declaration).replace(" <- function", " <- function  # static", 1),
            # v0.5.0 Masterpiece
            RecordDefinition: self._gen_record_definition,
            PropertyDefinition: self._gen_property_definition,
            ExtensionDefinition: self._gen_extension_definition,
            # v0.9.1+ Universal Polyglot
            SetLiteral: self._gen_set_stmt,
            TupleLiteral: lambda n: self._indent() + f"list({', '.join(str(e) for e in n.elements)})" if n.elements else self._indent() + "list()",
            MultiReturnStatement: self._gen_multi_return,
            YieldFromStatement: lambda n: self._indent() + f"# yield from: {self._gen_expression(n.iterable)}",
            GoStatement: lambda n: self._indent() + f"# goroutine: {n.name or 'anonymous'} (use future::future)",
            ChannelDeclaration: lambda n: self._indent() + f"# channel: {n.name}",
            ChannelSelect: lambda n: self._indent() + f"# select {len(n.cases)} channels",
            ChannelClose: lambda n: self._indent() + f"# channel close",
            SynchronizedBlock: lambda n: self._indent() + f"# synchronized",
            AsyncWithStatement: lambda n: self._indent() + f"# async with",
            ModuleDefinition: lambda n: self._indent() + f"# module {n.name}",
            MixinStatement: lambda n: self._indent() + f"# {n.mixin_type} {n.mixin_name}",
            ObjectDefinition: lambda n: self._indent() + f"# object {n.name} (singleton)",
            ActorDefinition: lambda n: self._indent() + f"# actor {n.name}",
            SealedClassDefinition: lambda n: self._indent() + f"# sealed class {n.name}",
            NewExpression: lambda n: self._indent() + f"# new {n.type_name}",
            DeleteExpression: lambda n: self._indent() + f"# delete {n.target} (GC handles)",
            GlobalStatement: lambda n: self._indent() + f"# global {', '.join(n.names)}",
            AtomicCounter: lambda n: self._indent() + f"{n.name} <- 0L  # atomic",
            FormulaExpression: self._gen_formula_stmt,
            VectorizeExpression: self._gen_vectorize_stmt,
        }
        gen_func = gen_map.get(type(node))
        if gen_func: return gen_func(node)
        return f"# Unknown: {type(node).__name__}"

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
        if isinstance(node, LengthExpression): return f"length({self._gen_expression(node.expression)})"
        if isinstance(node, AwaitExpression): return f"# await {self._gen_expression(node.expression)}"
        if isinstance(node, ListComprehension): return self._gen_list_comprehension(node)
        if isinstance(node, StringInterpolation): return self._gen_string_interpolation(node)
        if isinstance(node, SpreadElement): return f"# spread {self._gen_expression(node.expression)}"
        if isinstance(node, KeywordArgument): return f"{node.name} = {self._gen_expression(node.value)}"
        if isinstance(node, RangeLiteral):
            return f"seq({self._gen_expression(node.start)}, {self._gen_expression(node.end)})"
        if isinstance(node, InExpression): return f"({self._gen_expression(node.left)} %in% {self._gen_expression(node.right)})"
        if isinstance(node, IsExpression): return f"inherits({self._gen_expression(node.left)}, {self._gen_expression(node.right)})"
        if isinstance(node, DictComprehension): return f"# dict comp"
        if isinstance(node, MultiLineString): return self._gen_literal(Literal(node.value))
        if isinstance(node, SliceExpression): return f"# slice"
        if isinstance(node, GeneratorExpression): return f"# generator: {node.variable}"
        if isinstance(node, IncrementExpression): return f"{node.target} <- {node.target} + 1"
        if isinstance(node, DecrementExpression): return f"{node.target} <- {node.target} - 1"
        # v0.9.1+ Expression nodes
        if isinstance(node, SetLiteral):
            el = ", ".join(self._gen_expression(e) for e in node.elements)
            return f"unique(c({el}))"
        if isinstance(node, TupleLiteral):
            el = ", ".join(self._gen_expression(e) for e in node.elements)
            return f"list({el})"
        if isinstance(node, SymbolLiteral): return f"/* :{node.name} */"
        if isinstance(node, BlockExpression): return f"/* block */"
        if isinstance(node, JsxElement): return f"/* JSX:{node.tag} */"
        if isinstance(node, HookCall): return f"/* {node.hook_name}() */"
        if isinstance(node, NewExpression): return f"/* new */"
        if isinstance(node, DeleteExpression): return f"/* delete {node.target} */"
        if isinstance(node, BroadcastExpression): return f"/* broadcast */"
        if isinstance(node, VectorizeExpression):
            op = self._gen_expression(node.operation)
            col = self._gen_expression(node.collection) if node.collection else ""
            return f"Vectorize({op})({col})" if col else f"Vectorize({op})"
        if isinstance(node, FormulaExpression):
            resp = self._gen_expression(node.response)
            preds = " + ".join(self._gen_expression(p) for p in node.predictors)
            return f"{resp} ~ {preds}"
        if isinstance(node, KeyOfExpression): return f"/* keyof {node.target_type} */"
        if isinstance(node, TemplateLiteral): return f"/* template literal */"
        if isinstance(node, YieldToBlock): return f"/* yield to block */"
        return f"# Unknown: {type(node).__name__}"

    def _gen_literal(self, node: Literal) -> str:
        if node.value is None: return "NULL"
        if node.value is True: return "TRUE"
        if node.value is False: return "FALSE"
        if isinstance(node.value, str):
            return '"' + node.value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'
        return str(node.value)

    def _gen_binary_op(self, node: BinaryOp) -> str:
        op_map = {"and": "&", "or": "|", "^": "^",
                  "==": "==", "!=": "!=", "<": "<", ">": ">",
                  "<=": "<=", ">=": ">=", "+": "+", "-": "-",
                  "*": "*", "/": "/", "&": "bitwAnd", "|": "bitwOr", "<<": "bitwShiftL", ">>": "bitwShiftR"}
        r_op = op_map.get(node.operator, node.operator)
        left = self._gen_expression(node.left)
        right = self._gen_expression(node.right)
        # Null-coalescing: a ?? b -> if (is.null(a)) b else a
        if node.operator == "??":
            return f"ifelse(is.null({left}), {right}, {left})"
        if node.operator == "%":
            return f"({left} %% {right})"
        return f"({left} {r_op} {right})"

    def _gen_unary_op(self, node: UnaryOp) -> str:
        op_map = {"neg": "-", "not": "!", "~": "bitwNot"}
        r_op = op_map.get(node.operator, node.operator)
        operand = self._gen_expression(node.operand)
        return f"({r_op}{operand})"

    def _gen_call(self, node: Call) -> str:
        callee = self._gen_expression(node.callee)
        args = ", ".join(self._gen_expression(a) for a in node.arguments)
        if isinstance(node.callee, Identifier):
            if node.callee.name == "print":
                return f"print({args})"
            if node.callee.name == "input":
                return f"readline({args})"
            if node.callee.name == "str":
                return f"as.character({args})"
        return f"{callee}({args})"

    def _gen_attribute(self, node: Attribute) -> str:
        return f"{self._gen_expression(node.object)}${node.attribute}"

    def _gen_index(self, node: Index) -> str:
        # R uses 1-based indexing
        idx = self._gen_expression(node.index)
        return f"{self._gen_expression(node.object)}[{idx}]"

    def _gen_list_literal(self, node: ListLiteral) -> str:
        elements = ", ".join(self._gen_expression(e) for e in node.elements)
        return f"c({elements})"

    def _gen_dict_literal(self, node: DictLiteral) -> str:
        keys = ", ".join(self._gen_expression(k) for k, v in node.pairs)
        values = ", ".join(self._gen_expression(v) for k, v in node.pairs)
        return f"list({keys})" if not node.pairs else f"setNames(list({values}), c({keys}))"

    def _gen_lambda(self, node: Lambda) -> str:
        params = ", ".join(node.parameters)
        body = self._gen_expression(node.body)
        return f"function({params}) {body}"

    def _gen_ternary(self, node: Ternary) -> str:
        return f"ifelse({self._gen_expression(node.condition)}, {self._gen_expression(node.true_value)}, {self._gen_expression(node.false_value)})"

    def _gen_list_comprehension(self, node: ListComprehension) -> str:
        expr = self._gen_expression(node.expression)
        iterable = self._gen_expression(node.iterable)
        if node.condition:
            cond = self._gen_expression(node.condition)
            return f"sapply({iterable}, function({node.variable}) if ({cond}) {expr} else NA)"
        return f"sapply({iterable}, function({node.variable}) {expr})"

    def _gen_string_interpolation(self, node: StringInterpolation) -> str:
        parts = []
        for p in node.parts:
            if isinstance(p, Literal) and isinstance(p.value, str):
                parts.append(p.value)
            else:
                parts.append("{" + self._gen_expression(p) + "}")
        return f'paste0({", ".join(repr(part) if isinstance(part, str) else part for part in parts)})'

    def _gen_expression_statement(self, node: ExpressionStatement) -> str:
        return self._indent() + self._gen_expression(node.expression)

    def _gen_variable_declaration(self, node: VariableDeclaration) -> str:
        return self._indent() + f"{node.name} <- {self._gen_expression(node.value)}"

    def _gen_const_declaration(self, node: ConstDeclaration) -> str:
        return self._indent() + f"{node.name} <- {self._gen_expression(node.value)}  # const"

    def _gen_assignment(self, node: Assignment) -> str:
        return self._indent() + f"{node.target} <- {self._gen_expression(node.value)}"

    def _gen_augmented_assignment(self, node: AugmentedAssignment) -> str:
        val = self._gen_expression(node.value)
        target = node.target
        if node.operator == "||": return self._indent() + f"{target} <- {target} || {val}"
        if node.operator == "&&": return self._indent() + f"{target} <- {target} && {val}"
        if node.operator == "??": return self._indent() + f"{target} <- if (is.null({target})) {val} else {target}"
        return self._indent() + f"{target} <- {target} {node.operator} {val}"

    def _gen_if_statement(self, node: IfStatement) -> str:
        lines = [self._indent() + f"if ({self._gen_expression(node.condition)}) {{"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        for elif_cond, elif_body in node.elif_branches:
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
        lines = [self._indent() + f"__match_val <- {self._gen_expression(node.expression)}"]
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
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_for_loop(self, node: ForLoop) -> str:
        lines = []
        if node.iterable:
            lines.append(self._indent() + f"for ({node.variable} in {self._gen_expression(node.iterable)}) {{")
        else:
            from_v = self._gen_expression(node.range_from)
            to_v = self._gen_expression(node.range_to)
            lines.append(self._indent() + f"for ({node.variable} in {from_v}:{to_v}) {{")
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_repeat_loop(self, node: RepeatLoop) -> str:
        lines = [self._indent() + f"for (__fusionboa_i in 1:{self._gen_expression(node.times)}) {{"]
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
            params.append("...")
        param_strs = []
        for p in params:
            if p in node.defaults:
                param_strs.append(f"{p} = {self._gen_expression(node.defaults[p])}")
            else:
                param_strs.append(p)
        lines.append(self._indent() + f"{node.name} <- function({', '.join(param_strs)}) {{")
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_class_definition(self, node: ClassDefinition) -> str:
        lines = [self._indent() + f"# R class: {node.name} (using R6 or S3)"]
        lines.append(self._indent() + f"# R doesn't natively support classes like Fusion. Use R6 package or S3.")
        lines.append(self._indent() + f"{node.name} <- list()")
        if node.parent:
            lines.append(self._indent() + f"# inherits from: {node.parent}")
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                stmt_name = stmt.name if stmt.name != "init" else "initialize"
                # Avoid mutating the original AST node
                saved_name = stmt.name
                stmt.name = stmt_name
                lines.append(self._gen_function_definition(stmt))
                stmt.name = saved_name
                lines.append(self._indent() + f"{node.name}${stmt_name} <- {stmt_name}")
        return "\n".join(lines)

    def _gen_return_statement(self, node: ReturnStatement) -> str:
        if node.value:
            return self._indent() + f"return({self._gen_expression(node.value)})"
        return self._indent() + "return(invisible(NULL))"

    def _gen_import_statement(self, node: ImportStatement) -> str:
        if node.items:
            items_str = ", ".join(node.items)
            return self._indent() + f"library({node.module})  # import {items_str}"
        return self._indent() + f"library({node.module})"

    def _gen_export_statement(self, node: ExportStatement) -> str:
        return self._gen_statement(node.declaration) + "  # export"

    def _gen_try_statement(self, node: TryStatement) -> str:
        lines = [self._indent() + "tryCatch({"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        self.indent_level -= 1
        if node.catch_body:
            lines.append(self._indent() + f"}}, error = function({node.catch_var or 'e'}) {{")
            self.indent_level += 1
            for stmt in node.catch_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        if node.finally_body:
            lines.append(self._indent() + "}, finally = {")
            self.indent_level += 1
            for stmt in node.finally_body: lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
        lines.append(self._indent() + "})")
        return "\n".join(lines)

    def _gen_print_statement(self, node: PrintStatement) -> str:
        if node.expression:
            return self._indent() + f"print({self._gen_expression(node.expression)})"
        return self._indent() + "print()"

    def _gen_input_statement(self, node: InputStatement) -> str:
        if node.target:
            if node.prompt:
                return self._indent() + f'{node.target} <- readline(prompt = {self._gen_literal(Literal(value=node.prompt))})'
            return self._indent() + f"{node.target} <- readline()"
        return self._indent() + "readline()"

    def _gen_guard_statement(self, node):
        cond = self._gen_expression(node.condition)
        lines = [self._indent() + f"if (!({cond})) {{"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        lines.append(self._indent() + "return(invisible(NULL))")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_do_while_loop(self, node):
        lines = [self._indent() + "repeat {"]
        self.indent_level += 1
        for stmt in node.body: lines.append(self._gen_statement(stmt))
        lines.append(self._indent() + f"if (!({self._gen_expression(node.condition)})) break")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_enum_definition(self, node):
        lines = [self._indent() + f"# enum {node.name}"]
        for i, member in enumerate(node.members):
            lines.append(self._indent() + f"{node.name}_{member} <- {i}")
        return "\n".join(lines)

    def _gen_with_statement(self, node):
        r = self._gen_expression(node.resource)
        v = node.variable if node.variable else "_res"
        lines = [self._indent() + f"{v} <- {r}  # with"]
        for s in node.body: lines.append(self._gen_statement(s))
        return "\n".join(lines)

    def _gen_destructuring(self, node):
        targets = ", ".join(node.targets)
        value = self._gen_expression(node.value)
        return self._indent() + f"{targets} <- {value}"

    # ---- v0.5.0 Masterpiece Codegen ----

    def _gen_record_definition(self, node: RecordDefinition) -> str:
        """define record -> R list with class attribute"""
        lines = [self._indent() + f"# Record: {node.name}"]
        lines.append(self._indent() + f"{node.name} <- function({', '.join(fname + ' = NULL' for fname, _, _ in node.fields)}) {{")
        self.indent_level += 1
        for fname, _, fdefault in node.fields:
            if fdefault is not None:
                lines.append(self._indent() + f"if (missing({fname})) {fname} <- {self._gen_expression(fdefault)}")
        lines.append(self._indent() + f"obj <- list({', '.join(fname + ' = ' + fname for fname, _, _ in node.fields)})")
        lines.append(self._indent() + f"class(obj) <- '{node.name}'")
        lines.append(self._indent() + "return(obj)")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_property_definition(self, node: PropertyDefinition) -> str:
        """define property -> R active binding (makeActiveBinding)"""
        lines = [self._indent() + f"# Property: {node.name}"]
        if node.getter_body:
            lines.append(self._indent() + f"get_{node.name} <- function(self) {{")
            self.indent_level += 1
            for stmt in node.getter_body:
                lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
            lines.append(self._indent() + "}")
        if node.setter_body:
            lines.append(self._indent() + f"set_{node.name} <- function(self, {node.setter_param}) {{")
            self.indent_level += 1
            for stmt in node.setter_body:
                lines.append(self._gen_statement(stmt))
            self.indent_level -= 1
            lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_extension_definition(self, node: ExtensionDefinition) -> str:
        """define extension on Type -> R S3 generic method"""
        lines = [self._indent() + f"# Extension methods for {node.target_type}"]
        for stmt in node.body:
            if isinstance(stmt, FunctionDefinition):
                params = ", ".join(stmt.parameters) if stmt.parameters else ""
                lines.append(self._indent() + f"{stmt.name}.{node.target_type} <- function({params})" if params else self._indent() + f"{stmt.name}.{node.target_type} <- function()")
                self.indent_level += 1
                for s in stmt.body:
                    lines.append(self._gen_statement(s))
                self.indent_level -= 1
                lines.append(self._indent() + "}")
        return "\n".join(lines)


    # ---- v0.9.1+ Handler Methods ----

    def _gen_set_stmt(self, node):
        el = ", ".join(str(e) for e in node.elements)
        return self._indent() + f"unique(c({el}))  # set"

    def _gen_multi_return(self, node):
        vals = ", ".join(self._gen_expression(v) for v in node.values)
        return self._indent() + f"return(list({vals}))"

    def _gen_formula_stmt(self, node):
        resp = self._gen_expression(node.response)
        preds = " + ".join(self._gen_expression(p) for p in node.predictors)
        return self._indent() + f"{resp} ~ {preds}"

    def _gen_vectorize_stmt(self, node):
        op = self._gen_expression(node.operation)
        col = self._gen_expression(node.collection) if node.collection else ""
        return self._indent() + f"Vectorize({op})({col})" if col else self._indent() + f"Vectorize({op})"


def generate_r(ast: Program) -> str:
    gen = RGenerator(ast)
    return gen.generate()
