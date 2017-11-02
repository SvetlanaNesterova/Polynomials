import polynom
from monom import Monom

operators = ['+', '-', '*', '^']
letters = [chr(c) for c in range(ord('a'), ord('z') + 1)] + \
          [chr(c) for c in range(ord('A'), ord('Z') + 1)]
digits = [chr(c) for c in range(ord('0'), ord('9') + 1)]


def remove_spaces(string):
    return string.replace(' ', '')


def to_polynomials(seq):
    for index in range(len(seq)):
        if not seq[index] in operators:
            seq[index] = to_polynomial_from_monomial_str(seq[index])


def to_polynomial_from_monomial_str(value):
    monomial = Monom()
    if value[0] == '-':
        monomial.multiply(-1)
        value = value[1:]
    monomial.multiply(value)
    polynomial= polynom.Polynom("")
    polynomial+= monomial
    return polynomial


def contains_correct_bracket_sequence(string):
    depth = 0
    for symb in string:
        if symb == '(':
            depth += 1
        if symb == ')':
            depth -= 1
        if depth < 0:
            return False
    if depth > 0:
        return False
    return True


def form_lexemes( source):
    lexemes = []
    number = ""

    state = 0
    for symb in source:
        if state == 0:
            if symb in digits:
                number += symb
                state = 2
            elif symb == "-":
                state = 4
            else:
                if symb in letters:
                    state = 3
                elif symb == "(":
                    state = 1
                else:
                    state = 5
                lexemes.append(symb)
        elif state == 1:
            if symb in digits:
                number += symb
                state = 2
            elif symb == "-":
                state = 4
            else:
                if symb in letters or symb == ")":
                    state = 3
                elif symb == "(":
                    state = 1
                else:
                    state = 5
                lexemes.append(symb)
        elif state == 2:
            if symb in digits:
                number += symb
                state = 2
            else:
                lexemes.append(number)
                number = ""
                if symb in operators:
                    state = 0
                elif symb in letters:
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
            if symb in digits:
                lexemes.append("*")
                number += symb
                state = 2
            else:
                if symb in operators:
                    state = 0
                elif symb in letters:
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
            lexemes.append("*")
            if symb in digits:
                number += symb
                state = 2
            elif symb == "-":
                state = 4
            else:
                if symb in letters:
                    state = 3
                elif symb == '(':
                    state = 1
                else:
                    state = 5
                lexemes.append(symb)
        if state == 5:
            raise SyntaxError("Unknown symbol: " + symb + ".")

    if number != "":
        lexemes.append(number)
    return lexemes


def calculate(operand1, operand2, operation):
    if operation == '+':
        result = operand1 + operand2
    elif operation == '-':
        result = operand1 + operand2 * (-1)
    elif operation == '*':
        result = operand1 * operand2
    elif operation == '^':
        result = operand1 ** operand2
    else:
        raise Exception("Unknown or unhandled operator: " + operation)
    return result



class Parser:
    def parse(self, source):
        """
            Returns Polynom
        """
        if type(source) != str:
            raise TypeError("Source should be a string.")
        source = remove_spaces(source)
        if source == "":
            return []
        if not contains_correct_bracket_sequence(source):
            raise ValueError("Incorrect brackets.")
        lexemes_sequence = form_lexemes(source)
        postfix = self.to_postfix(lexemes_sequence)
        to_polynomials(postfix)
        result_polynomial = self.calculate_from_postfix_polynomial_sequence(postfix)
        return result_polynomial.monoms

    def to_postfix(self, seq):
        priority = {'(': 0, '+': 1, '-': 1, '*': 2, '^': 3}
        left_associativity = {'+': True, '-': True, '*': True, '^': False}
        stack = []
        result = []
        for elem in seq:
            if elem in operators:
                while len(stack) > 0:
                    cur = stack.pop()
                    if (priority[cur] >= priority[elem] and left_associativity[elem]) or (
                        priority[cur] > priority[elem]) and not left_associativity[elem] :
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
        while len(stack) > 0:
            result.append(stack.pop())
        return result

    def calculate_from_postfix_polynomial_sequence(self, seq):
        stack = []
        for elem in seq:
            if elem in operators:
                operand2 = stack.pop()
                operand1 = stack.pop()
                result = calculate(operand1, operand2, elem)
                stack.append(result)
            else:
                stack.append(elem)
        return stack.pop()
