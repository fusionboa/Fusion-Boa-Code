"""
Automated tests for all FusionBoa codegen backends.

Run: python -m pytest fusionboa_lang/codegen/test_codegens.py -v
Or:  python fusionboa_lang/codegen/test_codegens.py
"""

import sys
import os
import unittest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fusionboa_lang.codegen.html_gen import generate_html
from fusionboa_lang.codegen.css_gen import generate_css
from fusionboa_lang.codegen.json_gen import generate_json
from fusionboa_lang.codegen.yaml_gen import generate_yaml
from fusionboa_lang.codegen.toml_gen import generate_toml
from fusionboa_lang.codegen.xml_gen import generate_xml
from fusionboa_lang.codegen.markdown_gen import generate_markdown
from fusionboa_lang.codegen.ini_gen import generate_ini
from fusionboa_lang.codegen.data_parser import parse_data
from fusionboa_lang.codegen.target_router import split_by_target, is_programming_language
from fusionboa_lang.codegen.python_gen import generate_python
from fusionboa_lang.codegen.javascript_gen import generate_javascript
from fusionboa_lang.codegen.cpp_gen import generate_cpp
from fusionboa_lang.codegen.go_gen import generate_go
from fusionboa_lang.codegen.java_gen import generate_java
from fusionboa_lang.codegen.lua_gen import generate_lua
from fusionboa_lang.codegen.r_gen import generate_r
from fusionboa_lang.codegen.julia_gen import generate_julia
from fusionboa_lang.codegen.rust_gen import generate_rust
from fusionboa_lang.codegen.ruby_gen import generate_ruby
from fusionboa_lang.codegen.kotlin_gen import generate_kotlin
from fusionboa_lang.codegen.swift_gen import generate_swift
from fusionboa_lang.codegen.csharp_gen import generate_csharp
from fusionboa_lang.codegen.typescript_gen import generate_typescript
from fusionboa_lang.lexer.lexer import tokenize
from fusionboa_lang.parser.parser import Parser


class TestLexerNewFeatures(unittest.TestCase):
    """Tests for new lexer features."""

    def test_multi_line_string(self):
        """Triple-quoted multi-line strings."""
        source = 'let x be """\nhello\nworld\n"""'
        tokens = tokenize(source)
        # Should find a STRING token with the multi-line content
        strings = [t for t in tokens if t.type.name == "STRING"]
        self.assertTrue(len(strings) > 0, "Should produce a STRING token")
        content = strings[0].value
        self.assertIn("hello", content)
        self.assertIn("world", content)

    def test_comment_slash_slash(self):
        """// style comments should be treated as comments."""
        source = 'let x be 5\n// this is a comment\nset y to x + 1'
        tokens = tokenize(source)
        # // line should be skipped - comment words should not appear
        token_values = [t.value for t in tokens]
        self.assertIn("y", token_values, "Code after comment should still tokenize")
        self.assertIn("x", token_values, "Code after comment should still tokenize")
        self.assertNotIn("this", token_values, "Comment text should not produce tokens")
        self.assertNotIn("comment", token_values, "Comment text should not produce tokens")

    def test_backslash_skipped_between_tokens(self):
        """Backslash between tokens should be silently skipped."""
        source = 'let x be \\ 5'
        tokens = tokenize(source)
        token_values = [t.value for t in tokens if t.type.name in ("IDENTIFIER", "INTEGER")]
        self.assertIn("x", token_values)
        self.assertIn(5, token_values)
        self.assertEqual(len(tokens), 5, "Should produce LET, IDENTIFIER(x), BE, INTEGER(5), EOF")

    def test_backslash_at_start_of_file(self):
        """Backslash at start of file should not cause error."""
        source = '\\let x be 5'
        tokens = tokenize(source)
        self.assertTrue(len(tokens) > 0)
        token_values = [t.value for t in tokens if t.type.name in ("IDENTIFIER", "INTEGER")]
        self.assertIn("x", token_values)
        self.assertIn(5, token_values)

    def test_backslash_before_newline(self):
        """Backslash before newline should be skipped (line continuation in other langs)."""
        source = 'let x be ' + chr(92) + '\n5'
        tokens = tokenize(source)
        token_values = [t.value for t in tokens if t.type.name in ("IDENTIFIER", "INTEGER")]
        self.assertIn("x", token_values)
        self.assertIn(5, token_values)

    def test_multiple_backslashes(self):
        """Multiple consecutive backslashes should all be skipped."""
        source = 'let x be ' + chr(92) * 3 + ' 5'
        tokens = tokenize(source)
        token_values = [t.value for t in tokens if t.type.name in ("IDENTIFIER", "INTEGER")]
        self.assertIn("x", token_values)
        self.assertIn(5, token_values)

    def test_backslash_in_string_still_escapes(self):
        """Backslash should still work as escape character inside strings."""
        source = 'let x be "hello\\nworld"'
        tokens = tokenize(source)
        strings = [t for t in tokens if t.type.name == "STRING"]
        self.assertTrue(len(strings) > 0)
        msg = 'backslash-n in string should produce newline'
        self.assertIn("\n", strings[0].value, msg)

    def test_backslash_not_breaking_other_operators(self):
        """Backslash should not interfere with other operator parsing."""
        source = 'let x \\ be 5 \\ + 3'
        tokens = tokenize(source)
        plus_tokens = [t for t in tokens if t.type.name == "PLUS"]
        self.assertEqual(len(plus_tokens), 1, "PLUS operator should still be found")
        integers = [t.value for t in tokens if t.type.name == "INTEGER"]
        self.assertIn(5, integers)
        self.assertIn(3, integers)

    def test_backslash_in_raw_section_workaround(self):
        """Backslash in a simulated raw section context should not crash."""
        # Simulates a backslash that might appear in a file with native passthrough
        source = 'let path be "C:\\\\Users"'
        tokens = tokenize(source)
        strings = [t for t in tokens if t.type.name == "STRING"]
        self.assertTrue(len(strings) > 0)
        # The backslash should be in the string value
        self.assertIn("\\", strings[0].value)

class TestParserNewFeatures(unittest.TestCase):
    """Tests for new parser features."""

    def test_dict_comprehension(self):
        """{k: v for each k,v in items if cond} syntax."""
        source = 'let result be {k: k * 2 for each k in items if k > 0}'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertTrue(len(ast.statements) > 0, "Should parse without error")
        # The value should be a DictComprehension
        stmt = ast.statements[0]
        self.assertEqual(stmt.__class__.__name__, "VariableDeclaration")
        val = stmt.value
        self.assertEqual(val.__class__.__name__, "DictComprehension")

    def test_defer_statement(self):
        """defer: block syntax."""
        source = 'define function foo with x:\n    defer:\n        print "cleanup"\n    print x'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertTrue(len(ast.statements) > 0, "Should parse without error")

    def test_guard_statement(self):
        """guard condition else: block syntax."""
        source = 'define function foo with x:\n    guard x > 0 else:\n        print "invalid"\n    print x'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertTrue(len(ast.statements) > 0, "Should parse without error")


class TestNewFeatures(unittest.TestCase):
    """Tests for all newly added features in this update."""

    def test_pipe_operator_lexer(self):
        """|> should be tokenized as PIPE_OP."""
        source = 'let result be x |> f'
        tokens = tokenize(source)
        pipe_tokens = [t for t in tokens if t.type.name in ("PIPE_OP", "PIPE")]
        self.assertEqual(len(pipe_tokens), 1, "Should have exactly one pipe token")
        self.assertEqual(pipe_tokens[0].type.name, "PIPE_OP", "Should be PIPE_OP, not PIPE")

    def test_pipe_operator_parsing(self):
        """x |> f should parse as a binary operation."""
        source = 'let result be x |> f'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        stmt = ast.statements[0]
        self.assertEqual(stmt.__class__.__name__, "VariableDeclaration")
        self.assertEqual(stmt.value.__class__.__name__, "BinaryOp")
        self.assertEqual(stmt.value.operator, "|>")

    def test_pipe_operator_python_gen(self):
        """x |> f should generate f(x) in Python."""
        source = 'let result be x |> f'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("f(x)", code, "Pipe should generate f(x)")

    def test_pipe_operator_with_call(self):
        """x |> f(a, b) should generate f(x, a, b) in Python."""
        source = 'let result be x |> f(1, 2)'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("f(x, 1, 2)", code)

    def test_pipe_operator_chained(self):
        """x |> f |> g should generate g(f(x))."""
        source = 'let result be x |> f |> g'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("g(f(x))", code)

    def test_every_keyword(self):
        """'every' should work as alias for 'each' in for loops."""
        source = 'for every item in items:\n    print item'
        tokens = tokenize(source)
        # 'every' should be tokenized as EACH
        each_tokens = [t for t in tokens if t.type.name == "EACH"]
        self.assertEqual(len(each_tokens), 1, "'every' should produce an EACH token")
        # Should parse correctly
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertTrue(len(ast.statements) > 0, "Should parse without error")

    def test_html_doctype(self):
        """doctype html should generate <!DOCTYPE html>."""
        result = generate_html('doctype html')
        self.assertIn("<!DOCTYPE HTML>", result, "Should generate DOCTYPE declaration")

    def test_html_doctype_custom(self):
        """doctype svg should generate <!DOCTYPE svg>."""
        result = generate_html('doctype "svg"')
        self.assertIn("<!DOCTYPE SVG>", result)


class TestEnglishSyntaxFeatures(unittest.TestCase):
    """Tests for all new English-like syntax features."""

    def test_swap_statement(self):
        """swap x and y should swap values."""
        source = 'swap x and y'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertEqual(stmt.__class__.__name__, "SwapStatement")
        self.assertEqual(stmt.left, "x")
        self.assertEqual(stmt.right, "y")

    def test_swap_python_codegen(self):
        """swap x and y -> x, y = y, x"""
        source = 'swap x and y'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("x, y = y, x", code)

    def test_xor_operator(self):
        """x xor y should parse as binary operator."""
        source = 'if x xor y:\n    print "true"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        self.assertEqual(ast.statements[0].__class__.__name__, "IfStatement")

    def test_xor_python_codegen(self):
        """x xor y -> x ^ y"""
        source = 'let result be x xor y'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("x ^ y", code)

    def test_between_expression(self):
        """x between 5 and 10 should parse."""
        source = 'if x between 5 and 10:\n    print "yes"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)

    def test_between_python_codegen(self):
        """x between 5 and 10 -> 5 <= x <= 10"""
        source = 'let result be x between 5 and 10'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("5 <=", code)
        self.assertIn("<= 10", code)
        self.assertIn("x", code)

    def test_has_operator(self):
        """mylist has item should parse as membership check."""
        source = 'if mylist has item:\n    print "yes"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)

    def test_has_python_codegen(self):
        """mylist has item -> item in mylist (swapped)"""
        source = 'let result be mylist has item'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("item in mylist", code)

    def test_contains_operator(self):
        """name contains "hello" should parse."""
        source = 'if name contains "hello":\n    print "found"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)

    def test_contains_python_codegen(self):
        """name contains "hello" -> 'hello' in name (swapped, single quotes from repr)"""
        source = 'let result be name contains "hello"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("in name", code)
        self.assertIn("hello", code)

    def test_starts_with(self):
        """name starts with "hello" should parse."""
        source = 'if name starts with "hello":\n    print "found"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)

    def test_starts_with_python_codegen(self):
        """name starts with "hello" -> name.startswith('hello')"""
        source = 'let result be name starts with "hello"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("name.startswith", code)
        self.assertIn("hello", code)

    def test_ends_with(self):
        """name ends with "world" should parse."""
        source = 'if name ends with "world":\n    print "found"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)

    def test_ends_with_python_codegen(self):
        """name ends with "world" -> name.endswith('world')"""
        source = 'let result be name ends with "world"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("name.endswith", code)

    def test_push_statement(self):
        """push value into list should parse."""
        source = 'push 5 into mylist'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(ast.statements[0].__class__.__name__, "PushStatement")

    def test_push_python_codegen(self):
        """push value into list -> list.append(value)"""
        source = 'push 5 into mylist'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("mylist.append(5)", code)

    def test_pop_statement(self):
        """pop from list should parse."""
        source = 'pop from mylist'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(ast.statements[0].__class__.__name__, "PopStatement")

    def test_pop_python_codegen(self):
        """pop from list -> list.pop()"""
        source = 'pop from mylist'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("mylist.pop()", code)

    def test_when_expression(self):
        """when condition then value or other should parse."""
        source = 'let result be when x > 0 then "pos" or "neg"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)

    def test_when_python_codegen(self):
        """when x > 0 then "pos" or "neg" -> 'pos' if x > 0 else 'neg'"""
        source = 'let result be when x > 0 then "pos" or "neg"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("'pos' if (x > 0)", code)
        self.assertIn("else 'neg'", code)

    def test_where_in_comprehension(self):
        """[x for each x in items where x > 0] should work like 'if'."""
        source = 'let result be [x for each x in items where x > 0]'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        code = generate_python(ast)
        self.assertIn("for x in items if", code)
        self.assertIn("x > 0", code)

    def test_is_a_type_check(self):
        """'is a' should work as type check."""
        source = 'if x is a string:\n    print "yes"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)

    def test_add_statement(self):
        """add x to y -> y += x"""
        source = 'add 5 to total'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        code = generate_python(ast)
        self.assertIn("total += 5", code)

    def test_subtract_statement(self):
        """subtract x from y -> y -= x"""
        source = 'subtract 5 from total'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        code = generate_python(ast)
        self.assertIn("total -= 5", code)

    def test_multiply_statement(self):
        """multiply x by 2 -> x *= 2"""
        source = 'multiply x by 2'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("x *= 2", code)

    def test_divide_statement(self):
        """divide x by 2 -> x /= 2"""
        source = 'divide x by 2'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("x /= 2", code)

    def test_first_of(self):
        """first of items -> items[0]"""
        source = 'let result be first of items'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("items[0]", code)

    def test_last_of(self):
        """last of items -> items[-1]"""
        source = 'let result be last of items'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("items[-1]", code)

    def test_rest_of(self):
        """rest of items -> items[1:]"""
        source = 'let result be rest of items'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("items[1:]", code)

    def test_reverse_statement(self):
        """reverse items -> items.reverse()"""
        source = 'reverse items'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("items.reverse()", code)

    def test_sort_statement(self):
        """sort items -> items.sort()"""
        source = 'sort items'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("items.sort()", code)

    def test_clear_statement(self):
        """clear items -> items.clear()"""
        source = 'clear items'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("items.clear()", code)

    def test_append_statement(self):
        """append value to list -> list.append(value)"""
        source = 'append 5 to mylist'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("mylist.append(5)", code)

    def test_remove_statement(self):
        """remove value from list -> list.remove(value)"""
        source = 'remove "item" from mylist'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("mylist.remove", code)

    def test_includes_operator(self):
        """list includes item -> item in list"""
        source = 'if mylist includes "hello":\n    print "found"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)

    def test_has_no_operator(self):
        """mylist has no item -> item not in mylist"""
        source = 'if mylist has no "hello":\n    print "not found"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)

    def test_has_no_python_codegen(self):
        """mylist has no item -> item not in mylist"""
        source = 'let result be mylist has no "hello"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("not in mylist", code)

    def test_is_empty(self):
        """list is empty -> len(list) == 0"""
        source = 'if mylist is empty:\n    print "empty"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)

    def test_is_not_empty(self):
        """list is not empty -> not len(list) == 0"""
        source = 'if mylist is not empty:\n    print "has items"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)

    def test_min_of(self):
        """min of items -> min(items)"""
        source = 'let result be min of items'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("min(items)", code)

    def test_max_of(self):
        """max of items -> max(items)"""
        source = 'let result be max of items'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("max(items)", code)

    def test_sum_of(self):
        """sum of items -> sum(items)"""
        source = 'let result be sum of items'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("sum(items)", code)

    def test_abs_of(self):
        """abs of x -> abs(x)"""
        source = 'let result be abs of x'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("abs(x)", code)

    def test_round(self):
        """round x -> round(x)"""
        source = 'let result be round 3.14'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("round(3.14)", code)

    def test_count_of(self):
        """count of items -> len(items)"""
        source = 'let result be count of items'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("len(items)", code)

    def test_upper(self):
        """upper text -> text.upper()"""
        source = 'let result be upper text'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("text.upper()", code)

    def test_lower(self):
        """lower text -> text.lower()"""
        source = 'let result be lower text'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("text.lower()", code)

    def test_strip(self):
        """strip text -> text.strip()"""
        source = 'let result be strip text'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("text.strip()", code)

    def test_includes_python_codegen(self):
        """mylist includes item -> item in mylist (swapped)"""
        source = 'let result be mylist includes "hello"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("in mylist", code)

    def test_excludes_python_codegen(self):
        """mylist excludes item -> item not in mylist (swapped)"""
        source = 'let result be mylist excludes "hello"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("not in mylist", code)

    def test_is_same_as(self):
        """x is same as y -> x is y"""
        source = 'if x is same as y:\n    print "same"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)

    def test_is_same_as_python_codegen(self):
        """x is same as y -> x is y"""
        source = 'let result be x is same as y'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("x is y", code)

    def test_join_expression(self):
        """join items with separator -> separator.join(items)"""
        source = 'let result be join items with ","'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn(".join(items)", code)

    def test_split_expression(self):
        """split text by separator -> text.split(separator)"""
        source = 'let result be split text by ","'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn(".split", code)

    def test_pow_keyword(self):
        """pow should be alias for ^ (power)."""
        source = 'let result be 2 pow 3'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("**", code)


class TestCodegenNewSyntax(unittest.TestCase):
    """Tests that new AST nodes generate valid code without crashing."""

    def test_python_defer_and_guard(self):
        """Python generator should handle defer/guard."""
        source = 'define function test with x:\n    guard x > 0 else:\n        return -1\n    defer:\n        print "done"\n    return x * 2'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("not (", code, "Guard should generate 'if not'")
        self.assertIn("return", code, "Guard should have return")
        self.assertIn("deferred", code, "Defer should be noted")

    def test_python_dict_comp(self):
        """Python generator should handle dict comprehensions."""
        source = 'let result be {k: k * 2 for each k in items}'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("for", code)


class TestTargetRouter(unittest.TestCase):
    """Tests for the @target annotation system."""

    def test_split_basic(self):
        source = """let x be 1
// @target html
html:
    p "hello"
// @target css
style .foo:
    color "red"
"""
        sections = split_by_target(source)
        self.assertIn("html", sections)
        self.assertIn("css", sections)
        self.assertIn("fusion", sections)
        self.assertTrue(any("let x be 1" in l for l in sections["fusion"]))

    def test_split_hash_target(self):
        """Test that # @target also works."""
        source = """# @target python
let x be 1
"""
        sections = split_by_target(source)
        self.assertIn("python", sections)

    def test_is_programming_language(self):
        self.assertTrue(is_programming_language("python"))
        self.assertTrue(is_programming_language("js"))
        self.assertTrue(is_programming_language("react"))
        self.assertFalse(is_programming_language("html"))
        self.assertFalse(is_programming_language("json"))
        self.assertFalse(is_programming_language("css"))


class TestDataParser(unittest.TestCase):
    """Tests for the dedicated data value parser."""

    def test_parse_simple_dict(self):
        result = parse_data('{name: "FusionBoa", version: 1.0}')
        self.assertEqual(result, {"name": "FusionBoa", "version": 1.0})

    def test_parse_nested_dict(self):
        result = parse_data('{app: {name: "Test", enabled: true}}')
        self.assertEqual(result, {"app": {"name": "Test", "enabled": True}})

    def test_parse_list(self):
        result = parse_data('[1, 2, 3]')
        self.assertEqual(result, [1, 2, 3])

    def test_parse_keyword_keys(self):
        """Keys that are FusionBoa keywords should work."""
        result = parse_data('{in: 5, not: true, if: "maybe"}')
        self.assertEqual(result, {"in": 5, "not": True, "if": "maybe"})

    def test_parse_null_and_bool(self):
        result = parse_data('{a: null, b: true, c: false, d: none}')
        self.assertEqual(result, {"a": None, "b": True, "c": False, "d": None})

    def test_parse_empty(self):
        self.assertEqual(parse_data('{}'), {})
        self.assertEqual(parse_data('[]'), [])

    def test_parse_multi_line(self):
        source = """{
    name: "FusionBoa",
    version: 0.3,
    features: [1, 2, 3]
}"""
        result = parse_data(source)
        self.assertEqual(result["name"], "FusionBoa")
        self.assertEqual(result["version"], 0.3)
        self.assertEqual(result["features"], [1, 2, 3])

    def test_parse_with_comments(self):
        source = """{
    name: "FusionBoa",  # the name
    # this is a comment
    version: 1.0
}"""
        result = parse_data(source)
        self.assertEqual(result, {"name": "FusionBoa", "version": 1.0})


class TestHtmlGenerator(unittest.TestCase):
    """Tests for the HTML generator."""

    def test_simple_element(self):
        result = generate_html('h1 "Hello"')
        self.assertIn("<h1>", result)
        self.assertIn("Hello", result)
        self.assertIn("</h1>", result)

    def test_element_with_attrs(self):
        result = generate_html('div class "container" id "main"')
        self.assertIn('class="container"', result)
        self.assertIn('id="main"', result)

    def test_self_closing(self):
        result = generate_html('br/')
        self.assertIn("<br />", result)

    def test_void_element(self):
        result = generate_html('img src "pic.jpg" alt "Photo"')
        self.assertIn("<img", result)
        self.assertIn("src=\"pic.jpg\"", result)
        self.assertIn("/>", result)

    def test_nested_elements(self):
        source = """div class "container":
    p "Hello"
    span "World\""""
        result = generate_html(source)
        self.assertIn("<div", result)
        self.assertIn('class="container"', result)
        self.assertIn("<p>", result)
        self.assertIn("Hello", result)
        self.assertIn("</p>", result)
        self.assertIn("<span>", result)
        self.assertIn("World", result)
        self.assertIn("</div>", result)

    def test_trailing_colon_stripped(self):
        """Test that trailing : from FusionBoa block syntax is stripped."""
        source = """html:
    body:
        h1 "Test\""""
        result = generate_html(source)
        self.assertIn("<html>", result)
        self.assertIn("<body>", result)
        self.assertIn("<h1>", result)
        # Should NOT contain <html:> or <body:>
        self.assertNotIn("<html:", result)
        self.assertNotIn("<body:", result)

    def test_sibling_elements(self):
        """Test that elements at the same indent level are siblings."""
        source = """div:
    p "First"
    p "Second\""""
        result = generate_html(source)
        # Both p tags should be children of div
        self.assertIn("<div>", result)
        self.assertIn("First", result)
        self.assertIn("Second", result)
        self.assertIn("</div>", result)


class TestCssGenerator(unittest.TestCase):
    """Tests for the CSS generator."""

    def test_simple_rule(self):
        result = generate_css("""style .foo:
    color "red"
    font-size "16px\"""")
        self.assertIn(".foo", result)
        self.assertIn("color", result)
        self.assertIn("red", result)
        self.assertIn("font-size", result)
        self.assertIn("16px", result)

    def test_multiple_selectors(self):
        result = generate_css("""style .a:
    margin "0"
style #b:
    padding "10px\"""")
        self.assertIn(".a", result)
        self.assertIn("#b", result)


class TestJsonGenerator(unittest.TestCase):
    """Tests for the JSON generator."""

    def test_simple_dict(self):
        result = generate_json('{name: "FusionBoa", version: 1.0}')
        self.assertIn('"name"', result)
        self.assertIn('"FusionBoa"', result)
        self.assertIn('"version"', result)
        self.assertIn('1.0', result)

    def test_nested(self):
        result = generate_json('{a: {b: "c"}}')
        self.assertIn('"a"', result)
        self.assertIn('"b"', result)
        self.assertIn('"c"', result)

    def test_list(self):
        result = generate_json('[1, 2, 3]')
        self.assertIn("1", result)
        self.assertIn("2", result)
        self.assertIn("3", result)


class TestYamlGenerator(unittest.TestCase):
    """Tests for the YAML generator."""

    def test_simple(self):
        result = generate_yaml('{name: "FusionBoa"}')
        self.assertIn("name:", result)
        self.assertIn("FusionBoa", result)


class TestTomlGenerator(unittest.TestCase):
    """Tests for the TOML generator."""

    def test_simple(self):
        result = generate_toml('{name: "FusionBoa"}')
        self.assertIn("name =", result)
        self.assertIn('"FusionBoa"', result)


class TestXmlGenerator(unittest.TestCase):
    """Tests for the XML generator."""

    def test_simple_element(self):
        result = generate_xml('root "content"')
        self.assertIn("<?xml", result)
        self.assertIn("<root>", result)
        self.assertIn("content", result)

    def test_attrs(self):
        result = generate_xml('root version "1.0"')
        self.assertIn('version="1.0"', result)


class TestIniGenerator(unittest.TestCase):
    """Tests for the INI generator."""

    def test_simple(self):
        result = generate_ini('[section]\nname "FusionBoa"')
        self.assertIn("[section]", result)
        self.assertIn("name =", result)
        self.assertIn("FusionBoa", result)


class TestMarkdownGenerator(unittest.TestCase):
    """Tests for the Markdown generator."""

    def test_passthrough(self):
        result = generate_markdown("# Heading\n\nParagraph")
        self.assertIn("# Heading", result)
        self.assertIn("Paragraph", result)

    def test_heading_preserved(self):
        """Markdown # headings should NOT be stripped."""
        result = generate_markdown("# Title\n## Section\nContent")
        self.assertIn("# Title", result)
        self.assertIn("## Section", result)


class TestNewSyntaxFeatures(unittest.TestCase):
    """Tests for all newly added syntax features."""

    # === Destructuring Assignment ===

    def test_destructuring_list(self):
        """let [a, b] be [1, 2] should parse and codegen correctly."""
        source = 'let [a, b] be [1, 2]'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertEqual(stmt.__class__.__name__, "DestructuringDeclaration")
        self.assertEqual(stmt.targets, ["a", "b"])
        self.assertEqual(stmt.destructure_type, "list")
        # Python codegen: a, b = [1, 2]
        code = generate_python(ast)
        self.assertIn("a, b = [1, 2]", code)

    def test_destructuring_dict(self):
        """let {name, age} be user should parse and codegen."""
        source = 'let {name, age} be user'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertEqual(stmt.__class__.__name__, "DestructuringDeclaration")
        self.assertEqual(stmt.targets, ["name", "age"])
        self.assertEqual(stmt.destructure_type, "dict")
        # Python codegen: name, age = user['name'], user['age']
        code = generate_python(ast)
        self.assertIn("name, age = user['name'], user['age']", code)

    def test_destructuring_const(self):
        """const [a, b] be [1, 2] should work."""
        source = 'const [a, b] be [1, 2]'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertEqual(stmt.__class__.__name__, "DestructuringDeclaration")
        self.assertEqual(stmt.var_type, "constant")

    def test_destructuring_js_codegen(self):
        """let [a, b] be [1, 2] should generate correct JS (assignment, not let, to avoid redeclaration errors)."""
        source = 'let [a, b] be [1, 2]'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_javascript(ast)
        self.assertIn("a, b] = [1, 2]", code)

    def test_destructuring_dict_js_codegen(self):
        """let {name, age} be user should generate correct JS (wrapped in parens for assignment destructuring)."""
        source = 'let {name, age} be user'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_javascript(ast)
        self.assertIn("{name, age} = user", code)

    def test_destructuring_with_expression(self):
        """let [a, b] be get_values() should pass expression correctly."""
        source = 'let [a, b] be get_values()'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("a, b = get_values()", code)

    def test_destructuring_dict_from_call(self):
        """let {x, y} be get_point() should extract dict keys."""
        source = 'let {x, y} be get_point()'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("x, y = get_point()['x'], get_point()['y']", code)

    # === Generator Expressions ===

    def test_generator_expression(self):
        """(x for each x in items if x > 0) should parse."""
        source = 'let result be (x for each x in items if x > 0)'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertEqual(stmt.__class__.__name__, "VariableDeclaration")
        gen = stmt.value
        self.assertEqual(gen.__class__.__name__, "GeneratorExpression")
        self.assertEqual(gen.variable, "x")

    def test_generator_no_condition(self):
        """(x for each x in items) without condition."""
        source = 'let result be (x for each x in items)'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        gen = ast.statements[0].value
        self.assertEqual(gen.__class__.__name__, "GeneratorExpression")
        self.assertIsNone(gen.condition)

    def test_generator_python_codegen(self):
        """(x for each x in items if x > 0) -> (x for x in items if x > 0)"""
        source = 'let result be (x for each x in items if x > 0)'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        # Should generate a generator expression with for/filter
        self.assertIn("x for x in items", code)

    def test_generator_with_where(self):
        """(x for each x in items where x > 0)."""
        source = 'let result be (x for each x in items where x > 0)'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        gen = ast.statements[0].value
        self.assertEqual(gen.__class__.__name__, "GeneratorExpression")
        self.assertIsNotNone(gen.condition)

    def test_generator_in_variable(self):
        """Generator assigned to variable should work."""
        source = 'let gen be (x for each x in items if x > 0)'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        # Should generate a generator expression with for/filter
        self.assertIn("x for x in items", code)
        self.assertIn("if", code)
        self.assertIn("(x > 0)", code)

    # === Logical Assignment Operators ===

    def test_logical_or_assignment(self):
        """x ||= default should parse."""
        source = 'x ||= default'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertEqual(stmt.__class__.__name__, "AugmentedAssignment")
        self.assertEqual(stmt.operator, "||")

    def test_logical_or_assignment_python_codegen(self):
        """x ||= default -> x = x or default"""
        source = 'x ||= default'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("x = x or default", code)

    def test_logical_and_assignment(self):
        """x &&= value should parse."""
        source = 'x &&= value'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertEqual(stmt.__class__.__name__, "AugmentedAssignment")
        self.assertEqual(stmt.operator, "&&")

    def test_logical_and_assignment_python_codegen(self):
        """x &&= value -> x = x and value"""
        source = 'x &&= value'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("x = x and value", code)

    def test_nullish_coalescing_assignment(self):
        """x ??= default should parse."""
        source = 'x ??= default'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertEqual(stmt.__class__.__name__, "AugmentedAssignment")
        self.assertEqual(stmt.operator, "??")

    def test_nullish_coalescing_assignment_python_codegen(self):
        """x ??= default -> x = x if x is not None else default"""
        source = 'x ??= default'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("x is not None else default", code)

    # === Lexer Tests for New Operators ===

    def test_lexer_pipe_pipe_equal(self):
        """||= should tokenize as PIPE_PIPE_EQUAL."""
        source = 'x ||= default'
        tokens = tokenize(source)
        self.assertTrue(any(t.type.name == "PIPE_PIPE_EQUAL" for t in tokens))

    def test_lexer_ampersand_ampersand_equal(self):
        """&&= should tokenize as AMPERSAND_AMPERSAND_EQUAL."""
        source = 'x &&= value'
        tokens = tokenize(source)
        self.assertTrue(any(t.type.name == "AMPERSAND_AMPERSAND_EQUAL" for t in tokens))

    def test_lexer_question_question_equal(self):
        """??= should tokenize as QUESTION_QUESTION_EQUAL."""
        source = 'x ??= default'
        tokens = tokenize(source)
        self.assertTrue(any(t.type.name == "QUESTION_QUESTION_EQUAL" for t in tokens))

    def test_lexer_pipe_pipe(self):
        """|| should tokenize as PIPE_PIPE."""
        source = 'x || y'
        tokens = tokenize(source)
        self.assertTrue(any(t.type.name == "PIPE_PIPE" for t in tokens))

    def test_lexer_ampersand_ampersand(self):
        """&& should tokenize as AMPERSAND_AMPERSAND."""
        source = 'x && y'
        tokens = tokenize(source)
        self.assertTrue(any(t.type.name == "AMPERSAND_AMPERSAND" for t in tokens))

    # === String Method Codegen ===

    def test_capitalize_string_method(self):
        """capitalize text -> text.capitalize()"""
        source = 'let result be capitalize text'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("text.capitalize()", code)

    def test_title_string_method(self):
        """title text -> text.title()"""
        source = 'let result be title text'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("text.title()", code)

    def test_swapcase_string_method(self):
        """swapcase text -> text.swapcase()"""
        source = 'let result be swapcase text'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("text.swapcase()", code)

    # === Type Annotations ===

    def test_type_annotation_variable(self):
        """let x be integer should parse as variable with type."""
        source = 'let x be integer'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertEqual(stmt.__class__.__name__, "VariableDeclaration")
        val = stmt.value
        self.assertEqual(val.__class__.__name__, "Identifier")
        self.assertEqual(val.name, "integer")
        # Should generate: x = int (integer is used as identifier for the type)
        code = generate_python(ast)
        self.assertIn("x = integer", code)

    def test_type_annotation_is_check(self):
        """x is a string should check isinstance."""
        source = 'if x is a string:\n    print "yes"'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        self.assertEqual(ast.statements[0].__class__.__name__, "IfStatement")

    # === Edge Cases ===

    def test_destructuring_with_multiple_vars(self):
        """let [a, b, c] be [1, 2, 3] should work."""
        source = 'let [a, b, c] be [1, 2, 3]'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        stmt = ast.statements[0]
        self.assertEqual(stmt.targets, ["a", "b", "c"])
        code = generate_python(ast)
        self.assertIn("a, b, c = [1, 2, 3]", code)

    def test_destructuring_dict_multiple(self):
        """let {x, y, z} be point -> x = point['x'], y = point['y'], z = point['z']"""
        source = 'let {x, y, z} be point'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("x, y, z = point['x'], point['y'], point['z']", code)

    def test_logical_assignment_chaining(self):
        """Multiple logical assignments should all work."""
        source = 'x ||= a\ny &&= b\nz ??= c'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 3)
        code = generate_python(ast)
        self.assertIn("x = x or a", code)
        self.assertIn("y = y and b", code)
        self.assertIn("z = z if z is not None else c", code)

    def test_pipe_operator_robustness(self):
        """x |> f |> g |> h should chain correctly."""
        source = 'let result be x |> f |> g |> h'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("h(g(f(x)))", code)

    def test_unique_expression(self):
        """unique items -> list(set(items))"""
        source = 'let result be unique items'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("list(set(items))", code)

    def test_compact_expression(self):
        """compact items -> [i for i in items if i]"""
        source = 'let result be compact items'
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        code = generate_python(ast)
        self.assertIn("for i in items if i", code)


class TestNullCoalescingAllLang(unittest.TestCase):
    """Tests for binary ?? null-coalescing operator across ALL language generators."""

    def _parse(self, source):
        return Parser(tokenize(source)).parse()

    def test_parse_nco_binary(self):
        """a ?? b should parse as binary operation."""
        source = 'let result be x ?? "default"'
        ast = self._parse(source)
        stmt = ast.statements[0]
        self.assertEqual(stmt.value.__class__.__name__, "BinaryOp")
        self.assertEqual(stmt.value.operator, "??")

    # --- Python ---
    def test_nco_python(self):
        """Python: a ?? b -> a if a is not None else b"""
        source = 'let result be x ?? "default"'
        code = generate_python(self._parse(source))
        self.assertIn("x is not None else 'default'", code)

    def test_nco_python_complex(self):
        """Python: a ?? b ?? c should chain."""
        source = 'let result be a ?? b ?? c'
        code = generate_python(self._parse(source))
        self.assertIn("is not None", code)

    # --- JavaScript ---
    def test_nco_javascript(self):
        """JS: a ?? b should use native ??"""
        source = 'let result be x ?? "default"'
        code = generate_javascript(self._parse(source))
        self.assertIn("??", code)

    # --- C++ ---
    def test_nco_cpp(self):
        """C++: a ?? b -> (a ? a : b)"""
        source = 'let result be x ?? "default"'
        code = generate_cpp(self._parse(source))
        self.assertIn("?", code)
        self.assertIn(":", code)

    # --- Go ---
    def test_nco_go(self):
        """Go: a ?? b should generate func wrapper."""
        source = 'let result be x ?? "default"'
        code = generate_go(self._parse(source))
        self.assertIn("func()", code)
        self.assertIn("!= nil", code)

    # --- Java ---
    def test_nco_java(self):
        """Java: a ?? b -> a != null ? a : b"""
        source = 'let result be x ?? "default"'
        code = generate_java(self._parse(source))
        self.assertIn("!= null ?", code)

    # --- Lua ---
    def test_nco_lua(self):
        """Lua: a ?? b -> a ~= nil and a or b"""
        source = 'let result be x ?? "default"'
        code = generate_lua(self._parse(source))
        self.assertIn("~= nil", code)
        self.assertIn("and", code)

    # --- R ---
    def test_nco_r(self):
        """R: a ?? b -> ifelse(is.null(a), b, a)"""
        source = 'let result be x ?? "default"'
        code = generate_r(self._parse(source))
        self.assertIn("ifelse", code)
        self.assertIn("is.null", code)

    # --- Julia ---
    def test_nco_julia(self):
        """Julia: a ?? b -> something(a, b)"""
        source = 'let result be x ?? "default"'
        code = generate_julia(self._parse(source))
        self.assertIn("something", code)

    # --- Rust ---
    def test_nco_rust(self):
        """Rust: a ?? b -> a.unwrap_or(b)"""
        source = 'let result be x ?? "default"'
        code = generate_rust(self._parse(source))
        self.assertIn("unwrap_or", code)

    # --- Ruby ---
    def test_nco_ruby(self):
        """Ruby: a ?? b -> (a || b)"""
        source = 'let result be x ?? "default"'
        code = generate_ruby(self._parse(source))
        self.assertIn("||", code)

    # --- Kotlin ---
    def test_nco_kotlin(self):
        """Kotlin: a ?? b -> a ?: b"""
        source = 'let result be x ?? "default"'
        code = generate_kotlin(self._parse(source))
        self.assertIn("?:", code)

    # --- C# ---
    def test_nco_csharp(self):
        """C#: a ?? b should use native ??"""
        source = 'let result be x ?? "default"'
        code = generate_csharp(self._parse(source))
        self.assertIn("??", code)

    # --- TypeScript ---
    def test_nco_typescript(self):
        """TypeScript: a ?? b should use native ??"""
        source = 'let result be x ?? "default"'
        code = generate_typescript(self._parse(source))
        self.assertIn("??", code)


class TestPipeOperatorAllLang(unittest.TestCase):
    """Tests pipe operator with special keywords (first, last, sort, reverse) across generators."""

    def _parse(self, source):
        return Parser(tokenize(source)).parse()

    def test_pipe_first_python(self):
        """x |> first -> x[0] in Python"""
        source = 'let result be data |> first'
        code = generate_python(self._parse(source))
        self.assertIn("[0]", code)

    def test_pipe_last_python(self):
        """x |> last -> x[-1] in Python"""
        source = 'let result be data |> last'
        code = generate_python(self._parse(source))
        self.assertIn("[-1]", code)

    def test_pipe_sort_python(self):
        """x |> sort -> list(sorted(x)) in Python"""
        source = 'let result be data |> sort'
        code = generate_python(self._parse(source))
        self.assertIn("sorted", code)

    def test_pipe_reverse_python(self):
        """x |> reverse -> list(reversed(x)) in Python"""
        source = 'let result be data |> reverse'
        code = generate_python(self._parse(source))
        self.assertIn("reversed", code)

    def test_pipe_unique_python(self):
        """x |> unique -> list(set(x)) in Python"""
        source = 'let result be data |> unique'
        code = generate_python(self._parse(source))
        self.assertIn("list(set", code)

    def test_pipe_compact_python(self):
        """x |> compact -> [i for i in x if i] in Python"""
        source = 'let result be data |> compact'
        code = generate_python(self._parse(source))
        self.assertIn("for i in", code)

    def test_pipe_chained_special(self):
        """x |> sort |> reverse |> first should chain correctly."""
        source = 'let result be data |> sort |> reverse |> first'
        code = generate_python(self._parse(source))
        self.assertIn("sorted", code)
        self.assertIn("reversed", code)
        self.assertIn("[0]", code)

    def test_pipe_first_javascript(self):
        """x |> first -> data[0] in JavaScript (pipe operator resolves special keywords)."""
        source = 'let result be data |> first'
        code = generate_javascript(self._parse(source))
        self.assertIn("data[0]", code)

    def test_pipe_sort_cpp(self):
        """C++: x |> sort should generate valid code."""
        source = 'let result be data |> sort'
        code = generate_cpp(self._parse(source))
        self.assertIn("sort", code)

    def test_pipe_first_go(self):
        """Go: x |> first should generate valid code."""
        source = 'let result be data |> first'
        code = generate_go(self._parse(source))
        self.assertIn("first", code)

    def test_pipe_last_java(self):
        """Java: x |> last should generate valid code."""
        source = 'let result be data |> last'
        code = generate_java(self._parse(source))
        self.assertIn("last", code)

    def test_pipe_sort_lua(self):
        """Lua: x |> sort should generate valid code."""
        source = 'let result be data |> sort'
        code = generate_lua(self._parse(source))
        self.assertIn("sort", code)

    def test_pipe_first_r(self):
        """R: x |> first should generate valid code."""
        source = 'let result be data |> first'
        code = generate_r(self._parse(source))
        self.assertIn("first", code)


class TestCrossLanguageSanity(unittest.TestCase):
    """Tests that basic fusion code compiles across all supported languages."""

    def _parse(self, source):
        return Parser(tokenize(source)).parse()

    def _assert_compiles(self, gen_func, source, target_name):
        """Helper: verify code generation doesn't crash."""
        try:
            code = gen_func(self._parse(source))
            self.assertTrue(len(code) > 0, f"{target_name}: should generate code")
            return code
        except Exception as e:
            self.fail(f"{target_name}: generation failed with {e}")

    BASIC_SOURCE = 'let x be 42\nlet y be 10\nlet z be x + y\nprint z'
    IF_SOURCE = 'let score be 85\nif score >= 80:\n    print "pass"\nor:\n    print "fail"'
    FOR_SOURCE = 'for each i in [1, 2, 3]:\n    print i'
    FUNC_SOURCE = 'define function add with a, b:\n    return a + b\nlet result be add(3, 4)'
    WHILE_SOURCE = 'let count be 3\nwhile count > 0:\n    decrease count by 1'
    TERNARY_SOURCE = 'let status be "adult" if 20 >= 18 else "minor"'
    DESTRUCTURE_SOURCE = 'let pair be [10, 20]\nlet [a, b] be pair'

    def test_python_basic(self):
        self._assert_compiles(generate_python, self.BASIC_SOURCE, "Python")

    def test_javascript_basic(self):
        self._assert_compiles(generate_javascript, self.BASIC_SOURCE, "JavaScript")

    def test_cpp_basic(self):
        self._assert_compiles(generate_cpp, self.BASIC_SOURCE, "C++")

    def test_go_basic(self):
        self._assert_compiles(generate_go, self.BASIC_SOURCE, "Go")

    def test_java_basic(self):
        self._assert_compiles(generate_java, self.BASIC_SOURCE, "Java")

    def test_lua_basic(self):
        self._assert_compiles(generate_lua, self.BASIC_SOURCE, "Lua")

    def test_r_basic(self):
        self._assert_compiles(generate_r, self.BASIC_SOURCE, "R")

    def test_julia_basic(self):
        self._assert_compiles(generate_julia, self.BASIC_SOURCE, "Julia")

    def test_rust_basic(self):
        self._assert_compiles(generate_rust, self.BASIC_SOURCE, "Rust")

    def test_ruby_basic(self):
        self._assert_compiles(generate_ruby, self.BASIC_SOURCE, "Ruby")

    def test_kotlin_basic(self):
        self._assert_compiles(generate_kotlin, self.BASIC_SOURCE, "Kotlin")

    def test_swift_basic(self):
        self._assert_compiles(generate_swift, self.BASIC_SOURCE, "Swift")

    def test_csharp_basic(self):
        self._assert_compiles(generate_csharp, self.BASIC_SOURCE, "C#")

    def test_typescript_basic(self):
        self._assert_compiles(generate_typescript, self.BASIC_SOURCE, "TypeScript")

    # --- If/Else across languages ---
    def test_python_if(self):
        self._assert_compiles(generate_python, self.IF_SOURCE, "Python-if")

    def test_javascript_if(self):
        self._assert_compiles(generate_javascript, self.IF_SOURCE, "JavaScript-if")

    def test_cpp_if(self):
        self._assert_compiles(generate_cpp, self.IF_SOURCE, "C++-if")

    def test_java_if(self):
        self._assert_compiles(generate_java, self.IF_SOURCE, "Java-if")

    def test_go_if(self):
        self._assert_compiles(generate_go, self.IF_SOURCE, "Go-if")

    # --- For loop across languages ---
    def test_python_for(self):
        self._assert_compiles(generate_python, self.FOR_SOURCE, "Python-for")

    def test_javascript_for(self):
        self._assert_compiles(generate_javascript, self.FOR_SOURCE, "JavaScript-for")

    def test_cpp_for(self):
        self._assert_compiles(generate_cpp, self.FOR_SOURCE, "C++-for")

    def test_java_for(self):
        self._assert_compiles(generate_java, self.FOR_SOURCE, "Java-for")

    # --- Function definition across languages ---
    def test_python_func(self):
        self._assert_compiles(generate_python, self.FUNC_SOURCE, "Python-func")

    def test_javascript_func(self):
        self._assert_compiles(generate_javascript, self.FUNC_SOURCE, "JavaScript-func")

    def test_cpp_func(self):
        self._assert_compiles(generate_cpp, self.FUNC_SOURCE, "C++-func")

    def test_go_func(self):
        self._assert_compiles(generate_go, self.FUNC_SOURCE, "Go-func")

    def test_lua_func(self):
        self._assert_compiles(generate_lua, self.FUNC_SOURCE, "Lua-func")

    # --- While loop across languages ---
    def test_python_while(self):
        self._assert_compiles(generate_python, self.WHILE_SOURCE, "Python-while")

    def test_javascript_while(self):
        self._assert_compiles(generate_javascript, self.WHILE_SOURCE, "JavaScript-while")

    def test_cpp_while(self):
        self._assert_compiles(generate_cpp, self.WHILE_SOURCE, "C++-while")

    # --- Ternary across languages ---
    def test_python_ternary(self):
        self._assert_compiles(generate_python, self.TERNARY_SOURCE, "Python-ternary")

    def test_javascript_ternary(self):
        self._assert_compiles(generate_javascript, self.TERNARY_SOURCE, "JavaScript-ternary")

    def test_cpp_ternary(self):
        self._assert_compiles(generate_cpp, self.TERNARY_SOURCE, "C++-ternary")

    # --- Destructuring across languages ---
    def test_python_destructure(self):
        self._assert_compiles(generate_python, self.DESTRUCTURE_SOURCE, "Python-destructure")

    def test_javascript_destructure(self):
        self._assert_compiles(generate_javascript, self.DESTRUCTURE_SOURCE, "JavaScript-destructure")

    def test_lua_destructure(self):
        self._assert_compiles(generate_lua, self.DESTRUCTURE_SOURCE, "Lua-destructure")

    def test_rust_destructure(self):
        code = generate_rust(self._parse(self.DESTRUCTURE_SOURCE))
        self.assertTrue(len(code) > 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
