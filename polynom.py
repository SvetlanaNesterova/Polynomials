from polynomials_parser import Parser

class Polynom:
    def __init__(self, source):
        if type(source) == str:
            self.monoms = Parser.parse(source)

        raise NotImplemented()

    def __add__(self, other):
        """
        gets other Polynom or scalar
        returns Polynom, which is a result of summation
        """
        raise NotImplemented()

    def __mul__(self, other):
        """
        gets other Polynom or scalar
        returns Polynom, which is a result of multiplication
        """
        raise NotImplemented()

    def __str__(self):
        raise NotImplemented()

a = Polynom()
b = Polynom()
print(a + b)
