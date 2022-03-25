from random import randrange
from tabnanny import verbose
import threading
import RSA
import sympy
import argparse
import signal
from socket import socket, AF_INET, SOCK_STREAM
from typing import *
from multiprocessing import current_process
from threading import current_thread
from debugger import Debugger
from queue import Queue
import json

class ServerRSA:
    _timeout = 300 # 5 minutes
    _threads = []
    _key_gen: Callable
    _listen_port: int
    _pub_key: int
    _priv_key: int

    MSG_TYPE = "MSG_TYPE"
    ASYM_KEY_MSG = "RSA_KEY"
    ASYM_KEY_ACK = ASYM_KEY_MSG + "_ACK"
    SECRET_FLAG = "SECRET_FLAG"
    DATA = "DATA"

    SYM_KEY_MSG = "XOR_KEY"
    MOD = "N"
    EXP = "E"
    KEY_LEN_MSG = "KEY_LEN"
    FLAG_LEN_MSG = "FLAG_LEN"
    ENC_FLAG_MSG  = "ENC_FLAG"

    def __init__(self, key_generator: Callable, listen_port: int, status: Queue, verbose: bool=False):
        """Initializes and runs the server

        Parameters
        ----------
        key_generator : Callable
            the function to generate the RSA key variables p, q, r
        listen_port : int
            the port to listen for incoming connections on
        """
        _d = Debugger(verbose, current_process().name)
        _d.printf(f"Initializing server")

        self._key_gen = key_generator
        self._listen_port = listen_port

        self._pub_key, self._priv_key = RSA.calc_keys(*self._key_gen())
        # _d.printf(f"keygen complete {pub_key} {priv_key}")

        _d.printf(f"Starting server")

        listen_sock = socket(AF_INET, SOCK_STREAM)
        listen_sock.bind(("0.0.0.0", self._listen_port))

        def cleanup(*args):
            for t in self._threads: 
                t.join()
            
            listen_sock.close()
            
            _d.printf(f"Exiting serv")
            exit(0)

        signal.signal(signal.SIGINT, cleanup)
        signal.signal(signal.SIGTERM, cleanup)

        _d.ok(f"Listening on {self._listen_port}")
        status.put(True)
        listen_sock.listen()

        while True:
            cli_sock, addr = listen_sock.accept()
            _d.printf(f"New connection")
            # _d.printf(f"client connected")
            cli_sock.settimeout(self._timeout)

            try: 
                peer = cli_sock.getpeername()
            except OSError as e:
                # most likely to occur because of an nmap to the port
                peer = ("?.?.?.?", "?")

            cli_thread = threading.Thread(target=self.handle_connection, args=(cli_sock, addr), name=f"Conn {peer[0]}:{peer[1]}")
            self._threads.append(cli_thread)
            _d.printf(f"Thread ready")
            cli_thread.start()
        
    def handle_connection(self, cli_sock, addr):
        """Handles each incoming client connection on a separate thread

        Parameters
        ----------
        cli_sock : socket
            the socket established for the new connection
        addr : string
            the client's ip address
        """

        _d = Debugger(verbose, current_thread().name)
        _d.printf(f"Handle connection")

        buf = 1024

        while True:
            _d.debug("a")
            try:
                msg = cli_sock.recv(buf)
                _d.debug(f"Received {msg}")
                if not msg:
                    _d.printf('Client disconnected')
                    cli_sock.close()
                    return
                elif isinstance(msg, bytes) and isinstance(msg:=json.loads(msg), dict):
                    if msg[self.MSG_TYPE] == self.ASYM_KEY_MSG:
                        _d.debug(f"priv key: {self._priv_key[1]}")
                        payload = json.dumps ({
                            self.MSG_TYPE: self.ASYM_KEY_ACK,
                            self.DATA: {
                                self.MOD: self._pub_key[0],
                                self.EXP: self._pub_key[1]
                            }
                        })
                        cli_sock.send(payload.encode("ascii"))
                        _d.debug(f"sent pub key {payload}")
                    elif msg[self.MSG_TYPE] == self.SECRET_FLAG:
                        data = msg[self.DATA]
                        encrypted_flag = data[self.ENC_FLAG_MSG]
                        key_len = data[self.KEY_LEN_MSG]
                        encrypted_key = data[self.SYM_KEY_MSG]
                        flag_len = data[self.FLAG_LEN_MSG]
                        _d.debug(f"encrypted flag {encrypted_flag}")
                        _d.debug(f"sym key length {key_len}")
                        _d.debug(f"encrypted key {encrypted_key}")

                        _d.debug(f"decoding symmetric key")
                        # Decrypt the semmetric key\
                        symm_key = pow(encrypted_key, self._priv_key[1], self._priv_key[0])
                        _d.debug(f"Symmetric key: {symm_key}")

                        _d.debug(f"Key length: {key_len}")

                        while key_len < flag_len:
                            symm_key = (symm_key << (key_len * 8)) | symm_key
                            key_len *= 2

                        # Decrypt the message
                        flag = (encrypted_flag ^ symm_key) & (2**(flag_len*8) - 1)
                        _d.ok(f"Decoded message: {flag}={int.to_bytes(flag, 16, 'big')}")
                else:
                    raise RuntimeError(f"Unknown message {msg}")
            except OSError as e:
                _d.warn(e)
                cli_sock.close()
                exit(-2)

if __name__ == "__main__":
    # get RSA key-gen variables
    p = argparse.ArgumentParser()
    p.add_argument('-p', type=int, default=sympy.randprime(2**1, 2**8))
    p.add_argument('-q', type=int, default=sympy.randprime(2**1, 2**8))
    p.add_argument('-e', type=int, default=3)
    p.add_argument("--port", type=int, default=0x666c)
    p.add_argument("-v", default=False, action="store_true")
    args = p.parse_args()
    # _d.printf(f"got args")
    
    # default public exponent
    e = 65567
    if not args.e:
        phi = (args.p-1)*(args.q-1)
        # _d.printf(phi % e)
        while (phi % e) == 0:
            e = randrange(1, phi)
    else:
        e = args.e

    ServerRSA(lambda: (args.p, args.q, e), args.port, Queue(), args.v).run()