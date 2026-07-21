"""
FusionBoa → Go Code Generator
"""

from ..parser.ast_nodes import *


class GoGenerator:
    def __init__(self, ast: Program):
        self.ast = ast
        self.indent_level = 0

    def _indent(self) -> str:
        return "\t" * self.indent_level

    def generate(self) -> str:
        lines = ['package main', '', 'import "fmt"', '', 'func main() {']
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
        if isinstance(node, ExpressionStatement): return self._indent() + self._gen_expression(node.expression)
        if isinstance(node, VariableDeclaration): return self._indent() + f"{node.name} := {self._gen_expression(node.value)}"
        if isinstance(node, ConstDeclaration): return self._indent() + f"const {node.name} = {self._gen_expression(node.value)}"
        if isinstance(node, Assignment): return self._indent() + f"{node.target} = {self._gen_expression(node.value)}"
        if isinstance(node, AugmentedAssignment): return self._indent() + f"{node.target} {node.operator}= {self._gen_expression(node.value)}"
        if isinstance(node, PrintStatement):
            v = self._gen_expression(node.expression) if node.expression else '""'
            return self._indent() + f"fmt.Println({v})"
        if isinstance(node, IfStatement): return self._gen_if(node)
        if isinstance(node, ForLoop): return self._gen_for(node)
        if isinstance(node, WhileLoop): return self._gen_while(node)
        if isinstance(node, RepeatLoop): return self._gen_repeat(node)
        if isinstance(node, FunctionDefinition): return self._gen_function(node)
        if isinstance(node, ReturnStatement):
            return self._indent() + (f"return {self._gen_expression(node.value)}" if node.value else "return")
        if isinstance(node, BreakStatement): return self._indent() + "break"
        if isinstance(node, ContinueStatement): return self._indent() + "continue"
        if isinstance(node, DoWhileLoop): return self._gen_do_while(node)
        if isinstance(node, EnumDefinition): return self._gen_enum(node)
        if isinstance(node, DeferStatement): return self._indent() + "// deferred"
        if isinstance(node, GuardStatement): return self._gen_guard_statement(node)
        if isinstance(node, DestructuringDeclaration): return self._gen_destructuring(node)
        if isinstance(node, IncrementExpression):
            return self._indent() + f"{node.target}++"
        if isinstance(node, DecrementExpression):
            return self._indent() + f"{node.target}--"
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
            return self._gen_statement(node.declaration) + "  // static"
        return self._indent() + f"// {type(node).__name__}"

    def _gen_expression(self, node: ASTNode) -> str:
        if node is None: return "nil"
        if isinstance(node, Literal):
            if node.value is None: return "nil"
            if node.value is True: return "true"
            if node.value is False: return "false"
            if isinstance(node.value, str): return repr(node.value)
            return str(node.value)
        if isinstance(node, Identifier): return node.name
        if isinstance(node, BinaryOp):
            op_map = {"and": "&&", "or": "||", "^": "", "==": "==", "!=": "!=",
                       "<": "<", ">": ">", "<=": "<=", ">=": ">=",
                       "&": "&", "|": "|", "<<": "<<", ">>": ">>", "//": "/",
                       "??": " /*??*/ ", "in": " /*in*/ ", "not in": " /*not in*/", "is": " /*is*/ "}
            op = op_map.get(node.operator, node.operator)
            l = self._gen_expression(node.left)
            r = self._gen_expression(node.right)
            # Null-coalescing: a ?? b -> (func() interface{} { v := a; if v != nil { return v }; return b })()
            if node.operator == "??":
                return f"(func() interface{{}} {{ v := {l}; if v != nil {{ return v }}; return {r} }})()"
            if not op: return f"math.Pow({l}, {r})"
            return f"({l} {op} {r})"
        if isinstance(node, UnaryOp):
            m = {"neg": "-", "not": "!", "~": "^"}
            return f"({m.get(node.operator, '')}{self._gen_expression(node.operand)})"
        if isinstance(node, Call):
            callee = self._gen_expression(node.callee)
            args = ", ".join(self._gen_expression(a) for a in node.arguments)
            if isinstance(node.callee, Identifier) and node.callee.name == "print":
                return f"fmt.Println({args})"
            return f"{callee}({args})"
        if isinstance(node, Attribute): return f"{self._gen_expression(node.object)}.{node.attribute}"
        if isinstance(node, Index): return f"{self._gen_expression(node.object)}[{self._gen_expression(node.index)}]"
        if isinstance(node, ListLiteral):
            el = ", ".join(self._gen_expression(e) for e in node.elements)
            return f"[]interface{{}}{{{el}}}"
        if isinstance(node, DictLiteral):
            pairs = ", ".join(f'"{self._gen_expression(k)}": {self._gen_expression(v)}' for k, v in node.pairs)
            return "map[string]interface{}{" + pairs + "}"
        if isinstance(node, Ternary):
            return f"(func() interface{{}} {{ if {self._gen_expression(node.condition)} {{ return {self._gen_expression(node.true_value)} }} else {{ return {self._gen_expression(node.false_value)} }} }})()"
        if isinstance(node, LengthExpression):
            return f"len(fmt.Sprint({self._gen_expression(node.expression)}))"
        if isinstance(node, InExpression): return f"__fusionboa_contains({self._gen_expression(node.right)}, {self._gen_expression(node.left)})"
        if isinstance(node, IsExpression): return f"(interface{{}}(nil) != {self._gen_expression(node.left)})"
        if isinstance(node, RangeLiteral): return f"__fusionboa_range({self._gen_expression(node.start)}, {self._gen_expression(node.end)})"
        if isinstance(node, DictComprehension): return f"/* dict comp */"
        if isinstance(node, MultiLineString): return f'"{node.value}"'
        if isinstance(node, SliceExpression): return f"/* slice */"
        if isinstance(node, GeneratorExpression): return self._gen_generator(node)
        if isinstance(node, IncrementExpression): return f"{node.target}++"
        if isinstance(node, DecrementExpression): return f"{node.target}--"
        return f"nil"

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
            lines.append(self._indent() + f"for _, {node.variable} := range {self._gen_expression(node.iterable)} {{")
        else:
            fv = self._gen_expression(node.range_from)
            tv = self._gen_expression(node.range_to)
            lines.append(self._indent() + f"for {node.variable} := {fv}; {node.variable} <= {tv}; {node.variable}++ {{")
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_while(self, node):
        lines = [self._indent() + f"for {self._gen_expression(node.condition)} {{"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_repeat(self, node):
        i = "_i"
        lines = [self._indent() + f"for {i} := 0; {i} < int({self._gen_expression(node.times)}); {i}++ {{"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_function(self, node):
        params = ", ".join(f"{p} interface{{}}" for p in node.parameters)
        lines = [self._indent() + f"func {node.name}({params}) {{"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)


    def _gen_do_while(self, node):
        lines = [self._indent() + "for {"]
        self.indent_level += 1
        for s in node.body: lines.append(self._gen_statement(s))
        lines.append(self._indent() + f"if !({self._gen_expression(node.condition)}) {{ break }}")
        self.indent_level -= 1
        lines.append(self._indent() + "}")
        return "\n".join(lines)

    def _gen_enum(self, node):
        lines = [self._indent() + f"const ("]
        for i, member in enumerate(node.members):
            if i == 0:
                lines.append(self._indent() + f"\t{node.name}_{member} = iota")
            else:
                lines.append(self._indent() + f"\t{node.name}_{member}")
        lines.append(self._indent() + ")")
        return "\n".join(lines)

    def _gen_destructuring(self, node):
        targets = ", ".join(node.targets)
        value = self._gen_expression(node.value)
        return self._indent() + f"{targets} := {value}"

    def _gen_generator(self, node):
        it = self._gen_expression(node.iterable)
        return f"/* generator: {node.variable} in {it} */"

    def _gen_augmented_assignment(self, node):
        val = self._gen_expression(node.value)
        target = node.target
        if node.operator == "||":
            return self._indent() + f"if !{target} {{ {target} = {val} }}"
        if node.operator == "&&":
            return self._indent() + f"if {target} {{ {target} = {val} }}"
        if node.operator == "??":
            return self._indent() + f"if {target} == nil {{ {target} = {val} }}"
        return self._indent() + f"{target} {node.operator}= {val}"


def generate_go(ast: Program) -> str:
    return GoGenerator(ast).generate()
