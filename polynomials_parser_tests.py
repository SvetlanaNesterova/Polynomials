import unittest
from polynomials_parser import Parser
from polynom import Polynom

class TestPolynom(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_single_monoms_parse(self):
        values = [
            "1",
            "0",
            "100",
            "x",
            "-a",
            "a*b",
            "a^2",
            "3*t",
            "a^2",
            "x^3*y^4",
            "x^(-1)",
            "a^(-100)*b^100"
            "a*b^2*c^3",
            "15*a^3*b^2*c",
        ]
        for source in values:
            polynom = self.parser.parse(source)
            monom = polynom.monoms[0]
            self.assertEqual(str(monom), source)