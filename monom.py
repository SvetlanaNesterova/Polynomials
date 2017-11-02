def is_a_number(value):
    try:
        n = int(value)
        return True
    except:
        return False

class Monom:
    def __init__(self):
        self.multipliers_powers = dict()
        self.scalar = 1

    #add multiply on str scalar
    #
    def multiply(self, multiplier, count=1):
        if type(multiplier) is int or is_a_number(multiplier):
            self.scalar *= int(multiplier) ** count
        elif type(multiplier) is str:
            self._multiply_on_var(multiplier, count)
        elif type(multiplier) is Monom:
            self._multiply_on_monom(multiplier, count)
        else:
            raise TypeError("Multiplier should be a variable (str type), number (int type) or Monom.")
        return self

    def _multiply_on_var(self, multiplier, count):
        powers = self.multipliers_powers
        if not multiplier in powers.keys():
            powers[multiplier] = 0
        powers[multiplier] += count
        if powers[multiplier] == 0:
            powers.pop(multiplier)

    def _multiply_on_monom(self, multiplier, count):
        self.scalar *= multiplier.scalar ** count
        for var, power in multiplier.multipliers_powers.items():
            self._multiply_on_var(var, power)

    def __eq__(self, other):
        if not isinstance(other, Monom):
            return False
        if self.scalar != other.scalar:
            return False
        if self.is_simular_monom(other):
            return True
        return False

    def is_simular_monom(self, other):
        keys1 = list(self.multipliers_powers.keys())
        keys2 = list(other.multipliers_powers.keys())
        if len(keys1) != len(keys2):
            return False
        if len(keys1) == 0:
            return True
        keys1.sort()
        keys2.sort()
        for k1, k2 in zip(keys1, keys2):
            if k1 != k2 or self.multipliers_powers[k1] \
                           != other.multipliers_powers[k1]:
                return False
        return True

    def __str__(self):
        if self.scalar == 0:
            return "0"
        if len(self.multipliers_powers) == 0:
            return str(self.scalar)

        result = ""
        if self.scalar == -1:
            result += "-"
        elif self.scalar != 1:
            result += str(self.scalar) + "*"

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
        result = result[:-1]

        return result