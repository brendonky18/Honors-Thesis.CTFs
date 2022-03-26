from distutils.log import warn
import string
import argparse
from random import SystemRandom as SRand, randrange
from random import shuffle
from functools import *
from parse import *
from typing import *
from math import log, ceil, floor
# Listed in order of ascii value
char_set = string.digits + string.ascii_uppercase + string.ascii_lowercase
# char_set = string.ascii_letters #+ string.digits
bin_char_set = bytes(char_set, "ascii")
KEY_LEN = 10
MIN_VAL = bin_char_set[0]
MAX_VAL = bin_char_set[-1]
AVG_VAL = sum(bin_char_set) / len(bin_char_set)
MAGIC = round(AVG_VAL * KEY_LEN)

FINAL_KEY = 3 # the key number corresponding to the last key in the challenge
START_PASS = "start_here" # the password for the first user

def _calc_offset(keynum: int) -> int:
    """
        Calculates how much the magic number should be offset by, 
        based on the key number provided

        Parameters
        ----------
        keynum : int
            the key's number, must be greater than 0

        Returns
        -------
        int
            offset value
    """

    if keynum == 0:
        raise ValueError("Key number 0 is special, you should not need to get the offset")
    if keynum < 0:
        raise ValueError("Key number cannot be negative")

    offset = keynum // 2
    if not keynum % 2:
        offset *= -1
    return offset

def gen(keynum:int=FINAL_KEY) -> str:
    """
        Generates a random 10-byte key 
        - Each key can easily be validates
        - Each key is associated with a 'key number', each can only be validated with the same key number

        Parameters
        ----------
        keynum : int, optional
            The number corresponding to the key being generated, by default FINAL_KEY

        Returns
        -------
        str
            the raw key
    """

    if keynum == 0:
        return START_PASS

    # gets 8 random ascii chars, at least 1 of which is a digit
    key_base = bytes("".join(SRand().choice(char_set) for i in range(KEY_LEN - 2)), "ascii")

    # splits key in half
    mid = len(key_base) // 2
    val1 = sum(key_base[:mid])
    val2 = sum(key_base[mid:])

    # gets two more ascii chars such that the key will always sum to the correct target
    target = (MAGIC + _calc_offset(keynum))/2
    key1 = floor(target - val1)
    key2 = ceil(target - val2)
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
    return gen(keynum)

def check(key:Union[str, bytes, bytearray, int], keynum:int=FINAL_KEY) -> bool:
    """
        Check if the passed key is valid for the given key number

        Parameters
        ----------
        key : str | bytes | bytearray | int
            the key to be validated
        keynum : int, optional
            the corresponding key number, by default FINAL_KEY

        Returns
        -------
        bool
            True if the key is valid

        Raises
        ------
        ValueError
            if the key argument is not the correct type
    """

    # handle formatting
    # convert to string for parsing
    if isinstance(key, int):
        key_len = ceil(log(key, 256))
        key = key.to_bytes(key_len, "big")
    
    if isinstance(key, bytes) or isinstance(key, bytearray):
        key = key.decode()

    # Generally not pythonic a la "ask for forgiveness..."
    # Screw that
    if not isinstance(key, str):
        raise ValueError(f"arg 'key' is invalid type '{type(key)}'")

    # Parse string to isolate the raw flag
    parsed = parse("flag{{{}}}", key)
    if parsed is not None:
        key = parsed[0]

    # raw key is now isolated as a string
    key = key.encode()

    # Validate key
    # check that each char is a valid value
    for char in key:
        if char not in bin_char_set:
            return False
    # check that it sums to the correct value
    target = MAGIC + _calc_offset(keynum)
    # print(f"keynum: {keynum}")
    # print(f"offset: {_calc_offset(keynum)}")
    # print(f"key: {key}")
    # print(f"sum: {sum(key)}")
    # print(f"target: {target}")
    return sum(key) == target

# tests if key generator is correct
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("-u", dest="user_num", type=int)
    g = p.add_mutually_exclusive_group()
    g.add_argument('-c', dest="check",                         help="run the script in key checking mode")
    g.add_argument('-g', dest="generate", action="store_true", help="run the script in key generation mode")
    g.add_argument('-t', dest="test",     action="store_true", help="run the script in testing mode")

    args = p.parse_args()

    if args.generate:
        if args.user_num is None:
            p.error("-u must be specified when using -g")
        print(f"user{args.user_num}:{gen(args.user_num)}", end="")
    elif args.check is not None:
        if args.user_num is None:
            p.error("-u must be specified when using -c")
        print(f"Valid key: {check(args.check, args.user_num)}")
    else:
        # Run key gen and key check test
        key = gen()
        print(key)
        print(check(key))

        print("Testing 10000 keys:")
        keys = ""
        for i in range(10000):
            kn = randrange(1, 10)
            k = gen(kn)
            keys += k
            if not check(k, kn):
                print("invalid key")
                print(k)
                break

        print("Incorrect chars: ")
        print(len(list(filter(lambda val: val not in char_set, keys))))
 
        print("all keys valid")

    exit()