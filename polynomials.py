import polynomial_parser
import copy
from monomial import Monomial


class Polynomials:
    def __init__(self, source):
        if type(source) != str:
            raise TypeError("Source should be a string.")
        self.monomials = polynomial_parser.Parser.parse(source)

    def __add__(self, other):
        """
        gets other Polynomial, Monomial, or scalar
        returns Polynomial, which is a result of summation
        """
        result = Polynomials("")
        result.monomials = copy.deepcopy(self.monomials)

        if type(other) == Polynomials:
            for monom in other.monomials:
                result._add_monom(monom)
        elif type(other) == Monomial:
            result._add_monom(other)
        elif type(other) == int:
            additional = Monomial()
            additional.mul(other)
            result._add_monom(additional)
        else:
            raise TypeError("Additional should be Polynom, Monom, or int")
        return result

    def _add_monom(self, additional):
        """
        This method spoils self
        """
        for monom in self.monomials:
            if monom.is_similar_monomial(additional):
                monom.scalar = monom.scalar + additional.scalar
                if monom.scalar == 0:
                    monom.mul(0)
                break
        else:
            self.monomials.append(additional)
        self.clear_zeroes()

    def clear_zeroes(self):
        for monom in self.monomials:
            if monom.scalar == 0:
                self.monomials.remove(monom)

    def __mul__(self, other):
        """
        gets other Polynom, Monom or scalar
        returns Polynom, which is a result of multiplication
        """
        result = Polynomials("")

        if type(other) == Polynomials:
            for monom in other.monomials:
                multiplier = Polynomials("")
                multiplier.monomials = copy.deepcopy(self.monomials)
                multiplier._mul_on_monom(monom)
                result += multiplier
        else:
            result.monomials = copy.deepcopy(self.monomials)
            if type(other) == Monomial:
                result._mul_on_monom(other)
            elif type(other) == int:
                multiplier = Monomial()
                multiplier.mul(other)
                result._mul_on_monom(multiplier)
            else:
                raise TypeError("Multiplier should be Polynom, Monom, or int")
        return result

    def _mul_on_monom(self, multiplier):
        """
        This method spoils self
        """
        for monom in self.monomials:
            multiplication = monom.mul(multiplier)
            # self.monomials.remove(monom)
            # self.monomials.append(multiplication)

    def __pow__(self, power, modulo=None):
        """
        gets other SCALAR in type of Polynom, Monom or int
        returns Polynom, which is a power
        """
        return self._in_scalar_power(power.monomials[0].scalar)

    def _in_scalar_power(self, power):
        if type(power) is not int:
            raise TypeError("Polynomial can be only in scalar power")
        if power < 0:
            raise ValueError("Polynomial can't be in negative power")
        if power == 0:
            return Polynomials("1")
        if power == 1:
            return copy.deepcopy(self)
        result = self * self
        for p in range(3, power + 1):
            result *= self
        return result

    def __str__(self):
        self.monomials.sort(reverse=True)
        monomials_in_brackets = map(
            lambda monom:
            "(" + str(monom) + ")" if monom.scalar < 0 else str(monom),
            self.monomials)
        result = " + ".join(monomials_in_brackets)
        if result == "":
            return "0"
        return result

    def __eq__(self, other):
        if type(other) is not Polynomials:
            return False
        if len(self.monomials) != len(other.monomials):
            return False
        self.monomials.sort()
        other.monomials.sort()

        for a, b in zip(self.monomials, other.monomials):
            if a != b:
                return False
        return True
