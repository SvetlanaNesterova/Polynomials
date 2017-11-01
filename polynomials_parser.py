class Parser:
    """
    Return list of monoms
    """
    def parse(self, source):
        stack = []

        for symb in source:
            if symb == "+":
                pass
            elif symb == "-":
                pass
            elif symb == "*":
                pass
            elif symb == "":
                pass
            elif symb == "":
                pass
            elif symb == "":
                pass
            elif symb == "":

    def form_lexems(self, source):
        before_unaric = ['+', '*', '/', '^', '(']
        operators = ['+', '*', '/', '^', '(', ')']
        letters = [chr(c) for c in range(ord('a'), ord('z') + 1)] + \
                  [chr(c) for c in range(ord('A'), ord('Z') + 1)]
        lexems = []
        number = ""
        can_be_unaric = True
        needs_mul = False
        for symb in source:
            if symb in operators:
                if number != "":
                    if not can_be_unaric:
                        lexems.append("*")
                    lexems.append(number)
                    number = ""
                lexems.append(symb)
                if symb in before_unaric:
                    can_be_unaric = True
                else:
                    can_be_unaric = False
            elif symb == "-":
                if number != "":
                    if not can_be_unaric:
                        lexems.append("*")
                    lexems.append(number)
                    number = ""
                if can_be_unaric:
                    lexems.append("-1")
                    lexems.append("*")
                    can_be_unaric = True
                else:
                    lexems.append("+")
                    lexems.append("-1")
                    lexems.append("*")
                    can_be_unaric = True
            elif symb in letters:
                if number != "":
                    if not can_be_unaric:
                        lexems.append("*")
                    lexems.append(number)
                    number = ""
                if not can_be_unaric:
                    lexems.append("*")
                lexems.append(symb)
                can_be_unaric = False
            else:
                try:
                    n = int(symb)
                except:
                    raise SyntaxError("Unknown symbol: " + symb + ".")
                number += symb
                can_be_unaric = False

        return []


#       raise NotImplemented()
