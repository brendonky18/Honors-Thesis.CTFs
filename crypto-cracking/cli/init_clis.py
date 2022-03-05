from unicodedata import name
from cli import ClientRSA
import argparse
from ipaddress import ip_address
import signal, multiprocessing
from debugger import Debugger

d = Debugger(True)


def main(host: str):
    # TODO: randomly generate ports and send to server
    port = 0x666c, 0x666d, 0x666e
    
    procs = [
        multiprocessing.Process(target=ClientRSA, args=(host, port[0]), name="cli1"),
        multiprocessing.Process(target=ClientRSA, args=(host, port[1]), name="cli2"),
        multiprocessing.Process(target=ClientRSA, args=(host, port[2]), name="cli3")
    ]

    for p in procs:
        d.info("Spawning client process")
        p.start()
    d.info("All clients spawned")

    def cleanup(*args):
        for p in procs: 
            p.join()
        
        d.info("Exiting main")
        exit()

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    while True:
        d.info("Type \"q\" to quit the program")
        val = input()
        if val == "q":
            cleanup()
        else:
            d.warn("Ignoring input")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--host", type=ip_address, default=ip_address("127.0.0.1"))
    args = p.parse_args()
    
    main(str(args.host))