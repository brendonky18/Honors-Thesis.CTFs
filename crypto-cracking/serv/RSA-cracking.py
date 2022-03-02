import base64
from binascii import hexlify, unhexlify
from email.mime import base
from math import isqrt
from typing import Tuple

import RSA

# While the theory behind RSA is widely believed to be impossible to crack, 
# you should know by now that theory does not always translate nicely to reality.
# There are many edge cases under which a lazy or careless implementation makes it possible to crack RSA.

def is_prime(n: int) -> bool:
    # Primality test using 6k+-1 optimization.
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i <= isqrt(n) + 1:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True    

def main(self):

    messages = [int.from_bytes(f"Flag {i}".encode(), "little") for i in range(0, 3)]

    # brute force small primes
    pub_key, priv_key = RSA.calc_keys

    # fermat's factorization

    # shared modulus

    # small public exponent, no padding (coppersmith's attack) 

if __name__ == "__main__" :
    main()
    # print(calc_keys(61, 53, 11))


