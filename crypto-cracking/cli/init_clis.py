from unicodedata import name
import cli
import argparse
from ipaddress import ip_address
import signal, multiprocessing

def main(host: str):
    # TODO: randomly generate ports and send to server
    port = 0x666c, 0x666d, 0x666e
    
    procs = [
        multiprocessing.Process(target=cli.main, args=(host, port[0]), name="cli1"),
        # multiprocessing.Process(target=cli.main, args=(host, port[1]), name="cli2"),
        # multiprocessing.Process(target=cli.main, args=(host, port[2]), name="cli3")
    ]

    for p in procs:
        print("Spawning client process")
        p.start()
    print("All clients spawned")

    def cleanup(*args):
        for p in procs: 
            p.join()
        
        print("\nExiting main")
        exit()

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--host", type=ip_address, default=ip_address("127.0.0.1"))
    args = p.parse_args()
    
    main(str(args.host))