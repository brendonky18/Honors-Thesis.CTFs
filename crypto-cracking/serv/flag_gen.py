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
    key_base = bytes("".join(SRand().choice(char_set) for i in range(5)), "ascii") + bytes(SRand().choice(string.digits), "ascii")

    val1 = sum(key_base[:3])
    val2 = sum(key_base[3:])

    key1 = MAGIC//2 - val1
    key2 = MAGIC//2 - val2

    if val1 > val2:
        lo_key = key1
        hi_key = key2
    else:
        lo_key = key2
        hi_key = key1

    while MIN_VAL < lo_key and hi_key < MAX_VAL:
        if lo_key in bin_char_set and hi_key in bin_char_set:
            key_ba = bytearray(key_base + lo_key.to_bytes(1, "little") + hi_key.to_bytes(1, "little"))
            shuffle(key_ba)
            return key_ba.decode("ascii")

        lo_key -= 1
        hi_key += 1

    return gen()

def validate(key) -> bool:
    if type(key) is str:
        key = bytes(key, "ascii")
    return sum(key) == MAGIC

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
