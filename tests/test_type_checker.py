"""Type checker tests — validate semantic analysis on AST."""
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fusionboa_lang.lexer.lexer import tokenize
from fusionboa_lang.parser.parser import Parser
from fusionboa_lang.semantic.type_checker import TypeChecker


class TestTypeChecker(unittest.TestCase):
    """Test the semantic type checker."""

    def _check(self, source: str):
        """Parse source and run type checker, return errors."""
        tokens = tokenize(source)
        ast = Parser(tokens).parse()
        checker = TypeChecker(ast)
        return checker.check()

    def test_no_errors_on_valid_code(self):
        errors = self._check("let x be 5\nlet name be \"hello\"\nprint x")
        self.assertEqual(len(errors), 0, f"Unexpected errors: {errors}")

    def test_type_mismatch_warning(self):
        """Reassigning variable to different type should warn."""
        errors = self._check("let x be 5\nset x to \"hello\"")
        type_warnings = [e for e in errors if e.severity == "warning"]
        self.assertGreater(len(type_warnings), 0, "Expected type mismatch warning")

    def test_record_valid_types(self):
        """Records with valid field types."""
        errors = self._check("define record Point with x: int, y: int")
        record_errors = [e for e in errors if "unknown field type" in e.message.lower()]
        self.assertEqual(len(record_errors), 0, f"Unexpected record errors: {record_errors}")

    def test_empty_program(self):
        """Empty program should produce no errors."""
        errors = self._check("")
        self.assertEqual(len(errors), 0)

    def test_type_inference_literal_int(self):
        tokens = tokenize("let x be 42")
        ast = Parser(tokens).parse()
        checker = TypeChecker(ast)
        t = checker._infer_type(ast.statements[0].value)
        self.assertEqual(t, "int")

    def test_type_inference_literal_string(self):
        tokens = tokenize('let x be "hello"')
        ast = Parser(tokens).parse()
        checker = TypeChecker(ast)
        t = checker._infer_type(ast.statements[0].value)
        self.assertEqual(t, "string")

    def test_type_inference_literal_bool(self):
        tokens = tokenize("let x be true")
        ast = Parser(tokens).parse()
        checker = TypeChecker(ast)
        t = checker._infer_type(ast.statements[0].value)
        self.assertEqual(t, "bool")

    def test_type_inference_list(self):
        tokens = tokenize("let x be [1, 2, 3]")
        ast = Parser(tokens).parse()
        checker = TypeChecker(ast)
        t = checker._infer_type(ast.statements[0].value)
        self.assertEqual(t, "list")

    def test_type_inference_dict(self):
        tokens = tokenize("let x be {a: 1, b: 2}")
        ast = Parser(tokens).parse()
        checker = TypeChecker(ast)
        t = checker._infer_type(ast.statements[0].value)
        self.assertEqual(t, "dict")

    def test_types_compatible(self):
        checker = TypeChecker(None)
        self.assertTrue(checker._types_compatible("int", "any"))
        self.assertTrue(checker._types_compatible("string", "Union[string, int]"))


if __name__ == "__main__":
    unittest.main()
