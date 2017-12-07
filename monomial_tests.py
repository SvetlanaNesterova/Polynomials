from monomial import Monomial
import unittest


class TestMonomialStr(unittest.TestCase):
    def setUp(self):
        self.m = Monomial()
        self.a = Monomial()
        self.b = Monomial()

    def test_init(self):
        self.assertEqual(str(self.m), "1")

    def test_multiplication_on_zero(self):
        self.m.mul(0)
        self.assertEqual(str(self.m), "0")

    def test_multiplication_on_minus_one(self):
        self.m.mul(-1)
        self.assertEqual(str(self.m), "-1")

    def test_multiplication_on_negative(self):
        self.m.mul(-98)
        self.assertEqual(str(self.m), "-98")

    def test_multiplication_on_big_scalar(self):
        self.m.mul(12345678901234567890)
        self.assertEqual(str(self.m), "12345678901234567890")

    def test_multiplication_on_float(self):
        self.m.mul(1.23)
        self.assertEqual(str(self.m), "1.23")

    def test_multiplication_on_two_int_scalars(self):
        self.m.mul(5)
        self.m.mul(-12)
        self.assertEqual(str(self.m), "-60")

    def test_multiplication_on_two_float_scalars(self):
        self.m.mul(2.64)
        self.m.mul(0.5)
        self.assertEqual(str(self.m), "1.32")

    def test_multiplication_on_two_float_scalars_with_inaccuracy(self):
        self.m.mul(0.2)
        self.m.mul(0.2)
        self.assertAlmostEqual(float(str(self.m)), 0.04)

    def test_multiplication_on_scalar_in_power(self):
        self.m.mul(2, 10)
        self.assertEqual(str(self.m), "1024")

    def test_multiplication_on_neg_scalar_in_power(self):
        self.m.mul(-2, 10)
        self.assertEqual(str(self.m), "1024")

    def test_multiplication_on_float_scalar_in_power(self):
        self.m.mul(0.5, 3)
        self.assertEqual(str(self.m), "0.125")

    def test_multiplication_on_float_scalar_in_power_with_inaccuracy(self):
        self.m.mul(1.4, 2)
        self.assertAlmostEqual(float(str(self.m)), 1.96)

    def test_multiplication_on_scalar_in_float_power(self):
        self.m.mul(3, 0.5)
        self.assertEqual(str(self.m), str(3**0.5))

    def test_multiplication_on_variable(self):
        self.m.mul("x")
        self.assertEqual(str(self.m), "x")

    def test_multiplication_on_variable_and_zero(self):
        self.m.mul("x")
        self.m.mul(0)
        self.assertEqual(str(self.m), "0")

    def test_multiplication_on_variable_and_one(self):
        self.m.mul("x")
        self.m.mul(1)
        self.assertEqual(str(self.m), "x")

    def test_multiplication_on_variable_and_minus_one(self):
        self.m.mul("x")
        self.m.mul(-1)
        self.assertEqual(str(self.m), "-x")

    def test_multiplication_on_variable_and_float_scalar(self):
        self.m.mul("x")
        self.m.mul(23.24)
        self.assertEqual(str(self.m), "23.24*x")

    def test_multiplication_on_variable_and_negative_scalar(self):
        self.m.mul("x")
        self.m.mul("-12")
        self.assertEqual(str(self.m), "-12*x")

    def test_multiplication_on_variable_in_power(self):
        self.m.mul("x", 3)
        self.assertEqual(str(self.m), "x^3")

    def test_multiplication_on_variable_in_float_power(self):
        self.m.mul("x", 3.5)
        self.assertEqual(str(self.m), "x^3.5")

    def test_multiplication_sums_the_power_of_the_same_variable(self):
        self.m.mul("x", 3)
        self.m.mul("x", 2)
        self.assertEqual(str(self.m), "x^5")

    def test_multiplication_the_power_become_zero_is_one(self):
        self.m.mul("x", 3)
        self.m.mul("x", -3)
        self.assertEqual(str(self.m), "1")

    def test_multiplication_the_float_power_become_zero_is_one(self):
        self.m.mul("x", 0.2)
        self.m.mul("x", 0.2)
        self.m.mul("x", -0.4)
        self.assertEqual(str(self.m), "1")

    def test_mul_on_two_different_vars_in_power_sorts_in_alph_order(self):
        self.m.mul("x", 3)
        self.m.mul("a", 2)
        self.assertEqual(str(self.m), "a^2*x^3")

    def test_mul_on_three_different_vars_in_power_sorts_in_alph_order(self):
        self.m.mul("x", 3)
        self.m.mul("a", 2)
        self.m.mul("b", 1)
        self.assertEqual(str(self.m), "a^2*b*x^3")

    def test_multiplication_on_variable_in_zero_power(self):
        self.m.mul("x", 0)
        self.assertEqual(str(self.m), "1")

    def test_multiplication_on_variable_in_negative_power(self):
        self.m.mul("x", -1)
        self.assertEqual(str(self.m), "x^(-1)")

    def test_mul_on_two_different_vars_in_neg_power_sorts_in_alph_order(self):
        self.m.mul("y", -3)
        self.m.mul("y")
        self.m.mul("y")
        self.m.mul("x", -3)
        self.m.mul("x", -1)
        self.assertEqual(str(self.m), "x^(-4)*y^(-1)")

    def test_multiplication_on_many_vars_sorts_in_alphabet_order(self):
        self.m.mul("z")
        self.m.mul("d")
        self.m.mul("f")
        self.m.mul("c")
        self.m.mul("b")
        self.m.mul("a")
        self.assertEqual(str(self.m), "a*b*c*d*f*z")

    def test_multiplication_on_monomial(self):
        self.a.mul(10, 2)
        self.a.mul("x", 3)
        self.b.mul("a", -1)
        self.b.mul(-5)
        self.a.mul(self.b)
        self.assertEqual(str(self.a), "-500*a^(-1)*x^3")

    def test_multiplication_on_monomial_answer_one(self):
        self.a.mul("x", 3)
        self.b.mul("x", -3)
        self.a.mul(self.b)
        self.assertEqual(str(self.a), "1")


class TestMonomialEquality(unittest.TestCase):
    def setUp(self):
        self.a = Monomial()
        self.b = Monomial()

    def test_equal_monomials_of_one(self):
        self.assertEqual(self.a, self.b)

    def test_equal_zeros(self):
        self.a.mul(0)
        self.b.mul(0)
        self.assertEqual(self.a, self.b)

    def test_equal_minus_one(self):
        self.a.mul(-1)
        self.b.mul(-1)
        self.assertEqual(self.a, self.b)

    def test_not_equal_one_ane_minus_one(self):
        self.b.mul(-1)
        self.assertNotEqual(self.a, self.b)

    def test_equal_float_scalars(self):
        self.a.mul(10.77)
        self.b.mul(10.77)
        self.assertEqual(self.a, self.b)

    def test_equal_mul_on_two_float_scalars_with_inaccuracy(self):
        self.a.mul(0.2)
        self.a.mul(0.2)
        self.b.mul(0.04)
        self.assertEqual(self.a, self.b)

    def test_not_equal_scalars(self):
        self.a.mul(28)
        self.b.mul(10)
        self.assertNotEqual(self.a, self.b)

    def test_equal_single_variable(self):
        self.a.mul("x")
        self.b.mul("x")
        self.assertEqual(self.a, self.b)

    def test_not_equal_different_single_variable(self):
        self.a.mul("x")
        self.b.mul("y")
        self.assertNotEqual(self.a, self.b)

    def test_not_equal_scalars_with_equal_variables(self):
        self.a.mul(2)
        self.a.mul("x")
        self.b.mul("x")
        self.assertNotEqual(self.a, self.b)

    def test_not_equal_different_variable_count(self):
        self.a.mul("x")
        self.b.mul("x")
        self.b.mul("y")
        self.assertNotEqual(self.a, self.b)

    def test_equal_single_variable_in_power(self):
        self.a.mul("x", 2)
        self.b.mul("x", -8)
        self.b.mul("x", 10)
        self.assertEqual(self.a, self.b)

    def test_not_equal_single_variable_in_different_power(self):
        self.a.mul("x", 2)
        self.b.mul("x", -2)
        self.assertNotEqual(self.a, self.b)

    def test_equal_single_variable_in_zero_power_and_one(self):
        self.b.mul("x", -8)
        self.b.mul("x", 8)
        self.assertEqual(self.a, self.b)

    def test_equal_monoms_of_two_variables(self):
        self.a.mul("z")
        self.b.mul("z")
        self.a.mul("x")
        self.b.mul("x")
        self.assertEqual(self.a, self.b)

    def test_equal_monoms_of_two_variables_in_powers(self):
        self.a.mul("z", 2)
        self.b.mul("z", 2)
        self.a.mul("x", 10)
        self.b.mul("x", 10)
        self.assertEqual(self.a, self.b)

    def test_not_equal_monomials_of_two_variables_in_different_powers(self):
        self.a.mul("z", 3)
        self.b.mul("z", 2)
        self.a.mul("x", 10)
        self.b.mul("x", 1)
        self.assertNotEqual(self.a, self.b)

    def test_not_equal_monomials_of_two_different_vars(self):
        self.a.mul("a")
        self.b.mul("a")
        self.a.mul("x")
        self.b.mul("y")
        self.assertNotEqual(self.a, self.b)

    def test_complex_equal_monomials(self):
        self.a.mul(10)
        self.a.mul(-5)
        self.b.mul(-25)
        self.b.mul(2)
        self.a.mul("x", 10)
        self.b.mul("x", -4)
        self.b.mul("x", 14)
        self.a.mul("z", 2)
        self.b.mul("z", 2)
        self.a.mul("c", -5)
        self.b.mul("c", -5)
        self.assertEqual(self.a, self.b)

    def test_not_equal_with_not_monomials(self):
        self.a.mul("x", 10)
        self.a.mul("y", -4)
        self.a.mul("t", 2)
        self.assertNotEqual(self.a, {"t": 2, "x": 10, "y": -4})
