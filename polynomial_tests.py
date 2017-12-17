import unittest
from polynomial import Polynomial

if __name__ == "__main__":
    unittest.main()


class TestPolynomial(unittest.TestCase):
    def test_equal(self):
        pol1 = Polynomial("a*b+c")
        pol2 = Polynomial("a*b+c")
        self.assertEqual(pol1, pol2)

    def test_not_equal_different_length(self):
        pol1 = Polynomial("a*b+c")
        pol2 = Polynomial("a*b")
        self.assertNotEqual(pol1, pol2)

    def test_not_equal_different_monoms(self):
        pol1 = Polynomial("a*c")
        pol2 = Polynomial("a*b")
        self.assertNotEqual(pol1, pol2)

    def test_polynomial_to_str_sorts_monomials_in_classical_order(self):
        pol = Polynomial("a + 123456 + x^2 + x*y + y*x*z")
        self.assertEqual(str(pol), "x*y*z + x^2 + x*y + a + 123456")

    def test_polynomial_to_str_sorts_monomials_with_negative_power_in_classical_order(self):
        pol = Polynomial("x^2 + x*y + y*x^(-2)*z")
        self.assertEqual(str(pol), "x^2 + x*y + x^(-2)*y*z")

    def test_polynomial_to_str_scalar_has_zero_degree(self):
        pol = Polynomial("1000 + x + x^-1")
        self.assertEqual(str(pol), "x + 1000 + x^(-1)")

    def test_polynomial_to_str_sorts_monomials_in_degree_decrease_order(self):
        pol = Polynomial("a+x*y+x/x^2")
        self.assertEqual(str(pol), "x*y + a + x^(-1)")

    def test_scalars_sum(self):
        result = Polynomial("50")
        result.add(Polynomial("-123"))
        self.assertEqual(str(result), "(-73)")

    def test_scalar_sums_with_first_degree_monomial(self):
        result = Polynomial("128")
        result.add(Polynomial("7*x"))
        self.assertEqual(str(result), "7*x + 128")

    def test_same_addends_reduction(self):
        result = Polynomial("156*x*y*z")
        result.add(Polynomial("234*x*y*z"))
        self.assertEqual(str(result), "390*x*y*z")

    def test_many_same_addends_reduction(self):
        result = Polynomial("10*x^6 - y^5 + x^3*y^2 + t*z^4")
        result.add(Polynomial("x^6 - 8*y^5 - 10*x^3*y^2 + t*z^4"))
        self.assertEqual(str(result),
                         "11*x^6 + 2*t*z^4 + (-9*x^3*y^2) + (-9*y^5)")

    def test_simple_sum(self):
        result = Polynomial("a + b + c + d")
        result.add(Polynomial("x*y + z"))
        self.assertEqual(str(result), "x*y + a + b + c + d + z")

    def test_two_zero_sum(self):
        result = Polynomial("0")
        result.add(Polynomial("0"))
        self.assertEqual(str(result), "0")

    def test_add_int(self):
        result = Polynomial("0")
        result.add(100500)
        self.assertEqual(str(result), "100500")

    def test_zero_and_polynomial_sum(self):
        source = "a + b"
        result = Polynomial("0")
        result.add(Polynomial(source))
        self.assertEqual(str(result), source)

    def test_all_reduce_simple(self):
        result = Polynomial("a")
        result.add(Polynomial("-a"))
        self.assertEqual(str(result), "0")

    def test_all_reduce_complex(self):
        result = Polynomial("s^7*t*3 - u*v")
        result.add(Polynomial("-s^7*t*3 + u*v"))
        self.assertEqual(str(result), "0")

    def test_two_variables_multiplication(self):
        result = Polynomial("a")
        result.mul(Polynomial("b"))
        self.assertEqual(str(result), "a*b")

    def test_multiplication_sum_on_number(self):
        result = Polynomial("a+b")
        result.mul(Polynomial("7"))
        self.assertEqual(str(result), "7*a + 7*b")

    def test_multiplication_sum_on_variable(self):
        result = Polynomial("a+b")
        result.mul(Polynomial("c"))
        self.assertEqual(str(result), "a*c + b*c")

    def test_multiplication_sum_on_zero(self):
        result = Polynomial("a+b")
        result.mul(Polynomial("0"))
        self.assertEqual(str(result), "0")

    def test_two_scalar_and_variable_multiplication_with_short_form(self):
        result = Polynomial("2a")
        result.mul(Polynomial("4b"))
        self.assertEqual(str(result), "8*a*b")

    def test_two_polynomials_multiplication(self):
        result = Polynomial("a + b")
        result.mul(Polynomial("c + d"))
        self.assertEqual(str(result), "a*c + a*d + b*c + b*d")

    def test_division_on_variable(self):
        result = Polynomial("a/b")
        self.assertEqual(str(result), "a*b^(-1)")

    def test_division_on_scalar(self):
        result = Polynomial("a/0.5")
        self.assertEqual(str(result), "2.0*a")

    def test_division_on_polynomial_with_scalar_value(self):
        result = Polynomial("a/(a - a + 4)")
        self.assertEqual(str(result), "0.25*a")

    def test_division_of_polynomial_on_monomial(self):
        result = Polynomial("(a+b+c)/(0.25*a^5*b)")
        self.assertEqual(str(result),
                         "4.0*a^(-5) + 4.0*a^(-4)*b^(-1) + 4.0*a^(-5)*b^(-1)*c")

    def test_division_on_sum_of_two_monomials_raise_value_error(self):
        self.assertRaises(ValueError, Polynomial, "x/(x+y)")

    def test_zero_power_is_one(self):
        result = Polynomial("a^0")
        self.assertEqual(str(result), "1")

    def test_negative_power_of_monomial(self):
        result = Polynomial("(abc)^(-1)")
        self.assertEqual(str(result), "a^(-1)*b^(-1)*c^(-1)")

    def test_not_scalar_power_raise_value_error(self):
        self.assertRaises(ValueError, Polynomial, "x^x")
        self.assertRaises(ValueError, Polynomial, "x^(x + y)")

    def test_float_power_raise_type_error(self):
        self.assertRaises(TypeError, Polynomial, "x^(1.5)")

    def test_almost_int_power_raise_type_error(self):
        a = Polynomial("x^(2.0000000000000001)")
        self.assertEqual(str(a), "x^2")

    def test_polynomial_negative_power_raise_value_error(self):
        self.assertRaises(ValueError, Polynomial, "(x+y)^(-2)")

    def test_sum_in_square(self):
        a = Polynomial("(a + b)^2")
        self.assertEqual(str(a), "a^2 + 2*a*b + b^2")

    def test_subtraction_in_square(self):
        a = Polynomial("(a - b)^2")
        self.assertEqual(str(a), "a^2 + (-2*a*b) + b^2")

    def test_squares_subtraction(self):
        a = Polynomial("(a - b)(a + b)")
        self.assertEqual(str(a), "a^2 + (-b^2)")

    def test_equality(self):
        a = Polynomial("(x^2-y^2)(a+b)^2")
        b = Polynomial("(x-y)(a+b)(x+y)(a+b)")
        self.assertTrue(a == b)

    def test_commutativity_simple(self):
        self.help_test_commutativity("a", "b")

    def test_commutativity_complex(self):
        source1 = "10*x^6 + 200*y^5 + x^3*y^2 + t*z^4 + a + b + n + 123456"
        source2 = "s^7*t*3 - 4*x^6 - 3*x^3*y^2 + z^4 + a - 7"
        self.help_test_commutativity(source1, source2)

    def help_test_commutativity(self, source1, source2):
        first_result = Polynomial(source1)
        first_result.add(Polynomial(source2))
        second_result = Polynomial(source1)
        second_result.add(Polynomial(source2))
        self.assertEqual(str(first_result), str(second_result))

    def test_incorrect_expression_raise_exception(self):
        self.assertRaises(Exception, Polynomial, "a+b)")
        self.assertRaises(Exception, Polynomial, "a%4")
        self.assertRaises(Exception, Polynomial, "33,3")
