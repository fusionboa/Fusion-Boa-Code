"""
FusionBoa -> React (JSX) Code Generator

Converts FusionBoa-style components into React JSX.
Supports create element syntax for generating JSX markup.

Example Fusion React:
    // @target react
    define function App with props:
        create div class "app":
            create h1:
                text "Hello {props.name}!"
            create button onClick props.handleClick:
                text "Click me"
"""

from ..parser.ast_nodes import *


class ReactGenerator:
    def __init__(self, ast: Program):
        self.ast = ast
        self.indent_level = 0

    def _indent(self) -> str:
        return "  " * self.indent_level

    def generate(self) -> str:
        lines = []
        for stmt in self.ast.statements:
            lines.append(self._gen_statement(stmt))
        return '\n'.join(lines)

    def _gen_statement(self, node: ASTNode) -> str:
        if node is None:
            return ""
        if isinstance(node, FunctionDefinition):
            return self._gen_component(node)
        if isinstance(node, VariableDeclaration):
            return self._indent() + f"const {node.name} = {self._gen_expression(node.value)};"
        if isinstance(node, ConstDeclaration):
            return self._indent() + f"const {node.name} = {self._gen_expression(node.value)};"
        if isinstance(node, Assignment):
            return self._indent() + f"{node.target} = {self._gen_expression(node.value)};"
        if isinstance(node, AugmentedAssignment):
            return self._indent() + f"{node.target} {node.operator}= {self._gen_expression(node.value)};"
        if isinstance(node, ReturnStatement):
            if node.value:
                return self._gen_jsx_return(node.value)
            return self._indent() + "return null;"
        if isinstance(node, ExpressionStatement):
            return self._indent() + self._gen_expression(node.expression) + ";"
        if isinstance(node, DestructuringDeclaration):
            targets = "[" + ", ".join(node.targets) + "]" if node.destructure_type == "list" else "{" + ", ".join(node.targets) + "}"
            return self._indent() + f"const {targets} = {self._gen_expression(node.value)};"
        if isinstance(node, PrintStatement):
            v = self._gen_expression(node.expression) if node.expression else ""
            return self._indent() + f"console.log({v});"
        if isinstance(node, AugmentedAssignment):
            val = self._gen_expression(node.value)
            target = node.target
            if node.operator == "||": return self._indent() + f"{target} ||= {val};"
            if node.operator == "&&": return self._indent() + f"{target} &&= {val};"
            if node.operator == "??": return self._indent() + f"{target} ??= {val};"
            return self._indent() + f"{target} {node.operator}= {val};"
        if isinstance(node, IfStatement):
            lines = [self._indent() + f"if ({self._gen_expression(node.condition)}) {{"]
            self.indent_level += 1
            for s in node.body:
                lines.append(self._gen_statement(s))
            self.indent_level -= 1
            for cond, body in node.elif_branches:
                lines.append(self._indent() + f"}} else if ({self._gen_expression(cond)}) {{")
                self.indent_level += 1
                for s in body:
                    lines.append(self._gen_statement(s))
                self.indent_level -= 1
            if node.else_body:
                lines.append(self._indent() + "} else {")
                self.indent_level += 1
                for s in node.else_body:
                    lines.append(self._gen_statement(s))
                self.indent_level -= 1
            lines.append(self._indent() + "}")
            return '\n'.join(lines)
        if isinstance(node, IncrementExpression):
            return self._indent() + (f"++{node.target};" if node.prefix else f"{node.target}++;")
        if isinstance(node, DecrementExpression):
            return self._indent() + (f"--{node.target};" if node.prefix else f"{node.target}--;")
        if isinstance(node, WithStatement):
            r = self._gen_expression(node.resource)
            v = node.variable if node.variable else "_res"
            lines = [self._indent() + f"const {v} = {r};  // with", self._indent() + "try {"]
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
            return self._gen_statement(node.declaration).replace("const ", "static ")
        return self._indent() + f"// {type(node).__name__}"

    def _gen_expression(self, node: ASTNode) -> str:
        if node is None:
            return "null"
        if isinstance(node, Literal):
            if node.value is None:
                return "null"
            if isinstance(node.value, bool):
                return str(node.value).lower()
            if isinstance(node.value, str):
                return repr(node.value)
            return str(node.value)
        if isinstance(node, Identifier):
            return node.name
        if isinstance(node, BinaryOp):
            op_map = {"and": "&&", "or": "||", "==": "===", "!=": "!=="}
            op = op_map.get(node.operator, node.operator)
            return f"{self._gen_expression(node.left)} {op} {self._gen_expression(node.right)}"
        if isinstance(node, Call):
            callee = self._gen_expression(node.callee)
            args = ", ".join(self._gen_expression(a) for a in node.arguments)
            return f"{callee}({args})"
        if isinstance(node, Attribute):
            return f"{self._gen_expression(node.object)}.{node.attribute}"
        if isinstance(node, Index):
            return f"{self._gen_expression(node.object)}[{self._gen_expression(node.index)}]"
        if isinstance(node, ListLiteral):
            return "[" + ", ".join(self._gen_expression(e) for e in node.elements) + "]"
        if isinstance(node, DictLiteral):
            pairs = ", ".join(f"{self._gen_expression(k)}: {self._gen_expression(v)}" for k, v in node.pairs)
            return "{" + pairs + "}"
        if isinstance(node, StringInterpolation):
            parts = []
            for p in node.parts:
                if isinstance(p, Literal) and isinstance(p.value, str):
                    parts.append(p.value)
                else:
                    parts.append("${" + self._gen_expression(p) + "}")
            return "`" + "".join(parts) + "`"
        if isinstance(node, Ternary):
            return f"{self._gen_expression(node.condition)} ? {self._gen_expression(node.true_value)} : {self._gen_expression(node.false_value)}"
        if isinstance(node, RangeLiteral): return f"Array.from({{length: {self._gen_expression(node.end)} - {self._gen_expression(node.start)} + 1}}, (_, i) => i + {self._gen_expression(node.start)})"
        if isinstance(node, GeneratorExpression):
            expr = self._gen_expression(node.expression)
            it = self._gen_expression(node.iterable)
            cond = f".filter({node.variable} => {self._gen_expression(node.condition)})" if node.condition else ""
            return f"{it}.map({node.variable} => {expr}){cond}"
        if isinstance(node, IncrementExpression): return f"++{node.target}" if node.prefix else f"{node.target}++"
        if isinstance(node, DecrementExpression): return f"--{node.target}" if node.prefix else f"{node.target}--"
        return "null"

    def _gen_component(self, node: FunctionDefinition) -> str:
        """Generate a React functional component."""
        params = ", ".join(node.parameters) if node.parameters else "props"
        lines = [f"const {node.name} = ({params}) => {{"]
        self.indent_level += 1
        
        for stmt in node.body:
            lines.append(self._gen_statement(stmt))
        
        self.indent_level -= 1
        lines.append("};")
        lines.append("")
        lines.append(f"export default {node.name};")
        return '\n'.join(lines)

    def _gen_jsx_return(self, node: ASTNode) -> str:
        """Generate a JSX return statement from an expression."""
        jsx = self._gen_jsx_value(node)
        if jsx is None:
            return self._indent() + f"return {self._gen_expression(node)};"
        
        lines = [self._indent() + "return ("]
        self.indent_level += 1
        lines.append(self._indent() + jsx)
        self.indent_level -= 1
        lines.append(self._indent() + ");")
        return '\n'.join(lines)

    def _gen_jsx_value(self, node: ASTNode) -> str:
        """Convert an AST node to JSX. Returns None if it can't be JSX."""
        if node is None:
            return "null"
        
        # Check for create calls: create div class "foo": children
        if isinstance(node, Call):
            if isinstance(node.callee, Identifier) and node.callee.name == "create":
                return self._gen_jsx_create(node)
            if isinstance(node.callee, Identifier):
                name = node.callee.name
                if name[0].isupper() or name in self._html_tags():
                    return self._gen_jsx_element_tag(node.callee.name, node.arguments)
            return None
        
        if isinstance(node, Ternary):
            c = self._gen_jsx_value(node.condition)
            t = self._gen_jsx_value(node.true_value)
            f = self._gen_jsx_value(node.false_value)
            if c and t and f:
                return f"{{{c} ? {t} : {f}}}"
            return None
        
        if isinstance(node, Literal) and isinstance(node.value, str):
            return node.value
        
        return None

    def _html_tags(self) -> set:
        return {
            "div", "span", "p", "h1", "h2", "h3", "h4", "h5", "h6",
            "a", "button", "input", "img", "form", "label", "select",
            "option", "textarea", "ul", "ol", "li", "table", "tr",
            "td", "th", "thead", "tbody", "header", "footer", "nav",
            "main", "section", "article", "aside", "figure", "figcaption",
            "blockquote", "pre", "code", "em", "strong", "i", "b",
            "br", "hr", "link", "meta", "title", "head", "body",
            "html", "style", "script", "canvas", "svg", "video",
            "audio", "source", "iframe", "details", "summary",
            "dialog", "slot", "template",
        }

    def _gen_jsx_create(self, node: Call) -> str:
        """Generate JSX from a create call: create tagname attr1 val1 ... children"""
        args = node.arguments
        if not args:
            return "<div />"
        
        # First argument should be the tag name (string literal)
        tag = "div"
        attr_start = 0
        if isinstance(args[0], Literal) and isinstance(args[0].value, str):
            tag = args[0].value.lower()
            attr_start = 1
        
        # Parse attributes and children from remaining args
        attrs = {}
        children = []
        i = attr_start
        while i < len(args):
            if isinstance(args[i], KeywordArgument):
                attr_name = args[i].name
                attr_val = self._gen_expression(args[i].value)
                # Convert Fusion attribute names to React props
                react_attr = self._fusionboa_to_react_attr(attr_name)
                if react_attr:
                    attrs[react_attr] = attr_val
                i += 1
            else:
                # Check if this is a block child (nested elements)
                child_jsx = self._gen_jsx_value(args[i])
                if child_jsx:
                    children.append(child_jsx)
                else:
                    expr = self._gen_expression(args[i])
                    if expr:
                        children.append("{" + expr + "}")
                i += 1
        
        # Build attribute string
        attr_parts = []
        for k, v in attrs.items():
            if v.startswith('"') or v.startswith("'"):
                # String literal attribute
                attr_parts.append(f'{k}={v}')
            else:
                # Expression attribute
                attr_parts.append(f'{k}={{{v}}}')
        attr_str = ' ' + ' '.join(attr_parts) if attr_parts else ''
        
        # Build children
        if not children:
            if tag in self._void_elements():
                return f'<{tag}{attr_str} />'
            return f'<{tag}{attr_str} />'
        
        child_str = '\n'.join(children)
        return f'<{tag}{attr_str}>\n{child_str}\n</{tag}>'

    def _gen_jsx_element_tag(self, tag: str, args: list) -> str:
        """Generate JSX for a direct tag call like div(class='foo'): children."""
        attrs = {}
        children = []
        
        for arg in args:
            if isinstance(arg, KeywordArgument):
                attr_name = self._fusionboa_to_react_attr(arg.name)
                if attr_name:
                    attrs[attr_name] = self._gen_expression(arg.value)
            else:
                child = self._gen_jsx_value(arg) or self._gen_expression(arg)
                children.append(child)
        
        attr_parts = []
        for k, v in attrs.items():
            if v.startswith('"') or v.startswith("'"):
                attr_parts.append(f'{k}={v}')
            else:
                attr_parts.append(f'{k}={{{v}}}')
        attr_str = ' ' + ' '.join(attr_parts) if attr_parts else ''
        
        if not children:
            return f'<{tag}{attr_str} />'
        
        child_str = '\n'.join(children)
        return f'<{tag}{attr_str}>\n{child_str}\n</{tag}>'

    def _fusionboa_to_react_attr(self, attr: str) -> str:
        """Convert FusionBoa-style attribute name to React prop.
        
        Examples:
            class -> className
            onclick -> onClick
            onchange -> onChange
            for -> htmlFor
            tabindex -> tabIndex
            background-color -> backgroundColor
        """
        mapping = {
            "class": "className",
            "for": "htmlFor",
            "tabindex": "tabIndex",
            "readonly": "readOnly",
            "maxlength": "maxLength",
            "autocomplete": "autoComplete",
            "autofocus": "autoFocus",
            "enctype": "encType",
            "formaction": "formAction",
            "formenctype": "formEncType",
            "formmethod": "formMethod",
            "formnovalidate": "formNoValidate",
            "formtarget": "formTarget",
            "hreflang": "hrefLang",
            "inputmode": "inputMode",
            "ismap": "isMap",
            "usemap": "useMap",
        }
        
        if attr in mapping:
            return mapping[attr]
        
        # Convert event handlers: onclick -> onClick
        if attr.startswith('on') and len(attr) > 2:
            return 'on' + attr[2].upper() + attr[3:]
        
        # Convert kebab-case to camelCase: background-color -> backgroundColor
        parts = attr.split('-')
        if len(parts) > 1:
            return parts[0] + ''.join(p.capitalize() for p in parts[1:])
        
        return attr

    def _void_elements(self) -> set:
        return {"br", "hr", "img", "input", "link", "meta", "area", "base",
                "col", "embed", "param", "source", "track", "wbr"}


def generate_react(ast: Program) -> str:
    gen = ReactGenerator(ast)
    return gen.generate()
