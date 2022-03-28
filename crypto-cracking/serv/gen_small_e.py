import sympy
import serv
import argparse
# The largest possible message we will send
MAX_VAL = 136143999223230197147385125158541490813 # ==> the keys must be at least 191 bits long
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
    e = 3

    # e = 3 ==> n < 341 bits
    # otherwise it will be too large to do float arithmetic
    invalid = True
    while invalid:
        p = sympy.randprime(2**31, 2**32)
        invalid = (p-1) % e == 0
    
    invalid = True
    while invalid:
        q = sympy.randprime(2**31, 2**32)
        invalid = p == q or (q-1) % e == 0 #or hamming_weight((p^q) >> 512 < 256)
    
    return p, q, e

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=0x666c)
    args = generate()
    serv.main(*args, p.parse_args().port)