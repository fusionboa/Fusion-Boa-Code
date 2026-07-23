# Changelog

All notable changes to FusionBoa will be documented in this file.

## [v0.9.7] — 2026-07-23

### Added
- Professional error handling system (FusionBoaError base class with line/col/severity/hint)
- Pretty-printed errors with source context, ^ pointers, and fix hints
- --debug flag for full traceback visibility
- Keyword misspelling suggestions (whlie -> while, functoin -> function, etc.)
- Clean KeyboardInterrupt handling (no traceback)

### Changed
- VERSION now reads consistently across fusionboa.py, README, pyproject.toml, setup.py
- All error paths produce clean messages instead of cryptic tracebacks
- LexerError and ParseError properly wrapped before display

### Fixed
- LexerError crash in format_error_for_cli (missing severity/hint attributes)
- --debug flag now works after subcommand (not just before)
- CLI VERSION hardcoded to 1.0.0-alpha fixed to 0.9.7

## [v0.9.6] — 2026-07-23

### Added
- Real v0.9.1 codegen for JavaScript, TypeScript, and Go (sets, tuples, multi-return, yield-from, goroutines, channels, select, mixins, objects, actors, sealed classes, synchronized blocks, async-with)
- Go: native goroutine/channel support — `go func()`, `make(chan)`, `ch <- x`, `<-ch`, `select {}`, `close(ch)`
- Go: conditional time import for channel select timeout
- CI linting step (mypy + compileall) in GitHub Actions
- Integration test suite (17 tests: py, js, ts, go end-to-end)
- Type checker test suite (10 tests: inference, compatibility, records)

### Changed
- SetLiteral/TupleLiteral now properly handled in `_gen_expression` (not just `_gen_statement`)
- Updated all metadata to v0.9.6: 902 keywords, 318 token types, 90+ features, 232 tests

### Fixed
- MixinStatement uses correct field names (mixin_name/mixin_type)
- Removed duplicate SetLiteral/TupleLiteral from gen_map (expression nodes only)
- Go generate() method properly constructs package/import structure

## [v0.9.2] — 2026-07-23

### Changed
- Updated all metadata: 902 keywords, 318 token types, 90+ features
- Updated README, pyproject.toml, setup.py with accurate counts and v0.9.2 version
- Removed 15 clutter files from repository

## [v0.9.1] — 2026-07-23

### Added
- **65+ new token types**: Go concurrency (goroutines, channels, select, fan-out/in), Rust ownership (borrow, lifetime, mutable borrow, unsafe), C++ pointers (reference, address-of, dereference, new/delete, virtual, abstract), Ruby (module, mixin, symbol, block), Kotlin (object, companion, sealed, data class, lateinit, suspend), Swift (actor, subscript, protocol), TypeScript (type alias, keyof, infer, conditional type), Julia (broadcast, macro), R (vectorize, formula), C# (delegate, event, partial class), Java (package, synchronized, volatile, annotation), plus sets, tuples, multi-return, yield-from, global, nonlocal, async-with, native/FFI
- **45+ new AST nodes**: SetLiteral, TupleLiteral, GoStatement, ChannelDeclaration, ChannelSend, ChannelReceive, ChannelSelect, ChannelClose, OwnershipTransfer, BorrowExpression, LifetimeAnnotation, AddressOfExpression, DereferenceExpression, MultiReturnStatement, YieldFromStatement, GlobalStatement, NonlocalStatement, AsyncWithStatement, ModuleDefinition, MixinStatement, ObjectDefinition, SealedClassDefinition, ActorDefinition, TypeAliasDefinition, BroadcastExpression, MacroDefinition, VectorizeExpression, and more
- **25+ new parser methods**: Full parsing for all new syntax with English-like multi-word keyword support
- **250+ English-like keyword aliases**: goroutine → "spin up", "launch", "spawn", "fork"; channel → "typed pipe", "message queue"; send → "transmit", "pass through" etc.
- Python codegen for all new AST nodes (sets with set(), goroutines with threading.Thread, channels with queue.Queue, ownership as doc comments)

### Fixed
- Removed duplicate `_parse_class_definition` (dead code from v0.5.0)
- Removed dead `elif` in `_parse_channel_select` (IDENTIFIER check for "from" which is always FROM token)
- Fixed keyword collisions: "set", "include", "go", "new", "free", "event", "symbol", "block", "object", "actor", "macro", "protocol" changed to multi-word forms to avoid clashing with variable names
- Fixed duplicate NONLOCAL and DROP tokens

## [1.0.0-alpha] — 2026-07-21

### Added
- All 23 compilation targets in a single `.fusboa` file via `// @target` annotations
- `tests/complete_test_runner.py` — validates all 23 codegen backends
- Build output now goes to a timestamped folder on the Desktop (`~/Desktop/fusionboa-*`)
- Cross-platform Desktop path resolution (Windows, macOS, Linux)
- `CHANGELOG.md` — project changelog

### Changed
- Renamed all "Apex" references to "FusionBoa" across examples, docs, and tests
- Updated `fusionboa.py` build command for cleaner output with file locations
- Updated install scripts with proper pip install and dependency management
- README badges now point to actual GitHub repo and CI workflow
- Fixed license metadata in `setup.py` (MIT → Proprietary)

### Fixed
- License inconsistency between `setup.py` and `LICENSE` file
- GitHub URL in `setup.py` pointing to wrong repository
- `.gitignore` now excludes generated build outputs and IDE files
- Version badge in README now matches actual version (`1.0.0-alpha`)

## [0.7.0] — 2026-07-01

### Added
- 725 keywords, 228 token types, 550+ syntax aliases
- 23 compile targets (15 programming languages + 8 markup/data formats)
- Complete English-like syntax reference (`COMPLETE_SYNTAX.md`)
- Natural language patterns (60+ categories)
- Multi-target build system with `// @target` annotations
- Native passthrough mode with `// @raw`, `// @native`, `// @passthrough`

### Changed
- Syntax expansion with hundreds of new natural language aliases

### Fixed
- Various parser and codegen improvements

## [0.6.0] — 2026-06-15

### Added
- 170+ new natural language aliases
- Pipe operator (`|>`)
- Destructuring assignment
- Generator expressions
- Logical assignment operators (`||=`, `&&=`, `??=`)
- String method aliases (capitalize, title, swapcase)

## [0.5.0] — 2026-06-01

### Added
- Class and inheritance support
- Pattern matching
- Error handling (try/catch/finally)
- List and dict comprehensions
- English-like comparison operators
- Functional operations (map, filter, reduce)
