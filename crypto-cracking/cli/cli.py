from math import ceil, floor, log
from socket import socket, AF_INET, SOCK_STREAM
import argparse
from ipaddress import ip_address
from time import sleep
import signal
from random import randint, randrange
from os import urandom
from multiprocessing import current_process
from sympy import re
from debugger import Debugger

# serv = ("10.0.0.115", 0x666c)
# flag = 1
class ClientRSA:
    host: str
    port: int

    def __init__(self, host: str, port: int, conn_attempts: int = 3, conn_wait: float = 5, flag: int=1):
        """Initializes and runs the client

        Parameters
        ----------
        host : str
            IP address of the server
        port : int
            Port to connect to
        conn_attempts : int, optional
            The number of times to attempt to connect to the server
        conn_wait : float, optional
            The amount, in seconds, to wait between connection attempts
        """
        if conn_attempts < 1:
            raise ValueError("conn_attempts cannot be less than 1")

        _d = Debugger(False, current_process().name)
        _d.printf(f"Initializing client")

        self.host = host
        self.port = port


        # connect to server
        serv_sock = socket(AF_INET, SOCK_STREAM)

        def cleanup(*args):
            serv_sock.close()
            _d.printf(f"Exiting cli")
            exit(0)

        sleep(3)

        num_attempts = 0
        while conn_attempts > num_attempts:
            result = serv_sock.connect_ex((self.host, self.port))
            if result != 0:
                _d.warn(f"Port {self.host}:{self.port} not open. Will try again in {conn_wait} second{'s' if conn_wait > 1 else ''}")
            else:
                _d.ok(f"Connected to {self.host}:{self.port}")
                break

            num_attempts += 1
            sleep(conn_wait)

        if result != 0:
            _d.err(f"Port {self.host}:{self.port} not open. Unable to establish connection after {conn_attempts} attempts")
            cleanup()

        signal.signal(signal.SIGINT, cleanup)
        signal.signal(signal.SIGTERM, cleanup)

        _d.ok(f"Starting client")
        while True:
            # get the pub key
            sleep(randrange(5, 10))
            serv_sock.send(b"RSA_KEY:")
            try: 
                msg = serv_sock.recv(1024)

                if not msg:
                    _d.warn(f"Connection was closed")
                    exit(-1)
                else:
                    mod = int.from_bytes(msg, "big")
                    _d.info(f"mod: {mod}")
                    msg = serv_sock.recv(1024)
                    pub_exponent = int.from_bytes(msg, "big")
                    _d.info(f"e: {pub_exponent}")
            except OSError as e:
                _d.err(e)
                exit(-2)

            # Length of the flag in bytes
            FLAG_LEN = 16
            # calculate how many bytes can fit
            max_bytes = floor(log(mod, 256))
            _d.debug(f"max bytes {max_bytes}")
            key_byte_len = 1
            if max_bytes < 1:
                raise Exception(f"Length of key cannot be less than 1 byte. n={mod}, e={e}")
            else:
                key_byte_len = 2**(max_bytes - 1).bit_length()
            
            # calculate a key that will fit
            while key_byte_len > max_bytes:
                key_byte_len = key_byte_len // 2

            _d.debug(f"Key length={key_byte_len}")
            if key_byte_len < 4:
                _d.warn("Key lengths less than 4 are trivial to determine due to the flag's format")

            symm_key = 0
            for b in range(key_byte_len * 8):
                symm_key <<=1 
                symm_key |= randint(0, 1)

            # send symm key to server
            encrypted_symm_key = pow(symm_key, pub_exponent, mod)
            payload = b"XOR_KEY:" + encrypted_symm_key.to_bytes(512, "big")
            _d.debug(f"Symmetric key {hex(symm_key)}")
            _d.debug(f"Encrypted symmetric key {hex(encrypted_symm_key)}")

            # send key length
            payload += b"KEY_LEN:" + int.to_bytes(key_byte_len, 10, "big")
            _d.debug(f"Key len {key_byte_len}")

            # generate salt
            salt = randint(0,1)
            for i in range(FLAG_LEN):
                salt <<= 1
                salt |= randint(0,1)

            salted_flag = (salt << (14 * 8)) | flag

            # encrypt flag
            while key_byte_len < FLAG_LEN:
                symm_key = symm_key << (key_byte_len * 8) | symm_key
                key_byte_len *= 2

            encrypted_flag = symm_key ^ salted_flag
            encrypted_flag &= 0xffffffffffffffffffffffffffffffff
            _d.debug(f"Encrypted flag {hex(encrypted_flag)}")
            payload += b"FLAG:" + int.to_bytes(encrypted_flag, 16, "big")
            serv_sock.send(payload)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--host", type=ip_address, default=ip_address("127.0.0.1"))
    p.add_argument("--port", type=int, default=0x666c)
    p.add_argument("--flag", type=int, default=1)
    args = p.parse_args()
    
    ClientRSA(str(args.host), args.port, args.flag).run()