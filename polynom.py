import polynomials_parser
import copy
from monom import Monom

class Polynom:
    def __init__(self, source):
        if type(source) != str:
            raise TypeError("Source should be a string.")
        self.monoms = polynomials_parser.Parser().parse(source)

    def __add__(self, other):
        """
        gets other Polynom, Monom, or scalar
        returns Polynom, which is a result of summation
        """
        result = Polynom("")
        result.monoms = copy.deepcopy(self.monoms)

        if type(other) == Polynom:
            for monom in other.monoms:
                result._add_monom(monom)
        elif type(other) == Monom:
            result._add_monom(other)
        elif type(other) == int:
            additional = Monom()
            additional.multiply(other)
            result._add_monom(additional)
        else:
            raise TypeError("Additional should be Polynom, Monom, or int")
        return result

    def _add_monom(self, additional):
        """
        This method spoils self
        """
        for monom in self.monoms:
            if monom.is_simular_monom(additional):
                monom.scalar = monom.scalar + additional.scalar
                if monom.scalar == 0:
                    monom.multiply(0)
                break
        else:
            self.monoms.append(additional)
        self.clear_zeroes()

    def clear_zeroes(self):
        for monom in self.monoms:
            if monom.scalar == 0:
                self.monoms.remove(monom)

    def __mul__(self, other):
        """
        gets other Polynom, Monom or scalar
        returns Polynom, which is a result of multiplication
        """
        result = Polynom("")
        result.monoms = copy.deepcopy(self.monoms)

        if type(other) == Polynom:
            for monom in other.monoms:
                result._mul_on_monom(monom)
        elif type(other) == Monom:
            result._mul_on_monom(other)
        elif type(other) == int:
            multiplier = Monom()
            multiplier.multiply(other)
            result._mul_on_monom(multiplier)
        else:
            raise TypeError("Multiplier should be Polynom, Monom, or int")
        return result

    def _mul_on_monom(self, multiplier):
        """
        This method spoils self
        """
        for monom in self.monoms:
            multiplication = monom.multiply(multiplier)
            self.monoms.remove(monom)
            self.monoms.append(multiplication)

    def __pow__(self, power, modulo=None):
        """
        gets other SCALAR in type of Polynom, Monom or int
        returns Polynom, which is a power
        """
        return self._in_scalar_power(power.monoms[0].scalar)

    def _in_scalar_power(self, power):
        if type(power) is not int:
            raise TypeError("Polynomial can be only in scalar power")
        if power < 0:
            raise ValueError("Polynomial can't be in negative power")
        if power == 0:
            return Polynom("1")
        if power == 1:
            return copy.deepcopy(self)
        result = self * self
        for p in range(3, power + 1):
            result *= self
        return result

    def __str__(self):
        self.monoms.sort(reverse=True)
        monoms_in_brackets = map(lambda monom:
                                 "(" + str(monom) + ")" if monom.scalar < 0 else str(monom),
                                 self.monoms)
        result = " + ".join(monoms_in_brackets)
        if result == "":
            return "0"
        return result
