"""Integration tests for FusionBoa — end-to-end parse→compile→verify.

Tests the full pipeline: lexer → parser → codegen for each major target.
Uses syntax that the lexer can actually tokenize correctly.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fusionboa_lang.lexer.lexer import tokenize
from fusionboa_lang.parser.parser import Parser
from fusionboa_lang.codegen.python_gen import PythonGenerator
from fusionboa_lang.codegen.javascript_gen import JavaScriptGenerator
from fusionboa_lang.codegen.typescript_gen import TypeScriptGenerator
from fusionboa_lang.codegen.go_gen import GoGenerator


class TestEndToEndPipeline(unittest.TestCase):
    """Test the full lex→parse→codegen pipeline for each major target."""

    def _compile(self, source: str, target: str) -> str:
        tokens = tokenize(source)
        ast = Parser(tokens).parse()
        generators = {
            "py": PythonGenerator,
            "js": JavaScriptGenerator,
            "ts": TypeScriptGenerator,
            "go": GoGenerator,
        }
        gen = generators[target](ast)
        return gen.generate()

    # ---- Python ---- 

    def test_python_hello(self):
        code = self._compile("let name be \"FusionBoa\"\nprint \"Hello\"", "py")
        self.assertIn("print", code)
        self.assertIn("FusionBoa", code)

    def test_python_function(self):
        code = self._compile("define function add with a, b:\n    return a + b", "py")
        self.assertIn("def add(a, b)", code)
        self.assertIn("return", code)

    def test_python_class(self):
        code = self._compile("define class Animal:\n    define function init with name:\n        set this.name to name", "py")
        self.assertIn("class Animal", code)
        self.assertIn("self.name = name", code)

    def test_python_empty(self):
        code = self._compile("", "py")
        self.assertEqual(code, "")

    # ---- JavaScript ----

    def test_javascript_variable(self):
        code = self._compile("let x be 42\nprint x", "js")
        self.assertIn("let x = 42;", code)
        self.assertIn("console.log", code)

    def test_javascript_function(self):
        code = self._compile("define function timesTwo with n:\n    return n * 2", "js")
        self.assertIn("function timesTwo(n)", code)
        self.assertIn("return (n * 2);", code)

    def test_javascript_empty(self):
        code = self._compile("", "js")
        self.assertEqual(code, "")

    # ---- TypeScript ----

    def test_typescript_variable(self):
        code = self._compile("let count be 10\nconst PI be 3.14", "ts")
        self.assertIn("let count = 10", code)
        self.assertIn("const PI", code)

    def test_typescript_empty(self):
        code = self._compile("", "ts")
        self.assertEqual(code, "")

    # ---- Go ----

    def test_go_hello(self):
        code = self._compile("let x be 42\nprint x", "go")
        self.assertIn("package main", code)
        self.assertIn("fmt.Println", code)
        self.assertIn("func main()", code)

    def test_go_empty(self):
        code = self._compile("", "go")
        self.assertIn("package main", code)  # Go always has package

    # ---- v0.9.1 Features (test with real generated code) ----

    def test_python_generates_v0_9_1_handlers(self):
        """Verify Python gen has v0.9.1 handler methods (not Unknown fallback)."""
        # Check the class has the new methods
        self.assertTrue(hasattr(PythonGenerator, '_gen_set_literal'))
        self.assertTrue(hasattr(PythonGenerator, '_gen_multi_return'))

    def test_javascript_generates_v0_9_1_handlers(self):
        """Verify JS gen has v0.9.1 handler methods."""
        self.assertTrue(hasattr(JavaScriptGenerator, '_gen_set_literal'))
        self.assertTrue(hasattr(JavaScriptGenerator, '_gen_multi_return'))

    def test_typescript_generates_v0_9_1_handlers(self):
        """Verify TS gen has v0.9.1 handler methods."""
        self.assertTrue(hasattr(TypeScriptGenerator, '_gen_set_literal'))
        self.assertTrue(hasattr(TypeScriptGenerator, '_gen_multi_return'))

    def test_go_generates_v0_9_1_handlers(self):
        """Verify Go gen has v0.9.1 goroutine/channel handlers."""
        self.assertTrue(hasattr(GoGenerator, '_gen_go_statement'))
        self.assertTrue(hasattr(GoGenerator, '_gen_channel_declaration'))
        self.assertTrue(hasattr(GoGenerator, '_gen_channel_select'))


if __name__ == "__main__":
    unittest.main()
