from socket import socket, AF_INET, SOCK_STREAM
import argparse
from ipaddress import ip_address
from time import sleep
import signal
from random import randrange
from threading import current_thread
from sympy import re
from debugger import Debugger


# serv = ("10.0.0.115", 0x666c)
flag = 1

class ClientRSA:
    host: str
    port: int

    def __init__(self, host: str, port: int):
        """Initializes and runs the client

        Parameters
        ----------
        host : str
            IP address of the server
        port : int
            Port to connect to
        """

        _d = Debugger(True, current_thread().name)
        _d.printf(f"Initializing client")

        self.host = host
        self.port = port


        # connect to server
        serv_sock = socket(AF_INET, SOCK_STREAM)
        result = serv_sock.connect_ex((self.host, self.port))

        def cleanup(*args):
            serv_sock.close()
            _d.printf(f"Exiting cli")
            exit(0)
        
        if result != 0:
            _d.printf(f"Err: Port {self.port} on {self.host} not open")
            cleanup()


        signal.signal(signal.SIGINT, cleanup)
        signal.signal(signal.SIGTERM, cleanup)

        _d.ok(f"Starting client")
        while True:
            # get the pub key
            sleep(randrange(5, 10))
            serv_sock.send(b"KEY")
            try: 
                msg = serv_sock.recv(1024)

                if not msg:
                    _d.warn(f"Connection was closed")
                    exit(-1)
                else:
                    mod = int.from_bytes(msg, "little")
                    _d.info(f"mod: {mod}")
                    msg = serv_sock.recv(1024)
                    pub_exponent = int.from_bytes(msg, "little")
                    _d.info(f"e: {pub_exponent}")
            except Exception as e:
                _d.err(e)
                exit(-2)

            # send messages to server
            serv_sock.send((flag**pub_exponent % mod).to_bytes(1024, "little"))
            _d.printf(f"Sent {flag**pub_exponent % mod}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--host", type=ip_address, default=ip_address("127.0.0.1"))
    p.add_argument("--port", type=int, default=0x666c)
    args = p.parse_args()
    
    ClientRSA(str(args.host), args.port).run()