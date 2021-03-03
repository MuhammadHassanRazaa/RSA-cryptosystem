"""Extended Eucleadian Algorithm to find inverse of Number.

:param int: 1st Number.
:param int: 2nd Number.

:returns: tuple [d, a, b] such that d = extended_eucleadian(p, q), ap + bq = d
:rtype: tuple<int>
"""


def extended_eucleadian(p, q):
    if p == 0:
        return q, 0, 1
    else:
        gcd, x, y = extended_eucleadian(q % p, p)
        return gcd, y - (q // p) * x, x


"""The fast modular exponentiation algorithm.

:param int: 1st Number (base)
:param int: 2nd Number (exponenet)
:param int: 3rd Number (number with which mod to be taken)

:returns: Modular Exponentiation (A^B mod C)
:rtype: int
"""


def modular_exponentiation(a, b, c):
    return pow(a, b, c)


"""Chinese Remainder Theorem.

It will calculate minimum positive number x such that numbers and remainders are given by using following formula:
x =  ( ∑ (remainder[i]*pp[i]*Modular_Multiplictive_Inverse[i]) ) % product_of_all_numbers
   Where 0 <= i <= n-1 and 
   pp[i] is product of all divided by num[i]

:param list<int>: numbers
:param list<int>: remainders

:returns: x  =  ( ∑ (remainder[i]*pp[i]*Modular_Multiplictive_Inverse[i]) ) % product_of_all_numbers
:rtype: int
"""


def chineese_remainer(numbers, remainders):
    from math import prod
    product = prod(numbers)

    result = 0
    for index, number in enumerate(numbers):
        pp = product // number
        inverse = extended_eucleadian(pp, number)[1]
        if inverse < 0:
            inverse += number
        result += remainders[index] * inverse * pp

    return result % product


def main():
    print('Library for RSA cryptopsystem')

###########################################################


if __name__ == '__main__':
    main()
