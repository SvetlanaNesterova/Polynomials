import unittest
import polynomials_parser


class TestPolynom(unittest.TestCase):
    def setUp(self):
        self.parser = polynomials_parser.Parser()

    def test_brackets(self):
        self.assertTrue(polynomials_parser.contains_correct_bracket_sequence("()"))
        self.assertTrue(polynomials_parser.contains_correct_bracket_sequence("(()(()()))()(())"))

        self.assertFalse(polynomials_parser.contains_correct_bracket_sequence("(()"))
        self.assertFalse(polynomials_parser.contains_correct_bracket_sequence("())"))
        self.assertFalse(polynomials_parser.contains_correct_bracket_sequence(")("))

    def test_form_lexemes(self):
        values = []
        results = []
        values.append("1+a")
        results.append(['1', '+', 'a'])

        values.append("-10")
        results.append(['-1', '*', '10'])

        values.append("200^345")
        results.append(['200', '^', '345'])

        values.append("a*(b+c)")
        results.append(['a', '*', '(', 'b', '+', 'c', ')'])

        values.append("(x-b)*-2")
        results.append(['(', 'x', '-', 'b', ')', '*', '-1', '*', '2'])

        values.append("ac")
        results.append(['a', '*', 'c'])

        values.append("x-(x-y)")
        results.append(['x', '-', '(', 'x', '-', 'y', ')'])

        values.append("-(x-y)")
        results.append(['-1', '*', '(', 'x', '-', 'y', ')'])

        values.append("(xy)(-x*-y)")
        results.append(['(', 'x', '*', 'y', ')', '*', '(', '-1', '*', 'x', '*', '-1', '*', 'y', ')'])

        values.append("(-(-(-2)))")
        results.append(['(', '-1', '*', '(', '-1', '*', '(', '-1', '*', '2', ')', ')', ')'])

        for val, expected in zip(values, results):
            actual = polynomials_parser.form_lexemes(val)
            self.assertListEqual(expected, actual)

    def test_to_postfix(self):
        values = []
        results = []

        values.append(['1', '+', 'a'])
        results.append(['1', 'a', '+'])

        values.append(['-1', '*', '10'])
        results.append(['-1', '10', '*'])

        values.append(['200', '^', 'c'])
        results.append(['200', 'c', '^'])

        values.append(['a', '*', '(', 'b', '+', 'c', ')'])
        results.append(['a', 'b', 'c', '+', '*'])

        values.append(['(', 'x', '-', 'b', ')', '*', '-1', '*', '2'])
        results.append(['x', 'b', '-', '-1', '*', '2', '*'])

        values.append(['a', '-', 'c', '*', 'b'])
        results.append(['a', 'c', 'b', '*', '-'])

        values.append(['a', '*', 'c', '*', 'b'])
        results.append(['a', 'c', '*', 'b', '*'])

        values.append(['x', '-', '(', 'x', '-', 'y', ')'])
        results.append(['x', 'x', 'y', '-', '-'])

        values.append(['a', '^', 'c', '^', 'b'])
        results.append(['a', 'c', 'b', '^', '^'])

        values.append(['(', 'x', '-', 'y', ')', '*', '(', 'x', '^', 'y', ')'])
        results.append(['x', 'y', '-', 'x', 'y', '^', '*'])

        for val, expected in zip(values, results):
            actual = self.parser.to_postfix(val)
            self.assertListEqual(expected, actual)

    def test_simple_single_monoms_parse(self):
        values = [
            "1",
            "100",
            "x",
            "-a",
            "a*b",
            "a^2",
            "3*t",
            "a^2",
            "x^3*y^4",
            "a^100*b^100",
            "a*b^2*c^3",
            "15*a^3*b^2*c",
        ]
        for source in values:
            monoms = self.parser.parse(source)
            monom = monoms[0]
            self.assertEqual(str(monom), source)
