from math import ceil, floor, log
from socket import socket, AF_INET, SOCK_STREAM
import argparse
from ipaddress import ip_address
from sre_parse import FLAGS
from time import sleep
import signal
from random import randint, randrange
from os import urandom
from multiprocessing import current_process
from sympy import re
from debugger import Debugger
import json

class ClientRSA:
    host: str
    port: int

    MSG_TYPE = "MSG_TYPE"
    ASYM_KEY_MSG = "RSA_KEY"
    SECRET_FLAG = "SECRET_FLAG"
    DATA = "DATA"

    SYM_KEY_MSG = "XOR_KEY"
    MOD = "N"
    EXP = "E"
    KEY_LEN_MSG = "KEY_LEN"
    FLAG_LEN_MSG = "FLAG_LEN"
    ENC_FLAG_MSG  = "ENC_FLAG"

    def __init__(self, host: str, port: int, conn_attempts: int = 3, conn_wait: float = 5, flag: int=1, verbose: bool=False, small_key=False):
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

        _d = Debugger(verbose, current_process().name)
        _d.printf(f"Initializing client")

        self.host = host
        self.port = port


        # connect to server
        serv_sock = socket(AF_INET, SOCK_STREAM)

        def cleanup(*args, exit_code=0):
            serv_sock.close()
            _d.printf(f"Exiting cli")
            exit(exit_code)

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
            msg = json.dumps({
                self.MSG_TYPE: self.ASYM_KEY_MSG
            })
            msg = msg.encode("ascii")
            _d.debug(f"Sent {msg}")
            serv_sock.send(msg)
            try: 
                msg = serv_sock.recv(1024)
                _d.debug(f"recieved {msg}")

                if not msg:
                    _d.warn(f"Connection was closed")
                    exit(-1)
                elif isinstance(msg, bytes) and isinstance(msg:=json.loads(msg), dict):
                    data = msg[self.DATA]
                    mod = data[self.MOD]
                    _d.info(f"mod: {mod}")
                    pub_exponent = data[self.EXP]
                    _d.info(f"e: {pub_exponent}")
                    _d.debug("what")
                else:
                    _d.err(f"Unknown message type {msg}")
                    raise RuntimeError(f"Unknown message {msg}")
                _d.debug("No errors yet")
            except OSError as e:
                _d.err(e)
                cleanup(-2)
            except ValueError as e:
                _d.err(e)
                cleanup(-3)
            except RuntimeError as e:
                _d.err(e)
                cleanup(-4)

            _d.debug("Message recieved")

            # Length of the flag in bytes
            FLAG_LEN = 0x10
            FULL_LEN = 0x20
            SALT_LEN = FULL_LEN - FLAG_LEN
            # calculate how many bytes can fit
            if small_key:
                _d.debug("Small key")
                a_max_bytes = floor(log(mod**(1/e), 256))
            else:
                _d.debug("Normal key")
                a_max_bytes = floor(log(mod, 256))
            _d.debug(f"max bytes {a_max_bytes}")
            key_len = 1
            if a_max_bytes < 1:
                raise Exception(f"Length of key cannot be less than 1 byte. n={mod}, e={pub_exponent}")
            elif a_max_bytes > 1:
                key_len = 2**(a_max_bytes - 1).bit_length()
            
            # calculate a key that will fit
            while key_len > a_max_bytes:
                key_len = key_len // 2

            _d.debug(f"Asym key length={key_len}")
            if key_len < 4:
                _d.warn("Key lengths less than 4 are trivial to determine due to the flag's format")

            symm_key = 0
            for b in range(key_len * 8):
                symm_key <<=1 
                symm_key |= randint(0, 1)


            # generate salt
            salt = randint(0,1)
            for i in range(SALT_LEN * 8):
                salt <<= 1
                salt |= randint(0,1)

            salted_flag = (salt << (FLAG_LEN * 8)) | flag
            # salted_flag = flag
            encrypted_symm_key = pow(symm_key, pub_exponent, mod)

            _d.debug(f"Symmetric key {symm_key}")

            # Concatenate the symmetric key so it's long enough to encrypt the whole flag
            i = key_len
            while i < FULL_LEN:
                symm_key = symm_key << (i * 8) | symm_key
                i *= 2

            _d.debug(f"Padded sym key {symm_key}")

            # Encrypt the flag w/ the symmetric key, and the truncate it to the apprioate length
            encrypted_flag = symm_key ^ salted_flag & 2**(FULL_LEN * 8) - 1
            _d.debug(f"salted flag {salted_flag}")
            _d.debug(f"Encrypted flag {encrypted_flag}")
            # payload = b"XOR_KEY:" + encrypted_symm_key.to_bytes(512, "big")
            # payload += b"KEY_LEN:" + int.to_bytes(key_byte_len, 10, "big")
            # payload += b"FLAG:" + int.to_bytes(encrypted_flag, 16, "big")
            # send symm key info to server
            _d.debug(f"Encrypted symmetric key {encrypted_symm_key}")
            _d.debug(f"Asym key len {key_len}")
            payload = json.dumps({
                self.MSG_TYPE: self.SECRET_FLAG,
                self.DATA: {
                    self.SYM_KEY_MSG: encrypted_symm_key,
                    self.KEY_LEN_MSG: key_len,
                    self.FLAG_LEN_MSG: FLAG_LEN,
                    self.ENC_FLAG_MSG: encrypted_flag
                }
            })
            payload_msg = payload.encode("ascii")
            serv_sock.send(payload_msg)
            _d.debug(f"Sent {payload_msg}")



if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--host", type=ip_address, default=ip_address("127.0.0.1"))
    p.add_argument("--port", type=int, default=0x666c)
    p.add_argument("--flag", type=int, default=1)
    p.add_argument("-v", default=False, action="store_true")
    args = p.parse_args()
    
    ClientRSA(str(args.host), args.port, flag=args.flag, verbose=args.v).run()