from time import sleep
from cli import ClientRSA
import argparse
from ipaddress import ip_address
import signal, multiprocessing, threading
from debugger import Debugger
from queue import Queue
import os, sys, ctypes


d = Debugger(True)

# TODO: refactor with init_servs.py
def main(host: str):
    # load GLIBC
    libc = ctypes.CDLL(None)
    syscall = libc.syscall

    # other c constants
    SYS_KCMP = 312
    KCMP_FILE = 0

    # TODO: randomly generate ports and send to server
    port = 0x666c, 0x666d, 0x666e
    
    procs = [
        multiprocessing.Process(target=ClientRSA, args=(host, port[0]), name=f"cli-{port[0]}"),
        multiprocessing.Process(target=ClientRSA, args=(host, port[1]), name=f"cli-{port[1]}"),
        multiprocessing.Process(target=ClientRSA, args=(host, port[2]), name=f"cli-{port[2]}")
    ]

    for p in procs:
        d.info("Spawning client process")
        p.start()
    d.info("All clients spawned")

    def cleanup(signum: int, frame):
        """Signal handler to gracefully close terminate the clients and close their sockets

        Parameters
        ----------
        signum : int
            the signal number from 1 to 15
        frame : frame or None
            the stack frame at the time of execution
        """
        d.debug("cleanup")
        for p in procs: 
            p.terminate()
        d.debug("all procs terminated")
        input_thread.join()
        d.info("Exiting main")
        exit()

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    running = True

    def get_input(out: Queue):
        nonlocal running
        """Handles user input in a separate thread to prevent blocking

        Parameters
        ----------
        out : Queue
            Queue to write the input result to, so it can be parsed in main
        """
        # WARN: do not use sys.stdin.read() will err when set to nonblocking
        # INFO: stdout, stdin, and stderr when opened in a shell all point to the same file descriptor
        # Therefore, setting O_NONBLOCK for any one of these will set it for all of them
        # see: 
        #  - https://stackoverflow.com/questions/19485751/linux-c-why-fcntl-act-on-stdin-will-also-affect-on-stdout-and-stderr
        #  - https://stackoverflow.com/questions/23865898/when-non-blocking-i-o-is-turned-on-for-stdout-is-it-correct-for-the-os-to-turn
        
        # creates a new open file description for stdin, so it can be set to non-blocking separately from stdout
        out_fd = sys.stdout.fileno()
        old_in_fd = sys.stdin.fileno()
        new_in_fd = os.open("/dev/fd/0", os.O_RDONLY | os.O_NONBLOCK)
        sys.stdin = os.fdopen(new_in_fd)
        pid = os.getpid()

        # Calls the syscall kcmp (kernel compare) to check if the new OFDs have been created
        if syscall(SYS_KCMP, pid, pid, KCMP_FILE, old_in_fd, new_in_fd) == 0:
            raise RuntimeError("Could not create new open file description for stdin")
        else:
            d.debug(f"stdout blocking: {os.get_blocking(out_fd)} stdin blocking: {os.get_blocking(new_in_fd)}")

        while running:
            try:
                user_input = sys.stdin.readline(1)
            except EOFError as e:
                d.err(f"{e}. Could not read input")
                break
            except KeyboardInterrupt:
                d.info("done")
                break
            else:
                if user_input == "q":
                    running &= False
                elif user_input != "":
                    d.warn("Ignoring input")
                    d.info("Type \"q\" to quit the program")

            sleep(0.01)
            
    
    out = Queue()
    input_thread = threading.Thread(target=get_input, name="get_input", args=(out,))
    input_thread.start()

    live_procs = procs.copy()
    while running:
        live_procs = list(filter(lambda proc: proc.is_alive(), live_procs))
        # d.debug(live_procs)
        running &= len(live_procs) != 0
        
        sleep(0.01)
    d.debug("All procs ended")
    cleanup()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--host", type=ip_address, default=ip_address("127.0.0.1"))
    args = p.parse_args()
    
    main(str(args.host))

import string
string.ascii_letters