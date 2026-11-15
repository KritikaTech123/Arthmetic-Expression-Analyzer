import unittest

from expr_analyzer.analyzer import analyze, analyze_safe
from expr_analyzer.converter import postfix, prefix
from expr_analyzer.lexer import ExprError, tokenize
from expr_analyzer.parser import parse
from expr_analyzer.evaluator import evaluate


def result(expression: str):
    return evaluate(parse(tokenize(expression)))[0]


class AnalyzerTests(unittest.TestCase):
    def test_arithmetic_results(self):
        cases = {
            "1+2": 3, "2+3*4": 14, "(2+3)*4": 20, "10-4-3": 3,
            "100/10/5": 2, "2^3^2": 512, "-3+5": 2, "1.5*2": 3,
            "10%3": 1, "(3 + 4) * 2 - 8 / 4 ^ 2": 13.5,
        }
        for expression, expected in cases.items():
            with self.subTest(expression=expression):
                self.assertEqual(result(expression), expected)

    def test_conversions(self):
        tree = parse(tokenize("(3+4)*2"))
        self.assertEqual(postfix(tree), "3 4 + 2 *")
        self.assertEqual(prefix(tree), "* + 3 4 2")

    def test_token_shape(self):
        tokens = tokenize("12 + 3")
        self.assertEqual((tokens[0].lexeme, tokens[0].type, tokens[0].position), ("12", "NUMBER", 0))

    def test_report_contains_sections(self):
        report = analyze("1+2")
        for section in ("TOKEN TABLE", "SYNTAX TREE", "POSTFIX:", "THREE-ADDRESS CODE",
                        "STATISTICS", "EVALUATION STEPS", "RESULT: 3"):
            self.assertIn(section, report)

    def assert_error(self, expression: str, message: str):
        with self.assertRaises(ExprError) as context:
            result(expression)
        self.assertIn(message, str(context.exception))

    def test_invalid_character(self):
        self.assert_error("2 & 3", "invalid character")

    def test_malformed_number(self):
        self.assert_error("1.2.3", "malformed number")

    def test_unbalanced_parentheses(self):
        self.assert_error("(2+3", "missing closing bracket")
        self.assert_error("2+3)", "extra closing bracket")

    def test_missing_operand(self):
        self.assert_error("2 * * 3", "missing operand")
        self.assert_error("2 +", "missing operand")

    def test_empty_expression(self):
        self.assert_error("   ", "empty expression")

    def test_empty_parentheses(self):
        self.assert_error("()", "empty parentheses")

    def test_two_numbers(self):
        self.assert_error("2 3", "two operands")

    def test_division_by_zero(self):
        self.assert_error("4/0", "division by zero")

    def test_modulo_by_zero(self):
        self.assert_error("4%0", "modulo by zero")

    def test_overflow(self):
        self.assert_error("10^10000", "overflow")

    def test_safe_errors_have_no_traceback(self):
        self.assertTrue(analyze_safe("2 +").startswith("Error:"))

    def test_addition(self): self.assertEqual(result("7+8"), 15)
    def test_subtraction(self): self.assertEqual(result("7-8"), -1)
    def test_multiplication(self): self.assertEqual(result("7*8"), 56)
    def test_division(self): self.assertEqual(result("7/2"), 3.5)
    def test_modulo(self): self.assertEqual(result("7%2"), 1)
    def test_power(self): self.assertEqual(result("2^5"), 32)
    def test_nested_parentheses(self): self.assertEqual(result("((2))"), 2)
    def test_unary_plus(self): self.assertEqual(result("+4"), 4)
    def test_double_unary(self): self.assertEqual(result("--4"), 4)
    def test_spaces(self): self.assertEqual(result(" 1 + 2 "), 3)
    def test_decimal_addition(self): self.assertEqual(result("0.25+0.75"), 1.0)
    def test_decimal_subtraction(self): self.assertEqual(result("5.5-2"), 3.5)
    def test_tree_branch_characters(self): self.assertIn("├──", analyze("1+2"))
    def test_three_address_result(self): self.assertIn("result = t", analyze("1+2"))
    def test_statistics_operands(self): self.assertIn("Operands: 2", analyze("1+2"))
    def test_statistics_operators(self): self.assertIn("Operators: 1", analyze("1+2"))


if __name__ == "__main__":
    unittest.main()
