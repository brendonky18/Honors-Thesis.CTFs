from time import sleep
from serv import ServerRSA
import gen_brute_force, gen_small_e, gen_fermat
import signal, multiprocessing, threading
from enum import Enum
from debugger import Debugger
from queue import Queue as TQueue
from multiprocessing import Queue as PQueue
import argparse
 
# TODO: refactor with init_clis.py
def main(verbose: bool=False):
    d = Debugger(verbose)

    # tracks if all the servers have started
    status = PQueue()

    port_base = 0x666c
    key_generators = [
        gen_brute_force,
        gen_small_e,
        gen_fermat
    ]
    procs = []
    d.debug(f"init_servs verbose {verbose}")
    for i in range(len(key_generators)):
        port = port_base + i
        p = multiprocessing.Process(
            target=ServerRSA, 
            args=(key_generators[i].generate, port, status, verbose), 
            # kwargs={"verbose": verbose},
            name=f"proc_{key_generators[i].__name__}"
        )
        procs.append(p)

    for p in procs:
        d.printf(f"Spawning server process \"{p.name}\"")
        p.start()

    d.info("All servers started")

    while status.qsize() < len(procs):
        sleep(0.01)

    d.ok("All servers listening")
    
    def cleanup(*args):
        for p in procs: 
            p.terminate()
        
        d.info("Exiting main")
        exit()

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    running = True

    def get_input(out: TQueue):
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
                break
            else:
                out.put(user_input)
    
    out = TQueue()
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
    p.add_argument("-v", default=False, action="store_true")
    args = p.parse_args()
    main(args.v)