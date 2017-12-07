import unittest
from polynomials import Polynomials


class TestPolynomial(unittest.TestCase):
    def test_polynomial_to_str_sorts_monomials_in_classical_order(self):
        pol = Polynomials("a + 123456 + x^2 + x*y + y*x*z")
        self.assertEqual(str(pol), "x*y*z + x^2 + x*y + a + 123456")

    def test_polynomial_to_str_scalar_has_lowest_degree(self):
        pol = Polynomials("1000 + x")
        self.assertEqual(str(pol), "x + 1000")

    def test_polynomial_to_str_sorts_monomials_in_degree_decrease_order(self):
        pol = Polynomials("a+x*y")
        self.assertEqual(str(pol), "x*y + a")

    def test_scalars_sum(self):
        a = Polynomials("50")
        b = Polynomials("-123")
        result = a + b
        self.assertEqual(str(result), "(-73)")

    def test_scalar_sums_with_first_degree_monomial(self):
        result = Polynomials("128") + Polynomials("7*x")
        self.assertEqual(str(result), "7*x + 128")

    def test_same_addends_reduction(self):
        result = Polynomials("156*x*y*z") + Polynomials("234*x*y*z")
        self.assertEqual(str(result), "390*x*y*z")

    def test_many_same_addends_reduction(self):
        result = Polynomials("10*x^6 - y^5 + x^3*y^2 + t*z^4") + \
                 Polynomials("x^6 - 8*y^5 - 10*x^3*y^2 + t*z^4")
        self.assertEqual(str(result),
                         "11*x^6 + 2*t*z^4 + (-9*x^3*y^2) + (-9*y^5)")

    def test_simple_sum(self):
        result = Polynomials("a + b + c + d") + Polynomials("x*y + z")
        self.assertEqual(str(result), "x*y + a + b + c + d + z")

    def test_two_zero_sum(self):
        result = Polynomials("0") + Polynomials("0")
        self.assertEqual(str(result), "0")

    def test_zero_and_polynomial_sum(self):
        source = "a + b"
        result = Polynomials("0") + Polynomials(source)
        self.assertEqual(str(result), source)

    def test_all_reduce_simple(self):
        result = Polynomials("a") + Polynomials("-a")
        self.assertEqual(str(result), "0")

    def test_all_reduce_complex(self):
        a = Polynomials("s^7*t*3 - u*v")
        b = Polynomials("-s^7*t*3 + u*v")
        result = a + b
        self.assertEqual(str(result), "0")

    def test_commutativity_simple(self):
        self.help_test_commutativity("a", "b")

    def test_commutativity_complex(self):
        source1 = "10*x^6 + 200*y^5 + x^3*y^2 + t*z^4 + a + b + n + 123456"
        source2 = "s^7*t*3 - 4*x^6 - 3*x^3*y^2 + z^4 + a - 7"
        self.help_test_commutativity(source1, source2)

    def help_test_commutativity(self, source1, source2):
        pol1 = Polynomials(source1)
        pol2 = Polynomials(source2)
        first_result = pol1 + pol2
        second_result = pol2 + pol1
        self.assertEqual(str(first_result), str(second_result))

    def test_two_variables_multiplication(self):
        a = Polynomials("a")
        b = Polynomials("b")
        result = a * b
        self.assertEqual(str(result), "a*b")

    def test_multiplication_sum_on_number(self):
        a = Polynomials("a+b")
        b = Polynomials("7")
        result = a * b
        self.assertEqual(str(result), "7*a + 7*b")

    def test_multiplication_sum_on_variable(self):
        a = Polynomials("a+b")
        b = Polynomials("c")
        result = a * b
        self.assertEqual(str(result), "a*c + b*c")

    def test_multiplication_sum_on_zero(self):
        a = Polynomials("a+b")
        b = Polynomials("0")
        result = a * b
        self.assertEqual(str(result), "0")

    def test_two_scalar_and_variable_multiplication_with_short_form(self):
        a = Polynomials("2a")
        b = Polynomials("4b")
        result = a * b
        self.assertEqual(str(result), "8*a*b")

    def test_two_polynomials_multiplication(self):
        a = Polynomials("a + b")
        b = Polynomials("c + d")
        result = a * b
        self.assertEqual(str(result), "a*c + a*d + b*c + b*d")

    def test_sum_in_square(self):
        a = Polynomials("(a + b)^2")
        self.assertEqual(str(a), "a^2 + 2*a*b + b^2")

    def test_subtraction_in_square(self):
        a = Polynomials("(a - b)^2")
        self.assertEqual(str(a), "a^2 + (-2*a*b) + b^2")

    def test_squares_subtraction(self):
        a = Polynomials("(a - b)(a + b)")
        self.assertEqual(str(a), "a^2 + (-b^2)")

    def test_equality(self):
        a = Polynomials("(x^2-y^2)(a+b)^2")
        b = Polynomials("(x-y)(a+b)(x+y)(a+b)")
        self.assertTrue(a == b)
