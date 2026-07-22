# FusionBoa Language — Complete Syntax Reference

**Version 0.7.0 "FusionBoa" — July 2026**

A polyglot programming language with English-like syntax. Write once, compile to 23 targets.
**708 keywords**, **228 token types**, **500+ syntax aliases**, **60+ language features**.

---

## 🗣️ NATURAL ENGLISH — Write Like You Speak!

FusionBoa is designed so you can write code the way you naturally think and speak. The compiler understands **hundreds of different ways** to say the same thing.

### The Language Ignores Filler Words
The article `the` is silently skipped — write naturally:
```fusion
let the x be 5                       # "the" is ignored
for each item in the list:           # reads like English
    print the item                   # natural flow
```
→ Compiles to: `x = 5` / `for item in list: print(item)`

**Note:** `a` and `an` are NOT articles — they're too common as single-letter variable names. The parser handles them contextually (e.g., after `create`).

### Same Meaning, Many Ways — Pick Your Style!
```fusion
# ALL of these do the SAME thing:
let x be 5           var x be 5          declare x be 5
make x be 5          set up x be 5       establish x be 5
start x be 5         begin x be 5        commence x be 5
initialize x be 5    configure x be 5
```

---

## 🆕 v0.6.1 — 170+ NEW ALIASES!

This release adds massive English-like natural language patterns across every category.

### Casual & Polite Language
```fusion
please print x          # "please" → ignored (ARTICLE), prints x
kindly print x          # "kindly" → ignored (ARTICLE), prints x
print excellent          # "excellent" → print()
print awesome            # "awesome" → print()
print cool               # "cool" → print()
print sweet              # "sweet" → print()
print nice               # "nice" → print()
print neat               # "neat" → print()
print brilliant          # "brilliant" → print()
print fantastic          # "fantastic" → print()
print wonderful          # "wonderful" → print()
print terrific           # "terrific" → print()
print superb             # "superb" → print()
return yay               # "yay" → return
return woohoo            # "woohoo" → return
return hooray            # "hooray" → return
return success           # "success" → return
return victory           # "victory" → return
return accomplished      # "accomplished" → return
return achieved          # "achieved" → return
return fulfilled         # "fulfilled" → return
thank you                # "thank you" → return (with no value)
thanks                   # "thanks" → return
cheers                   # "cheers" → return
```

### Question & Sequence Words
```fusion
# Membership questions
2 appears in nums              → 2 in nums
5 exists in items              → 5 in items
num belongs to list            → num in list
value resides in collection    → value in collection
x is part of group             → x in group
x is member of set             → x in set
x is element of array          → x in array
x does not appear in nums      → x not in nums
x does not exist in nums       → x not in nums
x is absent from list          → x not in list

# Time & Sequence
let x be 5
after: print x                 # runs after (then)
before x be 10: ...            # conditional
subsequently: print done       # then
thereafter: cleanup()          # then
following that: print final    # then
```

### Natural Math Expressions
```fusion
let c be a add together b       → c = a + b
let d be a take away 3          → d = a - 3
let e be a multiply together b  → e = a * b
let f be items split into 2     → f = items / 2
distribute budget among 4       → budget / 4
share cookies among 6           → cookies / 6

# Natural comparisons
x is exactly y          → x == y
x identical to y        → x == y
x is roughly y          → x == y
x is approximately y    → x == y
x is close to y         → x == y
x is nowhere near y     → x != y
x exceeds by far y      → x > y
x is way bigger than y  → x > y
x is way smaller than y → x < y
as big as y             → == y
as large as y           → == y
not as big as y         → < y
```

### Rich Boolean Vocabulary
```fusion
# True (all produce actual Python True):
true  yes  yup  yep  yeah  on  enabled
definitely  absolutely  certainly  surely
indeed  positively  affirmative

# False (all produce actual Python False):
false  no  nope  nah  off  disabled
negative  never  nada

# Null (produce Python None):
null  none  nothing  blank  undefined  absent  missing
maybe  perhaps  possibly
```

### Extended Type Names
```fusion
# String types
let c: character be "h"       → c: str = "h"
let w: word be "hello"        → w: str = "hello"
let s: sentence be "Hi!"      → s: str = "Hi!"
let p: paragraph be "..."     → p: str = "..."
let b: bytes be "data"        → b: str = "data"
let sym: symbol be "@"        → sym: str = "@"

# Numeric
let n: bits be 8              → n: int = 8

# Collections
let items: element be [1,2,3]  → list
let vals: elements be [4,5,6]  → list
let e: entries be [7,8,9]      → list
let p: pairs be {a:1}          → dict
let k: keyed list be {x:0}     → dict
```

### Action Verbs (Create & Destroy)
```fusion
# Create aliases
launch a list called items     spin up a dict called config
initiate a list called data    boot up a list called services

# Copy / Clone
duplicate items                clone config
copy data                      replicate template
mirror settings

# Destroy (so many ways!)
delete x     destroy x     annihilate x     obliterate x
tear down x  toss x        chuck x         ditch x
bin x        trash x       scrap x         junk x
nuke x       zap x         prune x

# Const / Lock
freeze PI         lock MAX         seal ID

# Release
unlock name       release data
```

### Natural For Loops
```fusion
# Scanning-style loops
scanning through items: ...
looking at each item in list: ...
examining each item in data: ...
visiting each node in tree: ...
touching each element in array: ...
processing each record in stream: ...
walk items: ...
traverse items: ...
stroll through items: ...

# For-each extensions
for every single item in list: ...
for every one of items: ...
```

### Expanded Functional Operations
```fusion
# Reduce (collect/compile)
collect values using sum      gather data using merge
compile results using join    amass totals using add
marshal data using concat     summarize items using count
condense list using max       distill set using min
boil down items using logic

# Filter (sift/winnow)
narrow down items where x > 0  cull list where not valid
sift data where active         strain items where clean
winnow results where good

# Search (query/probe)
query database for key         interrogate system for status
probe network for responses    explore data for patterns
scan text for matches          sweep array for target
```

### Error Exclamations
```fusion
oops "something broke"     whoops "my bad"
uh oh "oh no"              yikes "that's bad"
alas "sad"                 oh no "not good"
darn "dang"                shoot "missed"
rats "nuts"                bother "annoying"
```

---

## 📊 SYNTAX ALIASES — Complete Reference

### Variables & Assignment
| Primary | Aliases (pick any!) |
|---------|---------------------|
| `let` | `var`, `make`, `declare`, `set up`, `establish`, `initialize`, `configure`, `start`, `begin`, `commence` |
| `const` | `constant`, `final`, `immutable`, `freeze`, `lock`, `seal` |
| `set` | `assign`, `change`, `update`, `unlock`, `release` |
| `create` | `instantiate`, `construct`, `build`, `launch`, `initiate`, `spin up`, `boot up`, `duplicate`, `clone`, `copy`, `replicate`, `mirror` |
| `lazy let` | Lazy initialization |

### Functions & Methods
| Primary | Aliases |
|---------|---------|
| `define` | `def` |
| `function` | `func`, `fn`, `method`, `procedure`, `routine`, `subroutine`, `operation`, `action`, `handler`, `callback`, `listener`, `constructor`, `initializer`, `factory`, `builder`, `arrow function` |
| `return` | `give`, `yield_result`, `send back`, `provide`, `furnish`, `supply`, `produce`, `respond with`, `answer with`, `hand back`, `thank you`, `thanks`, `cheers`, `yay`, `woohoo`, `hooray`, `victory`, `success`, `accomplished`, `achieved`, `fulfilled`, `liberate` |

### Printing & Output
| Primary | Aliases |
|---------|---------|
| `print` | `display`, `show`, `say`, `write`, `output`, `log`, `echo`, `emit`, `tell`, `announce`, `report`, `notify`, `dump`, `inspect`, `debug`, `trace`, `watch`, `nice`, `excellent`, `awesome`, `superb`, `cool`, `sweet`, `neat`, `brilliant`, `fantastic`, `wonderful`, `terrific` |

### Input
| Primary | Aliases |
|---------|---------|
| `input` | `read`, `ask`, `prompt`, `question`, `request` |

### Control Flow — Conditionals
| Primary | Aliases |
|---------|---------|
| `if` | `provided`, `given`, `supposing`, `whenever`, `in the event that`, `on the condition that`, `on condition`, `assuming`, `presuming`, `should`, `in the case that`, `if and when`, `before` |
| `else if` / `elif` | `or if`, `otherwise if`, `else when`, `or when` |
| `else` | `otherwise`, `otherwise else`, `or else` |
| `unless` | Negated if |
| `guard` | `check`, `verify` |

### Control Flow — Loops
| Primary | Aliases |
|---------|---------|
| `for` | `loop`, `foreach`, `loop over`, `iterate over`, `going through`, `traversing`, `iterating over`, `across`, `throughout`, `scanning through`, `looking at each`, `examining each`, `visiting each`, `touching each`, `processing each`, `traverse`, `walk`, `stroll through` |
| `each` | `every`, `for every`, `for all`, `on each`, `every single`, `each and every`, `for every single`, `for every one of` |
| `while` | `whilst`, `as long as` |
| `until` | `till` |
| `break` | `stop`, `exit`, `leave`, `end loop`, `quit`, `abort`, `halt`, `terminate`, `cease` |
| `continue` | `skip`, `next`, `proceed`, `carry on`, `keep going`, `move on`, `advance` |
| `pass` | `do nothing`, `nop` |

### Pattern Matching
| Primary | Aliases |
|---------|---------|
| `match` | `switch`, `select`, `choose`, `pick`, `in case` |
| `default` | `fallback` |

### Error Handling
| Primary | Aliases |
|---------|---------|
| `try` | `attempt`, `endeavor` |
| `catch` | `rescue`, `trap`, `on error` |
| `finally` | `ensure`, `always`, `cleanup` |
| `raise` | `throw`, `panic`, `fail`, `crash`, `oops`, `whoops`, `uh oh`, `yikes`, `alas`, `oh no`, `darn`, `shoot`, `rats`, `bother` |

### Arithmetic & Math
| Primary | Aliases |
|---------|---------|
| `increase` / `+=` | `increment`, `bump` |
| `decrease` / `-=` | `decrement`, `reduce` |
| `+` | `plus`, `add together` |
| `-` | `minus`, `take away` |
| `*` | `times`, `multiplied by`, `doubled`, `tripled`, `multiply together` |
| `/` | `over`, `divided by`, `halved`, `split into`, `distribute`, `share` |
| `^` (power) | `pow`, `raised to`, `squared`, `cubed`, `root of` |
| `%` | `mod`, `remainder of`, `modulo`, `percent` |
| `//` | `div` |

### Comparisons
| Primary | Aliases |
|---------|---------|
| `==` | `equals`, `is equal to`, `is exactly`, `identical to`, `is roughly`, `is approximately`, `is close to`, `as big as`, `as large as`, `as small as`, `as fast as`, `as good as` |
| `!=` | `is not equal to`, `is not`, `does not equal`, `differs from`, `is different from`, `is nowhere near`, `is nowhere close to`, `not as big as`, `not as large as`, `not as good as` |
| `>` | `exceeds`, `is above`, `is greater than`, `is more than`, `bigger than`, `larger than`, `longer than`, `taller than`, `exceeds by far`, `is way bigger than` |
| `<` | `below`, `is below`, `is under`, `is less than`, `is fewer than`, `smaller than`, `tinier than`, `shorter than`, `is way smaller than` |
| `>=` | `is greater than or equal to`, `is at least` |
| `<=` | `is less than or equal to`, `is at most` |
| `and` | `also` |
| `or` | `either` |
| `not` | `!`, `does not`, `cannot`, `can not` |

### Membership & Containment
| Primary | Aliases |
|---------|---------|
| `in` | `inside`, `within`, `among`, `appears in`, `exists in`, `belongs to`, `resides in`, `is part of`, `is member of`, `is element of` |
| `not in` | `outside`, `not within`, `does not appear in`, `does not exist in`, `is absent from` |
| `has` | `has item` |
| `has no` | `lacks`, `is missing`, `doesn't have`, `has not` |
| `contains` | `holds`, `contains word` |
| `starts with` | `starting with`, `begins with`, `beginning with` |
| `ends with` | `ending with`, `concludes with`, `finishing with` |

### Collections & Data
| Primary | Aliases |
|---------|---------|
| `in` | `inside`, `within`, `among` |
| `length` / `len()` | `size`, `count`, `number of` |
| `push` | `put`, `stuff`, `insert`, `prepend` |
| `pop` | `grab`, `pull`, `yank`, `extract`, `pluck` |
| `append` | `attach`, `tack on` |
| `remove` | `delete`, `erase`, `detach`, `strip out` |
| `reverse` | `flip`, `invert`, `turn around` |
| `sort` | `arrange`, `order`, `rank`, `organize` |
| `clear` | `purge`, `wipe`, `reset`, `empty out` |
| `first` | `fetch`, `retrieve`, `obtain`, `acquire` |
| `drop` | `discard`, `throw away`, `reject`, `omit` |
| `delete` | `erase`, `destroy`, `annihilate`, `obliterate`, `tear down`, `toss`, `chuck`, `ditch`, `bin`, `trash`, `scrap`, `junk`, `nuke`, `zap`, `prune` |

### Functional Operations (v0.5.1+)
| Primary | Aliases |
|---------|---------|
| `map` | `apply`, `convert`, `change each`, `process` |
| `filter` | `keep`, `screen`, `weed out`, `narrow down`, `cull`, `sift`, `strain`, `winnow` |
| `reduce` / `fold` | `accumulate`, `aggregate`, `total up`, `collect`, `gather`, `compile`, `amass`, `marshal`, `summarize`, `condense`, `distill`, `boil down` |
| `combine` | `merge`, `blend`, `fuse`, `unify` |
| `search` | `find`, `look for`, `hunt for`, `locate`, `seek`, `spot`, `discover`, `query`, `interrogate`, `probe`, `explore`, `scan`, `sweep` |
| `replace` | `substitute`, `swap out`, `exchange` |
| `count` | `total` |
| `transform` | Map-style transform on collection |

### OOP & Inheritance
| Primary | Aliases |
|---------|---------|
| `class` | `type`, `struct` |
| `inherits` | `extends`, `derives from`, `subclass of`, `child of`, `is a kind of` |

### Imports & Exports
| Primary | Aliases |
|---------|---------|
| `import` / `use` | `include`, `require`, `load` |
| `export` | `publish`, `expose`, `make public` |

### Resources & Context
| Primary | Aliases |
|---------|---------|
| `using` | `employing` |
| `defer` | `postpone`, `schedule` |
| `async` | Async function modifier |

### Null, Boolean & Types
| Value | Aliases |
|-------|---------|
| `true` | `yes`, `ok`, `correct`, `valid`, `enabled`, `on`, `yup`, `yeah`, `yep`, `definitely`, `absolutely`, `certainly`, `surely`, `indeed`, `positively`, `affirmative` |
| `false` | `no`, `not ok`, `incorrect`, `invalid`, `disabled`, `off`, `nope`, `nah`, `negative`, `never`, `nada` |
| `null` | `none`, `nothing`, `blank`, `undefined`, `absent`, `missing`, `maybe`, `perhaps`, `possibly` |

### Type Names (in annotations)
| Primary | Aliases |
|---------|---------|
| `int` / `integer` | `whole number`, `bits` |
| `float` | `number`, `decimal` |
| `string` | `text`, `character`, `chars`, `word`, `sentence`, `paragraph`, `bytes`, `symbol` |
| `bool` / `boolean` | `flag`, `truth` |
| `list` | `array`, `collection`, `sequence`, `tuple`, `group`, `made of`, `element`, `elements`, `entries` |
| `dict` / `dictionary` | `table`, `hash`, `mapping`, `key value pair`, `associative array`, `key value store`, `pairs`, `keyed list` |

### Prepositions & Connectors
| Word | Maps To |
|------|---------|
| `onto` | `into` push operation |
| `after` | `then` (sequential flow) |
| `subsequently` / `thereafter` / `following that` | `then` |
| `which` / `that` / `whose` | `where` filter condition |
| `and then` | `then` sequential flow |
| `are` | Used for "all items are > 5" pattern |
| `satisfy` / `satisfies` / `meets` | Condition matching |
| `please` / `kindly` | Ignored (ARTICLE) — politeness markers |

---

## 1. VARIABLES & TYPES

```fusion
let name be "Fusion"                    # Variable
var x be 5                              # Alias for let
declare y be 10                         # Alias for let
make z be 100                           # Alias for let
set up w be 100                         # Alias for let
establish v be 42                       # Alias for let
start a be 1                            # Alias for let
begin b be 2                            # Alias for let
commence c be 3                         # Alias for let
initialize counter be 0                 # Alias for let
configure options be []                 # Alias for let
let x: int be 5                         # Typed variable
let x: int? be null                     # Optional type
let x: string | int be "hello"         # Union type
const PI be 3.14159                     # Constant
constant MAX be 100                     # Alias for const
final NAME be "FusionBoa"                    # Alias for const
immutable ID be 42                      # Alias for const
freeze SECRET be "xyz"                  # Alias for const
lock KEY be 42                          # Alias for const
seal TOKEN be "abc"                     # Alias for const
set name to "FusionBoa"                      # Reassign
assign name to "Fusion"                 # Alias for set
change name to "New"                    # Alias for set
update name to "Latest"                 # Alias for set
unlock name                             # Alias for set/release
release data                            # Alias for set/release
lazy let data be expensive()            # Lazy init
increase score by 5                     # score += 5
increment x by 3                        # Alias for increase
bump count by 1                         # Alias for increase
decrease y by 2                         # y -= 2
decrement total by 1                    # y -= 1
reduce amount by 10                     # Alias for decreasing
x++   ++x   y--   --y                  # Increment/decrement
total ||= 10                            # Logical OR assignment
flag &&= false                          # Logical AND assignment
name ??= "guest"                        # Null-coalescing assignment
swap a and b                            # Swap values

# Destructuring
let [a, b, c] be [1, 2, 3]
let {x, y} be point
const [first, rest] be items
```

## 2. DATA TYPES

```fusion
"Hello World"                           # String
42                                      # Integer
19.99                                   # Float
true  |  yes  |  definitely  |  sure   # All → True
false |  no   |  negative   |  never   # All → False
null  |  none  |  nothing  |  maybe    # All → None
[1, 2, 3]                               # List
{name: "Bob", age: 30}                  # Dictionary
/(?:hello|world)/i                      # Regex literal
```

### Type Annotations
```fusion
int | integer | whole number | bits     # Integer type
float | number | decimal                # Float type
string | text | character | chars       # String type
word | sentence | paragraph | bytes     # More string
symbol                                  # String type
bool | boolean | flag | truth           # Boolean type
list | array | collection | sequence    # List type
element | elements | entries            # More list
dict | dictionary | table | hash        # Dict type
pairs | keyed list                      # More dict
any                                      # Any type
void                                     # No return value

# Union types
let x: string | int be "hello"
# Optional types
let x: int? be null
```

## 3. STRINGS & OPERATIONS

```fusion
let name be "Alice"
let msg be "Hello, {name}!"             # String interpolation
capitalize text
title text
swapcase text
upper text
lower text
strip text
join items with ", "
split text by ","
```

## 4. OPERATORS

```fusion
# Arithmetic
+  -  *  /  //  %  ^ (power)
plus  minus  times  over  div  mod  pow
add together   take away   multiply together
split into     distribute   share

# Natural Math
x squared    x cubed    root of x
remainder of x    modulo x    percent x
x doubled    x tripled    x halved

# Comparison
==  !=  <  >  <=  >=
equals  is equal to  is not  is not equal to
is exactly  identical to  is roughly  is approximately
is close to  is nowhere near  is nowhere close to
differs from  is different from  does not equal
is greater than  is more than  is less than  is fewer than
is above  exceeds  is below  is under
bigger than  larger than  longer than  taller than
smaller than  tinier than  shorter than
is way bigger than  is way smaller than
exceeds by far
as big as  as large as  as small as
not as big as  not as large as
is greater than or equal to  is at least
is less than or equal to  is at most

# Logical
and  or  not  !  xor
also  either  does not  cannot  can not

# Membership
x in items    2 appears in nums    5 exists in items
value belongs to list    x resides in collection
x is part of group    x is member of set    x is element of array
x not in items    value does not appear in list
x does not exist in data    x is absent from collection
x inside items    x within items    x among items
x outside items   x not within items
list has item    list holds item    list contains word
list has no item   list lacks item   list is missing item   list doesn't have item   list has not item

# Text checks
text contains "hello"     text starts with "he"     text ends with "lo"
text begins with "he"     text concludes with "lo"  text finishing with "lo"

# Identity & Types
x is same as y    x same as y
x is a string     x is an int
x between 1 and 10

# Bitwise
&  |  ~  <<  >>

# Null & Coalescing
a ?? b           # a if a is not None else b
x ?. property     # Optional chaining

# Pipe
x |> f            # f(x)
items |> reverse  # list(reversed(items))
items |> sort     # list(sorted(items))
items |> unique   # list(set(items))
items |> first    # items[0]
items |> last     # items[-1]

# Increment/Decrement
++x   --x   x++   x--
```

## 5. CONDITIONALS

```fusion
if condition:
    ...

# 15+ ways to start an if statement
provided condition: ...
given x > 0: ...
supposing enabled: ...
in the event that error: ...
on the condition that valid: ...
assuming ready: ...
presuming data: ...
should retry: ...
in the case that match: ...
if and when possible: ...
whenever triggered: ...
before value > 0: ...

unless condition:                       # Negated if (if not condition)
    ...

# Elif / Else
or if other: ...
otherwise if other: ...
else if other: ...
else when other: ...
or when other: ...
or: ...
otherwise: ...
or else: ...
otherwise else: ...

# Guard (early exit)
guard condition else: ...
check condition else: ...
verify condition else: ...

# Inline expressions
when x > 0 then "positive" or "negative"
"pass" if score >= 60 else "fail"
```

## 6. LOOPS

```fusion
# For-each loops (25+ ways!)
for each item in items: ...
loop each item in items: ...
foreach item in items: ...
loop over item in items: ...
iterate over item in items: ...
going through item in items: ...
traversing item in items: ...
iterating over item in items: ...
across item in items: ...
throughout item in items: ...
scanning through item in items: ...
looking at each item in items: ...
examining each item in items: ...
visiting each item in items: ...
touching each item in items: ...
processing each item in items: ...
walk item in items: ...
traverse item in items: ...
stroll through item in items: ...
for every item in items: ...
for all item in items: ...
on each item in items: ...
for every single item in items: ...
for every one of items: ...

# Range loops
for i from 1 to 10: ...
for i from 1 to 10 step 2: ...

# Dict iteration
for key in dict: ...
for key, value in dict: ...

# Async iteration
for await each x in stream: ...

# Repeat loops
repeat 5 times: ...
repeat forever: ...

# While loops
while x > 0: ...
whilst running: ...
as long as running: ...

# Until loops
until done: ...
till finished: ...

# Do-while
do: ... while x > 0

# Loop control
break  |  stop  |  exit  |  leave  |  end loop
quit   |  abort  |  halt  |  terminate  |  cease
continue  |  skip  |  next  |  proceed
carry on  |  keep going  |  move on  |  advance
pass  |  do nothing  |  nop
```

## 7. FUNCTIONS

```fusion
define function greet with name:
    return "Hello, " + name + "!"

# 20+ function aliases
def function process with data: ...
define func transform with x: ...
define fn compute with a, b: ...
define method calculate with x: ...
define procedure handle with event: ...
define routine cleanup: ...
define subroutine helper with args: ...
define operation execute with params: ...
define action perform with input: ...
define handler on_click with event: ...
define callback on_done with result: ...
define listener on_change with value: ...

# 20+ return aliases
give result          send back value        provide data
furnish info         supply answer           produce output
respond with msg     answer with result      hand back value
thank you            thanks                 cheers
yay                  woohoo                 hooray
victory              success                accomplished
achieved             fulfilled              liberate

# Parameter variations
define function power with base, exp = 2: ...
define function sum_all with ...args: ...
define function first<T> with items: list -> T: ...

# Async
define async function fetch with url: ...

# Static
define static function helper: ...

# Lambda
function with x: x * 2
```

## 8. CLASSES & OOP

```fusion
define class Animal:
    define function init with name:
        set this.name to name

# Class aliases
define type Animal: ...
define struct Point: ...

# Inheritance
define class Dog inherits from Animal: ...
define class Dog extends Animal: ...
define class Dog derives from Animal: ...
define class Dog subclass of Animal: ...
define class Dog child of Animal: ...
define class Dog is a kind of Animal: ...

# Generics
define class Box<T>:
define class Pair<T, U>:

# Interfaces
define class Service implements Drawable: ...

# Static methods
define static function factory with args: ...

# Operator overloading
define operator + with other: ...
define operator == with other: ...
```

## 9. RECORD TYPES

```fusion
define record Point with x: int, y: int
define record Person with name: string, age: int = 0
define record Pair<T, U> with first: T, second: U
```

## 10. PROPERTIES

```fusion
define property full_name with get:
    return this.first + " " + this.last
    set with value:
        let parts be split value by " "
        set this.first to first of parts
        set this.last to last of parts
```

## 11. INTERFACES

```fusion
define interface Drawable:
    define function draw:
        pass

define interface Comparable<T>:
    define function compare with other: T -> int:
        pass
```

## 12. PATTERN MATCHING

```fusion
match value:
    case 1: ...
    case 2: ...
    case x if x > 5: ...
    default: ...           # or fallback:

# Match aliases
select option: ...          choose item: ...
pick choice: ...             in case value: ...
```

## 13. FUNCTIONAL OPERATIONS

```fusion
# Map / Transform
map items using func
apply func to items
convert items using transform
change each item in items using process
transform each x in items using square

# Filter
filter items where x > 5
filter items keeping x where condition
keep items where condition
screen items where active
weed out items where not valid
narrow down items where x > 0
cull list where not valid
sift data where active
strain items where clean
winnow results where good

# Reduce / Fold / Combine
fold items using add starting with 0
combine items using merge starting with []
accumulate values using sum starting with 0
aggregate data using collect starting with {}
total up numbers using add starting with 0
collect values using sum
gather data using merge
compile results using join
amass totals using add
marshal data using concat
summarize items using count
condense list using max
distill set using min
boil down items using logic
merge lists using concat
blend dicts using update
fuse items using join
unify sets using union

# Search / Find (15+ ways)
search needle in haystack
search for pattern in text
find key in database
look for item in list
hunt for bug in code
locate element in array
seek value in collection
spot match in text
discover pattern in data
query database for key
interrogate system for status
probe network for responses
explore data for patterns
scan text for matches
sweep array for target

# Replace / Substitute
replace old in text with new
replace pattern in string with replacement
substitute target in source with value
swap out x in list with y
exchange a in items with b

# Count
count occurrences of item in collection
total occurrences of value in list

# Chaining
items |> map using double |> filter where x > 3 |> fold using add starting with 0
```

## 14. ERROR HANDLING

```fusion
try:
    ...
catch error as e:
    ...
finally:
    ...

# Error handling aliases
attempt: ... rescue error as e: ... ensure: ...
try: ... trap error as e: ... always: ...
try: ... on error as e: ... cleanup: ...

# Raising errors (so many fun ways!)
raise "message"
raise error "message"
throw "message"
panic "message"
fail "message"
crash "message"
oops "something broke"
whoops "my bad"
uh oh "not good"
yikes "bad news"
alas "sad trombone"
oh no "disaster"
darn "dang it"
shoot "missed"
rats "nuts"
bother "annoying"

# Assertions
assert condition
assert condition "message"
```

## 15. COLLECTION OPERATIONS

```fusion
# Creation
create a list called items with [1, 2, 3]
create a dict called user with {name: "Bob"}
instantiate a list called data
construct a dict called config
build a list called results
launch a list called workers
initiate a dict called settings
spin up a list called services
boot up a dict called config

# Copy / Clone
duplicate items
clone config
copy data
replicate template
mirror settings

# Delete / Destroy (so many ways!)
delete x         destroy x       annihilate x
obliterate x     tear down x     toss x
chuck x          ditch x         bin x
trash x          scrap x         junk x
nuke x           zap x           prune x

# Comprehensions
[x^2 for each x in items if x > 0]
{x: x*2 for each x in items where x > 0}
(k: v for each k, v in dict where v > 0)
(x*2 for each x in items where x > 2)

# Element access
first of list     last of list     rest of list
fetch first from list     retrieve last from list
obtain element from list  acquire item from collection

# Mutation
push value into list     insert value into list     stuff value into list     prepend value to list
pop from list            grab from list              pull from list             yank from list
extract from list        pluck from list
append value to list     attach value to list        tack on value to list
remove value from list   delete value from list      erase value from list
detach value from list   strip out value from list
discard value            throw away value            reject value               omit value
take 3 from list         drop 2 from list

# Transformation
reverse list   flip list   invert list   turn around list
sort list      arrange list   order list   rank list   organize list
clear list     purge list   wipe list   reset list   empty out list

# Info
length of list    size of list    count of list    number of list items
list is empty
x in items    x inside items    x within items    x among items
2 appears in items    5 exists in items    value belongs to list
x not in items    x outside items    x not within items
x does not appear in items    x does not exist in items    x is absent from list
```

## 16. NAMESPACES

```fusion
define namespace Math:
    define function sqrt with x:
        return x ^ 0.5
    define static function abs with x:
        return x if x >= 0 else -x
```

## 17. EXTENSION METHODS

```fusion
define extension on string:
    define function is_palindrome -> bool:
        return this == reverse this
    define function capitalize_words -> string:
        return join [capitalize w for each w in split this by " "] with " "
```

## 18. TYPE OPERATIONS

```fusion
typeof x                    # Get type of expression
x as int                    # Type casting
x is a string               # Type check
x is an integer             # Type check
x is not a list             # Negated type check
```

## 19. LAZY VARIABLES

```fusion
lazy let data be expensive_computation()
lazy let config: dict be load_config()
```

## 20. ADVANCED OPERATIONS

```fusion
# Swap
swap a and b

# Defer
defer: cleanup()
postpone: save_state()
schedule: backup()
```

## 21. ASYNC/AWAIT

```fusion
define async function fetch with url: ...
await promise()
for await each x in stream: ...
```

## 22. ENUMS & DECORATORS

```fusion
define enum Color: Red, Green, Blue
enum Status: Active, Inactive

@decorator
@decorator(args)
define function f: ...
```

## 23. REGEX LITERALS

```fusion
/pattern/flags
/^hello/i
/[a-z]+/g

text matches /regex/
```

## 24. SPREAD OPERATORS

```fusion
# ... (spread/rest)
define function sum_all with ...args: ...

# Partial application
let inc be add(_, 1)
```

## 25. MULTI-TARGET SYSTEM

### FusionBoa Syntax Mode
Write in FusionBoa English-like syntax for any target:
```fusionboa
// @target python
define function greet with name:
    print "Hello, " + name

// @target javascript
define function greet with name:
    print "Hello, " + name

// @target html
html lang "en":
    body: h1 "Hello!"

// @target json
{app: "FusionBoa", version: "0.7.0"}
```

### Native Passthrough Mode
Write directly in ANY target language's native syntax:
```fusion
// @raw python
def greet(name):
    print(f"Hello, {name}!")

// @native javascript
function greet(name) {
    console.log(`Hello, ${name}!`);
}

// @passthrough css
body { background: linear-gradient(135deg, #667eea, #764ba2); }

// @raw rust
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}
```

**All 23 targets support both modes!** Mix FusionBoa and native syntax freely in one file.

### Compilation Targets
**15 Languages:** Python, JavaScript, TypeScript, Ruby, Go, Rust, C++, Julia, R, Kotlin, Swift, Java, C#, Lua, React/JSX
**8 Formats:** HTML, CSS, JSON, YAML, TOML, XML, Markdown, INI

---

## 26. QUICK REFERENCE — ALL COMMANDS

```fusion
# === DECLARING VARIABLES (15+ ways!) ===
let x be 5        var x be 5        declare x be 5      make x be 5
set up x be 5     establish x be 5   start x be 5        begin x be 5
commence x be 5   initialize x be 5  configure x be 5
const PI be 3.14  constant X be 10   final X be 10      immutable X be 42
freeze X be 0     lock X be 0        seal X be 0
lazy let data be expr

# === ASSIGNING & MUTATING ===
set x to 10         assign x to 10      change x to 10        update x to 10
unlock x            release x
increase x by 5     increment x by 5    bump x by 5
decrease y by 2     decrement y by 2    reduce y by 2
x++  x--  ++x  --x
swap a and b        x ||= 10  x &&= false  x ??= "default"

# === TYPES ===
let x: int be 5     let x: string|int be ""    let x: int? be null
x as int            typeof x                   x is a string
int integer whole_number bits     float number decimal
string text character chars word sentence paragraph bytes symbol
bool boolean flag truth           list array collection sequence element elements entries
dict dictionary table hash mapping pairs keyed_list

# === CREATING COLLECTIONS (10+ ways!) ===
create a list called items        instantiate a list called data
construct a dict called config    build a list called results
launch a list called workers      initiate a dict called settings
spin up a list called services    boot up a dict called config
duplicate items                   clone config
copy data                         replicate template     mirror settings

# === DESTROYING (15+ ways!) ===
delete x    destroy x    annihilate x    obliterate x    tear down x
toss x      chuck x      ditch x         bin x           trash x
scrap x     junk x       nuke x          zap x           prune x

# === FUNCTIONS (20+ ways!) ===
define function f with a: ...         define func f with a: ...
define fn f with a: ...               define method f with a: ...
define procedure f with a: ...        define routine f with a: ...
define subroutine f with a: ...       define operation f with a: ...
define action f with a: ...           define handler f with a: ...
define callback f with a: ...         define listener f with a: ...
function with x: x * 2               # lambda

# === RETURNING (20+ ways!) ===
return x     give x     send back x     provide x     furnish x     supply x
produce x    respond with x     answer with x     hand back x
thank you    thanks    cheers    yay    woohoo    hooray
victory      success   accomplished   achieved   fulfilled   liberate

# === PRINTING (25+ ways!) ===
print x    display x    show x    say x    write x    output x    log x    echo x
emit x     tell x       announce x    report x    notify x    dump x
nice x     excellent x  awesome x     superb x    cool x      sweet x
neat x     brilliant x  fantastic x   wonderful x terrific x
inspect x  debug x      trace x       watch x

# === CLASSES & RECORDS ===
define class C: ...     define type T: ...        define struct S: ...
define class C<T>: ...  define class C implements I: ...
define class C inherits from P: ...  define class C extends P: ...
define record Point with x: int, y: int
define property name with get: ... set with value: ...
define namespace Math: ...
define extension on Type: ...

# === CONTROL FLOW (20+ ways for if!) ===
if x: ...     provided x: ...     given x: ...     supposing x: ...
in the event that x: ...     on the condition that x: ...
assuming x: ...     presuming x: ...     should x: ...
in the case that x: ...     whenever x: ...     before x: ...
or if y: ...  or: ...  unless x: ...  guard x else: ...
when x > 0 then "pos" or "neg"

# === LOOPS (25+ ways for for!) ===
for each x in items: ...    loop each x in items: ...
foreach x in items: ...     loop over x in items: ...
iterate over x in items: ...    going through x in items: ...
traversing x in items: ...      across x in items: ...
scanning through x in items: ...    looking at each x in items: ...
examining each x in items: ...      visiting each x in items: ...
touching each x in items: ...       processing each x in items: ...
walk x in items: ...                traverse x in items: ...
stroll through x in items: ...
for every single x in items: ...    for every one of items: ...
for i from 1 to 10: ...             for await each x in stream: ...
repeat 5 times: ...    while x: ...   whilst x: ...   as long as x: ...
until x: ...    do: ... while x
break | stop | exit | leave | quit | abort | halt | terminate
continue | skip | next | proceed | carry on | keep going | advance
pass | do nothing | nop

# === FUNCTIONAL OPERATIONS ===
map items using func       apply func to items      convert items using func
filter items where x > 5   keep items where valid   screen items where active
narrow down items where x>0   cull list where not x   sift data where x
strain items where x       winnow results where x
fold items using add starting with 0   accumulate items using sum
collect values using sum   gather data using merge   compile results using join
amass totals using add     summarize items using count
condense list using max    distill set using min     boil down items using x
combine items using merge              merge items
search needle in haystack   find key in database   look for item
query db for key            interrogate system     probe network
explore data                scan text               sweep array
replace old in text with new   substitute pattern in text
count occurrences of item in list
transform each x in items using square

# === ERROR HANDLING (25+ ways!) ===
try: ... catch error as e: ... finally: ...
attempt: ... rescue error as e: ... ensure: ...
try: ... trap error as e: ... always: ...
try: ... on error as e: ... cleanup: ...
raise | throw | panic | fail | crash "message"
oops "broke" | whoops "my bad" | uh oh "no" | yikes "bad"
alas "sad"  | oh no "bad"      | darn "dang" | shoot "miss"
rats "nuts" | bother "annoying"
assert condition "message"

# === IMPORTS & EXPORTS ===
use math   import math   include math   require math   load math
from math import sqrt
export | publish | expose | make public

# === COLLECTION OPS ===
length of x | size of x | count of x | number of x
first of x | last of x | rest of x
take 3 from x | drop 2 from x
push into x | pop from x | append to x | remove from x
reverse x | sort x | clear x | unique x | compact x
x in items | x inside items | x within items | x among items
x appears in items | x exists in items | x belongs to items
x is part of items | x is member of items | x is element of items
x not in items | x does not appear in items | x is absent from items
items has x | items holds x | items contains x

# === BOOLEAN VALUES (15+ ways for each!) ===
# True: true  yes  yup  yep  yeah  on  enabled  definitely  absolutely
#        certainly  surely  indeed  positively  affirmative
# False: false  no  nope  nah  off  disabled  negative  never  nada
# Null:  null  none  nothing  blank  undefined  absent  missing
#        maybe  perhaps  possibly

# === POLITE/CASUAL ===
please print x              # "please" is ignored
kindly let x be 5            # "kindly" is ignored

# === NATURAL ENGLISH (Parser ignores 'the') ===
let the x be 5               # "the" skipped
for each item in the list:   # reads like English!
    print the result         # natural flow
```

---

**FusionBoa Language v0.7.0**
*708 keywords · 228 token types · 500+ aliases · 23 compile targets · 200/200 tests*
