# FusionBoa Language — Complete Syntax Reference

**Version 0.9.0 "Insane Mode" — July 2026**

A polyglot programming language with English-like syntax. Write once, compile to 23 targets.
**725 keywords**, **228 token types**, **550+ syntax aliases**, **74+ language features**.

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
{app: "FusionBoa", version: "0.9.0"}
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

## 26. v0.9.0 FEATURE INDEX

Sections 1–25 cover all core language features. The 7 v0.8.0 "God Mode" paradigms are in §27–33. The 7 v0.9.0 "Insane Mode" advanced systems are in §35–41. Complete Quick Reference is at §42.

---

## 27. MULTIPLE DISPATCH (MULTI-METHODS)

Traditional OOP dispatches on the first argument (the caller) only. Multiple Dispatch checks the **runtime types of all arguments** to select the best matching function automatically — like Julia's core method system.

```fusion
define function collide with a: Warrior, b: Dragon:
    print "The warrior strikes the dragon with a sword!"

define function collide with a: Wizard, b: Dragon:
    print "The wizard casts a fireball at the dragon!"

define function collide with a: Warrior, b: Spell:
    print "The warrior deflects the spell with a shield!"

define function collide with a: Wizard, b: Spell:
    print "The wizard absorbs the magic into their staff!"

# Usage — the compiler picks the right one at runtime:
let hero be Warrior(name: "Arthur")
let enemy be Dragon(name: "Smaug")
collide hero with enemy        # → "The warrior strikes the dragon with a sword!"

let mage be Wizard(name: "Gandalf")
let curse be Spell(name: "Hex")
collide mage with curse        # → "The wizard absorbs the magic into their staff!"
```

**Cross-target compilation:**
| Target | Strategy |
|--------|----------|
| Python | `@singledispatch` + `@singledispatchmethod` or `multipledispatch` package |
| Julia | Native multiple dispatch — direct 1:1 mapping! |
| JavaScript/TS | Manual `typeof` dispatch table or visitor pattern |
| Java/C# | Visitor pattern or overloaded static methods with `instanceof` chains |
| C++ | Function overload resolution with `dynamic_cast` chains |
| Rust | Trait-based dispatch with `dyn` |

---

## 28. ASYNC STREAMS & GENERATOR YIELDING

Generators produce values **lazily**, one at a time, pausing their state between yields. Combined with `async`, they create asynchronous data streams that don't block execution.

```fusion
# Synchronous generator — yields values one at a time
define function stream_numbers -> generator:
    let counter be 0
    as long as counter < 100:
        increase counter by 1
        yield counter                     # Pauses state, returns value lazily

# Consuming a generator
for each num in stream_numbers():
    if num > 10:
        break                             # Only 11 iterations — never computes all 100
    print num

# Async generator — yields values asynchronously
define async function stream_events with url:
    let connection be connect to url
    as long as connection is alive:
        let event be await connection.read()
        yield event                       # Async yield — non-blocking!

# Consuming async streams
for await each event in stream_events("wss://api.example.com"):
    print "Received: " + event
```

**Generator expressions (lazy comprehensions):**
```fusion
let squares be (x * x for each x in 1 to 10)    # Generator, not list
let evens be (x for each x in items where x % 2 == 0)
```

**Cross-target compilation:**
| Target | Strategy |
|--------|----------|
| Python | `yield` keyword — native 1:1 mapping |
| JavaScript | `function*` + `yield` (sync) / `async function*` + `yield` (async) |
| C# | `yield return` with `IEnumerable<T>` / `IAsyncEnumerable<T>` |
| Ruby | `yield` / `Enumerator` |
| Go | Channel + goroutine (generates a channel, sends values in goroutine) |
| Rust | `impl Iterator<Item=T>` / `async_stream` crate |

---

## 29. FLOW-SENSITIVE REFINEMENT TYPING

TypeScript/Kotlin-style smart type narrowing. Once you check a variable's type or nullability, the compiler **automatically refines** its type inside that block — no redundant casts needed.

```fusion
let user_name: string | null be get_input()

# After this check, user_name is refined to just 'string'
if user_name is not null:
    # Compiler guarantees user_name is string inside this block!
    print user_name upper                 # Safe — no null error
    let length be length of user_name     # Safe

# Similarly for type checks
let value: int | string | list be get_value()

if value is a string:
    print value upper                      # Refined: only string methods available
    print length of value                  # Safe
or if value is an int:
    print value + 10                       # Refined: only int operations
or:
    print first of value                   # Refined: must be list

# Negated refinement
if value is not a list:
    let str_val be value as string         # Safe — must be string|int

# Refinement with guard
let data: dict | null be load_config()
guard data is not null else:
    return "No config found"
# After guard, data is refined to dict everywhere below
print data["key"]                          # Safe
```

**Advanced narrowing patterns:**
```fusion
# Discriminated unions with record types
define record Success<T> with value: T
define record Failure with error: string
type Result<T> be Success<T> | Failure

let result: Result<int> be do_something()
whenever result is a Success:
    print "Got: " + result.value           # Refined — value property accessible
or:
    print "Error: " + result.error         # Refined — error property accessible

# Array filtering refinement
let items: list of int? be [1, null, 3, null, 5]
filter items where x is not null:
    # Inside filter, x is refined to int
    print x * 2
```

---

## 30. UNIFORM FUNCTION CALL SYNTAX (UFCS)

Any function can be called as if it were a **method on its first argument**. This eliminates the friction between free-standing functions and object methods — like Nim, D, and Rust's method syntax.

```fusion
define function calculate_tax with amount: float -> float:
    return amount * 0.12

define function double with value: int -> int:
    return value * 2

define function greet with name: string -> string:
    return "Hello, " + name

# ALL of these pairs evaluate identically!
let choice_a be calculate_tax(100)          # Traditional call
let choice_b be 100.calculate_tax()          # UFCS — method-style

let a be double(21)                          # Traditional
let b be 21.double()                         # UFCS

let msg1 be greet("Alice")                   # Traditional
let msg2 be "Alice".greet()                  # UFCS

# Chaining with UFCS (pipeline style!)
let result be 100
    .calculate_tax()                         # 12.0
    .double()                                # 24.0

# Works with any type, anywhere
let numbers be [1, 2, 3, 4, 5]
let evens be numbers.filter(x > 2).map(x * 2)
let total be numbers.fold(add).first()
```

**Cross-target compilation:**
| Target | Strategy |
|--------|----------|
| All targets | UFCS is a source-to-source transform: `x.f(args)` → `f(x, args)`. The compiler rewrites before emitting target code. Works universally. |
| Rust | Maps naturally to method syntax (`impl` blocks or free functions called as methods) |
| D / Nim | Native language feature — direct 1:1 |
| C++ | ADL (Argument-Dependent Lookup) provides partial native support |

---

## 31. COMPILE-TIME MACROS (METAPROGRAMMING)

Code that writes code. Macros execute **inside the compiler** at compile time to generate boilerplate, derive traits, or create domain-specific syntax — like Lisp macros, Rust `macro_rules!`, or C++ templates.

```fusion
# Simple macro — generates getter methods for a record
macro create_getters for Point:
    generate:
        define function get_x -> int:
            return this.x
        define function get_y -> int:
            return this.y

# Usage — expands at compile time to the generated methods
define record Point with x: int, y: int
create_getters for Point                     # Injects get_x() and get_y()

let p be Point(x: 10, y: 20)
print p.get_x()                              # 10
```

**Advanced macro with AST inspection:**
```fusion
# Macro that inspects the target type and generates serialization code
macro auto_serialize for T:
    # $fields is a compile-time list of the record's field names
    generate:
        define function to_json -> string:
            let parts be []
            for each field in $fields:       # Compile-time loop!
                push into parts: "\"" + field + "\": " + string(this[field])
            return "{" + join parts with ", " + "}"
        
        define function from_json with data: string -> T:
            # Generated per-type at compile time
            ...

define record User with name: string, age: int, email: string
auto_serialize for User                      # Generates to_json() and from_json()

let user be User(name: "Alice", age: 30, email: "alice@example.com")
print user.to_json()                         # {"name": "Alice", "age": 30, "email": "alice@example.com"}
```

**Attribute-style macros (decorator-like):**
```fusion
@derive(Serialize, Deserialize)
define record Point with x: int, y: int

@measure_time
define function expensive_computation:
    # Compiler wraps this in timing instrumentation
    ...

@memoize(cache_size: 256)
define function fib with n: int -> int:
    return fib(n-1) + fib(n-2) if n > 1 else n
```

---

## 32. OPERATOR OVERLOADING

Give native math symbols (+, -, *, /, ==, <, etc.) custom behavior for your own types — like C++ operator overloading or Python's `__add__`/`__mul__` magic methods.

```fusion
define record Point with x: int, y: int

# Define custom + operator for Point
define operator + with a: Point, b: Point -> Point:
    return Point(x: a.x + b.x, y: a.y + b.y)

# Define custom - operator for Point
define operator - with a: Point, b: Point -> Point:
    return Point(x: a.x - b.x, y: a.y - b.y)

# Define custom * (scalar multiplication)
define operator * with a: Point, s: int -> Point:
    return Point(x: a.x * s, y: a.y * s)

# Define comparison
define operator == with a: Point, b: Point -> bool:
    return a.x == b.x and a.y == b.y

define operator < with a: Point, b: Point -> bool:
    return (a.x * a.x + a.y * a.y) < (b.x * b.x + b.y * b.y)

# Natural usage!
let p1 be Point(x: 1, y: 2)
let p2 be Point(x: 3, y: 4)
let sum be p1 + p2                           # Point(x: 4, y: 6)
let diff be p2 - p1                          # Point(x: 2, y: 2)
let scaled be p1 * 5                         # Point(x: 5, y: 10)

if p1 < p2:
    print "p1 is closer to origin"
```

**Overloadable operators:**
```fusion
# Arithmetic:   +  -  *  /  //  %  ^  **
# Comparison:   ==  !=  <  >  <=  >=
# Unary:        - (negate)  ~ (bitwise not)
# Index:        [] (subscript get/set)
# Call:         () (callable objects)
# Conversion:   as (type conversion)

# Index operator overload
define operator [] with self: Vector, index: int -> int:
    return self.data[index]

define operator []= with self: Vector, index: int, value: int:
    set self.data[index] to value

# Call operator (functors)
define operator () with self: Multiplier, x: int -> int:
    return self.factor * x

let mul be Multiplier(factor: 10)
print mul(5)                                 # 50 — called like a function!
```

**Cross-target compilation:**
| Target | Strategy |
|--------|----------|
| Python | `__add__`, `__mul__`, `__eq__`, `__lt__`, `__getitem__`, `__setitem__`, `__call__` |
| C++ | `operator+`, `operator*`, `operator==`, `operator<`, `operator[]`, `operator()` |
| C# | `operator +`, `operator *`, `operator ==`, `operator <` |
| Rust | `std::ops::Add`, `Mul`, `PartialEq`, `PartialOrd`, `Index`, `IndexMut`, `Fn` |
| Kotlin | `plus`, `times`, `compareTo`, `get`, `set`, `invoke` |
| Swift | `static func +`, `static func ==`, `subscript`, `@dynamicCallable` |
| Ruby | `+`, `*`, `==`, `<`, `[]`, `[]=`, `call` |
| Java | Manual interface (Java has no operator overloading) — generates `plus()`, `times()`, etc. |
| Go | Manual methods only (Go has no operator overloading) — generates `Add()`, `Mul()`, etc. |

---

## 33. CONCURRENCY CHANNELS (GO-STYLE ROUTINES)

Lightweight concurrent tasks (green threads) communicating through **typed channels** — safe, lock-free message passing. Channels guarantee no shared-memory race conditions.

```fusion
# Create a typed channel
let messages be create channel of string      # Channel that carries strings
let results be create channel of int          # Channel that carries ints
let events be create channel of dict          # Channel that carries dicts

# Launch a background worker (lightweight thread)
spin up background_worker:
    for i from 1 to 10:
        send "Message #" + string(i) through messages
    close messages                             # Signal: no more messages

# Launch another worker
spin up processor:
    as long as messages is open:
        listen to messages with msg:
            let upper_msg be msg.upper()
            send upper_msg through results
    close results

# Main thread — receive results
listen to results with result:
    print result
# Prints: MESSAGE #1, MESSAGE #2, ..., MESSAGE #10
```

**Channel patterns:**
```fusion
# Buffered channels (don't block until buffer is full)
let pipeline be create channel of int with capacity 100

# Select / multiplex (wait on multiple channels)
select:
    case msg from channel_a:
        print "From A: " + msg
    case msg from channel_b:
        print "From B: " + msg
    case after 5 seconds:
        print "Timed out!"
    default:
        print "Nothing ready yet"

# Fan-out (one producer → many consumers)
spin up producer:
    for each item in data:
        send item through work_queue
    close work_queue

for i from 1 to 4:                             # Launch 4 workers
    spin up worker + string(i):
        listen to work_queue with task:
            process task

# Fan-in (many producers → one consumer)
let merged be create channel of string
spin up source_a: ... send through merged ...
spin up source_b: ... send through merged ...
spin up source_c: ... send through merged ...

# Consumer reads from all sources
listen to merged with data:
    print "Received: " + data

# Atomic counters and shared state (when needed)
let counter be create shared int starting at 0

spin up incrementer:
    repeat 1000 times:
        atomically increase counter by 1      # Thread-safe
```

**Cross-target compilation:**
| Target | Strategy |
|--------|----------|
| Go | **Native goroutines + channels** — direct 1:1 mapping! `spin up` → `go func()`, `send through` → `ch <-`, `listen to` → `<-ch`, `select` → `select` |
| Python | `asyncio.Queue` + `asyncio.create_task()` for async channels; `threading.Thread` + `queue.Queue` for sync |
| JavaScript | `Promise` + async generators for async; `Worker` threads for true parallelism |
| Kotlin | `kotlinx.coroutines` + `Channel<T>` — very close to native |
| Rust | `tokio::spawn` + `tokio::sync::mpsc::channel` or `std::sync::mpsc` |
| C# | `Task.Run` + `System.Threading.Channels.Channel<T>` |
| Java | `CompletableFuture` + `java.util.concurrent.BlockingQueue` |
| C++ | `std::async` + thread-safe queues, or `boost::fiber` for lightweight |

---

## 34. v0.9.0 IMPLEMENTATION NOTES

These advanced systems (§35–41) are **forward-looking specifications**. The following keywords will need new token types and parser support before they can be compiled:

| Keyword | Current tokens.py status | Risk |
|---------|--------------------------|------|
| `lifetime` | ❌ Not in tokens.py | Safe — new token needed |
| `relinquish` | ❌ Not in tokens.py | Safe — new token needed |
| `ownership` | ❌ Not in tokens.py | Safe — new token needed |
| `borrow` | ❌ Not in tokens.py | Safe — new token needed |
| `location` | ❌ Not in tokens.py | Safe — new token needed |
| `offset` | ❌ Not in tokens.py | Safe — new token needed |
| `assembly` | ❌ Not in tokens.py | Safe — new token needed |
| `interrogate` | ⚠️ Maps to `SEARCH` | **COLLISION** — needs new `REFLECT` token or contextual parser disambiguation |
| `mapping` | ❌ Not in tokens.py | Safe — new token needed |
| `bidirectional` | ❌ Not in tokens.py | Safe — new token needed |
| `detach` | ❌ Not in tokens.py | Safe — new token needed |
| `suspend` | ❌ Not in tokens.py | Safe — new token needed |
| `structural` | ❌ Not in tokens.py | Safe — new token needed |
| `factory` | ⚠️ Maps to `FUNCTION` | Low risk — contextual ("structural factory" vs standalone) |
| `transmit` | ❌ Not in tokens.py | Safe — new token needed |
| `capturing` | ❌ Not in tokens.py | Safe — new token needed |
| `read_only` | ❌ Not in tokens.py | Safe — multi-word token needed |
| `creation` | ❌ Not in tokens.py | Safe — new token needed |

> **Note:** `interrogate` currently maps to `TokenType.SEARCH` (used for natural search like "query database"). For reflection-style "interrogate layout of...", a new `TokenType.REFLECT` or parser-level disambiguation is required. Similarly, `any` in §41's `any child_class` collides with `TokenType.ANY`. These are documented here for the implementation phase.

---

## 35. MEMORY TRACKING & MANAGEMENT (RUST BORROW CHECKER TARGET)

FusionBoa introduces explicit scope tracking and ownership handshakes to support deterministic memory safety without a runtime garbage collector. These compile down to Rust's borrow checker, C++ RAII, or manual memory management in C.

```fusion
# Establish an explicit memory boundary scope tag
with lifetime 'a:
    let message be "System Active"
    # message is valid only within this scope

# Formally hand over ownership of data to a separate execution sequence
let system_log be "Boot sequence complete"
relinquish ownership of system_log to monitor_process
# system_log is now invalid — compiler enforces this!

# Borrow data read-only without taking permanent ownership
let data_stream be open_sensor_port()
borrow read_only data_stream as stream_view
# stream_view can read, but cannot modify or delete
# data_stream retains ownership
```

**Ownership rules enforced at compile time:**
```fusion
# Move semantics: ownership transfers
let original be "Hello"
let moved be original                    # ownership moves
# print original                          # COMPILE ERROR: original was moved

# Borrow: multiple readers, no writers
let shared_data be [1, 2, 3]
borrow read_only shared_data as view_a
borrow read_only shared_data as view_b    # OK: multiple readers allowed
# borrow mutable shared_data as edit     # COMPILE ERROR: can't write while reading

# Lifetime annotations for complex scopes
with lifetime 'scope:
    let resource be allocate_buffer(1024)
    relinquish ownership of resource to cleanup_handler
    # Guaranteed: resource freed exactly once
```

**Cross-target compilation:**
| Target | Strategy |
|--------|----------|
| Rust | Native borrow checker — `&'a T`, `Box<T>`, `Rc<T>`, `Arc<T>`, `move` semantics |
| C++ | `std::unique_ptr<T>`, `std::shared_ptr<T>`, `const T&`, `std::move` |
| Go | GC simplifies — ownership annotations become no-ops; `borrow` → pointer copy |
| Python/JS | Ownership is documentation-only; all objects are reference-counted/GC'd |
| C | `malloc`/`free` with compile-time lifetime verification, `const T*` for borrow |

---

## 36. HARDWARE INTEGRATION & ADDRESSING (C++ NATIVE POINTER TARGET)

Provides direct memory location lookups and low-level execution for raw high-performance embedded systems logic. These primitives map to C/C++ pointer arithmetic, inline assembly, and memory-mapped I/O.

```fusion
# Locate the precise physical hardware memory address of a variable
let core_variable be 0x7FFF_4000
let memory_lock be location of core_variable
# memory_lock now holds the raw numerical address

# Direct hardware memory manipulation via numerical offset pointers
let device_base be location of hardware_register
set value at location device_base with offset 4 to 0xFF
# Writes 0xFF to address (device_base + 4)

# Read from a specific memory address
let sensor_value be value at location device_base with offset 8
# Reads from address (device_base + 8)

# Inject inline raw assembly commands straight to the physical microprocessor
execute assembly:
    "MOV RAX, 60"
    "MOV RDI, 0"
    "SYSCALL"
# Direct assembly — zero abstraction overhead
```

**Pointer safety modes:**
```fusion
# Safe mode (default): pointers are checked, bounds-verified
with safe pointers:
    let addr be location of buffer
    set value at location addr to 42       # Bounds-checked

# Unsafe mode: raw access, no checks — for embedded/kernel code
with unsafe memory:
    let raw_ptr be location of mmio_base
    set value at location raw_ptr with offset 0x1000 to 0xDEAD
    execute assembly: "CLI"                # Disable interrupts
    execute assembly: "HLT"                # Halt CPU
```

**Cross-target compilation:**
| Target | Strategy |
|--------|----------|
| C++ | `&var`, `uintptr_t`, `reinterpret_cast<T*>`, `__asm__ __volatile__`, placement new |
| C | `&var`, `uintptr_t`, pointer arithmetic, `asm()` with GCC/Clang inline asm |
| Rust | `unsafe { ptr::addr_of!(var) }`, `core::ptr::write()`, `asm!()` macro |
| Go | `unsafe.Pointer`, `uintptr`, assembly via `.s` files (limited) |
| Python | `ctypes.c_void_p`, `ctypes.memmove` (very limited, requires FFI) |
| JS/Java/C# | No native pointer support — compile error or `Unsafe`/`sun.misc.Unsafe` wrapper |

> **⚠️ Warning:** Hardware addressing and assembly features are **target-gated**. Compiling to non-C/C++/Rust targets with these features will produce compile-time errors or explicit stubs.

---

## 37. DYNAMIC TYPE STRUCTURING (TYPESCRIPT MAPPED TYPES TARGET)

Enables type configurations to evaluate, loop through, and modify existing data structures during the compiler's semantic checking phase — like TypeScript's mapped types and conditional types.

```fusion
# Crawl an existing record layout and dynamically make all its fields read-only
define record UserRecord with name: string, age: int, email: string

define type ImmutableUser by mapping fields of UserRecord to be constant
# ImmutableUser = { readonly name: string, readonly age: int, readonly email: string }

# Build a conditional type evaluation blueprint
define type NetworkResponse be when Data matches ErrorState then FailedState or SuccessState

# Map fields to optional
let partial_user be mapping fields of UserRecord to be optional
# { name?: string, age?: int, email?: string }

# Transform field types
let stringified_user be mapping fields of UserRecord converting each to string
# { name: string, age: string, email: string }

# Pick specific fields from a type
define type UserPreview be pick name, email from UserRecord
# { name: string, email: string }

# Omit specific fields
define type UserSafe be omit password, token from UserRecord
```

**Cross-target compilation:**
| Target | Strategy |
|--------|----------|
| TypeScript | Native mapped types: `type T = { [K in keyof U]: ... }`, conditional types, `Pick<T>`, `Omit<T>`, `Partial<T>`, `Readonly<T>` |
| Python | `typing.TypedDict` + decorators for read-only, `dataclass(frozen=True)`, `Protocol` |
| Kotlin | Inline classes, type aliases, sealed interfaces with smart derivation |
| C++ | `using` aliases, template metaprogramming with `std::conditional_t`, `std::enable_if_t` |
| Rust | `type` aliases, `PhantomData`, trait bounds, derive macros for field transformation |
| Go | Struct embedding + code generation (Go lacks mapped types) |
| Java | Annotation processing + code generation (Java lacks mapped types) |

---

## 38. RUNTIME SYSTEM INSPECTION (JAVA REFLECTION TARGET)

Allows an actively running application to programmatically analyze its own architecture and discover hidden structures dynamically — like Java reflection or Python's `inspect` module.

```fusion
# Programmatically inspect an object's structural blueprint at runtime
let active_session be Session(id: 42, user: "Alice")
interrogate layout of active_session capturing fields_list
# fields_list = ["id", "user"]

# Inspect methods available on an object
interrogate methods of active_session capturing methods_list
# methods_list = ["init", "get_id", "set_id", "get_user", ...]

# Invoke a method dynamically by looking up its text string name
let dynamic_suffix be "_backup"
execute method named "calculate" + dynamic_suffix on user_profile using system_context
# Calls user_profile.calculate_backup(system_context) at runtime

# Check if a method exists before calling
if active_session responds to "validate":
    execute method named "validate" on active_session

# Get/set fields by name dynamically
let field_value be value of "email" from user_record
set field "email" on user_record to "new@example.com"
```

**Cross-target compilation:**
| Target | Strategy |
|--------|----------|
| Java | Native reflection: `Class<?>`, `getDeclaredFields()`, `getDeclaredMethods()`, `Method.invoke()` |
| Python | `getattr()`, `setattr()`, `hasattr()`, `inspect.getmembers()`, `dir()` — very natural |
| JavaScript | `Object.keys()`, `obj[methodName]()`, `Reflect.get()`, `Reflect.set()`, `Proxy` |
| C# | `System.Reflection`: `typeof(T).GetFields()`, `GetMethod()`, `MethodInfo.Invoke()` |
| Kotlin | Kotlin reflection: `KClass`, `memberProperties`, `call()`, `callBy()` |
| Go | `reflect` package: `reflect.TypeOf()`, `reflect.ValueOf()`, `FieldByName()` |
| Rust | Limited — `std::any::TypeId`, `Any` trait for downcast; full reflection requires proc macros |
| C++ | Limited — RTTI with `typeid`, `dynamic_cast`; full reflection requires code generation |

---

## 39. HARDWARE CONCURRENCY MANAGEMENT (GO CHANNELS TARGET)

Provides native synchronization logic for fast, lightweight hardware threads communicating via memory paths. Extends the existing channel primitives (section 33) with bidirectional channels, detached tasks, and hardware-aware scheduling.

```fusion
# Allocate a dedicated, synchronized communication pipeline
let system_channel be create bidirectional channel of message
# Bidirectional: both ends can send AND receive

# Spin up a lightweight thread that monitors data streams in the background
detach async task using data_feed:
    transmit "Data Received" onto system_channel
    # Task runs independently — won't block main thread

# Attach a timeout to channel operations
listen to system_channel with msg within 100 milliseconds:
    process msg
or timeout:
    handle_missed_message()

# Priority channels (hardware interrupt level)
let urgent_signals be create high priority channel of signal

spin up interrupt_handler:
    listen to urgent_signals with signal:
        execute assembly: "STI"            # Re-enable interrupts after handling

# Direct thread affinity (pin goroutine/thread to CPU core)
spin up cpu_worker pinned to core 3:
    # This thread runs exclusively on CPU core 3
    ...
```

**Cross-target compilation:**
| Target | Strategy |
|--------|----------|
| Go | `chan T` (bidirectional), `go func()`, `select` with `time.After()`, no native core pinning |
| Rust | `tokio::spawn`, `tokio::sync::broadcast` (bidirectional), `core_affinity` crate for pinning |
| C++ | `std::thread` + `std::sync::mpsc::channel`, `std::thread::hardware_concurrency()`, CPU affinity via OS |
| C | `pthread_create`, `pthread_setaffinity_np`, POSIX message queues |
| Python | `asyncio.Queue`, `threading.Thread`, `multiprocessing.Pipe` (bidirectional), `os.sched_setaffinity` |
| Kotlin | `kotlinx.coroutines`, `Channel<T>` (bidirectional), `newFixedThreadPoolContext` |

---

## 40. HYDRATION STATE HOOKS (REACT CONCURRENT ENGINE TARGET)

Coordinates asynchronous user interface components by freezing template rendering until external data resources load safely — like React Suspense, Vue's async components, or Svelte's await blocks.

```fusion
# Instruct the interface layer to hold rendering until a data stream is loaded
suspend interface rendering using api_stream:
    render component UserDashboard with user_data

# Multiple suspense boundaries
suspend interface rendering using profile_stream:
    render component ProfileCard with profile
or fallback:
    render component LoadingSpinner

# Nested suspension with independent loading states
suspend interface rendering using header_stream:
    render component PageHeader with header_data

suspend interface rendering using body_stream:
    render component ContentBody with articles
or fallback:
    render component SkeletonPlaceholder

# Stream data in progressively (React Server Components style)
suspend interface streaming using data_feed:
    on each chunk:
        render component LiveChart updating with chunk
    on complete:
        render component SummaryView with full_dataset
```

**Cross-target compilation:**
| Target | Strategy |
|--------|----------|
| React/JSX | `<Suspense fallback={<Spinner />}>`, React.lazy(), React Server Components, streaming SSR |
| Vue | `<Suspense>`, `defineAsyncComponent()`, `<template #fallback>` |
| Svelte | `{#await promise}...{:then value}...{:catch error}...{/await}` |
| Angular | `@defer` blocks, `@loading`, `@placeholder`, `@error` templates |
| SwiftUI | `AsyncImage`, `.task {}` modifier, `ProgressView` |
| Flutter | `FutureBuilder`, `StreamBuilder`, `AsyncSnapshot` |
| Non-UI targets | Suspense/hydration becomes no-ops — generated as direct assignment or ignored |

---

## 41. META-FACTORY GENERATION (PYTHON METACLASS TARGET)

Allows developers to write master blueprints that intercept and modify how standard class objects are created across a project — like Python metaclasses, Ruby's method_missing, or JavaScript Proxy construct traps.

```fusion
# Define a master class-factory controller hook
define structural factory CoreModel:
    before creation of any child_class:
        automatically append field creation_timestamp: int

# Any class that uses CoreModel gets the timestamp automatically
define class User is built by CoreModel:
    fields: name: string, age: int
# User automatically has: name, age, creation_timestamp

# Lifecycle hooks
define structural factory AuditedModel:
    before creation of any child_class:
        automatically append field created_at: datetime
        automatically append field updated_at: datetime
    
    on access to any field:
        log "Field {field_name} was read"
    
    on mutation of any field:
        update this.updated_at to current_time()
    
    after destruction:
        log "Record {this.id} was deleted"

# Attribute validation at class creation time
define structural factory ValidatedModel:
    before creation of any child_class:
        for each field in child_class.fields:
            if field has no default and field is not optional:
                error "Field {field.name} must have a default value"

# Singleton factory pattern
define structural factory Singleton:
    before creation:
        if Singleton._instance exists:
            return Singleton._instance
    after creation:
        store this in Singleton._instance
```

**Cross-target compilation:**
| Target | Strategy |
|--------|----------|
| Python | `type.__new__`, `__init_subclass__`, `__set_name__`, `@dataclass(frozen=True)`, metaclass hooks |
| JavaScript | `Proxy` with `construct` trap, `Object.defineProperty()`, class decorators (TC39 stage 3) |
| Ruby | `method_missing`, `define_method`, `included`/`extended` hooks, `Class.new` with block |
| Kotlin | Delegated properties (`by lazy`, `Delegates.observable`), `companion object`, inline functions |
| Swift | Property wrappers (`@propertyWrapper`), `willSet`/`didSet` observers, `@dynamicMemberLookup` |
| Rust | Proc macros (`#[derive(...)]`), custom `#[attribute]` macros — compile-time factory |
| C++ | CRTP (Curiously Recurring Template Pattern), `std::enable_if`, template metaprogramming |
| Java | Annotation processing (APT), `java.lang.reflect.Proxy`, bytecode manipulation (ASM, ByteBuddy) |
| Go | Code generation with `go:generate`, struct embedding (Go has no metaclasses) |

---

## 42. QUICK REFERENCE — ALL COMMANDS

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

# === v0.9.0 ADVANCED SYSTEMS (7 new subsystems!) ===

# -- Memory Management (Rust borrow checker) --
with lifetime 'a: ...                    # Scope-bound lifetime annotation
relinquish ownership of x to y          # Move semantics
borrow read_only data as view          # Immutable borrow

# -- Hardware Integration (C++ pointers) --
let addr be location of variable        # Get raw memory address
set value at location addr with offset 4 to 0xFF
read value at location addr with offset 8
execute assembly: "MOV RAX, 60"         # Inline assembly
with unsafe memory: ...                 # Unsafe pointer block

# -- Dynamic Type Structuring (TS mapped types) --
define type T by mapping fields of U to be constant
define type T be when A matches B then C or D
pick name, email from UserRecord       # Pick<T>
omit password from UserRecord          # Omit<T>

# -- Runtime Inspection (Java reflection) --
interrogate layout of obj capturing fields   # Get field names
execute method named "x" on obj using ctx    # Dynamic dispatch
if obj responds to "method": ...            # Duck-type check

# -- Hardware Concurrency (Go channels extended) --
let ch be create bidirectional channel of T   # Two-way channel
detach async task using feed: ...            # Detached goroutine
spin up worker pinned to core 3: ...         # CPU affinity

# -- Hydration State Hooks (React Suspense) --
suspend interface rendering using stream:     # Lazy loading
    render component Card with data
or fallback: render component Spinner

# -- Meta-Factory Generation (Python metaclass) --
define structural factory CoreModel:          # Metaclass
define class User is built by CoreModel: ...  # Factory-built class

# === v0.8.0 GOD MODE (7 paradigms!) ===

# -- Multiple Dispatch --
define function collide with a: Warrior, b: Dragon: ...
define function collide with a: Wizard, b: Spell: ...
collide hero with enemy           # Compiler picks based on ALL argument types

# -- Generators & Yielding --
define function stream -> generator:    yield value
define async function events:           yield await data
for await each x in stream: ...

# -- Flow-Sensitive Typing --
if x is not null: ...              # x refined to non-null in block
if x is a string: ...              # x refined to string in block
guard data is not null else: ...   # data refined globally after guard

# -- UFCS (Uniform Function Call Syntax) --
100.calculate_tax()                # Same as calculate_tax(100)
"Alice".greet()                    # Same as greet("Alice")
numbers.filter(x>2).map(x*2)      # Chain any function as method

# -- Compile-Time Macros --
macro getters for Point:           # Code that generates code
    generate: define function get_x ...
@derive(Serialize)                 # Attribute-style macro
define record User with name: string, age: int

# -- Operator Overloading --
define operator + with a: Point, b: Point -> Point: ...
define operator [] with self: Vector, index: int -> int: ...
define operator () with self: Fn, x: int -> int: ...  # Callable objects

# -- Concurrency Channels --
let ch be create channel of string              # Typed channel
spin up worker: ... send msg through ch ...    # Goroutine
listen to ch with msg: ...                      # Receive
select: case msg from ch_a: ... case after 5s: ...

# === NATURAL ENGLISH (Parser ignores 'the') ===
let the x be 5               # "the" skipped
for each item in the list:   # reads like English!
    print the result         # natural flow
```

---

**FusionBoa Language v0.9.0**
*725 keywords · 228 token types · 550+ aliases · 23 compile targets · 207/207 tests*
