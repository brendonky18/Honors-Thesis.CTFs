import argparse
from math import isqrt
from os import get_terminal_size

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

def prime_factors(n: int):
    """calculates the prime factorization of a number using the 6+-1 trick

    Parameters
    ----------
    n : int
        The number to get the prime factorization of

    Returns
    -------
    list
        list of prime factors
    """
    factors = [1]

    root = isqrt(n)+1
    width = get_terminal_size()[0] - 1
    count = 0
    print(f"O{'o'*(width)}", end="", flush=True)

    for i in primes:         
        # while i divides n , print i and divide n
        while n % i== 0:
            # print(f" {i}", end="", flush=True)
            factors.append(i),
            n //= i

    p = (root - i) // width
    i1 = ((i//6)+1) * 6 - 1

    while i1 < root:
        while n % i1 == 0:
            # print(f" {i1}", end="", flush=True)
            factors.append(i1),
            n //= i1
        i2 = i1 + 2
        while n % i2 == 0:
            # print(f" {i2}", end="", flush=True)
            factors.append(i2),
            n //= i2
        i1 += 6
        # print loading bar
        if i1 + 1 > count * p:
            count += 1
            print(f"\r{'o' * count}O{'o'*(width-count)}", end="", flush=True)
    
    if n > 2:
        factors.append(n)
             
    print()
    return factors
    
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("number", type=int)
    args = p.parse_args()
    num = args.number
    
    pr = prime_factors(num)
    print(f"Prime factors of {num}:", end="")
    for p in pr:
        print(f" {p}", end="")
        
    print()


