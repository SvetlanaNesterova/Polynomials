import copy
import polynomial_parser
from monomial import Monomial
from monomial import is_almost_equal_scalars


def _try_convert_power_to_int_or_raise(to_number):
    if isinstance(to_number, Polynomial):
        if len(to_number.monomials) > 1:
            raise ValueError(
                "Power should be integer scalar, but " +
                "it is Polynomial: " + str(to_number))
        if len(to_number.monomials) == 1:
            to_number = to_number.monomials[0]
        else:
            to_number = Monomial()
            to_number.mul(0)
    if isinstance(to_number, Monomial):
        if to_number.multipliers_powers:
            raise ValueError(
                "Power should be integer scalar, but " +
                "it is Monomial: " + str(to_number))
        to_number = to_number.scalar
    if isinstance(to_number, int):
        return to_number
    if isinstance(to_number, float) and is_almost_equal_scalars(
                to_number, round(to_number)):
        return round(to_number)
    else:
        raise TypeError(
            "Power should be integer scalar, but " +
            "it is " + str(type(to_number)) + ": " + str(to_number))


class Polynomial:
    def __init__(self, source):
        if not isinstance(source, str):
            raise TypeError("Source should be a string.")
        self.monomials = polynomial_parser.Parser.parse(source)

    def add(self, other):
        """
        gets other Polynomial, Monomial or scalar
        and adds it to self
        """
        if isinstance(other, Polynomial):
            for monomial in other.monomials:
                self._add_monomial(monomial)
        elif isinstance(other, Monomial):
            self._add_monomial(other)
        elif isinstance(other, int):
            additional = Monomial()
            additional.mul(other)
            self._add_monomial(additional)
        else:
            raise TypeError("Additional should be Polynomial, " +
                            "Monomial, or int")

    def _add_monomial(self, additional):
        for monomial in self.monomials:
            if monomial.is_similar_monomial(additional):
                monomial.scalar = monomial.scalar + additional.scalar
                if monomial.scalar == 0:
                    monomial.mul(0)
                break
        else:
            self.monomials.append(additional)
        self._delete_zeroes()

    def _delete_zeroes(self):
        for monom in self.monomials:
            if monom.scalar == 0:
                self.monomials.remove(monom)

    def mul(self, other):
        """
        gets other Polynomial, Monomial or scalar
        and multiplicate self on it
        """
        if isinstance(other, Polynomial):
            result_pol = Polynomial("")
            for monomial in other.monomials:
                multiplier_pol = Polynomial("")
                multiplier_pol.monomials = copy.deepcopy(self.monomials)
                multiplier_pol.mul(monomial)
                result_pol.add(multiplier_pol)
            self.monomials = result_pol.monomials
        elif isinstance(other, Monomial):
            self._mul_on_monom(other)
        elif isinstance(other, int):
            multiplier_monom = Monomial()
            multiplier_monom.mul(other)
            self._mul_on_monom(multiplier_monom)
        else:
            raise TypeError("Multiplier should be Polynomial, "
                            "Monomial or scalar")

    def _mul_on_monom(self, multiplier):
        for monom in self.monomials:
            monom.mul(multiplier)

    def _in_scalar_power(self, power):
        if power == 0:
            self.monomials = Polynomial("1").monomials
        elif power < 0:
            if len(self.monomials) == 1:
                self.monomials[0].invert()
                power *= -1
            else:
                raise ValueError("Polynomial, which is sum of more "
                                 "then one Monomial, can't be in "
                                 "negative power")
        result = Polynomial("1")
        for power_counter in range(1, power + 1):
            result.mul(self)
        self.monomials = result.monomials

    def pow(self, power):
        """
        gets other scalar in type of Polynom, Monom or int
        returns Polynom, which is a power
        """
        power = _try_convert_power_to_int_or_raise(power)
        self._in_scalar_power(power)


    def invert(self):
        if len(self.monomials) != 1:
            raise ValueError(
                "Divider should be Monomial, but " +
                "it is Polynomial: " + str(self))
        monomial = self.monomials[0]
        monomial.invert()
        self.monomials = [monomial]

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
        if not isinstance(other, Polynomial):
            return False
        if len(self.monomials) != len(other.monomials):
            return False
        self.monomials.sort()
        other.monomials.sort()

        for monom_1, monom_2 in zip(self.monomials, other.monomials):
            if monom_1 != monom_2:
                return False
        return True
