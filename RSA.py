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


"""Miller-Rabin Primality Test.

:param int: number to be tested
:param int: Number of iterations to be performed

:returns: A return value of False means n is certainly not prime. A return value of True means n is very likely a prime
:rtype: boolean
"""


def miller_rabin(n, k = 5):
    from random import randrange
    if (n <= 1 or n == 4): 
        return False
    if (n <= 3): 
        return True
    if n % 2 == 0:
        return False

    r, s = 0, n - 1

    while s % 2 == 0: # findng r such that 2^s * r + 1 for some r >= 1 
        r += 1
        s //= 2
    for _ in range(k):
        x = modular_exponentiation(randrange(2, n - 1), s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
             """Keep squaring x while one of the following doesn't happen 
                (i) d does not reach n-1 
                (ii) (x^2) % n is not 1 
                (iii) (x^2) % n is not n-1"""
            x = modular_exponentiation(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def main():
    k = 4

    print("All primes smaller than 100: ")
    for n in range(1, 100):
        if (miller_rabin(n, k)):
            print(n, end=" ")
    print('Library for RSA cryptopsystem')

###########################################################


if __name__ == '__main__':
    main()
