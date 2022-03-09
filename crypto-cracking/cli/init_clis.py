from audioop import mul
from time import sleep
from unicodedata import name
from cli import ClientRSA
import argparse
from ipaddress import ip_address
import signal, multiprocessing, threading
from debugger import Debugger
from queue import Queue

d = Debugger(True)

# TODO: refactor with init_servs.py
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
            p.terminate()
        
        d.info("Exiting main")
        exit()

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    running = True

    def get_input(out: Queue):
        """Handles user input in a separate thread to prevent blocking

        Parameters
        ----------
        out : Queue
            Queue to write the input result to, so it can be parsed in main
        """
        while running:
            d.info("Type \"q\" to quit the program")
            try:
                user_input = input()
            except EOFError as e:
                d.err(f"{e}. Could not read input")
            else:
                out.put(user_input)
    
    out = Queue()
    input_thread = threading.Thread(target=get_input, name="get_input", args=(out,))
    input_thread.start()

    live_procs = procs.copy()
    while running:
        live_procs = list(filter(lambda proc: proc.is_alive(), live_procs))
        # d.debug(live_procs)
        running = len(live_procs) != 0
        if out.qsize() > 0:
            if out.get() == "q":
                running = False
            else:
                d.warn("Ignoring input")

        sleep(0.01)

    cleanup()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--host", type=ip_address, default=ip_address("127.0.0.1"))
    args = p.parse_args()
    
    main(str(args.host))