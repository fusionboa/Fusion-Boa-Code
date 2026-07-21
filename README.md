# ⚡ FusionBoa Language

**Write in English. Compile to everything.**

FusionBoa is the polyglot programming language where you write code the way you *think* — in natural, English-like syntax — and compile a single `.fusboa` file to **23 different targets**: Python, JavaScript, TypeScript, Go, Rust, C++, Java, C#, Ruby, Lua, Kotlin, Swift, Julia, R, React, HTML, CSS, JSON, YAML, TOML, XML, Markdown, and INI.

[![Tests](https://img.shields.io/badge/tests-200%2F200-brightgreen)](https://github.com)
[![Targets](https://img.shields.io/badge/targets-23-blue)](https://github.com)
[![Keywords](https://img.shields.io/badge/keywords-708-orange)](https://github.com)
[![Version](https://img.shields.io/badge/version-0.7.0-purple)](https://github.com)

```bash
fusionboa run hello.fusboa              # Compile + run as Python
fusionboa run hello.fusboa --target js  # Compile + run as JavaScript
fusionboa build app.fusboa              # Generate ALL targets at once
```

---

## 🚀 Quick Start — Clone & Install

### Windows
```batch
git clone https://github.com/fusionboa/Fusion-Boa-Code.git
cd Fusion-Boa-Code
install.bat                    # Double-click or run — adds to PATH automatically
:: Restart your terminal, then:
fusionboa version              # FusionBoa Language v1.0.0-alpha
```

### macOS / Linux
```bash
git clone https://github.com/fusionboa/Fusion-Boa-Code.git
cd Fusion-Boa-Code
chmod +x install.sh && ./install.sh
source ~/.zshrc                # (or ~/.bashrc)

fusionboa version              # FusionBoa Language v1.0.0-alpha
```

### Create a project & run
```bash
fusionboa init my_project
cd my_project
fusionboa run main.fusboa      # Compile + execute in one command
fusionboa build main.fusboa    # Generate output files
```

---

## 📦 Runtime Dependencies

FusionBoa itself only needs **Python 3.8+**. But to *run* compiled output for each target, you'll need that language's runtime installed.

### Quick Install (Recommended)

| Platform | Command | Gets You |
|----------|---------|----------|
| **Windows** | `winget install Python.Python.3.12 OpenJS.NodeJS` | Python + JavaScript |
| **macOS** | `brew install python node` | Python + JavaScript |
| **Linux** | `sudo apt install python3 nodejs -y` | Python + JavaScript |

> 💡 **Python + Node.js** covers 2 of the 3 executable targets. For the rest, install what you need below.

### All Targets — Install Guides

#### Programming Languages

| Target | Windows | macOS | Linux (Ubuntu/Debian) |
|--------|---------|-------|-----------------------|
| **Python** 🐍 | `winget install Python.Python.3.12` | `brew install python` | `sudo apt install python3 -y` |
| **JavaScript/Node** 🟨 | `winget install OpenJS.NodeJS` | `brew install node` | `sudo apt install nodejs -y` |
| **TypeScript** 🔷 | `npm i -g typescript ts-node` | `npm i -g typescript ts-node` | `npm i -g typescript ts-node` |
| **Ruby** 💎 | `winget install RubyInstallerTeam.Ruby` | `brew install ruby` | `sudo apt install ruby -y` |
| **Go** 🔵 | `winget install GoLang.Go` | `brew install go` | `sudo apt install golang -y` |
| **Rust** 🦀 | `winget install Rustlang.Rust` | `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \| sh` | `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \| sh` |
| **C++** ⚙️ | `winget install Microsoft.VisualStudio.2022.BuildTools` | `brew install gcc` | `sudo apt install g++ -y` |
| **Lua** 🌙 | `winget install Lua.Lua` | `brew install lua` | `sudo apt install lua5.4 -y` |
| **Swift** 🕊️ | `winget install Apple.Swift` | `brew install swift` | `sudo apt install swift -y` |
| **Kotlin** 🟣 | `winget install JetBrains.Kotlin` | `brew install kotlin` | `sudo apt install kotlin -y` |
| **Java** ☕ | `winget install Oracle.JDK.23` | `brew install openjdk` | `sudo apt install default-jdk -y` |
| **Julia** 🟢 | `winget install Julialang.Julia` | `brew install julia` | `sudo apt install julia -y` |
| **R** 📊 | `winget install RProject.R` | `brew install r` | `sudo apt install r-base -y` |
| **C# (.NET)** 🟪 | `winget install Microsoft.DotNet.SDK.8` | `brew install dotnet-sdk` | `sudo apt install dotnet-sdk-8.0 -y` |
| **React** ⚛️ | Requires Node.js (see above) | Requires Node.js (see above) | Requires Node.js (see above) |

#### No Runtimes Needed (Generated Files)

| Target | Notes |
|--------|-------|
| **HTML, CSS, JSON, YAML, TOML, XML, Markdown, INI** | These generate static files — open in any browser/editor. No runtime needed. |

---

## 📝 Write in English, Not Code

FusionBoa understands **hundreds of ways** to say the same thing. Pick your style:

```fusionboa
# ALL of these do the SAME thing — pick what feels natural:

let x be 5              var x be 5             declare x be 5
make x be 5             initialize x be 5      set up x be 5

# Functions — 20+ aliases:
define function greet with name:               # primary
def func greet with name:                      # short
define method greet with name:                 # OOP style
define procedure greet with name:              # formal

# Conditionals — 15+ ways:
if x > 0: ...              provided x > 0: ...
in the event that x > 0: ...    supposing x > 0: ...
given x > 0: ...            assuming x > 0: ...

# Loops — 25+ ways:
for each item in list: ...        loop over item in list: ...
iterate over item in list: ...    going through item in list: ...
scanning through item in list: ...   walk item in list: ...

# Booleans — 15+ ways each:
true  yes  yup  definitely  absolutely  certainly  on  enabled
false  no  nope  nah  never  off  disabled  negative
null  none  nothing  blank  undefined  maybe  perhaps

# Print — 20+ ways:
print x  display x  show x  say x  output x  log x  echo x
announce x  report x  mention x  proclaim x  remark x
```

### A Real Program in FusionBoa

```fusionboa
// Hello, FusionBoa!
// One file, compile to any language

use math

define function fibonacci with n:
    if n is less than or equal to 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

let result be fibonacci(10)
print "Fibonacci(10) = " + result

// Classes with inheritance
define class Animal:
    define function init with name:
        set this.name to name

define class Dog inherits from Animal:
    define function bark:
        print this.name + " says woof!"

let buddy be Dog("Buddy")
buddy.bark()

// Functional operations
let numbers be [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
map numbers using function with x: x * 2
filter numbers where x is greater than 5
fold numbers using add starting with 0

// Pattern matching
match result:
    case 0: print "zero"
    case 1: print "one"
    default: print "many"

// Error handling
try:
    let risky be 10 / 0
catch error as e:
    print "Oops: " + e
finally:
    print "Cleanup done"
```

---

## 🎯 All 23 Compilation Targets

### Programming Languages (15)
| Target | Extension | Runtime |
|--------|-----------|---------|
| Python | `.py` | `python` |
| JavaScript | `.js` | `node` |
| TypeScript | `.ts` | `ts-node` / `deno` |
| Go | `.go` | `go run` |
| Rust | `.rs` | `rustc` / `cargo` |
| C++ | `.cpp` | `g++` / `clang++` |
| Java | `.java` | `javac` + `java` |
| C# | `.cs` | `dotnet` / `mono` |
| Ruby | `.rb` | `ruby` |
| Lua | `.lua` | `lua` |
| Kotlin | `.kt` | `kotlinc` |
| Swift | `.swift` | `swift` |
| Julia | `.jl` | `julia` |
| R | `.r` | `Rscript` |
| React | `.jsx` | — (compiles to JS) |

### Markup & Data Formats (8)
| Target | Extension |
|--------|-----------|
| HTML | `.html` |
| CSS | `.css` |
| JSON | `.json` |
| YAML | `.yaml` |
| TOML | `.toml` |
| XML | `.xml` |
| Markdown | `.md` |
| INI | `.ini` |

---

## 📦 Multi-Target Power

One `.fusboa` file, many outputs. Use `// @target` annotations:

```fusionboa
// @target python
define function process with data:
    return sum(data)

// @target javascript
define function process with data:
    let total be fold data using add starting with 0
    return total

// @target html
html lang "en":
    head: title "FusionBoa App"
    body:
        h1 "Hello from FusionBoa!"
        p "This HTML was generated from a .fusboa file."

// @target css
body:
    font-family "system-ui"
    background-color "#0f0f23"
    color "#00ff88"

// @target json
{
    name: "fusionboa-app",
    version: "0.7.0",
    targets: ["python", "javascript", "html", "css", "json"]
}
```

```bash
fusionboa build app.fusboa
# Generates: app.py, app.js, app.html, app.css, app.json
```

### Native Passthrough Mode
Need full control? Use `// @native` to write raw target code:

```fusionboa
// @native python
import pygame
screen = pygame.display.set_mode((800, 600))
# ... full native Python with no restrictions

// @native javascript
const express = require('express');
const app = express();
// ... full native Node.js

// @native rust
use std::collections::HashMap;
fn main() { println!("Hello from Rust!"); }
```

---

## 🛠️ CLI Reference

| Command | Description |
|---------|-------------|
| `fusionboa run file.fusboa` | Compile + execute (auto-detects target) |
| `fusionboa run file.fusboa -t js` | Run targeting specific language |
| `fusionboa run file.fusboa -s` | Show generated code before running |
| `fusionboa build file.fusboa` | Compile all targets in file |
| `fusionboa build file.fusboa -t js` | Compile single target |
| `fusionboa build file.fusboa --targets py,js,html` | Specific targets only |
| `fusionboa build file.fusboa -o out.py` | Output to specific file |
| `fusionboa init my_project` | Scaffold new project |
| `fusionboa init my_project --multi` | Multi-target project |
| `fusionboa format file.fusboa` | Auto-format code |
| `fusionboa format file.fusboa --check` | Check formatting (CI mode) |
| `fusionboa targets` | List all 23 targets |
| `fusionboa tokens file.fusboa` | Debug: show token stream |
| `fusionboa ast file.fusboa` | Debug: show AST tree |
| `fusionboa version` | Show version |
| `fusionboa help` | Full help |

---

## 📊 By the Numbers

| Metric | Count |
|--------|-------|
| Keywords | **708** |
| Token types | **228** |
| Syntax aliases | **500+** |
| Compile targets | **23** |
| Tests passing | **200/200** |
| Natural language patterns | 60+ categories |

---

## 🏗️ Project Structure

```
Fusion lang/
├── fusionboa.py          # CLI entry point
├── fusionboa.bat         # Windows launcher
├── fusionboa             # macOS/Linux launcher
├── install.bat           # Windows one-click installer
├── install.sh            # macOS/Linux installer
├── install.py            # Cross-platform installer
├── README.md             # This file
├── COMPLETE_SYNTAX.md    # Full 700+ line syntax reference
├── fusionboa_lang/
│   ├── lexer/            # Tokenizer (708 keywords)
│   ├── parser/           # Parser (English-like AST)
│   ├── codegen/          # 23 code generators
│   └── runtime/          # Multi-language executor
└── examples/             # Demo .fusboa files
```

---

## 📄 License

Proprietary — All Rights Reserved. See [LICENSE](LICENSE) file.

---

**FusionBoa — Because code should read like a conversation, not a cipher.**
