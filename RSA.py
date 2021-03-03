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
"""Generating multiplicative inverse of given numbers (a,b modulo n)
:param int: first number
:param int 2nd number
:param int: module operation number

:returns: multiplicative Inverse of two numbers
:rtpe:int
"""
def multiplicativeInverse(a, b, n):
    
    d, x, y = extended_eucleadian(a, n)
    if b % d == 0:
        temp_x = (x * (b/d)) % n
        result = []
        for i in range(d):
            result.append((temp_x + i*(n/d)) % n)
        return result
    return []

"""The fast modular exponentiation algorithm.

:param int: 1st Number (base)
:param int: 2nd Number (exponenet)
:param int: 3rd Number (number with which mod to be taken)

:returns: Modular Exponentiation (A^B mod C)
:rtype: int
"""


def modular_exponentiation(a, b, c):
    return pow(a,b,c)


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


def miller_rabin(n, k=5):
    from random import randrange
    if (n <= 1 or n == 4):
        return False
    if (n <= 3):
        return True
    if n % 2 == 0:
        return False

    r, s = 0, n - 1

    while s % 2 == 0:  # findng r such that 2^s * r + 1 for some r >= 1
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


"""Get Big Random Prime Number
This method calcualte a random number of specified length and then using
miller rabin method check if primilarity.

:param int: Number of bits of the prime Number
:returns: Big Prime Number
:rtpe: int
"""


def getBigRandomPrime(b):
    from random import getrandbits

    while True:
        p = getrandbits(b)
        if miller_rabin(p):
            return p


def generate_keys():


    p = getBigRandomPrime(20)
    q = getBigRandomPrime(20)
    print(p,q)
    e = 3
    n = p*q
    
    pi_n = (p-1)*(q-1)

    while not (extended_eucleadian(pi_n,e)[0]==1):
        e=e+1
    d = multiplicativeInverse(e,1,pi_n)[0]

    return n, e, d

def encrypt(keys, message):
    e, n = keys
    result = [str(modular_exponentiation(ord(c), e, n)) for c in message]
    return " ".join(result)

def decrypt(keys, cipher):
    d, n = keys
    result = [chr(modular_exponentiation(c, d, n)) for c in cipher]
    return ''.join(result)

def main():
    from cs50 import get_int, get_string

    def user_input_for_result():
        res = 0
        while True:
            res = get_int(
                "What do you want to do with this:\n1:Print on console\n2:Save to File\nChoose One: ")
            if res not in [1, 2]:
                print("Error!! Please input in Range")
            else:
                break
        return res


    def encryption():
        message = get_string("Enter your message:\n")
        print("Enter Public Key")
        e = get_int("Enter e: ")
        n = get_int("Enter n: ")
       
        cipher = encrypt((e,n),message)
        res = user_input_for_result()
        if res == 1:
            print(cipher)
        else:
            with open("encrypted_message.txt", 'w') as file:
                file.write(cipher)

    def decryption():
        cipher = get_string("Enter the cipher:\n").split(' ')
        cipher = [int(c) for c in cipher]
        print("Enter Private Key")
        d = get_int("Enter d: ")
        n = get_int("Enter n: ")
       
        message = decrypt((d,n),cipher)
        res = user_input_for_result()
        if res == 1:
            print(message)
        else:
            with open("decrypted_message.txt", 'w') as file:
                file.write(message)


    def print_keys(n, e, d):
        res =user_input_for_result()
        if res == 1:
            print("Public Key:\n"+"n ->", str(n) + "\n e ->", str(e))
            print("Private Key:\n" + "d -> ", str(d))
        else:
            with open("public_key.txt", 'w') as file:
                file.write("n -> "+str(n)+"\n e -> "+str(e))
            with open("private_key.txt",'w') as file:
                file.write("d -> "+str(d))

    print("RSA Cryptosystem".center(50))
    inputted_value = 0
    while True:
        inputted_value = get_int(
            "1:Encrypt\n2:Decrypt\n3:GenerateKeys\nChoose one: ")
        if inputted_value not in [1, 2, 3]:
            print("Error!! Please Input in Range:")
        else:
            break

    if inputted_value == 1:
        encryption()
    elif inputted_value == 2:
        decryption()
    else:
        n, e, d = generate_keys()
        print_keys(n, e, d)


###########################################################


if __name__ == '__main__':
    main()
