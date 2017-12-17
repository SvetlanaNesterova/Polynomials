EPS = 1e-10


def try_as_a_number(value):
    """
    If value is int/flout or string representation of int/float number,
    returns this int/float number, else returns None
    """
    if isinstance(value, (int, float)):
        return value
    elif not isinstance(value, str):
        return None
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return None


def is_almost_equal_scalars(first, second):
    """Compares to float numbers with inaccuracy"""
    return abs(first - second) < EPS


class Monomial:
    def __init__(self):
        """Creation of monomial with value 1"""
        self.multipliers_powers = dict()
        self.scalar = 1

    def get_degree(self):
        """Returns degree of monomial (sum of multipliers degrees)"""
        degree = sum(self.multipliers_powers.values())
        return degree

    def mul(self, multiplier, count=1):
        """
        Multiply monomial on multiplier in power 'count'.
        """
        number = try_as_a_number(multiplier)
        if number is not None:
            self.scalar *= number ** count
        elif isinstance(multiplier, str):
            self._multiply_on_var(multiplier, count)
        elif isinstance(multiplier, Monomial):
            self._multiply_on_monomial(multiplier, count)
        else:
            raise TypeError("Multiplier should be a variable (str type), "
                            "number (float or int type) or Monomial, "
                            "but it is" + str(type(multiplier)) + ": " +
                            str(multiplier))

    def _multiply_on_var(self, multiplier, count):
        powers = self.multipliers_powers
        if multiplier not in powers.keys():
            powers[multiplier] = 0
        powers[multiplier] += count
        if is_almost_equal_scalars(powers[multiplier], 0):
            powers.pop(multiplier)

    def _multiply_on_monomial(self, multiplier, count):
        self.scalar *= multiplier.scalar ** count
        for var, power in multiplier.multipliers_powers.items():
            self._multiply_on_var(var, power)

    def invert(self):
        """
        """
        self.scalar = 1 / self.scalar
        for multiplier in self.multipliers_powers.keys():
            self.multipliers_powers[multiplier] *= -1

    def __eq__(self, other):
        if not isinstance(other, Monomial):
            return False
        if is_almost_equal_scalars(self.scalar, other.scalar) and \
                self.is_similar_monomial(other):
            return True
        return False

    def __lt__(self, other):
        if self.get_degree() == other.get_degree():
            return self.comparative_str() >= other.comparative_str()
        return self.get_degree() < other.get_degree()

    def is_similar_monomial(self, other):
        """Are monomials equal excluding constants"""
        keys1 = list(self.multipliers_powers.keys())
        keys2 = list(other.multipliers_powers.keys())
        if len(keys1) != len(keys2):
            return False
        if not keys1:
            return True
        keys1.sort()
        keys2.sort()
        for k_1, k_2 in zip(keys1, keys2):
            if k_1 != k_2 or not is_almost_equal_scalars(
                    self.multipliers_powers[k_1],
                    other.multipliers_powers[k_1]):
                return False
        return True

    def __str__(self):
        if self.scalar == 0:
            return "0"
        if not self.multipliers_powers:
            return str(self.scalar)

        result = ""
        if self.scalar == -1:
            result += "-"
        elif self.scalar != 1:
            result += str(self.scalar) + "*"
        result += self._str_without_scalar()
        return result

    def _str_without_scalar(self):
        result = ""
        keys = list(self.multipliers_powers.keys())
        keys.sort()
        for multiplier in keys:
            result += multiplier
            power = self.multipliers_powers[multiplier]
            if power != 1:
                if power > 0:
                    result += "^" + str(power)
                else:
                    result += "^(" + str(power) + ")"
            result += "*"
        return result[:-1]

    def comparative_str(self):
        """
        Returns primitive string view of monomial,
        which is suitable for variables and powers comparison
        """
        result = ""
        keys = list(self.multipliers_powers.keys())
        keys.sort()
        for multiplier in keys:
            power = self.multipliers_powers[multiplier]
            mul_str = str(multiplier)
            if power > 0:
                result += mul_str.replace(mul_str, mul_str, power)
        return result
