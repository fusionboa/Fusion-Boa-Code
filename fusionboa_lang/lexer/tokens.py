"""
FusionBoa Language Token Types
All the tokens our English-like language can produce.
"""

from enum import Enum, auto


class TokenType(Enum):
    # Literals
    IDENTIFIER = auto()
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()

    # English-like keywords
    LET = auto()             # let
    BE = auto()              # be
    SET = auto()             # set
    TO = auto()              # to
    DEFINE = auto()          # define
    FUNCTION = auto()        # function
    CLASS = auto()           # class
    WITH = auto()            # with
    RETURNS = auto()         # returns / return
    IF = auto()              # if
    OR = auto()              # or
    OTHERWISE = auto()       # otherwise
    FOR = auto()             # for
    EACH = auto()            # each
    IN = auto()              # in
    NOT_IN = auto()          # not in
    FROM = auto()            # from
    REPEAT = auto()          # repeat
    TIMES = auto()           # times
    UNTIL = auto()           # until
    WHILE = auto()           # while
    MATCH = auto()           # match
    CASE = auto()            # case
    DEFAULT = auto()         # default
    TRY = auto()             # try
    CATCH = auto()           # catch
    ERROR = auto()           # error
    FINALLY = auto()         # finally
    USE = auto()             # use
    IMPORT = auto()          # import
    AS = auto()              # as
    CREATE = auto()          # create
    CALLED = auto()          # called
    INCREASE = auto()        # increase
    DECREASE = auto()        # decrease
    BY = auto()              # by
    RETURN = auto()          # return
    BREAK = auto()           # break / stop
    CONTINUE = auto()        # continue / skip
    PASS = auto()            # pass
    AWAIT = auto()           # await
    ASYNC = auto()           # async
    INHERITS = auto()        # inherits
    THIS = auto()            # this / self
    NULL = auto()            # null / none / nothing
    PRINT = auto()           # print
    DISPLAY = auto()         # display
    SHOW = auto()            # show
    INPUT = auto()           # input / read
    LENGTH = auto()          # length / size
    TYPE = auto()            # type
    AND = auto()             # and
    NOT = auto()             # not
    ELIF = auto()            # or if (special)
    ELSE = auto()            # else
    CONST = auto()           # const
    YIELD = auto()           # yield
    SPREAD = auto()          # ... (spread/rest)
    EXPORT = auto()          # export

    # New keywords
    SWAP = auto()            # swap
    XOR = auto()             # xor
    WHERE = auto()           # where (in comprehensions)
    THEN = auto()            # then (inline if)
    HAS = auto()             # has (membership)
    HAS_NO = auto()          # has no
    MIN = auto()             # min
    MAX = auto()             # max
    SUM = auto()             # sum
    ABS = auto()             # abs
    ROUND = auto()           # round
    UPPER = auto()           # upper
    LOWER = auto()           # lower
    STRIP = auto()           # strip
    TAKE = auto()            # take
    DROP = auto()            # drop
    UNIQUE = auto()          # unique
    COMPACT = auto()         # compact
    CAPITALIZE = auto()      # capitalize
    TITLE = auto()           # title
    SWAPCASE = auto()        # swapcase
    CONTAINS = auto()        # contains
    STARTS_WITH = auto()     # starts with
    ENDS_WITH = auto()       # ends with
    BETWEEN = auto()         # between
    WHEN = auto()            # when (inline conditional)
    INTO = auto()            # into (push into)
    PUSH = auto()            # push
    POP = auto()             # pop
    EMPTY = auto()           # empty
    ASSERT = auto()          # assert
    RAISE = auto()           # raise / throw
    DELETE = auto()          # delete
    USING = auto()           # using (context manager)
    SWITCH = auto()          # switch (alias for match)
    UNLESS = auto()          # unless
    IS = auto()              # is (for type checks)
    DO = auto()              # do (for do-while loops)
    ENUM = auto()            # enum
    DEFER = auto()           # defer
    GUARD = auto()           # guard
    INTEGER_TYPE = auto()    # integer type
    FLOAT_TYPE = auto()      # float type
    STRING_TYPE = auto()     # string type
    BOOLEAN_TYPE = auto()    # boolean type
    LIST_TYPE = auto()       # list type
    DICT_TYPE = auto()       # dict/dictionary type
    ANY_TYPE = auto()        # any type

    # Bitwise operators
    AMPERSAND = auto()       # &
    TILDE = auto()           # ~
    LESS_LESS = auto()       # <<
    GREATER_GREATER = auto() # >>

    # Null-coalescing
    QUESTION_QUESTION = auto()  # ??
    QUESTION_QUESTION_EQUAL = auto()  # ??=
    PIPE_PIPE = auto()  # ||
    PIPE_PIPE_EQUAL = auto()  # ||=
    AMPERSAND_AMPERSAND = auto()  # &&
    AMPERSAND_AMPERSAND_EQUAL = auto()  # &&=

    # Operators (symbolic)
    PLUS = auto()            # +
    MINUS = auto()           # -
    STAR = auto()            # *
    SLASH = auto()           # /
    SLASH_SLASH = auto()     # // (floor division)
    PERCENT = auto()         # %
    CARET = auto()           # ^ (power)
    EQUAL = auto()           # =
    EQUAL_EQUAL = auto()     # ==
    BANG_EQUAL = auto()      # !=
    LESS = auto()            # <
    GREATER = auto()         # >
    LESS_EQUAL = auto()      # <=
    GREATER_EQUAL = auto()   # >=
    PLUS_EQUAL = auto()      # +=
    MINUS_EQUAL = auto()     # -=
    STAR_EQUAL = auto()      # *=
    SLASH_EQUAL = auto()     # /=
    DOT = auto()             # .
    COMMA = auto()           # ,
    COLON = auto()           # :
    SEMICOLON = auto()       # ;
    LPAREN = auto()          # (
    RPAREN = auto()          # )
    LBRACKET = auto()        # [
    RBRACKET = auto()        # ]
    LBRACE = auto()          # {
    RBRACE = auto()          # }
    ARROW = auto()           # ->
    PIPE = auto()            # |
    PIPE_OP = auto()         # |>
    FAT_ARROW = auto()       # =>
    DOT_DOT = auto()         # ..
    DOT_DOT_DOT = auto()     # ...
    QUESTION = auto()        # ?
    QUESTION_DOT = auto()    # ?.
    COLON_COLON = auto()     # ::

    # Increment/Decrement
    PLUS_PLUS = auto()       # ++
    MINUS_MINUS = auto()     # --

    # Decorator / Special
    AT_SIGN = auto()         # @ (decorator)

    # More English-like syntax
    ADD = auto()             # add
    SUBTRACT = auto()        # subtract
    MULTIPLY = auto()        # multiply
    DIVIDE = auto()          # divide
    FIRST = auto()           # first
    LAST = auto()            # last
    REST = auto()            # rest
    REVERSE = auto()         # reverse
    SORT = auto()            # sort
    CLEAR = auto()           # clear
    APPEND = auto()          # append
    REMOVE = auto()          # remove
    JOIN = auto()            # join
    SPLIT = auto()           # split
    INCLUDES = auto()        # includes
    EXCLUDES = auto()        # excludes
    SAME = auto()            # same as
    IS_SAME_AS = auto()      # is same as
    FOREVER = auto()           # forever (in repeat forever)
    RANGE_KEYWORD = auto()     # range (as a keyword for range from...to)

    # New v0.4.0 tokens
    INTERFACE = auto()        # interface
    IMPLEMENTS = auto()       # implements
    OPERATOR = auto()         # operator (for operator overloading)
    REGEX_LITERAL = auto()    # /pattern/flags
    TYPEOF = auto()           # typeof

    # v0.5.0 tokens - Masterpiece Edition
    RECORD = auto()           # record (data class)
    PROPERTY = auto()         # property (getter/setter)
    GET = auto()              # get (property getter)
    SETTER = auto()           # set (property setter, different from SET)
    NAMESPACE = auto()        # namespace
    EXTENSION = auto()        # extension (extension methods)
    CAST = auto()             # as (type casting operator)
    LAZY = auto()             # lazy (lazy initialization)
    PARTIAL = auto()          # _ (partial application placeholder)
    LOOP = auto()             # loop (for loop alias)

    # v0.5.1 tokens - English Masterpiece
    MAP = auto()              # map/transform collection
    FILTER = auto()           # filter collection
    REDUCE = auto()           # reduce/fold collection
    KEEP = auto()             # keep items where condition
    TRANSFORM = auto()        # transform items
    COMBINE = auto()          # combine/reduce items
    SEARCH = auto()           # search/find in text
    REPLACE_WITH = auto()     # replace pattern with replacement
    COUNT = auto()            # count occurrences
    FIND = auto()             # find in string
    CONTAINS_WORD = auto()    # contains substring
    BEGINS_WITH = auto()      # begins with (alias for starts with)
    CONCLUDES_WITH = auto()   # concludes with (alias for ends with)

    # v0.9.1 tokens - Universal Polyglot Edition (ALL 23 language features)
    # Data Structures
    SET_TYPE = auto()          # set (data type)
    TUPLE_TYPE = auto()        # tuple (data type)
    SET_LITERAL = auto()       # {1, 2, 3} set literal (distinct from dict by parser context)
    TUPLE_LITERAL = auto()     # (1, 2, 3) tuple literal
    PAIR = auto()              # (a, b) pair / 2-tuple

    # Go Concurrency (Goroutines & Channels)
    GOROUTINE = auto()         # goroutine / go / spin up / launch
    CHANNEL = auto()           # channel / create channel
    SEND = auto()              # send through / transmit / pass through
    RECEIVE = auto()           # receive / listen to / await from
    SELECT_CHANNEL = auto()    # select on channels
    CLOSE_CHANNEL = auto()     # close channel / shut channel
    BUFFERED = auto()          # buffered channel (with capacity)
    FAN_OUT = auto()           # fan out (one producer → many)
    FAN_IN = auto()            # fan in (many producers → one)

    # Rust Ownership & Borrowing
    OWNERSHIP = auto()         # ownership / own / possess
    BORROW = auto()            # borrow / lend
    LIFETIME = auto()          # lifetime / lifespan
    MUTABLE_BORROW = auto()    # mutable borrow
    MOVE_SEMANTICS = auto()    # move / transfer / hand over
    SMART_POINTER = auto()     # smart pointer / box / arc / rc
    UNSAFE = auto()            # unsafe
    RUST_DROP = auto()         # drop / dispose (Rust ownership context, distinct from collection DROP)

    # C++ Pointers & Memory
    POINTER = auto()           # pointer
    REFERENCE = auto()         # reference
    ADDRESS_OF = auto()        # address of / location of
    DEREFERENCE = auto()       # dereference / value at
    VIRTUAL = auto()           # virtual
    OVERRIDE = auto()          # override
    ABSTRACT = auto()          # abstract
    INLINE = auto()            # inline
    CONSTEXPR = auto()         # constexpr / compile time constant
    NEW_OP = auto()            # new (heap allocation)
    DELETE_OP = auto()         # delete / free

    # R Vectorization
    VECTORIZE = auto()         # vectorize / broadcast / element wise
    FORMULA = auto()           # formula (R ~ syntax)
    APPLY_FAMILY = auto()      # apply / lapply / sapply

    # React / JSX
    JSX_ELEMENT = auto()       # JSX element
    HOOK = auto()              # hook / use state / use effect
    COMPONENT = auto()         # component

    # Ruby-specific
    MODULE = auto()            # module (Ruby)
    MIXIN = auto()             # mixin / include / extend
    SYMBOL = auto()            # symbol / :name
    BLOCK = auto()             # block (Ruby do...end)
    YIELD_IMPLICIT = auto()    # yield (calls implicit block)

    # Multiple Return Values
    MULTI_RETURN = auto()      # return a, b, c (multiple values)
    YIELD_FROM = auto()        # yield from (Python delegation)

    # Python-specific
    GLOBAL = auto()            # global
    NONLOCAL = auto()          # nonlocal
    ASYNC_WITH = auto()        # async with

    # JS/TS-specific
    TEMPLATE_TAG = auto()      # tagged template literal
    OPTIONAL_CHAIN = auto()    # ?. deep optional chaining
    SYMBOL_TYPE = auto()       # Symbol type (JS)
    BIGINT_TYPE = auto()       # BigInt type (JS)
    TYPE_ALIAS = auto()        # type alias (TS)
    KEYOF = auto()             # keyof (TS)
    INFER = auto()             # infer (TS)
    CONDITIONAL_TYPE = auto()  # conditional type (TS)

    # Java-specific
    PACKAGE = auto()           # package declaration
    SYNCHRONIZED = auto()      # synchronized
    VOLATILE = auto()          # volatile
    TRANSIENT = auto()         # transient
    ANNOTATION = auto()        # annotation / @Override etc

    # C#-specific
    DELEGATE = auto()          # delegate
    EVENT = auto()             # event
    PARTIAL_CLASS = auto()     # partial class

    # Kotlin-specific
    OBJECT = auto()            # object (singleton)
    COMPANION = auto()         # companion object
    SEALED = auto()            # sealed class
    DATA_CLASS = auto()        # data class marker
    LATEINIT = auto()          # lateinit
    SUSPEND = auto()           # suspend (coroutine)
    TYPEALIAS = auto()         # typealias

    # Swift-specific
    ACTOR = auto()             # actor (Swift concurrency)
    SUBSCRIPT = auto()         # subscript
    PROTOCOL = auto()          # protocol (we have INTERFACE, this is for native Swift)

    # Julia-specific
    BROADCAST = auto()         # broadcast / dot operator
    MACRO = auto()             # macro

    # Go-specific extras
    IOTA = auto()              # iota (Go enum generator)
    STRUCT_TAG = auto()         # struct tag

    # General-purpose additions
    MUTABLE = auto()           # mutable modifier
    IMMUTABLE_RECORD = auto()  # immutable record marker
    PACKAGE_DECL = auto()      # package declaration (generalized)
    NATIVE = auto()            # native / extern
    FFI = auto()               # foreign function interface

    # v0.6.0 tokens - Ultimate English Syntax
    ARTICLE = auto()          # the, a, an (ignored by parser)
    ALL = auto()              # all / all of
    ALL_OF = auto()           # all of
    NONE = auto()             # none / none of
    NONE_OF = auto()          # none of
    ANY = auto()              # any / any of
    ANY_OF = auto()           # any of
    END = auto()              # end (block terminator)
    DO_BLOCK = auto()         # do (block starter, alternative to colon)
    THEN_KEYWORD = auto()     # then (control flow connector)
    SATISFY = auto()          # satisfy / match condition
    ARE = auto()              # are (for 'all items are > 5')

    # v0.9.1 - More operator tokens
    TRIPLE_DOT = auto()       # ... (spread/rest, distinct from DOT_DOT_DOT)
    COLON_COLON_LT = auto()   # ::< (turbofish)
    HASH = auto()             # # (Ruby symbol prefix, comment alt)
    BACKTICK = auto()         # ` (template literal, Go struct tag)
    DOLLAR = auto()           # $ (string interpolation prefix)
    TILDE_ARROW = auto()      # ~> (R formula, pattern match arrow)

    # String interpolation
    INTERP_STRING = auto()

    # Special
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    EOF = auto()
    COMMENT = auto()


KEYWORDS = {
    # v0.5.0 new keywords - Masterpiece Edition
    "interface": TokenType.INTERFACE,
    "implements": TokenType.IMPLEMENTS,
    "operator": TokenType.OPERATOR,
    "typeof": TokenType.TYPEOF,
    "record": TokenType.RECORD,
    "property": TokenType.PROPERTY,
    "get": TokenType.GET,
    "setter": TokenType.SETTER,
    "namespace": TokenType.NAMESPACE,
    "extension": TokenType.EXTENSION,
    "cast": TokenType.CAST,
    "lazy": TokenType.LAZY,

    "let": TokenType.LET,
    # v0.5.0 syntax aliases for let
    "var": TokenType.LET,
    "make": TokenType.LET,
    "declare": TokenType.LET,
    "be": TokenType.BE,
    "set": TokenType.SET,
    "assign": TokenType.SET,
    "change": TokenType.SET,
    "update": TokenType.SET,
    "to": TokenType.TO,
    "define": TokenType.DEFINE,
    "def": TokenType.DEFINE,
    "function": TokenType.FUNCTION,
    "func": TokenType.FUNCTION,
    "fn": TokenType.FUNCTION,
    "method": TokenType.FUNCTION,
    "class": TokenType.CLASS,
    "type": TokenType.CLASS,
    "struct": TokenType.CLASS,
    "record": TokenType.RECORD,
    "with": TokenType.WITH,
    "returns": TokenType.RETURNS,
    "if": TokenType.IF,
    "provided": TokenType.IF,
    "given": TokenType.IF,
    "supposing": TokenType.IF,
    "and": TokenType.AND,
    "also": TokenType.AND,
    "or": TokenType.OR,
    "either": TokenType.OR,
    "else": TokenType.ELSE,
    "otherwise else": TokenType.ELSE,
    "or else": TokenType.ELSE,
    "not": TokenType.NOT,
    "is not": TokenType.BANG_EQUAL,
    "otherwise": TokenType.OTHERWISE,
    "for": TokenType.FOR,
    "loop": TokenType.FOR,
    "each": TokenType.EACH,
    "every": TokenType.EACH,
    "foreach": TokenType.FOR,
    "loop over": TokenType.FOR,
    "iterate over": TokenType.FOR,
    "in": TokenType.IN,
    "inside": TokenType.IN,
    "within": TokenType.IN,
    "among": TokenType.IN,
    "not in": TokenType.NOT_IN,
    "outside": TokenType.NOT_IN,
    "not within": TokenType.NOT_IN,
    "from": TokenType.FROM,
    "repeat": TokenType.REPEAT,
    "times": TokenType.TIMES,
    "until": TokenType.UNTIL,
    "till": TokenType.UNTIL,
    "while": TokenType.WHILE,
    "whilst": TokenType.WHILE,
    "as long as": TokenType.WHILE,
    "unless": TokenType.UNLESS,
    "match": TokenType.MATCH,
    "matches": TokenType.MATCH,
    "switch": TokenType.SWITCH,
    "select": TokenType.MATCH,
    "choose": TokenType.MATCH,
    "pick": TokenType.MATCH,
    "case": TokenType.CASE,
    "default": TokenType.DEFAULT,
    "fallback": TokenType.DEFAULT,
    "try": TokenType.TRY,
    "attempt": TokenType.TRY,
    "endeavor": TokenType.TRY,
    "catch": TokenType.CATCH,
    "rescue": TokenType.CATCH,
    "trap": TokenType.CATCH,
    "on error": TokenType.CATCH,
    "error": TokenType.ERROR,
    "finally": TokenType.FINALLY,
    "ensure": TokenType.FINALLY,
    "always": TokenType.FINALLY,
    "cleanup": TokenType.FINALLY,
    "use": TokenType.USE,
    "using": TokenType.USING,
    "employing": TokenType.USING,
    "import": TokenType.IMPORT,
    "include": TokenType.IMPORT,
    "require": TokenType.IMPORT,
    "load": TokenType.IMPORT,
    "as": TokenType.AS,
    "create": TokenType.CREATE,
    "called": TokenType.CALLED,
    "increase": TokenType.INCREASE,
    "increment": TokenType.INCREASE,
    "bump": TokenType.INCREASE,
    "decrease": TokenType.DECREASE,
    "decrement": TokenType.DECREASE,
    "reduce": TokenType.DECREASE,
    "by": TokenType.BY,
    "return": TokenType.RETURN,
    "give": TokenType.RETURN,
    "yield_result": TokenType.RETURN,
    "break": TokenType.BREAK,
    "stop": TokenType.BREAK,
    "exit": TokenType.BREAK,
    "leave": TokenType.BREAK,
    "end loop": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "skip": TokenType.CONTINUE,
    "next": TokenType.CONTINUE,
    "proceed": TokenType.CONTINUE,
    "pass": TokenType.PASS,
    "do nothing": TokenType.PASS,
    "nop": TokenType.PASS,
    "say": TokenType.PRINT,
    "do": TokenType.DO,
    "defer": TokenType.DEFER,
    "postpone": TokenType.DEFER,
    "schedule": TokenType.DEFER,
    "guard": TokenType.GUARD,
    "check": TokenType.GUARD,
    "verify": TokenType.GUARD,
    "enum": TokenType.ENUM,
    "await": TokenType.AWAIT,
    "async": TokenType.ASYNC,
    "inherits": TokenType.INHERITS,
    "this": TokenType.THIS,
    "self": TokenType.THIS,
    "null": TokenType.NULL,
    "none": TokenType.NULL,
    "nothing": TokenType.NULL,
    "print": TokenType.PRINT,
    "display": TokenType.PRINT,
    "show": TokenType.PRINT,
    "input": TokenType.INPUT,
    "read": TokenType.INPUT,
    "length": TokenType.LENGTH,
    "size": TokenType.LENGTH,
    "count": TokenType.LENGTH,
    "number of": TokenType.LENGTH,
    "total": TokenType.COUNT,
    "type": TokenType.TYPE,
    "true": TokenType.BOOLEAN,
    "false": TokenType.BOOLEAN,
    "yes": TokenType.BOOLEAN,
    "no": TokenType.BOOLEAN,
    "const": TokenType.CONST,
    "constant": TokenType.CONST,
    "final": TokenType.CONST,
    "immutable": TokenType.CONST,
    "yield": TokenType.YIELD,
    "export": TokenType.EXPORT,
    "publish": TokenType.EXPORT,
    "expose": TokenType.EXPORT,
    "make public": TokenType.EXPORT,
    "add": TokenType.ADD,
    "subtract": TokenType.SUBTRACT,
    "multiply": TokenType.MULTIPLY,
    "divide": TokenType.DIVIDE,
    "first": TokenType.FIRST,
    "last": TokenType.LAST,
    "rest": TokenType.REST,
    "reverse": TokenType.REVERSE,
    "sort": TokenType.SORT,
    "clear": TokenType.CLEAR,
    "append": TokenType.APPEND,
    "remove": TokenType.REMOVE,
    "join": TokenType.JOIN,
    "split": TokenType.SPLIT,
    "includes": TokenType.INCLUDES,
    "excludes": TokenType.EXCLUDES,
    "same as": TokenType.SAME,
    "is same as": TokenType.IS_SAME_AS,
    "swap": TokenType.SWAP,
    "xor": TokenType.XOR,
    "where": TokenType.WHERE,
    "then": TokenType.THEN,
    "has": TokenType.HAS,
    "has no": TokenType.HAS_NO,
    "min": TokenType.MIN,
    "max": TokenType.MAX,
    "sum": TokenType.SUM,
    "abs": TokenType.ABS,
    "round": TokenType.ROUND,
    "upper": TokenType.UPPER,
    "lower": TokenType.LOWER,
    "strip": TokenType.STRIP,
    "take": TokenType.TAKE,
    "drop": TokenType.DROP,
    "unique": TokenType.UNIQUE,
    "compact": TokenType.COMPACT,
    "capitalize": TokenType.CAPITALIZE,
    "title": TokenType.TITLE,
    "swapcase": TokenType.SWAPCASE,
    "count": TokenType.LENGTH,
    "contains": TokenType.CONTAINS,
    "starts with": TokenType.STARTS_WITH,
    "ends with": TokenType.ENDS_WITH,
    "between": TokenType.BETWEEN,
    "when": TokenType.WHEN,
    "into": TokenType.INTO,
    "push": TokenType.PUSH,
    "pop": TokenType.POP,
    "empty": TokenType.EMPTY,
    "is a": TokenType.IS,
    "is an": TokenType.IS,
    "pow": TokenType.CARET,
    "assert": TokenType.ASSERT,
    "raise": TokenType.RAISE,
    "throw": TokenType.RAISE,
    "panic": TokenType.RAISE,
    "fail": TokenType.RAISE,
    "crash": TokenType.RAISE,
    "delete": TokenType.DELETE,
    "erase": TokenType.DELETE,
    "is": TokenType.IS,
    "mod": TokenType.PERCENT,
    "div": TokenType.SLASH_SLASH,
    "forever": TokenType.FOREVER,
    "range": TokenType.RANGE_KEYWORD,
    # v0.5.1 English masterpiece - even more natural aliases
    "map": TokenType.MAP,
    "transform": TokenType.TRANSFORM,
    "filter": TokenType.FILTER,
    "fold": TokenType.REDUCE,
    "combine": TokenType.REDUCE,
    "keep": TokenType.KEEP,
    "search": TokenType.SEARCH,
    "find": TokenType.FIND,
    "count": TokenType.LENGTH,
    "total": TokenType.LENGTH,
    "count occurrences": TokenType.COUNT,
    "total occurrences": TokenType.COUNT,
    # Arithmetic synonyms
    "plus": TokenType.PLUS,
    "minus": TokenType.MINUS,
    "times": TokenType.STAR,
    "over": TokenType.SLASH,
    "divided by": TokenType.SLASH,
    "multiplied by": TokenType.STAR,
    "raised to": TokenType.CARET,
    # More comparison synonyms
    "exceeds": TokenType.GREATER,
    "is above": TokenType.GREATER,
    "below": TokenType.LESS,
    "is below": TokenType.LESS,
    "is under": TokenType.LESS,
    "differs from": TokenType.BANG_EQUAL,
    "is different from": TokenType.BANG_EQUAL,
    # Natural preposition / action words
    "put": TokenType.PUSH,
    "stuff": TokenType.PUSH,
    "insert": TokenType.PUSH,
    "grab": TokenType.POP,
    "pull": TokenType.POP,
    "yank": TokenType.POP,
    # NOTE: 'for every'/'for all' removed as multi-word - they merge FOR+EACH
    # which breaks the parser's for-statement detection.
    # Use 'for each' or 'for every' (two separate tokens) instead.
    "from each": TokenType.FROM,
    "on each": TokenType.EACH,
    "whenever": TokenType.IF,
    "in case": TokenType.MATCH,
    "on condition": TokenType.IF,
    "if and when": TokenType.IF,
    "search for": TokenType.SEARCH,
    "look for": TokenType.SEARCH,
    "hunt for": TokenType.SEARCH,
    "replace": TokenType.REPLACE_WITH,
    "substitute": TokenType.REPLACE_WITH,
    "starting with": TokenType.STARTS_WITH,
    "begins with": TokenType.BEGINS_WITH,
    "beginning with": TokenType.STARTS_WITH,
    "ending with": TokenType.ENDS_WITH,
    "concludes with": TokenType.CONCLUDES_WITH,
    "finishing with": TokenType.ENDS_WITH,

    "contains word": TokenType.CONTAINS,
    "holds": TokenType.CONTAINS,
    # NOTE: 'has item' removed - merging into HAS loses the right operand.
    # Use 'has "item"' (quoted) or 'contains item' instead.
    "lacks": TokenType.HAS_NO,
    "is missing": TokenType.HAS_NO,
    "doesn't have": TokenType.HAS_NO,
    # Natural math words
    "squared": TokenType.CARET,
    "cubed": TokenType.CARET,
    "root of": TokenType.CARET,
    "remainder of": TokenType.PERCENT,
    "modulo": TokenType.PERCENT,
    # Type synonyms - ONLY canonical names retained
    "integer": TokenType.INTEGER_TYPE,
    "float": TokenType.FLOAT_TYPE,
    "string": TokenType.STRING_TYPE,
    "boolean": TokenType.BOOLEAN_TYPE,
    "list": TokenType.LIST_TYPE,
    "dict": TokenType.DICT_TYPE,
    "dictionary": TokenType.DICT_TYPE,
    "any": TokenType.ANY_TYPE,
    # Natural command words  
    "write": TokenType.PRINT,
    "output": TokenType.PRINT,
    "log": TokenType.PRINT,
    "echo": TokenType.PRINT,
    "ask": TokenType.INPUT,
    "prompt": TokenType.INPUT,
    "question": TokenType.INPUT,
    "request": TokenType.INPUT,
    "respond with": TokenType.RETURN,
    "answer with": TokenType.RETURN,
    "hand back": TokenType.RETURN,
    # Natural OOP words
    "constructor": TokenType.FUNCTION,
    "initializer": TokenType.FUNCTION,
    "factory": TokenType.FUNCTION,
    "builder": TokenType.FUNCTION,
    "extends": TokenType.INHERITS,
    "derives from": TokenType.INHERITS,
    "subclass of": TokenType.INHERITS,
    "child of": TokenType.INHERITS,
    "is a kind of": TokenType.INHERITS,
    # Natural control flow
    "otherwise if": TokenType.ELIF,
    "else if": TokenType.ELIF,
    "else when": TokenType.ELIF,
    "or when": TokenType.ELIF,
    # English comparison operators (multi-word)
    "is equal to": TokenType.EQUAL_EQUAL,
    "equals": TokenType.EQUAL_EQUAL,
    "is not equal to": TokenType.BANG_EQUAL,
    "is not": TokenType.BANG_EQUAL,
    "does not equal": TokenType.BANG_EQUAL,
    "is greater than": TokenType.GREATER,
    "is more than": TokenType.GREATER,
    "is less than": TokenType.LESS,
    "is fewer than": TokenType.LESS,
    "is greater than or equal to": TokenType.GREATER_EQUAL,
    "is at least": TokenType.GREATER_EQUAL,
    "is less than or equal to": TokenType.LESS_EQUAL,
    "is at most": TokenType.LESS_EQUAL,
    # v0.6.0 Ultimate English Syntax - articles, quantifiers, and natural speech
    # Articles (parser ignores these for natural language flow)
    # NOTE: 'a' and 'an' are NOT articles - they're too common as variable names
    # The parser handles 'a'/'an' contextually (e.g., after 'create')
    "the": TokenType.ARTICLE,
    # Quantifiers
    "all": TokenType.ALL,
    "all of": TokenType.ALL,
    "every single": TokenType.ALL,
    "every one of": TokenType.ALL,
    "each and every": TokenType.ALL,
    "none of": TokenType.NONE,
    "not a single": TokenType.NONE,
    "no items": TokenType.NONE,
    "any of": TokenType.ANY,
    "any item": TokenType.ANY,
    # Block keywords
    "end": TokenType.END,
    "done": TokenType.END,
    "finished": TokenType.END,
    "and then": TokenType.THEN,
    "satisfy": TokenType.SATISFY,
    "satisfies": TokenType.SATISFY,
    "meets": TokenType.SATISFY,
    "are": TokenType.ARE,
    # Even more function aliases
    "procedure": TokenType.FUNCTION,
    "routine": TokenType.FUNCTION,
    "subroutine": TokenType.FUNCTION,
    "operation": TokenType.FUNCTION,
    "action": TokenType.FUNCTION,
    "handler": TokenType.FUNCTION,
    "callback": TokenType.FUNCTION,
    "listener": TokenType.FUNCTION,
    "arrow function": TokenType.FUNCTION,
    # Even more variable aliases
    "set up": TokenType.LET,
    "establish": TokenType.LET,
    "initialize": TokenType.LET,
    "configure": TokenType.LET,
    "instantiate": TokenType.CREATE,
    "construct": TokenType.CREATE,
    "build": TokenType.CREATE,
    # Even more print/view aliases
    "emit": TokenType.PRINT,
    "tell": TokenType.PRINT,
    "announce": TokenType.PRINT,
    "report": TokenType.PRINT,
    "notify": TokenType.PRINT,
    "dump": TokenType.PRINT,
    # Even more return aliases
    "send back": TokenType.RETURN,
    "provide": TokenType.RETURN,
    "furnish": TokenType.RETURN,
    "supply": TokenType.RETURN,
    "produce": TokenType.RETURN,
    # Even more if aliases
    "in the event that": TokenType.IF,
    "on the condition that": TokenType.IF,
    "assuming": TokenType.IF,
    "presuming": TokenType.IF,
    "should": TokenType.IF,
    "in the case that": TokenType.IF,
    # Even more for loop aliases
    "going through": TokenType.FOR,
    "traversing": TokenType.FOR,
    "iterating over": TokenType.FOR,
    "across": TokenType.FOR,
    "throughout": TokenType.FOR,
    # Natural comparison aliases
    "bigger than": TokenType.GREATER,
    "larger than": TokenType.GREATER,
    "longer than": TokenType.GREATER,
    "taller than": TokenType.GREATER,
    "smaller than": TokenType.LESS,
    "tinier than": TokenType.LESS,
    "shorter than": TokenType.LESS,
    # Natural prepositions (mapped to existing tokens)
    "onto": TokenType.INTO,
    # v0.6.1 - Even more natural English speech patterns
    # Question words for conditions
    # NOTE: 'does' removed as IF alias - conflicts with statement parsing
    "does not": TokenType.NOT,
    "cannot": TokenType.NOT,
    "can not": TokenType.NOT,
    "has not": TokenType.HAS_NO,

    # Time and sequence words
    "after": TokenType.THEN,
    # NOTE: "before" removed from IF alias - handled by parser as soft keyword
    "then after": TokenType.THEN,
    "subsequently": TokenType.THEN,
    "thereafter": TokenType.THEN,
    "following that": TokenType.THEN,
    # Even more natural math
    "add up": TokenType.REDUCE,
    "add together": TokenType.PLUS,
    "take away": TokenType.MINUS,
    "multiply together": TokenType.STAR,
    "split into": TokenType.SLASH,
    "distribute": TokenType.DIVIDE,
    "share": TokenType.DIVIDE,
    "is exactly": TokenType.EQUAL_EQUAL,
    "identical to": TokenType.EQUAL_EQUAL,
    "is roughly": TokenType.EQUAL_EQUAL,
    "is approximately": TokenType.EQUAL_EQUAL,
    "is close to": TokenType.EQUAL_EQUAL,
    "is nowhere near": TokenType.BANG_EQUAL,
    "exceeds by far": TokenType.GREATER,
    "is way bigger than": TokenType.GREATER,
    "is way smaller than": TokenType.LESS,
    "is nowhere close to": TokenType.BANG_EQUAL,
    # Membership variations
    "appears in": TokenType.IN,
    "exists in": TokenType.IN,
    "belongs to": TokenType.IN,
    "resides in": TokenType.IN,
    "is part of": TokenType.IN,
    "is member of": TokenType.IN,
    "is element of": TokenType.IN,
    "does not appear in": TokenType.NOT_IN,
    "does not exist in": TokenType.NOT_IN,
    "is absent from": TokenType.NOT_IN,
    # Type annotations - canonical names only (non-canonical synonyms removed)
    # Even more Boolean variations
    "definitely": TokenType.BOOLEAN,
    "absolutely": TokenType.BOOLEAN,
    "certainly": TokenType.BOOLEAN,
    "surely": TokenType.BOOLEAN,
    "indeed": TokenType.BOOLEAN,
    "positively": TokenType.BOOLEAN,
    "affirmative": TokenType.BOOLEAN,
    "negative": TokenType.BOOLEAN,
    "never": TokenType.BOOLEAN,
    "nada": TokenType.BOOLEAN,
    "nah": TokenType.BOOLEAN,
    "yeah": TokenType.BOOLEAN,
    "yep": TokenType.BOOLEAN,
    "maybe": TokenType.NULL,
    "perhaps": TokenType.NULL,
    "possibly": TokenType.NULL,
    # Even more polite/casual language
    "please": TokenType.ARTICLE,
    "kindly": TokenType.ARTICLE,
    "thank you": TokenType.RETURN,
    "thanks": TokenType.RETURN,
    "cheers": TokenType.RETURN,
    # NOTE: Single-word print aliases (nice, excellent, etc.) removed from lexer.
    # These are handled by the parser as "soft keywords" to avoid collisions
    # with variable names like cool_factor or string values like "excellent".
    # Multi-word print aliases (like "thank you") remain in the lexer.
    # Even more action verbs
    "start": TokenType.LET,
    "begin": TokenType.LET,
    "commence": TokenType.LET,
    "launch": TokenType.CREATE,
    "initiate": TokenType.CREATE,
    "spin up": TokenType.CREATE,
    "boot up": TokenType.CREATE,
    "tear down": TokenType.DELETE,
    "destroy": TokenType.DELETE,
    "annihilate": TokenType.DELETE,
    "obliterate": TokenType.DELETE,
    "duplicate": TokenType.CREATE,
    "clone": TokenType.CREATE,
    "copy": TokenType.CREATE,
    "replicate": TokenType.CREATE,
    "mirror": TokenType.CREATE,
    "freeze": TokenType.CONST,
    "lock": TokenType.CONST,
    "seal": TokenType.CONST,
    "unlock": TokenType.SET,
    "release": TokenType.SET,
    "liberate": TokenType.RETURN,
    "toss": TokenType.DELETE,
    "chuck": TokenType.DELETE,
    "ditch": TokenType.DELETE,
    "bin": TokenType.DELETE,
    "trash": TokenType.DELETE,
    "scrap": TokenType.DELETE,
    "junk": TokenType.DELETE,
    "nuke": TokenType.DELETE,
    "zap": TokenType.DELETE,
    # Natural comparison connectors
    "as big as": TokenType.EQUAL_EQUAL,
    "as large as": TokenType.EQUAL_EQUAL,
    "as small as": TokenType.EQUAL_EQUAL,
    "as fast as": TokenType.EQUAL_EQUAL,
    "as good as": TokenType.EQUAL_EQUAL,
    "not as big as": TokenType.LESS,
    "not as large as": TokenType.LESS,
    "not as good as": TokenType.LESS,
    # Even more natural for loops
    # NOTE: 'for every single'/'for every one of' removed - same FOR+EACH merge issue
    "scanning through": TokenType.FOR,
    "looking at each": TokenType.FOR,
    "examining each": TokenType.FOR,
    "visiting each": TokenType.FOR,
    "touching each": TokenType.FOR,
    "processing each": TokenType.FOR,
    # Even more functional ops
    "collect": TokenType.REDUCE,
    "gather": TokenType.REDUCE,
    "compile": TokenType.REDUCE,
    "amass": TokenType.REDUCE,
    "marshal": TokenType.REDUCE,
    "summarize": TokenType.REDUCE,
    "condense": TokenType.REDUCE,
    "distill": TokenType.REDUCE,
    "boil down": TokenType.REDUCE,
    "narrow down": TokenType.FILTER,
    "cull": TokenType.FILTER,
    "prune": TokenType.DELETE,
    "sift": TokenType.FILTER,
    "strain": TokenType.FILTER,
    "winnow": TokenType.FILTER,
    "query": TokenType.SEARCH,
    # NOTE: "interrogate" removed from SEARCH to avoid collision
    # with v0.9.0 reflection syntax ("interrogate layout of...").
    # Falls through to IDENTIFIER for spec-level forward compatibility.
    "probe": TokenType.SEARCH,
    "explore": TokenType.SEARCH,
    "scan": TokenType.SEARCH,
    "sweep": TokenType.SEARCH,
    "traverse": TokenType.FOR,
    "walk": TokenType.FOR,
    "stroll through": TokenType.FOR,
    # Even more error words
    "oops": TokenType.RAISE,
    "whoops": TokenType.RAISE,
    "uh oh": TokenType.RAISE,
    "yikes": TokenType.RAISE,
    "alas": TokenType.RAISE,
    "oh no": TokenType.RAISE,
    "darn": TokenType.RAISE,
    "shoot": TokenType.RAISE,
    "rats": TokenType.RAISE,
    "bother": TokenType.RAISE,
    # Even more return words
    "yay": TokenType.RETURN,
    "woohoo": TokenType.RETURN,
    "hooray": TokenType.RETURN,
    "victory": TokenType.RETURN,
    "success": TokenType.RETURN,
    "accomplished": TokenType.RETURN,
    "achieved": TokenType.RETURN,
    "fulfilled": TokenType.RETURN,
    # v0.7.0 FusionBoa - more natural English patterns
    # Natural purpose/intent
    "in order to": TokenType.FOR,
    "so that": TokenType.IF,
    "for the purpose of": TokenType.FOR,
    "aiming to": TokenType.FOR,
    "seeking to": TokenType.FOR,
    # Time adverbs
    "initially": TokenType.LET,
    "firstly": TokenType.LET,
    "secondly": TokenType.LET,
    "lastly": TokenType.LET,
    "eventually": TokenType.LET,
    "meanwhile": TokenType.AND,
    # More math/number words
    "double": TokenType.STAR,
    "triple": TokenType.STAR,
    "quadruple": TokenType.STAR,
    # Natural string operations
    "trim": TokenType.STRIP,
    "whitespace": TokenType.STRIP,
    # More functional patterns
    "partition": TokenType.SPLIT,
    "chunk": TokenType.SPLIT,
    # More control flow
    "otherwise when": TokenType.ELIF,
    "in that case": TokenType.ELSE,
    "in other cases": TokenType.ELSE,
    "regardless": TokenType.FINALLY,
    "no matter what": TokenType.FINALLY,
    # More boolean/logic
    "whether or not": TokenType.IF,
    # More comparison
    "equals to": TokenType.EQUAL_EQUAL,
    "not equals": TokenType.BANG_EQUAL,
    "is deeper than": TokenType.GREATER,
    "is shallower than": TokenType.LESS,
    "is thicker than": TokenType.GREATER,
    "is thinner than": TokenType.LESS,
    # Sensory/quality words
    "is louder than": TokenType.GREATER,
    "is quieter than": TokenType.LESS,
    "is brighter than": TokenType.GREATER,
    "is dimmer than": TokenType.LESS,
    "is stronger than": TokenType.GREATER,
    "is weaker than": TokenType.LESS,
    "is faster than": TokenType.GREATER,
    "is slower than": TokenType.LESS,
    # More action verbs for operations
    # More action verbs for operations
    "rename": TokenType.SET,
    "modify": TokenType.SET,
    "adjust": TokenType.SET,
    "tweak": TokenType.SET,
    "overhaul": TokenType.SET,
    "revert": TokenType.SET,
    "undo": TokenType.SET,
    "redo": TokenType.SET,
    # More natural print statements
    "mention": TokenType.PRINT,
    "state": TokenType.PRINT,
    "proclaim": TokenType.PRINT,
    "remark": TokenType.PRINT,
    # v0.6.2 - The "Everything But The Kitchen Sink" Final Batch
    # Quantity & measurement words (multi-word 'X of' removed - breaks parser pattern)
    "number of": TokenType.LENGTH,
    # Natural prepositions - more ways to say the same thing
    "through": TokenType.FOR,
    "via": TokenType.USING,
    "per": TokenType.EACH,
    "apiece": TokenType.EACH,
    # Natural equality - more variations
    "same": TokenType.EQUAL_EQUAL,
    "the same": TokenType.EQUAL_EQUAL,
    "matches exactly": TokenType.EQUAL_EQUAL,
    "matches": TokenType.MATCH,
    "corresponds to": TokenType.EQUAL_EQUAL,
    "is equivalent to": TokenType.EQUAL_EQUAL,
    "is identical to": TokenType.EQUAL_EQUAL,
    "is matching": TokenType.EQUAL_EQUAL,
    # Natural inequality variations
    "is unlike": TokenType.BANG_EQUAL,
    "is distinct from": TokenType.BANG_EQUAL,
    "contrasts with": TokenType.BANG_EQUAL,
    "is opposed to": TokenType.BANG_EQUAL,
    # Natural greater/less - more variations
    "surpasses": TokenType.GREATER,
    "outweighs": TokenType.GREATER,
    "dominates": TokenType.GREATER,
    "is superior to": TokenType.GREATER,
    "is higher than": TokenType.GREATER,
    "is older than": TokenType.GREATER,
    "is wider than": TokenType.GREATER,
    "is heavier than": TokenType.GREATER,
    "is inferior to": TokenType.LESS,
    "is lower than": TokenType.LESS,
    "is younger than": TokenType.LESS,
    "is narrower than": TokenType.LESS,
    "is lighter than": TokenType.LESS,
    # Natural range boundaries
    "at minimum": TokenType.GREATER_EQUAL,
    "no less than": TokenType.GREATER_EQUAL,
    "a minimum of": TokenType.GREATER_EQUAL,
    "at maximum": TokenType.LESS_EQUAL,
    "no more than": TokenType.LESS_EQUAL,
    "a maximum of": TokenType.LESS_EQUAL,
    "up to": TokenType.LESS_EQUAL,
    # Natural boolean connectors
    "as well as": TokenType.AND,
    "together with": TokenType.AND,
    "alongside": TokenType.AND,
    "in addition to": TokenType.AND,
    "coupled with": TokenType.AND,
    "combined with": TokenType.AND,
    "alternatively": TokenType.OR,

    # Natural function words
    "given that": TokenType.IF,
    "provided that": TokenType.IF,
    "on the grounds that": TokenType.IF,
    "for the reason that": TokenType.IF,
    "seeing that": TokenType.IF,
    "considering that": TokenType.IF,
    # Natural loop variations
    "running through": TokenType.FOR,
    "cycling through": TokenType.FOR,
    "rotating through": TokenType.FOR,
    "passing through": TokenType.FOR,
    "moving through": TokenType.FOR,
    # Natural error variations
    "abort mission": TokenType.BREAK,
    "give up": TokenType.BREAK,
    "surrender": TokenType.BREAK,
    "withdraw": TokenType.BREAK,
    "retreat": TokenType.BREAK,
    # More casual speech
    "ok": TokenType.BOOLEAN,
    "okay": TokenType.BOOLEAN,
    "alright": TokenType.BOOLEAN,
    "fine": TokenType.BOOLEAN,
    "good": TokenType.BOOLEAN,
    "bad": TokenType.BOOLEAN,
    "not ok": TokenType.BOOLEAN,
    "not okay": TokenType.BOOLEAN,
    "not good": TokenType.BOOLEAN,
    "not fine": TokenType.BOOLEAN,
    # Etc/other
    # NOTE: 'rest of' removed as multi-word - breaks parser
    "remaining": TokenType.REST,
    "remainder": TokenType.REST,
    "everything else": TokenType.REST,
    "others": TokenType.REST,

    # ============ v0.9.1 UNIVERSAL POLYGLOT EDITION ============
    # --- Data Structures ---
    "set collection": TokenType.SET_TYPE,
    "hash set": TokenType.SET_TYPE,
    "unique set": TokenType.SET_TYPE,
    "unordered collection": TokenType.SET_TYPE,
    "tuple": TokenType.TUPLE_TYPE,
    "pair": TokenType.PAIR,
    "immutable list": TokenType.TUPLE_TYPE,
    "fixed list": TokenType.TUPLE_TYPE,
    "read only list": TokenType.TUPLE_TYPE,

    # --- Go Concurrency (Goroutines & Channels) ---
    # NOTE: "go" NOT mapped to GOROUTINE — too common as a variable name.
    # Use multi-word aliases instead.
    "goroutine": TokenType.GOROUTINE,
    "go routine": TokenType.GOROUTINE,
    "spin up": TokenType.GOROUTINE,
    "launch": TokenType.GOROUTINE,
    "spawn": TokenType.GOROUTINE,
    "fork": TokenType.GOROUTINE,
    "run concurrently": TokenType.GOROUTINE,
    "fire off": TokenType.GOROUTINE,
    "kick off": TokenType.GOROUTINE,
    "channel": TokenType.CHANNEL,
    "create channel": TokenType.CHANNEL,
    "make channel": TokenType.CHANNEL,
    "typed pipe": TokenType.CHANNEL,
    "message queue": TokenType.CHANNEL,
    "send through": TokenType.SEND,
    "send": TokenType.SEND,
    "transmit": TokenType.SEND,
    "pass through": TokenType.SEND,
    "push onto": TokenType.SEND,
    "pipe through": TokenType.SEND,
    "deliver to": TokenType.SEND,
    "forward to": TokenType.SEND,
    "relay to": TokenType.SEND,
    "receive": TokenType.RECEIVE,
    "listen to": TokenType.RECEIVE,
    "await from": TokenType.RECEIVE,
    "pull from": TokenType.RECEIVE,
    "take from": TokenType.RECEIVE,
    "consume from": TokenType.RECEIVE,
    "fetch from": TokenType.RECEIVE,
    "select": TokenType.SELECT_CHANNEL,
    "multiplex": TokenType.SELECT_CHANNEL,
    "wait on": TokenType.SELECT_CHANNEL,
    "close channel": TokenType.CLOSE_CHANNEL,
    "shut channel": TokenType.CLOSE_CHANNEL,
    "seal channel": TokenType.CLOSE_CHANNEL,
    "done with channel": TokenType.CLOSE_CHANNEL,
    "fan out": TokenType.FAN_OUT,
    "fan in": TokenType.FAN_IN,
    "broadcast": TokenType.FAN_OUT,
    "scatter": TokenType.FAN_OUT,
    # NOTE: "merge" removed from FAN_IN to avoid collision with common usage.
    "fan in": TokenType.FAN_IN,
    "gather": TokenType.FAN_IN,

    # --- Rust Ownership & Borrowing ---
    "ownership": TokenType.OWNERSHIP,
    "own": TokenType.OWNERSHIP,
    "possess": TokenType.OWNERSHIP,
    "take ownership": TokenType.OWNERSHIP,
    "seize": TokenType.OWNERSHIP,
    "borrow": TokenType.BORROW,
    "lend": TokenType.BORROW,
    "loan": TokenType.BORROW,
    "use temporarily": TokenType.BORROW,
    "lifetime": TokenType.LIFETIME,
    "lifespan": TokenType.LIFETIME,
    "scope": TokenType.LIFETIME,
    "validity": TokenType.LIFETIME,
    "mutable borrow": TokenType.MUTABLE_BORROW,
    "borrow mutably": TokenType.MUTABLE_BORROW,
    "mutably borrow": TokenType.MUTABLE_BORROW,
    "write borrow": TokenType.MUTABLE_BORROW,
    "move": TokenType.MOVE_SEMANTICS,
    "transfer": TokenType.MOVE_SEMANTICS,
    "hand over": TokenType.MOVE_SEMANTICS,
    "give away": TokenType.MOVE_SEMANTICS,
    "relinquish": TokenType.MOVE_SEMANTICS,
    "smart pointer": TokenType.SMART_POINTER,
    "box": TokenType.SMART_POINTER,
    "arc": TokenType.SMART_POINTER,
    "rc": TokenType.SMART_POINTER,
    "shared pointer": TokenType.SMART_POINTER,
    "unsafe": TokenType.UNSAFE,
    "dangerous": TokenType.UNSAFE,
    "unchecked": TokenType.UNSAFE,
    "raw": TokenType.UNSAFE,
    "rust drop": TokenType.RUST_DROP,
    "dispose resource": TokenType.RUST_DROP,
    "release resource": TokenType.RUST_DROP,

    # --- C++ Pointers & Memory ---
    "pointer": TokenType.POINTER,
    "ptr": TokenType.POINTER,
    "raw pointer": TokenType.POINTER,
    "reference": TokenType.REFERENCE,
    "ref": TokenType.REFERENCE,
    "address of": TokenType.ADDRESS_OF,
    "location of": TokenType.ADDRESS_OF,
    "memory address of": TokenType.ADDRESS_OF,
    "where is": TokenType.ADDRESS_OF,
    "dereference": TokenType.DEREFERENCE,
    "value at": TokenType.DEREFERENCE,
    "pointee of": TokenType.DEREFERENCE,
    "follow pointer": TokenType.DEREFERENCE,
    "virtual": TokenType.VIRTUAL,
    "overridable": TokenType.VIRTUAL,
    "polymorphic": TokenType.VIRTUAL,
    "override": TokenType.OVERRIDE,
    "overwrite method": TokenType.OVERRIDE,
    "replace method": TokenType.OVERRIDE,
    "abstract": TokenType.ABSTRACT,
    "pure virtual": TokenType.ABSTRACT,
    "stub": TokenType.ABSTRACT,
    "unimplemented": TokenType.ABSTRACT,
    "inline": TokenType.INLINE,
    "inlined": TokenType.INLINE,
    "embedded function": TokenType.INLINE,
    "constexpr": TokenType.CONSTEXPR,
    "compile time constant": TokenType.CONSTEXPR,
    "compile time eval": TokenType.CONSTEXPR,
    # NOTE: "new" NOT mapped — too common. Use "heap allocate" / "allocate" instead.
    "allocate": TokenType.NEW_OP,
    "heap allocate": TokenType.NEW_OP,
    # NOTE: "free" NOT mapped — too common. Use "deallocate" / "release memory" instead.
    "deallocate": TokenType.DELETE_OP,
    "release memory": TokenType.DELETE_OP,

    # --- R Vectorization ---
    "vectorize": TokenType.VECTORIZE,
    "element wise": TokenType.VECTORIZE,
    "element by element": TokenType.VECTORIZE,
    "broadcast operation": TokenType.VECTORIZE,
    "broadcast": TokenType.VECTORIZE,
    "formula": TokenType.FORMULA,
    "model formula": TokenType.FORMULA,
    "apply": TokenType.APPLY_FAMILY,
    "lapply": TokenType.APPLY_FAMILY,
    "sapply": TokenType.APPLY_FAMILY,
    "vapply": TokenType.APPLY_FAMILY,
    "apply to each": TokenType.APPLY_FAMILY,

    # --- React / JSX ---
    "jsx": TokenType.JSX_ELEMENT,
    "element": TokenType.JSX_ELEMENT,
    "render element": TokenType.JSX_ELEMENT,
    "hook": TokenType.HOOK,
    "use state": TokenType.HOOK,
    "use effect": TokenType.HOOK,
    "use context": TokenType.HOOK,
    "use memo": TokenType.HOOK,
    "use callback": TokenType.HOOK,
    "component": TokenType.COMPONENT,
    "react component": TokenType.COMPONENT,
    "functional component": TokenType.COMPONENT,

    # --- Ruby-specific ---
    "module": TokenType.MODULE,
    "mixin": TokenType.MIXIN,
    "mix in": TokenType.MIXIN,
    "include module": TokenType.MIXIN,
    "extend with": TokenType.MIXIN,
    "prepend module": TokenType.MIXIN,
    # NOTE: "symbol" NOT mapped directly — use "named symbol" to avoid collisions.
    "named symbol": TokenType.SYMBOL,
    # NOTE: "block" NOT mapped directly — too common. Use qualified forms.
    "code block": TokenType.BLOCK,
    "do block": TokenType.BLOCK,
    "yield to block": TokenType.YIELD_IMPLICIT,
    "yield block": TokenType.YIELD_IMPLICIT,
    "call block": TokenType.YIELD_IMPLICIT,

    # --- Multiple Return Values ---
    "return multiple": TokenType.MULTI_RETURN,
    "return pair": TokenType.MULTI_RETURN,
    "return values": TokenType.MULTI_RETURN,
    "yield from": TokenType.YIELD_FROM,
    "delegate yield": TokenType.YIELD_FROM,
    "yield all": TokenType.YIELD_FROM,

    # --- Python-specific ---
    "global": TokenType.GLOBAL,
    "nonlocal": TokenType.NONLOCAL,
    "outer variable": TokenType.NONLOCAL,
    "async with": TokenType.ASYNC_WITH,
    "await with": TokenType.ASYNC_WITH,

    # --- JS/TS-specific ---
    "tagged template": TokenType.TEMPLATE_TAG,
    "tagged string": TokenType.TEMPLATE_TAG,
    "optional chain": TokenType.OPTIONAL_CHAIN,
    "safe navigate": TokenType.OPTIONAL_CHAIN,
    "Symbol": TokenType.SYMBOL_TYPE,
    "BigInt": TokenType.BIGINT_TYPE,
    "type alias": TokenType.TYPE_ALIAS,
    "custom type": TokenType.TYPE_ALIAS,
    "keyof": TokenType.KEYOF,
    "keys of": TokenType.KEYOF,
    "property keys of": TokenType.KEYOF,
    "infer": TokenType.INFER,
    "infer type": TokenType.INFER,
    "conditional type": TokenType.CONDITIONAL_TYPE,
    "type if": TokenType.CONDITIONAL_TYPE,

    # --- Java-specific ---
    "package": TokenType.PACKAGE,
    "namespace package": TokenType.PACKAGE,
    "synchronized": TokenType.SYNCHRONIZED,
    "thread safe": TokenType.SYNCHRONIZED,
    "locked": TokenType.SYNCHRONIZED,
    "volatile": TokenType.VOLATILE,
    "transient": TokenType.TRANSIENT,
    "not serialized": TokenType.TRANSIENT,
    "annotation": TokenType.ANNOTATION,
    "attribute annotation": TokenType.ANNOTATION,

    # --- C#-specific ---
    "delegate": TokenType.DELEGATE,
    "function pointer type": TokenType.DELEGATE,
    # NOTE: "event" NOT mapped directly. Use "event handler" or "publish subscribe".
    "event declaration": TokenType.EVENT,
    "publish subscribe": TokenType.EVENT,
    "event handler": TokenType.EVENT,
    "partial class": TokenType.PARTIAL_CLASS,
    "split class": TokenType.PARTIAL_CLASS,

    # --- Kotlin-specific ---
    "object singleton": TokenType.OBJECT,
    # NOTE: "singleton" NOT mapped directly. Use "object singleton".
    "single instance": TokenType.OBJECT,
    "companion": TokenType.COMPANION,
    "companion object": TokenType.COMPANION,
    "static companion": TokenType.COMPANION,
    "sealed": TokenType.SEALED,
    "sealed class": TokenType.SEALED,
    "closed hierarchy": TokenType.SEALED,
    "data class": TokenType.DATA_CLASS,
    "data record": TokenType.DATA_CLASS,
    "lateinit": TokenType.LATEINIT,
    "late initialize": TokenType.LATEINIT,
    "delay init": TokenType.LATEINIT,
    "suspend": TokenType.SUSPEND,
    "suspend function": TokenType.SUSPEND,
    "pausable": TokenType.SUSPEND,
    "typealias": TokenType.TYPEALIAS,
    "type alias": TokenType.TYPEALIAS,
    "named type": TokenType.TYPEALIAS,

    # --- Swift-specific ---
    # NOTE: "actor" NOT mapped directly — too common. Use "concurrent actor" instead.
    "concurrent actor": TokenType.ACTOR,
    "isolated actor": TokenType.ACTOR,
    "subscript": TokenType.SUBSCRIPT,
    "index accessor": TokenType.SUBSCRIPT,
    # NOTE: "protocol" NOT mapped directly. Use "swift protocol".
    "swift protocol": TokenType.PROTOCOL,

    # --- Julia-specific ---
    "broadcast dot": TokenType.BROADCAST,
    "dot broadcast": TokenType.BROADCAST,
    "element apply": TokenType.BROADCAST,
    # NOTE: "macro" NOT mapped directly. Use "compile time macro" instead.
    "compile time macro": TokenType.MACRO,
    "code generation macro": TokenType.MACRO,

    # --- Go-specific extras ---
    "iota": TokenType.IOTA,
    "iota enum": TokenType.IOTA,
    "auto increment enum": TokenType.IOTA,
    "struct tag": TokenType.STRUCT_TAG,
    "field tag": TokenType.STRUCT_TAG,
    "json tag": TokenType.STRUCT_TAG,

    # --- General-purpose additions ---
    "mutable": TokenType.MUTABLE,
    "changeable": TokenType.MUTABLE,
    "modifiable": TokenType.MUTABLE,
    "immutable record": TokenType.IMMUTABLE_RECORD,
    "frozen record": TokenType.IMMUTABLE_RECORD,
    "fixed record": TokenType.IMMUTABLE_RECORD,
    "native": TokenType.NATIVE,
    "extern": TokenType.NATIVE,
    "foreign": TokenType.NATIVE,
    "ffi": TokenType.FFI,
    "foreign function": TokenType.FFI,
    "external call": TokenType.FFI,
    "c call": TokenType.FFI,

    # --- Operator extensions ---
    "spread": TokenType.SPREAD,
    "expand": TokenType.SPREAD,
    "unpack": TokenType.SPREAD,
    "splat": TokenType.SPREAD,
    "${": TokenType.DOLLAR,
    "#{": TokenType.HASH,
}


TOKEN_NAMES = {v: k for k, v in TokenType.__members__.items()}


class Token:
    """A single token produced by the lexer."""

    def __init__(self, token_type: TokenType, value, line: int, col: int):
        self.type = token_type
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, L{self.line}:C{self.col})"

    def __eq__(self, other):
        if isinstance(other, Token):
            return (self.type == other.type and self.value == other.value
                    and self.line == other.line and self.col == other.col)
        return False
