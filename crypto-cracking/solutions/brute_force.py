import sympy
import functools
from math import isqrt, sqrt

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

# n = sympy.randprime(2**1, 2**8)


def check_prime(self, i):
    for p in primes:
        if i % p == 0:
            primes.append(p)
            return True
    return False


def solve(n: int):
    factors = range(5, isqrt(n) + 1, 6)
    filtered = functools.reduce(check_prime, factors)
    

