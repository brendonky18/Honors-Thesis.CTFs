import sympy
import serv
import argparse

def hamming_weight(num: int) -> int:
    weight = 0

    while num:
        weight += 1
        num &= num - 1

    return weight


def generate():
    """Generate two large prime numbers, 
    but with a small e such that m < n^(1/e), 
    meaning that c can be reversed by solving m = c^(1/e)

    Returns
    -------
    int, int, int
        ints corresponding to p, q, and e
    """
    print("gen_small_e")
    e = 3

    invalid = True
    while invalid:
        p = sympy.randprime(2**1, 2**1024)
        invalid = (p-1) % e == 0
    
    invalid = True
    while invalid:
        q = sympy.randprime(2**1023, 2**2014)
        invalid = p == q or (q-1) % e == 0 or hamming_weight((p^q) >> 512 < 256)
    
    return p, q, e

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=0x666c)
    args = generate()
    print(args)
    serv.main(*args, p.parse_args().port)