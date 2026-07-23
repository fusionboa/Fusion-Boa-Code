"""
FusionBoa Language AST Node Definitions

The Abstract Syntax Tree represents the structure of a Fusion program
after parsing. Each node type corresponds to a language construct.
"""

from typing import List, Optional, Any
from dataclasses import dataclass, field


# ---- Base Node ----

@dataclass
class ASTNode:
    """Base class for all AST nodes."""
    line: int = 0
    col: int = 0


# ---- Expressions ----

@dataclass
class Identifier(ASTNode):
    """A variable or function name."""
    name: str = ""

    def __repr__(self):
        return f"Id({self.name})"


@dataclass
class Literal(ASTNode):
    """A literal value (number, string, boolean, null)."""
    value: Any = None

    def __repr__(self):
        return f"Lit({repr(self.value)})"


@dataclass
class BinaryOp(ASTNode):
    """A binary operation like x + y, x > y, etc."""
    left: ASTNode = None
    operator: str = ""
    right: ASTNode = None

    def __repr__(self):
        return f"BinOp({self.left} {self.operator} {self.right})"


@dataclass
class UnaryOp(ASTNode):
    """A unary operation like -x, not x, ++x, --x."""
    operator: str = ""
    operand: ASTNode = None
    prefix: bool = True  # True for ++x, False for x++

    def __repr__(self):
        return f"UnaryOp({self.operator} {self.operand})"


@dataclass
class Call(ASTNode):
    """A function/method call."""
    callee: ASTNode = None
    arguments: List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"Call({self.callee}, args={self.arguments})"


@dataclass
class Attribute(ASTNode):
    """An attribute access like obj.property."""
    object: ASTNode = None
    attribute: str = ""

    def __repr__(self):
        return f"Attr({self.object}.{self.attribute})"


@dataclass
class Index(ASTNode):
    """An index access like array[0]."""
    object: ASTNode = None
    index: ASTNode = None

    def __repr__(self):
        return f"Index({self.object}[{self.index}])"


@dataclass
class ListLiteral(ASTNode):
    """A list literal [1, 2, 3]."""
    elements: List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"List({self.elements})"


@dataclass
class DictLiteral(ASTNode):
    """A dictionary literal {key: value}."""
    pairs: List[tuple] = field(default_factory=list)

    def __repr__(self):
        return f"Dict({self.pairs})"


@dataclass
class Lambda(ASTNode):
    """An anonymous function / lambda."""
    parameters: List[str] = field(default_factory=list)
    body: ASTNode = None

    def __repr__(self):
        return f"Lambda({self.parameters} -> {self.body})"


@dataclass
class Ternary(ASTNode):
    """A ternary expression: value if condition else other_value."""
    condition: ASTNode = None
    true_value: ASTNode = None
    false_value: ASTNode = None

    def __repr__(self):
        return f"Ternary({self.true_value} if {self.condition} else {self.false_value})"


# ---- New Expression Types ----

@dataclass
class StringInterpolation(ASTNode):
    """A string with embedded expressions: "Hello, {name}!."""
    parts: List[ASTNode] = field(default_factory=list)
    """List of alternating string literals and expression nodes."""

    def __repr__(self):
        return f"Interp({self.parts})"


@dataclass
class ListComprehension(ASTNode):
    """[expr for each var in iterable if condition]."""
    expression: ASTNode = None
    variable: str = ""
    iterable: ASTNode = None
    condition: Optional[ASTNode] = None

    def __repr__(self):
        return f"ListComp({self.variable} in {self.iterable} => {self.expression})"


@dataclass
class RangeLiteral(ASTNode):
    """0 to 10 (used in expressions)."""
    start: ASTNode = None
    end: ASTNode = None

    def __repr__(self):
        return f"Range({self.start} to {self.end})"


@dataclass
class SpreadElement(ASTNode):
    """...expression (spread/rest)."""
    expression: ASTNode = None

    def __repr__(self):
        return f"Spread({self.expression})"


@dataclass
class KeywordArgument(ASTNode):
    """name = value in a function call."""
    name: str = ""
    value: ASTNode = None

    def __repr__(self):
        return f"Kwarg({self.name} = {self.value})"


# ---- Statements ----

@dataclass
class Program(ASTNode):
    """The root node of a Fusion program."""
    statements: List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"Program({len(self.statements)} stmts)"


@dataclass
class ExpressionStatement(ASTNode):
    """A statement that is just an expression."""
    expression: ASTNode = None


@dataclass
class VariableDeclaration(ASTNode):
    """'let x be value' or 'create a list called name with items'."""
    name: str = ""
    value: ASTNode = None
    var_type: str = ""
    type_annotation: Optional[ASTNode] = None  # TypeAnnotation node

    def __repr__(self):
        return f"VarDecl({self.name} = {self.value})"


@dataclass
class ConstDeclaration(ASTNode):
    """'const PI be 3.14'."""
    name: str = ""
    value: ASTNode = None
    type_annotation: Optional[ASTNode] = None  # TypeAnnotation node


@dataclass
class Assignment(ASTNode):
    """'set x to value'."""
    target: str = ""
    value: ASTNode = None

    def __repr__(self):
        return f"Assign({self.target} = {self.value})"


@dataclass
class AugmentedAssignment(ASTNode):
    """'increase x by value' or 'decrease x by value'."""
    target: str = ""
    operator: str = ""
    value: ASTNode = None


@dataclass
class IfStatement(ASTNode):
    """An if/otherwise-if/otherwise statement."""
    condition: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)
    elif_branches: List[tuple] = field(default_factory=list)
    else_body: List[ASTNode] = field(default_factory=list)


@dataclass
class MatchStatement(ASTNode):
    """A match/case statement (pattern matching)."""
    expression: ASTNode = None
    cases: List[tuple] = field(default_factory=list)
    guarded_cases: List[ASTNode] = field(default_factory=list)  # MatchGuard nodes
    default_body: List[ASTNode] = field(default_factory=list)


@dataclass
class ForLoop(ASTNode):
    """'for each item in collection: body' or 'for i from 0 to 10: body' or 'for key in obj: body'."""
    variable: str = ""
    iterable: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)
    range_from: Optional[ASTNode] = None
    range_to: Optional[ASTNode] = None
    is_dict_iteration: bool = False  # for key in obj (iterating dict keys)


@dataclass
class RepeatLoop(ASTNode):
    """'repeat n times: body'."""
    times: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class WhileLoop(ASTNode):
    """'while condition: body'."""
    condition: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class FunctionDefinition(ASTNode):
    """'define function name with params: body'."""
    name: str = ""
    parameters: List[str] = field(default_factory=list)
    defaults: dict = field(default_factory=dict)  # param_name -> default_value AST
    body: List[ASTNode] = field(default_factory=list)
    is_async: bool = False
    has_rest_param: bool = False
    rest_param_name: str = ""
    is_static: bool = False  # static method
    decorators: List[str] = field(default_factory=list)  # @decorator names
    generics: List[str] = field(default_factory=list)  # e.g. ["T", "U"]
    return_type: Optional[str] = None  # Return type annotation
    param_types: dict = field(default_factory=dict)  # param_name -> type string

    def __repr__(self):
        return f"FuncDef({self.name}({self.parameters}))"


@dataclass
class ClassDefinition(ASTNode):
    """'define class Name<T> inherits from Parent implements IFace: body'."""
    name: str = ""
    parent: Optional[str] = None
    generics: List[str] = field(default_factory=list)  # e.g. ["T", "U"]
    implements: List[str] = field(default_factory=list)  # e.g. ["Drawable"]
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class ReturnStatement(ASTNode):
    """'return value'."""
    value: Optional[ASTNode] = None


@dataclass
class YieldStatement(ASTNode):
    """'yield value'."""
    value: Optional[ASTNode] = None


@dataclass
class BreakStatement(ASTNode):
    """'break' or 'stop'."""
    pass


@dataclass
class ContinueStatement(ASTNode):
    """'continue' or 'skip'."""
    pass


@dataclass
class PassStatement(ASTNode):
    """'pass' or 'do nothing'."""
    pass


@dataclass
class ImportStatement(ASTNode):
    """'use module' or 'from module import items'."""
    module: str = ""
    items: List[str] = field(default_factory=list)
    alias: Optional[str] = None


@dataclass
class ExportStatement(ASTNode):
    """'export function name' or 'export let name be value'."""
    declaration: ASTNode = None


@dataclass
class TryStatement(ASTNode):
    """'try: body catch error as e: handler finally: cleanup'."""
    body: List[ASTNode] = field(default_factory=list)
    catch_var: Optional[str] = None
    catch_body: List[ASTNode] = field(default_factory=list)
    finally_body: List[ASTNode] = field(default_factory=list)


@dataclass
class AwaitExpression(ASTNode):
    """'await expression'."""
    expression: ASTNode = None


@dataclass
class PrintStatement(ASTNode):
    """'print expr'."""
    expression: ASTNode = None


@dataclass
class InputStatement(ASTNode):
    """'input' or 'read' - assigns to target."""
    target: str = ""
    prompt: Optional[str] = None


@dataclass
class LengthExpression(ASTNode):
    """'length of expr'."""
    expression: ASTNode = None


@dataclass
class DoWhileLoop(ASTNode):
    """'do: body; while condition'."""
    condition: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class EnumDefinition(ASTNode):
    """'define enum Name: A, B, C'."""
    name: str = ""
    members: List[str] = field(default_factory=list)


@dataclass
class InExpression(ASTNode):
    """'x in [1,2,3]' membership check."""
    left: ASTNode = None
    right: ASTNode = None


@dataclass
class IsExpression(ASTNode):
    """'x is type' type check."""
    left: ASTNode = None
    right: ASTNode = None


@dataclass
class DictComprehension(ASTNode):
    """{k: v for each k,v in iterable if condition}."""
    key: ASTNode = None
    value: ASTNode = None
    variable: str = ""
    iterable: ASTNode = None
    condition: Optional[ASTNode] = None

    def __repr__(self):
        return f"DictComp({self.variable} in {self.iterable} => {self.key}: {self.value})"


@dataclass
class MultiLineString(ASTNode):
    """A multi-line string literal (triple-quoted)."""
    value: str = ""

    def __repr__(self):
        return f"MLStr({repr(self.value[:30])}...)"


@dataclass
class DeferStatement(ASTNode):
    """'defer: body' - runs at function exit."""
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class SliceExpression(ASTNode):
    """items[1:3] or items[:5] or items[2:]."""
    object: ASTNode = None
    start: Optional[ASTNode] = None
    end: Optional[ASTNode] = None


@dataclass
class GuardStatement(ASTNode):
    """'guard condition else: body' - early exit if condition fails."""
    condition: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class SwapStatement(ASTNode):
    """'swap x and y' - swap values of two variables."""
    left: str = ""
    right: str = ""


@dataclass
class BetweenExpression(ASTNode):
    """'x between a and b' - range check."""
    left: ASTNode = None
    lower: ASTNode = None
    upper: ASTNode = None


@dataclass
class WhenExpression(ASTNode):
    """'when condition then value or other' - inline conditional."""
    condition: ASTNode = None
    true_value: ASTNode = None
    false_value: ASTNode = None


@dataclass
class PushStatement(ASTNode):
    """'push value into list' - append to list."""
    value: ASTNode = None
    target: str = ""


@dataclass
class PopStatement(ASTNode):
    """'pop from list' - remove and return last item."""
    target: str = ""


@dataclass
class EmptyExpression(ASTNode):
    """'list is empty' - check if collection is empty."""
    expression: ASTNode = None


@dataclass
class DestructuringDeclaration(ASTNode):
    """'let [a, b] be [1, 2]' or 'let {name, age} be user'."""
    targets: List[str] = field(default_factory=list)  # Variable names to unpack into
    value: ASTNode = None
    destructure_type: str = "list"  # "list" or "dict"
    var_type: str = "variable"  # "variable" or "constant"

    def __repr__(self):
        return f"DestrDecl({self.targets} = {self.value})"


@dataclass
class GeneratorExpression(ASTNode):
    """(x for each x in items if condition) -- lazy generator."""
    expression: ASTNode = None
    variable: str = ""
    iterable: ASTNode = None
    condition: Optional[ASTNode] = None

    def __repr__(self):
        return f"Generator({self.variable} in {self.iterable} => {self.expression})"


@dataclass
class WithStatement(ASTNode):
    """'with resource: body' - context manager."""
    resource: ASTNode = None
    variable: Optional[str] = None  # optional alias: with x as var
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class DecoratorStatement(ASTNode):
    """'@decorator' - decorator annotation before function/class."""
    name: str = ""
    arguments: List[ASTNode] = field(default_factory=list)


@dataclass
class IncrementExpression(ASTNode):
    """'x++' or '++x' - increment by 1."""
    target: str = ""
    prefix: bool = True

    def __repr__(self):
        op = "++" if self.prefix else "++"
        return f"Inc({self.target})"


@dataclass
class DecrementExpression(ASTNode):
    """'x--' or '--x' - decrement by 1."""
    target: str = ""
    prefix: bool = True

    def __repr__(self):
        op = "--" if self.prefix else "--"
        return f"Dec({self.target})"


@dataclass
class StaticMethodDeclaration(ASTNode):
    """'define static function name with params: body'."""
    declaration: FunctionDefinition = None


@dataclass
class MatchPattern(ASTNode):
    """Pattern match expression like 'x matches /pattern/'."""
    expression: ASTNode = None
    pattern: ASTNode = None


@dataclass
class MatchGuard(ASTNode):
    """Match case with guard: 'case x if x > 5:'."""
    pattern: ASTNode = None
    guard: ASTNode = None  # The condition after 'if'
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class TypeAnnotation(ASTNode):
    """Type annotation like ': int' or ': string'."""
    type_name: str = ""

    def __repr__(self):
        return f"TypeAnn({self.type_name})"


@dataclass
class RegexLiteral(ASTNode):
    """A regex literal like /pattern/flags."""
    pattern: str = ""
    flags: str = ""

    def __repr__(self):
        return f"Regex(/{self.pattern}/{self.flags})"


@dataclass
class InterfaceDefinition(ASTNode):
    """'define interface Name [inherits from Parent]: body'."""
    name: str = ""
    parent: Optional[str] = None
    methods: List[FunctionDefinition] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"Interface({self.name})"


@dataclass
class ImplementsClause(ASTNode):
    """'implements Interface1, Interface2' in class definition."""
    interfaces: List[str] = field(default_factory=list)


@dataclass
class ForAwaitLoop(ASTNode):
    """'for await each item in async_iterable: body'."""
    variable: str = ""
    iterable: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"ForAwait({self.variable} in {self.iterable})"


@dataclass
class OperatorOverload(ASTNode):
    """'define operator + with other: body' inside a class."""
    operator: str = ""  # e.g. "+", "-", "*", "==", "[]"
    parameters: List[str] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"OpOverload({self.operator})"


@dataclass
class TypeOfExpression(ASTNode):
    """'typeof expr' - get the type of an expression."""
    expression: ASTNode = None

    def __repr__(self):
        return f"TypeOf({self.expression})"


@dataclass
class AssertStatement(ASTNode):
    """'assert condition [message]'."""
    condition: ASTNode = None
    message: Optional[ASTNode] = None


@dataclass
class RaiseStatement(ASTNode):
    """'raise error message'."""
    message: ASTNode = None


@dataclass
class DeleteStatement(ASTNode):
    """'delete variable'."""
    target: str = ""
    source: Optional[ASTNode] = None


@dataclass
class UsingStatement(ASTNode):
    """'using resource [as name]: body' - resource management."""
    resource: ASTNode = None
    variable: Optional[str] = None
    body: List[ASTNode] = field(default_factory=list)


# ---- v0.5.0 Masterpiece Edition Nodes ----

@dataclass
class RecordDefinition(ASTNode):
    """'define record Name with field: type, field2: type'."""
    name: str = ""
    fields: List[tuple] = field(default_factory=list)  # [(name, type_str, default), ...]
    generics: List[str] = field(default_factory=list)

    def __repr__(self):
        return f"Record({self.name})"


@dataclass
class PropertyDefinition(ASTNode):
    """'define property name with get: body; set with value: body'."""
    name: str = ""
    type_annotation: Optional[ASTNode] = None
    getter_body: List[ASTNode] = field(default_factory=list)
    setter_body: List[ASTNode] = field(default_factory=list)
    setter_param: str = "value"

    def __repr__(self):
        return f"Property({self.name})"


@dataclass
class NamespaceDefinition(ASTNode):
    """'define namespace Name: body'."""
    name: str = ""
    body: List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"Namespace({self.name})"


@dataclass
class ExtensionDefinition(ASTNode):
    """'define extension on TypeName: body'."""
    target_type: str = ""
    body: List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"Extension({self.target_type})"


@dataclass
class PartialPlaceholder(ASTNode):
    """'_' placeholder for partial application."""
    index: int = 0  # Position in argument list

    def __repr__(self):
        return f"Partial({self.index})"


@dataclass
class CastExpression(ASTNode):
    """'x as int' type casting expression."""
    expression: ASTNode = None
    target_type: str = ""

    def __repr__(self):
        return f"Cast({self.expression} as {self.target_type})"


@dataclass
class LazyDeclaration(ASTNode):
    """'lazy let x be expensive_computation()'."""
    name: str = ""
    value: ASTNode = None
    type_annotation: Optional[ASTNode] = None

    def __repr__(self):
        return f"Lazy({self.name} = {self.value})"


@dataclass
class UnionType(ASTNode):
    """'string | int' union type."""
    types: List[str] = field(default_factory=list)

    def __repr__(self):
        return f"Union({' | '.join(self.types)})"


@dataclass
class OptionalType(ASTNode):
    """'int?' optional type shorthand."""
    inner_type: str = ""

    def __repr__(self):
        return f"Optional({self.inner_type})"


# ---- v0.9.1 Universal Polyglot Edition Nodes ----

# --- Data Structures ---

@dataclass
class SetLiteral(ASTNode):
    """A set literal {1, 2, 3} - distinct from dict by having elements not pairs."""
    elements: List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"Set({self.elements})"


@dataclass
class TupleLiteral(ASTNode):
    """A tuple literal (1, 2, 3) or pair (a, b)."""
    elements: List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"Tuple({self.elements})"


# --- Go Concurrency ---

@dataclass
class GoStatement(ASTNode):
    """'goroutine: body' / 'spin up worker: body' - launch a lightweight concurrent task."""
    name: Optional[str] = None  # optional goroutine name
    body: List[ASTNode] = field(default_factory=list)
    arguments: List[ASTNode] = field(default_factory=list)  # params to pass

    def __repr__(self):
        return f"Go({self.name})"


@dataclass
class ChannelDeclaration(ASTNode):
    """'create channel of Type [with capacity N]' - declare a typed channel."""
    name: str = ""
    channel_type: str = "string"  # Type carried by channel
    capacity: Optional[int] = None  # None = unbuffered

    def __repr__(self):
        return f"Chan({self.name}: {self.channel_type})"


@dataclass
class ChannelSend(ASTNode):
    """'send value through channel' - push data into a channel."""
    value: ASTNode = None
    channel: str = ""

    def __repr__(self):
        return f"ChanSend({self.value} -> {self.channel})"


@dataclass
class ChannelReceive(ASTNode):
    """'listen to channel with var:' / 'receive from channel' - pull data from channel."""
    channel: str = ""
    variable: Optional[str] = None  # bind received value to this var
    body: List[ASTNode] = field(default_factory=list)
    is_range: bool = False  # range over channel until closed

    def __repr__(self):
        return f"ChanRecv({self.channel} -> {self.variable})"


@dataclass
class ChannelSelect(ASTNode):
    """'select: case msg from ch_a: ... case msg from ch_b: ...' - multiplex channels."""
    cases: List[tuple] = field(default_factory=list)  # [(channel, var, body), ...]
    timeout: Optional[ASTNode] = None  # optional timeout
    default_body: List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"ChanSelect({len(self.cases)} cases)"


@dataclass
class ChannelClose(ASTNode):
    """'close channel' - signal no more values."""
    channel: str = ""

    def __repr__(self):
        return f"ChanClose({self.channel})"


# --- Rust Ownership ---

@dataclass
class OwnershipTransfer(ASTNode):
    """'relinquish ownership of var to target' - move semantics."""
    variable: str = ""
    target: Optional[str] = None  # target to transfer to

    def __repr__(self):
        return f"Move({self.variable})"


@dataclass
class BorrowExpression(ASTNode):
    """'borrow variable [mutably]' - borrow a reference."""
    variable: str = ""
    is_mutable: bool = False
    alias: Optional[str] = None  # bind borrowed ref to this name

    def __repr__(self):
        return f"Borrow({self.variable})"


@dataclass
class LifetimeAnnotation(ASTNode):
    """'with lifetime 'a:' - explicit lifetime scope."""
    name: str = "'a"  # lifetime name like 'a, 'scope
    body: List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"Lifetime({self.name})"


# --- C++ Pointers ---

@dataclass
class AddressOfExpression(ASTNode):
    """'location of variable' / 'address of x' - get memory address."""
    target: str = ""

    def __repr__(self):
        return f"AddrOf({self.target})"


@dataclass
class DereferenceExpression(ASTNode):
    """'value at pointer' / 'dereference ptr' - follow pointer."""
    pointer: ASTNode = None

    def __repr__(self):
        return f"Deref({self.pointer})"


@dataclass
class NewExpression(ASTNode):
    """'new Type(args)' - heap allocation."""
    type_name: str = ""
    arguments: List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"New({self.type_name})"


@dataclass
class DeleteExpression(ASTNode):
    """'delete ptr' / 'free memory' - deallocation."""
    target: str = ""

    def __repr__(self):
        return f"Free({self.target})"


# --- Multiple Return Values ---

@dataclass
class MultiReturnStatement(ASTNode):
    """'return a, b, c' - return multiple values (Go, Lua, Python)."""
    values: List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"MultiRet({self.values})"


@dataclass
class YieldFromStatement(ASTNode):
    """'yield from iterable' - delegate to sub-generator (Python)."""
    iterable: ASTNode = None

    def __repr__(self):
        return f"YieldFrom({self.iterable})"


# --- Python-specific ---

@dataclass
class GlobalStatement(ASTNode):
    """'global x, y' - declare names as global."""
    names: List[str] = field(default_factory=list)


@dataclass
class NonlocalStatement(ASTNode):
    """'nonlocal x' - declare name from enclosing scope."""
    names: List[str] = field(default_factory=list)


@dataclass
class AsyncWithStatement(ASTNode):
    """'async with resource as var: body' - async context manager."""
    resource: ASTNode = None
    variable: Optional[str] = None
    body: List[ASTNode] = field(default_factory=list)


# --- Ruby-specific ---

@dataclass
class ModuleDefinition(ASTNode):
    """'define module Name: body' - Ruby module."""
    name: str = ""
    body: List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"Module({self.name})"


@dataclass
class MixinStatement(ASTNode):
    """'include Module' / 'extend Module' - Ruby mixin."""
    mixin_name: str = ""
    mixin_type: str = "include"  # "include", "extend", "prepend"


@dataclass
class SymbolLiteral(ASTNode):
    """':name' - Ruby/Julia symbol literal."""
    name: str = ""

    def __repr__(self):
        return f"Sym(:{self.name})"


@dataclass
class BlockExpression(ASTNode):
    """Ruby block: do |x| ... end or { |x| ... }."""
    parameters: List[str] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)
    is_curly: bool = False  # {} vs do...end style


@dataclass
class YieldToBlock(ASTNode):
    """'yield to block' / 'yield args' - calls the implicit block (Ruby)."""
    arguments: List[ASTNode] = field(default_factory=list)


# --- R Vectorization ---

@dataclass
class VectorizeExpression(ASTNode):
    """'vectorize operation over collection' - element-wise apply."""
    operation: ASTNode = None
    collection: Optional[ASTNode] = None


@dataclass
class FormulaExpression(ASTNode):
    """'y ~ x1 + x2' - R model formula."""
    response: ASTNode = None
    predictors: List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"Formula({self.response} ~ {self.predictors})"


# --- Kotlin-specific ---

@dataclass
class ObjectDefinition(ASTNode):
    """'define object Name: body' - Kotlin singleton."""
    name: str = ""
    body: List[ASTNode] = field(default_factory=list)
    is_companion: bool = False

    def __repr__(self):
        return f"Object({self.name})"


@dataclass
class SealedClassDefinition(ASTNode):
    """'define sealed class Name: body' - Kotlin sealed class hierarchy."""
    name: str = ""
    subclasses: List[str] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class LateInitDeclaration(ASTNode):
    """'lateinit var name: Type' - Kotlin late initialization."""
    name: str = ""
    var_type: str = ""


@dataclass
class SuspendFunction(ASTNode):
    """'suspend function name with params: body' - Kotlin coroutine."""
    declaration: FunctionDefinition = None


# --- Swift-specific ---

@dataclass
class ActorDefinition(ASTNode):
    """'define actor Name: body' - Swift actor for concurrency safety."""
    name: str = ""
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class SubscriptDefinition(ASTNode):
    """'define subscript with index: Type -> ReturnType: body' - Swift subscript."""
    parameters: List[tuple] = field(default_factory=list)  # [(name, type), ...]
    return_type: Optional[str] = None
    getter_body: List[ASTNode] = field(default_factory=list)
    setter_body: List[ASTNode] = field(default_factory=list)


# --- JSX / React ---

@dataclass
class JsxElement(ASTNode):
    """A JSX element like <div className="foo">children</div>."""
    tag: str = ""  # element tag name
    attributes: dict = field(default_factory=dict)  # {name: value}
    children: List[ASTNode] = field(default_factory=list)
    is_self_closing: bool = False

    def __repr__(self):
        return f"JSX(<{self.tag}>)"


@dataclass
class HookCall(ASTNode):
    """React hook like useState(initial) or useEffect(fn, deps)."""
    hook_name: str = ""  # useState, useEffect, useContext, etc.
    arguments: List[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"Hook({self.hook_name})"


# --- TypeScript-specific ---

@dataclass
class TypeAliasDefinition(ASTNode):
    """'type alias Name = Type' - TypeScript type alias."""
    name: str = ""
    aliased_type: str = ""
    generics: List[str] = field(default_factory=list)


@dataclass
class KeyOfExpression(ASTNode):
    """'keyof Type' - TypeScript keyof operator."""
    target_type: str = ""


# --- Julia-specific ---

@dataclass
class BroadcastExpression(ASTNode):
    """'broadcast operation over collection' - Julia dot broadcasting."""
    operation: ASTNode = None
    collection: ASTNode = None


@dataclass
class MacroDefinition(ASTNode):
    """'macro name with args: body' - compile-time code generation."""
    name: str = ""
    parameters: List[str] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)


# --- General-purpose ---

@dataclass
class MutableModifier(ASTNode):
    """'mutable' modifier on variable/field declaration."""
    target: ASTNode = None


@dataclass
class NativeDeclaration(ASTNode):
    """'native function name with params -> Type' - FFI / extern declaration."""
    name: str = ""
    parameters: List[tuple] = field(default_factory=list)  # [(name, type), ...]
    return_type: Optional[str] = None
    library: Optional[str] = None  # external library name


@dataclass
class AtomicCounter(ASTNode):
    """'create shared counter starting at N' - thread-safe atomic counter."""
    name: str = ""
    initial_value: ASTNode = None


@dataclass
class StructTag(ASTNode):
    """Go struct field tag like `json:"name"`."""
    key: str = ""
    value: str = ""


@dataclass
class TemplateLiteral(ASTNode):
    """Tagged template literal: tag`template string`."""
    tag: Optional[str] = None  # e.g., styled, gql, etc.
    parts: List[ASTNode] = field(default_factory=list)  # alternating string/expr


# --- Java-specific additions ---

@dataclass
class PackageDeclaration(ASTNode):
    """'package com.example.app' - Java package declaration."""
    package_path: str = ""


@dataclass
class SynchronizedBlock(ASTNode):
    """'synchronized on lock: body' - Java synchronized block."""
    lock_object: Optional[str] = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class AnnotationDefinition(ASTNode):
    """'@AnnotationName(args)' - Java/C# annotation/attribute."""
    name: str = ""
    arguments: dict = field(default_factory=dict)


# --- C#-specific ---

@dataclass
class DelegateDefinition(ASTNode):
    """'define delegate Name with params -> ReturnType' - C# delegate type."""
    name: str = ""
    parameters: List[tuple] = field(default_factory=list)
    return_type: Optional[str] = None


@dataclass
class EventDeclaration(ASTNode):
    """'event Name with delegate_type' - C# event."""
    name: str = ""
    delegate_type: Optional[str] = None


@dataclass
class PartialClassDefinition(ASTNode):
    """'define partial class Name: body' - C# partial class."""
    name: str = ""
    body: List[ASTNode] = field(default_factory=list)
