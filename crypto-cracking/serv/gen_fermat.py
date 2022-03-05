from random import randrange
import sympy
import serv
import argparse

def generate():
    """Generate two large prime numbers, 
    that are close to eachother,
    such that when multiplied, they can easily be found using fermat's factorization

    Returns
    -------
    int, int, int
        ints corresponding to p, q, and e
    """
    print("gen_fermat")
    e = 65537

    base = randrange(2**1023, 2**1024)
    p = base - 1000
    invalid = True
    while invalid:
        p = sympy.nextprime(p)
        invalid = (p-1) % e == 0

    q = p
    for i in range(3, randrange(3, 10)):
        q = sympy.nextprime(q)

    invalid = True
    while invalid:
        q = sympy.nextprime(q)
        invalid = (q-1) % e == 0
    
    return p, q, 65537

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=0x666c)
    args = generate()
    print(args)
    serv.main(*args, p.parse_args().port)