import sympy
import serv
import argparse
from random import randrange

def generate():
    """Generate two small prime numbers, 
    which if multiplied, can easily be brute-forced to find the original primes

    Returns
    -------
    int, int, int
        ints corresponding to p, q, and e
    """
    e = 3

    
    invalid = True
    while invalid:
        p = sympy.randprime(2**1, 2**32)
        invalid = (p-1) % e == 0
    
    invalid = True
    while invalid:
        q = sympy.randprime(2**31, 2**32)
        invalid = p == q or (q-1) % e == 0

    return p, q, e

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=0x666c)
    args = generate()
    print(args)
    serv.main(*args, p.parse_args().port)