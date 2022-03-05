from socket import socket, AF_INET, SOCK_STREAM
import argparse
from ipaddress import ip_address
from time import sleep
import signal
from random import randrange

from sympy import re

# serv = ("10.0.0.115", 0x666c)
flag = 1

def main(host: str, port: int):
    print("Starting client")

    # connect to server
    serv_sock = socket(AF_INET, SOCK_STREAM)
    result = serv_sock.connect_ex((host, port))

    def cleanup(*args):
        serv_sock.close()
        print("\nExiting cli")
        exit(0)
    
    if result != 0:
        print(f"Err: Port {port} on {host} not open")
        cleanup()


    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    while True:
        # get the pub key
        sleep(randrange(10, 20))
        serv_sock.send(b"KEY")

        msg = serv_sock.recv(1024)
        mod = int.from_bytes(msg, "little")
        print(f"mod: {mod}")
        msg = serv_sock.recv(1024)
        pub_exponent = int.from_bytes(msg, "little")
        print(f"e: {pub_exponent}")

        # send messages to server
        serv_sock.send((flag**pub_exponent % mod).to_bytes(1024, "little"))
        print(f"sent {flag**pub_exponent % mod}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--host", type=ip_address, default=ip_address("127.0.0.1"))
    p.add_argument("--port", type=int, default=0x666c)
    args = p.parse_args()
    
    main(str(args.host), args.port)