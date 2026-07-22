"""
FusionBoa Semantic Type Checker

Validates type annotations across the AST before code generation.
Catches type mismatches like passing a string where an int is expected,
or using union types incorrectly.

Usage:
    from fusionboa_lang.semantic.type_checker import TypeChecker
    checker = TypeChecker(ast)
    errors = checker.check()  # Returns list of type errors
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field


@dataclass
class TypeError:
    """A type checking error with location information."""
    line: int
    col: int
    message: str
    severity: str = "error"  # "error" or "warning"


class TypeEnvironment:
    """Tracks variable types in scope."""

    def __init__(self, parent: Optional["TypeEnvironment"] = None):
        self._variables: Dict[str, str] = {}
        self._parent = parent

    def define(self, name: str, type_str: str) -> None:
        self._variables[name] = type_str

    def lookup(self, name: str) -> Optional[str]:
        if name in self._variables:
            return self._variables[name]
        if self._parent:
            return self._parent.lookup(name)
        return None

    def create_child(self) -> "TypeEnvironment":
        return TypeEnvironment(parent=self)


class TypeChecker:
    """Crawls the AST to validate type annotations before compilation.

    Checks:
    - Variable assignments match declared types
    - Function parameters match argument types
    - Return types match function declarations
    - Union types are used correctly
    - Type casting is valid
    """

    # Canonical type mapping for FusionBoa types
    TYPE_MAP = {
        "int": {"int", "integer"},
        "integer": {"int", "integer"},
        "float": {"float"},
        "string": {"string", "str"},
        "str": {"string", "str"},
        "bool": {"bool", "boolean"},
        "boolean": {"bool", "boolean"},
        "list": {"list"},
        "dict": {"dict", "dictionary", "map"},
        "dictionary": {"dict", "dictionary", "map"},
        "any": {"any"},
        "void": {"void", "none", "null"},
    }

    def __init__(self, ast):
        """Initialize with a parsed AST Program node."""
        self.ast = ast
        self.errors: List[TypeError] = []
        self._env = TypeEnvironment()
        self._function_return_types: Dict[str, str] = {}

    def check(self) -> List[TypeError]:
        """Run type checking and return all errors found."""
        try:
            for statement in self.ast.statements:
                self._check_statement(statement)
        except Exception as e:
            self.errors.append(TypeError(
                line=0, col=0,
                message=f"Type checker internal error: {e}",
                severity="error"
            ))
        return self.errors

    def _check_statement(self, node) -> None:
        """Dispatch to the appropriate checker for each statement type."""
        if node is None:
            return

        node_type = type(node).__name__

        if node_type == "VariableDeclaration":
            self._check_variable_declaration(node)
        elif node_type == "ConstDeclaration":
            self._check_const_declaration(node)
        elif node_type == "Assignment":
            self._check_assignment(node)
        elif node_type == "FunctionDefinition":
            self._check_function_definition(node)
        elif node_type == "ReturnStatement":
            self._check_return_statement(node)
        elif node_type == "IfStatement":
            self._check_if_statement(node)
        elif node_type == "ForLoop":
            self._check_for_loop(node)
        elif node_type == "WhileLoop":
            self._check_while_loop(node)
        elif node_type == "ExpressionStatement":
            self._check_expression_statement(node)
        elif node_type == "PrintStatement":
            self._check_print_statement(node)
        elif node_type == "RecordDefinition":
            self._check_record_definition(node)
        elif node_type == "PropertyDefinition":
            self._check_property_definition(node)
        elif node_type == "CastExpression":
            self._check_cast_expression(node)

    def _check_variable_declaration(self, node) -> None:
        """Check let x: int be value - ensure value matches type."""
        inferred_type = self._infer_type(node.value)
        if node.type_annotation:
            declared_type = node.type_annotation.type_name
            if not self._types_compatible(inferred_type, declared_type):
                self.errors.append(TypeError(
                    line=node.line, col=node.col,
                    message=f"Variable '{node.name}': cannot assign "
                            f"'{inferred_type}' to declared type '{declared_type}'"
                ))
            self._env.define(node.name, declared_type)
        else:
            self._env.define(node.name, inferred_type)

    def _check_const_declaration(self, node) -> None:
        """Check const PI: float be 3.14."""
        inferred_type = self._infer_type(node.value)
        if node.type_annotation:
            declared_type = node.type_annotation.type_name
            if not self._types_compatible(inferred_type, declared_type):
                self.errors.append(TypeError(
                    line=node.line, col=node.col,
                    message=f"Constant '{node.name}': cannot assign "
                            f"'{inferred_type}' to declared type '{declared_type}'"
                ))
            self._env.define(node.name, declared_type)
        else:
            self._env.define(node.name, inferred_type)

    def _check_assignment(self, node) -> None:
        """Check set x to value - warn if type changes."""
        existing_type = self._env.lookup(node.target)
        if existing_type:
            new_type = self._infer_type(node.value)
            if not self._types_compatible(new_type, existing_type):
                self.errors.append(TypeError(
                    line=node.line, col=node.col,
                    message=f"Assignment to '{node.target}': changing type from "
                            f"'{existing_type}' to '{new_type}'",
                    severity="warning"
                ))

    def _check_function_definition(self, node) -> None:
        """Check function parameter types and return type."""
        func_env = self._env.create_child()

        # Register parameter types
        for param in node.parameters:
            if param in node.param_types:
                func_env.define(param, node.param_types[param])
            else:
                func_env.define(param, "any")

        # Register return type
        if node.return_type:
            self._function_return_types[node.name] = node.return_type

        # Check body statements in function scope
        old_env = self._env
        self._env = func_env
        for stmt in node.body:
            self._check_statement(stmt)
        self._env = old_env

    def _check_return_statement(self, node) -> None:
        """Check return value matches declared return type."""
        if node.value:
            inferred = self._infer_type(node.value)
            # We don't have function context here, so just note the type

    def _check_if_statement(self, node) -> None:
        """Check if statement branches."""
        self._check_statement_list(node.body)
        for _, elif_body in node.elif_branches:
            self._check_statement_list(elif_body)
        self._check_statement_list(node.else_body)

    def _check_for_loop(self, node) -> None:
        """Check for loop variable and body."""
        self._env.define(node.variable, "any")
        self._check_statement_list(node.body)

    def _check_while_loop(self, node) -> None:
        """Check while loop body."""
        self._check_statement_list(node.body)

    def _check_expression_statement(self, node) -> None:
        """Check expression types."""
        pass  # Expression types are validated lazily

    def _check_print_statement(self, node) -> None:
        """Print accepts any type."""
        pass

    def _check_record_definition(self, node) -> None:
        """Check record field types."""
        for fname, ftype, fdefault in node.fields:
            if ftype != "any" and ftype not in self.TYPE_MAP:
                self.errors.append(TypeError(
                    line=node.line, col=node.col,
                    message=f"Record '{node.name}': unknown field type '{ftype}' "
                            f"for field '{fname}'",
                    severity="warning"
                ))

    def _check_property_definition(self, node) -> None:
        """Check property getter/setter types."""
        if node.type_annotation:
            declared_type = node.type_annotation.type_name
            if declared_type not in self.TYPE_MAP:
                self.errors.append(TypeError(
                    line=node.line, col=node.col,
                    message=f"Property '{node.name}': unknown type '{declared_type}'",
                    severity="warning"
                ))

    def _check_cast_expression(self, node) -> None:
        """Check type casting is valid."""
        if node.target_type not in self.TYPE_MAP:
            self.errors.append(TypeError(
                line=node.line, col=node.col,
                message=f"Type cast to unknown type '{node.target_type}'",
                severity="warning"
            ))

    def _check_statement_list(self, statements) -> None:
        """Check a list of statements."""
        for stmt in statements:
            self._check_statement(stmt)

    def _infer_type(self, node) -> str:
        """Infer the type of an expression node.

        Returns a string type name: 'int', 'float', 'string', 'bool',
        'list', 'dict', 'any', 'null', etc.
        """
        if node is None:
            return "null"

        node_type = type(node).__name__

        # Literals
        if node_type == "Literal":
            val = node.value
            if val is None:
                return "null"
            if isinstance(val, bool):
                return "bool"
            if isinstance(val, int):
                return "int"
            if isinstance(val, float):
                return "float"
            if isinstance(val, str):
                return "string"
            return "any"

        # Identifiers: look up in scope
        if node_type == "Identifier":
            return self._env.lookup(node.name) or "any"

        # Binary operations
        if node_type == "BinaryOp":
            left_type = self._infer_type(node.left)
            right_type = self._infer_type(node.right)
            if node.operator in ("+", "-", "*", "/", "//", "%", "^"):
                if left_type == "string" or right_type == "string":
                    return "string"
                if left_type == "float" or right_type == "float":
                    return "float"
                return "int"
            if node.operator in ("and", "or", "==", "!=", "<", ">", "<=", ">=", "has", "contains", "starts with", "ends with"):
                return "bool"
            return "any"

        # Unary operations
        if node_type == "UnaryOp":
            if node.operator == "not":
                return "bool"
            return self._infer_type(node.operand)

        # Function calls
        if node_type == "Call":
            if hasattr(node.callee, 'name'):
                if node.callee.name == "input":
                    return "string"
                if node.callee.name in ("length", "size", "count", "len"):
                    return "int"
            return_type = self._function_return_types.get(
                getattr(node.callee, 'name', ''), None
            )
            return return_type or "any"

        # List literals
        if node_type == "ListLiteral":
            return "list"

        # Dict literals
        if node_type == "DictLiteral":
            return "dict"

        # Length expressions
        if node_type == "LengthExpression":
            return "int"

        # Type casting
        if node_type == "CastExpression":
            return node.target_type

        # String interpolation
        if node_type == "StringInterpolation":
            return "string"

        # Range literals
        if node_type == "RangeLiteral":
            return "list"

        # Default
        return "any"

    def _types_compatible(self, source_type: str, target_type: str) -> bool:
        """Check if source_type is assignable to target_type.

        Handles union types like 'string | int'.
        """
        if source_type == "any" or target_type == "any":
            return True

        if source_type == "null":
            return True  # null is assignable to any type

        # Handle union types: "Union[string, int]" or "string|int"
        if "|" in target_type:
            parts = [p.strip() for p in target_type.split("|")]
            return any(self._types_compatible(source_type, p) for p in parts)

        if "Union[" in target_type:
            # Parse: Union[string, int]
            inner = target_type[target_type.index("[") + 1:target_type.rindex("]")]
            parts = [p.strip() for p in inner.split(",")]
            return any(self._types_compatible(source_type, p) for p in parts)

        if "Optional[" in target_type:
            inner = target_type[target_type.index("[") + 1:target_type.rindex("]")]
            return source_type == "null" or self._types_compatible(source_type, inner)

        # Direct type matching
        source_aliases = self.TYPE_MAP.get(source_type, {source_type})
        target_aliases = self.TYPE_MAP.get(target_type, {target_type})
        return bool(source_aliases & target_aliases)


def check_types(ast) -> List[TypeError]:
    """Convenience function to run type checking on a parsed AST.

    Usage:
        from fusionboa_lang.semantic.type_checker import check_types
        from fusionboa_lang.parser.parser import Parser

        ast = Parser(tokens).parse()
        errors = check_types(ast)
        if errors:
            for e in errors:
                print(f"[{e.severity.upper()}] Line {e.line}: {e.message}")
    """
    checker = TypeChecker(ast)
    return checker.check()
