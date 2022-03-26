import string
import argparse
from random import SystemRandom as SRand
from random import shuffle
from functools import *
# Listed in order of ascii value
char_set = string.digits + string.ascii_uppercase + string.ascii_lowercase
# char_set = string.ascii_letters #+ string.digits
bin_char_set = bytes(char_set, "ascii")
KEY_LEN = 10
MIN_VAL = bin_char_set[0]
MAX_VAL = bin_char_set[-1]
AVG_VAL = sum(bin_char_set) / len(bin_char_set)
MAGIC = round(AVG_VAL * KEY_LEN)


def gen() -> str:
    """Generates a random 8-byte key which can easily be validated for correctness
    Returns
    -------
    str
        the key that was generated
    """

    # # gets 6 random ascii chars, at least 1 of which is a digit
    # key_base = bytes("".join(SRand().choice(char_set) for i in range(5)), "ascii") + bytes(SRand().choice(string.digits), "ascii")
    key_base = bytes("".join(SRand().choice(char_set) for i in range(KEY_LEN - 2)), "ascii") #+ bytes(SRand().choice(string.digits), "ascii")

    # splits key in half
    mid = len(key_base) // 2
    val1 = sum(key_base[:mid])
    val2 = sum(key_base[mid:])

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
            key_ba = bytearray(key_base + lo_key.to_bytes(1, "big") + hi_key.to_bytes(1, "big"))
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
    p = argparse.ArgumentParser()
    p.add_argument("-u", dest="user_num", type=int)
    g = p.add_mutually_exclusive_group()
    g.add_argument('-v', dest="validate",                      help="run the script in key validation mode")
    g.add_argument('-g', dest="generate", action="store_true", help="run the script in key generation mode")
    g.add_argument('-t', dest="test",     action="store_true", help="run the script in testing mode")

    args = p.parse_args()

    if args.generate:
        if args.user_num is None:
            p.error("-u must be specified when using -g")
        elif args.user_num == 0:
            pswd = "start_here"
        else:
            pswd = gen()

        print(f"user{args.user_num}:{pswd}", end="")
    elif args.validate is not None:
        exit(validate(args.validate))
    else:
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

    exit()