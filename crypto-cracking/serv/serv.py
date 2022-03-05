from random import randrange
import threading
import RSA
import sympy
import argparse
import signal
from socket import socket, AF_INET, SOCK_STREAM


timeout = 300 # 5 minutes
key_msg = b"KEY"

def main(p: int, q: int, e: int, listen_port: int):
    print("Starting server")

    global pub_key
    global priv_key
    pub_key, priv_key = RSA.calc_keys(p, q, e)
    # print(f"keygen complete {pub_key} {priv_key}")

    threads = []

    listen_sock = socket(AF_INET, SOCK_STREAM)
    listen_sock.bind(("0.0.0.0", listen_port))

    def cleanup(*args):
        for t in threads: 
            t.join()
        
        listen_sock.close()
        
        print("\nExiting serv")
        exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    print("Listening")
    listen_sock.listen()

    while True:
        cli, addr = listen_sock.accept()
        print("New connection")
        # print("client connected")
        cli.settimeout(timeout)

        cli_thread = threading.Thread(target=handle_connection, args=(cli, addr))
        threads.append(cli_thread)
        print("thread ready")
        cli_thread.start()
    
def handle_connection(cli, addr):
    print("Handle connection")

    buf = 1024

    while True:
        try:
            msg = cli.recv(buf)
            # print(f"msg: {msg}")
            # print(msg == key_msg)
            if not msg:
                raise Exception('Client disconnected')
            elif msg == key_msg:
                # print("sending key")
                cli.send(pub_key[0].to_bytes(1024, "little"))
                # print("sent n")
                cli.send(pub_key[1].to_bytes(1024, "little"))
                # print("sent e")
            else:
                # print("decoding")
                # theoretically we would decrypt the messages here, but the server doesn't actually do anything with them
                print(f"Decoded message: {int.from_bytes(msg, 'little')**priv_key[1] % priv_key[0]}")
        except Exception as e:
            print(e)
            cli.close()
            return

if __name__ == "__main__":
    # get RSA key-gen variables
    p = argparse.ArgumentParser()
    p.add_argument('-p', type=int, default=sympy.randprime(2**1, 2**8))
    p.add_argument('-q', type=int, default=sympy.randprime(2**1, 2**8))
    p.add_argument('-e', type=int)
    p.add_argument("--port", type=int, default=0x666c)
    args = p.parse_args()
    # print("got args")
    
    # default public exponent
    e = 65567
    if not args.e:
        phi = (args.p-1)*(args.q-1)
        # print(phi % e)
        while (phi % e) == 0:
            e = randrange(1, phi)
    else:
        e = args.e
    # print("main")
    main(args.p, args.q, e, args.port)