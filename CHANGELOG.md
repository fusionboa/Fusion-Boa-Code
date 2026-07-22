# Changelog

All notable changes to FusionBoa will be documented in this file.

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
