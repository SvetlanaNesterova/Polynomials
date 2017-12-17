import polynomial
from monomial import Monomial

OPERATORS = ['+', '-', '*', '^', '/']
LETTERS = [chr(c) for c in range(ord('a'), ord('z') + 1)] + \
          [chr(c) for c in range(ord('A'), ord('Z') + 1)]
DIGITS = [chr(c) for c in range(ord('0'), ord('9') + 1)]


class Parser:
    @staticmethod
    def parse(source):
        """
        Returns list of Monoms
        """
        if not isinstance(source, str):
            raise TypeError("Source should be a string.")
        source = Parser._remove_spaces(source)
        if source == "":
            return []
        if not Parser._contains_correct_bracket_sequence(source):
            raise ValueError("Incorrect brackets.")
        lexemes_sequence = Parser._form_lexemes(source)
        postfix = Parser._to_postfix(lexemes_sequence)
        polynomials_postfix = Parser._to_polynomials(postfix)
        result_polynomial = Parser._calculate_from_postfix_polynomial_sequence(
            polynomials_postfix)
        return result_polynomial.monomials

    @staticmethod
    def _remove_spaces(string):
        return string.replace(' ', '')

    @staticmethod
    def _contains_correct_bracket_sequence(string):
        depth = 0
        for symb in string:
            if symb == '(':
                depth += 1
            if symb == ')':
                depth -= 1
            if depth < 0:
                return False
        return depth == 0

    @staticmethod
    def _to_polynomials(seq):
        polynoms = []
        for elem in seq:
            if elem not in OPERATORS:
                polynoms.append(
                    Parser._to_polynomial_from_monomial_str(elem))
            else:
                polynoms.append(elem)
        return polynoms

    @staticmethod
    def _to_polynomial_from_monomial_str(value):
        monomial = Monomial()
        if value[0] == '-':
            monomial.mul(-1)
            value = value[1:]
        monomial.mul(value)
        polynom = polynomial.Polynomial("")
        polynom.add(monomial)
        return polynom

    @staticmethod
    def _form_lexemes(source):
        lexemes = []
        number = ""
        state = 0
        symb_before = ''
        symb_twice_before = ''
        for symb in source:
            if state == 0:
                if symb in DIGITS:
                    number += symb
                    state = 2
                elif symb == "-":
                    state = 4
                else:
                    if symb in LETTERS:
                        state = 3
                    elif symb == "(":
                        state = 1
                    else:
                        state = 5
                    lexemes.append(symb)
            elif state == 1:
                if symb in DIGITS:
                    number += symb
                    state = 2
                elif symb == "-":
                    state = 4
                else:
                    if symb in LETTERS or symb == ")":
                        state = 3
                    elif symb == "(":
                        state = 1
                    else:
                        state = 5
                    lexemes.append(symb)
            elif state == 2:
                if symb in DIGITS or symb == '.':
                    number += symb
                    state = 2
                else:
                    lexemes.append(number)
                    number = ""
                    if symb in OPERATORS:
                        state = 0
                    elif symb in LETTERS:
                        lexemes.append("*")
                        state = 3
                    elif symb == ")":
                        state = 3
                    elif symb == "(":
                        lexemes.append("*")
                        state = 1
                    else:
                        state = 5
                    lexemes.append(symb)
            elif state == 3:
                if symb in DIGITS:
                    lexemes.append("*")
                    number += symb
                    state = 2
                else:
                    if symb in OPERATORS:
                        state = 0
                    elif symb in LETTERS:
                        lexemes.append("*")
                        state = 3
                    elif symb == ")":
                        state = 3
                    elif symb == "(":
                        lexemes.append("*")
                        state = 1
                    else:
                        state = 5
                    lexemes.append(symb)
            elif state == 4:
                lexemes.append("-1")
                if symb_twice_before == '/':
                    lexemes.append('/')
                elif symb_twice_before == '^':
                    lexemes.append('^')
                else:
                    lexemes.append("*")
                if symb in DIGITS:
                    number += symb
                    state = 2
                elif symb == "-":
                    state = 4
                else:
                    if symb in LETTERS:
                        state = 3
                    elif symb == '(':
                        state = 1
                    else:
                        state = 5
                    lexemes.append(symb)
            if state == 5:
                raise SyntaxError("Incorrect symbol: " + symb + ".")
            symb_twice_before = symb_before
            symb_before = symb

        if number != "":
            lexemes.append(number)
        return lexemes

    @staticmethod
    def _to_postfix(seq):
        priority = {
            '(': 0,
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '^': 3
        }
        left_associativity = {
            '+': True,
            '-': True,
            '*': True,
            '/': True,
            '^': False
        }
        stack = []
        result = []
        for elem in seq:
            if elem in OPERATORS:
                while stack:
                    cur = stack.pop()
                    if (priority[cur] >= priority[elem] and
                            left_associativity[elem]) or (
                        priority[cur] > priority[elem]) and \
                            not left_associativity[elem]:
                        result.append(cur)
                    else:
                        stack.append(cur)
                        break
                stack.append(elem)
            elif elem == '(':
                stack.append('(')
            elif elem == ')':
                cur = stack.pop()
                while cur != '(':
                    result.append(cur)
                    cur = stack.pop()
            else:
                result.append(elem)
        while stack:
            result.append(stack.pop())
        return result

    @staticmethod
    def _calculate_from_postfix_polynomial_sequence(seq):
        stack = []
        for elem in seq:
            if elem in OPERATORS:
                operand2 = stack.pop()
                operand1 = stack[-1]
                Parser._calculate_to_first(operand1, operand2, elem)
            else:
                stack.append(elem)
        return stack.pop()

    @staticmethod
    def _calculate_to_first(operand1, operand2, operator):
        if operator == '+':
            operand1.add(operand2)
        elif operator == '-':
            operand1.mul(-1)
            operand1.add(operand2)
            operand1.mul(-1)
        elif operator == '*':
            operand1.mul(operand2)
        elif operator == '/':
            operand2.invert()
            operand1.mul(operand2)
        elif operator == '^':
            operand1.pow(operand2)
        else:
            raise Exception("Unknown or unhandled operator: " + operator)
