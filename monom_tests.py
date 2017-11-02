from monom import Monom
import unittest

class TestMonom(unittest.TestCase):
    def test_init(self):
        m = Monom()
        self.assertEqual(str(m), "1")

    def test_multiplication_on_zero(self):
        m = Monom()
        m.multiply(0)
        self.assertEqual(str(m), "0")

    def test_multiplication_on_minus_one(self):
        m = Monom()
        m.multiply(-1)
        self.assertEqual(str(m), "-1")

    def test_multiplication_on_negative(self):
        m = Monom()
        m.multiply(-98)
        self.assertEqual(str(m), "-98")

    def test_multiplication_on_big_scalar(self):
        m = Monom()
        m.multiply(12345678901234567890)
        self.assertEqual(str(m), "12345678901234567890")

    def test_multiplication_on_two_scalars(self):
        m = Monom()
        m.multiply(5)
        m.multiply(-12)
        self.assertEqual(str(m), "-60")

    def test_multiplication_on_scalar_in_power(self):
        m = Monom()
        m.multiply(2, 10)
        self.assertEqual(str(m), "1024")

    def test_multiplication_on_variable(self):
        m = Monom()
        m.multiply("x")
        self.assertEqual(str(m), "x")

    def test_multiplication_on_variable_and_zero(self):
        m = Monom()
        m.multiply("x")
        m.multiply(0)
        self.assertEqual(str(m), "0")

    def test_multiplication_on_variable_and_one(self):
        m = Monom()
        m.multiply("x")
        m.multiply(1)
        self.assertEqual(str(m), "x")

    def test_multiplication_on_variable_and_minus_one(self):
        m = Monom()
        m.multiply("x")
        m.multiply(-1)
        self.assertEqual(str(m), "-x")

    def test_multiplication_on_variable_and_scalar(self):
        m = Monom()
        m.multiply("x")
        m.multiply(23)
        self.assertEqual(str(m), "23*x")

    def test_multiplication_on_variable_and_negative_scalar(self):
        m = Monom()
        m.multiply("x")
        m.multiply("-12")
        self.assertEqual(str(m), "-12*x")
# тесты на переменные в степени, на правильный порядок

    def test_multiplication_on_variable_in_power(self):
        m = Monom()
        m.multiply("x", 3)
        self.assertEqual(str(m), "x^3")

    def test_multiplication_sums_the_power_of_the_same_variable(self):
        m = Monom()
        m.multiply("x", 3)
        m.multiply("x", 2)
        self.assertEqual(str(m), "x^5")

    def test_multiplication_the_power_become_zero_is_one(self):
        m = Monom()
        m.multiply("x", 3)
        m.multiply("x", -3)
        self.assertEqual(str(m), "1")

    def test_multiplication_on_two_different_variables_in_power_sorts_in_alph_order(self):
        m = Monom()
        m.multiply("x", 3)
        m.multiply("a", 2)
        self.assertEqual(str(m), "a^2*x^3")

    def test_multiplication_on_three_different_variables_in_power_sorts_in_alph_order(self):
        m = Monom()
        m.multiply("x", 3)
        m.multiply("a", 2)
        m.multiply("b", 1)
        self.assertEqual(str(m), "a^2*b*x^3")

    def test_multiplication_on_variable_in_zero_power(self):
        m = Monom()
        m.multiply("x", 0)
        self.assertEqual(str(m), "1")

    def test_multiplication_on_variable_in_negative_power(self):
        m = Monom()
        m.multiply("x", -1)
        self.assertEqual(str(m), "x^(-1)")

    def test_multiplication_on_two_different_variables_in_negative_power_sorts_in_alph_order(self):
        m = Monom()
        m.multiply("y", -3)
        m.multiply("y")
        m.multiply("y")
        m.multiply("x", -3)
        m.multiply("x", -1)
        self.assertEqual(str(m), "x^(-4)*y^(-1)")

    def test_multiplication_on_many_variables_sorts_in_alph_order(self):
        m = Monom()
        m.multiply("z")
        m.multiply("d")
        m.multiply("f")
        m.multiply("c")
        m.multiply("b")
        m.multiply("a")
        self.assertEqual(str(m), "a*b*c*d*f*z")

    def test_multiplication_on_monom(self):
        a = Monom()
        b = Monom()
        a.multiply(10, 2)
        a.multiply("x", 3)
        b.multiply("a", -1)
        b.multiply(-5)
        a.multiply(b)
        self.assertEqual(str(a), "-500*a^(-1)*x^3")

    def test_multiplication_on_monom_answer_one(self):
        a = Monom()
        b = Monom()
        a.multiply("x", 3)
        b.multiply("x", -3)
        a.multiply(b)
        self.assertEqual(str(a), "1")

    def test_multiplication_on_variable_of_wrong_type(self):
        m = Monom()
        self.assertRaises(TypeError, m.multiply, 1.2)

    def test_equal_monoms_of_one(self):
        a = Monom()
        b = Monom()
        self.assertEqual(a, b)

    def test_equal_zeros(self):
        a = Monom()
        b = Monom()
        a.multiply(0)
        b.multiply(0)
        self.assertEqual(a, b)

    def test_equal_minus_one(self):
        a = Monom()
        b = Monom()
        a.multiply(-1)
        b.multiply(-1)
        self.assertEqual(a, b)

    def test_not_equal_one_ane_minus_one(self):
        a = Monom()
        b = Monom()
        b.multiply(-1)
        self.assertNotEqual(a, b)

    def test_equal_scalars(self):
        a = Monom()
        b = Monom()
        a.multiply(10)
        b.multiply(10)
        self.assertEqual(a, b)

    def test_not_equal_scalars(self):
        a = Monom()
        b = Monom()
        a.multiply(28)
        b.multiply(10)
        self.assertNotEqual(a, b)

    def test_equal_single_variable(self):
        a = Monom()
        b = Monom()
        a.multiply("x")
        b.multiply("x")
        self.assertEqual(a, b)

    def test_not_equal_different_single_variable(self):
        a = Monom()
        b = Monom()
        a.multiply("x")
        b.multiply("y")
        self.assertNotEqual(a, b)

    def test_not_equal_scalars_with_equal_variables(self):
        a = Monom()
        b = Monom()
        a.multiply(2)
        a.multiply("x")
        b.multiply("x")
        self.assertNotEqual(a, b)

    def test_not_equal_different_variable_count(self):
        a = Monom()
        b = Monom()
        a.multiply("x")
        b.multiply("x")
        b.multiply("y")
        self.assertNotEqual(a, b)

    def test_equal_single_variable_in_power(self):
        a = Monom()
        b = Monom()
        a.multiply("x", 2)
        b.multiply("x", -8)
        b.multiply("x", 10)
        self.assertEqual(a, b)

    def test_not_equal_single_variable_in_different_power(self):
        a = Monom()
        b = Monom()
        a.multiply("x", 2)
        b.multiply("x", -2)
        self.assertNotEqual(a, b)

    def test_equal_single_variable_in_zero_power_and_one(self):
        a = Monom()
        b = Monom()
        b.multiply("x", -8)
        b.multiply("x", 8)
        self.assertEqual(a, b)

    def test_equal_monoms_of_two_variables(self):
        a = Monom()
        b = Monom()
        a.multiply("z")
        b.multiply("z")
        a.multiply("x")
        b.multiply("x")
        self.assertEqual(a, b)

    def test_equal_monoms_of_two_variables_in_powers(self):
        a = Monom()
        b = Monom()
        a.multiply("z", 2)
        b.multiply("z", 2)
        a.multiply("x", 10)
        b.multiply("x", 10)
        self.assertEqual(a, b)

    def test_not_equal_monoms_of_two_variables_in_different_powers(self):
        a = Monom()
        b = Monom()
        a.multiply("z", 3)
        b.multiply("z", 2)
        a.multiply("x", 10)
        b.multiply("x", 1)
        self.assertNotEqual(a, b)

    def test_not_equal_monoms_of_two_different_variables(self):
        a = Monom()
        b = Monom()
        a.multiply("a")
        b.multiply("a")
        a.multiply("x")
        b.multiply("y")
        self.assertNotEqual(a, b)

    def test_complex_equal_monoms(self):
        a = Monom()
        b = Monom()
        a.multiply(10)
        a.multiply(-5)
        b.multiply(-25)
        b.multiply(2)
        a.multiply("x", 10)
        b.multiply("x", -4)
        b.multiply("x", 14)
        a.multiply("z", 2)
        b.multiply("z", 2)
        a.multiply("c", -5)
        b.multiply("c", -5)
        self.assertEqual(a, b)

    def test_not_equal_with_not_monom(self):
        a = Monom()
        a.multiply("x", 10)
        a.multiply("y", -4)
        a.multiply("t", 2)
        self.assertNotEqual(a, {"t": 2, "x": 10, "y": -4})