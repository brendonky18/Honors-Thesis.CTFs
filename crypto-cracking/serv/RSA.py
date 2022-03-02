from typing import Tuple


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def calc_keys(p: int, q: int, e: int) -> Tuple[Tuple[int, int], Tuple[int, int]]: 
    """generates the RSA public and private keys given the variables p, q and e

    Parameters
    ----------
    p : int
    q : int
    e : int
        the public exponent, checked for coprimality

    Returns
    -------
    ((int, int), (int, int))
        two tuples corresponding to the public and private keys respectively in the form of ((n, e), (n, d))
    """    
    
    n = p * q

    phi = (p - 1) * (q - 1)

    if phi % e == 0:
        raise Exception("Public exponent invalid, must be coprime with phi")

    d = pow(e, -1, phi)

    return (n, e), (n, d)