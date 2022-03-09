from random import randrange
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

class ServerRSA:
    _timeout = 300 # 5 minutes
    _threads = []
    _key_gen: Callable
    _listen_port: int
    _pub_key: int
    _priv_key: int

    key_msg = b"KEY"

    def __init__(self, key_generator: Callable, listen_port: int, status: Queue):
        """Initializes and runs the server

        Parameters
        ----------
        key_generator : Callable
            the function to generate the RSA key variables p, q, r
        listen_port : int
            the port to listen for incoming connections on
        """
        _d = Debugger(True, current_process().name)
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

        _d = Debugger(True, current_thread().name)
        _d.printf(f"Handle connection")

        buf = 1024

        while True:
            try:
                msg = cli_sock.recv(buf)

                if not msg:
                    _d.printf('Client disconnected')
                    cli_sock.close()
                    return
                elif msg == self.key_msg:
                    # _d.printf(f"sending key")
                    cli_sock.send(self._pub_key[0].to_bytes(1024, "little"))
                    # _d.printf(f"sent n")
                    cli_sock.send(self._pub_key[1].to_bytes(1024, "little"))
                    # _d.printf(f"sent e")
                else:
                    # _d.printf(f"decoding")
                    # theoretically we would decrypt the messages here, but the server doesn't actually do anything with them
                    _d.ok(f"Decoded message: {int.from_bytes(msg, 'little')**self._priv_key[1] % self._priv_key[0]}")
            except Exception as e:
                _d.printf(e)
                cli_sock.close()
                exit(-2)

if __name__ == "__main__":
    # get RSA key-gen variables
    p = argparse.ArgumentParser()
    p.add_argument('-p', type=int, default=sympy.randprime(2**1, 2**8))
    p.add_argument('-q', type=int, default=sympy.randprime(2**1, 2**8))
    p.add_argument('-e', type=int)
    p.add_argument("--port", type=int, default=0x666c)
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

    ServerRSA(lambda: (args.p, args.q, e), args.port).run()