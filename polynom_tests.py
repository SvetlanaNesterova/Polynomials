import unittest
from polynom import Polynom

class TestPolynom(unittest.TestCase):
    def test_polynom_to_str_sorts_monoms_in_classical_order(self):
        pol = Polynom("a + 123456 + x^2 + x*y + y*x*z")
        self.assertEqual(str(pol), "x*y*z + x^2 + x*y + a + 123456")
    '''
    def test_polynom_to_str_scalar_has_lowerest_degree(self):
        pol = Polynom("1000 + x")
        self.assertEqual(str(pol), "x + 1000")

    def test_polynom_to_str_sorts_three_var_monoms_in_degree_decrease_order(self):
        pol = Polynom("a+x*y")
        self.assertEqual(str(pol), "x*y + a")
    '''
    def test_scalars_sum(self):
        result = Polynom("50") + Polynom("-123")
        self.assertEqual(str(result), "-73")

    def test_scalar_sums_with_first_degree_monom(self):
        result = Polynom("128") + Polynom("7*x")
        self.assertEqual(str(result), "7*x + 128")

    def test_same_addents_reduction(self):
        result = Polynom("156*x*y*z") + Polynom("234*x*y*z")
        self.assertEqual(str(result), "390*x*y*z")

    def test_many_same_addents_reduction(self):
        result = Polynom("10*x^6 - y^5 + x^3*y^2 + t*z^4") + Polynom("x^6 - 8*y^5 - 10*x^3*y^2 + t*z^4")
        self.assertEqual(str(result), "11*x^6 - 9*y^5 - 9*x^3*y^2 + 2*t*z^4")

    def test_simple_sum(self):
        result = Polynom("a + b + c + d") + Polynom("x*y + z")
        self.assertEqual(str(result), "a + b + c + d + x*y + z")

    def test_two_zero_sum(self):
        result = Polynom("0") + Polynom("0")
        self.assertEqual(str(result), "0")

    def test_zero_and_polynom_sum(self):
        source = "a + b"
        result = Polynom("0") + Polynom(source)
        self.assertEqual(str(result), source)

    def test_all_reduct_simple(self):
        result = Polynom("a") + Polynom("-a")
        self.assertEqual(str(result), "0")

    def test_all_reduct_complex(self):
        result = Polynom("s^7*t*3 - u*v") + Polynom("-s^7*t*3 + u*v")
        self.assertEqual(str(result), "0")

    def test_communicativity_simple(self):
        self.test_communicativity("a", "b")

    def test_commutativity_complex(self):
        source1 = "10*x^6 + 200*y^5 + x^3*y^2 + t*z^4 + a + b + n + 123456"
        source2 = "s^7*t*3 - 4*x^6 - 3*x^3*y^2 + z^4 + a - 7"

    def test_communicativity(self, source1, source2):
        pol1 = Polynom(source1)
        pol2 = Polynom(source2)
        first_result = pol1 + pol2
        second_result = pol2 + pol1
        self.assertEqual(str(first_result), str(second_result))