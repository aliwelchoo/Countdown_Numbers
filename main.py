from typing import List
from itertools import product
import re

number_or_symbol = re.compile('(\d+|[^ 0-9])')
plus_minus = re.compile('([^+-]+)')
D = {}


def eval_product(prod):
    if prod in D:
        return D[prod]
    else:
        product_sol = eval(prod)
        D[product] = product_sol
        return product_sol


def eval_sum_product(sp):
    return sum([eval_product(prod) for prod in sp.split("+")])


def eval_equation(sp):
    return sum([eval_product(sp[max(m.start(0)-1, 0):m.end(0)]) for m in re.finditer(plus_minus, sp)])


def eval_equation_minus_then_plus(equation):
    parts = equation.split("-")
    solution = eval_sum_product(parts[0])
    for part in parts[1:]:
        solution -= eval_sum_product(part)
    return solution


def has_leading_zeros(string):
    split = re.findall(number_or_symbol, string)
    for idx in range(int(len(split)/2)+1):
        num = split[2*idx]
        if num != '0' and num[0] == '0':
            return True
    return False


def insertStr(word, insert, location):
    return word[:location] + insert + word[location:]


def laceStr(inner, outer):
    lace = outer[0]
    for gap in range(len(inner)):
        lace += inner[gap] + outer[gap+1]
    return lace


def has_lead_zero(string):
    return string != '0' and string[0] == '0'


def lace(inner, outer):
    laced = []
    idx = 0
    while idx < len(inner):
        next_bit = outer[idx]
        while inner[idx] == "":
            idx += 1
            next_bit += outer[idx]
            if idx >= len(inner):
                if has_lead_zero(next_bit):
                    return []
                laced.append(next_bit)
                return laced
        if has_lead_zero(next_bit):
            return []
        laced.append(next_bit)
        laced.append(inner[idx])
        idx += 1
    next_bit = outer[idx]
    if has_lead_zero(next_bit):
        return []
    laced.append(next_bit)
    return laced


def stringAddOperators(num: str, target: int) -> List[str]:
    operators = ["", "*", "+", "-"]
    op_perms = product(operators, repeat=len(num)-1)
    sols = []
    for perm in op_perms:
        equation = laceStr(perm, num)
        if has_leading_zeros(equation):
            continue
        if eval(equation) == target:
            sols.append(equation)
    return sols


def arrayAddOperators(num: str, target: int) -> List[str]:
    operators = ["", "*", "+", "-"]
    op_perms = product(operators, repeat=len(num)-1)
    sols = []
    for perm in op_perms:
        equation_bits = lace(perm, num)
        if not equation_bits:
            continue
        equation = ''.join(equation_bits)
        if eval(equation) == target:
            sols.append(equation)
    return sols


def multDictAddOperators(num: str, target: int) -> List[str]:
    operators = ["", "*", "+", "-"]
    op_perms = product(operators, repeat=len(num)-1)
    sols = []

    for perm in op_perms:
        equation_bits = lace(perm, num)
        if not equation_bits:
            continue
        equation = ''.join(equation_bits)
        if eval_equation(equation) == target:
            sols.append(equation)
    return sols


class Solution:
    def oldaddOperators(self, num: str, target: int) -> List[str]:
        return multDictAddOperators(num, target)

    def addOperators(self, num: str, target: int) -> List[str]:
        sols = []
        length = len(num) -1
        operators = ["", "*", "+", "-"]

        def recursAddOperators(idx: int, next_target: int, next_operator: str, current_product: int,
                               product_before_last_multiply, parts):
            char = num[idx]
            parts.append(next_operator)
            parts.append(char)
            digit = int(char)
            if next_operator == '+':
                new_product = digit
                total_change = digit
                product_before_last_multiply = 1
            elif next_operator == '-':
                new_product = -digit
                total_change = -digit
                product_before_last_multiply = -1
            elif next_operator == '*':
                new_product = current_product * digit
                total_change = new_product - current_product
                product_before_last_multiply = current_product
            elif next_operator == '':
                if current_product == 0:
                    return
                new_product = 10 * current_product + digit * product_before_last_multiply
                total_change = new_product - current_product

            new_target = next_target - total_change

            # eq = ''.join(parts[1:])
            # res = eval(eq)
            # if eval(eq) != target - new_target:
            #     print(eq + ' = ' + str(res), target - new_target, total_change)
            if idx == length:
                if new_target == 0:
                    eq = ''.join(parts[1:])
                    sols.append(eq)
                return
            for operator in operators:
                recursAddOperators(idx + 1, new_target, operator, new_product, product_before_last_multiply, parts)
                parts.pop()
                parts.pop()
            return sols
        return recursAddOperators(idx=0,
                                  next_target=target,
                                  next_operator='+',
                                  current_product=1,
                                  product_before_last_multiply=1,
                                  parts=[]
                                  )


def InOrderNumbers(numbers: List[int], target: int) -> set[str]:
    operators = ['+', '-', '*', '/']
    sols = []
    print(f'{numbers} and the target, {target}')

    def recursInOrderNumbers(idx, next_target: int, next_operator: str, current_product: int, eq_parts: List):

        num = numbers[idx]
        char = str(num)
        eq_parts.append(next_operator)
        eq_parts.append(char)

        if next_operator == '+' or num == 0:
            new_product = num
            total_change = num
        elif next_operator == '-':
            new_product = -num
            total_change = -num
        elif next_operator == '*':
            new_product = current_product * num
            total_change = new_product - current_product
        elif next_operator == '/':
            new_product = current_product / num
            if new_product != int(new_product):
                return
            total_change = new_product - current_product

        new_target = next_target - total_change
        if len(eq_parts) >= 2:
            eq = ''.join(eq_parts[1:])
            res = eval(eq)
            if res != target - new_target:
                return

        if new_target == 0:
            eq = ''.join(eq_parts[1:])
            if len(sols) == 0:
                print(f'First solution: {eq}')
            sols.append(eq)
            return
        if idx == len(numbers)-1:
            return
        for operator in operators:
            recursInOrderNumbers(idx+1, new_target, operator, new_product, eq_parts)
            eq_parts.pop()
            eq_parts.pop()
        return set(sols)

    sols = recursInOrderNumbers(idx=0,
                                  next_target=target,
                                  next_operator='+',
                                  current_product=1,
                                  eq_parts=[],
                                  )
    print(f'All solutions: {sols}')
    print(f'Verified all add to target: {np.all([eval(sol) for sol in sols])}')
    return sols

from itertools import permutations


def CountdownNumbers(numbers: List[int], target: int) -> set[str]:
    operators = ['+', '-', '*', '/']
    sols = []
    print(f'{numbers} and the target, {target}')

    def recursCountdownNumbers(eq_parts: List):
        if len(numbers) == 1:
            return
        for n1, n2 in permutations(numbers, 2):
            numbers.remove(n1)
            numbers.remove(n2)
            for operator in operators:
                if n2 == 0 and operator == '/':
                    continue
                new_calc = str(n1) + operator + str(n2)
                new_number = eval(new_calc)
                new_equation = f'{new_calc}={new_number}\n'
                if new_number < 0:
                    continue
                if new_number == target:
                    eq = ''.join(eq_parts + [new_equation])
                    sols.append(eq)
                    print(eq)
                else:
                    numbers.append(new_number)
                    eq_parts.append(new_equation)
                    recursCountdownNumbers(eq_parts)
                    eq_parts.remove(new_equation)
                    numbers.remove(new_number)
            numbers.append(n1)
            numbers.append(n2)
            if len(sols) > 0:
                break
        return set(sols)

    sols = recursCountdownNumbers(eq_parts=[])
    print(f'All solutions: {sols}')
    return sols


import numpy as np


def main():
    # while True:
    #     try:
    #         numbers = [int(input(f'Number {num+1}:')) for num in range(6)]
    #         target = int(input('and the target:'))
    #         countdownNumbers(numbers, target)
    #     except ValueError:
    #         print("Only input numbers")


    sol = Solution()
    # print(f'num: 123 target: 6 result: {sol.addOperators("123", 6)}')
    # print(f'num: 232 target: 8 result: {sol.addOperators("232", 8)}')
    # print(f'num: 105 target: 5 result: {sol.addOperators("105", 5)}')
    # print(f'num: 000  target: 0 result: {sol.addOperators("000", 0)}')
    # print(f'num: 3456237490  target: 9191 result: {sol.addOperators("3456237490", 9191)}')
    # print(f'num: 123 target: 6 result: {CountdownNumbers([1,2,3], 6)}')
    # print(f'num: 232 target: 8 result: {InOrderNumbers([4,2,2], 8)}')
    solutions = CountdownNumbers([50, 100, 10, 1, 3, 9], 602)
    # print(f'num: 105 target: 5 result: {countdownNumbers("105", 5)}')
    # print(f'num: 000  target: 0 result: {countdownNumbers("000", 0)}')
    # print(f'num: 3456237490  target: 9191 result: {sol.addOperators("3456237490", 9191)}')


def profile_main():
    """
    Profile the main function
    Creates a profile of timing stats into .prof file
    snakeviz ./time_profile.prof
    in terminal to view icicle chart
    :return: None
    """
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename='time_profile.prof')


if __name__ == '__main__':
    profile_main()
