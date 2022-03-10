import string
from random import SystemRandom as SRand
from random import shuffle
from functools import *
MAX_VAL = 122
MIN_VAL = 48
AVG_VAL = 87
MAGIC = 696

char_set = string.ascii_letters + string.digits
bin_char_set = bytes(char_set, "ascii")

def gen() -> str:
    """Generates a random 8-byte key which can easily be validated for correctness

    Returns
    -------
    str
        the key that was generated
    """

    # gets 6 random ascii chars, at least 1 of which is a digit
    key_base = bytes("".join(SRand().choice(char_set) for i in range(5)), "ascii") + bytes(SRand().choice(string.digits), "ascii")

    # splits key in half
    val1 = sum(key_base[:3])
    val2 = sum(key_base[3:])

    # gets two more ascii chars such that the key will always sum to MAGIC
    key1 = MAGIC//2 - val1
    key2 = MAGIC//2 - val2
    if val1 > val2:
        lo_key = key1
        hi_key = key2
    else:
        lo_key = key2
        hi_key = key1

    # ensures that our chars are within the specified char set
    while MIN_VAL < lo_key and hi_key < MAX_VAL:
        if lo_key in bin_char_set and hi_key in bin_char_set:
            key_ba = bytearray(key_base + lo_key.to_bytes(1, "little") + hi_key.to_bytes(1, "little"))
            shuffle(key_ba)
            return key_ba.decode("ascii")
        else:
            lo_key -= 1
            hi_key += 1

    # bad set of starting chars, try again
    return gen()

def validate(key) -> bool:
    """Check if the passed key is valid
    - A key is valid if all the bytes in the key sum to the magic number

    Parameters
    ----------
    key : str, bytes, or bytearray
        the key to be validated

    Returns
    -------
    bool
        True if the key is valid

    Raises
    ------
    ValueError
        if the key argument is not the correct type
    """

    if type(key) is str:
        key = bytes(key, "ascii")
    elif type(key) is bytearray:
        key = bytes(key)

    # Generally not pythonic a la "ask for forgiveness..."
    # Screw that
    if isinstance(key, bytes):
        raise ValueError(f"arg key must be 'bytes', passed arg is type {type(key)}")
    else:
        return sum(key) == MAGIC

# tests if key generator is correct
if __name__ == "__main__":
    key = gen()
    print(key)
    print(validate(key))

    print("test 10000:")
    keys = ""
    valid = True
    for i in range(10000):
        k = gen()
        keys += k
        valid &= validate(k)
        if not valid:
            print("invalid key")
            print(k)
            validate(k)
            break


    print("Incorrect chars: ")
    print(len(list(filter(lambda val: val not in char_set, keys))))

    if valid:        
        print("all keys valid")
