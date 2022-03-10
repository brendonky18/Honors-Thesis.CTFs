from socket import socket, AF_INET, SOCK_STREAM
import argparse
from ipaddress import ip_address
from time import sleep
import signal
from random import randrange
from multiprocessing import current_process
from sympy import re
from debugger import Debugger

# serv = ("10.0.0.115", 0x666c)
flag = 1
class ClientRSA:
    host: str
    port: int

    def __init__(self, host: str, port: int, conn_attempts: int = 3, conn_wait: float = 5):
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

        _d = Debugger(True, current_process().name)
        _d.printf(f"Initializing client")

        self.host = host
        self.port = port


        # connect to server
        serv_sock = socket(AF_INET, SOCK_STREAM)

        def cleanup(*args):
            serv_sock.close()
            _d.printf(f"Exiting cli")
            exit(0)

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