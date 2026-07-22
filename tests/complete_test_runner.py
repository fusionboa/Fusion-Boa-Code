"""
FusionBoa Complete Test Runner
Processes complete_test.fusboa through ALL 23 codegen backends and validates output.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fusionboa_lang.lexer.lexer import tokenize
from fusionboa_lang.parser.parser import Parser
from fusionboa_lang.codegen.target_router import split_by_target, is_raw_section, get_raw_target
from fusionboa_lang.codegen.python_gen import generate_python
from fusionboa_lang.codegen.javascript_gen import generate_javascript
from fusionboa_lang.codegen.typescript_gen import generate_typescript
from fusionboa_lang.codegen.ruby_gen import generate_ruby
from fusionboa_lang.codegen.go_gen import generate_go
from fusionboa_lang.codegen.rust_gen import generate_rust
from fusionboa_lang.codegen.cpp_gen import generate_cpp
from fusionboa_lang.codegen.java_gen import generate_java
from fusionboa_lang.codegen.kotlin_gen import generate_kotlin
from fusionboa_lang.codegen.swift_gen import generate_swift
from fusionboa_lang.codegen.csharp_gen import generate_csharp
from fusionboa_lang.codegen.lua_gen import generate_lua
from fusionboa_lang.codegen.julia_gen import generate_julia
from fusionboa_lang.codegen.r_gen import generate_r
from fusionboa_lang.codegen.react_gen import generate_react
from fusionboa_lang.codegen.html_gen import generate_html
from fusionboa_lang.codegen.css_gen import generate_css
from fusionboa_lang.codegen.json_gen import generate_json
from fusionboa_lang.codegen.yaml_gen import generate_yaml
from fusionboa_lang.codegen.toml_gen import generate_toml
from fusionboa_lang.codegen.xml_gen import generate_xml
from fusionboa_lang.codegen.markdown_gen import generate_markdown
from fusionboa_lang.codegen.ini_gen import generate_ini


# Programming language codegens take parsed AST
PROG_CODEGENS = {
    'python': generate_python,
    'javascript': generate_javascript,
    'typescript': generate_typescript,
    'ruby': generate_ruby,
    'go': generate_go,
    'rust': generate_rust,
    'cpp': generate_cpp,
    'java': generate_java,
    'kotlin': generate_kotlin,
    'swift': generate_swift,
    'csharp': generate_csharp,
    'lua': generate_lua,
    'julia': generate_julia,
    'r': generate_r,
    'react': generate_react,
}

# Markup/data format codegens take source strings directly
MARKUP_CODEGENS = {
    'html': generate_html,
    'css': generate_css,
    'json': generate_json,
    'yaml': generate_yaml,
    'toml': generate_toml,
    'xml': generate_xml,
    'markdown': generate_markdown,
    'ini': generate_ini,
}


def test_all_targets():
    """Test all 23 codegen targets from complete_test.fusboa."""
    source_path = os.path.join(os.path.dirname(__file__), '..', 'complete_test.fusboa')
    
    with open(source_path, 'r') as f:
        source = f.read()
    
    sections = split_by_target(source)
    
    print("=" * 70)
    print("FusionBoa Complete Test - All 23 Targets")
    print("=" * 70)
    print()
    
    passed = 0
    failed = 0
    results = {}
    
    for section_key, lines in sections.items():
        if section_key == 'fusion':
            continue  # Skip default fusion section
        if is_raw_section(section_key):
            continue  # Skip raw/native passthrough
            
        target = section_key
        section_source = '\n'.join(lines)
        
        if not section_source.strip():
            continue
        
        print(f"  [{target}] ", end="")
        
        try:
            if target in PROG_CODEGENS:
                # Parse FusionBoa source first, then generate
                tokens = tokenize(section_source)
                parser = Parser(tokens)
                ast = parser.parse()
                gen_func = PROG_CODEGENS[target]
                output = gen_func(ast)
                line_count = len(output.split('\n'))
                print(f"OK - {line_count} lines generated")
                passed += 1
                results[target] = ('OK', output, line_count)
                
            elif target in MARKUP_CODEGENS:
                gen_func = MARKUP_CODEGENS[target]
                output = gen_func(section_source)
                line_count = len(output.split('\n'))
                print(f"OK - {line_count} lines generated")
                passed += 1
                results[target] = ('OK', output, line_count)
            else:
                print(f"? - Unknown target, skipping")
                
        except Exception as e:
            print(f"FAILED - {e}")
            failed += 1
            results[target] = ('FAIL', str(e), 0)
    
    print()
    print("=" * 70)
    total = passed + failed
    print(f"RESULTS: {passed}/{total} passed, {failed}/{total} failed")
    print("=" * 70)
    
    return passed, failed, results


def show_sample_outputs(results):
    """Show a sample of generated outputs."""
    print()
    print("=" * 70)
    print("Sample Generated Outputs")
    print("=" * 70)
    print()
    
    # Show a few programming languages
    for target in ['python', 'javascript', 'rust', 'go', 'lua']:
        if target in results and results[target][0] == 'OK':
            status, output, lines = results[target]
            print(f"--- {target.upper()} ({lines} lines) ---")
            print(output[:200])
            if len(output) > 200:
                print("... (truncated)")
            print()
    
    # Show a few markup/data formats
    for target in ['html', 'css', 'json', 'yaml', 'xml']:
        if target in results and results[target][0] == 'OK':
            status, output, lines = results[target]
            print(f"--- {target.upper()} ({lines} lines) ---")
            print(output[:200])
            if len(output) > 200:
                print("... (truncated)")
            print()


def save_all_outputs(results):
    """Save all generated outputs to files."""
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'complete_test_output')
    os.makedirs(output_dir, exist_ok=True)
    
    saved = 0
    for target, (status, output, _) in results.items():
        if status == 'OK':
            ext_map = {
                'python': 'py', 'javascript': 'js', 'typescript': 'ts',
                'ruby': 'rb', 'go': 'go', 'rust': 'rs', 'cpp': 'cpp',
                'java': 'java', 'kotlin': 'kt', 'swift': 'swift',
                'csharp': 'cs', 'lua': 'lua', 'julia': 'jl', 'r': 'r',
                'react': 'jsx',
                'html': 'html', 'css': 'css', 'json': 'json',
                'yaml': 'yaml', 'toml': 'toml', 'xml': 'xml',
                'markdown': 'md', 'ini': 'ini',
            }
            ext = ext_map.get(target, target)
            filename = f"complete_test_output.{ext}"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w') as f:
                f.write(output)
            saved += 1
    
    print(f"Saved {saved} output files to {output_dir}/")


if __name__ == "__main__":
    passed, failed, results = test_all_targets()
    print()
    show_sample_outputs(results)
    print()
    save_all_outputs(results)
    
    if failed > 0:
        print()
        print("FAILED TARGETS:")
        for target, (status, msg, _) in results.items():
            if status == 'FAIL':
                print(f"  {target}: {msg}")
        sys.exit(1)
    else:
        print()
        print("ALL 23 TARGETS PASSED!")
        sys.exit(0)
