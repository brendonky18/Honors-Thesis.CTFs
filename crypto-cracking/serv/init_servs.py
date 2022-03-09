from time import sleep
from serv import ServerRSA
import gen_brute_force, gen_small_e, gen_fermat
import signal, multiprocessing, threading
from enum import Enum
from debugger import Debugger
from queue import Queue as TQueue
from multiprocessing import Queue as PQueue
 
# TODO: refactor with init_clis.py
def main():
    d = Debugger(True)

    # tracks if all the servers have started
    status = PQueue()

    # TODO: wait for client to send me the ports I should be using
    ports = 0x666c, 0x666d, 0x666e
    procs = [
        multiprocessing.Process(target=ServerRSA, args=(gen_brute_force.generate, ports[0], status), name="brute_force"),
        multiprocessing.Process(target=ServerRSA, args=(gen_small_e.generate,     ports[1], status), name="small_e"),
        multiprocessing.Process(target=ServerRSA, args=(gen_fermat.generate,      ports[2], status), name="fermat")
    ]

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
    main()