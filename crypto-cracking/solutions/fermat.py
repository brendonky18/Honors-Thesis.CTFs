import argparse
from math import ceil, isqrt, log

def solve(n: int):
    a = isqrt(n) + 1
    while a <= n and b**2 != b_sqr:
        b_sqr = a**2 - n
        b = isqrt(b_sqr)
        a += 1
            
    return (a+b, a-b)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("encrypted", type=int)
    p.add_argument("e", type=int)
    args = p.parse_args()

    decrypted = log(args.e, args.encrypted)

    print(f"Decoded: {int.to_bytes(decrypted, ceil(decrypted.bit_size() / 8), 'big')}")
