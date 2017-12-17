import unittest
from polynomial_parser import Parser

if __name__ == "__main__":
    unittest.main()

class TestPolynomial(unittest.TestCase):
    def test_brackets(self):
        self.assertTrue(Parser._contains_correct_bracket_sequence("()"))
        self.assertTrue(Parser._contains_correct_bracket_sequence(
            "(()(()()))()(())"))

        self.assertFalse(Parser._contains_correct_bracket_sequence("(()"))
        self.assertFalse(Parser._contains_correct_bracket_sequence("())"))
        self.assertFalse(Parser._contains_correct_bracket_sequence(")("))

        self.assertRaises(ValueError, Parser.parse, ")(")


    def test_form_lexemes(self):
        """Expression should be without spaces"""
        values = []
        results = []
        values.append("1+a")
        results.append(['1', '+', 'a'])

        values.append("-10")
        results.append(['-1', '*', '10'])

        values.append("1.05")
        results.append(['1.05'])

        values.append("200^345")
        results.append(['200', '^', '345'])

        values.append("20^-345")
        results.append(['20', '^', '-1', '^', '345'])

        values.append("0.9*12.33/0.05")
        results.append(['0.9', '*', '12.33', '/', '0.05'])

        values.append("a/-8.9")
        results.append(['a', '/', '-1', '/', '8.9'])

        values.append("a*(b+c)")
        results.append(['a', '*', '(', 'b', '+', 'c', ')'])

        values.append("(b+c)/12")
        results.append(['(', 'b', '+', 'c', ')', '/', '12'])

        values.append("(x-b)*-2")
        results.append(['(', 'x', '-', 'b', ')', '*', '-1', '*', '2'])

        values.append("ac")
        results.append(['a', '*', 'c'])

        values.append("a^b^c")
        results.append(['a', '^', 'b', '^', 'c'])

        values.append("a/b/c")
        results.append(['a', '/', 'b', '/', 'c'])

        values.append("a^-b^-c")
        results.append(['a', '^', '-1', '^', 'b', '^', '-1', '^', 'c'])

        values.append("a/-b/-c")
        results.append(['a', '/', '-1', '/', 'b', '/', '-1',  '/', 'c'])

        values.append("x-(x-y)")
        results.append(['x', '-', '(', 'x', '-', 'y', ')'])

        values.append("-(x-y)")
        results.append(['-1', '*', '(', 'x', '-', 'y', ')'])

        values.append("(xy)(-x*-y)")
        results.append(['(', 'x', '*', 'y', ')', '*', '(', '-1',
                        '*', 'x', '*', '-1', '*', 'y', ')'])

        values.append("(-(-(-2)))")
        results.append(['(', '-1', '*', '(', '-1', '*', '(', '-1',
                        '*', '2', ')', ')', ')'])

        for val, expected in zip(values, results):
            actual = Parser._form_lexemes(val)
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

        values.append(['a', '/', 'c', '/', 'b'])
        results.append(['a', 'c', '/', 'b', '/'])

        values.append(['x', '-', '(', 'x', '-', 'y', ')'])
        results.append(['x', 'x', 'y', '-', '-'])

        values.append(['a', '^', 'c', '^', 'b'])
        results.append(['a', 'c', 'b', '^', '^'])

        values.append(['(', 'x', '-', 'y', ')', '*', '(', 'x', '^', 'y', ')'])
        results.append(['x', 'y', '-', 'x', 'y', '^', '*'])

        for val, expected in zip(values, results):
            actual = Parser._to_postfix(val)
            self.assertListEqual(expected, actual)

    def test_simple_single_monomials_parse(self):
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
            monomials = Parser.parse(source)
            monomial = monomials[0]
            self.assertEqual(str(monomial), source)

    def test_simple_polynomials_parse(self):
        values = [
            "a*b*c + a*b*c",
            "2abc",
            "a^2b^2+b^2*a^2",
            "acc-3c^2*a",
            "a^3/a^5"
        ]
        results = [
            "2*a*b*c",
            "2*a*b*c",
            "2*a^2*b^2",
            "-2*a*c^2",
            "a^(-2)"
        ]
        for source, result in zip(values, results):
            monomials = Parser.parse(source)
            monomial = monomials[0]
            self.assertEqual(str(monomial), result)
