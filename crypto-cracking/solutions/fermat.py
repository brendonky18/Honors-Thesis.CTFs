from math import isqrt, sqrt


# n = 715225741 * 982451653 # n = p * q

# a^2 - b&2 = n -> (a+b) and (a-b) are factors of n



def solve(n: int):
    a = isqrt(n) + 1
    while a <= n and b**2 != b_sqr:
        b_sqr = a**2 - n
        b = isqrt(b_sqr)
        a += 1
            
    return (a+b, a-b)
