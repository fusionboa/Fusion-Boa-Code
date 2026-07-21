#!/usr/bin/env python3
"""
FusionBoa Language CLI

Usage:
    fusionboa run <file.fusboa>                    Run a FusionBoa file (default: Python)
    fusionboa run <file.fusboa> --target js        Run targeting JavaScript
    fusionboa build <file.fusboa>                  Compile to all targets (multi-target)
    fusionboa build <file.fusboa> -o out.py        Output to specific file
    fusionboa build <file.fusboa> --targets py,js  Compile to specific targets only
    fusionboa help                                 Show this help
    
Multi-Target Mode:
    Add // @target <language> annotations in your .fusboa file
    to compile different sections to different languages.
    
    Supported targets: python, javascript, typescript, ruby, go, rust,
    cpp, julia, r, kotlin, swift, java, csharp, lua,
    html, css, json, yaml, toml, xml, markdown, ini, react
"""

import sys
import os
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fusionboa_lang.lexer.lexer import Lexer, LexerError
from fusionboa_lang.lexer.tokens import TokenType
from fusionboa_lang.parser.parser import Parser, ParseError
from fusionboa_lang.parser.ast_nodes import Program

from fusionboa_lang.codegen.python_gen import PythonGenerator
from fusionboa_lang.codegen.javascript_gen import JavaScriptGenerator
from fusionboa_lang.codegen.ruby_gen import RubyGenerator
from fusionboa_lang.codegen.go_gen import GoGenerator
from fusionboa_lang.codegen.rust_gen import RustGenerator
from fusionboa_lang.codegen.typescript_gen import TypeScriptGenerator
from fusionboa_lang.codegen.cpp_gen import CppGenerator
from fusionboa_lang.codegen.julia_gen import JuliaGenerator
from fusionboa_lang.codegen.r_gen import RGenerator
from fusionboa_lang.codegen.kotlin_gen import KotlinGenerator
from fusionboa_lang.codegen.swift_gen import SwiftGenerator
from fusionboa_lang.codegen.java_gen import JavaGenerator
from fusionboa_lang.codegen.csharp_gen import CSharpGenerator
from fusionboa_lang.codegen.lua_gen import LuaGenerator
from fusionboa_lang.codegen.react_gen import ReactGenerator

from fusionboa_lang.codegen.html_gen import generate_html
from fusionboa_lang.codegen.css_gen import generate_css
from fusionboa_lang.codegen.json_gen import generate_json
from fusionboa_lang.codegen.yaml_gen import generate_yaml
from fusionboa_lang.codegen.toml_gen import generate_toml
from fusionboa_lang.codegen.xml_gen import generate_xml
from fusionboa_lang.codegen.markdown_gen import generate_markdown
from fusionboa_lang.codegen.ini_gen import generate_ini

from fusionboa_lang.codegen.target_router import (
    split_by_target,
    is_programming_language,
    build_output_filename,
    is_raw_section,
    get_raw_target,
    TARGET_EXTENSIONS,
)
from fusionboa_lang.runtime.executor import execute


VERSION = "1.0.0-alpha"

BANNER = r"""
  ______          _   _             ____
 |  ____|        (_) (_)           |  _ \           
 | |__   _   _    _   _   ___   _ __ | |_) |  ___    __ _
 |  __| | | | |  | | | | / __| | '_ \|  _ <  / _ \  / _` |
 | |    | |_| |  | | | | \__ \ | | | | |_) || (_) || (_| |
 |_|     \__,_|  |_| |_| |___/ |_| |_|____/  \___/  \__,_|

  The polyglot programming language
  Write in English, compile to everything
  Version {version}
"""


def compile_fusionboa(source: str) -> Program:
    """Compile FusionBoa source code into an AST."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()


def generate_code(ast: Program, target: str) -> str:
    """Generate target language code from AST."""
    generators = {
        "python": PythonGenerator, "py": PythonGenerator,
        "javascript": JavaScriptGenerator, "js": JavaScriptGenerator,
        "ruby": RubyGenerator, "rb": RubyGenerator,
        "go": GoGenerator, "golang": GoGenerator,
        "rust": RustGenerator, "rs": RustGenerator,
        "typescript": TypeScriptGenerator, "ts": TypeScriptGenerator,
        "cpp": CppGenerator, "c++": CppGenerator,
        "julia": JuliaGenerator, "jl": JuliaGenerator,
        "r": RGenerator,
        "kotlin": KotlinGenerator, "kt": KotlinGenerator,
        "swift": SwiftGenerator,
        "java": JavaGenerator,
        "csharp": CSharpGenerator, "cs": CSharpGenerator, "c#": CSharpGenerator,
        "lua": LuaGenerator,
        "react": ReactGenerator, "jsx": ReactGenerator,
    }
    gen_class = generators.get(target)
    if gen_class is None:
        raise ValueError(f"Unsupported target: {target}")
    return gen_class(ast).generate()


def generate_markup(target: str, source: str) -> str:
    """Generate markup/data format code from raw source (non-AST targets)."""
    markup_generators = {
        "html": generate_html, "htm": generate_html,
        "css": generate_css,
        "json": generate_json,
        "yaml": generate_yaml, "yml": generate_yaml,
        "toml": generate_toml,
        "xml": generate_xml,
        "markdown": generate_markdown, "md": generate_markdown,
        "ini": generate_ini, "cfg": generate_ini,
    }
    gen_func = markup_generators.get(target)
    if gen_func is None:
        raise ValueError(f"Unsupported markup target: {target}")
    return gen_func(source)


def build_multi_target(source: str, base_name: str, specific_targets: list = None):
    """Build a FusionBoa file with multiple target sections."""
    sections = split_by_target(source)
    fusion_code = sections.pop("fusion", [])
    outputs = {}
    
    for target, lines in sections.items():
        if specific_targets and target not in specific_targets:
            continue
        section_source = '\n'.join(lines)
        if not section_source.strip():
            continue
        if is_raw_section(target):
            actual_target = get_raw_target(target)
            code = section_source + '\n'
            output_file = build_output_filename(base_name, actual_target)
            outputs[target] = (output_file, code)
            continue
        try:
            if is_programming_language(target):
                ast = compile_fusionboa(section_source)
                code = generate_code(ast, target)
            else:
                code = generate_markup(target, section_source)
            output_file = build_output_filename(base_name, target)
            outputs[target] = (output_file, code)
        except Exception as e:
            print(f"  [!] Error compiling {target} section: {e}", file=sys.stderr)
    
    if fusion_code and not specific_targets:
        fusion_source = '\n'.join(fusion_code)
        if fusion_source.strip():
            code_lines = [l for l in fusion_code if l.strip() and not l.strip().startswith('#') and not l.strip().startswith('//')]
            if "python" not in sections and "py" not in sections:
                if code_lines:
                    try:
                        ast = compile_fusionboa(fusion_source)
                        code = generate_code(ast, "python")
                        output_file = build_output_filename(base_name, "python")
                        outputs["python (default)"] = (output_file, code)
                    except Exception as e:
                        print(f"  [!] Error compiling default section: {e}", file=sys.stderr)
            elif code_lines:
                try:
                    ast = compile_fusionboa(fusion_source)
                    code = generate_code(ast, "python")
                    output_file = f"{base_name}_preamble.py"
                    outputs["python (preamble)"] = (output_file, code)
                except Exception as e:
                    print(f"  [!] Error compiling preamble: {e}", file=sys.stderr)
    return outputs


def _resolve_target_alias(target: str) -> str:
    target = target.lower().strip()
    canonical = {
        "python": "python", "py": "python",
        "javascript": "javascript", "js": "javascript",
        "typescript": "typescript", "ts": "typescript",
        "ruby": "ruby", "rb": "ruby", "go": "go", "golang": "go",
        "rust": "rust", "rs": "rust", "cpp": "cpp", "c++": "cpp",
        "julia": "julia", "jl": "julia", "r": "r",
        "kotlin": "kotlin", "kt": "kotlin", "swift": "swift",
        "java": "java", "csharp": "csharp", "cs": "csharp", "c#": "csharp",
        "lua": "lua", "react": "react", "jsx": "react",
        "html": "html", "htm": "html", "css": "css",
        "json": "json", "yaml": "yaml", "yml": "yaml",
        "toml": "toml", "xml": "xml", "markdown": "markdown", "md": "markdown",
        "ini": "ini", "cfg": "ini",
    }
    return canonical.get(target, target)


def run_file(filepath: str, target: str = "python", show_code: bool = False):
    """Compile and run a FusionBoa file."""
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    if not filepath.endswith(".fusboa"):
        print(f"Warning: FusionBoa files should end with .fusboa")

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    if not source.strip():
        print("Error: Empty file")
        sys.exit(1)

    try:
        sections = split_by_target(source)
        has_annotations = any(t != "fusion" for t in sections)
        
        if has_annotations:
            prog_targets = [t for t in sections if t != "fusion" and is_programming_language(t)]
            markup_targets = [t for t in sections if t != "fusion" and not is_programming_language(t)]
            all_targets = prog_targets + markup_targets
            resolved = _resolve_target_alias(target)
            
            if resolved in sections:
                section_target = resolved
            elif target == "python":
                if not prog_targets:
                    print("No programming language targets found in this file.")
                    print(f"Markup targets available: {', '.join(markup_targets)}")
                    print(f"Use 'fusionboa build {filepath}' to compile markup/data formats.")
                    sys.exit(1)
                section_target = prog_targets[0]
            else:
                print(f"Error: Target '{target}' not found in this file.")
                print(f"Available targets: {', '.join(all_targets)}")
                print(f"Use 'fusionboa build {filepath}' to compile all targets.")
                sys.exit(1)
            
            section_source = '\n'.join(sections[section_target])
            if not section_source.strip():
                print(f"Error: '{section_target}' section is empty.")
                sys.exit(1)
            
            if is_raw_section(section_target):
                actual_target = get_raw_target(section_target)
                print(f"[Running {actual_target} native code...]")
                stdout, stderr, exit_code = execute(section_source, actual_target)
                if stdout: print(stdout)
                if stderr: print(stderr, file=sys.stderr)
                sys.exit(exit_code)
            
            if not is_programming_language(section_target):
                target_code = generate_markup(section_target, section_source)
                print(f"[{section_target} output]")
                print(target_code)
                return
            
            other_targets = [t for t in sections if t not in ("fusion", section_target)]
            if other_targets:
                print(f"[Multi-target: running '{section_target}' section]")
                print(f"   Other targets in file: {', '.join(other_targets)}")
                print()
            
            ast = compile_fusionboa(section_source)
            target_code = generate_code(ast, section_target)
            if show_code:
                print(f"\n--- Generated {section_target.upper()} code ---")
                print(target_code)
                print("--- End generated code ---\n")
            
            stdout, stderr, exit_code = execute(target_code, section_target)
            if stdout: print(stdout)
            if stderr: print(stderr, file=sys.stderr)
            sys.exit(exit_code)
        
        resolved = _resolve_target_alias(target)
        ast = compile_fusionboa(source)
        target_code = generate_code(ast, resolved)
        if show_code:
            print(f"\n--- Generated {resolved.upper()} code ---")
            print(target_code)
            print("--- End generated code ---\n")
        stdout, stderr, exit_code = execute(target_code, resolved)
        if stdout: print(stdout)
        if stderr: print(stderr, file=sys.stderr)
        sys.exit(exit_code)
    except LexerError as e:
        print(f"Lexer Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ParseError as e:
        print(f"Parse Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def build_file(filepath: str, target: str = "python", output: str = None, specific_targets: list = None):
    """Compile a FusionBoa file and output the generated code."""
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    if not source.strip():
        print("Error: Empty file")
        sys.exit(1)
    base_name = Path(filepath).stem
    try:
        sections = split_by_target(source)
        has_annotations = any(t != "fusion" for t in sections)
        if has_annotations:
            print(f"[Building {filepath}...]")
            outputs = build_multi_target(source, base_name, specific_targets)
            if not outputs:
                print("No targets generated.")
                return
            for target, (outfile, code) in outputs.items():
                try:
                    with open(outfile, "w", encoding="utf-8") as f:
                        f.write(code)
                    print(f"   [+] {outfile}  ({target})")
                except Exception as e:
                    print(f"   [!] Error writing {outfile}: {e}")
            print(f"\nGenerated {len(outputs)} file(s).")
        else:
            if specific_targets:
                target = specific_targets[0]
            ast = compile_fusionboa(source)
            target_code = generate_code(ast, target)
            if output:
                output_path = output
            else:
                ext = TARGET_EXTENSIONS.get(target, f".{target}")
                output_path = f"{base_name}{ext}"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(target_code)
            print(f"Compiled to: {output_path}")
    except LexerError as e:
        print(f"Lexer Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ParseError as e:
        print(f"Parse Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def show_tokens(filepath: str):
    """Show tokens for a FusionBoa file (debugging)."""
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    lexer = Lexer(source)
    for token in lexer.tokenize():
        if token.type not in (TokenType.NEWLINE, TokenType.INDENT, TokenType.DEDENT):
            print(f"  {token}")
        elif token.type == TokenType.INDENT:
            print("  -> INDENT")
        elif token.type == TokenType.DEDENT:
            print("  <- DEDENT")


def show_ast(filepath: str):
    """Show the AST for a FusionBoa file (debugging)."""
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    _print_ast(compile_fusionboa(source))


def _print_ast(node, indent: int = 0):
    prefix = "  " * indent
    if isinstance(node, list):
        for item in node:
            _print_ast(item, indent)
    elif node is None:
        print(f"{prefix}None")
    else:
        print(f"{prefix}{node}")


def init_project(name: str = "my_project", multi: bool = False):
    """Create a new FusionBoa project scaffold."""
    project_dir = name
    if os.path.exists(project_dir):
        print(f"Error: Directory '{project_dir}' already exists.")
        sys.exit(1)
    os.makedirs(project_dir)
    hello_content = '''// A multi-target FusionBoa demo
// Each section with @target compiles to a different language/format

// @target python
define function greet with name:
    print "hello, " + name + "!"

greet("world")

// @target html
html lang "en":
    body:
        h1 "Hello from FusionBoa!"
        p "This HTML was generated from FusionBoa syntax."

// @target json
{
    name: "fusionboa",
    version: "0.7.0",
    targets: ["python", "html", "json"]
}
''' if multi else '''// Hello, FusionBoa!
// Write in English, compile to any language

let name be "FusionBoa"
let version be "0.7.0"

print "Hello, " + name + "!"
print "Version: " + version

set name to name + " Language"
print name

define function greet with person:
    print "Hi there, " + person + "!"

greet("developer")

for each i in [1, 2, 3]:
    print "Count: " + i
'''
    filepath = os.path.join(project_dir, "main.fusboa")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(hello_content)
    print(f"Created FusionBoa project: {project_dir}/")
    print(f"  main.fusboa")
    print()
    print("Quick start:")
    print(f"  cd {project_dir}")
    print(f"  fusionboa run main.fusboa")
    if multi:
        print(f"  fusionboa build main.fusboa")
    print()


def format_file(filepath: str, check: bool = False):
    """Format a FusionBoa file with proper indentation."""
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    lines = source.split('\n')
    formatted = []
    indent_level = 0
    in_block = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            formatted.append('')
            continue
        if stripped.startswith('}') or stripped.startswith(']') or stripped.startswith(')'):
            indent_level = max(0, indent_level - 1)
        first_word = stripped.split()[0].rstrip(':') if stripped.split() else ''
        if first_word in ('otherwise', 'or', 'catch', 'finally', 'elif', 'else') and in_block:
            indent_level = max(0, indent_level - 1)
        indent = '    ' * indent_level
        formatted.append(indent + stripped)
        if stripped.endswith(':'):
            indent_level += 1
            in_block = True
        if stripped.endswith('{') or stripped.endswith('(') or stripped.endswith('['):
            indent_level += 1
    result = '\n'.join(formatted)
    if check:
        if source == result:
            print(f"{filepath} is properly formatted.")
        else:
            print(f"{filepath} needs formatting.")
            sys.exit(1)
    else:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Formatted: {filepath}")


def show_targets():
    """Show all available compilation targets."""
    print("\nFusionBoa Compilation Targets\n")
    print("  Programming Languages:")
    for t in ["python", "javascript", "typescript", "ruby", "go", "rust",
              "cpp", "julia", "r", "kotlin", "swift", "java", "csharp", "lua", "react"]:
        ext = TARGET_EXTENSIONS.get(t, f".{t}")
        print(f"    {t:12} -> {ext}")
    print("\n  Markup & Data Formats:")
    for t in ["html", "css", "json", "yaml", "toml", "xml", "markdown", "ini"]:
        ext = TARGET_EXTENSIONS.get(t, f".{t}")
        print(f"    {t:12} -> {ext}")
    print("\n  Use // @target <name> in your .fusboa file to route sections.")
    print("  Example: // @target html")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="FusionBoa Language - Write in English, compile to everything",
        prog="fusionboa"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command")

    run_parser = subparsers.add_parser("run", help="Compile and run a FusionBoa file")
    run_parser.add_argument("file", help="FusionBoa source file (.fusboa)")
    run_parser.add_argument("--target", "-t", default="python", help="Target language")
    run_parser.add_argument("--show-code", "-s", action="store_true", help="Show generated code before executing")

    build_parser = subparsers.add_parser("build", help="Compile a FusionBoa file")
    build_parser.add_argument("file", help="FusionBoa source file (.fusboa)")
    build_parser.add_argument("--target", "-t", default="python", help="Target language")
    build_parser.add_argument("--targets", help="Comma-separated targets for multi-target build")
    build_parser.add_argument("--output", "-o", help="Output file path")

    tokens_parser = subparsers.add_parser("tokens", help="Show tokens for a FusionBoa file")
    tokens_parser.add_argument("file", help="FusionBoa source file (.fusboa)")

    ast_parser = subparsers.add_parser("ast", help="Show AST for a FusionBoa file")
    ast_parser.add_argument("file", help="FusionBoa source file (.fusboa)")

    subparsers.add_parser("targets", help="List all available compilation targets")

    init_parser = subparsers.add_parser("init", help="Create a new FusionBoa project")
    init_parser.add_argument("name", nargs="?", default="my_project", help="Project name")
    init_parser.add_argument("--multi", action="store_true", help="Create a multi-target demo project")

    format_parser = subparsers.add_parser("format", help="Format a FusionBoa file")
    format_parser.add_argument("file", help="FusionBoa source file (.fusboa)")
    format_parser.add_argument("--check", action="store_true", help="Check if file is formatted (no changes)")

    subparsers.add_parser("version", help="Show version")
    subparsers.add_parser("help", help="Show help and usage")

    args = parser.parse_args()

    if args.command == "run":
        run_file(args.file, target=args.target, show_code=args.show_code)
    elif args.command == "build":
        specific_targets = args.targets.split(",") if args.targets else None
        build_file(args.file, target=args.target, output=args.output, specific_targets=specific_targets)
    elif args.command == "tokens":
        show_tokens(args.file)
    elif args.command == "ast":
        show_ast(args.file)
    elif args.command == "targets":
        show_targets()
    elif args.command == "init":
        init_project(args.name, multi=args.multi)
    elif args.command == "format":
        format_file(args.file, check=args.check)
    elif args.command == "version":
        print(f"FusionBoa Language v{VERSION}")
    elif args.command == "help":
        print(BANNER.format(version=VERSION))
        parser.print_help()
    else:
        print(BANNER.format(version=VERSION))
        parser.print_help()


if __name__ == "__main__":
    main()
